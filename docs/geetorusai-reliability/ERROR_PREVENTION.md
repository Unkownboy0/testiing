# GeetorusAI Proactive Error Prevention

## 1. Overview

Rather than waiting for failures to occur downstream or after consuming expensive inference tokens, GeetorusAI performs preflight validations at boundaries:
- Saving provider credentials and endpoints.
- Dispatching user tasks and agent routines.
- Invoking streaming or completion requests.

---

## 2. Validation Boundaries

The preflight validation layer lives in `server/src/services/self-healing/preflight-validator.ts` and exposes `validatePreflight()`.

```typescript
export interface PreflightValidationInput {
  provider: string;
  model: string;
  prompt?: string;
  baseUrl?: string;
  apiKey?: string;
  temperature?: number;
  maxTokens?: number;
  contextLengthEstimated?: number;
  knownModelContextWindow?: number | null;
  allowLocalhost?: boolean;
}
```

### 2.1 SSRF & Metadata Protection
Custom provider base URLs (e.g. for vLLM, Ollama, or private inference proxies) undergo security inspection:
- **Cloud Metadata Protection**: Immediately blocks `169.254.169.254`, `metadata.google.internal`, `instance-data`, and `fd00::`.
- **Private RFC1918 Ranges**: Requests to `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16` are blocked unless explicitly configured for local runtimes.
- **Protocol Whitelist**: Only `http:` and `https:` are permitted (preventing `file://`, `gopher://`, etc.).

### 2.2 Payload & Prompt Verification
- **Empty Prompt Detection**: Blocks blank or whitespace-only inputs before triggering inference fees.
- **Maximum Payload Safeguards**: Limits requests to 10MB maximum payload buffers.

### 2.3 Context Window Boundary Checks
When context lengths can be estimated or token metadata is known:
- If estimated token count exceeds `knownModelContextWindow`, the request is rejected with actionable feedback before network transmission.
- If estimated token count is within 90% of the maximum context capacity, a proactive warning is issued.

### 2.4 Parameter Bounds Checking
- Temperature verified within $[0.0, 2.0]$.
- Max tokens verified $> 0$.

---

## 3. Preflight API Endpoint

`POST /api/models/preflight`

### Request Example
```json
{
  "provider": "openai",
  "model": "gpt-4o",
  "prompt": "Analyze system performance telemetry.",
  "maxTokens": 4096,
  "contextLengthEstimated": 850,
  "knownModelContextWindow": 128000
}
```

### Response Example
```json
{
  "valid": true,
  "provider": "openai",
  "model": "gpt-4o",
  "checks": [
    { "name": "provider_configured", "passed": true, "message": "Provider 'openai' specified." },
    { "name": "model_selected", "passed": true, "message": "Model 'gpt-4o' selected." },
    { "name": "prompt_not_empty", "passed": true, "message": "Prompt payload is non-empty." },
    { "name": "payload_size", "passed": true, "message": "Prompt size is within safe bounds (1 KB)." },
    { "name": "context_window_limit", "passed": true, "message": "Estimated token count is within model context window." }
  ],
  "warnings": [],
  "errors": [],
  "checkedAt": "2026-10-09T14:00:00.000Z"
}
```
