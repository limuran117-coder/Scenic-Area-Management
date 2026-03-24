#!/usr/bin/env python3
"""
小红书发布图文笔记 - 使用Playwright
"""
import asyncio
from playwright.async_api import async_playwright

async def publish_xiaohongshu():
    images = [
        "/Users/tianjinzhan/Desktop/图片资料/实拍街区图/AB2A9096.jpg",
        "/Users/tianjinzhan/Desktop/图片资料/实拍街区图/AB2A9099.jpg",
    ]
    title = "郑州周边一日游｜建业电影小镇穿越民国体验"
    content = """📸 郑州周边一日游推荐：建业电影小镇

想体验民国时期的郑州老街吗？这里超适合拍照打卡！

🎬 亮点推荐：
✅ 100+电影场景，民国复古风满满
✅ NPC互动表演，沉浸式穿越
✅ 夜晚灯光秀+打铁花，超出片！

📍 地址：郑州市中牟县
🎫 门票：120元/人
⏰ 建议游玩时间：半天-一天

#郑州周边游 #建业电影小镇 #民国风 #郑州打卡 #一日游推荐"""

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:18800")
        context = browser.contexts[0]
        page = await context.new_page()
        
        # 打开小红书创作者平台-图文发布
        await page.goto("https://creator.xiaohongshu.com/publish/publish?from=menu&target=image")
        await page.wait_for_load_state("networkidle")
        print("✅ 已打开发布页面")
        
        # 等待页面上传区域出现
        await page.wait_for_timeout(2000)
        
        # 查找文件输入框并上传图片
        try:
            file_input = await page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files(images)
                print(f"✅ 已选择 {len(images)} 张图片")
            else:
                print("❌ 未找到文件输入框")
        except Exception as e:
            print(f"❌ 图片上传失败: {e}")
        
        # 等待图片上传处理
        await page.wait_for_timeout(3000)
        
        # 尝试填写标题和内容
        try:
            # 查找标题输入框
            title_input = await page.query_selector('input[placeholder*="标题"]')
            if title_input:
                await title_input.fill(title)
                print("✅ 已填写标题")
        except Exception as e:
            print(f"填写标题失败: {e}")
        
        # 查找正文输入框
        try:
            # 小红书正文通常是textarea或者contenteditable div
            content_area = await page.query_selector('textarea') or await page.query_selector('[contenteditable="true"]')
            if content_area:
                await content_area.fill(content)
                print("✅ 已填写正文")
        except Exception as e:
            print(f"填写正文失败: {e}")
        
        # 等待一下让内容加载
        await page.wait_for_timeout(2000)
        
        # 截图保存当前状态
        await page.screenshot(path="/Users/tianjinzhan/Desktop/xiaohongshu_preview.png")
        print("📸 预览图已保存到桌面")
        
        # 尝试点击发布按钮
        try:
            publish_btn = await page.query_selector('button:has-text("发布")')
            if publish_btn:
                await publish_btn.click()
                print("✅ 已点击发布按钮")
                await page.wait_for_timeout(2000)
        except Exception as e:
            print(f"发布失败: {e}")
        
        await browser.close()
        print("✨ 发布流程完成")

if __name__ == "__main__":
    asyncio.run(publish_xiaohongshu())
