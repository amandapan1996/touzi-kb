#!/usr/bin/env python3
"""
网站数据更新脚本
- 把雪球数据转换成网站格式
- 生成网站需要的数据文件
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# 路径
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
RAW_DIR = PROJECT_DIR / "raw" / "xueqiu"
WEBSITE_DIR = PROJECT_DIR / "website"


def load_xueqiu_posts():
    """加载雪球帖子"""
    posts_file = RAW_DIR / "duanyongping_posts.json"
    if not posts_file.exists():
        print("⚠️  没有找到雪球数据文件")
        return []

    with open(posts_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("posts", [])


def generate_company_timeline(posts):
    """按公司生成时间线"""
    companies = defaultdict(list)

    for post in posts:
        for company in post.get("companies", []):
            companies[company["name"]].append({
                "date": post.get("created_at_str", ""),
                "text": post["text"],
                "url": post.get("url", ""),
            })

    # 转成字典
    return {name: posts for name, posts in companies.items()}


def generate_timeline(posts, limit=100):
    """生成最新帖子时间线"""
    return posts[:limit]


def update_website_data():
    """更新网站数据"""
    print("📊 开始更新网站数据...")

    posts = load_xueqiu_posts()
    if not posts:
        print("❌ 没有数据")
        return

    print(f"   加载了 {len(posts)} 条帖子")

    # 生成网站数据
    data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_posts": len(posts),
        "timeline": generate_timeline(posts),
        "company_timeline": generate_company_timeline(posts),
    }

    # 保存到 website/js/xueqiu_data.js
    output_file = WEBSITE_DIR / "js" / "xueqiu_data.js"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"// 自动生成 - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"window.XUEQIU_DATA = ")
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write(";")

    print(f"✅ 已更新: {output_file}")


if __name__ == "__main__":
    update_website_data()
