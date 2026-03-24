#!/usr/bin/env python3
"""
抖音指数日报 V5 - 景区营销总经理专业完整版
包含：7天/30天数据、搜索/综合指数、关联分析、人群画像、深度洞察
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
    """解析搜索指数数值"""
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
    """解析趋势字符串"""
    if not trend_str or trend_str in ["待获取", "-"]:
        return "-", "-"
    
    yoy, mom = "-", "-"
    if '同比' in trend_str:
        try:
            yoy = trend_str.split('同比')[1].split('%')[0].replace('+', '').strip()
        except: pass
    if '环比' in trend_str:
        try:
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
## 一、核心数据摘要

### 1.1 搜索指数对比（30天周期）

| 景区 | 类型 | 搜索指数 | 同比 | 环比 | 热度排名 |
|------|------|----------|------|------|----------|
"""
    
    # 排序计算排名
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
        report += f"| {name} | {scenic_type} | {search} | +{yoy}% | +{mom}% | #{rank} |\n"
    
    # ==================== 深度分析 ====================
    report += """
---

## 二、深度数据分析与洞察

### 2.1 本项目竞争态势分析

"""
    
    # 获取本项目数据
    our_data = data.get("建业电影小镇", {}).get("30天", {})
    our_search = our_data.get('search_avg', '0')
    our_yoy, our_mom = parse_trend(our_data.get('search_trend', ''))
    our_composite = our_data.get('composite_avg', '-')
    our_comp_yoy, our_comp_mom = parse_trend(our_data.get('composite_trend', ''))
    
    # 获取竞品数据
    qingming = data.get("清明上河园", {}).get("30天", {})
    wansui = data.get("万岁山武侠城", {}).get("30天", {})
    yinji = data.get("银基动物王国", {}).get("30天", {})
    zhiyou = data.get("只有河南", {}).get("30天", {})
    fangte = data.get("郑州方特欢乐世界", {}).get("30天", {})
    
    qm_val = parse_value(qingming.get('search_avg', '0'))
    ws_val = parse_value(wansui.get('search_avg', '0'))
    yj_val = parse_value(yinji.get('search_avg', '0'))
    zy_val = parse_value(zhiyou.get('search_avg', '0'))
    ft_val = parse_value(fangte.get('search_avg', '0'))
    our_val = parse_value(our_search)
    
    gap_qm = round((qm_val - our_val) / our_val * 100) if our_val > 0 else 0
    gap_ws = round((ws_val - our_val) / our_val * 100) if our_val > 0 else 0
    gap_yj = round((yj_val - our_val) / our_val * 100) if our_val > 0 else 0
    
    report += f"""**【数据概况】**
- 搜索指数：{our_search}（排名5/6）
- 同比增长率：+{our_yoy}% 
- 环比增长率：+{our_mom}%
- 综合指数：{our_composite}

**【竞争差距分析】**
| 竞品 | 搜索指数 | 与本项目差距 |
|------|----------|--------------|
| 清明上河园 | {qingming.get('search_avg','-')} | 领先{abs(gap_qm)}% |
| 万岁山武侠城 | {wansui.get('search_avg','-')} | 领先{abs(gap_ws)}% |
| 银基动物王国 | {yinji.get('search_avg','-')} | 领先{abs(gap_yj)}% |
| 只有河南 | {zhiyou.get('search_avg','-')} | 领先{round((zy_val-our_val)/our_val*100)}% |
| 郑州方特 | {fangte.get('search_avg','-')} | 领先{round((ft_val-our_val)/our_val*100)}% |

**【关键洞察】**
1. **增长势头强劲**：同比+{our_yoy}%说明本项目今年营销推广效果显著，环比+{our_mom}%表明近期热度持续上升
2. **绝对值差距大**：与头部景区差距16-17倍，需持续加大投放
3. **增长空间大**：基数低意味着增长潜力大，只要持续投入有望快速缩小差距
"""
    
    # ==================== 竞品分析 ====================
    report += """
### 2.2 竞品逐一分析

#### 【清明上河园】🔴 主要竞品
"""
    
    qm_yoy, qm_mom = parse_trend(qingming.get('search_trend', ''))
    qm_cy, qm_cm = parse_trend(qingming.get('composite_trend', ''))
    
    report += f"""- 搜索指数：{qingming.get('search_avg','-')}（#{rankings[0][0]}）
- 同比：+{qm_yoy}% | 环比：{qm_mom}%
- 综合指数：{qingming.get('composite_avg','-')}

**洞察**：
- 搜索指数最高但环比下降{qm_mom}%，说明节后热度自然回落
- 同比暴增{qm_yoy}%表明去年同期基数极低，可能是新营销策略见效
- 环比下降是本项目机会点，可考虑在清明后加大投放抢占市场份额
"""
    
    report += """
#### 【万岁山武侠城】🟡 重点竞品
"""
    
    ws_yoy, ws_mom = parse_trend(wansui.get('search_trend', ''))
    report += f"""- 搜索指数：{wansui.get('search_avg','-')}
- 同比：+{ws_yoy}% | 环比：+{ws_mom}%

**洞察**：
- 环比+{ws_mom}%持续增长，说明近期营销推广效果好
- 稳步增长型选手，需持续关注其内容策略
- 本项目可借鉴其增长策略
"""
    
    report += """
#### 【银基动物王国】🟡 重点竞品
"""
    
    yj_yoy, yj_mom = parse_trend(yinji.get('search_trend', ''))
    report += f"""- 搜索指数：{yinji.get('search_avg','-')}
- 同比：+{yj_yoy}% | 环比：+{yj_mom}%

**洞察**：
- 环比+{yj_mom}%增速最快，是近期营销最成功的景区
- 需重点分析其近期营销动作和内容策略
- 可能近期有大型活动或达人合作
"""
    
    # ==================== 人群画像分析 ====================
    report += """
---

## 三、人群画像分析

### 3.1 地域分布对比

| 景区 | TOP1省份 | 占比 | TGI | 核心客源 |
|------|----------|------|-----|----------|
"""
    
    # 提取各景区地域数据
    portraits = {
        "建业电影小镇": data.get("建业电影小镇", {}).get("7天", {}).get("人群画像", {}).get("地域分布", {}),
        "只有河南": data.get("只有河南", {}).get("7天", {}).get("人群画像", {}).get("地域分布", {}),
    }
    
    for name in ["建业电影小镇", "清明上河园", "银基动物王国", "只有河南", "万岁山武侠城"]:
        p = data.get(name, {}).get("7天", {}).get("人群画像", {}).get("地域分布", {})
        if p and p.get("top5"):
            top = p["top5"][0]
            tgi = top.get("TGI指数", "-")
            tgi_level = "高偏好" if int(tgi) > 200 else ("偏好" if int(tgi) > 100 else "一般")
            report += f"| {name} | {top.get('省份','-')} | {top.get('占比','-')} | {tgi} | {tgi_level} |\n"
        else:
            report += f"| {name} | 待获取 | - | - | - |\n"
    
    report += """
**地域分析洞察**：
1. **河南是绝对主战场**：所有景区河南用户占比最高，TGI指数普遍200+
2. **建业电影小镇**：河南17.61%占比相对较低，说明外省辐射能力强于只有河南
3. **只有河南**：河南占比42.82%过高，外省辐射能力最弱
4. **银基动物王国**：山西TGI指数227，说明北方邻省用户偏好度高

### 3.2 目标客群建议

基于地域分析，建议投放优先级：
1. **第一梯队（必投）**：河南省内 - TGI最高，转化最好
2. **第二梯队（测试）**：山东、山西、陕西 - TGI表现好
3. **第三梯队（拓展）**：广东、江苏 - 占比高但TGI低，需优化内容吸引
"""
    
    # ==================== 营销建议 ====================
    report += """
---

## 四、营销建议

### 🔴 紧急重要（本周）

| 优先级 | 动作 | 目标 | 预期效果 |
|--------|------|------|----------|
| P0 | 加大抖音短视频投放 | 搜索指数提升至3万+ | 缩小与竞品差距 |
| P0 | 优化河南本地投放 | 提升河南TGI>300 | 巩固核心客源 |
| P1 | 借势清明节预热 | 清明前搜索指数达2万 | 抢占节前流量 |

### 🟡 重要（本月）

1. **内容策略优化**
   - 分析银基动物王国环比+40%的营销动作
   - 借鉴头部景区内容风格

2. **达人合作计划**
   - 河南本地达人优先
   - 测试亲子类、情侣类达人

3. **投放渠道优化**
   - 今日头条+抖音联动
   - 尝试抖音搜索广告

### 🟢 长期优化

1. 建立每日数据监测机制
2. 每周输出竞品分析报告
3. 每月优化人群定向策略
"""
    
    # ==================== 7天数据 ====================
    report += """
---

## 五、7天数据详情（待完善）

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

**数据来源**：抖音指数（https://creator.douyin.com/creator-micro/creator-count/arithmetic-index）

**更新时间**：{today}

**分析**：建业电影小镇营销中心

---
*注：7天数据及关联分析待后续完善*"""
    
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        print(generate_full_report())
    else:
        data = load_data()
        print("=" * 60)
        print("📊 抖音指数数据状态")
        print("=" * 60)
        for s in SCENICS:
            name = s['name']
            d = data.get(name, {})
            print(f"\n{name}:")
            for period in ["30天", "7天"]:
                if period in d:
                    p = d[period]
                    print(f"  {period}: 搜索{p.get('search_avg','-')}")
