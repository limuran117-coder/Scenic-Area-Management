#!/usr/bin/env python3
"""
智能图片选择器 - 根据文案主题匹配图片文件夹
"""
import os
import json
import re

USED_IMAGES_FILE = "/Users/tianjinzhan/.openclaw/workspace/data/used_images.json"

# 文案主题 -> 图片文件夹 映射
THEME_FOLDERS = {
    "夜景": "/Users/tianjinzhan/Desktop/图片资料/小镇夜景",
    "灯光": "/Users/tianjinzhan/Desktop/图片资料/小镇夜景",
    "晚上": "/Users/tianjinzhan/Desktop/图片资料/小镇夜景",
    "穿越": "/Users/tianjinzhan/Desktop/图片资料/穿越德化街",
    "德化街": "/Users/tianjinzhan/Desktop/图片资料/穿越德化街",
    "民国": "/Users/tianjinzhan/Desktop/图片资料/实拍街区图",
    "街区": "/Users/tianjinzhan/Desktop/图片资料/实拍街区图",
    "街道": "/Users/tianjinzhan/Desktop/图片资料/实拍街区图",
    "国风": "/Users/tianjinzhan/Desktop/图片资料/建业电影小镇-国风达人物料-雅合风华",
    "汉服": "/Users/tianjinzhan/Desktop/图片资料/建业电影小镇-国风达人物料-雅合风华",
    "古装": "/Users/tianjinzhan/Desktop/图片资料/建业电影小镇-国风达人物料-雅合风华",
    "秋天": "/Users/tianjinzhan/Desktop/图片资料/秋天图",
    "秋季": "/Users/tianjinzhan/Desktop/图片资料/秋天图",
    "儿童": "/Users/tianjinzhan/Desktop/图片资料/儿童素材挑选",
    "亲子": "/Users/tianjinzhan/Desktop/图片资料/儿童素材挑选",
    "暑期": "/Users/tianjinzhan/Desktop/图片资料/2023暑期",
    "夏天": "/Users/tianjinzhan/Desktop/图片资料/2023暑期",
    "客栈": "/Users/tianjinzhan/Desktop/图片资料/客栈",
}

# 默认图片文件夹
DEFAULT_FOLDERS = [
    "/Users/tianjinzhan/Desktop/图片资料/实拍街区图",
    "/Users/tianjinzhan/Desktop/图片资料/小镇夜景",
    "/Users/tianjinzhan/Desktop/图片资料/常用图",
    "/Users/tianjinzhan/Desktop/图片资料/穿越德化街",
]

def load_used_images():
    if os.path.exists(USED_IMAGES_FILE):
        with open(USED_IMAGES_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_used_images(used_set):
    os.makedirs(os.path.dirname(USED_IMAGES_FILE), exist_ok=True)
    with open(USED_IMAGES_FILE, 'w') as f:
        json.dump(list(used_set), f)

def match_folder_by_theme(content):
    """根据文案内容匹配最合适的图片文件夹"""
    content = content.lower()
    
    for keyword, folder in THEME_FOLDERS.items():
        if keyword in content:
            if os.path.exists(folder):
                return folder
    
    return None

def get_images_for_content(content, max_count=3):
    """
    根据文案内容智能选择图片
    1. 先匹配主题文件夹
    2. 排除已使用图片
    3. 跳过太大文件
    """
    used = load_used_images()
    
    # 1. 尝试匹配主题文件夹
    matched_folder = match_folder_by_theme(content)
    if matched_folder:
        folders = [matched_folder] + DEFAULT_FOLDERS
    else:
        folders = DEFAULT_FOLDERS
    
    # 2. 收集可用图片
    available = []
    for folder in folders:
        if not os.path.exists(folder):
            continue
        for f in sorted(os.listdir(folder)):
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                img_path = os.path.join(folder, f)
                # 跳过太大文件
                if os.path.getsize(img_path) > 10 * 1024 * 1024:
                    continue
                # 跳过已使用
                if img_path in used:
                    continue
                available.append(img_path)
                if len(available) >= max_count:
                    break
        if len(available) >= max_count:
            break
    
    return available

def mark_images_used(image_paths):
    """标记图片为已使用"""
    used = load_used_images()
    used.update(image_paths)
    save_used_images(used)

if __name__ == "__main__":
    # 测试
    test_contents = [
        "郑州周边一日游推荐：建业电影小镇穿越民国体验",
        "小镇夜景灯光秀太美了",
        "秋天去电影小镇拍照打卡",
    ]
    
    for content in test_contents:
        imgs = get_images_for_content(content, 3)
        folder = match_folder_by_theme(content)
        print(f"\n文案: {content}")
        print(f"匹配文件夹: {folder}")
        print(f"可用图片: {imgs[:2]}...")
