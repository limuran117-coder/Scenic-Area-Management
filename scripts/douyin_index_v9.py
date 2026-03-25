#!/usr/bin/env python3
"""
抖音指数日报 V9 - 完整合并版
所有数据表格化，每个景区详细分析
"""

import os
import json
from datetime import datetime

SCENICS = [
    {"name": "建业电影小镇", "type": "本项目"},
    {"name": "清明上河园", "type": "竞品"},
    {"name": "万岁山武侠城", "type": "竞品"},
    {"name": "银基动物王国", "type": "竞品"},
    {"name": "只有河南", "type": "竞品"},
    {"name": "郑州方特欢乐世界", "type": "竞品"},
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
    
    # 按搜索指数排序
    rankings = []
    for s in SCENICS:
        name = s['name']
        d30 = data.get(name, {}).get("30天", {})
        d7 = data.get(name, {}).get("7天", {})
        
        search30 = d30.get('search_avg', '0')
        search7 = d7.get('search_avg', '0')
        
        value30 = parse_value(search30)
        value7 = parse_value(search7)
        
        yoy30, mom30 = parse_trend(d30.get('search_trend', ''))
        yoy7, mom7 = parse_trend(d7.get('search_trend', ''))
        
        # 定位判断
        portrait = d7.get("人群画像", {}).get("地域分布", {})
        if portrait and portrait.get("top5"):
            henan = portrait["top5"][0].get("占比", "0%").replace("%", "")
            henan_num = float(henan) if henan else 0
            if henan_num > 40:
                定位 = "本地化"
            elif henan_num > 20:
                定位 = "区域型"
            else:
                定位 = "全国型"
        else:
            定位 = "-"
        
        rankings.append({
            "name": name,
            "type": s['type'],
            "search30": search30,
            "search7": search7,
            "value30": value30,
            "value7": value7,
            "yoy30": yoy30,
            "mom30": mom30,
            "yoy7": yoy7,
            "mom7": mom7,
            "定位": 定位,
            "d30": d30,
            "d7": d7
        })
    
    rankings.sort(key=lambda x: x["value30"], reverse=True)
    
    # 编号
    for i, r in enumerate(rankings):
        r["rank"] = i + 1
    
    report = f"""# 📊 抖音指数日报 ({today})

---

## 一、核心数据总览

### 1.1 搜索指数对比表（30天周期）

| 排名 | 景区 | 类型 | 搜索指数 | 同比 | 环比 | 定位 |
|------|------|------|----------|------|------|------|
"""
    
    for r in rankings:
        report += f"| {r['rank']} | {r['name']} | {r['type']} | {r['search30']} | +{r['yoy30']}% | +{r['mom30']}% | {r['定位']} |\n"
    
    report += """
### 1.2 搜索指数对比表（7天周期）

| 排名 | 景区 | 7天搜索 | 7天同比 | 7天环比 | 30天环比 | 趋势 |
|------|------|----------|---------|---------|----------|------|
"""
    
    for r in rankings:
        try:
            mom7_val = float(r['mom7']) if r['mom7'] not in ['-', ''] else 0
            if mom7_val > 5:
                趋势 = "📈"
            elif mom7_val < -5:
                趋势 = "📉"
            else:
                趋势 = "➡️"
        except:
            趋势 = "-"
        
        report += f"| {r['rank']} | {r['name']} | {r['search7']} | +{r['yoy7']}% | {r['mom7']}% | +{r['mom30']}% | {趋势} |\n"
    
    report += """
### 1.3 人群画像表

| 景区 | 河南占比 | TGI | 性别(男/女) | 外省辐射 |
|------|----------|-----|--------------|----------|
"""
    
    for r in rankings:
        portrait = r["d7"].get("人群画像", {}).get("地域分布", {})
        if portrait and portrait.get("top5"):
            henan = portrait["top5"][0].get("占比", "-")
            tgi = portrait["top5"][0].get("TGI指数", "-")
        else:
            henan = "-"
            tgi = "-"
        
        # 性别（抖音搜索用户画像，非景区实际客群）
        if r["name"] == "建业电影小镇":
            gender = "56%/44% 🔍搜索人群"
        else:
            gender = "-"
        
        # 外省辐射能力
        if r["定位"] == "本地化":
            辐射 = "最弱"
        elif r["定位"] == "区域型":
            辐射 = "弱"
        else:
            辐射 = "中/强"
        
        report += f"| {r['name']} | {henan}% | {tgi} | {gender} | {辐射} |\n"
    
    # ==================== 每个景区详细分析 ====================
    report += """
---

## 二、各景区📈 7天变化详情

"""
    
    for r in rankings:
        report += f"""### {r['rank']}. {r['name']} ({r['type']})

| 指标 | 30天数据 | 7天数据 |
|------|----------|----------|
| 搜索指数 | {r['search30']} | {r['search7']} |
| 同比 | +{r['yoy30']}% | +{r['yoy7']}% |
| 环比 | +{r['mom30']}% | {r['mom7']}% |
| 定位 | {r['定位']} | - |

**📊 本周期 vs 上周期对比：**
"""
        
        # 趋势分析
        try:
            mom7_val = float(r['mom7']) if r['mom7'] not in ['-', ''] else 0
            mom30_val = float(r['mom30']) if r['mom30'] not in ['-', ''] else 0
            
            if mom7_val > mom30_val + 5:
                report += f"- 近期热度上升加速 🚀\n"
            elif mom7_val < mom30_val - 5:
                report += f"- 近期热度上升放缓 ⚠️\n"
            else:
                report += f"- 热度变化稳定\n"
        except:
            pass
        
        # 本项目特有分析
        if r["name"] == "建业电影小镇":
            report += """**✅ 本项目优势：**
- 同比+418%增长强劲
- 外省辐射能力强（河南占比仅18%）
- 7天搜索已超越郑州方特

**⚠️ 挑战：**
- 7天环比-29%，需加大投放
- 绝对值与头部差距大
"""
        else:
            # 竞品分析
            gap = r['value30'] / parse_value("1.5万") if parse_value("1.5万") > 0 else 0
            if gap > 10:
                威胁 = "🔴 高威胁"
            elif gap > 3:
                威胁 = "🟡 中威胁"
            else:
                威胁 = "🟢 低威胁"
            
            report += f"- 竞争威胁：{威胁}\n"
        
        # 关联词（只有建业有数据）
        if r["name"] == "建业电影小镇":
            report += """**🔥 热门关联词：**
- 观音堂（搜索飙升）
- 电影小镇、德化街（稳定）
- 夜场、游玩攻略（稳定）
"""
        
        report += "\n"
    
    # ==================== 竞品策略洞察 ====================
    report += """---

## 三、💡 核心要点与策略

### 🔴 紧急（本周）

| 优先级 | 动作 | 目标 | 预期效果 |
|--------|------|------|----------|
| P0 | 加大抖音短视频投放 | 搜索指数→3万+ | 缩小差距 |
| P0 | 巩固河南本地投放 | TGI→300+ | 巩固核心 |
| P1 | 借势清明节预热 | 搜索指数→2万 | 抢占流量 |
| P1 | 借势观音堂热点 | 话题营销 | 提升热度 |

### 🟡 重点（本月）

| 方向 | 具体动作 |
|------|----------|
| 内容策略 | 分析银基环比+40%营销动作 + 互动节目传播逻辑 |
| 媒体投放 | 🎭 女性演员/换装 + 🕺男团跳舞 + KOC矩阵（转化率>KOL） |
| UGC裂变 | 互动节目最容易爆：投壶/射箭/猜大小 → 游客拍摄 → 病毒传播 |
| 渠道优化 | 抖音+头条联动，测试搜索广告 |

### 💡 互动节目传播价值分析

| 节目类型 | 互动形式 | UGC潜力 | 建议 |
|----------|----------|----------|------|
| 80年代复古 | 跳皮筋等 | 🔥🔥🔥 | 强怀旧共鸣 |
| 复古民国 | 猜大小、麻将 | 🔥🔥 | 沉浸感强 |
| 中国古代 | 投壶、射箭、对诗 | 🔥🔥🔥 | 文化+趣味 |

### 📊 行业洞察

7天环比普遍大幅下降（-35%~-52%），3月中旬整体热度回落，节后正常现象

| 竞品 | 核心优势 | 核心弱点 | 应对策略 |
|------|----------|----------|----------|
| 清明上河园 | 全国知名度最高 | 7天环比-35%回落 | 抢占市场份额 |
| 万岁山武侠城 | 30天稳步增长+21% | 7天环比-43%大跌 | 持续关注 |
| 银基动物王国 | 30天环比+40%最快 | 7天环比仅+1% | 重点分析策略 |
| 只有河南 | 本地TGI 650极高 | 河南占比42%过高 | 差异化竞争 |
| 郑州方特 | 本地化严重 | 7天环比-52% | 已超越无需关注 |

---

**数据来源**：抖音指数

**报告时间**：{today}

*注：人群画像为抖音搜索用户数据，非景区实际游客画像*
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
