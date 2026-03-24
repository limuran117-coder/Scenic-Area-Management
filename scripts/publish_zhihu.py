#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知乎自动发布脚本 V1
支持：发布文章
使用 Playwright + CDP 浏览器连接
"""

import asyncio
import os
import random
from datetime import datetime

# 配置
CDP_URL = "http://127.0.0.1:18800"
IMAGE_DIRS = [
    "/Users/tianjinzhan/Desktop/图片资料/小镇夜景",
    "/Users/tianjinzhan/Desktop/图片资料/实拍街区图",
    "/Users/tianjinzhan/Desktop/图片资料/活动图",
]

def get_today_images():
    """获取今日图片（基于日期哈希，每天不同）"""
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
    return random.sample(all_images, min(9, len(all_images)))

async def publish_zhihu_article(title, content):
    """发布知乎文章"""
    print("🚀 开始发布知乎文章...")
    
    async with asyncio.Semaphore(1):
        async with asyncio.timeout(60):
            try:
                # 连接到CDP
                from playwright.async_api import async_playwright
                async with async_playwright() as p:
                    # 连接到已运行的浏览器
                    browser = await p.chromium.connect_over_cdp(CDP_URL)
                    context = browser.contexts[0]
                    
                    # 找知乎页面
                    page = None
                    for p in context.pages:
                        if "zhihu.com" in p.url:
                            page = p
                            break
                    
                    if not page:
                        # 创建新标签
                        page = await context.new_page()
                        await page.goto("https://www.zhihu.com/publish/articles")
                        await page.wait_for_load_state("networkidle")
                        await asyncio.sleep(3)
                    
                    print(f"📄 当前页面: {page.url}")
                    
                    # 检查是否已登录
                    if "login" in page.url.lower():
                        print("❌ 请先手动登录知乎")
                        await browser.close()
                        return {"status": "error", "reason": "未登录"}
                    
                    # 填写标题
                    print("📝 填写标题...")
                    try:
                        title_input = await page.wait_for_selector(
                            'input[class*="Title-input"], input[placeholder*="标题"], input[class*="Input"]',
                            timeout=5000
                        )
                        if title_input:
                            await title_input.fill(title)
                            print("✅ 标题已填写")
                    except Exception as e:
                        print(f"⚠️ 标题填写尝试: {e}")
                    
                    # 填写正文 - 尝试多种选择器
                    print("📝 填写正文...")
                    try:
                        # 尝试正文编辑区域
                        editors = [
                            'div[class*="Editor-container"]',
                            'div[class*="rich-text"]', 
                            'div[contenteditable="true"]',
                            'div[class*="ql-editor"]'
                        ]
                        
                        for selector in editors:
                            editor = await page.query_selector(selector)
                            if editor:
                                await editor.fill(content)
                                print("✅ 正文已填写")
                                break
                    except Exception as e:
                        print(f"⚠️ 正文填写尝试: {e}")
                    
                    # 上传图片
                    if images := get_today_images():
                        print(f"📷 上传 {len(images)} 张图片...")
                        try:
                            # 查找图片上传按钮
                            upload_btn = await page.query_selector(
                                'input[type="file"], button[class*="upload"], div[class*="ImageUploader"]'
                            )
                            if upload_btn:
                                # 上传第一张图片作为封面
                                await upload_btn.set_input_files(images[:1])
                                print("✅ 图片已上传")
                        except Exception as e:
                            print(f"⚠️ 图片上传尝试: {e}")
                    
                    # 发布按钮
                    print("📤 尝试发布...")
                    try:
                        publish_btn = await page.wait_for_selector(
                            'button[class*="Publish"], button[class*="Submit"], button:has-text("发布")',
                            timeout=3000
                        )
                        if publish_btn:
                            await publish_btn.click()
                            print("✅ 文章已发布!")
                            await asyncio.sleep(2)
                    except Exception as e:
                        print(f"⚠️ 发布按钮: {e}")
                        print("ℹ️ 请手动点击发布按钮")
                    
                    await browser.close()
                    return {"status": "success", "platform": "知乎"}
                    
            except asyncio.TimeoutError:
                return {"status": "error", "reason": "超时"}
            except Exception as e:
                return {"status": "error", "reason": str(e)[:50]}

async def main():
    """主函数"""
    print("=" * 50)
    print("🚀 知乎文章自动发布")
    print("=" * 50)
    
    # 测试图片获取
    images = get_today_images()
    print(f"📷 今日图片: {len(images)}张")
    for img in images[:3]:
        print(f"   - {os.path.basename(img)}")
    
    # 默认文章内容
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

#郑州周边游 #电影小镇 #郑州旅游 #民国穿越 #一日游"""
    
    # 发布文章
    result = await publish_zhihu_article(title, content)
    print(f"\n📊 发布结果: {result}")

if __name__ == "__main__":
    asyncio.run(main())
