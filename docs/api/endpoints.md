# Geetorus — API Endpoints Reference

This reference catalogs the primary REST and SSE endpoints implemented across the 78 route modules in `server/src/routes/`.

---

## 1. Companies & Organizations (`/api/companies`)

| Method | Endpoint | Description | Request Body / Parameters | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/companies` | List all companies accessible to the authenticated user. | None | `Array<Company>` |
| `POST` | `/api/companies` | Create a new virtual company. | `{ name: string, budgetLimitDaily: number, currency: string }` | `Company` (201 Created) |
| `GET` | `/api/companies/:id` | Get details of a specific company. | `id: UUID` | `Company & { stats }` |
| `PATCH` | `/api/companies/:id` | Update company settings, budget caps, or name. | `{ name?: string, budgetLimitDaily?: number }` | `Company` |
| `DELETE` | `/api/companies/:id` | Soft-delete / archive a company. | `id: UUID` | `{ success: true }` |
| `POST` | `/api/companies/:id/onboard` | Seed company with pre-packaged template. | `{ templateName: string }` | `{ seededAgents: number, seededTools: number }` |

---

## 2. Tasks & Issues State Machine (`/api/issues`)

| Method | Endpoint | Description | Request Body / Parameters | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/issues` | Query tasks with filtering by status, assignee, priority. | `?companyId=...&status=...&assigneeId=...` | `Array<Issue>` |
| `POST` | `/api/issues` | Create a new task in the backlog or active sprint. | `{ companyId: UUID, title: string, description: string, assigneeId?: UUID, priority?: string }` | `Issue` (201 Created) |
| `GET` | `/api/issues/:id` | Get full task details including session turns and artifacts. | `id: UUID` | `IssueDetail & { workProducts: [], comments: [] }` |
| `PATCH` | `/api/issues/:id` | Transition task state or reassign agent. | `{ status?: 'todo'|'in_progress'|'in_review'|'done'|'blocked', assigneeId?: UUID }` | `Issue` |
| `GET` | `/api/issues/:id/live` | **SSE Stream**: Real-time turn chunks, logs, and tool calls. | `id: UUID` (Accept: `text/event-stream`) | `SSE Stream` |
| `POST` | `/api/issues/:id/pause` | Manually pause an active task execution. | `None` | `{ paused: true }` |
| `POST` | `/api/issues/:id/resume` | Resume a paused task execution. | `None` | `{ resumed: true }` |

---

## 3. Agents & Roster Management (`/api/agents`)

| Method | Endpoint | Description | Request Body / Parameters | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/agents` | List all agent profiles in the company. | `?companyId=UUID` | `Array<Agent>` |
| `POST` | `/api/agents` | Register a new autonomous agent worker. | `{ companyId: UUID, name: string, role: string, systemPrompt: string, modelProvider: string, modelName: string }` | `Agent` (201 Created) |
| `GET` | `/api/agents/:id` | Get agent configuration, assigned tools, and budget status. | `id: UUID` | `AgentDetail` |
| `PATCH` | `/api/agents/:id` | Update agent system instructions, model, or tool bindings. | `{ systemPrompt?: string, modelName?: string }` | `Agent` |
| `POST` | `/api/agents/:id/wakeup` | Trigger an immediate out-of-band heartbeat wakeup. | `{ reason: string }` | `{ wakeupQueued: true }` |

---

## 4. MCP Tools & Governed Gateway (`/api/tool-gateway` & `/api/tool-access`)

| Method | Endpoint | Description | Request Body / Parameters | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/tool-access` | List registered MCP servers and available tools. | `?companyId=UUID` | `Array<ToolDefinition>` |
| `POST` | `/api/tool-access` | Register a new MCP server (stdio or SSE). | `{ companyId: UUID, name: string, transport: 'stdio'|'sse', command?: string, url?: string }` | `ToolServer` (201 Created) |
| `POST` | `/api/tool-gateway/invoke` | Execute a governed tool action. | `{ agentId: UUID, taskId: UUID, toolName: string, arguments: object }` | `{ status: 'completed'|'approval_required', result?: object }` |

---

## 5. Approvals & Human Gates (`/api/approvals`)

| Method | Endpoint | Description | Request Body / Parameters | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/approvals` | List pending approval requests. | `?companyId=UUID&status=pending` | `Array<ApprovalRequest>` |
| `POST` | `/api/approvals/:id/decision` | Submit human approval or rejection decision. | `{ decision: 'approved'|'rejected', feedback?: string }` | `ApprovalRequest` |

---

## 6. Secrets Vault (`/api/secrets`)

| Method | Endpoint | Description | Request Body / Parameters | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/secrets` | List company secret keys (values masked). | `?companyId=UUID` | `Array<{ id, name, createdAt }>` |
| `POST` | `/api/secrets` | Store or update an encrypted secret. | `{ companyId: UUID, name: string, value: string }` | `{ id: UUID, name: string }` |
| `POST` | `/api/secrets/bind` | Bind a secret to an agent with access rules. | `{ secretId: UUID, agentId: UUID }` | `{ bound: true }` |

---

## 7. Health & System Diagnostics (`/api/health`)

| Method | Endpoint | Description | Request Body / Parameters | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Comprehensive system health check (DB, memory, runners). | None | `{ status: 'ok', uptime: number, db: 'healthy', version: string }` |
