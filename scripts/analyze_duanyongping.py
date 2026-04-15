#!/usr/bin/env python3
"""
段永平知识库内容分析脚本
从已提取的内容中提取关键知识点，构建多维度索引
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

# 公司关键词
COMPANIES = {
    # 互联网
    '网易': 'netease', '百度': 'baidu', '腾讯': 'tencent', '阿里': 'alibaba', '阿里巴巴': 'alibaba',
    '苹果': 'apple', '谷歌': 'google', '亚马逊': 'amazon', '微软': 'microsoft', 'facebook': 'facebook', 'meta': 'meta',
    '拼多多': 'pinduoduo', '字节跳动': 'bytedance', '抖音': 'tiktok', '快手': 'kuaishou',
    '新浪': 'sina', '搜狐': 'sohu', '盛大': 'shanda', '优酷': 'youku', '土豆': 'tudou',
    'yahoo': 'yahoo', '雅虎': 'yahoo', 'IBM': 'ibm',

    # 消费
    '茅台': 'maotai', '贵州茅台': 'maotai', '五粮液': 'wuliangye', '洋河': 'yanghe',
    '可口可乐': 'coca-cola', '百事可乐': 'pepsi', '星巴克': 'starbucks',
    '麦当劳': 'mcdonalds', '肯德基': 'kfc', '耐克': 'nike', '阿迪达斯': 'adidas',
    'OPPO': 'oppo', 'vivo': 'vivo', '步步高': 'bbk', '小霸王': 'xiaobawang',

    # 金融
    '银行': 'bank', '工商银行': 'icbc', '建设银行': 'ccb', '招商银行': 'cmb',
    '中国平安': 'pingan', '平安保险': 'pingan', '保险公司': 'insurance',

    # 其他
    '比亚迪': 'byd', '特斯拉': 'tesla', 'GE': 'ge', '通用电气': 'ge',
    'GEICO': 'geico', '迪士尼': 'disney', '吉列': 'gillette', '箭牌': 'wrigley',
    '喜诗糖果': 'sees', '亨氏': 'heinz', '卡夫': 'kraft',
}

# 投资主题
TOPICS = {
    '投资理念': ['投资理念', '买股票就是买公司', '未来现金流', '价值投资', '投资是什么'],
    '能力圈': ['能力圈', '不懂不做', '看懂', '理解'],
    '护城河': ['护城河', '商业模式', '生意模式', '壁垒', '护城河'],
    '安全边际': ['安全边际', '便宜', '低估', '折扣'],
    '平常心': ['平常心', '心态', '不着急', '不焦虑', '耐心', '淡定'],
    '本分': ['本分', '诚信', '正直', '本分主义'],
    'Stop Doing List': ['stop doing', '不为清单', '不为', '不做'],
    '风险控制': ['风险', '不做空', '不借钱', '止损', '安全'],
    '估值': ['估值', 'PE', '市盈率', 'PB', '市净率', 'DCF', '现金流折现'],
    '持仓管理': ['仓位', '集中', '分散', '持有', '持仓'],
    '企业文化': ['企业文化', '本分', '消费者导向', '做对的事情'],
    '止损': ['止损', '卖出', '卖出条件'],
}


def extract_companies(text):
    """从文本中提取公司名称"""
    found = set()
    for company in COMPANIES.keys():
        if company.lower() in text.lower() or company in text:
            found.add(company)
    return found


def extract_quotes(text):
    """提取段永平的语录"""
    quotes = []
    # 匹配各种引号格式
    patterns = [
        r'段永平[：:]([^"\'\n]{10,200})',  # 段永平说：
        r'"([^"]{20,300})"',  # "引号内容"
        r'“([^”]{20,300})"',  # "中文引号内容"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            match = match.strip()
            if len(match) > 15 and not match.startswith('http'):
                quotes.append(match)

    return list(set(quotes))[:5]  # 每页最多5条


def extract_topics(text):
    """提取主题"""
    found = set()
    text_lower = text.lower()
    for topic, keywords in TOPICS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower or keyword in text:
                found.add(topic)
                break
    return list(found)


def analyze_content(content, source_name):
    """分析内容并提取知识点"""
    results = {
        'source': source_name,
        'companies': defaultdict(list),
        'topics': defaultdict(list),
        'quotes': [],
        'pages': len(content)
    }

    for page_data in content:
        page = page_data['page']
        text = page_data['text']

        # 提取公司
        companies = extract_companies(text)
        for company in companies:
            results['companies'][company].append(page)

        # 提取主题
        topics = extract_topics(text)
        for topic in topics:
            results['topics'][topic].append(page)

        # 提取语录
        quotes = extract_quotes(text)
        for quote in quotes:
            if quote not in results['quotes']:
                results['quotes'].append({
                    'text': quote,
                    'page': page,
                    'source': source_name
                })

    return results


def main():
    base_dir = "/Users/panxiaoli/Desktop/投资大佬agent知识库"
    extracted_dir = os.path.join(base_dir, "raw", "duanyongping", "extracted")
    output_dir = os.path.join(base_dir, "wiki", "structured")
    os.makedirs(output_dir, exist_ok=True)

    # 书籍列表 (使用实际文件名)
    books = [
        ("段永平01 段永平投资问答录(投资逻辑篇) (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json", "投资逻辑篇"),
        ("段永平02 段永平投资问答录（商业逻辑篇） (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json", "商业逻辑篇"),
        ("段永平博客文章合集 (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json", "博客文章合集"),
        ("段永平帖子合集 (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json", "帖子合集"),
    ]

    all_results = []

    for filename, book_name in books:
        filepath = os.path.join(extracted_dir, filename)
        if os.path.exists(filepath):
            print(f"分析: {book_name}")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = json.load(f)
            result = analyze_content(content, book_name)
            all_results.append(result)
            print(f"  - 页数: {result['pages']}")
            print(f"  - 公司提及: {len(result['companies'])}")
            print(f"  - 主题提及: {len(result['topics'])}")
            print(f"  - 语录: {len(result['quotes'])}")

    # 汇总所有公司
    company_summary = defaultdict(list)
    for result in all_results:
        for company, pages in result['companies'].items():
            company_summary[company].extend(pages)

    # 按提及次数排序
    top_companies = sorted(company_summary.items(), key=lambda x: len(x[1]), reverse=True)[:50]

    # 汇总所有主题
    topic_summary = defaultdict(list)
    for result in all_results:
        for topic, pages in result['topics'].items():
            topic_summary[topic].extend(pages)

    # 合并所有语录
    all_quotes = []
    for result in all_results:
        all_quotes.extend(result['quotes'])

    # 保存分析结果
    analysis_result = {
        'top_companies': {k: list(set(v)) for k, v in top_companies},
        'topics': {k: list(set(v)) for k, v in topic_summary.items()},
        'quotes': all_quotes[:200],  # 限制200条
        'sources': [r['source'] for r in all_results]
    }

    with open(os.path.join(output_dir, 'analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)

    print(f"\n分析完成！")
    print(f"顶级公司: {len(top_companies)}")
    print(f"主题分类: {len(topic_summary)}")
    print(f"语录总数: {len(all_quotes)}")

    return analysis_result


if __name__ == "__main__":
    main()
