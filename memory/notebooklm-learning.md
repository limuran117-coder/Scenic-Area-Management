# NotebookLM 学习笔记

> 创建时间：2026-03-19
> 任务来源：Cron定时任务

## 1. NotebookLM 简介

NotebookLM 是 Google 推出的 AI 笔记和研究助手，主要功能包括：
- **来源管理**：支持添加 URL、Google Drive 文件、文本、PDF 等作为来源
- **AI 聊天**：基于来源内容进行问答
- **内容生成**：生成音频概述（播客）、视频、报告、测验、闪卡
- **研究功能**：网络搜索和 Drive 搜索

## 2. CLI 安装与配置

### 安装
```bash
npm install -g notebooklm
```

### 认证
```bash
notebooklm login
# 需要在浏览器中完成 Google 账号授权
```

## 3. 常用命令

### 认证与状态
```bash
notebooklm login              # 登录
notebooklm status             # 查看登录状态
```

### 笔记本管理
```bash
notebooklm list               # 列出所有笔记本
notebooklm create "标题"      # 创建新笔记本
notebooklm delete <id>        # 删除笔记本
notebooklm rename <id> "新标题"  # 重命名
```

### 来源管理
```bash
notebooklm source add <notebookId> <url>     # 添加 URL 来源
notebooklm source add-text <notebookId> <title>  # 添加文本来源
notebooklm source add-file <notebookId> <filePath>  # 添加文件来源
notebooklm source list <notebookId>           # 列出来源
notebooklm source refresh <notebookId> <sourceId>  # 刷新来源
```

### 聊天功能
```bash
notebooklm ask <notebookId> "问题内容"
```

### AI 内容生成
```bash
notebooklm generate audio <notebookId>    # 生成音频概述（播客）
notebooklm generate video <notebookId>     # 生成视频概述
notebooklm generate report <notebookId>   # 生成报告
notebooklm generate quiz <notebookId>      # 生成测验
notebooklm generate flashcards <notebookId>  # 生成闪卡
```

### 研究功能
```bash
notebooklm research web <notebookId> <query>    # 网络搜索
notebooklm research drive <notebookId> <query>  # Drive 搜索
```

## 4. OpenClaw 集成

### 通过 Skill 调用
OpenClaw 提供了 NotebookLM skill，位于 `~/.openclaw/skills/tiangong-notebooklm-cli/`

调用方式：
```bash
node ~/.openclaw/skills/tiangong-notebooklm-cli/scripts/notebooklm.mjs <command>
```

### 配合使用的最佳实践

1. **工作流程自动化**
   - 使用 CLI 自动创建笔记本
   - 批量添加来源
   - 自动生成内容

2. **研究与笔记**
   - 使用 `research web` 命令进行主题研究
   - 自动将搜索结果添加到笔记本
   - 生成音频概述方便学习

3. **内容创作**
   - 上传参考资料到笔记本
   - 使用 AI 生成报告、测验、闪卡
   - 导出生成的内容

4. **定时任务**
   - 可以通过 cron 定时运行研究任务
   - 定期生成内容更新

## 5. 注意事项

- 首次使用需要通过浏览器登录 Google 账号
- 某些功能（如 Google Drive 集成）需要相应权限
- 生成内容可能需要等待一段时间

## 6. 后续探索

- [ ] 完成登录并创建第一个测试笔记本
- [ ] 尝试添加 PDF 文件来源
- [ ] 尝试生成音频概述
- [ ] 探索与 OpenClaw 其他工具的集成

## 7. 当前状态

**登录状态**：需要手动完成

NotebookLM CLI 需要通过浏览器进行 Google 账号授权。目前在 cron 任务中无法自动完成交互式登录。

### 手动登录步骤
```bash
notebooklm login
# 会在浏览器中打开登录页面
# 登录成功后按 Enter 继续
```

### 登录后创建测试笔记本
```bash
# 登录后查看笔记本列表
notebooklm list

# 创建测试笔记本
notebooklm create "OpenClaw 测试笔记本"

# 添加来源（URL 或文件）
notebooklm source add <notebookId> https://example.com
notebooklm source add-file <notebookId> ./document.pdf

# 提问
notebooklm ask <notebookId> "总结这个笔记本的内容"

# 生成音频概述
notebooklm generate audio <notebookId>
```
