# Geetorus — User Manual & Operational Guide

## 1. First-Time Setup & Onboarding

When launching Geetorus for the first time, operators can initialize the platform through the browser UI or via the CLI:

### Web UI Onboarding
1. Navigate to `http://localhost:3100`.
2. The **Onboarding Wizard** (`ui/src/components/OnboardingWizard.tsx`) presents initial configuration options:
   - **Create New Company**: Set company name, default budget cap, and primary currency.
   - **Import Template**: Choose from pre-configured organizations (e.g., `fullstack-forge`, `clawteam-engineering`, `trail-of-bits-security`).
   - **Configure Model Provider**: Input API keys for Anthropic (Claude 3.7 / 3.5 Sonnet), OpenAI (GPT-4o), or OpenRouter.
3. Once submitted, Geetorus provisions the company workspace, creates the default agent roster, and displays the interactive Org Chart.

### CLI Setup
Run the unified CLI to initialize a company directly from the terminal:
```bash
npx geetorusai company init --template fullstack-forge
```

---

## 2. Navigating the Operator Interface

The Geetorus control plane is structured into four primary operational zones:

1. **Top Navigation & Company Selector**: Switch active companies, view real-time daily spend against budget caps, and check platform health status.
2. **Left Navigation Sidebar**:
   - **Tasks / Board**: Kanban board and list view of all active, queued, and completed work streams.
   - **Org Chart**: Visual hierarchy of active AI agents, their roles, assigned tools, and reporting relationships.
   - **Routines**: Scheduled recurring background tasks and watchdog triggers.
   - **Tools & MCP Gateway**: Configured Model Context Protocol servers and tool permission matrices.
   - **Secrets Vault**: Company-scoped environment variables and encrypted API keys.
   - **Audit Activity Log**: Immutable chronological stream of all system, user, and agent actions.
3. **Main Content Canvas**: Dense information display optimized for scanning task states, viewing streaming LLM output, inspecting code diffs, and reviewing generated artifacts.
4. **Approval & Intervention Takeover**: Amber-highlighted action drawers that surface when an agent requires human sign-off for critical tool executions.

---

## 3. Step-by-Step Task Operations

### Creating and Assigning a Task
1. Click **+ New Task** (or press `N` hotkey).
2. Specify:
   - **Title**: Clear, outcome-focused title (e.g., `Add rate limiting middleware to /api/health`).
   - **Description / Acceptance Criteria**: Detailed instructions or user stories.
   - **Assignee**: Select a specific agent (e.g., `Backend Lead`) or leave as unassigned for automatic triage.
   - **Execution Workspace**: Choose local repository path or cloud sandbox environment.
   - **Budget Limit**: Optional per-task dollar cap.
3. Click **Create Task**.

### Monitoring Live Agent Sessions
1. Click on any active task in the board to open the **Task Session Inspector**.
2. Observe the live turn stream:
   - **Reasoning**: Monospace display of model chain-of-thought.
   - **Tool Executions**: Real-time arguments, execution duration, and standard output.
   - **Work Products / Artifacts**: Live file diffs, test suite summaries, and screenshots.

### Handling Human Approvals
When an agent invokes a guarded tool (e.g., running `git push --force`, altering database tables, or making external payments):
1. An amber banner appears: **"Approval Required"**.
2. Click **Review Request** to inspect the planned command, affected files, and rationale.
3. Click **Approve** to authorize the execution, or **Reject with Feedback** to provide alternative instructions directly into the agent's turn context.

---

## 4. Managing Agent Skills & Tools

1. Navigate to **Tools & MCP Gateway** (`/tools`).
2. To connect a new MCP server:
   - Click **+ Add Tool Server**.
   - Select connection type: `stdio` (local command) or `sse` (remote HTTP).
   - Enter executable path/command or SSE endpoint URL.
3. Define permission scope:
   - `Allow All`: Any agent can invoke tools from this server automatically.
   - `Gated`: Invocations trigger a human approval modal.
   - `Restricted`: Explicit whitelist of agent roles authorized to use specific tool methods.
