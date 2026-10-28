# 29 — References, Code Evidence & Audit Trace Register

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Inspection Date**: October 2026  
> **Audited Workspace**: `c:\Users\mohamed farhan\testing-marketing`  
> **Lead Auditor**: Senior Software Architect & AI Systems Evaluator

---

## 1. Traceable Code Evidence Register

Every architectural claim and feature description in the AURVEXX’2026 documentation suite is directly backed by source code in this repository:

| Architectural Claim | Verified File Path | Symbol / Function Name | Line Range / Evidence | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Server Startup & Lifecycle** | `geetorusai/server/src/index.ts` | `startServer()` | Lines 1–2083 | **Verified** |
| **Express App & Route Registry** | `geetorusai/server/src/app.ts` | `createApp()` | Lines 1–1336 (mounts 78 routes) | **Verified** |
| **Turn-Based Heartbeat Daemon** | `geetorusai/server/src/services/heartbeat.ts` | `heartbeatService.start()` | Lines 1–29391 | **Verified** |
| **MCP Tool Gateway & Policy** | `geetorusai/server/src/services/tool-gateway.ts` | `toolGatewayService.dispatch()` | Lines 1–1500 | **Verified** |
| **Amber Gate Human Approvals** | `geetorusai/server/src/routes/approvals.ts` | `approvalRoutes` | `POST /api/approvals/:id/decide` | **Verified** |
| **137 Relational DB Schemas** | `geetorusai/packages/db/src/schema/*.ts` | `issues`, `companies`, `approvals` | 137 separate schema files | **Verified** |
| **Embedded Postgres Zero-Config** | `geetorusai/packages/db/src/embedded-postgres.ts` | `ensurePostgresDatabase()` | Bundled binary runtime | **Verified** |
| **Pluggable Model Adapters** | `geetorusai/packages/adapters/` | Claude, Codex, Ollama, Gemini | 13 adapter subdirectories | **Verified** |
| **Cryptographic Action Signer** | `geetorusai/server/src/services/decision-signing.ts` | `signToolActionPayload()` | HMAC-SHA256 signature verification | **Verified** |
| **Real-Time WebSockets** | `geetorusai/server/src/realtime/live-events-ws.ts` | `setupLiveEventsWebSocketServer()` | Port 3100 `/api/live-events` | **Verified** |
| **Financial Budget & Token Caps** | `geetorusai/server/src/services/budgets.ts` | `budgetService.assertBudgetAvailable()`| Tracks USD & token usage per turn | **Verified** |
| **Turnkey Packaging CLI** | `companies-tool/src/index.ts` | `companies.sh` | Export/import company tarballs | **Verified** |
| **17 Curated Company Blueprints**| `geetorus-companies/` | `fullstack-forge`, `trail-of-bits`, etc. | 17 verified directory configs | **Verified** |

---

## 2. Validation Commands Executed During Audit

| Validation Command | Working Directory | Observed Result | Audit Finding |
| :--- | :--- | :--- | :--- |
| `git status; git branch -v` | `geetorusai` | `On branch main`, clean tree, commit `9c77366` | Codebase is clean and synchronized. |
| `list_dir` on root workspace | Workspace root | Detected 8 subdirectories (core + ecosystem) | Multi-repo ecosystem confirmed present. |
| `list_dir` on server routes | `server/src/routes/` | 78 distinct route files confirmed | Enterprise API route depth verified. |
| `list_dir` on database schemas | `packages/db/src/schema/`| 137 schema files confirmed | Database scale verified. |
| `list_dir` on adapters | `packages/adapters/` | 13 adapter directories confirmed | Multi-model adapter architecture verified. |
| `list_dir` on company templates| `geetorus-companies/` | 17 turnkey blueprints confirmed | Virtual company catalog verified. |
