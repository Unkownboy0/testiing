# Geetorus Documentation Hub

Welcome to the comprehensive, code-backed engineering, architecture, and product documentation for **Geetorus** — the autonomous AI agent control plane and virtual company operating system.

---

## 📚 Documentation Index

### 1. Product & Vision
- **[Product Overview](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/product/overview.md)**: Product mission, core value propositions, and boundaries.
- **[Vision & Scope](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/product/vision-and-scope.md)**: Strategic vision, non-goals, and evolution path.
- **[Personas & Use Cases](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/product/personas-and-use-cases.md)**: Target user roles, workflows, and core operational scenarios.
- **[Feature Catalog & Capability Matrix](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/product/feature-catalog.md)**: Complete implementation status of all platform capabilities.
- **[User Guide](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/product/user-guide.md)**: Step-by-step walkthrough for operating virtual companies.
- **[FAQ & Troubleshooting](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/product/faq-and-troubleshooting.md)**: Common failure modes and operational solutions.

### 2. Architecture & Design
- **[System Overview](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/architecture/system-overview.md)**: High-level architectural topology and sub-system boundaries.
- **[Architecture Decisions (ADRs)](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/architecture/architecture-decisions.md)**: Key design decisions, trade-offs, and invariants.
- **[Component Design](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/architecture/component-design.md)**: Deep dive into Server, UI, DB, Adapters, and Plugin subsystems.
- **[Data Flow & Event Lifecycle](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/architecture/data-flow.md)**: Step-by-step trace from task creation to agent execution and artifact generation.

### 3. Engineering & Developer Guide
- **[Repository Guide](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/engineering/repository-guide.md)**: Directory map, entry points, and monorepo structure.
- **[Development Setup](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/engineering/development-setup.md)**: Local environment setup, dependencies, and troubleshooting.
- **[Coding Conventions](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/engineering/coding-conventions.md)**: Design tokens, TypeScript rules, and company scoping rules.
- **[Dependencies & Tooling](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/engineering/dependencies.md)**: Package manifest analysis and ecosystem dependencies.
- **[Testing & Quality Assurance](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/engineering/testing.md)**: Vitest, Playwright E2E, token-gates, and Storybook visual testing.

### 4. API & Integration Reference
- **[API Overview & Architecture](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/api/overview.md)**: REST and SSE endpoints, headers, and company context.
- **[Authentication & Scopes](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/api/authentication.md)**: Session tokens, API keys, CLI auth challenges, and board chat tokens.
- **[API Endpoints Reference](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/api/endpoints.md)**: Comprehensive schema definitions for all 78 server routes.
- **[Error Codes & Handling](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/api/error-codes.md)**: Standardized HTTP error responses and recovery patterns.
- **[OpenAPI Specification](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/api/openapi.yaml)**: OpenAPI v3 specification definition.

### 5. AI, Agents & Orchestration
- **[Model Support & Provider Gateway](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/ai/model-support.md)**: Anthropic, OpenAI, OpenRouter, MiniMax, Ollama, and local fallbacks.
- **[Agent Workflows & Lifecycle](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/ai/agent-workflows.md)**: Heartbeats, task session turns, watchdogs, and recovery.
- **[Tool Permissions & MCP Gateway](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/ai/tool-permissions.md)**: Model Context Protocol (MCP) server integration, security boundaries, and approval gating.
- **[Agent Evaluation & Quality Feedback](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/ai/evaluation.md)**: Promptfoo evals, decision training, and regression metrics.

### 6. Data & Storage
- **[Database Schema & Models](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/data/database-schema.md)**: 137 Drizzle PostgreSQL schema definitions and relationships.
- **[Migrations & Data Lifecycle](file:///c:/Users/moranet%20farhan/testing-marketing/docs/data/migrations.md)**: Drizzle Kit migrations, embedded Postgres runtime, and schema evolution.
- **[Backup & Recovery](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/data/backup-and-recovery.md)**: Database dump, restore, and automated snapshots.

### 7. Security, Privacy & Compliance
- **[Threat Model](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/security/threat-model.md)**: STRIDE analysis, agent isolation, and execution sandbox boundaries.
- **[Security Controls](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/security/security-controls.md)**: RBAC, secrets encryption, company isolation, and command gating.
- **[Security Audit & Findings](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/security/security-findings.md)**: Defensive security audit, identified vulnerabilities, and remediations.
- **[Privacy & Data Handling](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/security/privacy-and-data-handling.md)**: PII protection, external LLM data policies, and retention rules.

### 8. Operations & Infrastructure
- **[Deployment Guide](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/operations/deployment.md)**: Docker, self-hosted Linux/Windows, Cloudflare Workers, and cloud sandboxes (e2b, Daytona, Modal).
- **[Configuration & Environment](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/operations/configuration.md)**: Complete environment variables reference and instance settings.
- **[Monitoring & Health Checks](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/operations/monitoring.md)**: Prometheus/metrics, health probe endpoints, and error logging.
- **[Incident Response](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/operations/incident-response.md)**: Triage runbooks for agent runaway spend, stuck tasks, and DB locks.
- **[Disaster Recovery](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/operations/disaster-recovery.md)**: RTO/RPO targets, data reconstruction, and failover workflows.

### 9. Market Research & Strategy
- **[Competitor Analysis](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/research/competitor-analysis.md)**: Benchmarking against CrewAI, AutoGen, Devin, Agency Enterprise, and open-source stacks.
- **[Market Opportunities](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/research/market-opportunities.md)**: Enterprise agent operations, autonomous agencies, and verified gaps.
- **[Source Register](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/research/source-register.md)**: Primary market data sources, research dates, and citations.

### 10. Business & Go-To-Market
- **[Product Positioning](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/business/positioning.md)**: Core differentiation, messaging matrix, and buyer personas.
- **[Pricing Hypotheses & Packaging](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/business/pricing-hypotheses.md)**: Seat tiers, agent execution compute margins, and enterprise packaging.
- **[Go-To-Market Strategy](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/business/go-to-market.md)**: Open-source developer adoption, enterprise pilot programs, and partner channels.
- **[Investor Readiness & Traction Metrics](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/business/investor-readiness.md)**: Unit economics, defensibility moats, risk matrix, and pitch assessment.

### 11. Planning & Technical Debt
- **[Known Limitations](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/planning/known-limitations.md)**: Known constraints in Windows concurrency, sandbox persistence, and LLM rate limits.
- **[Technical Debt Register](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/planning/technical-debt.md)**: Legacy route monoliths, frontend token drift, and test coverage gaps.
- **[Prioritized Product Roadmap](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/planning/roadmap.md)**: P0–P3 roadmap with effort estimates, acceptance criteria, and ROI.
- **[Decision Log](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/planning/decision-log.md)**: Chronological architecture and product decisions.
