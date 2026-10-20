# 📄 AI Automation Run Book

> *"Filter before reading → reuse before generating → check for changes → stop failed loops."*

A proven, modular framework for building AI systems that are **cheap**, **scalable**, and **reliable**. Inspired by a 17-year-old who ran 300 Grok bots for under $0.02 per bot per week.

---

## 🎯 The Core Problem

Most AI automation burns money on:
- Empty checks (API calls when nothing needs doing)
- Rereading entire chats (sending full history every time)
- Retry loops (infinite retries on failed calls)
- Overfetching (sending 10-page docs when 1 paragraph would do)

This repo shows how to fix all four.

---

## 🧱 Architecture

```
Trigger → Filter → Fetch → Process → Cache → Output
```

| Principle | Why |
|-----------|-----|
| Event-driven | Bots wake up only when there's work |
| Stateless | Each task is self-contained |
| Idempotent | Re-running doesn't cause side effects |
| Composable | Small, reusable components |

---

## 🛠️ Tool Stack

### Cost Control
| Tool | Purpose |
|------|---------|
| [LiteLLM](https://github.com/BerriAI/litellm) | Track spending, set budgets |
| [RouteLLM](https://github.com/rousseau-ai/routellm) | Route simple requests to cheaper models |
| [Portkey Gateway](https://portkey.ai) | Cache API responses across workflows |

### Input Optimization
| Tool | Purpose |
|------|---------|
| [Crawl4AI](https://github.com/All-Hands-AI/crawl4ai) | Web pages → clean Markdown |
| [Firecrawl](https://github.com/firecrawldev/firecrawl) | Extract structured data, not clutter |
| [Chonkie](https://github.com/ai-chong/chonkie) | Split long docs into chunks |
| [LLMLingua](https://github.com/microsoft/LLMLingua) | Compress inputs, preserve facts |

### Retrieval & Context
| Tool | Purpose |
|------|---------|
| [Semantic Router](https://github.com/semantic-router/semantic-router) | Match requests via local embeddings |
| [FlagEmbedding](https://github.com/FlagEmbedding/FlagEmbedding) | Rerank retrieved passages |
| [Mem0](https://github.com/mem0ai/mem0) | Store/retrieve facts across runs |
| [Graphiti](https://github.com/mem0ai/graphiti) | Searchable fact graph |

### Output & Caching
| Tool | Purpose |
|------|---------|
| [GPTCache](https://github.com/ant-agi/GPTCache) | Reuse answers to similar requests |
| [requests-cache](https://github.com/requests-cache/requests-cache) | Cache HTTP responses with expiry |
| [Hishel](https://github.com/kimberleyjqs/hishel) | HTTP caching for fetching tools |

### Workflow Management
| Tool | Purpose |
|------|---------|
| [Prefect](https://github.com/PrefectHQ/prefect) | Cache task results, avoid reruns |
| [Celery](https://github.com/celery/celery) | Background job queue |
| [APScheduler](https://github.com/agronholm/apscheduler) | Schedule lightweight checks |
| [PyBreaker](https://github.com/danielfm/pybreaker) | Pause calls to failing services |

---

## 🚀 Quick Start

```bash
git clone https://github.com/mnemnon-ai/ai-automation-runbook
cd ai-automation-runbook
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python templates/minimal_bot.py
```

---

## 📂 Structure

```
ai-automation-runbook/
├── README.md              # This file
├── requirements.txt       # All dependencies
├── .env.example           # Required env vars
├── templates/
│   ├── minimal_bot.py     # Single bot: filter → fetch → process → cache → output
│   └── multi_bot.py       # 300+ bot orchestrator with budget tracking
├── tools/
│   ├── litellm_setup.py   # Budget tracking per API call
│   ├── routellm_setup.py  # Model routing (cheap vs. powerful)
│   └── cache_setup.py     # Response caching with freshness rules
└── examples/
    ├── customer_support.py
    └── data_processor.py
```

---

## 🧪 Metrics to Track

| Metric | Target |
|--------|--------|
| Cost per bot/week | < $0.02 |
| Avg response time | < 5s |
| Success rate | > 95% |
| API calls per task | < 3 |
| Memory per bot | < 100MB |

---

## 🧠 Pro Tips

1. **Start small** — one bot before scaling
2. **Use local embeddings** for routing, not LLMs
3. **Cache everything** — even simple responses
4. **Monitor usage daily** — adjust budgets as needed
5. **Log errors** — catch infinite loops early

---

## 📜 License

MIT — use it, share it, improve it.