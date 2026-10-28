# GeetorusAI — Project Overview & Executive Brief

> **Target Venue**: AURVEXX’2026 Hackathon (8-Hour Fast Pitch & Architecture Defense)  
> **Evaluation Tier**: First-Round Technical Audit & Live System Demonstration  
> **Inspection Date**: October 2026  
> **Verification Status**: Code-backed Audit (Verified against `geetorusai`, `geetorus-companies`, `companies-tool`, `geetorus-market`)

---

## 1. Executive Summary: What is GeetorusAI Today?

**GeetorusAI** is an open-source, enterprise-grade **Autonomous AI Agent Control Plane and Virtual Company Operating System**. Rather than being a simple prompt-response chat wrapper or a naive script loop, GeetorusAI provides a stateful orchestration substrate that allows engineering teams, founders, and enterprises to model, supervise, and deploy coordinated teams of autonomous agents organized as "Virtual Companies" (e.g., `fullstack-forge`, `trail-of-bits-security`, `clawteam-engineering`).

Agents in Geetorus operate with defined roles (e.g., CEO, Tech Lead, Backend Dev, QA, Security Auditor), communicate over asynchronous messaging threads, execute shell and git commands within governed sandboxes, trigger tools via the Model Context Protocol (MCP), and submit completed work for human operator approval or peer review.

### Verified Core Capabilities vs. Conventional Chatbots

| Dimension | Basic AI Chatbot / Wrapper | GeetorusAI Agent Control Plane | Verification Status |
| :--- | :--- | :--- | :--- |
| **Execution Model** | Synchronous, single-turn request/response | Asynchronous, turn-based heartbeat daemon (`heartbeat.ts`) | **Verified** (`server/src/services/heartbeat.ts`) |
| **Organizational Hierarchy** | Flat user-to-bot interaction | Multi-tier company org charts with reporting lines & roles | **Verified** (`server/src/routes/org-chart-svg.ts`, `companies.ts`) |
| **Tool Calling & Sandbox** | Raw API execution on host | Governed MCP tool gateway with approval gates & docker/e2b leases | **Verified** (`server/src/services/tool-gateway.ts`, `environments.ts`) |
| **State Persistence** | Ephemeral or simple chat logs | 137 relational tables via Drizzle ORM on PostgreSQL | **Verified** (`packages/db/src/schema/*.ts`) |
| **Governance & Safety** | System prompt instructions | Hard token gates, financial budget tracking, cryptographic action signing | **Verified** (`server/src/services/budgets.ts`, `costs.ts`) |
| **Multi-Tenancy** | Single session | Scoped Virtual Companies with strict cross-tenant data isolation | **Verified** (`server/src/middleware/auth.ts`, company-scope checks) |

---

## 2. Pitch Scripts: Explaining Geetorus to Judges

### ⚡ The 30-Second Elevator Pitch (For Quick Judging Rounds)
> *"Most AI tools today are single-agent chatbots that forget context, break production without asking, and have no accountability. **Geetorus is a Virtual Company Operating System**. We don't just prompt an LLM; we deploy an entire engineering department of coordinated agents—Tech Leads, Coders, and QA—governed by strict budget controls, human approval gates, and sandboxed Git environments. You assign a high-level goal, the agents decompose it into tracked issues, write code, run tests, and pause for your sign-off before anything touches production. It’s autonomous execution with enterprise safety."*

### 🔬 The 2-Minute Deep Technical Pitch (For Architecture & Systems Judges)
> *"Under the hood, Geetorus is built as a hardened TypeScript monorepo powered by an Express API server, React 19 frontend, and Drizzle ORM backed by 137 PostgreSQL relational tables. Autonomous behavior is driven by a deterministic heartbeat scheduling engine (`server/src/services/heartbeat.ts`) rather than uncontrolled while-loops. 
> 
> When a task is dispatched, the orchestration engine initializes an isolated workspace, provisions an execution lease, and dispatches the task to the designated agent runtime—supporting Anthropic Claude, OpenAI, OpenRouter, and local Ollama or Codex models. All tool interactions flow through an MCP-compliant Tool Gateway that enforces cryptographically signed execution tokens and strict authorization boundaries. If an agent attempts a sensitive shell command, file write, or external API call, Geetorus traps the call in an 'Amber' approval state, alerting the human operator via real-time WebSockets. Once approved, the agent resumes execution, verifies completion contracts, and records an immutable audit log. 
> 
> Furthermore, with our `companies-tool` CLI and catalog of 17 turnkey virtual company configurations, teams can export, version-control, and spin up an entire specialized AI team in seconds."*

---

## 3. Product Maturity & Reality Assessment

Geetorus is currently an **Enterprise-Ready MVP / Core Production Platform** for self-hosted developer teams.

* **What is Fully Functional Today (Verified)**:
  1. Complete Multi-Agent Company Orchestration (Agents, Roles, Hierarchy, Org Chart).
  2. Issue/Task Lifecycle Management (Task creation, sub-task tree decomposition, status transitions).
  3. Turn-based Heartbeat Engine with watchdog recovery and deadlock detection.
  4. Pluggable Foundation Model Adapters (Claude, OpenAI, OpenRouter, Ollama, Kimi, Grok).
  5. Multi-channel integrations (Discord, Slack, Telegram, Teams, GitHub Webhooks).
  6. MCP Tool Gateway with granular principal access policies and approval gates.
  7. Turnkey Virtual Company portability (`companies.sh` export/import).
  8. Real-time Reactive Dashboard with Live Events WebSocket streaming.

* **What is Partially Implemented (Partially Verified)**:
  1. *Cloud Sandboxing Providers*: Local execution is battle-tested; remote Daytona/e2b sandbox drivers exist in codebase but require external cloud API credentials and active leases.
  2. *Marketplace Commerce*: Next.js marketplace (`geetorus-market`) lists templates, but automated Stripe checkout is currently simulated via mock tokens.

* **What is Planned / Future Roadmap (Planned)**:
  1. Long-term semantic episodic memory via vector embeddings (`pgvector` integration).
  2. Distributed horizontal multi-node worker queues (migrating in-memory/DB heartbeats to Redis/BullMQ).
  3. Fully autonomous multi-agent code consensus voting prior to human review.

---

## 4. Realistic Hackathon Demonstration Scenarios

For the 8-Hour AURVEXX’2026 Hackathon, the most compelling live demonstrations are:

1. **Scenario 1: Full-Cycle Bug Triage & Fix**:
   - Operator creates a bug report in the Geetorus UI.
   - Tech Lead agent analyzes the issue, decomposes it into sub-tasks, and assigns it to a Fullstack Coder agent.
   - Coder agent spins up a local git worktree, reproduces the bug, generates a fix, and requests approval.
   - Operator approves the action via the UI; agent commits and verifies the fix.

2. **Scenario 2: Turnkey Virtual Company Spin-Up**:
   - Founder runs `companies.sh import geetorus-companies/trail-of-bits-security`.
   - In 5 seconds, an entire security audit firm (Lead Pentester, Static Analyst, Reporter) is provisioned with custom system prompts, tool permissions, and budgets.
