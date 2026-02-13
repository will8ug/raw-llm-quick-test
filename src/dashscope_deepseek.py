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

call_deepseek_v3_2()
