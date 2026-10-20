"""RouteLLM model routing setup.

Routes simple queries to cheaper models (gpt-3.5-turbo) and
complex queries to more powerful models (gpt-4o).

This is the single biggest cost saver — most queries don't need GPT-4.
"""

from routellm import Router
from typing import Tuple


def create_router() -> Router:
    """Create a configured RouteLLM router."""
    router = Router()
    return router


def classify_query(message: str) -> Tuple[str, str]:
    """Classify a query and return (model, reason).

    Returns:
        (model_name, explanation)
    """
    router = create_router()

    if router.is_simple_query(message):
        return "gpt-3.5-turbo", "Simple query — cheaper model sufficient"
    else:
        return "gpt-4o", "Complex query — needs more capable model"


# --- Example usage ---
if __name__ == "__main__":
    test_queries = [
        "What's the weather today?",
        "Analyze the implications of the new trade agreement on emerging markets",
        "Summarize this paragraph",
        "Debug this Python code and explain the error",
    ]

    for q in test_queries:
        model, reason = classify_query(q)
        print(f"Query: {q[:50]}...")
        print(f"  → {model} ({reason})")
        print()