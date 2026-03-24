#!/usr/bin/env python3
"""
抖音指数日报 V2 - 7天vs30天对比
本项目 + 5个竞品景区抖音指数对比分析

景区列表：
- 本项目：建业电影小镇
- 竞品：只有河南、银基动物王国、万岁山武侠城、方特欢乐世界、清明上河园

使用方法：
python3 douyin_index_report_v2.py
"""

import os
import json
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional

# 景区列表
SCENICS = [
    {"name": "建业电影小镇", "type": "本项目"},
    {"name": "只有河南", "type": "竞品"},
    {"name": "银基动物王国", "type": "竞品"},
    {"name": "万岁山武侠城", "type": "竞品"},
    {"name": "方特欢乐世界", "type": "竞品"},
    {"name": "清明上河园", "type": "竞品"},
]

# 数据存储文件
DATA_FILE = os.path.expanduser("~/.openclaw/data/douyin_index_history.json")

@dataclass
class DouyinIndex:
    keyword: str
    search_avg: str  # 搜索指数平均值
    search_trend: str  # 同比/环比
    composite_avg: str  # 综合指数平均值
    composite_trend: str
    period: str  # "7天" 或 "30天"

def load_history() -> dict:
    """加载历史数据"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_history(data: dict):
    """保存历史数据"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_card_message(scenics: list, period: str = "7天") -> str:
    """生成卡片表格消息"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    header = f"""## 📊 抖音指数日报 ({today})
### 📅 周期：{period}数据

| 景区 | 类型 | 搜索指数 | 趋势 | 综合指数 | 趋势 |
|------|------|----------|------|----------|------|
"""
    
    rows = []
    for s in scenics:
        name = s.get('name', '')
        scenic_type = s.get('type', '竞品')
        search_avg = s.get('search_avg', '-')
        search_trend = s.get('search_trend', '-')
        综合_avg = s.get('综合_avg', '-')
        综合_trend = s.get('综合_trend', '-')
        
        rows.append(f"| {name} | {scenic_type} | {search_avg} | {search_trend} | {综合_avg} | {综合_trend} |")
    
    return header + "\n".join(rows)

def generate_compare_message(data_7d: list, data_30d: list) -> str:
    """生成7天vs30天对比消息"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 构建对比表格
    header = f"""## 📊 抖音指数日报 ({today})
### 🔄 7天 vs 30天 对比

| 景区 | 类型 | 7天搜索指数 | 7天趋势 | 30天搜索指数 | 30天趋势 |
|------|------|-------------|---------|--------------|----------|
"""
    
    # 合并数据
    rows = []
    for i, scenic in enumerate(SCENICS):
        name = scenic['name']
        scenic_type = scenic['type']
        
        d7 = data_7d[i] if i < len(data_7d) else {}
        d30 = data_30d[i] if i < len(data_30d) else {}
        
        search_7d = d7.get('search_avg', '-')
        trend_7d = d7.get('search_trend', '-')
        search_30d = d30.get('search_avg', '-')
        trend_30d = d30.get('search_trend', '-')
        
        rows.append(f"| {name} | {scenic_type} | {search_7d} | {trend_7d} | {search_30d} | {trend_30d} |")
    
    footer = """

---
**数据来源**：抖音指数 (https://creator.douyin.com/creator-micro/creator-count/arithmetic-index)
**更新说明**：请打开浏览器访问抖音指数，手动更新各景区数据"""
    
    return header + "\n".join(rows) + footer

def generate_simple_message(data: dict, period: str = "7天") -> str:
    """生成简化的文本消息（供定时任务使用）"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    msg = f"""📊 抖音指数日报 ({today}) - {period}数据

🏰 本项目 vs 竞品景区抖音指数对比

| 景区 | 搜索指数 | 趋势 | 综合指数 | 趋势 |
|------|----------|------|----------|------|
"""
    
    for s in SCENICS:
        name = s['name']
        scenic_type = s['type']
        d = data.get(name, {})
        
        search_avg = d.get('search_avg', '-')
        search_trend = d.get('search_trend', '-')
        综合_avg = d.get('综合_avg', '-')
        综合_trend = d.get('综合_trend', '-')
        
        msg += f"| {name}({scenic_type}) | {search_avg} | {search_trend} | {综合_avg} | {综合_trend} |\n"
    
    return msg

def generate_feishu_card(data: dict, period: str = "7天") -> dict:
    """生成飞书卡片消息格式"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 构建表格内容
    rows = []
    for s in SCENICS:
        name = s['name']
        scenic_type = s['type']
        d = data.get(name, {})
        
        search_avg = d.get('search_avg', '-')
        search_trend = d.get('search_trend', '-')
        综合_avg = d.get('综合_avg', '-')
        综合_trend = d.get('综合_trend', '-')
        
        rows.append([
            {"tag": "text", "content": name},
            {"tag": "text", "content": scenic_type},
            {"tag": "text", "content": search_avg},
            {"tag": "text", "content": search_trend},
            {"tag": "text", "content": 综合_avg},
            {"tag": "text", "content": 综合_trend},
        ])
    
    # 飞书卡片模板
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"📊 抖音指数日报 ({today}) - {period}数据"
            },
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**🏰 本项目 vs 竞品景区抖音指数对比**"
                }
            },
            {
                "tag": "table",
                "trs": [
                    {
                        "ths": [
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**景区**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**类型**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**搜索指数**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**趋势**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**综合指数**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**趋势**"}},
                        ]
                    },
                    *[
                        {
                            "tds": [
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[0]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[1]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[2]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[3]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[4]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[5]["content"]}},
                            ]
                        }
                        for row in rows
                    ]
                ]
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "📌 数据来源：[抖音指数](https://creator.douyin.com/creator-micro/creator-count/arithmetic-index)"
                }
            }
        ]
    }
    
    return card

