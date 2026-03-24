#!/usr/bin/env python3
"""
抖音指数日报 V6 - 景区营销总经理完整专业版
包含：30天/7天搜索指数、竞品分析、人群画像、地域洞察、营销建议
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
| 竞品 | 搜索指数 | 与本项目差距 | 威胁等级 |
|------|----------|--------------|----------|
"""
    
    our_val = parse_value("1.5万")
    for name, search, gap in [
        ("清明上河园", "24.0万", 1500),
        ("万岁山武侠城", "15.9万", 960),
        ("银基动物王国", "6.3万", 320),
        ("只有河南", "4.7万", 213),
        ("郑州方特欢乐世界", "1.1万", -27)
    ]:
        threat = "🟡" if gap > 200 else ("🔴" if gap > 500 else "🟢")
        report += f"| {name} | {search} | 领先{gap}% | {threat} |\n"
    
    report += """
**【关键洞察】**
1. **增长势头强劲**：同比+418%说明本项目今年营销推广效果显著，环比+45%表明近期热度持续上升
2. **绝对值差距大**：与头部景区差距16倍，需持续加大投放
3. **增长空间大**：基数低意味着增长潜力大，只要持续投入有望快速缩小差距
4. **郑州方特可超越**：本项目搜索指数1.5万 vs 郑州方特1.1万，已形成领先
"""
    
    # ==================== 竞品分析 ====================
    report += """
### 2.2 竞品逐一深度分析

#### 【清明上河园】🔴 头部竞品
- 搜索指数：24.0万（#1）
- 同比：+654% | 环比：-12%
- 综合指数：8.4万

**深度洞察**：
- 搜索指数最高但环比下降12%，说明节后热度自然回落
- 同比暴增654%表明去年同期基数极低，可能是新营销策略见效
- 环比下降是本项目**机会点**，可考虑在清明后加大投放抢占市场份额
- 河南占比仅13.24%，外省辐射能力最强，全国知名度最高
"""
    
    report += """
#### 【万岁山武侠城】🟡 重点竞品
- 搜索指数：15.9万（#2）
- 同比：+10% | 环比：+21%

**深度洞察**：
- 环比+21%持续增长，说明近期营销推广效果好
- 稳步增长型选手，需持续关注其内容策略
- 本项目可借鉴其增长策略
- 安徽TGI指数140表现突出，华东市场开拓成功
"""
    
    report += """
#### 【银基动物王国】🟡 重点竞品
- 搜索指数：6.3万（#3）
- 同比：+22% | 环比：+40%

**深度洞察**：
- 环比+40%增速**最快**，是近期营销最成功的景区
- 需重点分析其近期营销动作和内容策略
- 可能近期有大型活动或达人合作
- 山西TGI指数227，北方市场开拓成功
"""
    
    report += """
#### 【只有河南】🟡 区域竞品
- 搜索指数：4.7万（#4）
- 同比：+48% | 环比：+22%

**深度洞察**：
- 河南占比42.82%过高，外省辐射能力最弱
- 本项目河南占比仅17.61%，外省辐射能力是其2倍以上
- 可利用差异化定位进行竞争
"""
    
    # ==================== 人群画像分析 ====================
    report += """
---

## 三、人群画像深度分析

### 3.1 地域分布全对比

| 景区 | 河南占比 | TGI | 外省辐射 | 定位 |
|------|----------|-----|----------|------|
"""
    
    portraits = {}
    for name in ["建业电影小镇", "清明上河园", "银基动物王国", "只有河南", "万岁山武侠城", "郑州方特欢乐世界"]:
        p = data.get(name, {}).get("7天", {}).get("人群画像", {}).get("地域分布", {})
        if p and p.get("top5"):
            top = p["top5"][0]
            henan = top.get("占比", "0%").replace("%", "")
            tgi = top.get("TGI指数", 0)
            henan_num = float(henan) if henan else 0
            
            # 辐射能力判断
            if henan_num > 40:
                radiation = "最弱"
            elif henan_num > 20:
                radiation = "弱"
            elif henan_num > 15:
                radiation = "中等"
            else:
                radiation = "较强"
            
            # 定位
            if henan_num > 40:
               定位 = "本地化"
            elif henan_num > 20:
                定位 = "区域型"
            else:
                定位 = "全国型"
            
            portraits[name] = (henan, tgi, radiation, 定位)
            report += f"| {name} | {henan}% | {tgi} | {radiation} | {定位} |\n"
    
    report += """
**地域分析核心洞察**：

1. **郑州方特欢乐世界**：河南占比65.21%**极端本地化**，TGI指数989绝对霸主
   - 解读：几乎完全依赖本地市场，外省开拓能力为零
   - 机会：与其错位竞争，抢占外省游客

2. **只有河南**：河南占比42.82%高度本地化，TGI指数650
   - 解读：本地化严重，外省辐射能力最弱
   - 机会：差异化竞争，强调"电影+穿越"特色

3. **银基动物王国/万岁山武侠城**：河南占比17-18%，TGI270+
   - 解读：本地+外省平衡型，外省开拓较成功
   - 借鉴：可学习其外省拓客策略

4. **建业电影小镇**：河南占比17.61%，TGI指数267
   - 解读：**外省辐射能力较强**，全国化潜力大
   - 优势：这是本项目的**核心差异化优势**！

5. **清明上河园**：河南占比13.24%最低，TGI指数201
   - 解读：**全国知名度最高**，外省辐射能力最强
   - 地位：行业标杆，需持续对标学习

### 3.2 目标客群投放建议

基于地域分析，制定投放策略：

| 优先级 | 区域 | 策略 | 预期效果 |
|--------|------|------|----------|
| P0 | 河南省内 | 巩固TGI>250高偏好区域 | 提升转化率 |
| P1 | 山东/山西/陕西 | 测试投放，TGI100+ | 增量市场 |
| P2 | 江苏/浙江/广东 | 优化内容吸引 | 潜力市场 |
| P3 | 全国 | 品牌曝光 | 长期增长 |
"""
    
    # ==================== 营销建议 ====================
    report += """
---

## 四、营销策略建议

### 🔴 紧急重要（本周）

| 优先级 | 动作 | 目标 | 预期效果 |
|--------|------|------|----------|
| P0 | 加大抖音短视频投放 | 搜索指数提升至3万+ | 缩小与竞品差距 |
| P0 | 优化河南本地投放 | 提升河南TGI>300 | 巩固核心客源 |
| P1 | 借势清明节预热 | 清明前搜索指数达2万 | 抢占节前流量 |

### 🟡 重要（本月）

1. **内容策略优化**
   - 分析银基动物王国环比+40%的营销动作
   - 借鉴清明上河园全国化传播策略
   - 制作"电影穿越"主题短视频

2. **达人合作计划**
   - 河南本地达人：巩固核心用户
   - 测试亲子类、情侣类达人
   - 尝试跨区域达人合作

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

| 景区 | 30天搜索 | 同比 | 环比 | 综合指数 |
|------|----------|------|------|----------|
"""
    
    for s in SCENICS:
        name = s['name']
        d30 = data.get(name, {}).get("30天", {})
        search = d30.get('search_avg', '-')
        yoy, mom = parse_trend(d30.get('search_trend', ''))
        composite = d30.get('composite_avg', '-')
        report += f"| {name} | {search} | +{yoy}% | +{mom}% | {composite} |\n"
    
    report += f"""
---

**数据来源**：抖音指数（https://creator.douyin.com/creator-micro/creator-count/arithmetic-index）

**报告时间**：{today}

**分析**：建业电影小镇营销中心

---
*注：关联分析、年龄/性别分布数据待后续完善*"""
    
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
