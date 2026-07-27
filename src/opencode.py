import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass
class EndpointConfig:
    chat_completion_url: str = "https://opencode.ai/zen/go/v1"
    message_url: str = "https://opencode.ai/zen/go/v1/messages"

def main():
    client = OpenAI(
        api_key=os.getenv("OPENCODE_API_KEY_DEFAULT"),
        base_url=EndpointConfig().chat_completion_url
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

if __name__ == "__main__":
    main()
