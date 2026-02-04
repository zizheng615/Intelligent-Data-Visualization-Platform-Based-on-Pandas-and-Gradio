import json
import os
from openai import OpenAI

def chat(message):
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-fae4a997d9e74ecbbbdc8dc113da30bd", # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-plus", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=message
    )
    # print(json.loads(completion.model_dump_json()))
    content = json.loads(completion.model_dump_json())['choices'][0]['message']['content']
    return content

if __name__ == '__main__':
    chat('介绍一下数据分析')