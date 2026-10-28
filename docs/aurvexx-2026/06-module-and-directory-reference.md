# 06 — Module and Directory Reference

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Inspection Basis**: Complete directory scan of the active workspace and monorepo packages.

---

## 1. Monorepo Root Directory Layout (`geetorusai/`)

```
geetorusai/
├── cli/                         # Unified `geetorusai` CLI command suite
├── packages/                    # Decoupled shared libraries and adapters
│   ├── adapter-utils/           # Git sync, prompt rendering, stream serialization
│   ├── adapters/                # 13 Model adapters (Claude, Codex, Ollama, Gemini, etc.)
│   ├── db/                      # Drizzle ORM schemas, migration runtime, embedded Postgres
│   ├── geetorus-eval-kernel/    # Evaluation harnesses, scoring, promptfoo integrations
│   ├── geetorus-runner/         # Containerized runner runtime and remote process managers
│   ├── google-sheets-mcp-server/# Built-in MCP server for Google Sheets integration
│   ├── kv-demo-mcp-server/      # Key-Value demonstration MCP server
│   ├── mcp-server/              # Core embedded Model Context Protocol server
│   ├── plugins/                 # Extensible plugin system and lifecycle hooks
│   ├── shared/                  # Shared TypeScript types, Zod validators, design constants
│   ├── skills-catalog/          # Reusable skill definitions (agentmail, para-memory, etc.)
│   ├── tailscale-https-broker/  # Tailscale HTTPS tunneling broker for secure remote access
│   └── teams-catalog/           # Pre-configured agent team blueprints
├── patches/                     # Patched npm dependencies (embedded-postgres, acpx, etc.)
├── scripts/                     # Dev runner (`dev-runner.ts`), token checkers, release tools
├── server/                      # Express.js REST API server and background orchestrator
├── skills/                      # Internal agent skills (board, create-agent, task conversion)
├── tests/                       # E2E test suites, Playwright, acceptance tests, perf tests
└── ui/                          # React 19 + Vite frontend control plane application
```

---

## 2. Server Architecture Layout (`geetorusai/server/`)

| Directory / File | Size / File Count | Purpose and Key Responsibilities |
| :--- | :--- | :--- |
| `server/src/index.ts` | 2,083 lines / 90KB | Main server entry point. Boots OpenTelemetry, Sentry, embedded Postgres, and initiates background services. |
| `server/src/app.ts` | 1,336 lines / 54KB | Express application factory. Registers middlewares, mounts 78 route modules, and binds WebSocket servers. |
| `server/src/routes/` | **78 files** | Complete REST endpoint layer. Handlers for `issues.ts`, `companies.ts`, `agents.ts`, `approvals.ts`, `tools.ts`, etc. |
| `server/src/services/` | **487 files** | Business logic layer. Includes `heartbeat.ts` (29K lines), `chat-channels.ts` (1.4MB), `tool-gateway.ts` (373KB), and `secrets.ts` (221KB). |
| `server/src/middleware/` | 15+ files | Security, authentication (`actorMiddleware`), HTTP logging, CORS, and trust proxy policies. |
| `server/src/realtime/` | 4 files | WebSocket servers: `live-events-ws.ts`, `environment-custom-image-terminal-ws.ts`, `runner-prp-ws.ts`. |
| `server/src/storage/` | 5+ files | Storage abstractions for local disk, artifacts, and file resource attachments. |

---

## 3. Database Package Layout (`geetorusai/packages/db/`)

| Sub-path | File Count | Description |
| :--- | :--- | :--- |
| `packages/db/src/schema/` | **137 files** | Declarative PostgreSQL table schemas defined via Drizzle ORM. Covers issues, companies, agents, turns, approvals, and secrets. |
| `packages/db/src/index.ts` | Central barrel | Exports all schema objects, query builders, and database connection utilities (`createDb`). |
| `packages/db/src/embedded-postgres.ts` | Core runtime | Manages the lifecycle of the local embedded PostgreSQL binary (`embedded-postgres@18.1.0`). |
| `packages/db/src/migration-runtime.ts` | Migrator | Applies pending SQL migrations deterministically on server boot without requiring manual database commands. |

---

## 4. Frontend Architecture Layout (`geetorusai/ui/`)

| Sub-path | Key Files | Description |
| :--- | :--- | :--- |
| `ui/src/App.tsx` | 842 lines | Main client router defining routes for Dashboard, Issues, Agents, Approvals, Companies, Pipelines, and Settings. |
| `ui/src/pages/` | 35+ pages | Top-level view components (`Dashboard.tsx`, `Issues.tsx`, `IssueDetail.tsx`, `Agents.tsx`, `Approvals.tsx`). |
| `ui/src/components/` | 150+ components | Reusable UI building blocks, modal dialogs, approval cards, and layout containers. |
| `ui/src/hooks/` | 25+ hooks | Custom data fetching and mutation hooks powered by TanStack Query (`useIssues.ts`, `useLiveEvents.ts`). |
| `ui/src/index.css` | Design Tokens | The canonical design token system (HSL colors, glassmorphism, spacing, animations). No raw hex values permitted. |

---

## 5. Ecosystem Repositories Layout (Workspace Level)

1. **`companies-tool/`**:
   - Contains the `companies.sh` CLI for packaging virtual company templates into tarballs and unpacking them into target Geetorus instances.
2. **`geetorus-companies/`**:
   - Curated library of 17 turnkey virtual company configurations:
     - `fullstack-forge`: General full-stack TypeScript/React/Node software engineering department.
     - `trail-of-bits-security`: Security audit, dependency vulnerability analysis, and fuzzing team.
     - `clawteam-engineering`: High-velocity systems engineering team.
     - `product-compass-consulting`: Product management, user story decomposition, and spec writing team.
3. **`geetorus-market/`**:
   - Next.js 15 web application for sharing, browsing, and importing virtual company templates.
4. **`geetorus-docs-docusaurus/`**:
   - Public documentation site built on Docusaurus for external community documentation.
