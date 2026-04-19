#!/usr/bin/env python3
"""
段永平知识库 - 智能问答解析与归类脚本
功能：
1. 解析原始问答数据
2. 识别问答对
3. 提取主题上下文
4. 合并相似问题
5. 生成结构化数据
6. 输出 karpathy-llm-wiki 格式的文章

用法：
  python smart_qa_parser.py                    # 处理并生成所有输出
  python smart_qa_parser.py --dry-run         # 仅分析，不生成文件
  python smart_qa_parser.py --company 苹果    # 仅处理指定公司
"""

import json
import re
import os
import argparse
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# 段永平简介模式 - 用于过滤
DUANYONGPING_INTRO_PATTERNS = [
    r'著名企业家，小霸王品牌缔造者',
    r'步步高创始人',
    r'vivo和OPPO',
    r'网易丁磊生命中的贵人',
    r'拼多多黄峥的人生导师',
    r'著名投资人',
    r'不管[是作]',
    r'网易丁磊',
]

# 主题关键词配置 - 用于自动归类问答
TOPIC_KEYWORDS = {
    "投资逻辑": {
        "keywords": ["买股票", "买入", "投资", "股票", "回报", "长期持有", "价值", "估值", "内在价值", "现金流", "折现", "护城河"],
        "context": "关于价值投资的核心逻辑和方法"
    },
    "商业模式": {
        "keywords": ["生意模式", "商业模式", "护城河", "差异化", "竞争力", "盈利模式", "利润", "毛利率", "成本"],
        "context": "如何评估和理解企业商业模式"
    },
    "企业文化": {
        "keywords": ["企业文化", "本分", "平常心", "价值观", "诚信", "正直", "文化", "使命", "追求"],
        "context": "企业文化的重要性及其对企业长期发展的影响"
    },
    "管理层": {
        "keywords": ["管理层", "CEO", "乔布斯", "库克", "马化腾", "丁磊", "马云", "创始人", "领导", "管理"],
        "context": "管理层的能力和人品对企业的影响"
    },
    "风险控制": {
        "keywords": ["风险", "安全边际", "不做空", "不借钱", "不懂不做", "止损", "分散", "仓位"],
        "context": "投资中的风险意识和风险管理"
    },
    "苹果公司": {
        "keywords": ["苹果", "iPhone", "iPad", "乔布斯", "库克", "Apple", "智能手机"],
        "context": "关于苹果公司的投资分析"
    },
    "茅台公司": {
        "keywords": ["茅台", "飞天", "酱香", "白酒", "茅台酒", "国酒"],
        "context": "关于贵州茅台的投资分析"
    },
    "腾讯公司": {
        "keywords": ["腾讯", "微信", "QQ", "马化腾", "社交", "腾讯控股"],
        "context": "关于腾讯控股的投资分析"
    },
    "网易公司": {
        "keywords": ["网易", "丁磊", "游戏", "NetEase", "魔兽"],
        "context": "关于网易的投资分析"
    },
    "投资案例": {
        "keywords": ["投资案例", "买入时机", "卖出", "持仓", "买卖", "建仓"],
        "context": "具体投资案例分析"
    }
}

