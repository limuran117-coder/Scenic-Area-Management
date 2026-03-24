#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub CLI 管理器 - 命令行版GitHub Desktop
功能：
1. 仓库管理（列表、克隆、创建）
2. 提交管理（查看、创建）
3. 分支管理
4. PR管理
5. 同步
"""

import subprocess
import os
import json
from datetime import datetime

WORKSPACE = "/Users/tianjinzhan/.openclaw/workspace"

def run_cmd(cmd):
    """执行shell命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def list_repos():
    """列出用户的仓库"""
    code, out, err = run_cmd("gh repo list --limit 20")
    if code != 0:
        return f"错误: {err}"
    
    lines = out.strip().split('\n')
    report = "# 📂 GitHub 仓库列表\n\n"
    report += "| # | 仓库名 | 描述 | 私有? |\n"
    report += "|:---:|:---|:---|:---:|\n"
    
    for i, line in enumerate(lines, 1):
        parts = line.split('\t')
        if len(parts) >= 2:
            name = parts[0]
            desc = parts[1] if len(parts) > 1 else ""
            is_private = "🔒" if "private" in line else "🌎"
            report += f"| {i} | {name} | {desc[:40]} | {is_private} |\n"
    
    return report

def create_commit(repo_path, message, files=None):
    """创建提交"""
    os.chdir(repo_path)
    
    # 添加文件
    if files:
        for f in files:
            run_cmd(f"git add {f}")
    else:
        run_cmd("git add .")
    
    # 提交
    code, out, err = run_cmd(f'git commit -m "{message}"')
    if code != 0:
        return f"提交失败: {err}"
    
    return f"✅ 提交成功: {message}"

def push():
    """推送到远程"""
    os.chdir(WORKSPACE)
    code, out, err = run_cmd("git push")
    if code != 0:
        return f"推送失败: {err}"
    return "✅ 推送成功"

def create_pr(title, body, base="main"):
    """创建PR"""
    code, out, err = run_cmd(f'gh pr create --title "{title}" --body "{body}" --base {base}')
    if code != 0:
        return f"创建PR失败: {err}"
    return f"✅ PR创建成功: {out.strip()}"

def sync_workspace():
    """同步工作区到GitHub"""
    os.chdir(WORKSPACE)
    
    # 检查变更
    code, out, err = run_cmd("git status --porcelain")
    if not out.strip():
        return "📝 没有变更需要提交"
    
    # 自动提交
    today = datetime.now().strftime("%Y-%m-%d")
    commit_msg = f"Auto-sync: {today}"
    
    run_cmd("git add .")
    run_cmd(f'git commit -m "{commit_msg}"')
    run_cmd("git push")
    
    return f"✅ 已同步: {commit_msg}"

def generate_github_report():
    """生成GitHub状态报告"""
    report = f"""# 📊 GitHub Desktop CLI 状态报告

---

## 📂 仓库

{list_repos()}

---

## 🔄 工作区同步

| 项目 | 状态 |
|------|------|
| 当前目录 | {WORKSPACE} |
| Git状态 | {run_cmd('git status --short')[1][:200] if run_cmd('git status --short')[1] else '正常'} |

---

## 📋 可用命令

| 命令 | 功能 |
|------|------|
| gh repo list | 列出仓库 |
| gh repo clone | 克隆仓库 |
| gh pr create | 创建PR |
| gh pr list | 列出PR |
| gh issue list | 列出Issue |

---

*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return report

if __name__ == "__main__":
    print(generate_github_report())
