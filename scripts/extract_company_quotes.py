#!/usr/bin/env python3
"""
段永平知识库 - 深度分析脚本
从书籍中提取：
1. 每家公司相关的评价（含页码来源）
2. 决策链路分析
3. 完整的语录库
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

# 公司关键词映射
COMPANIES = {
    # 主要持仓/投资
    '网易': {'name': '网易', 'symbol': 'NTES', 'type': '历史持仓', 'return': '100倍+'},
    '苹果': {'name': '苹果', 'symbol': 'AAPL', 'type': '持仓公司', 'return': '长期持有'},
    '茅台': {'name': '贵州茅台', 'symbol': '600519', 'type': '持仓公司', 'return': '长期持有'},
    '腾讯': {'name': '腾讯控股', 'symbol': '0700.HK', 'type': '持仓公司', 'return': '长期持有'},
    '拼多多': {'name': '拼多多', 'symbol': 'PDD', 'type': '持仓公司', 'return': '长期持有'},

    # 历史持仓/案例
    '百度': {'name': '百度', 'symbol': 'BIDU', 'type': '教训案例', 'return': '做空亏损'},
    '雅虎': {'name': '雅虎', 'symbol': 'YHOO', 'type': '历史持仓', 'return': '已清仓'},
    'GE': {'name': '通用电气', 'symbol': 'GE', 'type': '案例分析', 'return': '分析案例'},
    'Yahoo': {'name': '雅虎', 'symbol': 'YHOO', 'type': '历史持仓', 'return': '已清仓'},

    # 步步高系
    'OPPO': {'name': 'OPPO', 'symbol': '', 'type': '创业公司', 'return': '创始人'},
    'vivo': {'name': 'vivo', 'symbol': '', 'type': '关联公司', 'return': '联合创始人'},
    '步步高': {'name': '步步高', 'symbol': '', 'type': '创业公司', 'return': '创始人'},
    '小霸王': {'name': '小霸王', 'symbol': '', 'type': '早期创业', 'return': '缔造者'},

    # 关注公司
    '阿里巴巴': {'name': '阿里巴巴', 'symbol': 'BABA', 'type': '关注公司', 'return': '间接持股'},
    '阿里': {'name': '阿里巴巴', 'symbol': 'BABA', 'type': '关注公司', 'return': '间接持股'},
    '五粮液': {'name': '五粮液', 'symbol': '000858', 'type': '关注公司', 'return': '关注'},
    '微软': {'name': '微软', 'symbol': 'MSFT', 'type': '关注公司', 'return': '关注'},
    'Facebook': {'name': 'Facebook', 'symbol': 'META', 'type': '关注公司', 'return': '关注'},
    '特斯拉': {'name': '特斯拉', 'symbol': 'TSLA', 'type': '关注公司', 'return': '关注'},
    '比亚迪': {'name': '比亚迪', 'symbol': '002594', 'type': '关注公司', 'return': '关注'},
    '可口可乐': {'name': '可口可乐', 'symbol': 'KO', 'type': '关注公司', 'return': '案例分析'},
    '亚马逊': {'name': '亚马逊', 'symbol': 'AMZN', 'type': '关注公司', 'return': '关注'},
    '谷歌': {'name': 'Alphabet/谷歌', 'symbol': 'GOOGL', 'type': '关注公司', 'return': '关注'},
    '星巴克': {'name': '星巴克', 'symbol': 'SBUX', 'type': '关注公司', 'return': '关注'},
    '迪士尼': {'name': '迪士尼', 'symbol': 'DIS', 'type': '关注公司', 'return': '关注'},
    'GEICO': {'name': 'GEICO', 'symbol': '', 'type': '学习案例', 'return': '巴菲特案例'},
    '喜诗糖果': {'name': '喜诗糖果', 'symbol': '', 'type': '学习案例', 'return': '巴菲特案例'},
    '招商银行': {'name': '招商银行', 'symbol': '600036', 'type': '关注公司', 'return': '关注'},
    '新浪': {'name': '新浪', 'symbol': 'SINA', 'type': '关注公司', 'return': '关注'},
    'IBM': {'name': 'IBM', 'symbol': 'IBM', 'type': '案例分析', 'return': '关注'},
    '京东': {'name': '京东', 'symbol': 'JD', 'type': '关注公司', 'return': '关注'},
    '美团': {'name': '美团', 'symbol': '3690.HK', 'type': '关注公司', 'return': '关注'},
    '万科': {'name': '万科', 'symbol': '000002', 'type': '关注公司', 'return': '关注'},
}

def extract_company_quotes(content, source_name):
    """从内容中提取公司相关语录"""
    results = defaultdict(list)

    for page_data in content:
        page = page_data['page']
        text = page_data['text']

        for keyword, company_info in COMPANIES.items():
            if keyword in text:
                # 提取包含该公司的段落
                sentences = re.split(r'[。！？\n]', text)
                for sentence in sentences:
                    if keyword in sentence and len(sentence) > 15:
                        sentence = sentence.strip()
                        if sentence:
                            results[company_info['name']].append({
                                'quote': sentence,
                                'page': page,
                                'source': source_name,
                                'type': company_info['type'],
                                'return': company_info['return']
                            })

    return results

def analyze_decision_chain(quotes_by_company):
    """分析决策链路"""
    decision_chains = {}

    for company, quotes in quotes_by_company.items():
        if len(quotes) < 3:
            continue

        chain = {
            'why_buy': [],
            'business_model': [],
            'risk': [],
            'valuation': [],
            'holding': [],
            'lesson': []
        }

        for q in quotes:
            text = q['quote'].lower()
            if any(k in text for k in ['为什么', '因为', '看好', '买', '买入', '投资']):
                if '不懂' not in text:
                    chain['why_buy'].append(q)
            if any(k in text for k in ['商业模式', '护城河', '竞争力', '盈利', '商业模式']):
                chain['business_model'].append(q)
            if any(k in text for k in ['风险', '安全', '亏', '跌', '问题']):
                chain['risk'].append(q)
            if any(k in text for k in ['估值', '价格', '便宜', '贵', 'pe', '市值', '内在价值']):
                chain['valuation'].append(q)
            if any(k in text for k in ['持有', '长期', '不卖', '继续']):
                chain['holding'].append(q)
            if any(k in text for k in ['教训', '错误', '亏钱', '后悔', '失败']):
                chain['lesson'].append(q)

        if chain['why_buy'] or chain['business_model'] or chain['valuation']:
            decision_chains[company] = chain

    return decision_chains

def main():
    base_dir = "/Users/panxiaoli/Desktop/投资大佬agent知识库"
    extracted_dir = os.path.join(base_dir, "raw", "duanyongping", "extracted")
    output_dir = os.path.join(base_dir, "wiki", "structured")

    os.makedirs(output_dir, exist_ok=True)

    # 书籍列表
    books = [
        ("段永平01 段永平投资问答录(投资逻辑篇) (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json", "投资逻辑篇"),
        ("段永平02 段永平投资问答录（商业逻辑篇） (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json", "商业逻辑篇"),
        ("段永平博客文章合集 (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json", "博客文章合集"),
        ("段永平帖子合集 (段永平) (z-library.sk, 1lib.sk, z-lib.sk)_content.json", "帖子合集"),
    ]

    all_quotes = defaultdict(list)

    print("开始提取公司相关语录...")

    for filename, book_name in books:
        filepath = os.path.join(extracted_dir, filename)
        if os.path.exists(filepath):
            print(f"处理: {book_name}")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = json.load(f)

            company_quotes = extract_company_quotes(content, book_name)

            for company, quotes in company_quotes.items():
                for q in quotes:
                    # 去重
                    is_duplicate = False
                    for existing in all_quotes[company]:
                        if existing['quote'][:50] == q['quote'][:50]:
                            is_duplicate = True
                            break
                    if not is_duplicate:
                        all_quotes[company].append(q)

            print(f"  - 找到 {len(company_quotes)} 家公司的 {sum(len(v) for v in company_quotes.values())} 条语录")

    # 分析决策链路
    print("\n分析决策链路...")
    decision_chains = analyze_decision_chain(all_quotes)

    # 生成完整分析结果
    result = {
        'companies': {},
        'decision_chains': decision_chains,
        'summary': {
            'total_companies': len(all_quotes),
            'companies_with_quotes': {k: len(v) for k, v in all_quotes.items()}
        }
    }

    for company, quotes in all_quotes.items():
        if len(quotes) >= 1:
            # 找出公司信息
            company_info = None
            for kw, info in COMPANIES.items():
                if info['name'] == company:
                    company_info = info
                    break

            result['companies'][company] = {
                'info': company_info,
                'quotes': quotes,
                'quote_count': len(quotes)
            }

    # 保存结果
    output_file = os.path.join(output_dir, 'company_analysis.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n分析完成！")
    print(f"- 公司数量: {len(all_quotes)}")
    print(f"- 决策链路: {len(decision_chains)}")
    print(f"- 保存到: {output_file}")

    return result

if __name__ == "__main__":
    main()
