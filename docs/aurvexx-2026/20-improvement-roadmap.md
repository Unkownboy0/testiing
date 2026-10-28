# 20 — Prioritized Product & Engineering Improvement Roadmap

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Structure**: 8-Hour Hackathon Quick Wins vs. Medium/Long-Term Engineering Sprints.

---

## 1. 8-Hour Hackathon Actionable Sprints (Feasible Today)

These 3 high-impact improvements can realistically be completed within an 8-hour hackathon to impress judges:

### Sprint 1: Auto-Kill Windows Embedded Postgres on Dev Runner Exit (Effort: 45 Mins)
* **Problem**: Abruptly terminating `pnpm dev` leaves `postgres.exe` running, locking the shared memory block and blocking subsequent server boots.
* **Solution**: In `scripts/dev-runner.ts`, register `process.on('SIGINT')`, `process.on('SIGTERM')`, and `process.on('exit')` cleanup handlers that run PowerShell `taskkill /F /IM postgres.exe` or call `Stop-Process` on Windows.
* **Files to Change**: `geetorusai/scripts/dev-runner.ts`.
* **Expected Benefit**: 100% reliable zero-crash demo boots during judge presentations.

---

### Sprint 2: Live "Amber Gate" Sound / Notification Ping in UI (Effort: 1 Hour)
* **Problem**: When an agent pauses at an Amber Gate waiting for human approval, the operator might not notice if they are looking away from the screen.
* **Solution**: Add an audible chime or subtle desktop notification in `ui/src/components/ApprovalBanner.tsx` when WebSocket receives an `approval:created` event.
* **Files to Change**: `geetorusai/ui/src/hooks/useLiveEvents.ts`, `ui/src/components/ApprovalCard.tsx`.
* **Expected Benefit**: Dramatic, high-engagement live demonstration effect when judges watch the agent ask for permission.

---

### Sprint 3: Turnkey Company Import Verification Smoke Test (Effort: 1.5 Hours)
* **Problem**: Operators need confidence that importing a template from `geetorus-companies` immediately works without broken dependencies.
* **Solution**: Add a CLI subcommand `companies.sh verify <template-path>` that unpacks the company manifest, validates agent roles and tool permissions against the database schema, and prints a green verification table.
* **Files to Change**: `companies-tool/src/index.ts`, `companies-tool/src/verifier.ts`.
* **Expected Benefit**: Proves virtual company portability to judges in 5 seconds.

---

## 2. Comprehensive Medium & Long-Term Roadmap (P0 – P3)

```
+---------------------------------------------------------------------------------------------------+
|                                  GEETORUS PRODUCT ROADMAP MATRIX                                  |
|                                                                                                   |
|  [P0: Core Correctness & Architecture Hygiene] (Sprint: Next 2 Weeks)                            |
|  1. Route Monolith Splitting: Refactor `server/src/routes/issues.ts` (664KB) into modular routers. |
|  2. Strict Secret Key Startup Guard: Block server boot if weak default secret key in production.  |
|                                                                                                   |
|  [P1: Agent Reasoning & Memory Expansion] (Sprint: Month 1)                                       |
|  1. pgvector Semantic Memory: Persist past task solutions & code snippets with vector embeddings.  |
|  2. Multi-Agent Consensus Voting: Require Tech Lead + QA agents to agree before human review.    |
|  3. Stripe Connect Integration: Real payments for `geetorus-market` template creators.            |
|                                                                                                   |
|  [P2: Enterprise Scaling & Concurrency] (Sprint: Months 2-3)                                      |
|  1. Redis / BullMQ Distributed Worker Queues: Offload heartbeats to multi-node worker clusters.  |
|  2. Hardened Docker Sandbox Autoscaling: On-demand ephemeral containers per agent turn.           |
|  3. Enterprise SAML / SSO: Okta and Azure AD integration for company access management.          |
|                                                                                                   |
|  [P3: Autonomous Agency Ecosystem] (Sprint: Months 4-6)                                           |
|  1. Inter-Company Agent Contracting: Company A hires an agent from Company B for specialized audit.|
|  2. Native Mobile Companion App: iOS/Android app to approve amber gates with FaceID.             |
+---------------------------------------------------------------------------------------------------+
```
