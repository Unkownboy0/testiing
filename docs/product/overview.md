# Geetorus — Product Overview

## 1. Executive Summary

**Geetorus** is an open-source, enterprise-grade **Autonomous AI Agent Control Plane & Virtual Company Operating System**. Built with a Node.js/Express backend, React/Vite frontend (powered by strict Tailwind v4 CSS design tokens), and Drizzle ORM on PostgreSQL, Geetorus allows software engineers, founders, and enterprises to orchestrate, supervise, and deploy multi-agent virtual companies that execute software engineering, research, marketing, customer support, and administrative workflows.

Unlike simple prompt wrappers, single-turn LLM chatbots, or basic script orchestrators, Geetorus treats agents as autonomous, persistent employees within an organizational chart. It provides durable task lifecycle management, multi-turn session tracking, scheduled routines, tool gating via Model Context Protocol (MCP), fine-grained budget limits, human-in-the-loop approvals, and full audit logs.

---

## 2. Problem Statement

Organizations adopting generative AI face critical structural roadblocks when moving from single-user playground prompts to autonomous production workflows:

1. **Unconstrained Execution & Cost Explosion**: Autonomous agent loops without strict budget policies and token gates can run endlessly, incurring thousands of dollars in unintended API expenses.
2. **Lack of Organizational Context**: Agents operate in isolated silos without shared memory, role hierarchies, reporting lines, or coordinated delegation.
3. **Black Box Execution**: Operators cannot see what agents are doing in real time, what tools they are invoking, or why a task failed.
4. **Security & Credential Exposure**: Injecting production API keys into agent prompts or arbitrary code sandboxes creates severe data-leak and command-injection vulnerabilities.
5. **No Enforcement of Tangible Outcomes**: Traditional frameworks declare tasks "completed" when an LLM stops generating text, regardless of whether tests passed, code merged, or artifacts were produced.

---

## 3. Product Vision & Mission

- **Vision**: To provide the universal control plane for human-agent collaboration, enabling high-leverage virtual organizations where human operators guide strategy and autonomous agent teams execute complex projects safely and transparently.
- **Mission**: Deliver a reliable, secure, and extensible operating system that governs agent lifecycles, guarantees observable executions, enforces least-privilege tool access, and translates business goals into verified software and operational deliverables.

---

## 4. Target Personas & Primary Use Cases

| Persona | Role & Objectives | Key Pain Points Solved |
| :--- | :--- | :--- |
| **Technical Founder / CTO** | Runs an early-stage startup with limited human headcount; needs autonomous engineering and product operations. | Multiplies engineering velocity without linearly scaling headcount; ensures budget limits prevent surprise bills. |
| **Engineering Lead / VP Eng** | Supervise automated PR reviews, refactoring tasks, QA smoke testing, and routine maintenance runs. | Eliminates prompt boilerplate; enforces CI/CD verification gates before accepting agent code outputs. |
| **AI Agency Operator** | Manages multiple client projects with bespoke agent teams, custom MCP tools, and isolated environments. | Uses `companies.sh` to package, export, and deploy distinct virtual company configurations across customer environments. |
| **Enterprise Security Officer** | Mandates strict least-privilege access, encrypted secret storage, and complete audit trails of all agent actions. | Scoped secret bindings, per-agent MCP permissions, explicit human approvals for high-risk actions, and tamper-resistant audit logs. |

---

## 5. Core Value Propositions

1. **True Multi-Agent Organizational Hierarchy**: Agents have reporting lines, roles, and dedicated project workspaces rather than being flat, undifferentiated chat workers.
2. **Enforced Outcomes & Recovery Watchdogs**: Tasks are bounded by completion contracts and self-healing recovery actions. If an agent loops or stalls, watchdogs intervene to terminate or retry safely.
3. **Governed Tool Access via MCP Gateway**: Integrates any standard Model Context Protocol (MCP) server, subjecting tool invocations to company policies and approval gates.
4. **Zero Visual Drift & Operator-First UI**: Built on strict CSS design tokens (`ui/src/index.css`), presenting state density, heartbeat health, live task logs, and interactive diff reviews.
5. **Multi-Environment Sandbox Flexibility**: Seamless execution across local native runtimes, Docker containers, e2b, Daytona, Modal, and Cloudflare Workers.

---

## 6. Product Boundaries & Non-Goals

### In-Scope (Core Platform)
- Control plane orchestration, state persistence, and event delivery.
- Agent task decomposition, heartbeats, and lifecycle state machines.
- Role-based permissions, secret vault integration, and budget policy enforcement.
- Rich web UI for monitoring, debugging, approving, and interacting with running agents.
- Headless CLI (`geetorusai`) and company packaging CLI (`companies.sh`).

### Non-Goals (Out of Scope)
- **Proprietary Foundation Models**: Geetorus does not train or host base LLMs; it connects to Anthropic, OpenAI, OpenRouter, MiniMax, Ollama, and external endpoints.
- **Generic Consumer Chatbot**: Geetorus is an operational control plane for goal-driven tasks, not an unfocused conversational chatbot.
- **Raw Cloud Infrastructure Provisioner**: Geetorus delegates virtual machine and container provisioning to dedicated sandbox providers (Docker, e2b, Daytona) rather than managing cloud hypervisors directly.

---

## 7. Supported Platforms & Technology Stack Summary

- **Backend Runtime**: Node.js `>= 24.11.0` (ES Modules, TypeScript, Express, Drizzle ORM).
- **Database Engine**: PostgreSQL 16+ (or PGlite/embedded Postgres for zero-config local development).
- **Frontend Framework**: React 19, Vite, Tailwind CSS v4 design tokens, Radix UI primitives.
- **CLI Utilities**: `geetorusai` (Node/tsx), `companies.sh` (Node/Commander).
- **Operating Systems**: Linux (Ubuntu 22.04+), macOS (Apple Silicon / Intel), Windows 11 (PowerShell / WSL2).
