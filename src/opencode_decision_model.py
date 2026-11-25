import json
import os

import requests
from dotenv import load_dotenv

SYSTEMONE_URL = "https://opencode.ai/inference/systemone/v1/systemone"
API_KEY_ENV_VARS = "OPENCODE_API_KEY_DEFAULT"
DEFAULT_TIMEOUT = 30

DEFAULT_MODEL = "gemini-decision-1"

URGENCY_STATE = "My payments have failed for three days and I am losing sales. Please help now."
REFUND_STATE = "My order arrived late and the item is damaged. I want a refund."


def _api_key() -> str:
    api_key = os.getenv(API_KEY_ENV_VARS)
    if api_key:
        return api_key
    raise RuntimeError(
        "No API key set. Define one of the environment variables: " + ", ".join(API_KEY_ENV_VARS)
    )


def _call_systemone(model: str, state: str, questions: dict) -> None:
    response = requests.post(
        SYSTEMONE_URL,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
        json={"model": model, "state": state, "questions": questions},
        timeout=DEFAULT_TIMEOUT,
    )
    if not response.ok:
        raise RuntimeError(
            f"System One request failed with status {response.status_code}: {response.text}"
        )
    print(json.dumps(response.json(), indent=2))


def call_jev_urgency_noul(model: str = DEFAULT_MODEL):
    _call_systemone(
        model,
        URGENCY_STATE,
        {
            "is_urgent": {
                "type": "noul",
                "instructions": "Does this request require urgent attention?",
            }
        },
    )


def call_jev_refund_choice_score(model: str = DEFAULT_MODEL):
    _call_systemone(
        model,
        REFUND_STATE,
        {
            "department": {
                "type": "choice",
                "instructions": "Which team should handle this request?",
                "criteria": {
                    "returns": "Refunds, exchanges, or damaged items",
                    "shipping": "Delivery delays or lost packages",
                    "billing": "Charges, invoices, or payment problems",
                },
            },
            "frustration": {
                "type": "score",
                "instructions": "How frustrated is the customer?",
                "criteria": ["Calm", "Frustrated", "Very angry"],
            },
        },
    )


if __name__ == "__main__":
    load_dotenv()
    call_jev_urgency_noul()
    # call_jev_refund_choice_score()
