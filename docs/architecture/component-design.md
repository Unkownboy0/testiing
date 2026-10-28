# Geetorus — Component Design & Subsystem Specifications

## 1. Server Subsystem (`@geetorusai/server`)

The server is built with Express.js running on Node.js 24+ ES Modules. It manages HTTP REST routes, SSE streaming pipelines, background heartbeat loops, and execution workspaces.

```
server/src/
├── index.ts                   # Main server bootstrap & inline route spine
├── routes/                    # 78 domain-specific API route handlers
│   ├── companies.ts           # Company CRUD, onboarding seeds, invites
│   ├── issues.ts              # Core task state machine & comments
│   ├── agents.ts              # Agent roster, heartbeats, runtime state
│   ├── tool-gateway.ts        # MCP tool connection & routing
│   ├── secrets.ts             # Encrypted secret management & proposals
│   ├── environments.ts        # Sandboxes (Docker, Daytona, e2b, Modal)
│   ├── approvals.ts           # Human-in-the-loop sign-off workflows
│   └── openapi.ts             # Automated OpenAPI specification generator
├── services/
│   ├── native-runtime/       # Local process execution, turns & watchdogs
│   ├── sandbox/              # Cloud sandbox provider adapters
│   └── watchdog/             # Run stall detection & auto-recovery
└── middleware/
    ├── auth.ts                # Session token & API key verification
    ├── company-scope.ts       # Tenant boundary verification
    └── error-handler.ts       # Standardized JSON error response formatter
```

---

## 2. Frontend Subsystem (`@geetorusai/ui`)

The UI is a high-performance Single Page Application (SPA) built with React 19, Vite, and Radix UI headless components, styled strictly with Tailwind CSS v4 design tokens.

```
ui/src/
├── pages/                     # Routed view views
│   ├── CompaniesPage.tsx      # Multi-company dashboard & switchers
│   ├── IssuesPage.tsx         # Task Kanban board & tree view
│   ├── AgentsPage.tsx         # Org Chart & Agent detail inspectors
│   ├── ToolsPage.tsx          # MCP Gateway management & permissions
│   ├── SecretsPage.tsx        # Encrypted vault & agent binding rules
│   └── ActivityPage.tsx       # Immutable activity ledger
├── components/                # Modular UI components
│   ├── ui/                    # Primitive design token components (Button, Card, Dialog)
│   ├── OnboardingWizard.tsx   # Step-by-step company initialization
│   ├── TaskChat/              # Real-time streaming turn inspector
│   └── OrgChart/              # Interactive SVG agent organizational hierarchy
├── index.css                  # SINGLE SOURCE OF TRUTH for design tokens
└── main.tsx                   # React app entry point & router setup
```

---

## 3. Database Subsystem (`@geetorusai/db`)

Built with Drizzle ORM, providing end-to-end type safety between database tables, API routes, and frontend state.

- **Schema Definitions**: 137 separate schema files under `packages/db/src/schema/`.
- **Core Entities**:
  - `companies`: Primary multi-tenant root entity.
  - `agents`: Autonomous virtual worker records, system prompts, assigned roles.
  - `issues`: Hierarchical tasks, states, assignments, and budget allocations.
  - `heartbeat_runs`: Execution turns, LLM provider metadata, token consumption.
  - `company_secrets`: Encrypted secrets, key versions, and agent access rules.
  - `tool_access`: MCP tool registrations, permissions, and execution delivery logs.
  - `activity_log`: Tamper-evident audit records of all human and agent operations.
