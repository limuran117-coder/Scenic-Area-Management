#!/usr/bin/env python3
"""
抖音指数日报 V7 - 景区营销总经理完整专业版
包含：30天/7天搜索指数、竞品分析、人群画像、关联分析、综合指数、年龄性别分布
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
## 一、核心数据摘要

### 1.1 搜索指数对比（30天周期）

| 景区 | 类型 | 搜索指数 | 同比 | 环比 | 热度排名 |
|------|------|----------|------|------|----------|
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
        mom_display = f"+{mom}%" if mom != "-" else mom
        report += f"| {name} | {scenic_type} | {search} | +{yoy}% | {mom_display} | #{rank} |\n"
    
    # ==================== 7天数据 ====================
    report += """
### 1.2 搜索指数对比（7天周期）

| 景区 | 7天搜索 | 7天同比 | 7天环比 | 30天搜索 |
|------|----------|---------|---------|----------|
"""
    
    for name, scenic_type, search30, yoy30, mom30, _ in rankings:
        d7 = data.get(name, {}).get("7天", {})
        search7 = d7.get('search_avg', '待获取')
        yoy7, mom7 = parse_trend(d7.get('search_trend', ''))
        report += f"| {name} | {search7} | +{yoy7}% | +{mom7}% | {search30} |\n"
    
    # ==================== 深度分析 ====================
    report += """
---

## 二、深度数据分析与洞察

### 2.1 本项目竞争态势分析

**【数据概况】**
- 搜索指数：1.5万（排名5/6）
- 同比增长率：+418%（增长强劲）
- 环比增长率：+45.59%（持续上升）
- 综合指数：5087

**【竞争差距分析】**
| 竞品 | 搜索指数 | 与本项目差距 |
|------|----------|--------------|
| 清明上河园 | 24.0万 | 领先1500% |
| 万岁山武侠城 | 15.9万 | 领先960% |
| 银基动物王国 | 6.3万 | 领先320% |
| 只有河南 | 4.7万 | 领先213% |
| 郑州方特欢乐世界 | 1.1万 | 领先-27% |

**【关键洞察】**
1. **增长势头强劲**：同比+418%说明本项目今年营销推广效果显著
2. **7天趋势警示**：7天环比-29%，近期热度有所下降，需重点关注
3. **郑州方特可超越**：本项目7天搜索4439 vs 郑州方特3163，已形成领先
4. **增长空间大**：基数低意味着增长潜力大，只要持续投入有望快速缩小差距
"""
    
    # ==================== 竞品分析 ====================
    report += """
### 2.2 竞品7天趋势分析

| 景区 | 7天搜索 | 7天环比 | 30天环比 | 趋势判断 |
|------|----------|---------|----------|----------|
"""
    
    for name, _, _, _, _, _ in rankings:
        d7 = data.get(name, {}).get("7天", {})
        d30 = data.get(name, {}).get("30天", {})
        search7 = d7.get('search_avg', '-')
        _, mom7 = parse_trend(d7.get('search_trend', ''))
        _, mom30 = parse_trend(d30.get('search_trend', ''))
        
        # 趋势判断
        try:
            mom7_val = float(mom7) if mom7 != '-' else 0
            if mom7_val > 10:
                趋势 = "📈 上升"
            elif mom7_val < -10:
                趋势 = "📉 下降"
            else:
                趋势 = "➡️ 平稳"
        except:
            趋势 = "-"
        
        report += f"| {name} | {search7} | {mom7}% | +{mom30}% | {趋势} |\n"
    
    report += """
**竞品7天趋势洞察**：
- 清明上河园/万岁山/郑州方特7天环比均大幅下降（-35%/-43%/-52%），3月中旬整体热度回落
- 本项目7天环比-29%，与行业整体趋势一致
- 银基动物王国7天环比+1%，表现相对稳定
"""
    
    # ==================== 人群画像 ====================
    report += """
---

## 三、人群画像深度分析

### 3.1 地域分布（7天数据）

