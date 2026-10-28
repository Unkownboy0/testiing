# 08 — AI, LLM Integration, and Model Routing

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Codebase audit of `packages/adapters/*`, `server/src/services/ai-connections.ts`, and `ai-connection-runtime.ts`.

---

## 1. Supported Model Providers & Adapters

Geetorus provides a normalized AI provider adapter layer located in `geetorusai/packages/adapters/`. This decouples the agent orchestration engine from vendor-specific LLM APIs.

| Provider / Target | Adapter Package | Supported Models | Execution Type | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **Anthropic** | `packages/adapters/claude-local` | `claude-3-5-sonnet-20241022`, `claude-3-5-haiku`, `claude-3-opus` | Hosted Cloud (HTTPS API) | **Verified** |
| **OpenAI** | `packages/adapters/codex-local` | `gpt-4o`, `gpt-4o-mini`, `o1-preview`, `o1-mini` | Hosted Cloud (HTTPS API) | **Verified** |
| **OpenRouter** | `packages/adapters/cursor-cloud` | Multi-model gateway (Llama 3.3, Qwen 2.5 72B, DeepSeek V3) | Hosted Cloud Gateway | **Verified** |
| **Ollama** | `packages/adapters/ollama-local` | `llama3.2`, `qwen2.5-coder`, `mistral`, `deepseek-coder` | Local On-Premises (Port 11434) | **Verified** |
| **Google Gemini** | `packages/adapters/gemini-local` | `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-2.0-flash` | Hosted Cloud (HTTPS API) | **Verified** |
| **Kimi / Moonshot** | `packages/adapters/kimi-local` | `moonshot-v1-8k`, `moonshot-v1-32k` | Hosted Cloud (HTTPS API) | **Verified** |
| **xAI Grok** | `packages/adapters/grok-local` | `grok-beta`, `grok-2` | Hosted Cloud (HTTPS API) | **Verified** |

---

## 2. Model Selection & Routing Rules

Model selection follows a hierarchical priority cascade evaluated per heartbeat turn in `server/src/services/ai-connection-runtime.ts`:

```
+---------------------------------------------------------------------------------------------------+
|                                MODEL SELECTION CASCADE                                            |
|                                                                                                   |
|  [Priority 1: Agent Pinning]                                                                      |
|  Does the specific agent profile explicitly pin a model?                                          |
|  (e.g., QA Agent pinned to `gpt-4o-mini`, Tech Lead pinned to `claude-3-5-sonnet`)                |
|  ├── YES ──▶ Use pinned model configuration                                                       |
|  └── NO  ──▼                                                                                      |
|                                                                                                   |
|  [Priority 2: Company Default AI Connection]                                                      |
|  Does the target Virtual Company have a configured default provider?                              |
|  ├── YES ──▶ Use company default provider and API key                                             |
|  └── NO  ──▼                                                                                      |
|                                                                                                   |
|  [Priority 3: System Environment Fallback]                                                        |
|  Evaluate process environment variables:                                                          |
|  1. ANTHROPIC_API_KEY set? ──▶ Route to Claude 3.5 Sonnet                                         |
|  2. OPENAI_API_KEY set?    ──▶ Route to GPT-4o                                                    |
|  3. OPENROUTER_API_KEY set?──▶ Route to OpenRouter Default                                        |
|  4. Ollama daemon online?  ──▶ Fallback to local Ollama inference                                 |
|  5. None available         ──▶ Refusal error: Prompt operator to configure an AI connection.      |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Request & Response Normalization

Each adapter package translates the standardized Geetorus agent turn payload into the target provider's native format:

1. **System Prompt Normalization**:
   - System prompt instructions, agent identity, company guidelines, and available tool descriptions are formatted into the provider's native `system` role.
2. **Function Calling / Tool Schema**:
   - Tool specifications are converted into JSON Schema standards (e.g., Anthropic `tools` array with `input_schema` or OpenAI `functions` array with `parameters`).
3. **Token Usage Normalization**:
   - Adapters extract prompt tokens, completion tokens, and cache-read tokens, returning a unified `TokenUsageReport`:
   ```typescript
   export interface TokenUsageReport {
     promptTokens: number;
     completionTokens: number;
     totalTokens: number;
     estimatedCostUsd: number;
   }
   ```
   - This report is ingested by `costs.ts` to update the company's financial budget counters.

---

## 4. Failure, Rate-Limit, and Timeout Handling

* **Rate Limits (HTTP 429)**:
  - Adapters implement exponential backoff with jitter (initial delay: 1,000ms, multiplier: 2.0, max attempts: 3).
* **Provider Outages (HTTP 5xx)**:
  - If a primary cloud provider fails after retries, the turn reconciler evaluates whether a secondary fallback provider is defined for that company. If yes, it attempts failover; if no, the turn pauses and alerts the operator.
* **Context Window Truncation**:
  - Long conversation threads undergo sliding-window truncation. Older assistant observations are compressed into a summary slot (`summary-slots.ts`) to stay within model token limits (e.g., 200,000 tokens for Claude 3.5).
* **Network Timeouts**:
  - Default request timeout is set to 90 seconds. If an inference request exceeds this threshold, the watchdog supervisor aborts the socket connection, records a timeout error, and prevents the heartbeat runner from stalling.

---

## 5. Adding a New AI Provider: Developer Guide

Adding a new provider (e.g., a custom enterprise model endpoint) requires 3 straightforward steps:

1. **Create Adapter Package**: Add `packages/adapters/custom-provider` implementing the `AiModelAdapter` interface (`packages/shared/src/types/adapter.ts`).
2. **Implement `invokeTurn()`**: Handle authentication, request serialization, tool-call parsing, and token counting.
3. **Register in Adapter Registry**: Add the adapter identifier to `server/src/services/adapter-registry-bootstrap.ts`.
