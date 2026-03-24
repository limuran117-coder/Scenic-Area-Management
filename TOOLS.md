# TOOLS.md - 本地工具与脚本

## 数据查询脚本

### query_data_v2.py
电影小镇历史数据查询工具（防错版）

**位置**: `scripts/query_data_v2.py`

**使用方式**:
```bash
# 进入工作目录
cd /Users/tianjinzhan/.openclaw/workspace

# 数据校验
python3 scripts/query_data_v2.py --type validate

# 查询节假日
python3 scripts/query_data_v2.py --type holiday --name 清明节
python3 scripts/query_data_v2.py --type holiday --name 劳动节
python3 scripts/query_data_v2.py --type holiday --name 端午节
python3 scripts/query_data_v2.py --type holiday --name 国庆节
python3 scripts/query_data_v2.py --type holiday --name 春节

# 查询月度
python3 scripts/query_data_v2.py --type month --month 4
python3 scripts/query_data_v2.py --type month --month 5

# 查询单年
python3 scripts/query_data_v2.py --type holiday --name 清明节 --year 2024
```

**防错机制**:
- 动态日期匹配，不手动算列索引
- 节假日日期配置化管理
- 启动自动校验 + 抽样检查
- 打印每日明细供核对

**数据源**: `2023-2025年门票销售及客流统计数据表.xlsx`

---

## 注意事项

### 数据查询防错规范
1. **必须使用 query_data_v2.py**，不要手动写代码查询
2. **先运行校验**：确认数据文件正常
3. **核对明细**：查询结果会显示每日数据，记得核对
4. **注意日期**：节假日放假日每年可能不同，以配置为准

### 常见节假日日期（配置中已包含）
- 清明节：4月4-6日 或 4月5-7日
- 劳动节：4月29-5月3日 或 5月1-5日
- 端午节：6月
- 国庆节：10月1-7日

---

## 其他工具

### 抖音指数日报标准（重要！）

**脚本位置**：`/Users/tianjinzhan/.openclaw/workspace/scripts/douyin_index_v9.py`

**标准格式**（必须遵守）：
1. 所有数据以表格形式展示
2. 30天/7天搜索指数对比表
3. 人群画像对比表
4. 每个景区详细分析（含指标表格）
5. 竞品策略洞察表
6. 营销建议表

**重要**：分析内容需要自行优化纠错，根据数据变化给出深入洞察，不能简单填充表格

**发送时间**：每日8:00
**发送目标**：飞书群 oc_f109bcfd1bc7e166fd0ae077f70247cf

---

### 小红书数据分析日报（已创建）

**日报脚本**：`scripts/xiaohongshu_report.py`

**日报内容**：
- AIPS人群资产（认知/兴趣/深度兴趣/购买/分享）
- 行业排名变化
- 品牌度量数据
- **KOC矩阵效果分析**（重点！达人效果已被证伪）
- 综合洞察与营销建议

**核心原则**：聚焦KOC，弱化达人数据

**发送时间**：每日10:00
**发送目标**：飞书群 oc_f109bcfd1bc7e166fd0ae077f70247cf

### Excel处理
参见 `~/.openclaw/skills/excel-handler/SKILL.md`

### 飞书文档
参见 `~/.openclaw/skills/feishu-doc/SKILL.md`

### 浏览器自动化（反爬解决方案）
当web_search受限或网站有反爬时，使用Playwright浏览器自动化：

```bash
# 打开网页（可绑过反爬）
browser(action="open", url="https://www.xiaohongshu.com/explore")

# 获取页面内容
browser(action="snapshot")

# 截图保存
browser(action="screenshot", path="screenshot.png")
```

**优势**：
- 用真实Chrome浏览器，模拟人工操作
- 无需API Key
- 可抓取JS动态渲染的内容
- 可登录后抓取会员内容
