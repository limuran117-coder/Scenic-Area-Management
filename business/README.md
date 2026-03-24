# 中期业务记忆目录

> 本目录用于存储周期性业务成果、可复用经验、结构化业务数据

## 目录结构

```
business/
├── data_reports/          # 周期性数据分析报告
│   ├── weekly/           # 周度经营/营销数据报告
│   ├── monthly/          # 月度经营/营销数据报告
│   └── campaign/         # 单次营销活动专项复盘报告
├── marketing_library/      # 营销素材与策略库
│   ├── campaign_cases/   # 历史活动方案与效果复盘
│   ├── channel_rules/    # 各渠道运营规则与投放经验
│   └── content_templates/# 可复用的内容/文案/直播模板
├── market_competitor/    # 市场与竞品信息库
│   ├── competitor_monitor/ # 竞品动态月度跟踪报告
│   └── industry_trend/   # 文旅行业趋势分析报告
└── user_insights/       # 用户画像与洞察库
    ├── tourist_portrait.md  # 景区游客核心画像
    └── user_feedback.md    # 游客反馈汇总与优化建议
```

## 写入规则

1. 周度/月度数据报告生成后，自动归档到对应目录
2. 营销活动结束后，必须将完整方案、数据、复盘结论归档到`campaign_cases/`
3. 所有文件开头添加frontmatter元数据

## 示例frontmatter

```markdown
---
title: 2026年春节景区营销活动专项复盘
date: 2026-02-18
type: campaign_report
core_tags: 春节营销,抖音投放,ROI分析,客流增长
core_indicator: 客流同比+35%,营收同比+42%,营销ROI 1:4.2
---
```
