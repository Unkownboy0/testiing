# 04 — Complete System Architecture Diagrams (Mermaid)

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Visual Format**: Validated GitHub-flavored Mermaid diagrams  
> **Explanation Format**: Dual-Language (Simple Professional English + Founder-Friendly Thanglish)

---

## Diagram A: High-Level System Architecture

```mermaid
graph TB
    subgraph Clients["1. Operator Clients"]
        UI["React 19 / Vite UI (Port 3100)"]
        CLI["Geetorus CLI & companies.sh"]
        ChatBridges["Discord / Slack / Teams Webhooks"]
    end

    subgraph Server["2. Geetorus Control Plane Server"]
        Router["Express REST API (78 Route Modules)"]
        AuthMid["Auth & Company Scoping Middleware"]
        Heartbeat["Turn Scheduler & Heartbeat Daemon (heartbeat.ts)"]
        ApprovalEng["Human-in-the-Loop Approval Engine"]
        ToolGateway["MCP Tool Gateway & Action Signer"]
    end

    subgraph Execution["3. Execution & AI Layer"]
        Adapters["Model Adapters (Claude, OpenAI, Ollama, OpenRouter)"]
        Sandboxes["Local Git Worktrees / Docker / e2b Sandboxes"]
    end

    subgraph Data["4. Persistence & State"]
        Postgres[("PostgreSQL 16 / Drizzle ORM (137 Tables)")]
        Secrets[("AES Encrypted Secrets Store")]
    end

    UI -->|REST / WebSockets| Router
    CLI -->|REST API| Router
    ChatBridges -->|Webhook Events| Router

    Router --> AuthMid
    AuthMid --> Heartbeat
    Heartbeat --> ApprovalEng
    Heartbeat --> ToolGateway
    Heartbeat --> Adapters

    ToolGateway --> Sandboxes
    Router --> Postgres
    Heartbeat --> Postgres
    AuthMid --> Secrets
```

### Step-by-Step Explanation
* **English**: The Operator initiates tasks via the React UI, CLI, or Chat Bridges (Slack/Discord). Requests hit Express API routes guarded by tenant-isolation middleware. The Heartbeat Daemon schedules turns, queries the Model Adapter, routes required tools through the MCP Tool Gateway, enforces human approvals if sensitive actions are requested, and commits execution state to PostgreSQL.
* **Thanglish**: *Namma user UI-la iruntho illa CLI-la iruntho task create pannuvanga. Request direct-ah Express API-kku pogum. Anga tenant check panni, Heartbeat Runner turn start pannum. LLM-kitta kettu tool call execute panna MCP Gateway vazhiya safe sandbox-la run aagum. Crucial actions iruntha human approval ketkum. Ella data-vum 137 tables ulla PostgreSQL DB-la safe-ah save aagum.*

---

## Diagram B: Detailed Component Architecture

```mermaid
graph LR
    subgraph UI_Layer["UI Subsystem"]
        Pages["Pages (Issues, Dashboard, OrgChart)"]
        Hooks["useLiveEvents, useIssues, useApprovals"]
        Tokens["Semantic Design Tokens (ui/src/index.css)"]
    end

    subgraph Server_Core["Express Server Core"]
        App["app.ts (Express 4 App)"]
        Routes["routes/ (issues, companies, agents, tools)"]
        Services["services/ (heartbeat, budgets, watchdogs)"]
        WsServer["realtime/live-events-ws.ts"]
    end

    subgraph Adapters_Layer["AI Adapters"]
        ClaudeAd["claude-local"]
        CodexAd["codex-local"]
        OllamaAd["ollama-local"]
        OpenRouterAd["openrouter-local"]
    end

    subgraph Storage_Layer["Database Subsystem"]
        Drizzle["Drizzle ORM Engine"]
        PgRuntime["Embedded PostgreSQL / Postgres 16"]
    end

    Pages --> Hooks
    Hooks -->|Fetch & WS| App
    App --> Routes
    Routes --> Services
    Services --> WsServer
    WsServer -.->|Real-time events| Hooks
    Services --> Adapters_Layer
    Services --> Drizzle
    Drizzle --> PgRuntime
```

### Step-by-Step Explanation
* **English**: Shows the exact internal wiring: React Pages consume custom hooks connected to Express routes and the WebSocket live event stream. Server services invoke AI Adapters and persist data via Drizzle ORM.
* **Thanglish**: *Frontend pages hooks vazhiya backend API-kooda pesum. Real-time updates WebSocket live-events stream vazhiya instantly display aagum. Server services AI adapter-ah call panni result-ah Drizzle ORM moolama database-la update pannum.*

---

