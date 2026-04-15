#!/usr/bin/env python3
"""
将时间线信息与公司评价语录关联
"""

import json
import re
from datetime import datetime

# 读取原始语录数据
with open('wiki/structured/company_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 读取时间线数据
with open('wiki/structured/timeline_raw.json', 'r', encoding='utf-8') as f:
    timeline_data = json.load(f)

blog_timeline = timeline_data['blog']
post_timeline = timeline_data['posts']

# 读取帖子合集（用于提取具体日期）
post_file = 'raw/duanyongping/extracted/段永平帖子合集 (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json'
with open(post_file, 'r', encoding='utf-8') as f:
    post_data = json.load(f)

def extract_date_from_text(text):
    """从文本中提取日期"""
    pattern = r'\((\d{4}-\d{2}-\d{2})\)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def find_date_for_quote(quote_text, source):
    """根据语录内容查找对应的日期"""
    # 先在语录文本中查找日期
    date = extract_date_from_text(quote_text)
    if date:
        return date
    
    # 对于帖子合集，尝试在帖子数据中查找
    if source == '帖子合集':
        # 语录内容可能在帖子的某处
        for item in post_data:
            if any(quote_text[:50] in text for text in [item.get('text', '')[:200]]):
                date = extract_date_from_text(item.get('text', ''))
                if date:
                    return date
    
    return None

# 定义来源的时间范围（书籍没有具体时间）
source_info = {
    '投资逻辑篇': {'period': '2006-2020', 'desc': '雪球问答整理'},
    '商业逻辑篇': {'period': '2006-2020', 'desc': '雪球问答整理'},
    '博客文章合集': {'period': '2006-2018', 'desc': '博客文章'},
    '帖子合集': {'period': '2010-2020', 'desc': '雪球帖子'}
}

# 增强每家公司的语录
for company_name, company_data in data.get('companies', {}).items():
    quotes = company_data.get('quotes', [])
    enhanced_quotes = []
    
    for quote in quotes:
        source = quote.get('source', '')
        text = quote.get('quote', '')
        
        # 尝试提取时间
        date = find_date_for_quote(text, source)
        
        if date:
            quote['date'] = date
            quote['date_type'] = '确切'
            quote['period'] = date
        else:
            # 使用来源的时间范围
            info = source_info.get(source, {'period': '2006-2020'})
            quote['date'] = info['period']
            quote['date_type'] = '时间范围'
            quote['period'] = info['period']
        
        enhanced_quotes.append(quote)
    
    # 排序：确切时间在前，时间范围在后，同一时间范围内按时间正序
    def sort_key(q):
        date = q.get('date', '')
        if q.get('date_type') == '确切':
            return ('a', date)
        else:
            return ('b', date)
    
    enhanced_quotes.sort(key=sort_key)
    company_data['quotes'] = enhanced_quotes
    
    # 统计
    exact_count = sum(1 for q in enhanced_quotes if q.get('date_type') == '确切')
    range_count = sum(1 for q in enhanced_quotes if q.get('date_type') == '时间范围')
    print(f"{company_name}: 确切{ exact_count}条, 范围{range_count}条")

# 保存增强后的数据
output_path = 'wiki/structured/company_analysis_timeline.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ 增强数据已保存到 {output_path}")
