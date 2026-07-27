import os
from dataclasses import dataclass

from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass
class EndpointConfig:
    openai_url: str = "https://opencode.ai/zen/go/v1"
    anthropic_url: str = "https://opencode.ai/zen/go"

def call_openai_compatible_endpoint():
    client = OpenAI(
        api_key=os.getenv("OPENCODE_API_KEY_DEFAULT"),
        base_url=EndpointConfig().openai_url
    )
    completion = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "user",
                "content": "Hello, this is a health check. Are you working?"
            },
        ]
    )

    print(completion.choices[0].message.content)

def call_anthropic_compatible_endpoint():
    client = Anthropic(
        api_key=os.getenv("OPENCODE_API_KEY_DEFAULT"),
        base_url=EndpointConfig().anthropic_url
    )
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, this is a health check. Are you working?"
            },
        ],
        model="minimax-m2.7"
    )

    print(message.content)

if __name__ == "__main__":
    # call_openai_compatible_endpoint()
    call_anthropic_compatible_endpoint()