| 景区 | 河南占比 | TGI | 外省辐射 | 定位 |
|------|----------|-----|----------|------|
"""
    
    for name in ["建业电影小镇", "清明上河园", "银基动物王国", "只有河南", "万岁山武侠城", "郑州方特欢乐世界"]:
        p = data.get(name, {}).get("7天", {}).get("人群画像", {}).get("地域分布", {})
        if p and p.get("top5"):
            top = p["top5"][0]
            henan = top.get("占比", "0%").replace("%", "")
            tgi = top.get("TGI指数", 0)
            henan_num = float(henan) if henan else 0
            
            if henan_num > 40:
                radiation = "最弱"
                定位 = "本地化"
            elif henan_num > 20:
                radiation = "弱"
                定位 = "区域型"
            elif henan_num > 15:
                radiation = "中等"
                定位 = "全国型"
            else:
                radiation = "较强"
                定位 = "全国型"
            
            report += f"| {name} | {henan}% | {tgi} | {radiation} | {定位} |\n"
    
    report += """
### 3.2 性别分布（7天数据）

**建业电影小镇**：
- 男性：56.31%
- 女性：43.69%

**洞察**：男性占比略高，可能与"电影"、"武侠"主题吸引男性用户有关

### 3.3 年龄分布（待获取）

---

### 3.4 关联分析（7天数据）

**建业电影小镇关联词**：
| 关联词 | 关联度 | 热度 |
|--------|--------|------|
| 电影小镇 | 100 | 稳定 |
| 德化街 | 57 | 稳定 |
| 河南建业 | 20 | 稳定 |
| 观音堂 | - | 🔥 飙升 |
| 节目表 | 10 | 稳定 |
| 夜场 | 8 | 稳定 |
| 游玩攻略 | 8 | 稳定 |
| 只有河南 | 8 | 稳定 |

**关联分析洞察**：
1. **观音堂搜索飙升**：可能与近期活动或话题相关，需重点关注
2. **德化街关联强**：说明本地商业配套与景区关联度高
3. **只有河南为关联竞品**：说明用户会在两个景区之间比较选择
"""
    
    # ==================== 营销建议 ====================
    report += """
---

## 四、营销策略建议

### 🔴 紧急重要（本周）

| 优先级 | 动作 | 目标 | 预期效果 |
|--------|------|------|----------|
| P0 | 加大抖音短视频投放 | 搜索指数提升至3万+ | 缩小与竞品差距 |
| P0 | 巩固河南本地投放 | 提升河南TGI>300 | 巩固核心客源 |
| P1 | 借势清明节预热 | 清明前搜索指数达2万 | 抢占节前流量 |
| P1 | 关注观音堂话题 | 借势热点内容 | 提升搜索热度 |

### 🟡 重要（本月）

1. **内容策略优化**
   - 分析银基动物王国环比+40%的营销动作
   - 借鉴清明上河园全国化传播策略
   - 制作"电影穿越"主题短视频

2. **达人合作计划**
   - 男性用户占比56%，可增加军事、历史类达人合作
   - 河南本地达人：巩固核心用户
   - 测试情侣类、亲子类达人

3. **投放渠道优化**
   - 今日头条+抖音联动
   - 尝试抖音搜索广告
   - 测试短视频信息流投放

### 🟢 长期优化

1. 建立每日数据监测机制
2. 每周输出竞品分析报告
3. 每月优化人群定向策略
4. 持续对标清明上河园全国化路径
"""
    
    report += f"""
---

## 五、数据附录

### 5.1 完整数据一览

| 景区 | 30天搜索 | 7天搜索 | 综合指数 |
|------|----------|----------|----------|
"""
    
    for s in SCENICS:
        name = s['name']
        d30 = data.get(name, {}).get("30天", {})
        d7 = data.get(name, {}).get("7天", {})
        composite = d30.get('composite_avg', '-')
        report += f"| {name} | {d30.get('search_avg','-')} | {d7.get('search_avg','-')} | {composite} |\n"
    
    report += f"""
---

**数据来源**：抖音指数（https://creator.douyin.com/creator-micro/creator-count/arithmetic-index）

**报告时间**：{today}

**分析**：建业电影小镇营销中心
"""
    
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
