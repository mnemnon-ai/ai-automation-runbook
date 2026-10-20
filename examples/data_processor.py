"""Example: Data Processor Bot

Flow:
1. Trigger: New file in S3
2. Filter: Is this a data file?
3. Fetch: Download file (requests-cache)
4. Process: Extract fields (Firecrawl + Chonkie)
5. Generate: Summary (LiteLLM)
6. Cache: Store result
7. Output: Write to database

Cost target: ~$0.01/bot/week
"""

import litellm
from routellm import Router
from gptcache import cache
import requests
from typing import Optional


class DataProcessor:
    def __init__(self):
        self.router = Router()

    def is_data_file(self, filename: str) -> bool:
        """Check if the file is a data file we should process."""
        return filename.endswith((".csv", ".json", ".xml"))

    def download_file(self, url: str) -> str:
        """Download a file with caching."""
        # requests-cache handles this automatically
        response = requests.get(url)
        return response.text

    def extract_fields(self, content: str) -> str:
        """Extract relevant fields from the content."""
        # Use Firecrawl or Crawl4AI for web content
        # Use Chonkie for long documents
        return content[:1000]  # Simplified

    def generate_summary(self, data: str) -> str:
        """Generate a summary of the data."""
        prompt = f"Summarize this data:\n{data}"
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def process_file(self, url: str) -> Optional[str]:
        """Main handler — filters, fetches, processes, caches, outputs."""
        # 1. Filter
        if not self.is_data_file(url):
            return None

        # 2. Fetch
        content = self.download_file(url)

        # 3. Process
        extracted = self.extract_fields(content)

        # 4. Generate
        summary = self.generate_summary(extracted)

        # 5. Cache
        cache.set(
            key=url,
            value=summary,
            ttl=7200,  # 2 hours
        )

        return summary


if __name__ == "__main__":
    processor = DataProcessor()
    result = processor.process_file("https://example.com/data.csv")
    if result:
        print(f"Summary: {result}")