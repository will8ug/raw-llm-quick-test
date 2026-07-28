import os
from dataclasses import dataclass

from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI

@dataclass(frozen=True)
class EndpointConfig:
    openai_url_go: str = "https://opencode.ai/zen/go/v1"
    openai_url_zen: str = "https://opencode.ai/zen/v1"
    anthropic_url_go: str = "https://opencode.ai/zen/go"
    anthropic_url_zen: str = "https://opencode.ai/zen"

ENDPOINTS = EndpointConfig()

def call_openai_compatible_endpoint():
    client = OpenAI(
        api_key=os.getenv("OPENCODE_API_KEY_DEFAULT"),
        base_url=ENDPOINTS.openai_url_go
    )
    completion = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "user",
                "content": "Hello, this is a health check. Are you working?"
            },
        ],
        timeout=30
    )

    print(completion.choices[0].message.content)

def call_anthropic_compatible_endpoint():
    client = Anthropic(
        api_key=os.getenv("OPENCODE_API_KEY_DEFAULT"),
        base_url=ENDPOINTS.anthropic_url_go
    )
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, this is a health check. Are you working?"
            },
        ],
        model="minimax-m2.7",
        timeout=30
    )

    print(message.content)

def call_anthropic_compatible_endpoint_zen_mode():
    client = Anthropic(
        api_key=os.getenv("OPENCODE_API_KEY_DEFAULT"),
        base_url=ENDPOINTS.anthropic_url_zen
    )
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, this is a health check. Are you working?"
            },
        ],
        model="qwen3.6-plus",
        timeout=30
    )

    print(message.content)

if __name__ == "__main__":
    load_dotenv()
    # call_openai_compatible_endpoint()
    # call_anthropic_compatible_endpoint()
    call_anthropic_compatible_endpoint_zen_mode()
