# Geetorus — Incident Response Runbooks

## Runbook 1: Runaway Agent Spend Incident
1. **Detection**: Notification from `budget_policies` or daily cap threshold breached.
2. **Immediate Action**:
   - Access Company Settings -> Click **Emergency Pause All Agents** (`POST /api/companies/:id/pause`).
   - All active heartbeat loops and task turns immediately abort.
3. **Investigation**:
   - Inspect `cost_events` filtered by `companyId` and order by `cost DESC`.
   - Identify the specific agent and task triggering repetitive inference calls.
4. **Resolution**:
   - Adjust watchdog max turn parameters or correct the recursive prompt issue.
   - Click **Resume Agents** when resolved.

---

## Runbook 2: Stuck Task Session Lock
1. **Detection**: Task remains in `in_progress` without turn progress for >15 minutes.
2. **Resolution**:
   - Trigger task recovery via `POST /api/issues/:id/recover`.
   - The server terminates the lingering child workspace process, rolls back the turn state, and posts a diagnostic notice.
