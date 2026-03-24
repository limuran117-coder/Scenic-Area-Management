#!/usr/bin/env python3
"""
小红书发布图文笔记 - V2版本
"""
import asyncio
from playwright.async_api import async_playwright
import os

async def publish_xiaohongshu():
    # 图片文件夹
    image_folder = "/Users/tianjinzhan/Desktop/图片资料/实拍街区图"
    
    # 获取文件夹中的图片 - 只取前3张
    images = []
    for f in os.listdir(image_folder):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            img_path = os.path.join(image_folder, f)
            # 检查文件大小，只选小于10MB的
            if os.path.getsize(img_path) < 10 * 1024 * 1024:
                images.append(img_path)
                if len(images) >= 9:  # 最多9张图，小红书支持9图
                    break
    
    print(f"找到 {len(images)} 张图片: {images}")
    
    # 笔记内容
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
        print("打开发布页面...")
        await page.goto("https://creator.xiaohongshu.com/publish/publish?from=menu&target=image")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        
        # 查找文件输入框
        print("查找上传按钮...")
        file_input = await page.query_selector('input[type="file"]')
        if file_input:
            # 使用set_input_files上传图片
            await file_input.set_input_files(images)
            print(f"✅ 已选择 {len(images)} 张图片")
        else:
            print("❌ 未找到文件输入框")
            await browser.close()
            return
        
        # 等待图片上传处理
        print("等待图片上传...")
        await page.wait_for_timeout(5000)
        
        # 填写标题 - 尝试多种选择器
        print("填写标题...")
        try:
            # 尝试多种选择器
            title_selectors = [
                'input[placeholder*="标题"]',
                'input[placeholder*="标题"]',
                '.title-input input',
                'input.title'
            ]
            for selector in title_selectors:
                title_input = await page.query_selector(selector)
                if title_input:
                    await title_input.fill(title)
                    print("✅ 标题已填写")
                    break
        except Exception as e:
            print(f"填写标题失败: {e}")
        
        # 填写正文
        print("填写正文...")
        try:
            content_selectors = [
                'textarea',
                '.content-editor',
                '[contenteditable="true"]',
                '.ql-editor'
            ]
            for selector in content_selectors:
                content_area = await page.query_selector(selector)
                if content_area:
                    await content_area.fill(content)
                    print("✅ 正文已填写")
                    break
        except Exception as e:
            print(f"填写正文失败: {e}")
        
        # 等待内容加载
        await page.wait_for_timeout(2000)
        
        # 截图保存当前状态
        await page.screenshot(path="/Users/tianjinzhan/Desktop/xiaohongshu_preview.png")
        print("📸 预览图已保存")
        
        # 查找并点击发布按钮
        print("查找发布按钮...")
        try:
            publish_selectors = [
                'button:has-text("发布")',
                '.publish-btn',
                'button.btn-primary'
            ]
            for selector in publish_selectors:
                publish_btn = await page.query_selector(selector)
                if publish_btn:
                    await publish_btn.click()
                    print("✅ 已点击发布按钮")
                    await page.wait_for_timeout(3000)
                    break
        except Exception as e:
            print(f"发布失败: {e}")
        
        # 再次截图
        await page.screenshot(path="/Users/tianjinzhan/Desktop/xiaohongshu_after.png")
        
        await browser.close()
        print("✨ 发布流程完成")

if __name__ == "__main__":
    asyncio.run(publish_xiaohongshu())
