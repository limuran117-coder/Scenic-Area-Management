# OpenClaw Skills 手动安装指南

> 2026-03-25 | 需要手动下载安装的技能

---

## 🟢 必要安装 (3个)

| # | 技能 | 下载URL |
|---|------|---------|
| 1 | **auto-updater** (系统自动维护) | https://github.com/openclaw/skills/tree/main/skills/maximeprades-auto-updater |
| 2 | **arc-memory-pruner** (内存清理) | https://github.com/openclaw/skills/tree/main/skills/trypto1019-arc-memory-pruner |
| 3 | **audit-code** (代码审计) | https://github.com/openclaw/skills/tree/main/skills/itsnishi-audit-code |

---

## 🔵 建议安装 (5个)

| # | 技能 | 下载URL |
|---|------|---------|
| 4 | **alex-session-wrap-up** (自动提交) | https://github.com/openclaw/skills/tree/main/skills/xbillwatsonx-alex-session-wrap-up |
| 5 | **agent-cost-monitor** (成本监控) | https://github.com/openclaw/skills/tree/main/skills/neal-collab-agent-cost-monitor |
| 6 | **csv-pipeline** (数据处理) | https://github.com/openclaw/skills/tree/main/skills/gitgoodordietrying-csv-pipeline |
| 7 | **api-tester** (API测试) | https://github.com/openclaw/skills/tree/main/skills/wanng-ide-api-tester |
| 8 | **add-analytics** (GA4分析) | https://github.com/openclaw/skills/tree/main/skills/jeftekhari-add-analytics |

---

## 📥 手动安装步骤

### 方法1：直接下载ZIP
1. 访问上面对应的GitHub链接
2. 点击绿色 "Code" 按钮
3. 选择 "Download ZIP"
4. 解压后放到 `~/.openclaw/skills/` 目录

### 方法2：克隆单个技能
```bash
cd ~/.openclaw/skills
git clone --depth 1 https://github.com/openclaw/skills.git --branch main --single-branch --filter=blob:none --sparse skills_temp
cd skills_temp
git sparse-checkout set skills/技能名称
cp -r skills/技能名称 ../ 
cd .. && rm -rf skills_temp
```

### 方法3：下载完整仓库（推荐）
```bash
# 一次性下载所有技能（较大，约500MB）
cd ~/.openclaw/skills
curl -L "https://github.com/openclaw/skills/archive/refs/heads/main.zip" -o skills.zip
unzip -o skills.zip
# 复制需要的技能
cp -r skills-main/skills/maximeprades-auto-updater .
cp -r skills-main/skills/trypto1019-arc-memory-pruner .
# ... 其他需要的技能
# 清理
rm -rf skills-main skills.zip
```

---

## 📋 技能对应目录

安装后放至：`~/.openclaw/skills/<技能名>/`

例如：
```
~/.openclaw/skills/
├── maximeprades-auto-updater/
│   ├── SKILL.md
│   └── references/
├── oyi77-data-analyst/
│   ├── SKILL.md
│   └── references/
└── ...
```

---

## 🔗 快速访问汇总

### 必要安装
- auto-updater: https://github.com/openclaw/skills/tree/main/skills/maximeprades-auto-updater
- arc-memory-pruner: https://github.com/openclaw/skills/tree/main/skills/trypto1019-arc-memory-pruner
- audit-code: https://github.com/openclaw/skills/tree/main/skills/itsnishi-audit-code

### 建议安装
- alex-session-wrap-up: https://github.com/openclaw/skills/tree/main/skills/xbillwatsonx-alex-session-wrap-up
- agent-cost-monitor: https://github.com/openclaw/skills/tree/main/skills/neal-collab-agent-cost-monitor
- csv-pipeline: https://github.com/openclaw/skills/tree/main/skills/gitgoodordietrying-csv-pipeline
- api-tester: https://github.com/openclaw/skills/tree/main/skills/wanng-ide-api-tester
- add-analytics: https://github.com/openclaw/skills/tree/main/skills/jeftekhari-add-analytics
