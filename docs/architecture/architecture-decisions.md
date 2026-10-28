# Geetorus — Architectural Decision Records (ADRs)

This document captures the foundational architectural decisions, rationale, trade-offs, and invariants governing the Geetorus codebase.

---

## ADR-001: Monorepo Architecture with PNPM Workspaces
- **Status**: Accepted & Implemented
- **Context**: Geetorus requires tightly synchronized schemas, shared validation logic, and shared types across the CLI, backend server, frontend UI, and database migrations.
- **Decision**: Adopt a PNPM monorepo with strict package boundaries (`packages/db`, `packages/shared`, `packages/adapters`, `server`, `ui`, `cli`).
- **Consequences**:
  - *Positive*: Zero code duplication for domain schemas; single-command installs; strict workspace dependency resolution.
  - *Trade-off*: Requires workspace linking preflight scripts (`scripts/ensure-workspace-package-links.ts`).

---

## ADR-002: Strict Design Token Architecture (`ui/src/index.css`)
- **Status**: Accepted & Implemented (Governed by `DESIGN.md`)
- **Context**: Frontend drift, inconsistent colors, and hardcoded pixel spacing degrade operational scanning speed and UX quality.
- **Decision**: Mandate a single source of visual truth in `ui/src/index.css` using Tailwind CSS v4 `@theme`. Ban all inline hex codes, raw pixel dimensions, and arbitrary Tailwind brackets in UI components.
- **Consequences**:
  - *Positive*: Guaranteed visual consistency; instant runtime dark/light theme switching; automated lint enforcement (`pnpm check:token-gates`).
  - *Trade-off*: Minor initial developer friction when adding new visual primitives (must be registered in `index.css` first).

---

## ADR-003: Model Context Protocol (MCP) as Universal Tool Standard
- **Status**: Accepted & Implemented
- **Context**: Custom proprietary tool schemas create lock-in and require continuous maintenance for every external SaaS API integration.
- **Decision**: Adopt Anthropic's open **Model Context Protocol (MCP)** as the sole standard for agent tool exposure, discovery, and execution.
- **Consequences**:
  - *Positive*: Seamless interoperability with any standard MCP server (GitHub, PostgreSQL, Filesystem, Slack, Google Sheets); pluggable enterprise integrations.
  - *Trade-off*: Tool calls require structured JSON-RPC serialization and governance middleware.

---

## ADR-004: Mandatory Company-Scope Multi-Tenancy
- **Status**: Accepted & Implemented
- **Context**: Accidental data leakage between different organizations or client workspaces in multi-tenant environments is a catastrophic security failure.
- **Decision**: Every database entity (issues, agents, secrets, runs, tools) must carry a foreign key to `companies.id`, and every backend route must validate active company membership before executing queries.
- **Consequences**:
  - *Positive*: Robust multi-tenant isolation; verifiable data ownership.
  - *Trade-off*: All API queries must include company context in route parameters or headers.

---

## ADR-005: Dual Embedded / Dedicated PostgreSQL Database Architecture
- **Status**: Accepted & Implemented
- **Context**: Developers want zero-config local setup (`pnpm dev`), while enterprise deployments require production-grade managed PostgreSQL (e.g., AWS RDS, Neon, Supabase).
- **Decision**: Support zero-dependency local embedded PostgreSQL via `@geetorusai/db/migration-runtime.ts` while allowing instant configuration of external `DATABASE_URL` for production environments.
- **Consequences**:
  - *Positive*: Frictionless developer onboarding without Docker prerequisites; identical Drizzle ORM schema across local and production.
  - *Trade-off*: Windows developers must handle stale embedded process cleanup on abnormal terminations.
