#!/usr/bin/env python3
"""
抖音指数日报 V3 - 完整版
包含：7天/30天数据、关键词指数、关联分析、人群画像、综合指数

景区列表：
- 本项目：建业电影小镇
- 竞品：只有河南、银基动物王国、万岁山武侠城、方特欢乐世界、清明上河园
"""

import os
import json
from datetime import datetime, timedelta

# 景区列表
SCENICS = [
    {"name": "建业电影小镇", "type": "本项目"},
    {"name": "只有河南", "type": "竞品"},
    {"name": "银基动物王国", "type": "竞品"},
    {"name": "万岁山武侠城", "type": "竞品"},
    {"name": "郑州方特欢乐世界", "type": "竞品"},
    {"name": "清明上河园", "type": "竞品"},
]

# 数据存储文件
DATA_FILE = os.path.expanduser("~/.openclaw/data/douyin_index_v3.json")

def load_data() -> dict:
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data: dict):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_report():
    """生成完整日报"""
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# 📊 抖音指数日报 ({today})

## 一、搜索指数对比（30天）

| 景区 | 类型 | 搜索指数 | 同比 | 环比 |
|------|------|----------|------|------|
"""
    
    for s in SCENICS:
        name = s['name']
        scenic_type = s['type']
        d = data.get(name, {}).get("30天", {})
        
        search = d.get('search_avg', '-')
        trend = d.get('search_trend', '-')
        
        # 解析趋势
        yoy = "-"  # 同比
        mom = "-"  # 环比
        if '同比' in trend and '｜' in trend:
            parts = trend.split('｜')
            for p in parts:
                if '同比' in p:
                    yoy = p.replace('同比', '').replace('%', '').strip()
                if '环比' in p:
                    mom = p.replace('环比', '').replace('%', '').strip()
        
        report += f"| {name} | {scenic_type} | {search} | {yoy}% | {mom}% |\n"
    
    report += f"""
## 二、搜索指数对比（7天）

| 景区 | 类型 | 搜索指数 | 同比 | 环比 |
|------|------|----------|------|------|
"""
    
    for s in SCENICS:
        name = s['name']
        scenic_type = s['type']
        d = data.get(name, {}).get("7天", {})
        
        search = d.get('search_avg', '-')
        trend = d.get('search_trend', '-')
        
        yoy = "-"
        mom = "-"
        if '同比' in trend and '｜' in trend:
            parts = trend.split('｜')
            for p in parts:
                if '同比' in p:
                    yoy = p.replace('同比', '').replace('%', '').strip()
                if '环比' in p:
                    mom = p.replace('环比', '').replace('%', '').strip()
        
        report += f"| {name} | {scenic_type} | {search} | {yoy}% | {mom}% |\n"
    
    report += """
## 三、7天 vs 30天 趋势变化

"""
    
    for s in SCENICS:
        name = s['name']
        d7 = data.get(name, {}).get("7天", {})
        d30 = data.get(name, {}).get("30天", {})
        
        search_7d = d7.get('search_avg', '-')
        search_30d = d30.get('search_avg', '-')
        
        report += f"- **{name}**: 7天={search_7d}, 30天={search_30d}\n"
    
    report += f"""
## 四、人群画像分析（待完善）

### 建业电影小镇
- 地域分布：待获取
- 年龄分布：待获取
- 性别比例：待获取

### 竞品对比
- 待完善...

## 五、综合指数（待完善）

| 景区 | 综合指数 | 同比 | 环比 |
|------|----------|------|------|
"""
    
    for s in SCENICS:
        name = s['name']
        d = data.get(name, {}).get("30天", {})
        
        composite = d.get('composite_avg', '-')
        trend = d.get('composite_trend', '-')
        
        report += f"| {name} | {composite} | {trend} |\n"
    
    report += f"""
---
*数据来源：抖音指数*
*更新时间：{today}*
"""
    
    return report

def generate_card_data():
    """生成飞书卡片数据"""
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 构建表格行
    rows = []
    for s in SCENICS:
        name = s['name']
        scenic_type = s['type']
        d30 = data.get(name, {}).get("30天", {})
        d7 = data.get(name, {}).get("7天", {})
        
        search_30d = d30.get('search_avg', '-')
        trend_30d = d30.get('search_trend', '-')
        search_7d = d7.get('search_avg', '-')
        trend_7d = d7.get('search_trend', '-')
        
        rows.append([
            {"tag": "text", "content": name},
            {"tag": "text", "content": scenic_type},
            {"tag": "text", "content": search_7d},
            {"tag": "text", "content": trend_7d},
            {"tag": "text", "content": search_30d},
            {"tag": "text", "content": trend_30d},
        ])
    
    return {
        "title": f"📊 抖音指数日报 ({today})",
        "rows": rows
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--report":
            print(generate_report())
        elif sys.argv[1] == "--card":
            print(json.dumps(generate_card_data(), ensure_ascii=False, indent=2))
    else:
        # 显示当前数据状态
        data = load_data()
        print("=" * 60)
        print(f"📊 抖音指数数据 (已获取)")
        print("=" * 60)
        
        for s in SCENICS:
            name = s['name']
            d = data.get(name, {})
            print(f"\n{name}:")
            for period in ["7天", "30天"]:
                if period in d:
                    p = d[period]
                    print(f"  {period}: 搜索{p.get('search_avg','-')} ({p.get('search_trend','-')})")
                else:
                    print(f"  {period}: 待获取")
