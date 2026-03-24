#!/usr/bin/env python3
"""测试Cognee基本功能"""
import asyncio
import os

# 设置环境变量
os.environ["LLM_API_KEY"] = "sk-dummy"  # 测试用

import cognee

async def test_cognee():
    print("1. 添加测试数据...")
    await cognee.add("建业电影小镇是郑州的一个民国风情主题景区")
    await cognee.add("电影小镇门票价格约为80元/人")
    await cognee.add("小镇每天晚上有夜场表演")
    
    print("2. 构建知识图谱...")
    await cognee.cognify()
    
    print("3. 查询测试...")
    results = await cognee.search("电影小镇门票多少钱?")
    
    print("\n查询结果:")
    for r in results:
        print(f"- {r}")
    
    print("\n✅ Cognee测试成功!")

if __name__ == "__main__":
    asyncio.run(test_cognee())
