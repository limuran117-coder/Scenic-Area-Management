#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百家号发布图文 - V3版本（修复版）
修复：蓝色按钮插入、图片上传、正文填写
"""

import asyncio
from playwright.async_api import async_playwright
import os
import time

# 配置
CDP_URL = "http://127.0.0.1:18800"
IMAGE_DIRS = [
    "/Users/tianjinzhan/Desktop/图片资料/小镇夜景",
    "/Users/tianjinzhan/Desktop/图片资料/实拍街区图",
    "/Users/tianjinzhan/Desktop/图片资料/活动图",
]

def get_today_images():
    """获取今日图片"""
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
    print("🚀 百家号 V3 发布")
    print("=" * 50)
    
    # 获取图片
    images = get_today_images()
    print(f"📷 找到 {len(images)} 张图片")
    
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

适合闺蜜打卡、情侣约会、家庭出游！

#郑州周边游 #电影小镇 #郑州旅游 #民国穿越 #一日游"""
    
    async with async_playwright() as p:
        # 连接浏览器
        print("🔗 连接CDP浏览器...")
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        
        # 找百家号页面
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
        
        # ===== 步骤1: 填写标题 =====
        print("📝 步骤1: 填写标题...")
        try:
            # 多种标题输入框选择器
            title_selectors = [
                'input[placeholder*="标题"]',
                'input[class*="Title"]',
                'input[class*="title"]',
                'input[type="text"]',
                '#title',
            ]
            
            title_input = None
            for sel in title_selectors:
                title_input = await page.query_selector(sel)
                if title_input:
                    break
            
            if title_input:
                await title_input.fill(title)
                print("✅ 标题已填写")
                await asyncio.sleep(1)
            else:
                print("⚠️ 未找到标题输入框")
        except Exception as e:
            print(f"❌ 标题填写失败: {e}")
        
        # ===== 步骤2: 点击蓝色按钮插入标题/内容 =====
        print("🟢 步骤2: 点击蓝色按钮...")
        try:
            # 找蓝色按钮（可能包含"素材库"、"草稿箱"等）
            blue_buttons = await page.query_selector_all('button')
            
            clicked = False
            for btn in blue_buttons:
                try:
                    style = await btn.get_attribute('style')
                    text = await btn.inner_text()
                    # 尝试点击看起来像蓝色或素材库的按钮
                    if 'background' in str(style).lower() or '素材' in text or '草稿' in text:
                        await btn.click()
                        print(f"✅ 点击按钮: {text[:20]}")
                        await asyncio.sleep(2)
                        clicked = True
                        break
                except:
                    pass
            
            if not clicked:
                print("⚠️ 未点击蓝色按钮")
        except Exception as e:
            print(f"❌ 点击按钮失败: {e}")
        
        # ===== 步骤3: 从草稿箱/素材库选择内容 =====
        print("📋 步骤3: 查找已有内容...")
        try:
            # 查找内容列表
            items = await page.query_selector_all('div[class*="item"], li[class*="item"]')
            if items:
                print(f"   找到 {len(items)} 个内容项")
                # 点击第一个
                if items[0]:
                    await items[0].click()
                    print("✅ 已选择内容")
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️ 选择内容: {e}")
        
        # ===== 步骤4: 上传图片 =====
        if images:
            print("🖼️ 步骤4: 上传图片...")
            try:
                # 查找图片上传按钮
                upload_btns = await page.query_selector_all('input[type="file"]')
                
                for i, up_btn in enumerate(upload_btns):
                    try:
                        await up_btn.set_input_files([images[i]])
                        print(f"✅ 第{i+1}张图片已选择")
                        await asyncio.sleep(1)
                    except:
                        pass
            except Exception as e:
                print(f"❌ 图片上传: {e}")
        
        # ===== 截图 =====
        try:
            await page.screenshot(path="/Users/tianjinzhan/Desktop/baidu_v3_preview.png", full_page=True)
            print("📸 预览图已保存: baidu_v3_preview.png")
        except:
            pass
        
        # ===== 步骤5: 点击发布 =====
        print("📤 步骤5: 点击发布按钮...")
        try:
            publish_selectors = [
                'button:has-text("发布")',
                'button:has-text("提交")',
                'button[class*="publish"]',
                'button[class*="submit"]',
            ]
            
            publish_btn = None
            for sel in publish_selectors:
                publish_btn = await page.query_selector(sel)
                if publish_btn:
                    break
            
            if publish_btn:
                await publish_btn.click()
                print("✅ 已点击发布按钮")
                await asyncio.sleep(3)
            else:
                print("⚠️ 未找到发布按钮，请手动点击")
        except Exception as e:
            print(f"❌ 发布失败: {e}")
        
        await browser.close()
        print("✨ 百家号 V3 发布流程完成")

if __name__ == "__main__":
    asyncio.run(publish_baidu())
