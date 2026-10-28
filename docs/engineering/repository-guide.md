# Geetorus — Repository Guide & Codebase Map

## 1. Monorepo Directory Structure

```
c:\Users\mohamed farhan\testing-marketing\
├── geetorusai/                      # Core control plane monorepo
│   ├── cli/                         # geetorusai command-line tool
│   ├── packages/                    # Shared workspace packages
│   │   ├── db/                      # Drizzle ORM schemas & embedded Postgres
│   │   ├── shared/                  # TypeScript types, constants, validators
│   │   ├── adapters/                # LLM provider clients (Anthropic, OpenAI)
│   │   ├── plugins/                 # Extensible plugin system
│   │   ├── adapter-utils/           # Streaming & token calculation helpers
│   │   ├── mcp-server/              # Embedded Model Context Protocol server
│   │   ├── skills-catalog/          # Skill manifests and schemas
│   │   └── geetorus-eval-kernel/    # Evaluation harness
│   ├── server/                      # Express REST API & Orchestration Engine
│   │   ├── src/index.ts             # Main entry point & inline routes
│   │   ├── src/routes/              # 78 domain-specific route files
│   │   └── src/services/            # Native runtime, sandboxes, watchdogs
│   ├── ui/                          # React 19 + Vite frontend
│   │   ├── src/pages/               # Routed views (Tasks, Org Chart, Secrets)
│   │   ├── src/components/          # Reusable design token components
│   │   ├── src/index.css            # Single source of visual tokens
│   │   └── storybook/               # Component visual baseline stories
│   ├── scripts/                     # Dev runner, build, token gate scripts
│   ├── tests/                       # E2E (Playwright) & Acceptance test suites
│   ├── DESIGN.md                    # Canonical design token governance
│   ├── ROADMAP.md                   # Platform milestones & future features
│   └── package.json                 # Monorepo root scripts & dev dependencies
├── companies-tool/                  # companies.sh CLI for org packaging
├── geetorus-companies/              # 17 pre-packaged company templates
├── geetorus-docs/                   # Cloudflare Worker markdown docs renderer
├── geetorus-docs-docusaurus/        # Docusaurus documentation website
└── geetorus-market/                 # Next.js 15 template marketplace web app
```

---

## 2. Key Monorepo Entry Points

| Subsystem | Primary Entry Point | Purpose |
| :--- | :--- | :--- |
| **API Server** | `geetorusai/server/src/index.ts` | Bootstraps Express server, middleware, routes, and background runners. |
| **Frontend UI** | `geetorusai/ui/src/main.tsx` | Initializes React DOM, router context, and design token theme provider. |
| **Database Schema** | `geetorusai/packages/db/src/schema/index.ts` | Exports all 137 Drizzle ORM table models and relational queries. |
| **CLI Tool** | `geetorusai/cli/src/index.ts` | Headless CLI for company orchestration and task dispatches. |
| **Companies CLI** | `companies-tool/src/index.ts` | Command-line tool for importing and exporting company templates. |
| **Dev Runner** | `geetorusai/scripts/dev-runner.ts` | Orchestrates dual-process watch execution of server and UI. |
