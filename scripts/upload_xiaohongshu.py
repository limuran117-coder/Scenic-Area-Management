#!/usr/bin/env python3
"""
小红书图片上传脚本 - 使用Playwright
"""
import asyncio
from playwright.async_api import async_playwright

async def upload_image():
    image_path = "/Users/tianjinzhan/Desktop/图片资料/实拍街区图/AB2A9096.jpg"
    
    async with async_playwright() as p:
        # 使用已存在的浏览器
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:18800")
        context = browser.contexts[0]
        page = await context.new_page()
        
        # 打开小红书创作者平台
        await page.goto("https://creator.xiaohongshu.com/publish/publish?from=menu&target=image")
        await page.wait_for_load_state("networkidle")
        
        # 等待上传按钮出现
        try:
            # 尝试找到文件输入框
            file_input = await page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files(image_path)
                print(f"✅ 图片已选择: {image_path}")
            else:
                print("❌ 未找到文件输入框")
        except Exception as e:
            print(f"❌ 上传失败: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(upload_image())
