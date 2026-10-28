# Geetorus — Technical Architecture & System Overview

## 1. High-Level Architectural Topology

Geetorus is structured as a modular monorepo combining a Node.js API server, a real-time reactive web frontend, an enterprise Drizzle ORM data layer, and pluggable AI adapters and sandbox execution providers.

```
+-----------------------------------------------------------------------------------------+
|                                    OPERATOR CLIENTS                                     |
|  +-------------------------------------+       +-------------------------------------+  |
|  |       Geetorus React / Vite UI      |       |          Geetorus CLI Tools         |  |
|  |  (Tailwind v4 Semantic Design Tokens)|       |   (geetorusai / companies.sh)       |  |
|  +-------------------------------------+       +-------------------------------------+  |
+-----------------------------------------------------------------------------------------+
                                │ HTTP / REST & Server-Sent Events (SSE)
                                ▼
+-----------------------------------------------------------------------------------------+
|                                  GEETORUS API SERVER                                    |
|  +-----------------------------------------------------------------------------------+  |
|  |  Express.js API Router (78 Routes: /api/companies, /api/issues, /api/agents, ...) |  |
|  +-----------------------------------------------------------------------------------+  |
|  |  Security & Auth Engine (Session Tokens, API Keys, Company-Scope Middleware)       |  |
|  +-----------------------------------------------------------------------------------+  |
|  |  Orchestration Core:                                                              |  |
|  |  • Heartbeat Runner & Turn Scheduler       • Watchdog & Recovery Supervisor       |  |
|  |  • MCP Tool Gateway & Intent Router        • Budget & Token Gatekeeper            |  |
|  |  • Completion Contract Verifier            • Immutable Audit Activity Logger      |  |
|  +-----------------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------------+
             │                                    │                          │
             ▼                                    ▼                          ▼
+-------------------------+          +-------------------------+    +---------------------+
|   DATA & PERSISTENCE    |          |    AI ADAPTER LAYER     |    | EXECUTION SANDBOXES |
|  • PostgreSQL 16+       |          |  • Anthropic (Claude)   |    |  • Local Workspace  |
|  • Drizzle ORM Schema   |          |  • OpenAI (GPT-4o)      |    |  • Docker Container |
|    (137 Domain Tables)  |          |  • OpenRouter Gateway   |    |  • e2b Sandboxes    |
|  • Encrypted Secrets    |          |  • MiniMax & Ollama     |    |  • Daytona / Modal  |
+-------------------------+          +-------------------------+    +---------------------+
```

---

## 2. Monorepo Package Topology

The repository follows a clean, decoupled package architecture managed via `pnpm` workspaces:

```
geetorusai/
├── cli/                   # Unified geetorusai CLI entrypoint
├── packages/
│   ├── db/                # Drizzle ORM schema, migrations, connection pools
│   ├── shared/            # Shared TypeScript interfaces, validators, constants
│   ├── adapters/          # AI model provider adapters and token counters
│   ├── plugins/           # Extensible plugin runtime and lifecycle hooks
│   ├── adapter-utils/     # Token streaming and message serialization helpers
│   ├── mcp-server/        # Embedded Model Context Protocol server endpoints
│   ├── skills-catalog/    # Reusable skill definitions and YAML validators
│   └── geetorus-eval-kernel # Evaluation harnesses and regression scoring
├── server/                # Express.js REST API and background worker daemon
└── ui/                    # React 19 + Vite frontend application
```

---

## 3. Core System Responsibilities

### Server Subsystem (`@geetorusai/server`)
- Exposes 78 REST API routes and Server-Sent Event (SSE) streams under `/api`.
- Enforces multi-tenant isolation via mandatory company-scope request checks.
- Manages agent turn lifecycles, execution timeouts, and watchdog interventions.
- Handles encrypted secret storage and dynamic injection into execution environments.

### Frontend Subsystem (`@geetorusai/ui`)
- Implements high-density operational dashboards with zero visual drift.
- Connects to backend SSE endpoints for real-time turn streaming and log output.
- Features interactive Org Chart rendering, Task Kanban boards, and Approval takeover modals.
- Enforces strict design tokens (`ui/src/index.css`) verified by visual regression tests.

### Database Subsystem (`@geetorusai/db`)
- 137 strictly typed Drizzle schema definitions covering companies, agents, tasks, tool permissions, and finance events.
- Embedded PostgreSQL runner (`migration-runtime.ts`) for effortless local developer bootstrapping.
- Foreign key constraints, unique indexes, and audit timestamps across all tables.
