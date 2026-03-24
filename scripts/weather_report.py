#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
郑州天气日报 - 表格形式
"""

import urllib.request
import json
import sys
from datetime import datetime

def get_weather():
    url = "https://wttr.in/%E9%84%AD%E5%B7%9E?format=j1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def generate_weather_report():
    data = get_weather()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if not data:
        return "❌ 天气数据获取失败"
    
    current = data["current_condition"][0]
    
    # 解析数据 - 直接是字符串，不是数组
    weather_desc = current["weatherDesc"][0]["value"] if isinstance(current["weatherDesc"], list) else current["weatherDesc"]
    temp_c = current["temp_C"]
    feels_like = current["FeelsLikeC"]
    humidity = current["humidity"]
    wind = current["windspeedKmph"]
    
    # 尝试获取今日预报
    try:
        weather = data.get("weather", [{}])[0]
        mintemp = weather.get("mintempC", "N/A") if isinstance(weather.get("mintempC"), str) else weather.get("mintempC", [{}])[0].get("value", "N/A")
        maxtemp = weather.get("maxtempC", "N/A") if isinstance(weather.get("maxtempC"), str) else weather.get("maxtempC", [{}])[0].get("value", "N/A")
    except:
        mintemp = maxtemp = "N/A"
    
    # 生成表格报告
    report = f"""# 🌤️ 郑州天气日报 ({today})

---

## 今日天气

| 指标 | 数值 |
|------|------|
| 天气 | {weather_desc} |
| 温度 | {temp_c}°C ({mintemp}~{maxtemp}°C) |
| 体感 | {feels_like}°C |
| 湿度 | {humidity}% |
| 风速 | {wind} km/h |

---

## 出行建议

| 时段 | 建议 |
|------|------|
| 白天 | {"适合外出，建议春装" if int(temp_c) >= 15 else "注意保暖"} |
| 夜晚 | {"温差较大，建议带外套" if int(mintemp) < 10 else "舒适"} |
| 出行 | {"适合户外活动" if "晴" in weather_desc or "多云" in weather_desc else "建议带伞"} |

---

*数据来源：wttr.in | 更新时间：{datetime.now().strftime('%H:%M')}*
"""
    return report

if __name__ == "__main__":
    print(generate_weather_report())
