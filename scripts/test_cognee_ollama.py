#!/usr/bin/env python3
"""测试Cognee - 用本地Ollama"""
import asyncio
import os

os.environ["LLM_PROVIDER"] = "openai"
os.environ["LLM_MODEL"] = "qwen2.5:14b"  # 更小的模型
os.environ["LLM_API_KEY"] = "test"
os.environ["OPENAI_API_KEY"] = "test"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"

import cognee

async def test():
    print("1. 添加数据...")
    await cognee.add("电影小镇门票120元")
    print("2. 构建图谱...")
    await cognee.cognify()
    print("3. 查询...")
    results = await cognee.search("门票?")
    for r in results:
        print(f"- {r}")
    print("✅ 成功!")

if __name__ == "__main__":
    asyncio.run(test())
