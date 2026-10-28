# 07 — Functions, Classes, and Responsibilities Reference

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Extracted directly from `geetorusai/server`, `packages/db`, and `packages/adapters`.

---

## 1. Application Lifecycle & Startup

### `startServer()`
* **File Path**: `geetorusai/server/src/index.ts`
* **Purpose**: Orchestrates the complete bootstrap sequence of the Geetorus control plane daemon.
* **Parameters**: None. Reads configuration from environment variables and `loadConfig()`.
* **Return Value**: `Promise<HttpServer>` — The running Node.js HTTP server instance.
* **Internal Operations**:
  1. Awaits `instrumentationReady` (OpenTelemetry bootstrap) and `sentryReady`.
  2. Resolves database connection: invokes `ensurePostgresDatabase()` and `prepareEmbeddedPostgresNativeRuntime()`.
  3. Executes database migration check via `inspectMigrations()` and applies changes via `applyPendingMigrations()`.
  4. Calls `createApp(db, config)` to instantiate the Express application and routes.
  5. Binds WebSockets (`setupLiveEventsWebSocketServer`, `setupEnvironmentCustomImageTerminalWebSocketServer`).
  6. Starts the background heartbeat loop via `heartbeatService.start()`.
* **Dependencies**: `@geetorusai/db`, `detect-port`, `createApp`, OpenTelemetry SDK.
* **Callers**: Direct execution on process start (`server/src/index.ts`).
* **Side Effects**: Spawns background PostgreSQL process (if embedded), opens port 3100, writes startup banners to stdout.
* **Exceptions**: Throws `StartupRefusalError` if Node version is unsupported or database migrations fail.
* **Security**: Enforces `NODE_ENV` policy and redacts sensitive environment keys from startup logs.
* **Status**: **Verified** (`server/src/index.ts:L1-L2083`).

---

### `createApp(db: Db, config: AppConfig)`
* **File Path**: `geetorusai/server/src/app.ts`
* **Purpose**: Express application factory function constructing middleware pipelines and routing tables.
* **Parameters**:
  - `db: Db`: Drizzle ORM database client.
  - `config: AppConfig`: Parsed server runtime configuration object.
* **Return Value**: `Express.Application`: Configured Express application instance.
* **Internal Operations**:
  1. Registers global middlewares: `express.json({ limit: '50mb' })`, `express.urlencoded()`, `httpLogger`.
  2. Binds authentication and scoping middleware: `actorMiddleware(db)`.
  3. Mounts 78 distinct route routers under `/api/*` prefix.
  4. Attaches fallback static handler for the React UI and standard error boundary `errorHandler`.
* **Callers**: `startServer()` in `server/src/index.ts`.
* **Security**: Applies `privateHostnameGuard` and `trustProxy` to protect against SSRF and IP spoofing.
* **Status**: **Verified** (`server/src/app.ts:L44-L1336`).

---

## 2. Orchestration & Heartbeat Execution

### `heartbeatService.start()` / `executeRunnableHeartbeatTurn()`
* **File Path**: `geetorusai/server/src/services/heartbeat.ts`
* **Purpose**: Schedules and executes the turn-based autonomous agent loop across all active companies.
* **Parameters**: `intervalMs?: number` (default: 1000ms).
* **Return Value**: `void` (runs as a long-lived async timer loop).
* **Internal Operations**:
  1. Polls `issues` table for records matching `status = 'in_progress'` or runnable `status = 'open'`.
  2. Invokes `workspaceRuntimeLeaseService.claimLease()` to acquire an exclusive lock on the issue workspace.
  3. Checks financial budget thresholds via `budgetService.assertBudgetAvailable()`.
  4. Calls `renderGeetorusWakePrompt()` to construct system prompts and inject file tree context.
  5. Dispatches prompt to the active AI adapter (`claude-local`, `codex-local`, etc.).
  6. Evaluates LLM output: if tool calls are requested, routes each call through `toolGatewayService.dispatch()`.
  7. If tool calls require approval, sets issue to paused state and emits live WebSocket event.
  8. Commits turn outcomes, token usage, and execution telemetry to `heartbeat_runs` table.
* **Dependencies**: `aiConnectionService`, `toolGatewayService`, `budgetService`, `workspaceRuntimeLeaseService`.
* **Security**: Prevents runaway loops by enforcing strict max turn limits and watchdog deadlines.
* **Status**: **Verified** (`server/src/services/heartbeat.ts:L1-L29391`).

---

## 3. Tool Gateway & Governance

### `toolGatewayService.dispatch(request: ToolDispatchRequest)`
* **File Path**: `geetorusai/server/src/services/tool-gateway.ts`
* **Purpose**: The central security gateway regulating and executing all agent tool intents.
* **Parameters**:
  - `request.companyId: string`: Scoped company ID.
  - `request.agentId: string`: Originating agent ID.
  - `request.toolName: string`: Tool identifier (e.g., `bash`, `file_write`, `git_commit`).
  - `request.parameters: Record<string, unknown>`: Tool arguments.
  - `request.actionSignature?: string`: Cryptographic HMAC token for authenticated actions.
* **Return Value**: `Promise<ToolDispatchResult>`: Object containing `{ status: 'success' | 'amber_gate' | 'denied', output?: string, approvalId?: string }`.
* **Internal Operations**:
  1. Inspects company tool access policies via `toolAccessPolicyService`.
  2. If tool policy is `DENY`, returns immediate rejection error.
  3. If tool policy is `REQUIRE_APPROVAL` (Amber Gate), calls `approvalService.createApproval()` and returns `{ status: 'amber_gate' }`.
  4. If tool policy is `ALLOW`, verifies HMAC signature using `GEETORUS_TOOL_ACTION_SIGNING_SECRET`.
  5. Dispatches execution to the target execution workspace or container sandbox.
  6. Captures execution stdout/stderr and records an immutable entry in `activity_log`.
* **Security**: Strictly prevents shell injection and unauthorized file path traversal (`portable-path.ts`).
* **Status**: **Verified** (`server/src/services/tool-gateway.ts`).

---

## 4. Human Approval Management

### `approvalService.decideApproval(approvalId: string, decision: 'approved' | 'rejected', actor: Actor)`
* **File Path**: `geetorusai/server/src/services/approvals.ts`
* **Purpose**: Processes human operator decisions on amber-gated agent actions.
* **Parameters**:
  - `approvalId: string`: Unique ID of the pending approval record.
  - `decision: 'approved' | 'rejected'`: The operator's verdict.
  - `actor: Actor`: The authenticated operator performing the review.
* **Return Value**: `Promise<ApprovalRecord>`: Updated approval entity.
* **Internal Operations**:
  1. Verifies operator has write permissions for the target company.
  2. Updates `approvals` table with decision status and timestamp.
  3. Inserts review comments if operator supplied feedback.
  4. If `approved`, wakes up the associated heartbeat turn via `heartbeatService.wakeTurnForApproval(approvalId)`.
  5. If `rejected`, notifies the agent with the operator's rejection explanation to allow replanning.
* **Status**: **Verified** (`server/src/services/approvals.ts`).
