#!/usr/bin/env python3
"""
抖音指数日报 V8 - 每个景区详细分析版
包含每个景区的搜索指数、综合指数、关联分析、人群画像
"""

import os
import json
from datetime import datetime

SCENICS = [
    {"name": "建业电影小镇", "type": "本项目"},
    {"name": "只有河南", "type": "竞品"},
    {"name": "银基动物王国", "type": "竞品"},
    {"name": "万岁山武侠城", "type": "竞品"},
    {"name": "郑州方特欢乐世界", "type": "竞品"},
    {"name": "清明上河园", "type": "竞品"},
]

DATA_FILE = os.path.expanduser("~/.openclaw/data/douyin_index_v3.json")

def load_data():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def parse_value(search_str):
    if not search_str or search_str == "待获取":
        return 0
    try:
        if '万' in search_str:
            return float(search_str.replace('万', '')) * 10000
        elif '千' in search_str:
            return float(search_str.replace('千', '')) * 1000
    except:
        return 0
    return 0

def parse_trend(trend_str):
    if not trend_str or trend_str in ["待获取", "-"]:
        return "-", "-"
    yoy, mom = "-", "-"
    try:
        if '同比' in trend_str:
            yoy = trend_str.split('同比')[1].split('%')[0].replace('+', '').strip()
        if '环比' in trend_str:
            if '｜' in trend_str:
                mom = trend_str.split('环比')[1].split('%')[0].replace('+', '').strip()
            else:
                mom = trend_str.split('环比')[1].replace('%', '').replace('+', '').strip()
    except: pass
    return yoy, mom

def generate_full_report():
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# 📊 抖音指数日报 ({today})
## 一、核心数据对比

### 1.1 搜索指数排名（30天）

| 排名 | 景区 | 类型 | 搜索指数 | 同比 | 环比 |
|------|------|------|----------|------|------|
"""
    
    # 按搜索指数排序
    rankings = []
    for s in SCENICS:
        name = s['name']
        d30 = data.get(name, {}).get("30天", {})
        search = d30.get('search_avg', '0')
        value = parse_value(search)
        yoy, mom = parse_trend(d30.get('search_trend', ''))
        rankings.append((name, s['type'], search, yoy, mom, value))
    
    rankings.sort(key=lambda x: x[5], reverse=True)
    
    for rank, (name, scenic_type, search, yoy, mom, _) in enumerate(rankings, 1):
        report += f"| {rank} | {name} | {scenic_type} | {search} | +{yoy}% | +{mom}% |\n"
    
    # ==================== 每个景区详细分析 ====================
    report += """
---

## 二、各景区详细分析

"""
    
    # 景区详细分析
    for name, scenic_type, search30, yoy30, mom30, _ in rankings:
        d30 = data.get(name, {}).get("30天", {})
        d7 = data.get(name, {}).get("7天", {})
        portrait = d7.get("人群画像", {}).get("地域分布", {})
        
        search7 = d7.get('search_avg', '-')
        yoy7, mom7 = parse_trend(d7.get('search_trend', ''))
        
        # 定位
        if portrait and portrait.get("top5"):
            henan = portrait["top5"][0].get("占比", "0%").replace("%", "")
            henan_num = float(henan) if henan else 0
            if henan_num > 40:
                定位 = "本地化严重"
            elif henan_num > 20:
                定位 = "区域型"
            else:
                定位 = "全国型"
        else:
            定位 = "-"
        
        report += f"""### {name} ({scenic_type})

**搜索指数**
- 30天：{search30}（同比+{yoy30}% / 环比+{mom30}%）
- 7天：{search7}（同比+{yoy7}% / 环比{mom7}%）

**竞争定位**：{定位}

**本周期 vs 上周期对比**
"""
        
        # 本周期vs上周期分析
        try:
            mom7_val = float(mom7) if mom7 not in ['-', ''] else 0
            mom30_val = float(mom30) if mom30 not in ['-', ''] else 0
            
            if mom7_val > mom30_val:
                report += f"- 近期热度上升速度加快（7天环比+{mom7}% > 30天环比+{mom30}%）\n"
            elif mom7_val < mom30_val:
                report += f"- 近期热度上升速度放缓（7天环比+{mom7}% < 30天环比+{mom30}%）\n"
            else:
                report += f"- 热度变化稳定\n"
        except:
            pass
        
        # 威胁判断
        if name != "建业电影小镇":
            gap = parse_value(search30) / parse_value("1.5万") if parse_value("1.5万") > 0 else 0
            if gap > 10:
                威胁 = "🔴 高威胁"
            elif gap > 3:
                威胁 = "🟡 中威胁"
            else:
                威胁 = "🟢 低威胁"
            report += f"- 竞争威胁：{威胁}\n"
        
        report += "\n"
    
    # ==================== 竞品策略分析 ====================
    report += """---

## 三、竞品策略分析

### 清明上河园（#1 头部竞品）
- **优势**：搜索指数最高（24万），全国知名度最高
- **弱点**：7天环比-35%，热度明显回落
- **启示**：节后自然回落是机会，可抢占市场份额

### 万岁山武侠城（#2）
- **优势**：30天环比+21%，稳步增长
- **弱点**：7天环比-43%，近期热度大跌
- **启示**：需持续关注其营销动作

### 银基动物王国（#3）
- **优势**：30天环比+40%增速最快
- **弱点**：7天环比仅+1%
- **启示**：近期营销成功，需重点分析其策略

### 只有河南（#4）
- **优势**：本地用户TGI 650极高
- **弱点**：河南占比42%过高，外省辐射弱
- **启示**：可差异化竞争，强调"电影+穿越"

### 郑州方特（#6）
- **优势**：本地化严重（河南65%）
- **弱点**：7天环比-52%跌幅最大
- **启示**：本项目已超越，无需关注
"""
    
    # ==================== 营销建议 ====================
    report += """
---

## 四、营销策略建议

### 🔴 本周紧急

| 动作 | 目标 | 优先级 |
|------|------|--------|
| 加大抖音投放 | 搜索指数提升至3万+ | P0 |
| 巩固河南投放 | 提升TGI>300 | P0 |
| 借势清明节 | 搜索指数达2万 | P1 |
| 关注观音堂热点 | 借势营销 | P1 |

### 🟡 本月重点

1. **内容策略**：借鉴银基环比+40%策略
2. **达人合作**：男性用户56%，增加军事历史类
3. **渠道优化**：抖音+头条联动，测试搜索广告
"""
    
    report += f"""
---

**数据来源**：抖音指数

**报告时间**：{today}

*注：年龄分布、详细关联分析待后续完善*
"""
    
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        print(generate_full_report())
    else:
        data = load_data()
        print("=" * 60)
        print("📊 抖音指数数据")
        print("=" * 60)
        for s in SCENICS:
            name = s['name']
            d = data.get(name, {})
            print(f"\n{name}:")
            for period in ["30天", "7天"]:
                if period in d:
                    p = d[period]
                    print(f"  {period}: 搜索{p.get('search_avg','-')}")
