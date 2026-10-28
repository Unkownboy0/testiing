# GEETORUSAI — AURVEXX’2026 Hackathon Technical Documentation Hub

> **Event**: AURVEXX’2026 8-Hour Fast-Pitch & Technical Hackathon  
> **Repository Under Audit**: GeetorusAI Ecosystem (`geetorusai`, `companies-tool`, `geetorus-companies`, `geetorus-market`)  
> **Audit Status**: Complete Code-Backed Technical Audit (October 2026)

---

## 🧭 Master Documentation Index

| File | Document Title | Primary Target Audience | Core Focus |
| :--- | :--- | :--- | :--- |
| **[`00-project-overview.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/00-project-overview.md)** | Project Overview & Executive Brief | All Evaluators & Founder | 30s & 2min pitch scripts, executive summary, maturity assessment. |
| **[`01-product-purpose-and-problem.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/01-product-purpose-and-problem.md)** | Product Purpose & Problem Statement | Product Judges | Why single-agent wrappers fail; the Virtual Company solution. |
| **[`02-existing-features-and-capabilities.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/02-existing-features-and-capabilities.md)** | Existing Features & Catalog | Technical Judges | Verified capabilities matrix with code evidence. |
| **[`03-system-architecture.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/03-system-architecture.md)** | Complete System Architecture | System Architects | Multi-layer component breakdown, failure modes, inputs/outputs. |
| **[`04-architecture-diagrams.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/04-architecture-diagrams.md)** | Architecture Diagrams (Mermaid) | Visual Evaluators & Founder | 9 validated Mermaid diagrams with English & Thanglish explanations. |
| **[`05-complete-working-flow.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/05-complete-working-flow.md)** | Complete Working Flow & Request Trace | Backend Engineers | End-to-end trace from UI task creation to git commit. |
| **[`06-module-and-directory-reference.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/06-module-and-directory-reference.md)** | Module & Directory Reference | Developers | Directory map of server, UI, packages, adapters, and tools. |
| **[`07-functions-classes-and-responsibilities.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/07-functions-classes-and-responsibilities.md)** | Functions & Classes Inventory | Technical Evaluators | Core symbols, signatures, callers/callees, and security guards. |
| **[`08-ai-llm-and-model-routing.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/08-ai-llm-and-model-routing.md)** | AI & Model Routing Engine | AI / LLM Judges | Claude, GPT-4o, Ollama, model selection cascade, rate limits. |
| **[`09-agentic-workflows-and-tool-execution.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/09-agentic-workflows-and-tool-execution.md)** | Agentic Workflows & MCP Tool Gateway | AI Judges & Hackathon Mentors | Turn planner loop, MCP tool gateway, Amber approval gates. |
| **[`10-api-and-integration-reference.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/10-api-and-integration-reference.md)** | API & Integration Reference | Backend Developers | REST routes, WebSocket events, and GitHub webhooks. |
| **[`11-data-flow-and-database-design.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/11-data-flow-and-database-design.md)** | Data Flow & Database Design | Database Architects | 137 Drizzle PostgreSQL schemas, entity relationships, privacy. |
| **[`12-security-and-privacy.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/12-security-and-privacy.md)** | Security & Privacy Audit | Security Judges | Threat model, SSRF protection, HMAC action signing, risk register. |
| **[`13-error-handling-and-failure-recovery.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/13-error-handling-and-failure-recovery.md)** | Error Handling & Failure Recovery | Reliability Engineers | Error tiers, watchdog timeouts, and reboot reconciliation. |
| **[`14-configuration-and-environment-variables.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/14-configuration-and-environment-variables.md)** | Configuration & Environment Guide | DevOps Engineers | Full environment variables catalog and sample `.env`. |
| **[`15-installation-and-local-development.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/15-installation-and-local-development.md)** | Installation & Local Setup | Developers & Evaluators | Fast 3-step setup, prerequisites, and common commands. |
| **[`16-testing-and-validation.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/16-testing-and-validation.md)** | Testing & Quality Assurance | QA & Lead Engineers | Vitest, Playwright E2E, Token Gates, Promptfoo evals. |
| **[`17-deployment-and-infrastructure.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/17-deployment-and-infrastructure.md)** | Deployment & Infrastructure | DevOps / Cloud Judges | Docker production multi-stage build, Nginx, cloud sandboxes. |
| **[`18-performance-and-resource-requirements.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/18-performance-and-resource-requirements.md)** | Performance & Scalability Specs | Systems Evaluators | Hardware specs, turn latency profile, and benchmark scripts. |
| **[`19-limitations-and-technical-debt.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/19-limitations-and-technical-debt.md)** | Technical Debt & Honest Limitations | Technical Judges | Monolithic routes, Windows Postgres locks, missing pgvector. |
| **[`20-improvement-roadmap.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/20-improvement-roadmap.md)** | Prioritized Product Roadmap | Product & Business Judges | 8-hour hackathon quick wins + P0–P3 engineering roadmap. |
| **[`21-hackathon-demonstration-plan.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/21-hackathon-demonstration-plan.md)** | Live Demonstration Plan | Founder & Presenter | 3-minute judging script, pre-demo checklist, offline fallback. |
| **[`22-first-round-presentation.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/22-first-round-presentation.md)** | Presentation & Pitch Scripts | Founder | Natural English pitch script + Thanglish preparation guide. |
| **[`23-judge-question-and-answer-bank.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/23-judge-question-and-answer-bank.md)** | Judge Q&A Defense Bank (60+ Qs) | Founder | 60 technical questions, spoken answers, deep code evidence. |
| **[`24-technical-glossary.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/24-technical-glossary.md)** | Technical Glossary (Dual Language) | All Readers | Core concepts explained in English and Thanglish. |
| **[`25-implementation-status-matrix.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/25-implementation-status-matrix.md)** | Implementation Status Matrix | Technical Auditors | Verified vs partially verified vs planned feature matrix. |
| **[`26-repository-and-dependency-map.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/26-repository-and-dependency-map.md)** | Repository & Dependency Map | DevOps & Architects | Ecosystem repo topology, dependencies, patched npm packages. |
| **[`27-decision-log-and-design-rationale.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/27-decision-log-and-design-rationale.md)** | Decision Log & ADRs | Architects & Evaluators | Architectural Decision Records (Turn loop, Drizzle, Amber gate). |
| **[`28-troubleshooting-guide.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/28-troubleshooting-guide.md)** | Operational Troubleshooting | Developers & Presenter | Fast fixes for Windows Postgres locks, port conflicts, API keys. |
| **[`29-references-and-evidence.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/29-references-and-evidence.md)** | References & Evidence Register | Lead Auditor | Traceable code references, line numbers, and audit commands. |

