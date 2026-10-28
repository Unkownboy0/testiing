# Geetorus — API Overview & Protocols

## 1. Overview

The Geetorus API is a RESTful and event-driven HTTP service exposing 78 distinct route spines under the `/api` namespace. All API requests and responses utilize standard `application/json` payloads, while real-time task sessions and activity feeds stream via Server-Sent Events (`text/event-stream`).

---

## 2. Global Request Headers

| Header Name | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `Authorization` | `string` | Yes | Bearer token (`Bearer <session_token>` or `Bearer <api_key>`). |
| `X-Geetorus-Company-Id` | `string` | Conditional | UUID of the active target virtual company. Required when not in path. |
| `Content-Type` | `string` | Yes | Must be `application/json` for POST, PUT, and PATCH operations. |
| `Accept` | `string` | Yes | `application/json` or `text/event-stream` for live SSE endpoints. |

---

## 3. Protocol Architecture

```
+-----------------------------------------------------------------------------------+
|                              GEETORUS API LAYER                                   |
+-----------------------------------------------------------------------------------+
|  [REST / JSON]                                      [SSE / text/event-stream]     |
|  • /api/companies (CRUD)                            • /api/issues/:id/live        |
|  • /api/issues (Task State Machine)                 • /api/activity/stream        |
|  • /api/agents (Roster & Config)                    • /api/heartbeats/live        |
|  • /api/tool-gateway (MCP Invocations)              • /api/chat-channels/live     |
|  • /api/secrets (Encrypted Vault)                                                 |
|  • /api/approvals (Human-in-the-loop Gates)                                       |
+-----------------------------------------------------------------------------------+
```
