#!/usr/bin/env python3
"""
增强公司评价数据：添加时间维度
1. 从原始数据中提取时间信息
2. 为语录添加时间字段
3. 按时间排序
"""

import json
import re
import os
from datetime import datetime

# 读取公司分析数据
with open('wiki/structured/company_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 定义来源的时间范围（用于估算书籍中语录的时间）
source_time_ranges = {
    '投资逻辑篇': ('2006', '2020'),  # 基于书中提到的雪球问答时间
    '商业逻辑篇': ('2006', '2020'),
    '博客文章合集': ('2006', '2018'),  # 博客文章合集的时间范围
    '帖子合集': ('2010', '2020'),  # 雪球帖子时间范围
}

def extract_date_from_text(text):
    """从文本中提取日期"""
    # 匹配格式如：(2010-03-17)、(2011-12-14)、(2019-08-05)
    patterns = [
        r'\((\d{4}-\d{2}-\d{2})\)',  # (2010-03-17)
        r'\((\d{4}/\d{2}/\d{2})\)',  # (2010/03/17)
        r'(\d{4}-\d{2}-\d{2})',       # 2010-03-17
        r'(\d{4}年\d{1,2}月\d{1,2}日)',  # 2010年3月17日
        r'\[(\d{4}-\d{2}-\d{2})\]',   # [2010-03-17]
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1)
            # 标准化格式
            date_str = date_str.replace('/', '-')
            return date_str
    return None

def estimate_date_from_source(source, page):
    """根据来源和页码估算时间"""
    if source in source_time_ranges:
        start, end = source_time_ranges[source]
        # 根据页码估算（粗略）
        return f"{start}~{end}"
    return "未知时间"

# 增强每家公司的语录
for company_name, company_data in data.get('companies', {}).items():
    quotes = company_data.get('quotes', [])
    enhanced_quotes = []
    
    for quote in quotes:
        source = quote.get('source', '')
        page = quote.get('page', 0)
        text = quote.get('quote', '')
        
        # 尝试从文本中提取时间
        date = extract_date_from_text(text)
        
        if date:
            quote['date'] = date
            quote['date_type'] = '确切'
        else:
            # 使用估算时间
            quote['date'] = estimate_date_from_source(source, page)
            quote['date_type'] = '估算'
        
        enhanced_quotes.append(quote)
    
    # 按时间排序（确切时间在前，估算时间在后）
    def sort_key(q):
        date = q.get('date', '')
        if '~' in date:
            return ('z', date)  # 估算时间排后面
        return ('a', date)  # 确切时间排前面
    
    enhanced_quotes.sort(key=sort_key)
    company_data['quotes'] = enhanced_quotes

# 保存增强后的数据
output_path = 'wiki/structured/company_analysis_enhanced.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 数据已增强并保存到 {output_path}")
print(f"处理了 {len(data.get('companies', {}))} 家公司")

# 统计
total_quotes = 0
exact_dates = 0
for company_name, company_data in data.get('companies', {}).items():
    quotes = company_data.get('quotes', [])
    total_quotes += len(quotes)
    for q in quotes:
        if q.get('date_type') == '确切':
            exact_dates += 1

print(f"总语录数: {total_quotes}")
print(f"有确切时间的语录: {exact_dates}")
