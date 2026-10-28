# Geetorus — Vision, Scope & Positioning

## 1. Strategic Vision

The software and knowledge workforce is undergoing a paradigm shift from human-executed tasks augmented by AI tools to **autonomous virtual organizations governed by human directors**. In this emergent paradigm, software engineering teams, marketing agencies, and research labs are composed of specialized AI agent workers organized into functional departments.

Geetorus serves as the foundational operating system and control plane for these virtual entities. It provides:
1. **Predictability**: Structured task pipelines and deterministic outcome verification replace non-deterministic raw prompt loops.
2. **Accountability**: Every decision, command execution, and file modification is attributed to a specific agent identity and stored in an immutable audit ledger.
3. **Safety & Budget Fences**: Hard cost caps, rate limits, and human approval gates prevent unauthorized financial spend or destructive repository mutations.

---

## 2. Product Boundaries & Non-Goals

To maintain high engineering focus, Geetorus defines clear boundary lines:

```
+-------------------------------------------------------------------------------+
|                               GEETORUS CORE                                   |
|  +-------------------+  +-------------------+  +---------------------------+  |
|  | Org Charts & ACL  |  | Task State Machine|  | Secrets & Policy Engine   |  |
|  +-------------------+  +-------------------+  +---------------------------+  |
|  +-------------------+  +-------------------+  +---------------------------+  |
|  | MCP Tool Gateway  |  | Watchdog Monitors |  | Activity & Audit Logs     |  |
|  +-------------------+  +-------------------+  +---------------------------+  |
+-------------------------------------------------------------------------------+
          │                           │                            │
          ▼                           ▼                            ▼
+---------------------+     +--------------------+     +------------------------+
| External LLM APIs   |     | Execution Sandboxes|     | External Storage & Git |
| Anthropic, OpenAI,  |     | Docker, e2b,       |     | GitHub, PostgreSQL,    |
| OpenRouter, MiniMax |     | Daytona, Modal     |     | S3/R2 Artifact Buckets |
+---------------------+     +--------------------+     +------------------------+
```

### In-Scope (What Geetorus Owns)
- **Virtual Organization Modeling**: Companies, departments, agents, roles, and reporting lines.
- **Task & Session State Machines**: Issues, subtrees, tasks, turn history, and completion verification.
- **Governed Tool Access**: MCP server registration, connection intents, tool routing, and approval gates.
- **Policy Enforcement**: Per-agent budget limits, secret vault access, and workspace runtime leases.
- **Operator Interface**: Dense, real-time React UI with Tailwind v4 design tokens and CLI tools.

### Non-Goals (What Geetorus Explicitly Does Not Do)
- **Model Training / Fine-Tuning**: Geetorus does not train weights or host proprietary foundational LLMs.
- **Unsandboxed Host Takeover**: Geetorus forbids uncontrolled, unmonitored execution of arbitrary shell scripts directly on host environments without explicit operator configuration or sandbox isolation.
- **Ad-Hoc Consumer Social Chat**: Geetorus is not designed as a casual chatbot or discord replacement; all interactions are anchored to tasks, projects, and companies.

---

## 3. Product Principles (Core Invariants)

1. **Density over Chrome**: Information density in service of fast scanning beats decorative whitespace. Every screen answers: *What is happening? Does it need me? What do I do about it?*
2. **Tokens are the Sole Source of Visual Truth**: All visual attributes (color, typography, spacing, radius, motion) resolve strictly to CSS custom properties defined in `ui/src/index.css`.
3. **Canonical Vocabulary**: The primary unit of work across the UI, API, and documentation is the **Task** (with legacy database tables mapped under `issues`).
4. **Machine Values Look Machine-Made**: IDs, timestamps, token counts, and costs are formatted using monospace typography and uniform helper formatters.
5. **Zero Silent Failures**: When an agent fails or exhausts retries, the task state visibly transitions to `blocked` or `failed` with explicit diagnostic error context and suggested recovery actions.
