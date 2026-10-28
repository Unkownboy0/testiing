# Geetorus — FAQ & Operational Troubleshooting

## 1. Frequently Asked Questions

### Q: How is Geetorus different from LangChain, CrewAI, or AutoGen?
**A**: LangChain and AutoGen are primarily developer software libraries designed for script-based orchestration in code. Geetorus is a **full-stack enterprise control plane and operating system** equipped with a persistent relational database (PostgreSQL), strict design-token UI, multi-tenant company isolation, human approval gates, encrypted secret vaults, and hardware/cloud sandbox runtime management.

### Q: Does Geetorus require Docker?
**A**: No. For local development, Geetorus runs natively on Node.js using local execution workspaces and an embedded PostgreSQL instance. Docker is only required if you choose containerized execution sandboxes or wish to deploy via the official multi-container `docker-compose.yml`.

### Q: How does Geetorus prevent runaway AI API spending?
**A**: Geetorus enforces a multi-tier budget engine:
1. **Company-Level Daily Caps**: Halts all agent heartbeats when daily spend reaches the threshold.
2. **Per-Task Hard Limits**: Automatically pauses individual tasks exceeding their designated token/dollar budget.
3. **Loop Watchdogs**: Terminates agent turns if consecutive non-productive tool calls or repetitive error patterns are detected.

---

## 2. Operational Troubleshooting Guide

### Issue 1: Embedded Postgres "Shared Memory Block" Error on Windows
- **Symptom**: Starting the server fails with `could not open shared memory block: error code 5` or similar lock error.
- **Root Cause**: A stale `postgres.exe` process remained active after an abnormal server termination or crash.
- **Resolution**:
  Run the following PowerShell command to terminate orphaned processes:
  ```powershell
  Stop-Process -Name postgres -Force -ErrorAction SilentlyContinue
  pnpm dev
  ```

### Issue 2: Agent Task Stalled in `in_progress` with No Output
- **Symptom**: Task shows active status, but no turns or tool outputs appear in the live feed.
- **Root Cause**: The upstream LLM provider API encountered a timeout, or a long-running shell command in the execution workspace is waiting on interactive stdin.
- **Resolution**:
  1. Open the task in UI and click **Pause Work**.
  2. Inspect the Task Session Log for the last recorded process PID.
  3. Click **Recover Task** to trigger a safe turn rollback (`server/src/services/native-runtime/native-safe-replacement.ts`).

### Issue 3: Token Gate Lint Failure (`check-token-gates`)
- **Symptom**: CI or pre-commit hook fails with `check:token-gates: hardcoded visual values detected`.
- **Root Cause**: Direct hex colors (e.g., `#1e293b`), arbitrary pixel values (`w-[342px]`), or raw inline styles were introduced into `ui/src/components/` or `ui/src/pages/`.
- **Resolution**:
  Replace hardcoded styles with semantic CSS custom properties defined in `ui/src/index.css` (e.g., `var(--card)`, `var(--primary)`, `var(--radius)`). Run:
  ```bash
  pnpm check:token-gates
  ```

### Issue 4: MCP Server Connection Failure (`ECONNREFUSED` or `ENOENT`)
- **Symptom**: Agent cannot invoke MCP tools; error logs show failed stdio spawn or remote endpoint connection refused.
- **Root Cause**: The local binary specified in tool configuration is not on `PATH`, or the remote SSE server is unreachable.
- **Resolution**:
  Verify the server path under **Tools & MCP Gateway** (`/tools`) and test binary execution in terminal before binding to agents.