def generate_feishu_compare_card(data_7d: dict, data_30d: dict) -> dict:
    """生成7天vs30天对比的飞书卡片"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    rows = []
    for s in SCENICS:
        name = s['name']
        scenic_type = s['type']
        
        d7 = data_7d.get(name, {})
        d30 = data_30d.get(name, {})
        
        search_7d = d7.get('search_avg', '-')
        trend_7d = d7.get('search_trend', '-')
        search_30d = d30.get('search_avg', '-')
        trend_30d = d30.get('search_trend', '-')
        
        rows.append([
            {"tag": "text", "content": name},
            {"tag": "text", "content": scenic_type},
            {"tag": "text", "content": search_7d},
            {"tag": "text", "content": trend_7d},
            {"tag": "text", "content": search_30d},
            {"tag": "text", "content": trend_30d},
        ])
    
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"📊 抖音指数日报 ({today}) - 7天 vs 30天对比"
            },
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**🔄 7天 vs 30天 对比分析**"
                }
            },
            {
                "tag": "table",
                "trs": [
                    {
                        "ths": [
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**景区**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**类型**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**7天搜索**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**7天趋势**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**30天搜索**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**30天趋势**"}},
                        ]
                    },
                    *[
                        {
                            "tds": [
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[0]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[1]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[2]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[3]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[4]["content"]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[5]["content"]}},
                            ]
                        }
                        for row in rows
                    ]
                ]
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "📌 数据来源：[抖音指数](https://creator.douyin.com/creator-micro/creator-count/arithmetic-index)"
                }
            }
        ]
    }
    
    return card

def update_data(keyword: str, period: str, search_avg: str, search_trend: str, 综合_avg: str, 综合_trend: str):
    """更新数据"""
    data = load_history()
    
    if period not in data:
        data[period] = {}
    
    data[period][keyword] = {
        "search_avg": search_avg,
        "search_trend": search_trend,
        "综合_avg": 综合_avg,
        "综合_trend": 综合_trend,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    save_history(data)
    print(f"✅ 已更新 {keyword} ({period}) 数据")

def show_current_data():
    """显示当前数据"""
    data = load_history()
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n{'='*60}")
    print(f"📊 抖音指数日报 ({today})")
    print(f"{'='*60}\n")
    
    # 7天数据
    if "7天" in data:
        print("📅 7天数据:")
        print("-" * 40)
        for s in SCENICS:
            name = s['name']
            d = data["7天"].get(name, {})
            if d:
                print(f"  {name}: 搜索{d.get('search_avg','-')} ({d.get('search_trend','-')})")
        print()
    
    # 30天数据
    if "30天" in data:
        print("📅 30天数据:")
        print("-" * 40)
        for s in SCENICS:
            name = s['name']
            d = data["30天"].get(name, {})
            if d:
                print(f"  {name}: 搜索{d.get('search_avg','-')} ({d.get('search_trend','-')})")
        print()
    
    # 7天 vs 30天 对比
    if "7天" in data and "30天" in data:
        print("🔄 7天 vs 30天 对比:")
        print("-" * 60)
        print(f"| 景区 | 类型 | 7天搜索 | 7天趋势 | 30天搜索 | 30天趋势 |")
        print(f"|------|------|---------|---------|----------|---------|")
        for s in SCENICS:
            name = s['name']
            scenic_type = s['type']
            d7 = data["7天"].get(name, {})
            d30 = data["30天"].get(name, {})
            
            search_7d = d7.get('search_avg', '-')
            trend_7d = d7.get('search_trend', '-')
            search_30d = d30.get('search_avg', '-')
            trend_30d = d30.get('search_trend', '-')
            
            print(f"| {name} | {scenic_type} | {search_7d} | {trend_7d} | {search_30d} | {trend_30d} |")
    
    print(f"\n{'='*60}")
    print("💡 使用说明:")
    print("   1. 手动更新数据: python3 douyin_index_report_v2.py --update")
    print("   2. 查看日报: python3 douyin_index_report_v2.py --report")
    print("   3. 生成飞书卡片: python3 douyin_index_report_v2.py --card")
    print(f"{'='*60}\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='抖音指数日报工具')
    parser.add_argument('--update', action='store_true', help='更新数据')
    parser.add_argument('--report', action='store_true', help='显示日报')
    parser.add_argument('--card', action='store_true', help='生成飞书卡片JSON')
    parser.add_argument('--keyword', type=str, help='关键词')
    parser.add_argument('--period', type=str, default='30天', choices=['7天', '30天'], help='周期')
    parser.add_argument('--search', type=str, help='搜索指数平均值')
    parser.add_argument('--trend', type=str, help='搜索趋势')
    parser.add_argument('--composite', type=str, help='综合指数平均值')
    parser.add_argument('--composite-trend', type=str, help='综合指数趋势')
    
    args = parser.parse_args()
    
    if args.update:
        if args.keyword:
            update_data(
                args.keyword,
                args.period,
                args.search or '-',
                args.trend or '-',
                args.composite or '-',
                args.composite_trend or '-'
            )
        else:
            show_current_data()
    elif args.card:
        data = load_history()
        card = generate_feishu_compare_card(data.get("7天", {}), data.get("30天", {}))
        print(json.dumps(card, ensure_ascii=False, indent=2))
    elif args.report:
        show_current_data()
    else:
        show_current_data()

if __name__ == "__main__":
    main()
