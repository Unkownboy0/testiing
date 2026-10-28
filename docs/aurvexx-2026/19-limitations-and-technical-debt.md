# 19 — Technical Limitations, Bottlenecks, and Technical Debt

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Integrity Principle**: Absolute technical honesty. Judges reward founders who can pinpoint their real engineering trade-offs and technical debt rather than making exaggerated claims.

---

## 1. Technical Debt Register

| Priority | Component | Specific Technical Debt / Limitation | Evidence in Codebase | Engineering Impact | Feasible Hackathon Fix? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P0** | **Backend Routing** | **Monolithic Route Handlers**: `routes/issues.ts` is ~664KB and contains extensive inline business logic. | `server/src/routes/issues.ts` (14,000+ lines) | Slower hot-reload compilation during active dev; risk of merge conflicts. | Modularize sub-routes into separate controllers (4h). |
| **P0** | **Process Lifecycle** | **Windows Embedded Postgres Stale Locks**: Abrupt process exit leaves `postgres.exe` holding shared memory locks. | `packages/db/src/embedded-postgres.ts` | Causes `EADDRINUSE` or memory lock errors on subsequent restarts. | Add cleanup trap in `scripts/dev-runner.ts` (1h). |
| **P1** | **Agent Memory** | **No Vector Semantic Retrieval**: Memory relies on relational issue discussion history; no cross-task embeddings. | `packages/db/src/schema/*.ts` (No vector columns) | Agents cannot recall patterns solved in completely separate tasks from last month. | Add `pgvector` table extension (4h). |
| **P1** | **Marketplace** | **Mocked Marketplace Checkout**: `geetorus-market` has modern UI but simulates template purchases. | `geetorus-market/src/app` | Monetization loop is currently a demonstration rather than real billing. | Add Stripe Payment Link integration (3h). |
| **P2** | **Scaling** | **Single-Node In-Memory Scheduler**: Heartbeat daemon runs as a local timer loop; not distributed across workers. | `server/src/services/heartbeat.ts` | Limits horizontal scaling across multiple container replicas. | Post-hackathon initiative (requires Redis/BullMQ). |
| **P3** | **Sandbox** | **Host Process Risk in Local Mode**: Shell tool calls execute with the Node process user privileges. | `server/src/services/execution-workspaces.ts` | Untrusted public agents could attempt hostile shell commands. | Enforce Docker container runtime for low-trust agents. |

---

## 2. In-Depth Architectural Critique

### Why does `server/src/routes/issues.ts` have 664KB?
During rapid product evolution, issue transitions (assignment, wakeups, comments, approvals, work product generation, git branch creation) were authored directly inside the route controllers to move fast. 

* **The Trade-Off**: It enabled building a comprehensive enterprise feature set in record time without cross-package ceremony.
* **The Long-Term Solution**: Extract issue sub-domains into distinct service files (`issue-transitions.ts`, `issue-comments.ts`, `issue-git.ts`), leaving the route file as a slim 300-line Zod schema validator and router dispatch.

---

### Windows Embedded Postgres Lock Explanation
On Windows, child process signal termination behaves differently from POSIX `SIGTERM`. When a developer presses `Ctrl+C`, Node exits immediately, but Windows does not automatically terminate child process trees. The orphaned `postgres.exe` continues running in the background, keeping port 54322 bound.
* *Workaround*: Run `Stop-Process -Name postgres -Force -ErrorAction SilentlyContinue` before launching.
