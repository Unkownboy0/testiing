# Geetorus — AI Model Support & Provider Gateway

## 1. Supported AI Providers & Models

Geetorus decouples model inference through modular adapters in `packages/adapters/`. Agents can be individually configured with specialized foundation models based on reasoning requirements, latency, and cost.

| Provider | Supported Models | Primary Use Cases | Streaming / Tool Calling Support |
| :--- | :--- | :--- | :--- |
| **Anthropic** | `claude-3-7-sonnet-20250219`<br>`claude-3-5-sonnet-20241022`<br>`claude-3-5-haiku-20241022` | Complex code refactoring, lead architectural planning, complex multi-file debugging. | Full native tool calling & token streaming |
| **OpenAI** | `gpt-4o`<br>`gpt-4o-mini`<br>`o1`<br>`o3-mini` | Fast task triage, unit test generation, documentation writing. | Native tool calling & token streaming |
| **OpenRouter** | 200+ open and proprietary models (`deepseek/deepseek-r1`, `meta-llama/llama-3.3-70b-instruct`) | Cost-effective fallback execution and specialized reasoning benchmarks. | Tool calling & streaming via unified API |
| **MiniMax** | `minimax-01` | High-throughput multilingual and creative content generation. | Supported via OpenAI-compatible adapter |
| **Ollama / Local** | `llama3.2:latest`, `qwen2.5-coder:32b` | Completely offline, zero-data-leak local execution in air-gapped environments. | Local HTTP adapter |

---

## 2. Model Selection & Fallback Cascades

Geetorus allows configuring fallback chains in `ai_provider_defaults.ts`. If an upstream model experiences an outage or rate limit (HTTP 429), the orchestrator automatically cascades to the configured fallback model while recording the provider event in `provider_trace_records.ts`.
