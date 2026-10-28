# Geetorus — Data Flow & Event Lifecycle

This document traces the complete end-to-end data flow from user interaction to agent turn execution, tool invocation, and outcome verification.

---

## 1. End-to-End Task Execution Flow

```mermaid
sequenceDiagram
    autonumber
    actor Operator as Human Operator
    participant UI as React UI (SPA)
    participant API as Express Server
    participant DB as PostgreSQL (Drizzle)
    participant Orchestrator as Heartbeat & Task Engine
    participant LLM as AI Model Provider
    participant Sandbox as Execution Workspace / Sandbox
    participant MCP as MCP Tool Gateway

    Operator->>UI: Submits new Task: "Refactor Auth Middleware"
    UI->>API: POST /api/issues { companyId, title, assigneeId, requirements }
    API->>DB: INSERT into issues (status = 'todo')
    API->>DB: INSERT into activity_log (action = 'issue_created')
    API-->>UI: 201 Created (Issue Record)

    Note over Orchestrator: Heartbeat Loop detects active todo task
    Orchestrator->>DB: UPDATE issues SET status = 'in_progress'
    Orchestrator->>DB: INSERT into heartbeat_runs (status = 'running')
    Orchestrator->>DB: Resolves authorized secrets & tool bindings

    Orchestrator->>LLM: Dispatches Prompt + System Instructions + Available Tools
    LLM-->>Orchestrator: Streaming LLM Response (Reasoning + Tool Call: run_shell)
    Orchestrator->>API: SSE Stream: emits turn chunk to active UI sessions

    alt Tool requires Human Approval
        Orchestrator->>DB: INSERT into approvals (status = 'pending')
        Orchestrator->>API: SSE Stream: emits approval_required event
        API-->>UI: Displays Amber Approval Takeover
        Operator->>UI: Clicks "Approve"
        UI->>API: POST /api/approvals/:id/decision { decision: 'approved' }
        API->>DB: UPDATE approvals SET status = 'approved'
        API->>Orchestrator: Resumes tool execution
    end

    Orchestrator->>Sandbox: Executes shell command inside isolated workspace
    Sandbox-->>Orchestrator: Command Output (stdout, exitCode = 0)
    Orchestrator->>DB: INSERT into issue_work_products (diff, artifacts)

    Orchestrator->>LLM: Sends tool result back to model
    LLM-->>Orchestrator: Final Turn Message: "Refactoring completed and verified"
    
    Orchestrator->>DB: UPDATE issues SET status = 'in_review' / 'done'
    Orchestrator->>DB: UPDATE heartbeat_runs SET status = 'completed', cost_events logged
    Orchestrator->>API: SSE Stream: task_completed event
    API-->>UI: Updates Task Card to Done with Work Product links
```

---

## 2. Event Dispatch & Real-Time Streaming

Geetorus employs **Server-Sent Events (SSE)** for zero-overhead, real-time streaming from the server to connected UI clients:

- `/api/issues/:id/live`: Streams raw turn-by-turn thinking blocks, tool invocations, and command stdout.
- `/api/activity/stream`: Global tenant-wide activity stream for live operator situational awareness.
- `/api/heartbeats/live`: Live heartbeat state indicators across all agents in the virtual company.
