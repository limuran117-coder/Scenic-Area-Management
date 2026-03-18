# 工具与脚本

## 数据查询工具

### 电影小镇客流收入查询
- **触发关键词**：`查询客流`、`查询收入`、`电影小镇客流`、`电影小镇收入`
- **脚本位置**：`~/.openclaw/scripts/visitor_query.py`

#### 支持的查询方式
| 你这样问我 | 查询结果 |
|-----------|---------|
| `查询客流 2023-11-13` | 具体某一天客流+收入 |
| `查询收入 2023-10月` | 某月数据 |
| `查询客流 最高` | 客流TOP10 |
| `查询收入 最高` | 收入TOP10 |
| `查询客流 月排名` | 各月客流排名 |
| `查询收入 年度` | 年度汇总 |

#### 数据说明
- 数据源：`~/电影小镇2023年，2024年，2025年客流及收入情况.xlsx`
- 日期逻辑：序号1 = 1月1日，序号365 = 12月31日
- 金额单位：**元**
- 人数单位：**人**

#### 数据现状
- 2023年：✅ 完整365天
- 2024年：⚠️ 部分数据（主要是2月、10月）
- 2025年：暂无数据

---

## 定时任务脚本

| 任务 | 脚本位置 |
|------|----------|
| 天气日报 | /Users/tianjinzhan/.openclaw/scripts/weather_daily.py |
| 抖音日报 | /Users/tianjinzhan/.openclaw/scripts/juliang_daily.py |
| 抖音周报 | /Users/tianjinzhan/.openclaw/scripts/juliang_weekly.py |

---

## 技能

### excel-handler
- **位置**：~/.openclaw/skills/excel-handler/SKILL.md
- **能力**：
  - 本地xlsx读取（openpyxl）
  - 飞书云文档内容获取
  - 图片表格识别
  - 生成格式化Excel

### notebooklm
- **位置**：~/.openclaw/skills/notebooklm-skill/SKILL.md
- **能力**：
  - 查询Google NotebookLM笔记本
  - 浏览器自动化
  - 持续认证

---

## 模型配置

| 场景 | 模型 | 配置 |
|------|------|------|
| 默认 | MiniMax M2.5 | minimax-cn/MiniMax-M2.5 |
| 图片理解 | Qwen Vision | 自动切换 |
| 本地推理 | Qwen3:32b | ollama/qwen3:32b |
