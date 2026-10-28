# 26 — Repository and Dependency Map

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Verified from `package.json`, `pnpm-workspace.yaml`, and ecosystem repository structures.

---

## 1. Ecosystem Repository Mapping

The Geetorus ecosystem is composed of five interrelated repositories within the workspace:

```
c:/Users/mohamed farhan/testing-marketing/
│
├── geetorusai/                     # [CORE MONOREPO]
│   ├── cli/                        # Unified CLI command suite
│   ├── packages/db/                # Drizzle ORM schemas & embedded Postgres runtime
│   ├── packages/shared/            # Shared interfaces, Zod schemas, constants
│   ├── packages/adapters/          # 13 Model adapters (Claude, Codex, Ollama, etc.)
│   ├── packages/mcp-server/        # Embedded Model Context Protocol server
│   ├── server/                     # Express.js REST API & heartbeat daemon
│   └── ui/                         # React 19 + Vite frontend control plane
│
├── companies-tool/                 # [PACKAGING & PORTABILITY CLI]
│   └── src/index.ts                # `companies.sh` CLI for exporting/importing company blueprints
│
├── geetorus-companies/             # [TURNKEY BLUEPRINT LIBRARY]
│   ├── fullstack-forge/            # General software engineering department
│   ├── trail-of-bits-security/     # Security audit & vulnerability triage team
│   ├── clawteam-engineering/       # Systems & high-velocity backend team
│   └── ... (17 total companies)    # Specialized company blueprints
│
├── geetorus-market/                # [COMMUNITY MARKETPLACE]
│   └── src/app/                    # Next.js 15 web app for sharing & importing company templates
│
└── geetorus-docs-docusaurus/       # [PUBLIC DOCUMENTATION]
    └── docs/                       # External community documentation website
```

---

## 2. Key Production Dependencies & Rationale

| Dependency | Version / Package | Primary Consumer | Technical Rationale |
| :--- | :--- | :--- | :--- |
| **Node.js** | `>= 24.11.0` | Global Runtime | Native WebSocket client, stable fetch, modern crypto APIs. |
| **pnpm** | `9.15.4` | Package Manager | Fast, deterministic workspace symlinks with patched dependencies support. |
| **Express** | `4.21.x` | `server/` | Lightweight, un-opinionated HTTP router supporting long-lived WebSockets. |
| **Drizzle ORM** | `^0.39.x` | `packages/db/` | Ultra-fast compile-time type-safe SQL query generation with zero runtime schema overhead. |
| **React** | `^19.2.8` | `ui/` | Concurrent rendering, latest server action hooks, optimal reactivity. |
| **Vite** | `^6.x` | `ui/` | Sub-millisecond HMR compilation during frontend development. |
| **TanStack Query**| `^5.x` | `ui/` | Declarative server-state caching, background re-fetching, mutation tracking. |
| **Commander.js** | `^12.x` | `cli/` | Clean command-line parsing for the unified `geetorusai` CLI. |
| **ws** | `^8.x` | `server/` | High-throughput WebSocket server handling real-time live events. |

---

## 3. Patched Dependencies Inventory (`patches/`)

Geetorus applies custom patches to third-party dependencies to ensure enterprise stability and Windows compatibility:

1. **`embedded-postgres@18.1.0-beta.16.patch`**:
   - Patches process spawning and signal handling to minimize orphan processes on Windows.
2. **`acpx@0.12.0.patch` & `acpx@0.13.1.patch`**:
   - Patches Agent Client Protocol bindings for enhanced session resumption.
3. **`@agentclientprotocol/claude-agent-acp` & `codex-acp`**:
   - Overrides default model versions and normalizes token usage reporting.
4. **`@chat-adapter/*` (Slack, Discord, Telegram, Teams, GitHub)**:
   - Patches webhook signature verification and reaction receipt handling.
