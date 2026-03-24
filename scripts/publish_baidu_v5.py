#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百家号 V5 - 刷新页面后重新填写
"""

import asyncio
from playwright.async_api import async_playwright
import os
import time

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
    print("🚀 百家号 V5 发布")
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
        
        # 关闭现有百家号页面，重新打开
        print("🔄 刷新页面...")
        for p in list(browser.contexts[0].pages):
            if "baijiahao" in p.url:
                await p.close()
        
        # 新建页面
        page = await browser.contexts[0].new_page()
        await page.goto("https://baijiahao.baidu.com/builder/rc/edit?type=news")
        
        print("⏳ 等待页面加载...")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(5)  # 等待更长时间
        
        print(f"📄 当前页面: {page.url}")
        
        # 检查页面内容
        body = await page.inner_html('body')
        print(f"   页面长度: {len(body)} 字符")
        
        if len(body) < 1000:
            print("⚠️ 页面可能未完全加载，重试...")
            await page.reload()
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(5)
        
        # 步骤1: 填写标题
        print("📝 步骤1: 填写标题...")
        try:
            title_input = await page.wait_for_selector('input[placeholder*="标题"]', timeout=10000)
            if title_input:
                await title_input.fill(title)
                print("✅ 标题已填写")
        except Exception as e:
            print(f"⚠️ 标题: {e}")
            # 尝试其他选择器
            try:
                title_input = await page.query_selector('input[type="text"]')
                if title_input:
                    await title_input.fill(title)
                    print("✅ 标题已填写(备用)")
            except:
                pass
        
        # 步骤2: 点击正文编辑区
        print("🟢 步骤2: 点击正文编辑区...")
        try:
            # 等待编辑区出现
            await asyncio.sleep(2)
            content_selectors = ['div[contenteditable="true"]', '.ueditor_0', '#ueditor_0']
            for sel in content_selectors:
                try:
                    content_area = await page.wait_for_selector(sel, timeout=5000)
                    if content_area:
                        await content_area.click()
                        print(f"✅ 已点击: {sel}")
                        break
                except:
                    continue
        except Exception as e:
            print(f"⚠️ 点击正文: {e}")
        
        # 步骤3: 上传图片
        if images:
            print("🖼️ 步骤3: 上传图片...")
            try:
                file_inputs = await page.query_selector_all('input[type="file"]')
                for i, inp in enumerate(file_inputs[:3]):
                    try:
                        await inp.set_input_files([images[i]])
                        print(f"✅ 第{i+1}张")
                    except:
                        pass
            except Exception as e:
                print(f"⚠️ 图片: {e}")
        
        # 步骤4: 粘贴内容
        print("📋 步骤4: 粘贴内容...")
        try:
            await page.keyboard.type(content, delay=20)
            print("✅ 内容已粘贴")
        except Exception as e:
            print(f"⚠️ 粘贴: {e}")
        
        # 截图
        await page.screenshot(path="/Users/tianjinzhan/Desktop/baidu_v5_preview.png", full_page=True)
        print("📸 截图已保存")
        
        print("\n请检查截图，如需手动发布请点击发布按钮")
        print("⏸️ 等待30秒...")
        await asyncio.sleep(30)
        
        await browser.close()
        print("✨ 完成")

if __name__ == "__main__":
    asyncio.run(publish_baidu())
