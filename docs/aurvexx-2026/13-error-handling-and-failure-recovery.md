# 13 — Error Handling, Failure Modes, and Recovery Architecture

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Codebase audit of `server/src/errors.ts`, `server/src/services/task-watchdogs.ts`, `server/src/startup-refusals.ts`, and `embedded-postgres.ts`.

---

## 1. Error Taxonomy and Propagation Flow

Geetorus categorizes errors into four distinct operational tiers:

```
+---------------------------------------------------------------------------------------------------+
|                                     ERROR PROPAGATION TIERS                                       |
|                                                                                                   |
|  [Tier 1: Boundary & Schema Errors]                                                               |
|  • Zod Validation Failures ──▶ Express Middleware ──▶ HTTP 400 Bad Request with field details.    |
|  • Auth & Scoping Mismatches ──▶ `actorMiddleware` ──▶ HTTP 401 Unauthorized / 403 Forbidden.     |
|                                                                                                   |
|  [Tier 2: Model & Network Outages]                                                                |
|  • Rate Limits (HTTP 429) ──▶ Adapter Exponential Backoff (3 retries with jitter).                |
|  • Provider Downtime (5xx) ──▶ Failover to secondary provider or pause turn with alert.          |
|                                                                                                   |
|  [Tier 3: Autonomous Execution Failures]                                                          |
|  • Tool Non-Zero Exit (e.g. test failure) ──▶ Stderr captured as observation; Agent self-corrects.|
|  • Deadlocks / Infinite Hangs ──▶ `task-watchdogs.ts` revokes lease after 300s stall timeout.      |
|                                                                                                   |
|  [Tier 4: Process & Infrastructure Failures]                                                      |
|  • Embedded Postgres Stale PID ──▶ Detects locked memory block; logs recovery instructions.       |
|  • Server Crash / Reboot ──▶ On restart, `reconcileAbandonedExecutionControl()` resets leases.   |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Detailed Failure Modes & Verified Recovery Behavior

### 2.1. Tool Non-Zero Exit Codes (Syntax Errors, Test Failures)
* **Root Cause**: An agent creates a TypeScript file with a syntax error or runs a test suite that fails.
* **Current Behavior**:
  - The tool execution process in the worktree exits with a non-zero exit code (e.g., code `1`).
  - Instead of crashing the server or terminating the issue, `toolGatewayService` captures `stdout` and `stderr`.
  - It packages the error message into a standard tool response:
    ```json
    { "error": "Command failed with exit code 1", "stderr": "TypeError: Cannot read property 'id' of undefined" }
    ```
  - This observation is fed back to the LLM on the next heartbeat turn.
  - The model observes the stack trace, modifies the file to fix the bug, and re-executes the test.
* **Verification Status**: **Verified** (`server/src/services/tool-gateway.ts`).

---

### 2.2. Long-Running Turn Stalls & Watchdog Expiry
* **Root Cause**: An agent executes an interactive shell command that hangs waiting for stdin (e.g., `npm init` or unflagged prompt) or model API connection drops silently.
* **Current Behavior**:
  - `taskWatchdogService` runs periodically in `server/src/services/task-watchdogs.ts`.
  - If a turn's active lease has had no activity for greater than the configured timeout (default: 300 seconds), the watchdog intervenes.
  - The watchdog revokes the `workspace_runtime_leases` record, transitions the issue to `'stalled'` status, and broadcasts a warning over WebSocket.
* **Verification Status**: **Verified** (`server/src/services/task-watchdogs.ts`).

---

### 2.3. Embedded PostgreSQL Process Locking (Windows Gotcha)
* **Root Cause**: If the Node.js development server is killed abruptly via `Ctrl+C` or a terminal crash on Windows, the spawned `postgres.exe` subprocess may remain running in the background.
* **Symptom**: On subsequent `pnpm dev`, the server fails with:
  ```
  Embedded Postgres Error: shared memory block already in use / port locked
  ```
* **Recovery Procedure**:
  Run PowerShell kill command before restarting:
  ```powershell
  Stop-Process -Name postgres -Force -ErrorAction SilentlyContinue
  pnpm dev
  ```
* **Verification Status**: **Verified** (`packages/db/src/embedded-postgres.ts`).

---

### 2.4. Abandoned Turn Reconciliation on Server Reboot
* **Root Cause**: The host machine reboots or the container is terminated while 5 tasks are `in_progress`.
* **Current Behavior**:
  - On server startup, `startServer()` calls `reconcileAbandonedExecutionControl()` in `server/src/index.ts:L14`.
  - It queries all issues marked `in_progress` whose leases have expired.
  - It clears orphan locks, writes a restart tombstone event to `heartbeat_runs`, and returns the issues to the ready queue so the heartbeat runner can resume them safely.
* **Verification Status**: **Verified** (`server/src/services/execution-control-reconciliation.ts`).
