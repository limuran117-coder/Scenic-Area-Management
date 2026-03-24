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

## 本地技能（2026-03-20新增）

### browser-understanding
- **位置**：`~/.openclaw/skills/browser-understanding/SKILL.md`
- **功能**：浏览器+视觉AI理解，智能页面分析
- **用途**：抖音/小红书数据采集

### workflow-templates
- **位置**：`~/.openclaw/skills/workflow-templates/SKILL.md`
- **功能**：标准化工作流模板
- **用途**：数据采集、报告生成、任务执行

### task-validator
- **位置**：`~/.openclaw/skills/task-validator/SKILL.md`
- **功能**：任务验证与防错
- **用途**：执行前/中/后验证检查

### project-organizer
- **位置**：`~/.openclaw/skills/project-organizer/SKILL.md`
- **功能**：项目与技能组织管理
- **用途**：工作区结构、技能映射、任务管理

### elite-longterm-memory
- **位置**：`~/.openclaw/skills/elite-longterm-memory/SKILL.md`
- **功能**：增强记忆系统（WAL协议+向量搜索+Git-Notes）
- **状态**：已安装

### feishu-doc-manager
- **位置**：`~/.openclaw/skills/feishu-doc-manager/SKILL.md`
- **功能**：飞书文档管理（Markdown表格转换、权限管理、长内容分段）
- **状态**：✅ 已安装
- **用途**：解决飞书文档三大痛点

---

## NPM插件（已安装）

### openclaw-workflowskill
- **位置**：`~/.openclaw/extensions/openclaw-workflowskill/`
- **功能**：YAML工作流编写、验证、执行、审查
- **状态**：✅ 已安装并生效
- **用途**：标准化工作流模板定义

### 备用：clawaid（已安装未配置）
- **功能**：AI自动诊断修复（崩溃/配置错误/网络问题/模型失败）
- **状态**：已安装，需手动启用

---

## 未安装的技能

### openclaw-hybrid-memory
- **功能**：持久记忆+语义搜索（SQLite+LanceDB）
- **状态**：已安装未配置，需要embedding API Key
- **替代方案**：使用本地elite-longterm-memory技能

### openclaw-plugin-life-validation
- **功能**：验证层（冲突检测、可信度裁决、记忆审计）
- **状态**：插件格式不兼容
- **替代方案**：使用本地task-validator技能

---

## 模型配置

| 场景 | 模型 | 配置 |
|------|------|------|
| 默认 | MiniMax M2.5 | minimax-cn/MiniMax-M2.5 |
| 图片理解 | Qwen Vision | 自动切换 |
| 本地推理 | Qwen3:32b | ollama/qwen3:32b |
