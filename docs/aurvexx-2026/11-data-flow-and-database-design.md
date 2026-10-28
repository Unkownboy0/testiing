# 11 — Data Flow, Persistence, and Database Design

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Codebase audit of `geetorusai/packages/db/src/schema/*.ts` (137 tables) and Drizzle ORM models.

---

## 1. Database Architecture & Technology

Geetorus uses **PostgreSQL 16+** as its single source of truth, managed through **Drizzle ORM** (`packages/db`). 

* **ORM Layer**: Type-safe schema definitions across 137 schema files in `packages/db/src/schema/`.
* **Zero-Config Local Runtime**: Uses `embedded-postgres@18.1.0-beta.16` (patched binary in `patches/`) which automatically starts a local PostgreSQL cluster inside the project directory if no external `DATABASE_URL` is provided.
* **Migration Runtime**: Migrations are version-controlled under `packages/db/drizzle/` and applied automatically during server startup via `migration-runtime.ts`.

---

## 2. Core Relational Entities & ER Schema

```
+---------------------------------------------------------------------------------------------------+
|                                 CORE RELATIONAL DOMAIN ENTITIES                                   |
|                                                                                                   |
|    +-------------------+           +-------------------+           +-------------------+          |
|    |     companies     | 1       * |      agents       | 1       * |   agent_task_     |          |
|    |-------------------|──────────▶|-------------------|──────────▶|     sessions      |          |
|    | id (PK)           |           | id (PK)           |           |-------------------|          |
|    | name              |           | company_id (FK)   |           | id (PK)           |          |
|    | created_at        |           | role              |           | agent_id (FK)     |          |
|    +---------┬---------+           +---------┬---------+           +-------------------+          |
|              │ 1                             │ 1                                                  |
|              │                               │                                                    |
|              ▼ *                             ▼ *                                                  |
|    +-------------------+           +-------------------+           +-------------------+          |
|    |      issues       | 1       * |  heartbeat_runs   | 1       * |     approvals     |          |
|    |-------------------|──────────▶|-------------------|──────────▶|-------------------|          |
|    | id (PK)           |           | id (PK)           |           | id (PK)           |          |
|    | company_id (FK)   |           | issue_id (FK)     |           | run_id (FK)       |          |
|    | title             |           | agent_id (FK)     |           | status            |          |
|    | status            |           | prompt_tokens     |           | action_payload    |          |
|    | assignee_agent_id |           | cost_usd          |           +-------------------+          |
|    +---------┬---------+           +-------------------+                                          |
|              │ 1                                                                                  |
|              ▼ *                                                                                  |
|    +-------------------+           +-------------------+                                          |
|    |  issue_relations  |           |    cost_events    |                                          |
|    |-------------------|           |-------------------|                                          |
|    | parent_issue_id   |           | company_id (FK)   |                                          |
|    | child_issue_id    |           | issue_id (FK)     |                                          |
|    | relation_type     |           | amount_usd        |                                          |
|    +-------------------+           +-------------------+                                          |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Key Schema Groupings & Responsibilities

### 3.1. Company & Tenancy
* **`companies.ts`**: The top-level tenant entity representing an enterprise or virtual team.
* **`company_memberships.ts`**: Maps human user identities to roles (`owner`, `admin`, `operator`, `viewer`).
* **`company_secrets.ts` & `company_secret_versions.ts`**: Stores encrypted API keys and service tokens with version tracking.

### 3.2. Tasks, Issues & Tree Decomposition
* **`issues.ts`**: Core task table (`id`, `title`, `description`, `status`, `priority`, `assignee_agent_id`).
* **`issue_relations.ts`**: Represents hierarchical decomposition (`parent_child`, `blocks`, `relates_to`).
* **`issue_comments.ts`**: Chronological discussion messages, prompt notes, and operator instructions.
* **`issue_work_products.ts`**: Tracks deliverables produced by agents (git commits, diffs, PR links, generated documents).

### 3.3. Execution Turns & Telemetry
* **`heartbeat_runs.ts`**: Records each execution turn of an agent, turn duration, prompt/completion token count, and final status (`succeeded`, `failed`, `amber_gate`).
* **`execution_workspace_runtime_leases.ts`**: Enforces mutually exclusive access locks on workspaces during turn execution to prevent race conditions.
* **`task_watchdogs.ts`**: Tracks timeout thresholds and stall states for long-running turns.

### 3.4. Safety, Budgets & Governance
* **`approvals.ts` & `approval_comments.ts`**: Records gated actions requiring human sign-off, operator verdict, and reason.
* **`budget_policies.ts`**: Maximum token and dollar limits defined per company or per task.
* **`cost_events.ts`**: Immutable ledger of token expenditures across OpenAI, Anthropic, and other providers.
* **`activity_log.ts`**: Append-only audit log tracking every user login, agent action, approval verdict, and secret rotation.

---

## 4. Privacy & Data Sent to External LLMs

* **What leaves the server**: System instructions, sanitized issue description, relevant file context, and tool schemas.
* **What NEVER leaves the server**:
  - `GEETORUS_SECRET_KEY` and encrypted database values.
  - Raw database credentials.
  - Secret keys belonging to other companies (guaranteed by company scoping).
  - Redacted environment secrets (filtered by `log-redaction.ts` and `run-secret-redaction.ts`).
