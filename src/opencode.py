import os
from dataclasses import dataclass

from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI

HEALTH_CHECK_PROMPT = "Hello, this is a health check. Are you working?"
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_TOKENS = 1024
API_KEY_ENV_VAR = "OPENCODE_API_KEY_DEFAULT"


@dataclass(frozen=True)
class EndpointConfig:
    openai_url_go: str = "https://opencode.ai/zen/go/v1"
    openai_url_zen: str = "https://opencode.ai/zen/v1"
    anthropic_url_go: str = "https://opencode.ai/zen/go"
    anthropic_url_zen: str = "https://opencode.ai/zen"


ENDPOINTS = EndpointConfig()


def _health_check_message() -> dict[str, str]:
    return {"role": "user", "content": HEALTH_CHECK_PROMPT}


def _openai_client(base_url: str) -> OpenAI:
    return OpenAI(api_key=os.getenv(API_KEY_ENV_VAR), base_url=base_url, timeout=DEFAULT_TIMEOUT)


def _anthropic_client(base_url: str) -> Anthropic:
    return Anthropic(api_key=os.getenv(API_KEY_ENV_VAR), base_url=base_url, timeout=DEFAULT_TIMEOUT)


def _call_openai_chat_completion_endpoint(base_url: str, model: str):
    client = _openai_client(base_url)
    completion = client.chat.completions.create(
        model=model,
        messages=[_health_check_message()],
    )

    print(completion.choices[0].message.content)


def _call_openai_response_endpoint(base_url: str, model: str):
    client = _openai_client(base_url)
    response = client.responses.create(
        model=model,
        input=[_health_check_message()],
    )

    print(response.output_text)


def _call_anthropic_endpoint(base_url: str, model: str):
    client = _anthropic_client(base_url)
    message = client.messages.create(
        max_tokens=DEFAULT_MAX_TOKENS,
        messages=[_health_check_message()],
        model=model,
    )

    print(message.content)


def call_openai_chat_endpoint_go_mode(model: str = "deepseek-v4-flash"):
    _call_openai_chat_completion_endpoint(ENDPOINTS.openai_url_go, model)


def call_anthropic_compatible_endpoint_go_mode(model: str = "minimax-m2.7"):
    _call_anthropic_endpoint(ENDPOINTS.anthropic_url_go, model)


def call_openai_chat_endpoint_zen_mode(model: str = "big-pickle"):
    _call_openai_chat_completion_endpoint(ENDPOINTS.openai_url_zen, model)


def call_openai_resp_endpoint_zen_mode(model: str = "gpt-5-nano"):
    _call_openai_response_endpoint(ENDPOINTS.openai_url_zen, model)


def call_anthropic_compatible_endpoint_zen_mode(model: str = "qwen3.6-plus"):
    _call_anthropic_endpoint(ENDPOINTS.anthropic_url_zen, model)


if __name__ == "__main__":
    load_dotenv()
    # call_openai_chat_endpoint_go_mode()
    # call_anthropic_compatible_endpoint_go_mode()
    # call_anthropic_compatible_endpoint_zen_mode(model="claude-opus-5")
    # call_openai_chat_endpoint_zen_mode()
    call_openai_resp_endpoint_zen_mode()
