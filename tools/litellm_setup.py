"""LiteLLM budget tracking setup.

Tracks spending per API call, per model, and per bot.
Prevents runaway workflows from eating the whole budget.
"""

import litellm
import os
from typing import Dict


def setup_budget_tracking(
    daily_limit: float = 0.10,
    monthly_limit: float = 3.00,
) -> None:
    """Configure LiteLLM budget tracking."""
    litellm.set_budget(
        model="gpt-4o-mini",
        daily_limit=daily_limit,
        monthly_limit=monthly_limit,
    )


def get_current_spend() -> Dict[str, float]:
    """Return current daily and monthly spend."""
    return {
        "daily": litellm.get_current_spend("daily"),
        "monthly": litellm.get_current_spend("monthly"),
    }


def check_budget_available(model: str, estimated_cost: float) -> bool:
    """Check if there's enough budget for the operation."""
    current = get_current_spend()
    daily_limit = float(os.getenv("LITELLM_DAILY_LIMIT", "0.10"))
    monthly_limit = float(os.getenv("LITELLM_MONTHLY_LIMIT", "3.00"))

    return (
        current["daily"] + estimated_cost <= daily_limit
        and current["monthly"] + estimated_cost <= monthly_limit
    )


# --- Example usage ---
if __name__ == "__main__":
    setup_budget_tracking()
    print("Budget tracking configured.")
    print(f"Current spend: {get_current_spend()}")