#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百家号 V4 - 不自动关闭浏览器，截图后手动关闭
"""

import asyncio
from playwright.async_api import async_playwright
import os

CDP_URL = "http://127.0.0.1:18800"
IMAGE_DIRS = [
    "/Users/tianjinzhan/Desktop/图片资料/小镇夜景",
    "/Users/tianjinzhan/Desktop/图片资料/实拍街区图",
]

def get_today_images():
    import random
    from datetime import datetime
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

async def publish_baidu():
    print("=" * 50)
    print("🚀 百家号 V4 发布")
    print("=" * 50)
    
    images = get_today_images()
    print(f"📷 找到 {len(images)} 张图片")
    
    title = "郑州周边一日游推荐：建业电影小镇穿越民国体验"
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

#郑州周边游 #电影小镇 #郑州旅游"""
    
    async with async_playwright() as p:
        print("🔗 连接CDP浏览器...")
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        
        page = None
        for p in browser.contexts[0].pages:
            if "baijiahao" in p.url:
                page = p
                break
        
        if not page:
            page = await browser.contexts[0].new_page()
            await page.goto("https://baijiahao.baidu.com/builder/rc/edit?type=news")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(3)
        
        print(f"📄 当前页面: {page.url[:60]}")
        
        # 步骤1: 填写标题
        print("📝 步骤1: 填写标题...")
        try:
            title_input = await page.query_selector('input[placeholder*="标题"]')
            if not title_input:
                title_input = await page.query_selector('input[type="text"]')
            if title_input:
                await title_input.fill(title)
                print("✅ 标题已填写")
        except Exception as e:
            print(f"⚠️ 标题: {e}")
        
        # 步骤2: 点击大红色方框（正文编辑区）
        print("🟢 步骤2: 点击大红色方框（正文编辑区）...")
        try:
            content_selectors = ['div[contenteditable="true"]', '.ueditor_0', '#ueditor_0', 'div[class*="editor"]']
            content_area = None
            for sel in content_selectors:
                content_area = await page.query_selector(sel)
                if content_area:
                    print(f"   找到: {sel}")
                    break
            
            if content_area:
                await content_area.click()
                print("✅ 已点击正文编辑区")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ 点击正文区: {e}")
        
        # 步骤3: 上传图片
        if images:
            print("🖼️ 步骤3: 上传图片...")
            try:
                file_inputs = await page.query_selector_all('input[type="file"]')
                print(f"   找到 {len(file_inputs)} 个上传按钮")
                for i, inp in enumerate(file_inputs):
                    try:
                        await inp.set_input_files([images[i]])
                        print(f"✅ 第{i+1}张图片已选择")
                        await asyncio.sleep(1)
                    except:
                        pass
            except Exception as e:
                print(f"❌ 图片上传: {e}")
        
        # 步骤4: 粘贴内容
        print("📋 步骤4: 粘贴内容...")
        try:
            await page.mouse.click(x=400, y=450)
            await asyncio.sleep(0.5)
            await page.keyboard.type(content, delay=30)
            print("✅ 内容已粘贴")
        except Exception as e:
            print(f"❌ 粘贴: {e}")
        
        # 截图
        print("📸 截图...")
        try:
            await page.screenshot(path="/Users/tianjinzhan/Desktop/baidu_v4_preview.png", full_page=True)
            print("✅ 预览图已保存: baidu_v4_preview.png")
        except Exception as e:
            print(f"⚠️ 截图: {e}")
        
        print("\n" + "=" * 50)
        print("请手动完成以下步骤：")
        print("1. 检查内容是否正确")
        print("2. 点击右上角蓝色发布按钮")
        print("3. 关闭浏览器")
        print("=" * 50)
        
        # 不关闭浏览器，等待手动操作
        print("\n⏸️ 浏览器保持打开，按回车结束...")
        await asyncio.sleep(60)  # 保持60秒
        
        await browser.close()
        print("✨ 完成")

if __name__ == "__main__":
    asyncio.run(publish_baidu())
