#!/usr/bin/env python3
"""
抖音指数日报 - 7天vs30天对比
获取抖音热榜数据并生成简单的趋势报告
"""

import subprocess
import json
import os
from datetime import datetime, timedelta

def get_douyin_hot_list(limit=30):
    """获取抖音热榜数据"""
    script_path = os.path.expanduser("~/.openclaw/skills/douyin-hot-trend/scripts/douyin.js")
    try:
        result = subprocess.run(
            ["node", script_path, "hot", str(limit)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"获取失败: {str(e)}"

def parse_hot_list(output):
    """解析热榜数据"""
    lines = output.strip().split('\n')
    items = []
    current_item = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
            if current_item:
                items.append(current_item)
            current_item = {'title': line[3:].strip()}
        elif '热度:' in line:
            try:
                heat = line.split('热度:')[1].strip().replace(',', '')
                current_item['heat'] = int(heat)
            except:
                pass
    
    if current_item:
        items.append(current_item)
    
    return items

def generate_report():
    """生成日报"""
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📊 抖音指数日报 ({today})")
    print("=" * 60)
    print(f"📅 报告周期: 7天 vs 30天")
    print(f"⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 获取当前热榜
    print("🔥 正在获取抖音热榜数据...")
    output = get_douyin_hot_list(30)
    items = parse_hot_list(output)
    
    if not items:
        print("❌ 未能获取数据")
        return
    
    # 计算总热度
    total_heat = sum(item.get('heat', 0) for item in items)
    avg_heat = total_heat // len(items) if items else 0
    
    print(f"📈 数据概览")
    print("-" * 40)
    print(f"  • 热榜条目数: {len(items)}")
    print(f"  • 总热度值: {total_heat:,}")
    print(f"  • 平均热度: {avg_heat:,}")
    print()
    
    # 7天 vs 30天 对比（模拟数据，因为没有历史存储）
    print(f"📊 7天 vs 30天 对比分析")
    print("-" * 40)
    print(f"  • 当前热度(30条): {total_heat:,}")
    print(f"  • 注: 历史对比需要数据存储支持")
    print(f"  • 建议: 每日记录数据以实现趋势对比")
    print()
    
    # TOP 10
    print(f"🏆 热榜 TOP 10")
    print("-" * 40)
    for i, item in enumerate(items[:10], 1):
        title = item.get('title', 'N/A')[:30]
        heat = item.get('heat', 0)
        print(f"  {i:2d}. {title}")
        print(f"      🔥 {heat:,}")
    print()
    
    # 标签分析
    print(f"📌 热点话题分析")
    print("-" * 40)
    # 简单统计话题类型
    categories = {
        '春日/季节': 0,
        '美食': 0,
        '科技/AI': 0,
        '社会/时事': 0,
        '体育': 0,
        '其他': 0
    }
    
    for item in items:
        title = item.get('title', '').lower()
        if any(k in title for k in ['春', '春日', '春季', '花', '旅游']):
            categories['春日/季节'] += 1
        elif any(k in title for k in ['味', '水果', '凤梨', '芒果', '美食', '多巴胺']):
            categories['美食'] += 1
        elif any(k in title for k in ['ai', '科技', 'ipo', '未来']):
            categories['科技/AI'] += 1
        elif any(k in title for k in ['国家', '日本', '朝鲜', '校园', '退役']):
            categories['社会/时事'] += 1
        elif any(k in title for k in ['退役', '球', '雨航']):
            categories['体育'] += 1
        else:
            categories['其他'] += 1
    
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        if count > 0:
            bar = '█' * count
            print(f"  {cat:12s}: {bar} ({count})")
    print()
    
    print("=" * 60)
    print("📝 备注: 本报告基于抖音公开热榜数据")
    print("   如需7天vs30天历史对比，需建立数据存储机制")

if __name__ == "__main__":
    generate_report()
