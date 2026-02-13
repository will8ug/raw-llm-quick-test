import os
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

def call_deepseek_v3_2():
    response = Generation.call(
        model='deepseek-v3.2',
        prompt='你好，请介绍一下你自己',
        max_tokens=1024,
        top_p=0.8,
        stream=False,
        stop=['\n\n']
    )
    
    if response.status_code == 200:
        print(response.output.choices[0].message.content)
    else:
        print(f'Error: {response.code} - {response.message}')

def stream_deepseek_v3_2():
    responses = Generation.call(
        model='deepseek-v3.2',
        prompt='写一个关于人工智能的短故事，字数控制在500字内。',
        stream=True,
        incremental_output=True
    )
    
    for chunk in responses:
        if chunk.status_code == 200:
            print(chunk.output.choices[0].message.content, end='', flush=True)
        else:
            print(f'Error: {chunk.code}')

call_deepseek_v3_2()

stream_deepseek_v3_2()
