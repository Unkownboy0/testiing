# 10 — API and External Integration Reference

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Codebase audit of `server/src/routes/*.ts` (78 routes) and `server/src/app.ts`.

---

## 1. API Architecture & Standards

Geetorus exposes a RESTful JSON API alongside WebSocket streams under the `/api/` path prefix on port `3100`:

* **Protocol**: HTTP/1.1 and WebSockets (`ws://`).
* **Authentication**: Bearer tokens via `Authorization: Bearer <session-token | api-key>`.
* **Multi-Tenancy**: Tenant context supplied via `x-company-id` header or embedded URL slug.
* **Payload Format**: Standard JSON (`Content-Type: application/json`).
* **Error Envelope**:
  ```json
  {
    "error": {
      "code": "VALIDATION_FAILED",
      "message": "Invalid issue priority: must be low, medium, or high",
      "details": [ ... ]
    }
  }
  ```

---

## 2. Core Endpoint Reference

### 2.1. Company Management (`server/src/routes/companies.ts`)

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/companies` | Yes | List all Virtual Companies accessible to the authenticated actor. |
| `POST` | `/api/companies` | Yes (Admin) | Create a new Virtual Company with initial budget caps and settings. |
| `GET` | `/api/companies/:id` | Yes | Retrieve company details, active members, and budget allocations. |
| `GET` | `/api/companies/:id/org-chart` | Yes | Generate SVG and hierarchical tree of agents and reporting lines. |

---

### 2.2. Issue & Task Management (`server/src/routes/issues.ts`)

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/issues` | Yes | List issues with optional filters (`companyId`, `status`, `assignee`). |
| `POST` | `/api/issues` | Yes | Create a new engineering task or bug report. |
| `GET` | `/api/issues/:id` | Yes | Retrieve full issue thread, comments, attachments, and turn history. |
| `PATCH` | `/api/issues/:id` | Yes | Update issue priority, status, or reassign to another agent. |
| `POST` | `/api/issues/:id/comments` | Yes | Post a comment or operator instruction into the issue thread. |

---

### 2.3. Agent Profiles (`server/src/routes/agents.ts`)

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/agents` | Yes | List configured AI agents, roles, and status within a company. |
| `POST` | `/api/agents` | Yes (Admin) | Create an agent profile with role instructions and tool allowlists. |
| `GET` | `/api/agents/:id/runtime-state` | Yes | Inspect agent's active execution lease and memory context. |

---

### 2.4. Human Approvals (`server/src/routes/approvals.ts`)

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/approvals` | Yes | List pending amber approval requests across all tasks. |
| `POST` | `/api/approvals/:id/decide` | Yes | Submit operator verdict: `approved` or `rejected` with comments. |

---

### 2.5. Real-Time WebSockets (`server/src/realtime/live-events-ws.ts`)

* **Endpoint**: `ws://localhost:3100/api/live-events`
* **Handshake**: Requires query param `?token=<session_token>` or cookie header.
* **Event Payloads**:
  ```json
  {
    "type": "issue:updated",
    "companyId": "cmp_101",
    "payload": { "id": "iss_55", "status": "in_progress", "activeTurn": 3 }
  }
  ```

---

### 2.6. Health & Diagnostics (`server/src/routes/health.ts`)

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | **Public** | Returns `{ "status": "ok", "version": "1.0.0", "database": "connected" }`. |
| `GET` | `/api/health/db` | **Public** | Detailed status of PostgreSQL connection pool and pending migrations. |

---

## 3. External Webhook Integrations

1. **GitHub Webhooks** (`server/src/routes/chat-channels.ts`):
   - Receives `push`, `pull_request`, and `issues` events. Automatically links commits to Geetorus issue records via `#ISS-123` mention regex parser (`issue-references.ts`).
2. **Discord / Slack / Teams Adapters**:
   - Bi-directional chat bots that post approval notifications and allow operators to click "Approve" directly from team chat channels.
