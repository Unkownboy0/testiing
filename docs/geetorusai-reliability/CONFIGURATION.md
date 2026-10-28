# GeetorusAI Configuration Guide

## 1. Environment Variables & Runtime Flags

GeetorusAI supports standard configuration flags for self-healing, provider endpoints, and operational thresholds.

### 1.1 Core Server Configuration
| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `PORT` | `3100` | HTTP listener port for API and frontend. |
| `DATABASE_URL` | Local embedded PostgreSQL | PostgreSQL connection string. |
| `DEPLOYMENT_MODE` | `local_trusted` | `local_trusted` or `authenticated`. |
| `TRUST_PROXY` | `false` | Enable reverse-proxy IP handling (e.g. Railway, Cloudflare). |

### 1.2 Self-Healing & Pulse Tuning
| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `PULSE_AUTO_RECOVERY` | `true` | Enable or disable automated retry and fallback routines. |
| `CIRCUIT_BREAKER_THRESHOLD` | `4` | Number of consecutive failures before tripping a provider breaker. |
| `CIRCUIT_BREAKER_COOLDOWN_MS` | `30000` | Cooldown duration (in milliseconds) before half-open state testing. |
| `MAX_RETRY_ATTEMPTS` | `3` | Maximum bounded retry attempts for recoverable errors. |
| `MODEL_DISCOVERY_TTL_MS` | `900000` | Cache time-to-live for discovered model catalogs (15 minutes). |

---

## 2. AI Provider Settings & Security

### 2.1 Supported Upstream Providers
1. **OpenAI**: Requires `apiKey`. Optional `baseUrl` (defaults to `https://api.openai.com`) and `organizationId`.
2. **Anthropic**: Requires `apiKey` (`sk-ant-...`). Base URL: `https://api.anthropic.com`.
3. **Google Gemini**: Requires `apiKey`. Uses Generative Language v1beta endpoints.
4. **OpenRouter**: Requires `apiKey` (`sk-or-...`). Base URL: `https://openrouter.ai/api`.
5. **Ollama**: Local instance at `http://127.0.0.1:11434` or custom URL. Requires no API key.

### 2.2 Security Guidelines
- **Secret Redaction**: All API keys stored in GeetorusAI secrets are encrypted using the platform's key vault and are never echoed back in plain text across the network.
- **SSRF Safety**: If configuring a private provider URL or inference proxy, do not target internal metadata services (`169.254.169.254`). Such requests will be rejected by the preflight security validator.
