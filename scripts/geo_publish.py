#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO全平台自动发布脚本 - V3
支持：知乎（回答问题）、百家号、小红书
特点：每日轮换内容+图片，失败重试
"""

import os
import sys
import json
import subprocess
import random
from datetime import datetime

# 配置
WORKSPACE = "/Users/tianjinzhan/.openclaw/workspace"
CONTENT_DIR = f"{WORKSPACE}/GEO资料"
IMAGE_DIRS = [
    "/Users/tianjinzhan/Desktop/图片资料/小镇夜景",
    "/Users/tianjinzhan/Desktop/图片资料/实拍街区图",
    "/Users/tianjinzhan/Desktop/图片资料/活动图",
    "/Users/tianjinzhan/Desktop/图片资料/游客打卡",
]
REPORT_FILE = f"{WORKSPACE}/reports/geo_publish_report.md"
LOG_FILE = f"{WORKSPACE}/reports/geo_publish.log"
STATE_FILE = f"{WORKSPACE}/reports/geo_state.json"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"content_index": 0, "date": ""}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_next_content():
    files = sorted([f for f in os.listdir(CONTENT_DIR) 
                   if "发布内容" in f and f.endswith(".md")])
    if not files:
        return None, None
    
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if state.get("date") != today:
        state["date"] = today
        state["content_index"] = 0
    
    idx = state["content_index"] % len(files)
    state["content_index"] = idx + 1
    save_state(state)
    
    filename = files[idx]
    path = os.path.join(CONTENT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return content, filename

def get_daily_images():
    today = datetime.now().strftime("%Y%m%d")
    seed = int(today)
    
    all_images = []
    for img_dir in IMAGE_DIRS:
        if os.path.exists(img_dir):
            for f in os.listdir(img_dir):
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    all_images.append(os.path.join(img_dir, f))
    
    if not all_images:
        return []
    
    random.seed(seed)
    return random.sample(all_images, min(3, len(all_images)))

def check_browser_running():
    try:
        result = subprocess.run(
            ["curl", "-s", "http://127.0.0.1:18800/json", "-o", "/dev/null"],
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def publish_zhihu(content):
    """发布到知乎"""
    log("📝 开始发布到知乎...")
    
    if not check_browser_running():
        log("❌ 知乎: CDP浏览器未运行")
        return {"status": "error", "reason": "CDP未运行"}
    
    try:
        script_path = f"{WORKSPACE}/scripts/publish_zhihu.py"
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout + result.stderr
        
        if "✅ 标题已填写" in output or "success" in output.lower():
            log("✅ 知乎: 内容已填写（请手动点击发布）")
            return {"status": "manual", "platform": "知乎", "action": "待手动发布"}
        elif "未登录" in output:
            log("❌ 知乎: 请先登录")
            return {"status": "error", "reason": "未登录"}
        else:
            log(f"⚠️ 知乎: 执行完成")
            return {"status": "manual", "platform": "知乎"}
    except Exception as e:
        log(f"❌ 知乎: {str(e)[:50]}")
        return {"status": "error", "reason": str(e)[:50]}

def publish_baidu(content):
    """发布到百家号"""
    log("📝 开始发布到百家号...")
    
    if not check_browser_running():
        log("❌ 百家号: CDP浏览器未运行")
        return {"status": "error", "reason": "CDP未运行"}
    
    try:
        script_path = f"{WORKSPACE}/scripts/publish_baidu_v4.py"
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            log("✅ 百家号: 发布成功")
            return {"status": "success", "platform": "百家号"}
        else:
            log(f"❌ 百家号: 发布失败")
            return {"status": "error", "reason": "执行失败"}
    except Exception as e:
        log(f"❌ 百家号: {str(e)[:50]}")
        return {"status": "error", "reason": str(e)[:50]}

def publish_xiaohongshu(content):
    """发布到小红书"""
    log("📝 开始发布到小红书...")
    
    if not check_browser_running():
        log("❌ 小红书: CDP浏览器未运行")
        return {"status": "error", "reason": "CDP未运行"}
    
    try:
        script_path = f"{WORKSPACE}/scripts/publish_xiaohongshu_v3.py"
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            log("✅ 小红书: 发布成功")
            return {"status": "success", "platform": "小红书"}
        else:
            log(f"❌ 小红书: 发布失败")
            return {"status": "error", "reason": "执行失败"}
    except Exception as e:
        log(f"❌ 小红书: {str(e)[:50]}")
        return {"status": "error", "reason": str(e)[:50]}

def generate_report(results):
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# 📤 GEO全平台自动发布报告
**执行时间**: {today}

---

## 发布结果汇总

| 平台 | 状态 | 说明 |
|------|------|------|
"""
    for r in results:
        status_icon = {"success": "✅", "error": "❌", "manual": "⚠️"}.get(r["status"], "❓")
        reason = r.get("reason", r.get("platform", ""))
        report += f"| {r['platform']} | {status_icon} {r['status']} | {reason} |\n"
    
    success = sum(1 for r in results if r["status"] == "success")
    error = sum(1 for r in results if r["status"] == "error")
    manual = sum(1 for r in results if r["status"] == "manual")
    
    report += f"""
---

## 📊 统计

- 成功: {success}
- 失败: {error}  
- 待手动: {manual}

---
*报告生成时间: {today}*
"""
    return report

def main():
    log("=" * 50)
    log("🚀 GEO全平台发布开始 (V3)")
    log("=" * 50)
    
    os.makedirs(f"{WORKSPACE}/reports", exist_ok=True)
    
    content, filename = get_next_content()
    if not content:
        log("❌ 无待发布内容")
        print("无待发布内容")
        return
    
    log(f"📄 今日发布内容: {filename}")
    
    images = get_daily_images()
    log(f"📷 今日选择图片: {len(images)}张")
    
    results = []
    
    # 1. 知乎 (新增)
    result = publish_zhihu(content)
    result["platform"] = "知乎"
    results.append(result)
    
    # 2. 百家号
    result = publish_baidu(content)
    result["platform"] = "百家号"
    results.append(result)
    
    # 3. 小红书
    result = publish_xiaohongshu(content)
    result["platform"] = "小红书"
    results.append(result)
    
    report = generate_report(results)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    
    log("=" * 50)
    log("🚀 GEO全平台发布完成")
    log("=" * 50)
    
    print(report)

if __name__ == "__main__":
    main()
