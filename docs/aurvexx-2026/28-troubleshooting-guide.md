# 28 — Operational Troubleshooting & Diagnostic Guide

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Purpose**: Fast, field-tested solutions for common operational issues encountered during local development and live demonstrations.

---

## 1. Quick Diagnostic Table

| Symptom / Error Message | Root Cause | Immediate Fix Command | Verification Check |
| :--- | :--- | :--- | :--- |
| **`Embedded Postgres: shared memory block already in use`** | Stale background `postgres.exe` from an unclean previous process exit. | `Stop-Process -Name postgres -Force -ErrorAction SilentlyContinue` | Rerun `pnpm dev`; boots cleanly on dynamic port. |
| **`Node.js engine check failed: required >=24.11.0`** | Host system is running an older Node version (e.g. Node 18 or 20). | Upgrade Node via `nvm use 24` or install latest Node.js 24 LTS. | `node -v` shows `v24.11.0` or higher. |
| **`EADDRINUSE: address already in use :::3100`** | Another dev server instance is already running on port 3100. | `Get-Process -Id (Get-NetTCPConnection -LocalPort 3100).OwningProcess \| Stop-Process -Force` | Rerun `pnpm dev`. |
| **`Missing AI Credentials / No Provider Configured`** | `.env` has empty API keys and Ollama is offline. | Add `ANTHROPIC_API_KEY` to `.env` OR run `ollama serve` locally. | Refresh Company Settings; green connection status appears. |
| **`Agent Turn Paused / Amber Gate Pending`** | Agent executed a privileged action and is awaiting human approval. | Navigate to **Approvals** tab (`/approvals`) in the UI and click **Approve**. | Issue resumes execution immediately. |
| **`Workspace link error / cannot resolve @geetorusai/db`** | Symlinks not initialized after fresh clone. | Run `pnpm run preflight:workspace-links` | Symlinks verified under `node_modules`. |

---

## 2. In-Depth Recovery Runbooks

### Runbook A: Resolving Windows Embedded Postgres Locks
On Windows, when you press `Ctrl+C` in PowerShell, the Node process exits, but the background `postgres.exe` child process may continue running.
1. Open PowerShell as Administrator (or standard user).
2. Execute:
   ```powershell
   Stop-Process -Name postgres -Force -ErrorAction SilentlyContinue
   ```
3. Restart Geetorus:
   ```powershell
   pnpm dev
   ```

---

### Runbook B: Resetting an Issue Execution Lock
If an agent turn stalls due to an external network timeout:
1. In the Geetorus UI, navigate to the stuck issue.
2. Click **Actions ➔ Revoke Lease** or use the CLI:
   ```bash
   pnpm geetorusai issue unlock <issue-id>
   ```
3. The lease lock in `execution_workspace_runtime_leases` is deleted, and the task returns to the ready queue.
