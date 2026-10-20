"""Minimal cost-efficient AI bot template.

Flow: Filter → Fetch → Process → Cache → Output

Cost target: < $0.02 per bot per week
"""

import litellm
from routellm import Router
from gptcache import cache
import os
from typing import Optional

# --- Setup ---
router = Router()
litellm.set_budget(
    model="gpt-4o-mini",
    daily_limit=float(os.getenv("LITELLM_DAILY_LIMIT", "0.10")),
    monthly_limit=float(os.getenv("LITELLM_MONTHLY_LIMIT", "3.00")),
)


def is_simple_query(message: str) -> bool:
    """Check if a query can be handled by a cheaper model."""
    return router.is_simple_query(message)


@cache
def handle_request(message: str, model: str = "auto") -> str:
    """Route the request to the appropriate model and return the response.

    Simple queries → gpt-3.5-turbo (cheap)
    Complex queries → gpt-4o (powerful)
    """
    if model == "auto":
        model = "gpt-3.5-turbo" if is_simple_query(message) else "gpt-4o"

    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": message}],
    )
    return response.choices[0].message.content


def get_new_message() -> Optional[str]:
    """Replace with your actual message source (Slack, email, etc.)."""
    # TODO: Connect to your message source
    return None


def send_to_user(response: str) -> None:
    """Replace with your actual output channel."""
    print(f"Bot: {response}")


# --- Main loop ---
if __name__ == "__main__":
    print("Bot started. Waiting for messages...")

    while True:
        msg = get_new_message()
        if msg:
            response = handle_request(msg)
            send_to_user(response)