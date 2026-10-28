# Geetorus — Development Setup & Operations Guide

## 1. Prerequisites

- **Node.js**: `>= 24.11.0` (required for native ES Modules and modern crypto/web APIs).
- **PNPM**: `>= 9.4.0` (required for monorepo workspace resolution).
- **Git**: `>= 2.40.0`.
- **Operating System**: Linux, macOS, or Windows 11 (PowerShell / WSL2).

---

## 2. Local Setup & Quickstart

### Step 1: Install Dependencies
From the repository root (`geetorusai/`):
```bash
pnpm install
```

### Step 2: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your LLM API keys:
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
PORT=3100
GEETORUS_SECRET_KEY=change-this-to-a-secure-random-32-byte-hex-string
```

### Step 3: Launch Local Development Server
```bash
pnpm dev
```
This runs `scripts/dev-runner.ts`, automatically:
1. Bootstrapping embedded PostgreSQL on a dedicated local port.
2. Executing pending Drizzle database migrations.
3. Starting the Express API server on `http://localhost:3100/api`.
4. Launching Vite dev server for the React UI on `http://localhost:3100`.

---

## 3. Essential Developer Commands

| Command | Purpose |
| :--- | :--- |
| `pnpm dev` | Start full development environment with hot reload (Port 3100). |
| `pnpm test` | Run stable Vitest test suite. |
| `pnpm --filter @geetorusai/ui exec tsc --noEmit` | Fast TypeScript typecheck on the UI package. |
| `pnpm check:token-gates` | Validate that all UI components strictly use design tokens. |
| `pnpm db:generate` | Generate Drizzle migration files after editing schemas. |
| `pnpm db:migrate` | Apply pending database schema migrations. |
| `pnpm storybook` | Launch Storybook component visual testing workbench. |

---

## 4. Windows-Specific Developer Notes

- **Stale Postgres Process**: If the server fails to start with a shared memory or socket error, an orphaned embedded `postgres.exe` is lingering. Fix it with:
  ```powershell
  Stop-Process -Name postgres -Force -ErrorAction SilentlyContinue
  pnpm dev
  ```
