#!/usr/bin/env python3
"""
从原始数据中提取时间，构建公司评价时间线
"""

import json
import re
import os
from datetime import datetime

# 读取原始博客文章数据
blog_file = 'raw/duanyongping/extracted/段永平博客文章合集 (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json'
with open(blog_file, 'r', encoding='utf-8') as f:
    blog_data = json.load(f)

# 读取帖子合集
post_file = 'raw/duanyongping/extracted/段永平帖子合集 (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json'
with open(post_file, 'r', encoding='utf-8') as f:
    post_data = json.load(f)

def extract_date_from_text(text):
    """从文本中提取日期"""
    # 匹配格式：(2010-03-17)
    pattern = r'\((\d{4}-\d{2}-\d{2})\)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    
    # 匹配博客文章标题中的日期
    pattern = r'(\d{4}-\d{2}-\d{2})'
    match = re.search(pattern, text[:100])
    if match:
        return match.group(1)
    
    return None

def build_timeline(data, source_name):
    """构建时间线"""
    timeline = []
    for item in data:
        text = item.get('text', '')
        page = item.get('page', 0)
        
        # 尝试提取日期
        date = extract_date_from_text(text)
        
        timeline.append({
            'page': page,
            'text': text[:500],  # 只保留前500字符
            'date': date,
            'source': source_name
        })
    
    return timeline

# 构建博客时间线
blog_timeline = build_timeline(blog_data, '博客文章合集')
print(f"博客文章：{len(blog_timeline)} 条")

# 构建帖子时间线
post_timeline = build_timeline(post_data, '帖子合集')
print(f"帖子合集：{len(post_timeline)} 条")

# 统计有日期的条目
blog_with_dates = sum(1 for t in blog_timeline if t['date'])
post_with_dates = sum(1 for t in post_timeline if t['date'])
print(f"博客有日期：{blog_with_dates} 条")
print(f"帖子有日期：{post_with_dates} 条")

# 保存时间线数据
timeline_data = {
    'blog': blog_timeline,
    'posts': post_timeline
}

with open('wiki/structured/timeline_raw.json', 'w', encoding='utf-8') as f:
    json.dump(timeline_data, f, ensure_ascii=False, indent=2)

print(f"✅ 时间线数据已保存")
