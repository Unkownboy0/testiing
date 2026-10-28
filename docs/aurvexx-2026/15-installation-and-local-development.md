# 15 — Installation and Local Development Setup

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Verified from `geetorusai/package.json` scripts, `dev-runner.ts`, and root `README.md`.

---

## 1. System Prerequisites

Before launching Geetorus locally, ensure the host system satisfies:

1. **Node.js**: Version **>= 24.11.0** (Required by engine policy in `package.json:L100`).
2. **Package Manager**: **`pnpm` 9.15.4+** (Uses pnpm workspaces and patched dependencies).
3. **Git**: Installed and available in PATH.
4. **Operating System**: Supported on Windows 10/11, macOS, and Linux (Ubuntu 22.04+).

---

## 2. Step-by-Step Local Setup Guide

### Step 1: Install Dependencies
From the repository root or inside `geetorusai/`, install all monorepo workspace dependencies:
```bash
# Inside geetorusai directory
pnpm install
```
*Note: This automatically triggers post-install scripts including linking the plugin SDK and preparing patched packages (`patches/embedded-postgres`).*

---

### Step 2: Configure Environment Variables
Copy the template configuration file:
```bash
cp .env.example .env
```
Open `.env` and add at least one AI API key (e.g., `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`). If you plan to test without external APIs, ensure a local Ollama instance is running on `http://localhost:11434`.

---

### Step 3: Launch Local Development Daemon
```bash
pnpm dev
```
This runs `scripts/dev-runner.ts`, which:
1. Verifies workspace package links.
2. Initializes embedded PostgreSQL on a dynamic loopback port.
3. Automatically runs Drizzle schema migrations.
4. Starts the Express API server on `http://localhost:3100`.
5. Starts the React 19 Vite UI server.

Open your browser and navigate to:
```
http://localhost:3100
```

---

## 3. Working with Turnkey Virtual Companies (`companies-tool`)

Geetorus provides a standalone CLI tool to export and import complete virtual company configurations:

```bash
# Navigate to companies tool directory
cd ../companies-tool

# List available turnkey virtual company templates
pnpm start list

# Import the Fullstack Forge engineering department into your active Geetorus instance
pnpm start import ../geetorus-companies/fullstack-forge

# Import the Trail of Bits security audit team
pnpm start import ../geetorus-companies/trail-of-bits-security
```

---

## 4. Common Development Commands Reference

| Command | Purpose | When to Use |
| :--- | :--- | :--- |
| `pnpm dev` | Starts server + UI with hot-reload watch mode | Standard development workflow |
| `pnpm test` | Runs fast Vitest unit test suite | Verifying changes to services |
| `pnpm db:generate` | Generates Drizzle migration files from schemas | After editing `packages/db/src/schema/*.ts` |
| `pnpm check:tokens` | Validates that UI uses design tokens from `index.css` | Before committing frontend code |
| `pnpm --filter @geetorusai/ui build` | Builds production React frontend bundle | Validating UI for build errors |
