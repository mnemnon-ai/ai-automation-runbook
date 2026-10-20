"""Multi-bot orchestrator for 300+ bots.

Each bot has its own budget, routing rules, and caching strategy.
Total cost target: < $6.00/week for 300 bots (~$0.02/bot/week).
"""

import litellm
from routellm import Router
from gptcache import cache
import os
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from threading import Lock


@dataclass
class BotConfig:
    name: str
    daily_budget: float
    model_default: str = "gpt-4o-mini"
    model_complex: str = "gpt-4o"
    cache_ttl: int = 3600  # 1 hour


class BotSwarm:
    """Manages 300+ bots with individual budgets and shared infrastructure."""

    def __init__(self, configs: List[BotConfig]):
        self.bots: Dict[str, BotConfig] = {c.name: c for c in configs}
        self.router = Router()
        self._lock = Lock()
        self._spending: Dict[str, float] = {c.name: 0.0 for c in configs}
        self._message_queue: List[str] = []

    def add_message(self, bot_name: str, message: str) -> None:
        """Add a message to a bot's queue."""
        with self._lock:
            self._message_queue.append((bot_name, message))

    def _check_budget(self, bot_name: str, estimated_cost: float) -> bool:
        """Return True if the bot can afford the operation."""
        config = self.bots[bot_name]
        current = self._spending[bot_name]
        return (current + estimated_cost) <= config.daily_budget

    def _record_spend(self, bot_name: str, amount: float) -> None:
        with self._lock:
            self._spending[bot_name] += amount

    def process_message(self, bot_name: str, message: str) -> Optional[str]:
        """Process a single message for a bot.

        Steps:
        1. Check budget
        2. Route to appropriate model
        3. Generate response
        4. Cache result
        5. Return output
        """
        config = self.bots[bot_name]

        # 1. Budget check
        estimated_cost = 0.001  # rough estimate
        if not self._check_budget(bot_name, estimated_cost):
            return None  # Skip — out of budget

        # 2. Route
        is_simple = self.router.is_simple_query(message)
        model = config.model_default if is_simple else config.model_complex

        # 3. Generate
        try:
            response = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": message}],
            )
            result = response.choices[0].message.content

            # 4. Cache
            cache.set(
                key=f"{bot_name}:{message}",
                value=result,
                ttl=config.cache_ttl,
            )

            # 5. Record spend
            actual_cost = response._hidden_params.get("cost", estimated_cost)
            self._record_spend(bot_name, actual_cost)

            return result
        except Exception as e:
            print(f"Error in bot {bot_name}: {e}")
            return None

    def run(self) -> None:
        """Main event loop — processes messages as they arrive."""
        while True:
            with self._lock:
                if not self._message_queue:
                    time.sleep(0.1)  # Avoid busy-waiting
                    continue
                bot_name, message = self._message_queue.pop(0)

            result = self.process_message(bot_name, message)
            if result:
                print(f"[{bot_name}] {result}")


# --- Example: Create 300 bots ---
def create_swarm(n: int = 300) -> BotSwarm:
    """Create a swarm of N bots with individual budgets."""
    configs = [
        BotConfig(
            name=f"bot-{i:03d}",
            daily_budget=0.01,  # ~$0.07/week per bot
        )
        for i in range(n)
    ]
    return BotSwarm(configs)


if __name__ == "__main__":
    swarm = create_swarm(300)
    print(f"Swarm initialized with {len(swarm.bots)} bots")

    # Example: Add a message
    swarm.add_message("bot-001", "Hello, what's the weather?")
    swarm.run()