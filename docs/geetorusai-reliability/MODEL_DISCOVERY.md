# GeetorusAI Dynamic AI Model Discovery

## 1. Objectives

Hardcoding model names into static arrays leads to stale catalogs, broken workflows when models are deprecated, and an inability to use newly released frontier models without code releases. 

GeetorusAI introduces **Dynamic Model Discovery** (`server/src/services/model-discovery/model-discovery-service.ts`) which queries live provider APIs directly and normalizes their capabilities into a single standard schema.

---

## 2. Supported Provider Discovery Endpoints

| Provider | Endpoint | Authentication | Metadata Discovered |
| :--- | :--- | :--- | :--- |
| **OpenAI / Compatible** | `GET {baseUrl}/v1/models` | `Authorization: Bearer <key>` | Model ID, created date, family capabilities |
| **Anthropic** | `GET https://api.anthropic.com/v1/models` | `x-api-key: <key>`, `anthropic-version` | Claude IDs, display names, 200k context |
| **Google Gemini** | `GET https://generativelanguage.googleapis.com/v1beta/models` | `?key=<key>` | Input token limits (up to 2M), modalities (video, audio) |
| **OpenRouter** | `GET https://openrouter.ai/api/v1/models` | `Authorization: Bearer <key>` | Architecture modalities, context lengths, pricing |
| **Ollama (Local)** | `GET {baseUrl}/api/tags` | None (Local socket/HTTP) | Quantization, parameter size, clip vision tags |

---

## 3. Discovered Model Schema

Every model across all providers is normalized to the `DiscoveredModel` interface:

```typescript
export interface DiscoveredModel {
  id: string;
  name: string;
  provider: string;
  contextWindow: number | null;
  maxOutputTokens: number | null;
  modalities: string[];
  capabilities: {
    toolCalling: boolean;
    vision: boolean;
    streaming: boolean;
    jsonOutput: boolean;
  };
  status: "available" | "degraded" | "unsupported" | "unknown";
  discoveredAt: string;
  source: "live_api" | "cached" | "catalog" | "manual";
  rawMetadata?: Record<string, unknown>;
}
```

---

## 4. Connection Testing vs. Model Discovery

GeetorusAI decouples connection verification from catalog enumeration:
1. **Connection Test (`POST /api/models/test-connection`)**:
   - Pings endpoint with credentials.
   - Measures network round-trip latency in milliseconds.
   - Verifies whether credentials authenticate without downloading full catalogs.
2. **Model Discovery (`POST /api/models/discover`)**:
   - Downloads full catalog.
   - Normalizes metadata.
   - Caches results with a 15-minute TTL.
   - Operators can trigger instant cache invalidation via `POST /api/models/refresh` or the "Refresh Catalog" button in the UI.

---

## 5. Security Safeguards

- **No Secret Echo**: Saved API keys are never returned to the frontend or included in discovery responses.
- **Masked Input**: Keys in connection testing modals are input as password fields and transmitted directly over secure session channels.
- **SSRF Validation**: Custom endpoints are audited for private/metadata IP restrictions before the backend sends discovery requests.
