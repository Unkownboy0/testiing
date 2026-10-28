# 21 — AURVEXX’2026 Live Demonstration Plan & Backup Strategy

> **Target Venue**: AURVEXX’2026 Hackathon (Round 1 Live Judging)  
> **Allocated Demo Time**: 3 to 5 Minutes Live Presentation  
> **Key Goal**: Demonstrate autonomous agent task execution, amber gate human approval, and virtual company portability without relying on brittle network calls.

---

## 1. Pre-Demo Setup & Environment Checklist

Execute these 3 setup checks **15 minutes before the judges arrive at your booth**:

1. **Clean Any Stale Windows Postgres Processes**:
   ```powershell
   Stop-Process -Name postgres -Force -ErrorAction SilentlyContinue
   ```
2. **Start Geetorus in Hot Watch Mode**:
   ```powershell
   cd geetorusai
   pnpm dev
   ```
   *Verify: `http://localhost:3100` loads instantly with green database status.*
3. **Verify API Credentials**:
   *Check that `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` is active in `.env`, OR ensure `ollama run qwen2.5-coder` is running locally for 100% offline fallback.*
4. **Pre-Import Showcase Company**:
   ```bash
   cd ../companies-tool
   pnpm start import ../geetorus-companies/fullstack-forge
   ```

---

## 2. The 3-Minute Live Demonstration Flow

```
+---------------------------------------------------------------------------------------------------+
|                                  THE 3-MINUTE JUDGING SCRIPT                                      |
|                                                                                                   |
|  [0:00 - 0:30] THE HOOK & VIRTUAL COMPANY OVERVIEW                                                |
|  • Show Org Chart on `http://localhost:3100`:                                                     |
|    "Judges, welcome to Geetorus. This isn't a chatbot. This is 'Fullstack Forge', a complete      |
|    autonomous software engineering department with a Tech Lead, Senior Developer, and QA Agent."  |
|                                                                                                   |
|  [0:30 - 1:15] DISPATCHING AN AUTONOMOUS ENGINEERING TASK                                         |
|  • Click "New Issue" in the Issues tab.                                                           |
|  • Enter Title: "Add Input Validation & Unit Test to User Profile API"                            |
|  • Assign to: Tech Lead Agent. Priority: High. Click "Create Task".                               |
|  • Show Live WebSocket Telemetry:                                                                 |
|    "Watch the control plane: The Heartbeat scheduler claims an exclusive lease, spins up an       |
|    isolated Git worktree, and the Tech Lead decomposes the task into actionable code changes."    |
|                                                                                                   |
|  [1:15 - 2:00] THE HERO MOMENT: THE "AMBER GATE" APPROVAL                                         |
|  • Agent generates the code patch and attempts to execute `git commit` or run a shell tool.      |
|  • The UI instantly flashes with an **AMBER APPROVAL CARD**:                                      |
|    "Look at this. Traditional AI agents break production because they run unchecked. Geetorus     |
|    traps privileged tools in an Amber Gate. The agent cannot proceed without my explicit verdict."|
|  • Show the proposed code diff in the modal dialog.                                               |
|  • Click **"Approve Action"**.                                                                    |
|  • The agent immediately wakes up, applies the commit, and logs the token cost in real time.     |
|                                                                                                   |
|  [2:00 - 2:45] PORTABILITY & 10-SECOND COMPANY DEPLOYMENT                                         |
|  • Open terminal and run: `companies.sh import ../geetorus-companies/trail-of-bits-security`     |
|  • Refresh the browser: A brand-new security audit firm is provisioned with custom roles!        |
|                                                                                                   |
|  [2:45 - 3:00] CLOSING & ARCHITECTURAL SUMMARY                                                    |
|  • "137 relational PostgreSQL tables, MCP-compliant tool governance, multi-model flexibility,     |
|    and enterprise safety by design. That is Geetorus."                                            |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Bulletproof Backup Plan (If Network / LLM Fails)

### Scenario A: Hackathon Venue Wi-Fi Drops / Slow Internet
* **Root Cause**: Venue Wi-Fi is congested; Anthropic/OpenAI API calls time out.
* **Immediate Backup Action**:
  - Geetorus has built-in local Ollama support (`packages/adapters/ollama-local`).
  - Switch the company's active model connection to `ollama-local` (Qwen 2.5 Coder 7B).
  - All inference runs 100% locally on your laptop GPU/CPU with **zero internet connection required**.

### Scenario B: Model Provider Returns HTTP 429 Rate Limit
* **Immediate Backup Action**:
  - Switch provider dropdown from Anthropic to OpenAI GPT-4o or OpenRouter in the Company Settings page.
  - Or run the pre-recorded end-to-end acceptance demo harness:
    ```bash
    pnpm test:e2e:headed
    ```
    This launches Playwright in visible browser mode, executing the full task lifecycle with deterministic mock fixtures!

---

## 4. Adapting Geetorus to ANY Hackathon Problem Statement

When the AURVEXX’2026 problem statement is announced at the hackathon, adapt Geetorus in 15 minutes:

1. **If the problem is "Automated Customer Support"**:
   - Create a virtual company with Triage Agent, Escalation Lead, and Knowledge Base Specialist.
2. **If the problem is "Cybersecurity / Threat Hunting"**:
   - Import `geetorus-companies/trail-of-bits-security` and demo automated CVE scanning.
3. **If the problem is "Financial Analysis / Trading"**:
   - Import `geetorus-companies/clawteam-capital` with strict financial budget policies enabled.
4. **If the problem is "Autonomous Code Refactoring"**:
   - Use `fullstack-forge` to scan a repository, identify lint/type errors, and generate automated PRs.
