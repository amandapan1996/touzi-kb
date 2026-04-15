#!/usr/bin/env python3
"""
雪球增量爬虫 - 段永平（增强版）
- 支持增量更新（只爬新帖子）
- 自动发现新提到的公司
- 记录公司提及时间线

使用方法:
1. 配置Cookie: 编辑本文件第28行
2. 首次运行: python3 scripts/crawl_xueqiu.py --full
3. 增量更新: python3 scripts/crawl_xueqiu.py
"""

import requests
import json
import time
import os
import re
from datetime import datetime
from pathlib import Path

# ============ 配置区 ============
# 段永平的雪球用户ID (大道无形我有型)
XUEQIU_USER_ID = "5497652514"

# 雪球Cookie (登录后从浏览器复制)
# 优先级: 命令行参数 > 环境变量 > 这里配置的默认值
COOKIE = os.environ.get("XUEQIU_COOKIE", "e3118a66020384f18b8fdae7f409604396bae918")  # 雪球认证Cookie

# 输出目录
OUTPUT_DIR = Path("raw/xueqiu")
STATE_FILE = OUTPUT_DIR / "crawl_state.json"  # 记录爬取状态
# ============ 配置区结束 ============

# 已知公司列表（用于识别）
KNOWN_COMPANIES = {
    # 主要持仓/历史持仓
    "腾讯": {"symbol": "00700", "category": "stock"},
    "腾讯控股": {"symbol": "00700", "category": "stock"},
    "苹果": {"symbol": "AAPL", "category": "stock"},
    "贵州茅台": {"symbol": "600519", "category": "stock"},
    "茅台": {"symbol": "600519", "category": "stock"},
    "网易": {"symbol": "NTES", "category": "stock"},
    "阿里巴巴": {"symbol": "BABA", "category": "stock"},
    "阿里": {"symbol": "BABA", "category": "stock"},
    "拼多多": {"symbol": "PDD", "category": "stock"},
    "谷歌": {"symbol": "GOOGL", "category": "watching"},
    "Google": {"symbol": "GOOGL", "category": "watching"},
    "亚马逊": {"symbol": "AMZN", "category": "watching"},
    "特斯拉": {"symbol": "TSLA", "category": "watching"},
    "比亚迪": {"symbol": "002594", "category": "watching"},
    "百度": {"symbol": "BIDU", "category": "lesson"},
    "雅虎": {"symbol": "YHOO", "category": "watching"},
    # 创业/关联公司
    "OPPO": {"symbol": "", "category": "entrepreneur"},
    "vivo": {"symbol": "", "category": "entrepreneur"},
    "步步高": {"symbol": "", "category": "entrepreneur"},
    "小霸王": {"symbol": "", "category": "entrepreneur"},
    # 关注公司
    "万科": {"symbol": "000002", "category": "watching"},
    "平安": {"symbol": "601318", "category": "watching"},
    "京东": {"symbol": "JD", "category": "watching"},
    "美的": {"symbol": "000333", "category": "watching"},
    "格力": {"symbol": "000651", "category": "watching"},
    "五粮液": {"symbol": "000858", "category": "watching"},
    "可口可乐": {"symbol": "KO", "category": "watching"},
    "GE": {"symbol": "GE", "category": "watching"},
    "IBM": {"symbol": "IBM", "category": "watching"},
    "微软": {"symbol": "MSFT", "category": "watching"},
    "Facebook": {"symbol": "META", "category": "watching"},
    "Meta": {"symbol": "META", "category": "watching"},
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Origin": "https://xueqiu.com",
    "Referer": f"https://xueqiu.com/u/{XUEQIU_USER_ID}",
    "Cookie": COOKIE,
}


def load_state():
    """加载爬取状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"last_post_id": None, "last_crawl_time": None, "total_crawled": 0}


def save_state(state):
    """保存爬取状态"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_company_config():
    """加载公司配置"""
    config_file = OUTPUT_DIR / "companies_config.json"
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"companies": {}, "discovered_companies": []}


