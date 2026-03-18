# NotebookLM 学习笔记

> 更新日期：2026-03-18

## 1. 概述

NotebookLM 是 Google 的 AI 笔记本工具，核心能力：
- **Source-grounded Q&A**: 基于上传的文档回答问题，引用原文
- **Audio Overview**: 生成播客风格的音频对话
- **多种内容生成**: 幻灯片、测验、闪卡、思维导图、信息图表、视频、数据表

## 2. OpenClaw 可用的 NotebookLM 技能

### 2.1 notebooklm-skill
- **特点**: 浏览器自动化版本，每次问题打开新浏览器会话
- **命令**: `python scripts/run.py [script]`
- **用途**: 适合快速查询文档

### 2.2 notebooklm-cli-v2 (推荐)
- **特点**: 全功能 CLI，支持所有生成类型
- **命令**: `nlm [command]`
- **安装**: `pip install notebooklm-mcp-cli`
- **用途**: 生产环境使用

### 2.3 tiangong-notebooklm-cli
- **特点**: 官方 NotebookLM CLI 包装器
- **命令**: `notebooklm` (需单独安装)

### 2.4 notebooklm-ppt
- **特点**: PPT 生成专用，包含预置风格模板
- **模板风格**: 现代报纸、极简、漫画、杂志等 12 种

### 2.5 notebooklm-ops
- **特点**: Linux MCP 运维自动化 (本环境不适用)

## 3. nlm CLI 核心命令

### 认证
```bash
nlm login          # 打开 Chrome 进行认证
nlm doctor         # 检查安装和认证状态
nlm auth list      # 列出所有配置档案
```

### 笔记本管理
```bash
nlm notebook list                    # 列出所有笔记本
nlm notebook create "标题"            # 创建新笔记本
nlm notebook describe <id>           # AI 总结
nlm notebook query <id> "问题"        # 问答
```

### 源管理
```bash
nlm source add <id> --url "https://..."    # 添加 URL 源
nlm source add <id> --text "内容" --title "标题"  # 添加文本
nlm source list <id>                        # 列出源
```

### 内容生成 (全部需要 --confirm)
```bash
nlm audio create <id> --confirm        # 播客
nlm slides create <id> --confirm       # 幻灯片
nlm quiz create <id> --confirm         # 测验
nlm flashcards create <id> --confirm   # 闪卡
nlm mindmap create <id> --confirm      # 思维导图
nlm report create <id> --confirm      # 报告
nlm video create <id> --confirm       # 视频
nlm infographic create <id> --confirm  # 信息图表
```

### 下载
```bash
nlm studio status <id>                          # 查看生成的产物
nlm download slide-deck <id> --id <artifact> --format pptx  # 下载 PPT
```

## 4. 最佳实践

### 与 OpenClaw 配合
1. **自动化问答**: 将 notebooklm-skill 用于文档查询
2. **PPT 生成**: 使用 notebooklm-ppt 配合预置模板
3. **内容创作**: 使用 nlm CLI 生成播客、报告等

### 使用技巧
- 每次生成内容都会创建新版本，记录 artifact_id
- 建议文件大小 <15MB
- 使用 alias 设置笔记本简称方便操作
- 支持多账户 (profiles)

## 5. 当前状态

- [x] nlm CLI 已安装 (v0.4.9)
- [ ] 认证完成 (需要用户手动登录 Chrome)
- [ ] 创建测试笔记本

## 6. 待完成任务

- [ ] 执行 `nlm login` 完成认证
- [ ] 创建第一个测试笔记本
- [ ] 测试添加源和问答功能
- [ ] 测试生成幻灯片

---

## 相关技能位置
- `~/.openclaw/skills/notebooklm-skill/`
- `~/.openclaw/skills/notebooklm-cli-v2/`
- `~/.openclaw/skills/notebooklm-ppt/`
- `~/.openclaw/skills/tiangong-notebooklm-cli/`
