"""Response caching setup.

Caches AI responses so similar requests don't hit the API again.
Reduces cost and latency for repeated queries.
"""

from gptcache import cache
from gptcache.manager import CacheBase
import os
from typing import Optional


def setup_cache(
    ttl: int = 3600,  # 1 hour
    max_size: int = 1000,
) -> None:
    """Configure GPTCache with TTL and size limits."""
    cache.init(
        cache_base=CacheBase(
            ttl=ttl,
            max_size=max_size,
        ),
    )


def get_cached_response(query: str) -> Optional[str]:
    """Check if a response is already cached."""
    return cache.get(key=query)


def cache_response(query: str, response: str, ttl: Optional[int] = None) -> None:
    """Cache a response with optional custom TTL."""
    cache.set(
        key=query,
        value=response,
        ttl=ttl or int(os.getenv("GPT_CACHE_TTL", "3600")),
    )


# --- Example usage ---
if __name__ == "__main__":
    setup_cache()

    # First request — hits the API
    query = "What is the capital of France?"
    cached = get_cached_response(query)
    if cached:
        print(f"Cached: {cached}")
    else:
        # Simulate API call
        response = "The capital of France is Paris."
        cache_response(query, response)
        print(f"Generated and cached: {response}")

    # Second request — served from cache
    cached = get_cached_response(query)
    if cached:
        print(f"Served from cache: {cached}")