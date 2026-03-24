#!/usr/bin/env python3
"""
小红书数据周报 - 基于AIPS人群资产数据
包含：人群资产、行业排名、竞品对比、爆款笔记分析
"""

import os
import json
from datetime import datetime, timedelta

DATA_FILE = os.path.expanduser("~/.openclaw/data/xiaohongshu_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def format_number(num):
    """格式化数字，千分位"""
    if isinstance(num, str):
        return num
    return f"{num:,}"

def generate_weekly_report():
    """生成小红书数据周报"""
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    
    data = load_data()
    
    if not data:
        return "暂无数据"
    
    # 解析数据
    key_metrics = data.get('key_metrics', {})
    brand_metrics = data.get('brand_metrics_7d', {})
    top_notes = data.get('top_notes', [])
    data_date = data.get('data_date', today_str)
    
    # 人群资产数据
    crowd_total = key_metrics.get('crowd_total', {})
    search_volume = key_metrics.get('search_volume', {})
    exposure_rate = key_metrics.get('exposure_rate', {})
    read_rate = key_metrics.get('read_rate', {})
    
    report = f"""# 📊 小红书数据周报 ({week_ago} ~ {today_str})

> 数据周期：近30天 | 更新日期：{data_date}

---

## 一、AIPS人群资产（出行旅游-景点景区行业）

### 1.1 人群规模与增长

| 人群指标 | 数值 | 周变化 | 较品牌集均值 | 行业排名 |
|----------|------|--------|--------------|----------|
| 人群资产总数 | {format_number(crowd_total.get('value', 0))} | {crowd_total.get('wow', '-')} | {crowd_total.get('vs_brand_avg', '-')} | 第{crowd_total.get('industry_rank', '-')}位 |
| 搜索量 | {format_number(search_volume.get('value', 0))} | {search_volume.get('wow', '-')} | {search_volume.get('vs_brand_avg', '-')} | 第{search_volume.get('industry_rank', '-')}位 |
| 搜后曝光渗透率 | {exposure_rate.get('value', '-')} | {exposure_rate.get('wow', '-')} | {exposure_rate.get('vs_brand_avg', '-')} | 第{exposure_rate.get('industry_rank', '-')}位 |
| 阅读渗透率 | {read_rate.get('value', '-')} | {read_rate.get('wow', '-')} | {read_rate.get('vs_brand_avg', '-')} | 第{read_rate.get('industry_rank', '-')}位 |

### 1.2 人群资产解读

- **认知(Awareness)**：人群资产总数 {format_number(crowd_total.get('value', 0))}，{crowd_total.get('wow', '持平')}
- **兴趣(Interest)**：搜索量 {format_number(search_volume.get('value', 0))}，{search_volume.get('wow', '持平')}
- **深度兴趣(TI)**：阅读渗透率 {read_rate.get('value', '-')}，{read_rate.get('wow', '持平')}，排名第{read_rate.get('industry_rank', '-')}位
- **曝光转化**：搜后曝光渗透率 {exposure_rate.get('value', '-')}，{exposure_rate.get('wow', '持平')}

---

## 二、品牌热度（近7日）

| 指标 | 数值 | 说明 |
|------|------|------|
| 点击指数 | {format_number(brand_metrics.get('click_index', 0))} | 内容曝光后点击 |
| 互动指数 | {format_number(brand_metrics.get('interaction_index', 0))} | 点赞+收藏+评论 |
| TI人群 | {format_number(brand_metrics.get('ti_crowd', 0))} | 深度兴趣人群 |
| I_TI人群 | {format_number(brand_metrics.get('i_ti_crowd', 0))} | 兴趣+深度兴趣 |

---

## 三、爆款笔记分析（本周TOP）

"""
    
    # 添加爆款笔记
    for i, note in enumerate(top_notes[:5], 1):
        report += f"""### {i}. {note.get('title', '无标题')[:30]}...
- 曝光: {format_number(note.get('exposure', 0))} | 阅读: {format_number(note.get('read', 0))} | 互动: {note.get('interaction', 0)} | TI人群: {format_number(note.get('i_ti_crowd', 0))}

"""

    report += f"""---

## 四、周度洞察

### 📈 增长亮点
- 人群资产总量{crowd_total.get('wow', '持平')}，整体呈上升趋势
- 阅读渗透率{read_rate.get('wow', '持平')}，内容质量获用户认可
- 深度兴趣人群(TI)排名第{read_rate.get('industry_rank', '-')}位，领先多数竞品

### ⚠️ 待提升
- 较品牌集均值仍有差距（{crowd_total.get('vs_brand_avg', '-')}）
- 搜后曝光渗透率偏低，曝光→点击转化待优化
- 搜索量排名{search_volume.get('industry_rank', '-')}位，搜索流量有待加强

---

## 五、营销建议

### 🔴 本周重点
1. **优化搜索关键词**：提升搜索排名，增加主动搜索流量
2. **提升曝光点击率**：优化封面标题，提高曝光→点击转化

### 🟡 持续优化
1. **内容质量**：保持阅读渗透率优势，产出更多优质内容
2. **互动运营**：引导用户点赞收藏，提升互动指数
3. **达人合作**：扩大TI人群覆盖，提升品牌影响力

---

**数据来源**：小红书数据平台（出行旅游-景点景区行业）

**周报生成时间**：{today_str}
"""
    
    return report

if __name__ == "__main__":
    print(generate_weekly_report())
