# 09 — Agentic Workflows, Tool Execution, and Automation

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Codebase audit of `server/src/services/heartbeat.ts`, `tool-gateway.ts`, `task-watchdogs.ts`, and `packages/mcp-server/`.

---

## 1. What Makes an "Agent" Different from a "Chatbot"?

In simple chatbots, execution is **passive and reactive**: the user provides a prompt, the model returns a text string, and execution terminates. 

In GeetorusAI, agents are **active, stateful systems** that run in a continuous feedback loop:

```
[Observe State / Context] ──▶ [Reason / Plan] ──▶ [Act via Tool] ──▶ [Evaluate Observation] ──▶ [Iterate]
```

| Dimension | LLM Answering a Question (Chatbot) | Agent Executing a Task (Geetorus) |
| :--- | :--- | :--- |
| **Control Flow** | 1 prompt in ➔ 1 response out | Multi-turn heartbeat loop with autonomous state transitions |
| **Environment Interaction** | None (Isolated text output) | Reads/writes files, executes git branches, runs unit tests |
| **Self-Correction** | Cannot test or verify its own code | Reads stderr from test runs and updates code until tests pass |
| **Supervision** | No governance boundaries | Governed by MCP tool gates, budget limits, and human approvals |
| **Coordination** | Single monolithic prompt | Hierarchical delegation between Tech Lead, Dev, and QA agents |

---

## 2. Agentic Capabilities Inventory

| Capability | Status | Implementation Details in Geetorus | Code Evidence |
| :--- | :--- | :--- | :--- |
| **1. Tool-Enabled Execution** | **Verified** | Agents invoke MCP-compliant tools (`bash`, `git_commit`, `file_read`, `file_write`) via JSON function schemas. | `server/src/services/tool-gateway.ts` |
| **2. Turn-Based Planner Loop** | **Verified** | `heartbeat.ts` drives recurring turns; agents plan steps, emit tool intents, and ingest execution outputs. | `server/src/services/heartbeat.ts` |
| **3. Human Approval Gates** | **Verified** | Sensitive tools (e.g., git push, package install, production writes) enter an "Amber" state awaiting operator decision. | `server/src/services/approvals.ts` |
| **4. Hierarchical Task Delegation** | **Verified** | Tech Lead agents create sub-issues with parent-child links in `issue_relations` and assign them to specialized agents. | `server/src/routes/issues.ts`, `issue-tree-control.ts` |
| **5. Long-Running Workspaces** | **Verified** | Tasks execute inside isolated Git worktrees (`.geetorus/worktrees/<issue-id>`) that persist across turns. | `server/src/services/execution-workspaces.ts` |
| **6. Deadlock & Stall Watchdogs** | **Verified** | `task-watchdogs.ts` monitors running turns; if an agent hangs for >5 minutes without emitting output, the lease is revoked. | `server/src/services/task-watchdogs.ts` |
| **7. Multi-Channel Triggers** | **Verified** | Webhook receivers on Slack, Discord, and GitHub can awaken agents and trigger task turns. | `server/src/services/chat-channels.ts` |
| **8. Long-Term Vector Memory** | **Planned** | Cross-task episodic semantic search via `pgvector` is designed on roadmap but not yet implemented in DB. | `docs/planning/roadmap.md` |

---

## 3. Verified Execution Path: From Plan to Verification

```
+---------------------------------------------------------------------------------------------------+
|                              GEETORUS AGENTIC CONTROL LOOP                                        |
|                                                                                                   |
|  1. WAKEUP TICK                                                                                   |
|     `heartbeatService` identifies an active task lease.                                           |
|                                                                                                   |
|  2. CONTEXT CONSOLIDATION                                                                         |
|     Assembles: System Persona + Current File Tree + Previous Tool Outputs + Budget Thresholds.    |
|                                                                                                   |
|  3. REASONING & INTENT GENERATION                                                                 |
|     LLM evaluates previous step:                                                                  |
|     - Did `npm test` fail? ──▶ Inspect test output and determine required file patch.             |
|     - Did `npm test` pass? ──▶ Prepare completion summary and mark task ready for review.         |
|                                                                                                   |
|  4. MCP TOOL GATEWAY ARBITRATION                                                                  |
|     Tool call passes through `toolAccessPolicyService`:                                           |
|     - Read-only action (e.g., `file_read`, `git_diff`) ──▶ Immediate execution.                   |
|     - Gated action (e.g., `bash: rm -rf`, `git_push`)   ──▶ Emit Amber Approval Request.           |
|                                                                                                   |
|  5. EXECUTION & FEEDBACK INGESTION                                                                |
|     Tool executes inside workspace; stdout/stderr is appended to context for next turn.           |
|                                                                                                   |
|  6. COMPLETION CONTRACT VERIFICATION                                                              |
|     Task finalizer checks if declared acceptance criteria are met before closing issue.           |
+---------------------------------------------------------------------------------------------------+
```

---

## 4. Safety Boundaries & Cryptographic Protection

To prevent rogue agent behavior or prompt injection attacks from hijacking host infrastructure:

1. **Path Traversal Sandboxing**: All file manipulation tools validate canonical file paths using `portable-path.ts` to ensure operations cannot escape the designated workspace directory.
2. **Cryptographic Action Signing**: Every privileged tool dispatch requires an HMAC-SHA256 signature generated with `GEETORUS_TOOL_ACTION_SIGNING_SECRET`. Tampered tool requests are discarded.
3. **Budget Incidents**: If total token expenditure on an issue exceeds the company's allocated budget policy (`budget_policies` table), the execution orchestrator immediately revokes the agent's turn lease and blocks further inference.
