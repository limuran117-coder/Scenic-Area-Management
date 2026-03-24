#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动同步工作区到GitHub - 增强版
每日执行 + 可选手动触发
"""

import subprocess
import os
import sys
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
LOG_FILE = os.path.expanduser("~/.openclaw/logs/github_sync.log")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

def run_cmd(cmd, cwd=WORKSPACE):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout, result.stderr

def get_status():
    """获取Git状态摘要"""
    code, out, err = run_cmd("git status --short")
    if not out.strip():
        return "✅ 无变更"
    
    lines = out.strip().split('\n')
    modified = sum(1 for l in lines if l.startswith(' M') or l.startswith('M '))
    added = sum(1 for l in lines if l.startswith('A '))
    deleted = sum(1 for l in lines if l.startswith('D '))
    untracked = sum(1 for l in lines if l.startswith('??'))
    
    return f"📝 {modified}修改 / {added}新增 / {deleted}删除 / {untracked}未跟踪"

def auto_sync(verbose=False):
    """自动同步"""
    if verbose:
        log("=" * 60)
        log("🚀 GitHub仓库同步工具")
        log("=" * 60)
        log(f"📁 工作区: {WORKSPACE}")
        log(f"📊 状态: {get_status()}")
    
    # 检查变更
    code, out, err = run_cmd("git status --porcelain")
    if not out.strip():
        if verbose:
            log("📝 没有变更，跳过同步")
        return
    
    # 添加所有变更
    if verbose:
        log("📦 添加所有变更...")
    run_cmd("git add .")
    
    # 提交
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"auto-sync: {today}"
    code, out, err = run_cmd(f'git commit -m "{commit_msg}"')
    
    if code != 0:
        if "nothing to commit" in err or "nothing to commit" in out:
            log("📝 没有需要提交的变更")
            return
        log(f"❌ 提交失败: {err}")
        return
    
    if verbose:
        log(f"✅ 已提交: {commit_msg}")
    
    # 推送
    code, out, err = run_cmd("git push origin main")
    if code != 0:
        log(f"❌ 推送失败: {err}")
        return
    
    if verbose:
        log("✅ 推送成功!")
        log(f"📊 同步后状态: {get_status()}")
    else:
        print("✅ GitHub同步完成")

if __name__ == "__main__":
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    auto_sync(verbose=verbose)
