# 14 — Configuration and Environment Variables Reference

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Codebase audit of `.env.example`, `geetorusai/.env.example`, and `server/src/config.ts`.

---

## 1. Environment Variable Reference

All configuration variables are loaded via Node.js environment or a root `.env` file during startup:

| Variable Name | Required? | Default / Type | Purpose & Description | Verification Evidence |
| :--- | :--- | :--- | :--- | :--- |
| `NODE_ENV` | Optional | `development` | Runtime environment mode (`development`, `production`, `test`). | `server/src/config.ts` |
| `PORT` | Optional | `3100` | Port for the Express API server and UI bundle. | `server/src/index.ts:L43` |
| `DATABASE_URL` | Optional | *(empty)* | PostgreSQL connection string. If omitted, boots embedded PostgreSQL automatically. | `packages/db/src/embedded-postgres.ts` |
| `GEETORUS_SECRET_KEY` | **Required** | 32-byte hex string | Master encryption key used to encrypt API tokens in `company_secrets` table. | `server/src/services/secrets.ts` |
| `BETTER_AUTH_SECRET` | Optional | `geetorus-dev-secret` | Session token signing secret for human operator logins. | `server/src/app.ts` |
| `GEETORUS_TOOL_ACTION_SIGNING_SECRET` | **Required** | Shared string | HMAC signing secret used by the Tool Gateway to verify privileged tool calls. | `server/src/services/tool-gateway.ts` |
| `ANTHROPIC_API_KEY` | Optional* | `sk-ant-api03-...` | API key for Anthropic Claude 3.5 Sonnet / Haiku. | `packages/adapters/claude-local` |
| `OPENAI_API_KEY` | Optional* | `sk-proj-...` | API key for OpenAI GPT-4o / GPT-4o-mini. | `packages/adapters/codex-local` |
| `OPENROUTER_API_KEY` | Optional* | `sk-or-v1-...` | API key for OpenRouter multi-model gateway. | `packages/adapters/cursor-cloud` |
| `DAYTONA_API_KEY` | Optional | String | API key for provisioning remote Daytona execution sandboxes. | `server/src/services/environments.ts` |
| `E2B_API_KEY` | Optional | String | API key for provisioning remote e2b cloud sandboxes. | `server/src/services/environments.ts` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Optional | URL | OpenTelemetry collector endpoint for metrics and tracing. | `server/src/instrumentation.ts` |

*\* Note: At least one LLM API key (or a running local Ollama instance on `http://localhost:11434`) is required for agent execution.*

---

## 2. Sample `.env` Configuration File

Create this file as `.env` in the repository root for zero-config local development:

```bash
# Core Server Settings
NODE_ENV=development
PORT=3100

# Database Configuration (Leave empty to use embedded PostgreSQL on Windows/Linux)
DATABASE_URL=

# Cryptographic Master Keys (Generate unique 32-byte string for production)
GEETORUS_SECRET_KEY=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
BETTER_AUTH_SECRET=geetorus-local-development-secret-key-12345
GEETORUS_TOOL_ACTION_SIGNING_SECRET=geetorus-tool-signing-secret-local-dev-key

# Foundation Model Providers (Configure at least one)
ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-key-here
OPENAI_API_KEY=sk-proj-your-openai-key-here
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key-here

# Performance & Concurrency Tuning
GEETORUS_WORKSPACE_GIT_SCAN_CONCURRENCY=2
GEETORUS_WORKSPACE_GIT_SCAN_TIMEOUT_MS=8000
```
