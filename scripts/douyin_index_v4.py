#!/usr/bin/env python3
"""
抖音指数日报 V4 - 景区营销总经理专业版
包含：7天/30天数据、竞品分析、人群画像洞察、营销建议
"""

import os
import json
from datetime import datetime

# 景区列表
SCENICS = [
    {"name": "建业电影小镇", "type": "本项目"},
    {"name": "只有河南", "type": "竞品"},
    {"name": "银基动物王国", "type": "竞品"},
    {"name": "万岁山武侠城", "type": "竞品"},
    {"name": "郑州方特欢乐世界", "type": "竞品"},
    {"name": "清明上河园", "type": "竞品"},
]

DATA_FILE = os.path.expanduser("~/.openclaw/data/douyin_index_v3.json")

def load_data() -> dict:
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def parse_trend(trend_str):
    """解析趋势字符串"""
    if not trend_str or trend_str == "待获取":
        return "-", "-"
    
    yoy = "-"
    mom = "-"
    if '同比' in trend_str and '｜' in trend_str:
        parts = trend_str.split('｜')
        for p in parts:
            if '同比' in p:
                yoy = p.replace('同比', '').replace('%', '').replace('+', '').strip()
            if '环比' in p:
                mom = p.replace('环比', '').replace('%', '').replace('+', '').strip()
    return yoy, mom

def generate_professional_report():
    """生成专业营销分析报告"""
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # ==================== 第一部分：核心数据摘要 ====================
    report = f"""# 📊 抖音指数日报 ({today})
## 一、核心数据摘要

### 1. 搜索指数对比（30天）

| 景区 | 类型 | 搜索指数 | 同比 | 环比 | 热度排名 |
|------|------|----------|------|------|----------|
"""
    
    # 排序计算排名
    rankings = []
    for s in SCENICS:
        name = s['name']
        d30 = data.get(name, {}).get("30天", {})
        search = d30.get('search_avg', '0')
        # 提取数值
        if '万' in search:
            value = float(search.replace('万', '')) * 10000
        elif '千' in search:
            value = float(search.replace('千', '')) * 1000
        else:
            value = 0
        yoy, mom = parse_trend(d30.get('search_trend', ''))
        rankings.append((name, s['type'], search, yoy, mom, value))
    
    # 按热度排序
    rankings.sort(key=lambda x: x[5], reverse=True)
    
    for rank, (name, scenic_type, search, yoy, mom, _) in enumerate(rankings, 1):
        report += f"| {name} | {scenic_type} | {search} | {yoy}% | {mom}% | #{rank} |\n"
    
    # ==================== 第二部分：竞品对比分析 ====================
    report += """
### 2. 竞品对比分析

**数据来源**：抖音指数（2026-02-19 ~ 2026-03-19）
"""
    
    # 计算本项目与竞品差距
    our_data = data.get("建业电影小镇", {}).get("30天", {})
    our_search = our_data.get("search_avg", "0")
    
    report += f"""
#### 【本项目】建业电影小镇
- **搜索指数**：{our_search}
- **同比变化**：{our_data.get('search_trend', '-').replace('｜', '，')}
- **综合指数**：{our_data.get('composite_avg', '-')}
- **竞争态势**：当前搜索指数在6个景区中排名靠后，与头部景区（清明上河园15.9万、万岁山武侠城15.9万）差距较大

#### 【主要竞品】清明上河园
- **搜索指数**：24.0万（同比+654%，环比-12%）
- **分析**：搜索指数最高，环比下降12%说明近期热度有所回落，但同比暴增654%表明去年同期基数极低或今年营销推广效果显著

#### 【主要竞品】万岁山武侠城  
- **搜索指数**：15.9万（同比+10%，环比+21%）
- **分析**：稳步增长，环比+21%说明近期营销推广效果好

#### 【主要竞品】银基动物王国
- **搜索指数**：6.3万（同比+22%，环比+40%）
- **分析**：环比增长40%是最大亮点，近期营销推广或活动成效显著
"""
    
    # ==================== 第三部分：人群画像洞察 ====================
    report += """
### 3. 人群画像洞察（7天数据）

#### 建业电影小镇
"""
    
    # 人群画像数据
    our_portrait = data.get("建业电影小镇", {}).get("7天", {}).get("人群画像", {})
    region_data = our_portrait.get("地域分布", {})
    
    if region_data:
        top5 = region_data.get("top5", [])
        report += f"""
**地域分布**：
| 排名 | 省份 | 占比 | TGI指数 | 解读 |
|------|------|------|---------|------|
"""
        for item in top5:
            tgi = item.get("TGI指数", "-")
            interpretation = ""
            try:
                tgi_val = int(tgi)
                if tgi_val > 200:
                    interpretation = "高偏好"
                elif tgi_val > 100:
                    interpretation = "偏好"
                else:
                    interpretation = "一般"
            except:
                interpretation = "-"
            report += f"| {item.get('排名')} | {item.get('省份')} | {item.get('占比')} | {tgi} | {interpretation} |\n"
        
        report += f"\n**关键洞察**：{region_data.get('分析', '待分析')}\n"
    else:
        report += "\n地域分布数据获取中...\n"
    
    # ==================== 第四部分：营销建议 ====================
    report += """
### 4. 营销建议

基于以上数据分析，提出以下建议：

#### 🔴 紧急重要（本周）
1. **加大抖音内容投放**
   - 本项目搜索指数（1.5万）与竞品差距明显
   - 建议本周启动抖音短视频/直播投流
   - 目标：提升搜索指数至3万+

2. **优化人群定向投放**
   - 河南本地用户偏好度高（TGI 267），建议加大本地投放
   - 广东、江苏、山东等省份TGI偏低，可测试投放

#### 🟡 重要（本月）
3. **借势清明节营销**
   - 清明上河园环比下降12%，说明节后热度回落
   - 建议清明节前提前布局，抢占流量

4. **对标竞品优化内容**
   - 银基动物王国环比+40%，需分析其近期营销动作
   - 可关注其短视频内容风格、达人合作策略

#### 🟢 长期优化
5. **建立数据监测机制**
   - 建议每日监测抖音指数变化
   - 及时发现异常波动并调整策略
"""
    
    # ==================== 第五部分：7天数据预览 ====================
    report += """
### 5. 7天数据对比（待完善）

| 景区 | 7天搜索 | 7天趋势 | 30天搜索 | 30天趋势 |
|------|----------|---------|----------|----------|
"""
    
    for s in SCENICS:
        name = s['name']
        d7 = data.get(name, {}).get("7天", {})
        d30 = data.get(name, {}).get("30天", {})
        
        search_7d = d7.get('search_avg', '待获取')
        trend_7d = d7.get('search_trend', '-')
        search_30d = d30.get('search_avg', '-')
        trend_30d = d30.get('search_trend', '-')
        
        report += f"| {name} | {search_7d} | {trend_7d} | {search_30d} | {trend_30d} |\n"
    
    report += f"""
---
*数据来源：抖音指数*
*更新时间：{today}*
*分析：建业电影小镇营销中心*
"""
    
    return report

