# OpenClaw Skills 详细功能说明

> 2026-03-25 | 必要安装(3) + 建议安装(5)

---

## 一、必要安装技能 🟢

### 1. active-maintenance
**安装命令**: `clawhub install trypto1019-active-maintenance`

**功能说明**:
- **系统健康检查**: 自动检测OpenClaw系统状态，监控内存、CPU、存储等
- **内存代谢**: 自动清理过期的临时文件和缓存，防止内存无限膨胀
- **主动维护**: 定期执行维护任务，保持系统运行在最佳状态
- **异常预警**: 检测到异常时主动告警

**价值**: 保障系统长期稳定运行，防止内存泄漏导致性能下降

---

### 2. arc-memory-pruner
**安装命令**: `clawhub install trypto1019-arc-memory-pruner`

**功能说明**:
- **内存文件修剪**: 自动检测并清理过大的内存文件
- **防止无限增长**: 定期压缩历史记忆数据，保持文件大小可控
- **智能清理**: 只清理过期或不重要的记忆，保留关键信息
- **定期执行**: 可设置定时任务，自动执行清理

**价值**: 防止memory目录无限膨胀，影响系统性能和磁盘空间

---

### 3. audit-code
**安装命令**: `clawhub install itsnishi-audit-code`

**功能说明**:
- **敏感信息检测**: 扫描代码中的API Key、密码、token等敏感信息
- **安全漏洞检查**: 检测常见的安全隐患和代码缺陷
- **代码质量审计**: 提供代码安全性评分和建议
- **多语言支持**: 支持Python、JavaScript、Java等多种语言

**价值**: 防止代码中的敏感信息泄露，避免安全风险

---

## 二、建议安装技能 🔵

### 4. alex-session-wrap-up
**安装命令**: `clawhub install xbillwatsonx-alex-session-wrap-up`

**功能说明**:
- **自动提交**: 会话结束时自动检测未推送的变更并commit
- **学习要点提取**: 自动从会话中提取学习要点和重要决策
- **模式检测**: 分析历史会话，发现重复模式和问题
- **规则持久化**: 将学到的规则自动保存，供后续使用

**价值**: 再也不怕忘记提交代码，自动沉淀经验教训

---

### 5. agent-cost-monitor
**安装命令**: `clawhub install neal-collab-agent-cost-monitor`

**功能说明**:
- **实时成本追踪**: 监控所有OpenClaw Agent的token使用量
- **费用统计**: 按天/周/月统计API调用费用
- **预算提醒**: 设置预算阈值，超过时自动提醒
- **优化建议**: 分析使用模式，提供成本优化建议
- **多模型支持**: 支持MiniMax、Claude、OpenAI等多种模型

**价值**: 清晰了解AI使用成本，避免意外超额

---

### 6. csv-pipeline
**安装命令**: `clawhub install gitgoodordietrying-csv-pipeline`

**功能说明**:
- **数据处理**: 处理、转换、分析CSV和JSON文件
- **数据清洗**: 自动清洗脏数据，处理缺失值
- **格式转换**: 支持CSV/JSON/Excel等多种格式互转
- **报表生成**: 自动生成数据分析报表
- **管道处理**: 支持多步骤数据管道处理

**价值**: 快速处理景区数据报表，生成分析结果

---

### 7. api-tester
**安装命令**: `clawhub install wanng-ide-api-tester`

**功能说明**:
- **HTTP请求**: 支持GET/POST/PUT/DELETE等HTTP方法
- **自定义请求**: 支持自定义headers和JSON body
- **响应验证**: 自动验证API响应格式和内容
- **测试用例**: 支持保存和复用测试用例
- **批量测试**: 批量执行API测试，生成测试报告

**价值**: 快速测试各种API接口，调试数据接口

---

### 8. add-analytics
**安装命令**: `clawhub install jeftekhari-add-analytics`

**功能说明**:
- **GA4集成**: 为项目自动添加Google Analytics 4追踪代码
- **事件追踪**: 自动设置常见事件追踪
- **转化漏斗**: 配置转化跟踪和漏斗分析
- **代码注入**: 自动注入追踪代码到网页

**价值**: 分析网站访客行为，优化营销效果

---

## 三、技能协同效应

### 日常运维组合
```
active-maintenance (健康检查)
    ↓
arc-memory-pruner (内存清理)
    ↓
agent-cost-monitor (成本监控)
```

### 开发效率组合
```
alex-session-wrap-up (自动提交)
    ↓
audit-code (安全审计)
    ↓
csv-pipeline (数据处理)
```

### 接口调试组合
```
api-tester (API测试)
    ↓
add-analytics (分析集成)
```

---

## 四、安装顺序建议

```
第1步: 安装3个必要技能
├── active-maintenance
├── arc-memory-pruner
└── audit-code

第2步: 安装5个建议技能
├── alex-session-wrap-up
├── agent-cost-monitor
├── csv-pipeline
├── api-tester
└── add-analytics
```

---

*注：安装前请确认clawhub CLI已安装，部分技能需要API Key*
