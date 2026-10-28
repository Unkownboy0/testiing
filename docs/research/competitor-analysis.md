# Geetorus — Market Research & Competitor Benchmarking

## 1. Competitive Landscape Matrix

The AI Agent market has bifurcated into **developer python libraries** (raw orchestration), **single-purpose coding agents** (Devin, Cursor), and **enterprise multi-agent operating systems** (Geetorus).

| Dimension | Geetorus | CrewAI Enterprise | AutoGen (Microsoft) | Devin (Cognition) | LangGraph / LangChain |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Paradigm** | Full-Stack Control Plane & Virtual Company OS | Agent Role Scripting Framework + Cloud UI | Python Multi-Agent Library | Single Autonomous Software Engineer | Graph-based Orchestration Library |
| **Persistence Layer** | PostgreSQL (137 Drizzle schemas) | Cloud SaaS / SQLite | In-memory state | Proprietary Cloud | In-memory / Custom Checkpointers |
| **Tool Protocol** | Standard Model Context Protocol (MCP) | Custom Python Tools | Function Calling API | Custom Sandbox CLI | Custom Python Functions |
| **UI Experience** | Dense Tailwind v4 Token-gated Dashboard & Org Chart | Cloud Dashboard | AutoGen Studio (Basic Web UI) | Chat + Diff Web Interface | LangSmith (Telemetry / Traces) |
| **Governance & Safety** | Granular Budget Caps, Approval Modals, Encrypted Vault | Role boundaries | Conversational Filters | Sandboxed Cloud Machine | Code-level conditionals |
| **Self-Hosting** | 100% Open Source & Self-Hostable | Commercial SaaS | Open Source Python | Closed Source SaaS ($500+/mo) | Open Source Library |

---

## 2. Competitive Differentiation & Moats

1. **Enterprise MCP Tool Gateway**: Geetorus is the first control plane built natively around Anthropic's Model Context Protocol, enabling instant compatibility with hundreds of enterprise tools.
2. **Virtual Company Model**: Instead of ad-hoc prompt scripts, Geetorus models organizational hierarchies with reporting lines, roles, and modular department templates (`companies.sh`).
3. **True Self-Hosting & Zero-Telemetry Option**: Enterprises with sensitive source code can deploy Geetorus entirely on-premise with air-gapped models (Ollama).