def save_company_config(config):
    """保存公司配置"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config_file = OUTPUT_DIR / "companies_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def extract_companies_from_text(text):
    """从文本中提取公司"""
    found = []
    for company, info in KNOWN_COMPANIES.items():
        if company in text:
            found.append({
                "name": company,
                "symbol": info["symbol"],
                "category": info["category"]
            })
    return found


def extract_topics(text):
    """从文本中提取话题"""
    topics = re.findall(r'#([^#]+)#', text)
    return topics


def get_posts(page=1, count=20, max_id=None):
    """获取用户帖子"""
    url = "https://xueqiu.com/v4/statuses/user_timeline.json"
    params = {
        "user_id": XUEQIU_USER_ID,
        "page": page,
        "count": count,
    }
    if max_id:
        params["max_id"] = max_id

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)

        if response.status_code == 401:
            print("❌ Cookie已过期或无效，请重新获取")
            return None, None

        if response.status_code != 200:
            print(f"❌ 请求失败: {response.status_code}")
            return None, None

        data = response.json()
        return data, data.get("next_max_id")

    except requests.exceptions.Timeout:
        print("⏰ 请求超时，重试中...")
        return None, None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None, None


def parse_post(post):
    """解析帖子数据"""
    created_at = post.get("created_at", 0)
    created_at_str = datetime.fromtimestamp(created_at / 1000).strftime("%Y-%m-%d %H:%M") if created_at else ""

    text = post.get("text", "")

    return {
        "id": post.get("id"),
        "created_at": created_at,
        "created_at_str": created_at_str,
        "text": text,
        "text_raw": post.get("text_raw", ""),
        "like_count": post.get("like_count", 0),
        "reply_count": post.get("reply_count", 0),
        "retweet_count": post.get("retweet_count", 0),
        "source": post.get("source", ""),
        "companies": extract_companies_from_text(text),
        "topics": extract_topics(text),
        "url": f"https://xueqiu.com/{XUEQIU_USER_ID}/{post.get('id')}",
    }


def discover_new_companies(posts, config):
    """发现帖子中的新公司"""
    discovered = []
    for post in posts:
        for company in post.get("companies", []):
            name = company["name"]
            # 如果是已知公司
            if name in KNOWN_COMPANIES:
                # 更新首次提及时间
                if name not in config["companies"]:
                    config["companies"][name] = {
                        "symbol": company["symbol"],
                        "category": company["category"],
                        "first_mentioned": post["created_at_str"],
                        "mention_count": 1,
                        "quotes": []
                    }
                else:
                    config["companies"][name]["mention_count"] += 1
            # 如果是新发现的公司
            else:
                if name not in config["discovered_companies"]:
                    config["discovered_companies"].append(name)
                    discovered.append({
                        "name": name,
                        "first_mentioned": post["created_at_str"],
                        "post_id": post["id"]
                    })
                    print(f"   🆕 发现新公司: {name}")
    return discovered


def crawl_posts_incremental(max_pages=20):
    """增量爬取（只爬取新帖子）"""
    state = load_state()
    last_id = state.get("last_post_id")

    new_posts = []
    page = 1
    max_id = None

    print("📡 开始增量爬取...")

    while page <= max_pages:
        print(f"   第 {page} 页...", end=" ")

        data, next_max_id = get_posts(page=page, count=20, max_id=max_id)

        if data is None:
            print("失败")
            break

        posts = data.get("statuses", [])
        if not posts:
            print("无更多帖子")
            break

        for post in posts:
            post_id = post.get("id")

            # 如果遇到上次爬过的帖子，停止
            if last_id and post_id == last_id:
                print(f"遇到已爬帖子，停止")
                return new_posts

            parsed = parse_post(post)
            new_posts.append(parsed)

        print(f"获取 {len(posts)} 条，新增 {len(new_posts)} 条")

        # 检查是否遇到边界
        if not next_max_id or next_max_id == max_id:
            break

        max_id = next_max_id
        page += 1

        # 随机延时 2-5 秒
        time.sleep(2 + int(time.time()) % 4)

    return new_posts


def crawl_posts_full(max_pages=100):
    """全量爬取（首次使用）"""
    all_posts = []
    page = 1
    max_id = None

    print("📡 开始全量爬取...")

    while page <= max_pages:
        print(f"   第 {page} 页...", end=" ")

        data, next_max_id = get_posts(page=page, count=20, max_id=max_id)

        if data is None:
            print("失败，保存已获取的")
            break

        posts = data.get("statuses", [])
        if not posts:
            print("无更多帖子")
            break

        for post in posts:
            parsed = parse_post(post)
            all_posts.append(parsed)

        print(f"获取 {len(posts)} 条，累计 {len(all_posts)} 条")

        if not next_max_id or next_max_id == max_id:
            break

        max_id = next_max_id
        page += 1

        # 随机延时
        time.sleep(2 + int(time.time()) % 4)

    return all_posts


def merge_posts(new_posts):
    """合并新帖子到已有数据"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 读取已有数据
    existing_file = OUTPUT_DIR / "duanyongping_posts.json"
    existing_posts = []

    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            existing_posts = data.get("posts", [])

    # 去重合并
    existing_ids = {p["id"] for p in existing_posts}
    merged_posts = []

    for post in new_posts:
        if post["id"] not in existing_ids:
            merged_posts.append(post)

    # 按时间排序（新的在前）
    all_posts = merged_posts + existing_posts
    all_posts.sort(key=lambda x: x.get("created_at", 0), reverse=True)

    return all_posts, len(merged_posts)


