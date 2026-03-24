#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书发布 - V3版本（9图版）- 修复50MB限制
"""

import asyncio
from playwright.async_api import async_playwright
import os

CDP_URL = "http://127.0.0.1:18800"
IMAGE_DIRS = [
    "/Users/tianjinzhan/Desktop/图片资料/小镇夜景",
    "/Users/tianjinzhan/Desktop/图片资料/实拍街区图",
    "/Users/tianjinzhan/Desktop/图片资料/活动图",
    "/Users/tianjinzhan/Desktop/图片资料/游客打卡",
]

def get_small_images(max_size_mb=20, count=9):
    """获取小于max_size_mb的图片"""
    import random
    from datetime import datetime
    today = datetime.now().strftime("%Y%m%d")
    seed = int(today)
    
    all_images = []
    for img_dir in IMAGE_DIRS:
        if os.path.exists(img_dir):
            for f in os.listdir(img_dir):
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    img_path = os.path.join(img_dir, f)
                    size_mb = os.path.getsize(img_path) / (1024 * 1024)
                    if size_mb < max_size_mb:
                        all_images.append(img_path)
    
    if not all_images:
        return []
    
    random.seed(seed)
    return random.sample(all_images, min(count, len(all_images)))

async def publish_xiaohongshu():
    print("=" * 50)
    print("🚀 小红书 V3 发布 (9图)")
    print("=" * 50)
    
    # 获取小于20MB的图片
    images = get_small_images(max_size_mb=20, count=9)
    print(f"📷 找到 {len(images)} 张图片 (<20MB)")
    for i, img in enumerate(images):
        size = os.path.getsize(img) / (1024*1024)
        print(f"   {i+1}. {os.path.basename(img)} ({size:.1f}MB)")
    
    title = "郑州周边一日游｜建业电影小镇穿越民国体验"
    content = """📸 郑州周边一日游推荐：建业电影小镇穿越民国体验

想体验民国时期的郑州老街吗？建业电影小镇是不错的选择！

🎬 亮点推荐：
1️⃣ 100+电影场景，民国复古风满满
2️⃣ NPC互动表演，沉浸式穿越
3️⃣ 夜晚灯光秀+打铁花，超出片！

📍 地址：郑州市中牟县
🎫 门票：120元/人
⏰ 建议游玩时间：半天-一天

适合闺蜜打卡、情侣约会、家庭出游！

#郑州周边游 #电影小镇 #郑州旅游 #民国穿越 #一日游 #郑州周末好去处"""
    
    async with async_playwright() as p:
        print("🔗 连接CDP浏览器...")
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        
        page = None
        for p in browser.contexts[0].pages:
            if "xiaohongshu.com" in p.url and "publish" in p.url:
                page = p
                break
        
        if not page:
            page = await browser.contexts[0].new_page()
            await page.goto("https://creator.xiaohongshu.com/publish/publish")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(3)
        
        print(f"📄 当前页面: {page.url[:60]}")
        
        # 步骤1: 逐个上传图片（避免50MB限制）
        print(f"🖼️ 步骤1: 上传 {len(images)} 张图片...")
        try:
            upload_input = await page.query_selector('input[type="file"]')
            if upload_input:
                # 逐个上传
                for i, img in enumerate(images):
                    try:
                        await upload_input.set_input_files([img])
                        print(f"   上传第{i+1}张...")
                        await asyncio.sleep(1)
                    except Exception as e:
                        print(f"   第{i+1}张失败: {str(e)[:30]}")
                print("✅ 图片上传完成")
        except Exception as e:
            print(f"⚠️ 上传: {e}")
        
        # 步骤2: 填写标题
        print("📝 步骤2: 填写标题...")
        try:
            title_input = await page.query_selector('input[placeholder*="标题"]')
            if title_input:
                await title_input.fill(title)
                print("✅ 标题已填写")
        except Exception as e:
            print(f"⚠️ 标题: {e}")
        
        # 步骤3: 填写正文
        print("📋 步骤3: 填写正文...")
        try:
            content_input = await page.query_selector('textarea[placeholder*="正文"]')
            if content_input:
                await content_input.fill(content)
                print("✅ 正文已填写")
        except Exception as e:
            print(f"⚠️ 正文: {e}")
        
        # 截图
        await page.screenshot(path="/Users/tianjinzhan/Desktop/xiaohongshu_v3_preview.png", full_page=True)
        print("📸 截图已保存")
        
        # 步骤4: 点击发布
        print("📤 步骤4: 点击发布...")
        try:
            publish_btn = await page.query_selector('button:has-text("发布")')
            if publish_btn:
                await publish_btn.click()
                print("✅ 已点击发布")
        except Exception as e:
            print(f"⚠️ 发布: {e}")
        
        print("\n请检查发布结果")
        await asyncio.sleep(10)
        
        await browser.close()
        print("✨ 小红书 V3 完成")

if __name__ == "__main__":
    asyncio.run(publish_xiaohongshu())
