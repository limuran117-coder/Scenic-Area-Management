# OpenClaw Skills 综合学习笔记

> 来源: VoltAgent/awesome-openclaw-skills | 日期: 2026-03-25

---

## 一、核心分类技能汇总

### 1.1 Browser & Automation (322个) - 浏览器自动化
| 技能 | 功能 | 适用场景 |
|------|------|----------|
| Agent Browser | Rust-based headless浏览器自动化CLI | 高效爬虫/测试 |
| agent-browser | 浏览器交互自动化 | 表单填写/web测试 |
| android-adb | Android设备控制 | 手机测试自动化 |
| anycrawl | AnyCrawl API集成 | 网页抓取/搜索 |
| api-tester | HTTP请求测试 | API调试 |
| apify-lead-generation | B2B潜在客户生成 | 竞品监控 |
| accessibility-toolkit | 无障碍优化 | 辅助功能检查 |

### 1.2 Git & GitHub (159个) - 代码管理
| 技能 | 功能 | 适用场景 |
|------|------|----------|
| alex-session-wrap-up | 会话结束自动化 | 自动提交/总结 |
| auto-pr-merger | 自动合并PR | 代码审查 |
| arc-skill-gitops | 技能自动化部署 | CI/CD |
| arc-security-audit | 安全审计 | 技能安全检查 |
| azure-devops | Azure DevOps集成 | 项目管理 |

### 1.3 CLI Utilities (179个) - 命令行工具
| 技能 | 功能 | 适用场景 |
|------|------|----------|
| arc-memory-pruner | 自动清理内存文件 | 防止内存膨胀 |
| activity-analyzer | ActivityWatch分析 | 用户行为分析 |
| audit-code | 代码安全审查 | 敏感信息检查 |
| agent-rate-limiter | API限流器 | 防止429错误 |
| agents-skill-security-audit | 供应链安全审计 | 技能安全 |

### 1.4 AI & LLMs (184个) - AI模型相关
| 技能 | 功能 | 适用场景 |
|------|------|----------|
| agent-memory | 持久记忆系统 | 长期记忆 |
| agent-orchestrator | 多Agent编排 | 复杂任务 |
| agent-context | 本地记忆系统 | 上下文管理 |
| agent-cost-monitor | 成本监控 | 费用追踪 |
| adaptive-suite | 自适应技能套件 | 动态配置 |
| adversarial-prompting | 对抗性提示分析 | 安全分析 |

### 1.5 Coding Agents & IDEs (1200个) - 编程开发
| 技能 | 功能 | 适用场景 |
|------|------|----------|
| active-maintenance | 系统健康/内存代谢 | 自动维护 |
| agent-audit | AI代理审计 | 性能/成本/ROI |
| agent-config | 核心配置文件修改 | 配置管理 |
| agent-council | 创建AI代理工具包 | Agent开发 |
| 2nd-brain | 个人知识库 | 信息管理 |

### 1.6 Data & Analytics (39个) - 数据分析
| 技能 | 功能 | 适用场景 |
|------|------|----------|
| add-analytics | GA4追踪添加 | 网站分析 |
| csv-pipeline | CSV/JSON处理 | 数据处理 |
| data-analyst | 数据可视化/报表 | 数据分析 |
| daily-report | 进度跟踪/报表 | 日报生成 |
| check-analytics | GA4审计 | 分析检查 |

### 1.7 PDF & Documents (105个) - 文档处理
（待提取）

### 1.8 Productivity & Tasks (205个) - 效率工具
（待提取）

### 1.9 Search & Research (345个) - 搜索研究
（待提取）

---

## 二、立即可用的技能（优先级排序）

### 🔴 高优先级 - 立即可用
| 技能 | 用途 | 状态 |
|------|------|------|
| active-maintenance | 系统自动维护/内存清理 | 待安装 |
| alex-session-wrap-up | 自动提交推送/会话总结 | 待安装 |
| agent-cost-monitor | 成本监控 | 待安装 |
| arc-memory-pruner | 内存文件自动清理 | 待安装 |
| audit-code | 代码安全审查 | 待安装 |

### 🟡 中优先级 - 探索价值
| 技能 | 用途 | 状态 |
|------|------|------|
| data-analyst | 数据可视化/报表 | 待探索 |
| agent-memory | 持久记忆系统 | 待探索 |
| api-tester | API测试 | 待探索 |
| csv-pipeline | 数据处理 | 待探索 |

### 🟢 低优先级 - 未来潜力
| 技能 | 用途 | 状态 |
|------|------|------|
| android-adb | Android控制 | 待研究 |
| anycrawl | 网页抓取 | 待研究 |
| azure-devops | 项目管理 | 待研究 |

---

## 三、技能安装命令

```bash
# 系统维护类
clawhub install trypto1019-active-maintenance
clawhub install trypto1019-arc-memory-pruner
clawhub install xbillwatsonx-alex-session-wrap-up
clawhub install neal-collab-agent-cost-monitor

# 安全审计类
clawhub install itsnishi-audit-code
clawhub install cerbug45-agents-skill-security-audit

# 数据分析类
clawhub install oyi77-data-analyst
clawhub install gitgoodordietrying-csv-pipeline
clawhub install jeftekhari-add-analytics

# 浏览器自动化类
clawhub install murphykobe-agent-browser-2
clawhub install techlaai-anycrawl
```

---

## 四、本地优化建议

### 4.1 系统维护
- 安装 `active-maintenance` - 自动系统健康检查
- 安装 `arc-memory-pruner` - 防止内存文件无限增长

### 4.2 开发效率
- 安装 `alex-session-wrap-up` - 自动提交总结
- 安装 `api-tester` - API调试

### 4.3 安全审计
- 安装 `audit-code` - 敏感信息检查
- 安装 `agents-skill-security-audit` - 供应链检查

### 4.4 数据处理
- 安装 `csv-pipeline` - CSV/JSON处理
- 安装 `data-analyst` - 数据分析可视化

---

## 五、后续行动计划

- [ ] 探索 PDF & Documents 分类
- [ ] 探索 Productivity & Tasks 分类  
- [ ] 探索 Search & Research 分类
- [ ] 安装高优先级技能
- [ ] 测试技能效果

---

## 六、完整分类统计

| 分类 | 技能数量 |
|------|----------|
| Coding Agents & IDEs | 1200 |
| Web & Frontend Development | 919 |
| DevOps & Cloud | 393 |
| Search & Research | 345 |
| Browser & Automation | 322 |
| Smart Home & IoT | 41 |
| Marketing & Sales | 102 |
| Communication | 146 |
| Total | 5000+ |
