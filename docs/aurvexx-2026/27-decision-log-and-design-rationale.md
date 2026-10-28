# 27 — Decision Log & Architectural Design Rationale (ADRs)

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Purpose**: Document the key engineering trade-offs and design invariants chosen during Geetorus development.

---

## ADR-01: Turn-Based Heartbeat Loop vs. Uncontrolled While-Loops

* **Context**: Most early agent frameworks run an unconstrained `while True` loop that queries the LLM and calls tools until completion.
* **Problem**: When models hallucinate or hit repeating errors, while-loops run uncontrollably, burning through token budgets and starving CPU resources.
* **Decision**: Implement a deterministic **Turn-Based Heartbeat Scheduler** (`server/src/services/heartbeat.ts`).
* **Consequences**:
  - *Positive*: Every turn requires lease acquisition, checks budget thresholds, and records audit telemetry. Deadlocks are caught by task watchdogs.
  - *Negative*: Introduces minor scheduling latency (100–500ms) between consecutive turns.

---

## ADR-02: PostgreSQL + Drizzle ORM vs. SQLite or ChromaDB

* **Context**: Many AI prototypes use SQLite or flat JSON files for persistence and ChromaDB for memory.
* **Problem**: SQLite lacks robust multi-tenant concurrency and row-level locking. Flat files corrupt under parallel access.
* **Decision**: Standardize on **PostgreSQL 16+** with **Drizzle ORM** across 137 relational tables, bundling `embedded-postgres` for zero-config local development.
* **Consequences**:
  - *Positive*: Full ACID compliance, cross-table relational integrity (`issues`, `companies`, `turns`), and seamless transition from local developer machines to cloud AWS RDS.
  - *Negative*: Higher initial startup footprint (~120MB RSS) compared to SQLite.

---

## ADR-03: MCP Tool Gateway with "Amber Gates" vs. Unconstrained Execution

* **Context**: Tools like AutoGPT execute shell commands without human intervention.
* **Problem**: Autonomous command execution creates severe security liabilities (accidental deletions, unauthorized pushes, credential exposure).
* **Decision**: Route all agent tool intents through an **MCP Tool Gateway** (`server/src/services/tool-gateway.ts`) enforcing **Amber Approval Gates** on privileged actions.
* **Consequences**:
  - *Positive*: Enterprise-grade safety; operators have complete oversight before changes touch repositories.
  - *Negative*: Requires human-in-the-loop interaction to approve amber states before a task completes.

---

## ADR-04: Drizzle ORM vs. Prisma ORM

* **Context**: Selecting an ORM for the TypeScript monorepo.
* **Decision**: Adopt **Drizzle ORM** over Prisma.
* **Rationale**:
  - Prisma generates heavy Rust query engine binaries that increase cold start latency and complicate cross-platform packaging.
  - Drizzle compiles directly to lightweight SQL prepared statements with zero runtime engine overhead, providing superior performance and simpler migration control.

---

## ADR-05: React 19 Semantic Design Tokens vs. Ad-Hoc Tailwind CSS

* **Context**: Designing the web control plane interface.
* **Decision**: Enforce a centralized **Semantic Token System** (`ui/src/index.css`) backed by strict token gate linters (`scripts/check-token-gates.mjs`).
* **Rationale**: Banning raw hex colors and arbitrary pixels ensures visual consistency across 35+ pages, supports dark/light themes natively, and delivers a premium enterprise interface.
