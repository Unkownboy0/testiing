# 05 — End-to-End Execution Trace & Working Flow

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Trace Target**: Representative Lifecycle of a Task ("Fix Express Route Bug") from UI Submission to Git Commit

---

## 1. Step-by-Step Chronological Execution Trace

### Phase 1: Application Boot & Environment Initialization
1. **Runner Launch**: Developer runs `pnpm dev` from the repository root. This triggers `scripts/dev-runner.ts`, launching the Express backend (`server/src/index.ts`) and the React Vite frontend (`ui/`).
2. **Telemetry & Sentry Readiness**: `startServer()` in `server/src/index.ts:L3-L7` awaits `instrumentationReady` (OpenTelemetry OTLP) and `sentryReady`.
3. **Database Initialization**: 
   - `ensurePostgresDatabase()` in `packages/db/src/embedded-postgres.ts` checks if `DATABASE_URL` is configured. If empty, it spins up an embedded PostgreSQL instance on a dynamic loopback port.
   - `applyPendingMigrations()` inspects and applies any pending Drizzle migrations from `packages/db/drizzle`.
4. **Express App Construction**: `createApp(db, config)` in `server/src/app.ts:L44` mounts global middlewares (CORS, body parsers, `httpLogger`, `actorMiddleware`), registers 78 route modules, and binds the WebSocket servers (`setupLiveEventsWebSocketServer`).
5. **Heartbeat Scheduler Awaken**: `heartbeatService.start()` initiates the background polling loop (`server/src/services/heartbeat.ts`), running every 1,000ms to detect pending work.

---

### Phase 2: User Request Submission (Frontend to API)
6. **User Interaction**: In the Geetorus UI at `http://localhost:3100`, the user navigates to the **Issues** page (`ui/src/pages/Issues.tsx`) and clicks "New Issue".
7. **Form Input**:
   ```json
   {
     "title": "Fix Auth Token Expiration Bug",
     "description": "Tokens do not refresh after 1 hour in auth.ts",
     "companyId": "cmp_engineering_01",
     "priority": "high",
     "assigneeAgentId": "agent_techlead_01"
   }
   ```
8. **Frontend Handler**: Handled by `createIssueMutation.mutateAsync()` via TanStack Query in `ui/src/hooks/useIssues.ts`, making an authenticated `POST /api/issues` HTTP request.
9. **API Ingestion & Validation**:
   - `server/src/routes/issues.ts` intercepts the request.
   - Zod validation schema `createIssueSchema` (`packages/shared/src/validators`) parses and strictly verifies field types.
   - `assertCompanyAccess(req.actor, companyId)` validates tenant membership.
10. **Database Insertion**:
    - The server inserts the record into the `issues` table via Drizzle ORM:
    ```sql
    INSERT INTO issues (id, company_id, title, status, priority, assignee_agent_id, created_at)
    VALUES ('iss_101', 'cmp_engineering_01', 'Fix Auth Token Expiration Bug', 'open', 'high', 'agent_techlead_01', NOW());
    ```
    - Emits a real-time event via `liveEventsWebSocketServer.broadcast('issue:created', issue)`.
    - Returns HTTP `201 Created` with the issue JSON payload to the UI.

---

### Phase 3: Orchestration & Turn Awakening
11. **Heartbeat Detection**: In `server/src/services/heartbeat.ts`, the poller runs `detectRunnableIssues()`. Issue `iss_101` matches status `'open'` with an assigned agent.
12. **Execution Lease Acquisition**:
    - `workspaceRuntimeLeaseService.claimLease()` acquires an exclusive lease lock (`execution_workspace_runtime_leases` table) to prevent dual-agent collision.
    - Status transitions from `'open'` to `'in_progress'`.
13. **Workspace Provisioning**:
    - `executionWorkspaceService.ensureWorkspace()` checks if a local Git worktree exists for this issue. If not, it runs `git worktree add .geetorus/worktrees/iss_101 -b fix/auth-token`.
14. **Prompt & Context Assembly**:
    - System instructions for `agent_techlead_01` are retrieved from `agent_instructions` table.
    - Issue title, description, and workspace file list are formatted using `renderGeetorusWakePrompt()`.
    - Available MCP tool schemas (`bash`, `git_diff`, `file_read`, `file_write`) are appended into the function-calling tool definition array.

---

### Phase 4: AI Model Invocation & Tool Execution
15. **Model Routing**:
    - `aiConnectionService.resolveActiveConnection(companyId)` retrieves configured credentials (e.g., Anthropic Claude 3.5 Sonnet).
    - Provider adapter (`packages/adapters/claude-local`) formats the message payload into Anthropic's Messages API specification.
16. **LLM Inference**:
    - Adapter sends HTTPS request to `https://api.anthropic.com/v1/messages`.
    - Model responds with a structured tool call:
    ```json
    {
      "stop_reason": "tool_use",
      "content": [
        { "type": "text", "text": "I will inspect the token expiration logic in auth.ts" },
        { "type": "tool_use", "name": "file_read", "input": { "path": "server/src/auth.ts" } }
      ]
    }
    ```
17. **Tool Gateway Validation**:
    - `toolGatewayService.dispatch()` evaluates the tool call against the company's `tool_access` policy.
    - `file_read` is marked policy `'ALLOW'` (Read-only action).
    - Tool executes safely in `.geetorus/worktrees/iss_101` and returns the file contents.
18. **Subsequent Turn & Code Modification**:
    - The file contents are injected back into the LLM context.
    - Model responds with `file_write` modifying `server/src/auth.ts`.
    - `file_write` is flagged as an active change, verified via HMAC signing, and applied to the file.
19. **Amber Gate Human Approval (Sensitive Action)**:
    - Model calls `git_commit_and_push`.
    - Policy triggers `REQUIRE_APPROVAL` (Amber Gate).
    - Turn pauses. An approval record is created in `approvals` table.
    - WebSocket broadcasts `approval:created` to the UI.
    - Operator clicks **Approve** in the UI.
    - `POST /api/approvals/:id/decide` receives `{ "decision": "approved" }`.
    - Turn resumes, executes the commit, and tags the work product.

---

### Phase 5: Completion & State Persistence
20. **Finalization**:
    - Model produces final response summary: *"Successfully patched token expiration logic and verified unit test passes."*
    - Heartbeat records turn metrics in `heartbeat_runs` and token usage in `cost_events`.
    - Issue status transitions to `'completed'`.
    - Runtime lease is released.
    - Live Event `issue:completed` is broadcast to all connected web clients.

---

## 2. Execution Modes Comparison

| Mode | Trigger | Autonomy Level | Human Gate Required? | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Normal Chat (Board Chat)** | Operator message in UI | Reactive (1 turn) | No | Quick Q&A, brainstorming, spec clarification |
| **Model Switching** | Settings dropdown change | N/A (Config change) | No | Testing prompt performance on GPT-4o vs Claude |
| **Autonomous Agent Turn** | Heartbeat scheduler tick | Proactive (multi-turn) | Only if sensitive tool called | Background coding, documentation generation |
| **Tool Execution** | LLM `tool_use` output block | Governed by MCP policy | Yes (if write/network tool) | Reading files, executing tests, making API calls |
| **Multi-Agent Delegation** | Parent issue sub-task creation | Hierarchical delegation | Tech Lead agent reviews work | Complex architectural feature development |
