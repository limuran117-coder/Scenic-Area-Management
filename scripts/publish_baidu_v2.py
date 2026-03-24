#!/usr/bin/env python3
"""
百家号发布图文 - V2版本
"""
import asyncio
from playwright.async_api import async_playwright
import os

async def publish_baidu():
    # 图片文件夹
    image_folder = "/Users/tianjinzhan/Desktop/图片资料/实拍街区图"
    
    # 获取文件夹中的图片 - 只取小的
    images = []
    for f in os.listdir(image_folder):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            img_path = os.path.join(image_folder, f)
            if os.path.getsize(img_path) < 10 * 1024 * 1024:
                images.append(img_path)
                if len(images) >= 3:  # 百家号支持3图
                    break
    
    print(f"找到 {len(images)} 张图片")
    
    # 文章内容
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

适合闺蜜打卡、情侣约会、家庭出游！"""

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:18800")
        context = browser.contexts[0]
        page = await context.new_page()
        
        # 打开百家号发布页面
        print("打开发布页面...")
        await page.goto("https://baijiahao.baidu.com/builder/rc/edit?type=news")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        
        # 填写标题
        print("填写标题...")
        try:
            title_input = await page.query_selector('input[placeholder*="标题"]')
            if title_input:
                await title_input.fill(title)
                print("✅ 标题已填写")
        except Exception as e:
            print(f"标题失败: {e}")
        
        # 填写正文 - 尝试点击正文区域
        print("填写正文...")
        try:
            # 找到iframe内的编辑器
            try:
                frame = page.frame(name="ueditor_0")
            except:
                frame = None
            if frame:
                editor = await frame.query_selector('.ql-editor')
                if editor:
                    await editor.fill(content)
                    print("✅ 正文已填写")
        except Exception as e:
            print(f"正文失败: {e}")
        
        # 上传封面图
        print("上传封面图...")
        try:
            cover_input = await page.query_selector('input[type="file"]')
            if cover_input and images:
                await cover_input.set_input_files([images[0]])
                print("✅ 封面图已上传")
        except Exception as e:
            print(f"封面上传失败: {e}")
        
        # 截图
        await page.screenshot(path="/Users/tianjinzhan/Desktop/baidu_preview.png")
        print("📸 预览图已保存")
        
        # 点击发布按钮
        print("点击发布...")
        try:
            publish_btn = await page.query_selector('button:has-text("发布")')
            if publish_btn:
                await publish_btn.click()
                print("✅ 已点击发布按钮")
        except Exception as e:
            print(f"发布失败: {e}")
        
        await page.wait_for_timeout(3000)
        await browser.close()
        print("✨ 百家号发布流程完成")

if __name__ == "__main__":
    asyncio.run(publish_baidu())
