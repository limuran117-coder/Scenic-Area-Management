#!/bin/bash
# 郑州天气播报 - 定时任务脚本
# 每天 8:00、12:00、16:00 在"站长办公室"群@毕超发送天气

# 获取郑州天气
WEATHER=$(curl -s "https://wttr.in/郑州?format=j1" | python3 -c '
import json, sys
data = json.load(sys.stdin)
current = data["data"]["current_condition"][0]
today = data["data"]["weather"][0]
weather_desc = current["weatherDesc"][0]["value"]
print("🌤️ 郑州今日天气")
print("⛅ " + weather_desc)
print("🌡️ 温度: " + today["mintempC"] + "°C ~ " + today["maxtempC"] + "°C")
print("💨 风速: " + current["windspeedKmph"] + "km/h")
print("💧 湿度: " + current["humidity"] + "%")
')

# 发送到群并@毕超
openclaw message send \
  --channel feishu \
  --target "oc_f109bcfd1bc7e166fd0ae077f70247cf" \
  --message "@毕超 $WEATHER"
