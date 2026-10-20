"""Example: AI Customer Support Bot

Flow:
1. Trigger: New message in Slack
2. Filter: Is this a support request?
3. Fetch: User history (Mem0)
4. Process: Summarize issue (LiteLLM + GPTCache)
5. Generate response
6. Cache result
7. Send to user

Cost target: ~$0.015/bot/week
"""

import litellm
from routellm import Router
from gptcache import cache
from typing import Optional


class SupportBot:
    def __init__(self):
        self.router = Router()

    def is_support_request(self, message: str) -> bool:
        """Use Semantic Router to classify the message."""
        return self.router.is_simple_query(message)

    def get_user_history(self, user_id: str) -> str:
        """Fetch relevant user history from Mem0."""
        # TODO: Connect to Mem0
        return f"History for user {user_id}"

    def summarize_issue(self, message: str, history: str) -> str:
        """Summarize the issue using LiteLLM."""
        prompt = f"Summarize this support issue:\nMessage: {message}\nHistory: {history}"
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def generate_response(self, summary: str) -> str:
        """Generate a helpful response."""
        prompt = f"Generate a helpful response to this support issue:\n{summary}"
        response = litellm.completion(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def handle_message(self, user_id: str, message: str) -> Optional[str]:
        """Main handler — filters, fetches, processes, caches, outputs."""
        # 1. Filter
        if not self.is_support_request(message):
            return None

        # 2. Fetch
        history = self.get_user_history(user_id)

        # 3. Process
        summary = self.summarize_issue(message, history)

        # 4. Generate
        response = self.generate_response(summary)

        # 5. Cache
        cache.set(
            key=f"{user_id}:{message}",
            value=response,
            ttl=3600,
        )

        return response


if __name__ == "__main__":
    bot = SupportBot()
    result = bot.handle_message("user-123", "I can't log into my account")
    if result:
        print(f"Response: {result}")