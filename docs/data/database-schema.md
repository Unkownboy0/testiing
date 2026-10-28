# Geetorus — Database Schema & Data Models

## 1. Relational Topology & Technology Stack

Geetorus utilizes **PostgreSQL 16+** managed via **Drizzle ORM** (`@geetorusai/db`). The database schema consists of **137 modular table definitions** providing comprehensive domain modeling across companies, agents, tasks, tool governance, encrypted secrets, and financial billing.

```
                           +----------------------+
                           |      companies       |
                           +----------------------+
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
+-----------------+          +-----------------+          +-----------------+
|     agents      |          |     issues      |          | company_secrets |
+-----------------+          +-----------------+          +-----------------+
         │                            │                            │
         ▼                            ▼                            ▼
+-----------------+          +-----------------+          +-----------------+
| heartbeat_runs  |          | issue_comments  |          | secret_bindings |
+-----------------+          +-----------------+          +-----------------+
         │                            │
         ▼                            ▼
+-----------------+          +-----------------+
|   cost_events   |          | issue_approvals |
+-----------------+          +-----------------+
```

---

## 2. Core Domain Table Clusters

### Cluster A: Organizations & Multi-Tenancy
- `companies`: Primary tenant record (UUID, name, daily budget limit, currency, timestamps).
- `company_memberships`: Human user roles within each virtual company.
- `company_onboarding_seeds`: Track templates applied during initialization.

### Cluster B: Agents & Execution State
- `agents`: Agent profiles, system prompts, role titles, and supervisor hierarchy.
- `heartbeat_runs`: Execution turns, assigned models, token counts, and durations.
- `agent_runtime_state`: Active leases, memory checkpoints, and execution health.
- `agent_wakeup_requests`: Asynchronous wakeup events queued for next heartbeat.

### Cluster C: Tasks & Task State Machine
- `issues`: Hierarchical tasks (`backlog`, `todo`, `in_progress`, `in_review`, `done`, `blocked`).
- `issue_tree_holds`: Recursive dependency holds across parent/child tasks.
- `issue_work_products`: Generated pull requests, documents, and diff artifacts.
- `issue_watchdogs`: Stall monitoring records and recovery intervention logs.

### Cluster D: Governed Tools & Secrets
- `tool_access`: MCP tool registrations, transport types (`stdio`/`sse`), and schemas.
- `company_secrets`: Encrypted secret records and version histories.
- `company_secret_bindings`: Least-privilege bindings between agents and specific secrets.
- `approvals`: Human-in-the-loop sign-off requests and decisions.

### Cluster E: Finance & Audit
- `cost_events`: Fine-grained token usage and dollar expenses per turn.
- `budget_policies`: Company-level and agent-level financial constraints.
- `activity_log`: Tamper-evident ledger of all system, user, and agent actions.