## Diagram C: Request Lifecycle Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Operator as Human Operator
    participant UI as React 19 Frontend
    participant API as Express Router (/api/issues)
    participant HB as Heartbeat Daemon (heartbeat.ts)
    participant LLM as AI Model Adapter (Claude/OpenAI)
    participant GW as MCP Tool Gateway
    participant DB as PostgreSQL (Drizzle)

    Operator->>UI: Submit New Issue ("Fix Auth Bug")
    UI->>API: POST /api/issues { title, companyId, priority }
    API->>DB: Insert issue record (status: 'open')
    API-->>UI: 201 Created (Issue #101)
    Note over HB: Heartbeat Poller detects runnable issue
    HB->>DB: Acquire execution lease & set status 'in_progress'
    HB->>LLM: Generate plan with system prompt + issue context
    LLM-->>HB: Tool Call Requested: "git_checkout_branch"
    HB->>GW: Dispatch tool execution intent
    GW->>GW: Check policy: Is action gated?
    alt Action is Safe (Read-only)
        GW-->>HB: Execute immediately & return stdout
    else Action requires Human Approval (Amber Gate)
        GW->>DB: Create Approval Request (status: 'pending')
        GW-->>HB: Pause turn; wait for operator decision
        HB->>UI: Emit Live Event (WS: "Approval Needed")
        Operator->>UI: Click "Approve Action"
        UI->>API: POST /api/approvals/12/decide { decision: 'approved' }
        API->>DB: Update approval record
        API->>HB: Wake up paused heartbeat turn
        HB->>GW: Resume execution in sandbox
    end

    HB->>DB: Write turn logs, token costs, and work products
    HB->>DB: Update issue status to 'completed'
    HB->>UI: Emit Live Event ("Issue Completed")
```

### Step-by-Step Explanation
* **English**: Traces a complete user request from creation through heartbeat dispatch, LLM tool generation, approval gating, sandbox execution, and final database status update.
* **Thanglish**: *Operator issue submit panna udane DB-la insert aagum. Heartbeat engine athai pick panni lease edukum. LLM tool run panna solrapo, athu dangerous action-ah iruntha 'Amber Gate' approval request create panni pause pannum. User UI-la approve pannona turn resume aagi, sandbox-la code execute panni issue complete aagum.*

---

## Diagram D: AI Model Routing Flowchart

```mermaid
flowchart TD
    Start([Task Turn Triggered]) --> CheckConfig{Check Agent Configuration}
    CheckConfig -->|Agent pins Model| UsePinned[Use Pinned Model Profile]
    CheckConfig -->|Default Routing| CheckCompanyDefault{Check Company AI Connection}

    CheckCompanyDefault -->|Anthropic Key Set| RouteClaude[Route to Claude 3.5 Sonnet]
    CheckCompanyDefault -->|OpenAI Key Set| RouteOpenAI[Route to OpenAI GPT-4o]
    CheckCompanyDefault -->|OpenRouter Key Set| RouteOpenRouter[Route to OpenRouter Gateway]
    CheckCompanyDefault -->|No Cloud Key Set| RouteOllama[Fallback to Local Ollama]

    RouteClaude --> ExecLLM[Invoke Adapter via Provider SDK]
    RouteOpenAI --> ExecLLM
    RouteOpenRouter --> ExecLLM
    RouteOllama --> ExecLLM

    ExecLLM --> CheckResponse{Response Status?}
    CheckResponse -->|Success 200| ParseTools[Parse Response & Function Calls]
    CheckResponse -->|Rate Limit 429| TriggerBackoff[Exponential Backoff & Retry]
    CheckResponse -->|Auth Error 401| RefusalError[Emit Configuration Error & Stop]
    CheckResponse -->|Timeout / Network Err| CheckFallback{Fallback Provider Configured?}

    CheckFallback -->|Yes| SwitchFallback[Switch to Secondary Provider] --> ExecLLM
    CheckFallback -->|No| FailTurn[Mark Turn Failed & Alert Operator]
```

### Step-by-Step Explanation
* **English**: Illustrates how Geetorus inspects company-level and agent-level configurations to select between Anthropic, OpenAI, OpenRouter, and local Ollama, handling rate limits with backoff and attempting fallback providers if configured.
* **Thanglish**: *Task start aagum pothu, agent config check pannum. Anthropic, OpenAI, OpenRouter or local Ollama ethu available-nu pathu route pannum. Rate limit vantha exponential backoff panni retry pannum. Fallback model iruntha athuku switch pannum.*

---

## Diagram E: Agent and Tool Execution Flowchart

```mermaid
flowchart TD
    StartTurn([Heartbeat Turn Awakens]) --> BuildPrompt[Assemble System Prompt + History + MCP Tool Schemas]
    BuildPrompt --> CallModel[Call LLM Provider]
    CallModel --> ReceiveOutput{Output Type?}
    ReceiveOutput -->|Plain Text Answer| RecordFinal[Record Final Response in Issue Thread]
    ReceiveOutput -->|Tool Call Request| CheckToolPolicy{Check Tool Access Policy}

    CheckToolPolicy -->|Policy: DENY| RejectTool[Reject Tool Call & Send Error to Agent]
    CheckToolPolicy -->|Policy: AMBER GATE| PauseApproval[Create Amber Approval & Pause Turn]
    CheckToolPolicy -->|Policy: ALLOW| VerifySigning[Verify Cryptographic Tool Signing Token]

    PauseApproval --> WaitHuman{Human Decision?}
    WaitHuman -->|Approved| VerifySigning
    WaitHuman -->|Rejected| InformAgent[Notify Agent: Action Denied by Operator] --> CallModel

    VerifySigning --> DispatchSandbox[Dispatch to Git Worktree / Sandbox]
    DispatchSandbox --> CaptureOutput[Capture stdout / stderr / diffs]
    CaptureOutput --> AppendObs[Append Observation to Context]
    AppendObs --> LoopNextTurn{More Turns or Completed?}
    LoopNextTurn -->|Continue| CallModel
    LoopNextTurn -->|Done| CloseIssue[Update Issue to Closed & Log Activity]
```

### Step-by-Step Explanation
* **English**: Shows the complete inner agent loop: prompt assembly, model reasoning, policy verification (Deny, Amber Gate, Allow), cryptographic token verification, sandbox execution, and feedback ingestion into subsequent turns.
* **Thanglish**: *Agent prompt ready panni model kitta pogum. Model tool execute panna sonna, policy check nadakum. Amber gate na human approve panra varaikum wait pannum. Verify aana apram sandbox-la run panni, output-ah thirumba agent context-ku feedback-ah anupum.*

---

## Diagram F: Data Flow Diagram

```mermaid
graph TD
    subgraph Ingestion["Input Sources"]
        UserIn["User Prompts & Issues"]
        WebhookIn["GitHub Commits & PR Events"]
        EnvIn["Environment Variables & Secrets"]
    end

    subgraph State_Storage["PostgreSQL Relational Entities"]
        CompaniesTable[("companies & company_memberships")]
        IssuesTable[("issues, issue_comments, issue_relations")]
        TurnsTable[("heartbeat_runs, turn_telemetry")]
        ApprovalsTable[("approvals & approval_comments")]
        CostsTable[("cost_events & budget_policies")]
        SecretsTable[("company_secrets (AES-256)")]
    end

    subgraph Output_Deliverables["Outputs & Side Effects"]
        GitOutput["Git Commits & Pull Requests"]
        LiveEvents["WebSocket Live Event Feeds"]
        AuditLog["Immutable Activity Log"]
    end

    UserIn --> IssuesTable
    WebhookIn --> IssuesTable
    EnvIn --> SecretsTable

    IssuesTable --> TurnsTable
    TurnsTable --> ApprovalsTable
    TurnsTable --> CostsTable
    TurnsTable --> GitOutput
    TurnsTable --> AuditLog
    TurnsTable --> LiveEvents
```

### Step-by-Step Explanation
* **English**: Demonstrates data lineage: user issues and webhook events flow into relational tables, drive heartbeat turns, record budget costs and approvals, and generate git commits and live WebSocket updates.
* **Thanglish**: *Input data issues table-ku pogum, secrets encrypted-ah store aagum. Turn execute aagura apo cost events, approvals, git commits nu ovvoru data layer-um systematically update aagum.*

---

## Diagram G: Error Handling Flowchart

```mermaid
flowchart TD
    ErrorOccurs([Error Encountered]) --> CategorizeError{Error Category?}
    CategorizeError -->|HTTP / Schema Validation| Return400[Return 400 Bad Request with Zod Error Details]
    CategorizeError -->|Authentication Failure| Return401[Return 401 Unauthorized / Tenant Mismatch]
    CategorizeError -->|LLM Provider 5xx / 429| RetryLLM[Retry with Exponential Backoff max 3 attempts]
    CategorizeError -->|Tool Execution Non-Zero Exit| ToolFail[Capture stderr as Observation; Prompt Agent to Fix]
    CategorizeError -->|Process / Watchdog Timeout| WatchdogTrigger[Task Watchdog Marks Turn Stalled; Releases Lease]
    CategorizeError -->|Embedded Postgres Lock| WinLock[Detect Lock; Instruct Operator to Kill PID]

    RetryLLM --> CheckExhausted{Retries Exhausted?}
    CheckExhausted -->|Yes| HaltTask[Mark Issue Blocked & Alert Operator via Live Events]
    CheckExhausted -->|No| RetryLLM

    ToolFail --> AgentNextTurn[Agent attempts code adjustment]
```

### Step-by-Step Explanation
* **English**: Details how the system handles validation errors, auth mismatches, LLM rate limits/outages, tool execution failures, watchdog turn timeouts, and embedded database process locks.
* **Thanglish**: *Error vantha category pathu handle pannum: Validation na 400, LLM outage na 3 times backoff retry, tool fail aana stderr-ah agent-kitteye kuduthu thirumba fix panna sollum. Stalled aana watchdog lease release panni alert pannum.*

---

## Diagram H: Deployment Architecture

```mermaid
graph TB
    subgraph DevMode["Local Development (Zero Config)"]
        LocalHost["Developer Machine (Node >= 24)"]
        LocalServer["Express API Server (Port 3100)"]
        LocalUI["Vite Dev Server (Port 5173 / 3100)"]
        EmbedPg["Embedded PostgreSQL (Port 54322 / dynamic)"]
        LocalGit["Local Git Worktrees (.geetorus/worktrees)"]
    end

    subgraph ProdMode["Production / Cloud Deployment"]
        DockerHost["Docker Container / Cloud VM"]
        ProdServer["Node.js Cluster (NODE_ENV=production)"]
        ExtPg[("External Managed PostgreSQL 16")]
        CloudSandbox["e2b / Daytona Remote Cloud Sandboxes"]
    end

    LocalHost --> LocalServer
    LocalServer --> LocalUI
    LocalServer --> EmbedPg
    LocalServer --> LocalGit

    DockerHost --> ProdServer
    ProdServer --> ExtPg
    ProdServer --> CloudSandbox
```

### Step-by-Step Explanation
* **English**: Compares the zero-configuration local development mode (using embedded PostgreSQL and local git worktrees) with the production deployment mode (using external managed PostgreSQL and cloud execution sandboxes).
* **Thanglish**: *Local-la run panna extra software ethuvum thevailla—Node.js mattum pothum, embedded Postgres thanave launch aagirum. Production-la external PostgreSQL matrum Docker/e2b cloud sandboxes use pannalam.*

---

## Diagram I: Trust Boundaries and Security Diagram

```mermaid
graph TD
    subgraph Untrusted_Zone["Untrusted Client Zone"]
        WebUser["Browser User / Mobile Client"]
        ExternalWebhooks["External Webhooks (GitHub, Discord)"]
    end

    subgraph Boundary_1["Trust Boundary 1: Perimeter"]
        AuthFirewall["CORS, TrustProxy, Auth Token Verifier"]
    end

    subgraph Controlled_Zone["Geetorus Control Plane (High Trust)"]
        CoreAPI["Express API Server"]
        ScopeCheck["Tenant / Company Isolation Barrier"]
        ActionSigner["Cryptographic HMAC Action Signer"]
        SecretsVault[("Encrypted Secrets (AES-256)")]
    end

    subgraph Boundary_2["Trust Boundary 2: Execution Gating"]
        ApprovalFirewall["Amber Approval Gatekeeper"]
    end

    subgraph Sandbox_Zone["Isolated Agent Execution Zone (Low Trust)"]
        AgentRuntime["AI Agent Model Context"]
        Worktree["Constrained Git Sandbox / Workspace"]
    end

    WebUser -->|HTTPS Bearer Token| Boundary_1
    ExternalWebhooks -->|Webhook Signature| Boundary_1
    Boundary_1 --> CoreAPI

    CoreAPI --> ScopeCheck
    ScopeCheck --> ActionSigner
    ActionSigner --> Boundary_2
    Boundary_2 -->|Gated Approval Passed| AgentRuntime
    AgentRuntime --> Worktree
    CoreAPI -.-> SecretsVault
```

### Step-by-Step Explanation
* **English**: Highlights the dual security perimeters: Perimeter 1 validates incoming HTTP traffic, tokens, and company multi-tenancy. Perimeter 2 sits between the AI Agent reasoning engine and actual code execution, preventing untrusted LLM outputs from running arbitrary commands without cryptographic signing and human approval.
* **Thanglish**: *Rendu security walls iruku: First wall incoming user tokens and company access-ah check pannum. Second wall AI agent-kum execute aagura code-kum naduvula iruku. Agent ethavathu dangerous command pota, human approval illama run panna mudiyathu.*