---

## 🎯 Recommended Reading Orders

### Path 1: For the Founder Preparing for Hackathon Round 1 (30 Mins)
1. Read **[`00-project-overview.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/00-project-overview.md)** for pitch memorization.
2. Review **[`21-hackathon-demonstration-plan.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/21-hackathon-demonstration-plan.md)** and practice the 3-minute live demo.
3. Read **[`22-first-round-presentation.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/22-first-round-presentation.md)** (especially the Thanglish prep script).
4. Study **[`23-judge-question-and-answer-bank.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/23-judge-question-and-answer-bank.md)** to confidently answer judge cross-questions.
5. Keep **[`28-troubleshooting-guide.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/28-troubleshooting-guide.md)** open during the demo in case of unexpected errors.

### Path 2: For Technical Judges & System Architects (15 Mins)
1. Review **[`03-system-architecture.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/03-system-architecture.md)** and **[`04-architecture-diagrams.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/04-architecture-diagrams.md)** for system topology.
2. Inspect **[`08-ai-llm-and-model-routing.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/08-ai-llm-and-model-routing.md)** and **[`09-agentic-workflows-and-tool-execution.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/09-agentic-workflows-and-tool-execution.md)** for agent orchestration depth.
3. Review **[`12-security-and-privacy.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/12-security-and-privacy.md)** and **[`19-limitations-and-technical-debt.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/19-limitations-and-technical-debt.md)** for honest technical assessment.
4. Check **[`25-implementation-status-matrix.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/25-implementation-status-matrix.md)** and **[`29-references-and-evidence.md`](file:///c:/Users/mohamed%20farhan/testing-marketing/docs/aurvexx-2026/29-references-and-evidence.md)** for code evidence.