def save_posts(posts, is_incremental=False):
    """保存帖子"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 保存完整数据
    filepath = OUTPUT_DIR / "duanyongping_posts.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "source": "雪球",
            "user_id": XUEQIU_USER_ID,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_count": len(posts),
            "posts": posts
        }, f, ensure_ascii=False, indent=2)

    print(f"💾 已保存到 {filepath}")

    # 保存今天的增量
    if is_incremental and posts:
        today_file = OUTPUT_DIR / f"incremental_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(today_file, "w", encoding="utf-8") as f:
            json.dump({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "count": len(posts),
                "posts": posts
            }, f, ensure_ascii=False, indent=2)
        print(f"📝 今日增量已保存: {today_file}")

    return filepath


def update_company_config(posts):
    """更新公司配置"""
    config = load_company_config()

    # 更新公司数据
    for post in posts:
        for company in post.get("companies", []):
            name = company["name"]
            if name in KNOWN_COMPANIES:
                if name not in config["companies"]:
                    config["companies"][name] = {
                        "symbol": company["symbol"],
                        "category": company["category"],
                        "first_mentioned": post["created_at_str"],
                        "mention_count": 1,
                        "quotes": []
                    }
                else:
                    config["companies"][name]["mention_count"] += 1

    save_company_config(config)
    return config


def main():
    import argparse

    parser = argparse.ArgumentParser(description="雪球爬虫")
    parser.add_argument("--full", action="store_true", help="全量爬取（首次使用）")
    parser.add_argument("--cookie", type=str, help="通过命令行传递Cookie")
    args = parser.parse_args()

    print("=" * 50)
    print("雪球帖子爬虫 - 段永平（增强版）")
    print("=" * 50)

    # 允许命令行传入Cookie
    global COOKIE, HEADERS
    if args.cookie:
        COOKIE = args.cookie
        HEADERS["Cookie"] = COOKIE

    if not COOKIE:
        print("\n⚠️  警告: Cookie未设置，爬取可能失败")
        print("请编辑本文件，填入有效的Cookie值\n")

    state = load_state()

    if args.full:
        # 全量爬取
        posts = crawl_posts_full()
        is_incremental = False
    else:
        # 增量爬取
        posts = crawl_posts_incremental()
        is_incremental = True

    if posts:
        # 发现新公司
        print("\n🔍 检查新提及的公司...")
        config = load_company_config()
        discovered = discover_new_companies(posts, config)

        if discovered:
            print(f"\n🆕 发现 {len(discovered)} 个新公司:")
            for d in discovered:
                print(f"   - {d['name']} (首次提及: {d['first_mentioned']})")

        # 更新公司配置
        update_company_config(posts)

        # 合并到已有数据
        all_posts, new_count = merge_posts(posts)
        save_posts(all_posts, is_incremental)

        # 更新状态
        state["last_post_id"] = posts[0]["id"] if posts else state.get("last_post_id")
        state["last_crawl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state["total_crawled"] = state.get("total_crawled", 0) + len(posts)
        save_state(state)

        print("\n" + "=" * 50)
        print(f"✅ 完成! 本次新增 {len(posts)} 条")
        print(f"   累计 {len(all_posts)} 条帖子")
        print(f"   累计发现 {len(config['discovered_companies'])} 个潜在新公司")
        print("=" * 50)

        # 统计
        if posts:
            print(f"\n📊 本次统计:")
            print(f"   - 时间范围: {posts[-1]['created_at_str']} ~ {posts[0]['created_at_str']}")

            # 统计公司提及
            all_companies = {}
            for p in posts:
                for c in p.get("companies", []):
                    name = c["name"]
                    all_companies[name] = all_companies.get(name, 0) + 1

            if all_companies:
                print(f"   - 提及的公司: {', '.join(f'{k}({v})' for k, v in sorted(all_companies.items(), key=lambda x: -x[1])[:5])}")
    else:
        print("\n❌ 爬取失败，请检查Cookie或网络连接")


if __name__ == "__main__":
    main()