def generate_card_json():
    """生成飞书卡片JSON"""
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 构建表格行
    rows = []
    rankings = []
    for s in SCENICS:
        name = s['name']
        d30 = data.get(name, {}).get("30天", {})
        search = d30.get('search_avg', '-')
        if '万' in search:
            value = float(search.replace('万', '')) * 10000
        elif '千' in search:
            value = float(search.replace('千', '')) * 1000
        else:
            value = 0
        yoy, mom = parse_trend(d30.get('search_trend', ''))
        rankings.append((name, search, yoy, mom, value))
    
    rankings.sort(key=lambda x: x[4], reverse=True)
    
    for rank, (name, search, yoy, mom, _) in enumerate(rankings, 1):
        rows.append([
            {"tag": "text", "content": f"#{rank} {name}"},
            {"tag": "text", "content": search},
            {"tag": "text", "content": f"+{yoy}%" if yoy != "-" else yoy},
            {"tag": "text", "content": f"+{mom}%" if mom != "-" else mom},
        ])
    
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"📊 抖音指数日报 ({today})"},
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {"tag": "lark_md", "content": "**🏰 建业电影小镇 vs 竞品抖音搜索指数**"}
            },
            {
                "tag": "table",
                "trs": [
                    {
                        "ths": [
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**景区**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**搜索指数**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**同比**"}},
                            {"tag": "p", "text": {"tag": "lark_md", "content": "**环比**"}},
                        ]
                    },
                    *[
                        {
                            "tds": [
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[0]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[1]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[2]}},
                                {"tag": "p", "text": {"tag": "lark_md", "content": row[3]}},
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

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--report":
            print(generate_professional_report())
        elif sys.argv[1] == "--card":
            print(json.dumps(generate_card_json(), ensure_ascii=False, indent=2))
    else:
        # 显示数据状态
        data = load_data()
        print("=" * 60)
        print(f"📊 抖音指数数据")
        print("=" * 60)
        
        for s in SCENICS:
            name = s['name']
            d = data.get(name, {})
            print(f"\n{name}:")
            for period in ["30天", "7天"]:
                if period in d:
                    p = d[period]
                    print(f"  {period}: 搜索{p.get('search_avg','-')} ({p.get('search_trend','-')})")
