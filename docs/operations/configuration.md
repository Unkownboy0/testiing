# Geetorus — Configuration & Environment Variables

## 1. Environment Variables Reference

| Variable Name | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `NODE_ENV` | No | `development` | Environment mode (`development`, `production`, `test`). |
| `PORT` | No | `3100` | Port on which Express API and Vite reverse proxy listen. |
| `DATABASE_URL` | No | *Embedded Postgres* | PostgreSQL connection URI (`postgres://user:pass@host:5432/dbname`). |
| `GEETORUS_SECRET_KEY` | Yes (in prod) | *Dev Fallback* | 32-byte hex key used for AES-256 vault encryption. |
| `ANTHROPIC_API_KEY` | No | None | API key for Claude 3.7 / 3.5 Sonnet & Haiku models. |
| `OPENAI_API_KEY` | No | None | API key for GPT-4o, GPT-4o-mini, o1, and o3-mini. |
| `OPENROUTER_API_KEY`| No | None | Unified API key for 200+ OpenRouter foundation models. |
| `DAYTONA_API_KEY` | No | None | API key for Daytona remote cloud sandbox runners. |
| `E2B_API_KEY` | No | None | API key for e2b cloud sandbox code execution. |
