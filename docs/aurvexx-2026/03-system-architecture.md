# 03 — Complete System Architecture & Component Inventory

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Inspection Basis**: Real source code in `geetorusai` monorepo  
> **Architecture Style**: Modular Monorepo, Turn-based Orchestration, Multi-Tenant Virtual Company OS

---

## 1. System Topology Overview

Geetorus is structured as a layered, modular architecture where operator requests and agent turns are governed by a central control plane:

```
+---------------------------------------------------------------------------------------------------+
|                                      LAYER 1: PRESENTATION                                        |
|  • Geetorus Web UI (React 19 + Vite + Tailwind Semantic Tokens) [ui/src/App.tsx]                  |
|  • Geetorus CLI (`geetorusai` commander CLI) [cli/src/index.ts]                                   |
|  • Turnkey CLI Tool (`companies.sh` export/import) [companies-tool/src/index.ts]                 |
+---------------------------------------------------------------------------------------------------+
                                                  │ HTTP (REST) / WebSocket (Live Events)
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                      LAYER 2: API & ROUTING                                       |
|  • Express.js Server (`server/src/app.ts`, `server/src/index.ts`)                                 |
|  • 78 Route Handlers (`server/src/routes/*.ts`: companies, issues, agents, approvals, etc.)       |
|  • Security & Scoping Middleware (`server/src/middleware/auth.ts`, company-scope isolation)        |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                 LAYER 3: ORCHESTRATION & CONTROL                                  |
|  • Heartbeat Runner & Turn Scheduler (`server/src/services/heartbeat.ts`)                         |
|  • Watchdogs & Deadlock Reconciler (`server/src/services/task-watchdogs.ts`)                      |
|  • Budget & Financial Guard (`server/src/services/budgets.ts`, `costs.ts`)                        |
|  • Human Approval Engine (`server/src/services/approvals.ts`)                                     |
+---------------------------------------------------------------------------------------------------+
                          │                                           │
                          ▼                                           ▼
+---------------------------------------------+   +-------------------------------------------------+
|     LAYER 4: AI & TOOL EXECUTION            |   |           LAYER 5: DATA & PERSISTENCE           |
|  • Model Adapter Layer (`packages/adapters`)|   |  • PostgreSQL 16+ (Embedded or External)        |
|    - Claude, OpenAI, OpenRouter, Ollama     |   |  • Drizzle ORM Schema (137 Relational Tables)   |
|  • MCP Tool Gateway (`tool-gateway.ts`)     |   |    (`packages/db/src/schema/*.ts`)              |
|  • Execution Sandboxes (`environments.ts`)  |   |  • Encrypted Secrets Store (`secrets.ts`)       |
|    - Local Worktrees, Docker, e2b, Daytona  |   |  • Immutable Activity Log (`activity-log.ts`)   |
+---------------------------------------------+   +-------------------------------------------------+
```

---

## 2. In-Depth Component Breakdown

### 2.1. Presentation Layer (Frontend & CLI)
* **What it is**: The operator interface for supervising virtual companies, inspecting agent task boards, approving actions, and configuring model settings.
* **Location in Repository**: `geetorusai/ui/` and `geetorusai/cli/`.
* **Technology Stack**: React 19, Vite, TanStack Query, Tailwind CSS semantic tokens, Lucide Icons, Commander.js.
* **Responsibilities**:
  - Render real-time task progress, agent turns, and cost metrics.
  - Intercept operator decisions (Approve / Reject / Revise) on amber gates.
  - Deliver instant live updates via WebSocket subscription (`/api/live-events`).
* **Inputs & Outputs**:
  - *Inputs*: REST API endpoints, WebSocket messages, operator mouse/keyboard interactions.
  - *Outputs*: JSON payloads to Express REST endpoints.
* **Failure Mode**: If frontend fails, background agent orchestration continues running uninterrupted on the server.
* **Verification Status**: **Verified** (`ui/src/App.tsx`, `ui/src/pages/Dashboard.tsx`).

---

### 2.2. API & Routing Layer (Backend)
* **What it is**: The centralized HTTP entry point exposing REST and WebSocket interfaces for companies, issues, agents, and tools.
* **Location in Repository**: `geetorusai/server/src/app.ts` and `geetorusai/server/src/routes/*.ts`.
* **Responsibilities**:
  - Route validation via Zod schemas (`@geetorusai/shared`).
  - Strict company scoping: Every route checks tenant membership before granting data access.
  - Authentication: Validates session tokens, Bearer API keys, and CLI auth challenges.
* **Inputs & Outputs**:
  - *Inputs*: HTTP requests with `Authorization` headers and JSON bodies.
  - *Outputs*: Standardized JSON envelopes or SSE streams.
* **Key Routes**:
  - `POST /api/companies`: Creates and configures virtual companies.
  - `POST /api/issues`: Creates issues/tasks with parent-child relationship tracking.
  - `POST /api/approvals/:id/decide`: Grants or denies execution for gated actions.
* **Verification Status**: **Verified** (78 route files in `server/src/routes/`).

---

### 2.3. Orchestration Engine: Heartbeat Daemon
* **What it is**: The core turn-based scheduler that drives autonomous agent actions.
* **Location in Repository**: `geetorusai/server/src/services/heartbeat.ts` (~29,391 lines).
* **Responsibilities**:
  - Detects runnable issues in `in_progress` status.
  - Acquires exclusive execution leases (`workspace-runtime-leases.ts`) to prevent race conditions.
  - Assembles prompt context (system prompt, issue history, tool descriptions).
  - Invokes the appropriate AI model adapter.
  - Processes tool invocation requests or final response outputs.
* **Why it is needed**: Prevents unmanaged infinite while-loops; executes turns deterministically with configurable cooldowns and backoffs.
* **Failure Mode**: If a turn times out or crashes, the watchdog supervisor (`task-watchdogs.ts`) marks the turn as failed and triggers recovery attempts without taking down the server.
* **Verification Status**: **Verified** (`server/src/services/heartbeat.ts`).

---

### 2.4. Tool Gateway & Governance (MCP Compliant)
* **What it is**: The security boundary regulating every tool execution requested by an AI agent.
* **Location in Repository**: `geetorusai/server/src/services/tool-gateway.ts` and `packages/mcp-server/`.
* **Responsibilities**:
  - Maps tool intents (`bash`, `git_commit`, `file_write`, `http_request`) to registered handlers.
  - Checks permission policies: `ALLOW`, `REQUIRE_APPROVAL` (Amber Gate), or `DENY`.
  - Enforces cryptographic action signing using `GEETORUS_TOOL_ACTION_SIGNING_SECRET`.
  - Dispatches execution to local worktrees or isolated sandboxes.
* **Failure Mode**: Unauthorized or malformed tool calls are rejected and fed back into the agent context as error observations.
* **Verification Status**: **Verified** (`server/src/services/tool-gateway.ts`, `server/src/services/tool-access.ts`).

---

### 2.5. AI Model Adapter Layer
* **What it is**: A normalized abstraction interface over external foundation model APIs and local inference engines.
* **Location in Repository**: `geetorusai/packages/adapters/`.
* **Supported Adapters**:
  - `claude-local`: Anthropic Claude 3.5 Sonnet / Haiku.
  - `codex-local`: OpenAI GPT-4o / GPT-4o-mini.
  - `cursor-cloud` & `hermes-gateway`: Cloud gateway bridges.
  - `ollama-local`: Local open-weights models (Llama 3, Qwen 2.5, DeepSeek).
  - `gemini-local`: Google Gemini models.
* **Responsibilities**: Standardizes system instructions, function calling schemas, and token usage reporting across divergent provider APIs.
* **Verification Status**: **Verified** (`packages/adapters/*`).

---

### 2.6. Data & Persistence Layer
* **What it is**: The relational state store tracking the complete operational history of all virtual companies.
* **Location in Repository**: `geetorusai/packages/db/` and PostgreSQL 16+.
* **Technology**: Drizzle ORM, embedded PostgreSQL binary for zero-dependency local development (`embedded-postgres@18.1.0`).
* **Scale**: 137 strictly typed schema definitions covering companies, issues, comments, turns, approvals, budget events, and audit logs.
* **Verification Status**: **Verified** (`packages/db/src/schema/*.ts`).