def parse_date(text):
    """从文本中提取日期"""
    patterns = [
        r'（(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)）',  # （2024-01-01）
        r'（(\d{4}[-/年]\d{1,2}[日]?)）',  # （2024-01）
        r'（(\d{4}年)）',  # （2024年）
        r'\((\d{4}-\d{2}-\d{2})\)',  # (2024-01-01)
        r'(\d{4}-\d{2}-\d{2})',  # 2024-01-01
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return None

def extract_question_answer_pairs(text):
    """
    从文本中提取问答对
    返回格式: [{'type': 'q/a', 'content': '...', 'date': '...'}, ...]
    """
    results = []

    # 清理文本中的多余空白
    text = re.sub(r'\s+', ' ', text)

    # 模式1: 段永平回答在前，网友问题在后
    # 例如: "段永平：回答。（日期）02.网友：问题？"
    pattern1 = re.compile(
        r'段永平[：:]\s*([^。（]+(?:[（(][^）)]*[）)][^。]*)?。?)'  # 段永平的回答
        r'\s*'  # 中间可能有空白
        r'(\d{1,2}[.、]?\s*)?网友[：:：]?\s*([^？?]*[？?])?'  # 网友问题
        r'([\s\S]*?(?=\d{1,2}[.、]?\s*网友|段永平[：:]|$))?'  # 后续内容
    )

    # 模式2: 网友问题在前，段永平回答在后
    # 例如: "01.网友：问题？段永平：回答。（日期）"
    pattern2 = re.compile(
        r'(\d{1,2}[.、]?\s*)?网友[：:：]?\s*([^？?]*[？?])?'  # 网友问题
        r'\s*'  # 中间可能有空白
        r'段永平[：:]\s*([^。（]+(?:[（(][^）)]*[）)][^。]*)?。?)'  # 段永平的回答
    )

    # 模式3: 简单问答格式 "网友：xxx？段永平：yyy。"
    pattern3 = re.compile(
        r'网友[：:]\s*([^？?]*[？?])?\s*段永平[：:]\s*([^。]*。?)'
    )

    # 模式4: 博客回复格式 "段永平回复xxx 日期 时间"
    pattern4 = re.compile(
        r'段永平(回复[^：:]*)?[：:]\s*([^。\n]+(?:[。\n]|$))+'
    )

    # 提取段永平的回答（可能是单独的）
    answer_pattern = re.compile(r'段永平[：:]\s*([^。]+(?:[（(][^）)]*[）)][^。]*)?。?)')
    for match in answer_pattern.finditer(text):
        content = match.group(1).strip()
        if len(content) > 5:  # 过滤太短的
            date = parse_date(content)
            results.append({
                'type': 'answer',
                'content': content,
                'date': date
            })

    # 提取网友问题
    question_pattern = re.compile(r'(\d{1,2}[.、]?\s*)?网友[：:：]?\s*([^？?]*[？?])?')
    for match in question_pattern.finditer(text):
        prefix = match.group(1) or ''
        content = match.group(2)
        if content and len(content.strip()) > 3:
            results.append({
                'type': 'question',
                'content': content.strip(),
                'prefix': prefix.strip()
            })

    return results

def classify_topic(text):
    """
    根据文本内容分类到主题
    返回最匹配的主题和置信度
    """
    text_lower = text.lower()
    scores = {}

    for topic, config in TOPIC_KEYWORDS.items():
        score = 0
        for keyword in config['keywords']:
            if keyword.lower() in text_lower:
                score += 1
        if score > 0:
            scores[topic] = score

    if not scores:
        return "其他", 0

    # 返回得分最高的主题
    best_topic = max(scores, key=scores.get)
    return best_topic, scores[best_topic]

def extract_context(text, max_length=200):
    """
    提取上下文摘要
    移除问答标记，提取核心内容
    """
    # 移除问答标记
    cleaned = re.sub(r'段永平[：:]\s*', '', text)
    cleaned = re.sub(r'网友[：:：]?\s*', '', cleaned)
    cleaned = re.sub(r'\d{1,2}[.、]\s*', '', cleaned)
    cleaned = re.sub(r'[（(][^）)]*[）)]\s*', '', cleaned)

    # 移除日期
    cleaned = re.sub(r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?', '', cleaned)
    cleaned = re.sub(r'\d{4}[-/年]\d{1,2}[日]?', '', cleaned)
    cleaned = re.sub(r'\d{4}年', '', cleaned)

    # 截取前N个字符
    cleaned = cleaned.strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + '...'

    return cleaned

def process_quote(quote):
    """
    处理单条语录，提取问答对和主题
    """
    text = quote['text']
    page = quote.get('page', '')
    source = quote.get('source', '')

    # 分类主题
    topic, topic_score = classify_topic(text)

    # 提取问答对
    qa_pairs = extract_question_answer_pairs(text)

    # 提取上下文
    context = extract_context(text)

    return {
        'text': text,
        'page': page,
        'source': source,
        'topic': topic,
        'topicScore': topic_score,
        'context': context,
        'qaPairs': qa_pairs
    }

def group_by_topic(quotes):
    """
    将语录按主题分组
    """
    grouped = defaultdict(list)

    for quote in quotes:
        topic = quote['topic']
        grouped[topic].append(quote)

    return dict(grouped)

def merge_similar_questions(quotes):
    """
    合并相似的问题
    这个功能需要更复杂的 NLP，可以先实现简单的关键词匹配
    """
    # 简化版本：按主题和时间分组
    merged = []

    for quote in quotes:
        # 检查是否与已有条目重复
        is_duplicate = False
        for existing in merged:
            # 检查相似度（简单比较前50个字符）
            if existing['text'][:80] == quote['text'][:80]:
                is_duplicate = True
                break

        if not is_duplicate:
            merged.append(quote)

    return merged

def generate_wiki_article(company_name, company_data, topic_quotes):
    """
    生成 karpathy-llm-wiki 格式的文章
    """
    lines = []
    lines.append("---")
    lines.append(f"title: {company_name}")
    lines.append(f"type: company-analysis")
    lines.append(f"Updated: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {company_name}")

    # 公司基本信息
    company_type = company_data.get('type', '未分类')
    return_info = company_data.get('returnInfo', '')
    if return_info:
        lines.append(f"**投资状态**: {return_info} | **类型**: {company_type}")
    else:
        lines.append(f"**类型**: {company_type}")
    lines.append("")

    # 按主题生成内容
    for topic, quotes in topic_quotes.items():
        if topic == "其他" or len(quotes) < 2:
            continue

        lines.append(f"## {topic}")
        lines.append("")

        # 主题概述
        topic_config = TOPIC_KEYWORDS.get(topic, {})
        if 'context' in topic_config:
            lines.append(f"*{topic_config['context']}*")
            lines.append("")

        # 合并相似问答
        merged = merge_qa_pairs(quotes)

        # 生成问答对
        for idx, qa in enumerate(merged, 1):
            # 问
            if qa.get('question'):
                lines.append(f"**问**: {qa['question']}")

            # 答
            if qa.get('answer'):
                lines.append(f"**答**: {qa['answer']}")

            # 来源
            if qa.get('source'):
                source_info = f"[{qa['source']}"
                if qa.get('page'):
                    source_info += f" 第{qa['page']}页"
                if qa.get('date'):
                    source_info += f" {qa['date']}"
                source_info += "]"
                lines.append(f"*{source_info}*")

            lines.append("")

    # 添加未分类的问答（如果有）
    if "其他" in topic_quotes and len(topic_quotes["其他"]) > 0:
        lines.append("## 其他观点")
        lines.append("")
        for qa in topic_quotes["其他"][:5]:  # 限制数量
            if qa.get('text'):
                # 清理格式
                text = re.sub(r'段永平[：:]\s*', '', qa['text'])
                text = re.sub(r'网友[：:：]?\s*', '', text)
                lines.append(f"- {text[:200]}{'...' if len(text) > 200 else ''}")

    lines.append("")
    lines.append("---")
    lines.append("## Sources")
    lines.append("- [companyData.js](website/js/companyData.js)")

    return "\n".join(lines)


def is_intro_content(text):
    """
    判断是否是段永平简介内容
    """
    # 简介特征：较短，包含多个头衔
    if len(text) > 200:
        return False

    intro_count = 0
    for pattern in DUANYONGPING_INTRO_PATTERNS:
        if re.search(pattern, text):
            intro_count += 1

    # 如果匹配多个简介模式，认为是简介
    return intro_count >= 2


def filter_intro_from_text(text):
    """
    从文本中过滤掉段永平简介部分
    """
    result = text

    # 移除开头的简介
    intro_patterns = [
        r'^段永平[：:]\s*著名[^\n。]*?(?:企业家|投资人)[^\n。]*?。',  # 段永平：著名企业家...。
        r'^段永平[：:]\s*[^\n]*?(?:创始人|贵人|导师)[^\n。]*?。',  # 段永平：...创始人...。
    ]

    for pattern in intro_patterns:
        result = re.sub(pattern, '', result)

    # 清理多余空白
    result = re.sub(r'\n+', '\n', result)
    result = re.sub(r' +', ' ', result)

    return result.strip()


def merge_qa_pairs(quotes):
    """
    合并相似的问答对
    """
    merged = []
    seen_answers = set()  # 用于去重

    for quote in quotes:
        text = quote.get('text', '')

        # 过滤简介
        if is_intro_content(text):
            continue

        # 清理文本
        clean_text = filter_intro_from_text(text)
        if len(clean_text) < 20:
            continue

        # 提取问答
        q_pattern = re.compile(r'(\d{1,2}[.、]?\s*)?网友[：:：]?\s*([^？?]*[？?])?')
        q_match = q_pattern.search(clean_text)

        # 段永平回答 - 更严格的匹配
        a_pattern = re.compile(r'段永平[：:]\s*([^。（]+(?:[（(][^）)]*[）)][^。]*)?。?)')
        a_match = a_pattern.search(clean_text)

        if q_match or a_match:
            question = q_match.group(2).strip() if q_match and q_match.group(2) else None
            answer = a_match.group(1).strip() if a_match else None

            # 跳过简介内容
            if answer and is_intro_content(answer):
                continue

            # 跳过太短的回答
            if answer and len(answer) < 10:
                continue

            # 检查是否重复
            is_dup = False
            if answer:
                # 使用前50个字符作为唯一标识
                answer_key = answer[:50]
                if answer_key in seen_answers:
                    is_dup = True
                else:
                    seen_answers.add(answer_key)

            if not is_dup:
                qa = {
                    'question': question,
                    'answer': answer,
                    'source': quote.get('source', ''),
                    'page': quote.get('page', ''),
                    'date': quote.get('date')
                }

                # 提取日期
                if not qa['date'] and answer:
                    qa['date'] = parse_date(answer)

                merged.append(qa)

    return merged


def parse_with_node_js(content):
    """
    使用 Node.js 解析 JavaScript 对象
    通过临时文件方式，避免命令行参数过长
    """
    import subprocess
    import tempfile
    import os

    # 创建 Node.js 解析器脚本
    parser_script = '''
const fs = require('fs');
const path = require('path');

const inputFile = process.argv[2];
if (!inputFile) {
    console.error('Usage: node parser.js <input.js>');
    process.exit(1);
}

const content = fs.readFileSync(inputFile, 'utf8');
let jsonStr = content.replace(/^const\\s+companyData\\s*=\\s*/, '');
jsonStr = jsonStr.replace(/;\\s*$/, '');

try {
    const data = JSON.parse(jsonStr);
    console.log(JSON.stringify(data));
} catch (e) {
    console.error('JSON parse error: ' + e.message);
    process.exit(1);
}
'''

    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as parser_f:
        parser_path = parser_f.name
        parser_f.write(parser_script)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as input_f:
        input_path = input_f.name
        input_f.write(content)

    try:
        result = subprocess.run(
            ['node', parser_path, input_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Node.js 错误: {result.stderr[:500]}")
            return None
    except subprocess.TimeoutExpired:
        print("Node.js 解析超时")
        return None
    except Exception as e:
        print(f"Node.js 解析异常: {e}")
        return None
    finally:
        for p in [parser_path, input_path]:
            if os.path.exists(p):
                os.unlink(p)


def fix_json_content(content):
    r"""
    修复 JSON 内容中的非法转义字符
    1. \ + 空格 -> \\ + 空格 (转义反斜杠，避免 \ 后跟空格导致无效的 JSON 转义)
    2. 。" (句号+引号) 孤立引号问题 -> 。\" (转义引号，避免引号提前关闭字符串)
       当 。" 后紧跟非空白/逗号/换行时，说明引号是孤立的，需要修复
    """
    # 修复1: 反斜杠+空格 (无效的 JSON 转义)
    # 修复1: 反斜杠+空格 (无效的 JSON 转义)
    # 在源文件中: \ (反斜杠) + " "(空格) -> \\ (两个反斜杠) + " "(空格)
    fixed = content.replace('\\ ', '\\\\ ')

    # 修复2: 孤立引号问题
    # 模式: 。" 后紧跟非空白/逗号/换行 -> 引号孤立，需要转义
    def fix_orphaned_quotes(text):
        result = []
        i = 0
        while i < len(text):
            if (text[i] == '。' and i + 1 < len(text) and text[i + 1] == '"'):
                if i + 2 < len(text) and text[i + 2] not in [',', '\n', ' ', '\t']:
                    # 孤立引号！转义它
                    result.append(text[i])  # 。
                    result.append('\\')      # 添加反斜杠
                    result.append('"')       # 引号（现在变成转义的）
                    i += 2
                else:
                    result.append(text[i])
                    result.append(text[i + 1])
                    i += 2
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)

    fixed = fix_orphaned_quotes(fixed)
    return fixed


def process_company_data(input_file, output_file, wiki_output_dir, company_filter=None):
    """
    处理公司数据文件
    """
    print(f"读取数据文件: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 移除 JavaScript 变量声明
    content = re.sub(r'^const\s+companyData\s*=\s*', '', content)
    content = re.sub(r';\s*$', '', content)

    data = None

    # 方法1: 尝试使用 Node.js 解析
    print("尝试使用 Node.js 解析...")
    fixed_content = fix_json_content(content)
    data = parse_with_node_js(fixed_content)

    if not data:
        # 方法2: 使用正则表达式解析
        print("尝试使用 Python 正则表达式解析...")
        data = parse_js_with_regex(content)

    if not data:
        print("无法解析文件，请检查文件格式")
        return None

    # 创建 wiki 输出目录
    os.makedirs(wiki_output_dir, exist_ok=True)

    # 处理每家公司的数据
    processed_data = {}

    total_quotes = 0
    total_qa_pairs = 0
    companies_processed = 0

    for company_name, company_data in data.items():
        # 如果指定了过滤器，跳过其他公司
        if company_filter and company_name != company_filter:
            continue

        print(f"\n处理公司: {company_name}")

        quotes = company_data.get('quotes', [])
        processed_quotes = []

        for quote in quotes:
            processed = process_quote(quote)
            processed_quotes.append(processed)

            if processed['qaPairs']:
                total_qa_pairs += len(processed['qaPairs'])

        # 按主题分组
        topic_grouped = group_by_topic(processed_quotes)

        # 合并相似问题
        merged_quotes = merge_similar_questions(processed_quotes)

        processed_data[company_name] = {
            **company_data,
            'processedQuotes': processed_quotes,
            'topicGrouped': topic_grouped,
            'topics': list(topic_grouped.keys()),
            'quoteCount': len(quotes),
            'processedCount': len(processed_quotes)
        }

        print(f"  - 原始语录: {len(quotes)}")
        print(f"  - 处理后: {len(processed_quotes)}")
        print(f"  - 主题分类: {len(topic_grouped)}")
        print(f"  - 问答对: {total_qa_pairs}")

        total_quotes += len(quotes)
        companies_processed += 1

        # 生成 wiki 文章
        # 清理文件名中的非法字符
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', company_name)
        article_filename = f"{safe_name}.md"
        article_path = os.path.join(wiki_output_dir, article_filename)

        article_content = generate_wiki_article(company_name, company_data, topic_grouped)

        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(article_content)
        print(f"  - 生成 wiki 文章: {article_path}")

    # 生成全局索引
    index_content = generate_wiki_index(processed_data)
    index_path = os.path.join(os.path.dirname(wiki_output_dir), 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"\n生成全局索引: {index_path}")

    # 生成处理后的 JSON 数据
    output = {
        'meta': {
            'version': '2.0',
            'generated': datetime.now().strftime('%Y-%m-%d'),
            'totalCompanies': len(processed_data),
            'totalQuotes': total_quotes,
            'totalQAPairs': total_qa_pairs
        },
        'companies': processed_data
    }

    print(f"\n保存处理数据到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n处理完成!")
    print(f"- 处理公司数: {companies_processed}")
    print(f"- 总语录数: {total_quotes}")
    print(f"- 总问答对: {total_qa_pairs}")

    return processed_data


def generate_wiki_index(companies_data):
    """
    生成 wiki 全局索引
    """
    lines = []
    lines.append("# Knowledge Base Index")
    lines.append("")
    lines.append(f"*最后更新: {datetime.now().strftime('%Y-%m-%d')}*")
    lines.append("")

    # 按主题分组
    by_type = defaultdict(list)
    for company, data in companies_data.items():
        company_type = data.get('type', '未分类')
        by_type[company_type].append({
            'name': company,
            'topics': data.get('topics', []),
            'quoteCount': data.get('quoteCount', 0)
        })

    # 生成索引
    for type_name in sorted(by_type.keys()):
        lines.append(f"## {type_name}")
        lines.append("")

        for company in sorted(by_type[type_name], key=lambda x: -x['quoteCount']):
            topics_str = ", ".join(company['topics'][:3]) if company['topics'] else "其他"
            lines.append(f"- [{company['name']}](entities/{company['name']}.md) - {topics_str} ({company['quoteCount']}条语录)")

        lines.append("")

    return "\n".join(lines)


def parse_quotes_array(quotes_str):
    """
    手动解析 quotes 数组
    """
    quotes = []

    # 移除多余空白
    quotes_str = quotes_str.strip()

    # 分割每个对象 - 匹配 { ... }
    i = 0
    while i < len(quotes_str):
        if quotes_str[i] == '{':
            # 找到对象的开始
            depth = 1
            j = i + 1
            while j < len(quotes_str) and depth > 0:
                if quotes_str[j] == '{' and quotes_str[j-1] != '\\':
                    depth += 1
                elif quotes_str[j] == '}' and quotes_str[j-1] != '\\':
                    depth -= 1
                j += 1

            if depth == 0:
                obj_str = quotes_str[i:j]
                try:
                    obj = json.loads(obj_str)
                    quotes.append(obj)
                except:
                    # 手动解析
                    quote = parse_quote_object(obj_str)
                    if quote:
                        quotes.append(quote)
            i = j
        else:
            i += 1

    return quotes


def parse_quote_object(obj_str):
    """
    手动解析单个 quote 对象
    """
    quote = {}

    # 提取 text
    text_match = re.search(r'"text":\s*"([^"]*(?:\\.[^"]*)*)"', obj_str)
    if text_match:
        text = text_match.group(1)
        # 清理转义
        text = text.replace('\\"', '"').replace('\\n', '\n').replace('\\r', '\r')
        quote['text'] = text

    # 提取 page
    page_match = re.search(r'"page":\s*"?(\d*)"?', obj_str)
    if page_match and page_match.group(1):
        quote['page'] = int(page_match.group(1))

    # 提取 source
    source_match = re.search(r'"source":\s*"([^"]*)"', obj_str)
    if source_match:
        quote['source'] = source_match.group(1)

    return quote if quote else None


def parse_company_block(block_content):
    """
    解析公司数据块
    """
    company_data = {
        'type': '',
        'returnInfo': '',
        'quoteCount': 0,
        'quotes': []
    }

    # 提取 type
    type_match = re.search(r'"type":\s*"([^"]*)"', block_content)
    if type_match:
        company_data['type'] = type_match.group(1)

    # 提取 returnInfo
    return_match = re.search(r'"returnInfo":\s*"([^"]*)"', block_content)
    if return_match:
        company_data['returnInfo'] = return_match.group(1)

    # 提取 quoteCount
    count_match = re.search(r'"quoteCount":\s*(\d+)', block_content)
    if count_match:
        company_data['quoteCount'] = int(count_match.group(1))

    # 提取 quotes 数组
    quotes_match = re.search(r'"quotes":\s*\[([\s\S]*)\]', block_content)
    if quotes_match:
        quotes_str = quotes_match.group(1)
        company_data['quotes'] = parse_quotes_array(quotes_str)

    return company_data


def parse_js_with_regex(content):
    """
    使用正则表达式解析 JavaScript 对象
    这是一个备选方案，当 JSON.parse 失败时使用
    """
    data = {}

    # 移除注释
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # 匹配公司名和其数据块
    pos = 0
    while pos < len(content):
        # 找到下一个公司名
        name_match = re.search(r'"([^"]+)":\s*\{', content[pos:])
        if not name_match:
            break

        company_name = name_match.group(1)
        block_start = pos + name_match.end() - 1  # 回到 {

        # 找到匹配的 }
        depth = 1
        block_end = block_start + 1
        while block_end < len(content) and depth > 0:
            if content[block_end] == '{':
                depth += 1
            elif content[block_end] == '}':
                depth -= 1
            block_end += 1

        if depth == 0:
            block_content = content[block_start:block_end]
            company_data = parse_company_block(block_content)
            if company_data and company_data.get('quotes'):
                data[company_name] = company_data

        pos = block_end

    return data if data else None


def main():
    parser = argparse.ArgumentParser(description='段永平知识库 - 智能问答解析与归类')
    parser.add_argument('--dry-run', action='store_true', help='仅分析，不生成文件')
    parser.add_argument('--company', type=str, help='仅处理指定公司')
    args = parser.parse_args()

    base_dir = "/Users/panxiaoli/Desktop/投资大佬agent知识库"
    input_file = os.path.join(base_dir, "js/companyData.js")
    output_file = os.path.join(base_dir, "js/companyData_processed.js")
    wiki_output_dir = os.path.join(base_dir, "wiki/entities")

    if not os.path.exists(input_file):
        print(f"错误: 文件不存在 {input_file}")
        return

    if args.dry_run:
        print("Dry run 模式 - 仅分析数据，不生成文件")
        # TODO: 实现干运行模式
        return

    process_company_data(input_file, output_file, wiki_output_dir, args.company)

if __name__ == "__main__":
    import os
    main()
