#!/usr/bin/env python3
"""
网站数据生成脚本
- 从雪球爬取的数据生成网站可用格式
- 自动发现新公司
- 生成公司列表和语录数据

使用方法:
1. 先运行爬虫获取数据
2. python3 scripts/generate_website_data.py
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# 路径配置
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
RAW_DIR = PROJECT_DIR / "raw" / "xueqiu"
WEBSITE_DIR = PROJECT_DIR / "website"
DATA_DIR = WEBSITE_DIR / "js"


def load_xueqiu_posts():
    """加载雪球帖子数据"""
    posts_file = RAW_DIR / "duanyongping_posts.json"
    if not posts_file.exists():
        print("⚠️  没有找到雪球数据文件，请先运行爬虫")
        return []

    with open(posts_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("posts", [])


def load_company_config():
    """加载公司配置"""
    config_file = RAW_DIR / "companies_config.json"
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"companies": {}, "discovered_companies": []}


def load_existing_company_data():
    """加载已有的公司数据"""
    existing_file = WEBSITE_DIR / "js" / "companyData.js"
    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 提取JSON部分
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                return json.loads(content[start:end])
    return {}


def generate_company_list(posts, config, existing_data):
    """生成公司列表"""
    # 统计每个公司的提及次数和语录
    company_stats = defaultdict(lambda: {"mentions": 0, "posts": [], "first_mentioned": None})

    for post in posts:
        for company in post.get("companies", []):
            name = company["name"]
            company_stats[name]["mentions"] += 1
            company_stats[name]["posts"].append({
                "text": post["text"],
                "date": post["created_at_str"],
                "url": post.get("url", ""),
                "source": "帖子合集"
            })
            if not company_stats[name]["first_mentioned"] or post["created_at_str"] < company_stats[name]["first_mentioned"]:
                company_stats[name]["first_mentioned"] = post["created_at_str"]

    # 合并已有数据
    all_companies = {}

    # 先加入已有数据
    for name, data in existing_data.items():
        if name not in company_stats:
            company_stats[name] = {
                "mentions": data.get("quoteCount", 0),
                "posts": data.get("quotes", []),
                "first_mentioned": None
            }

    # 生成公司数据
    for name, stats in company_stats.items():
        # 获取分类信息
        category = "watching"
        symbol = ""

        if name in config.get("companies", {}):
            category = config["companies"][name].get("category", "watching")
            symbol = config["companies"][name].get("symbol", "")

        # 判断持仓状态
        return_info = ""
        if category == "stock":
            return_info = "持仓中"
        elif category == "lesson":
            return_info = "教训案例"

        all_companies[name] = {
            "symbol": symbol,
            "type": category,
            "returnInfo": return_info,
            "quoteCount": stats["mentions"],
            "quotes": stats["posts"][:100],  # 只保留最近100条
            "first_mentioned": stats["first_mentioned"]
        }

    return all_companies


def generate_new_companies_list(posts, config):
    """生成新提及的公司列表"""
    discovered = config.get("discovered_companies", [])

    new_companies = []
    for name in discovered:
        # 找出首次提及的帖子
        for post in posts:
            for company in post.get("companies", []):
                if company["name"] == name:
                    new_companies.append({
                        "name": name,
                        "first_mentioned": post["created_at_str"],
                        "post_url": post.get("url", ""),
                        "preview": post["text"][:200]
                    })
                    break

    return new_companies


def generate_timeline(posts, limit=50):
    """生成最新帖子时间线"""
    return [{
        "date": post.get("created_at_str", ""),
        "text": post.get("text", ""),
        "companies": [c["name"] for c in post.get("companies", [])],
        "url": post.get("url", ""),
        "like_count": post.get("like_count", 0)
    } for post in posts[:limit]]


def generate_topic_stats(posts):
    """生成话题统计"""
    topics = defaultdict(int)
    for post in posts:
        for topic in post.get("topics", []):
            topics[topic] += 1

    return sorted(topics.items(), key=lambda x: -x[1])[:20]


def generate_website_data():
    """生成网站数据"""
    print("📊 开始生成网站数据...")

    # 加载数据
    posts = load_xueqiu_posts()
    if not posts:
        print("❌ 没有数据")
        return

    config = load_company_config()
    existing_data = load_existing_company_data()

    print(f"   加载了 {len(posts)} 条帖子")
    print(f"   已有 {len(existing_data)} 个公司数据")

    # 生成数据
    companies = generate_company_list(posts, config, existing_data)
    new_companies = generate_new_companies_list(posts, config)
    timeline = generate_timeline(posts)
    topics = generate_topic_stats(posts)

    # 保存公司数据
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 生成 companyData.js
    company_data_js = f"""// 自动生成 - {datetime.now().strftime('%Y-%m-%d %H:%M')}
// 包含已知公司 + 新提及公司
const companyData = {json.dumps(companies, ensure_ascii=False, indent=2)};
"""

    with open(DATA_DIR / "companyData.js", 'w', encoding='utf-8') as f:
        f.write(company_data_js)

    print(f"✅ 已更新: {DATA_DIR / 'companyData.js'}")

    # 生成 xueqiu_data.js
    xueqiu_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_posts": len(posts),
        "total_companies": len(companies),
        "new_companies": new_companies,
        "timeline": timeline,
        "topics": [{"name": t[0], "count": t[1]} for t in topics]
    }

    xueqiu_data_js = f"""// 自动生成 - {datetime.now().strftime('%Y-%m-%d %H:%M')}
window.XUEQIU_DATA = {json.dumps(xueqiu_data, ensure_ascii=False, indent=2)};
"""

    with open(DATA_DIR / "xueqiu_data.js", 'w', encoding='utf-8') as f:
        f.write(xueqiu_data_js)

    print(f"✅ 已更新: {DATA_DIR / 'xueqiu_data.js'}")

    # 生成新公司报告
    if new_companies:
        print(f"\n🆕 新提及的公司 ({len(new_companies)}):")
        for c in new_companies[:5]:
            print(f"   - {c['name']} ({c['first_mentioned']})")
        if len(new_companies) > 5:
            print(f"   ... 还有 {len(new_companies) - 5} 个")

    print(f"\n📊 统计:")
    print(f"   - 总帖子数: {len(posts)}")
    print(f"   - 公司数量: {len(companies)}")
    print(f"   - 新提及公司: {len(new_companies)}")


if __name__ == "__main__":
    generate_website_data()
