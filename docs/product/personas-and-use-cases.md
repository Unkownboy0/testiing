# Geetorus — Personas, Workflows & Use Cases

## 1. User Personas

### Persona A: The AI-First Technical Founder (Alex)
- **Profile**: Solo founder or technical co-founder building a high-velocity SaaS startup.
- **Goals**: Wants a full engineering team (Backend Engineer, Frontend Engineer, QA Reviewer, DevOps) running autonomously on backlog issues.
- **Needs in Geetorus**:
  - Out-of-the-box company templates (`fullstack-forge`, `clawteam-engineering`).
  - Budget caps ($50/day hard stop) to protect runway.
  - Automatic PR creation and branch management in GitHub.
  - Interactive web UI to inspect agent diffs, approve merges, and unblock stalled agents.

### Persona B: The Engineering Manager / Platform Lead (Priya)
- **Profile**: Manages a team of 15 human engineers at a mid-market tech company.
- **Goals**: Automate maintenance, dependency updates, test flakiness fixes, and security patch reviews without context-switching human engineers.
- **Needs in Geetorus**:
  - Scheduled routines running nightly.
  - Sandboxed execution environments (e2b, Daytona) to ensure agent builds do not touch production infrastructure.
  - Granular MCP tool permissions (read-only git access for junior agents; write access gated by human approval).
  - Multi-user authentication with role-based access control.

### Persona C: The Digital Agency Operator (Marcus)
- **Profile**: Operates an AI-driven digital marketing and content agency serving 20+ clients.
- **Goals**: Maintain isolated virtual companies per client, equipped with client-specific brand voices, social media tools, and analytics MCP connections.
- **Needs in Geetorus**:
  - Multi-tenancy with strict company isolation in PostgreSQL.
  - CLI import/export via `companies.sh` to replicate proven agency team topologies across client workspaces.
  - Client-scoped secret management and budget allocations.

---

## 2. Core User Journeys & Workflows

### Journey 1: Company Initialization & Agent Onboarding
```mermaid
sequenceDiagram
    autonumber
    actor User as Human Operator
    participant UI as Geetorus UI / CLI
    participant Server as Geetorus API Server
    participant DB as PostgreSQL DB
    participant Engine as Agent Runtime

    User->>UI: Selects "Create Company" or imports template (e.g., fullstack-forge)
    UI->>Server: POST /api/companies (Name, Budget, Agent definitions)
    Server->>DB: Persists Company, Agents, Roles & Default Budget Policy
    Server->>Engine: Seeds Default Skills & MCP Tool Bindings
    Server-->>UI: Returns Company Dashboard with Org Chart
    User->>UI: Views interactive hierarchy (Lead Agent, Frontend, Backend, QA)
```

### Journey 2: Task Execution, Delegation & Human Approval
```mermaid
sequenceDiagram
    autonumber
    actor User as Human Operator
    participant UI as Geetorus UI (Task Board)
    participant Server as Geetorus Server
    participant Lead as Lead Architect Agent
    participant Worker as Worker Agent (Backend)
    participant Watchdog as Watchdog & Budget Engine

    User->>UI: Submits new Task: "Implement OAuth2 Google Login"
    UI->>Server: POST /api/issues (Title, Requirements, Target Project)
    Server->>Lead: Triggers Task Session via Heartbeat Run
    Lead->>Lead: Decomposes task into sub-tasks (Plan Decomposition)
    Lead->>Server: Assigns sub-task #102 to Worker Agent
    Server->>Worker: Dispatches task session turn with execution workspace
    Worker->>Server: Requests high-risk tool call: "Execute database migration"
    Server->>Watchdog: Evaluates tool access policy -> Requires Approval
    Server->>UI: Emits Awaiting-Approval Event (SSE)
    UI->>User: Displays amber Takeover Modal with migration SQL diff
    User->>UI: Clicks "Approve Action"
    UI->>Server: POST /api/issues/:id/approvals
    Server->>Worker: Resumes tool execution & completes sub-task
    Worker->>Server: Emits Completion Contract & PR Artifact
    Server->>UI: Updates Task to "Completed" with green status badge
```

### Journey 3: Self-Healing & Automatic Run Recovery
```mermaid
flowchart TD
    A[Agent Task Session Starts] --> B[Execute Model Inference & Tool Call]
    B --> C{Execution Status?}
    C -->|Success| D[Verify Completion Contract]
    C -->|API Timeout / Rate Limit| E[Watchdog Detects Stall]
    C -->|Invalid Tool Output| F[Agent Turn Error]
    
    E --> G{Retry Policy Available?}
    F --> G
    
    G -->|Yes (Retries < Max)| H[Dispatch Recovery Action / Safe Turn Restart]
    H --> B
    
    G -->|No (Exceeded)| I[Transition Task to 'Blocked']
    I --> J[Post Diagnostic Summary to Task Feed]
    J --> K[Notify Operator for Intervention]
    
    D -->|Passed| L[Task Marked Completed]
    D -->|Failed Criteria| M[Re-queue with Feedback Injection]
    M --> B
```
