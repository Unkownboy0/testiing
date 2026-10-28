# Pulse — System Health & Recovery

## 1. Concept & Renaming

In GeetorusAI, the user-facing concept previously referred to as "Heartbeat" is officially renamed to:

**Pulse — System Health & Recovery**

### 1.1 Compatibility Boundary
To guarantee zero regressions and complete backwards compatibility:
- **Database Tables**: Internal execution tables (such as `heartbeat_runs`) remain untouched to avoid disruptive database schema migrations or external API breakage.
- **User-Facing UI**: All navigation links, page titles, tables, badges, metric cards, and dashboard summaries display **Pulse** or **Pulse runs**.
- **URL Aliases**: Navigation to `/heartbeat` and `/heartbeats` transparently redirects to `/pulse`.

---

## 2. Health States & Taxonomy

Pulse evaluates overall platform health using five discrete states:

| Health State | Definition | Trigger Condition |
| :--- | :--- | :--- |
| `healthy` | All services operating normally | Database connected, zero open circuit breakers, no active critical incidents. |
| `degraded` | Partial operational impairment | One or more provider circuit breakers open, or active non-fatal incidents. |
| `recovering` | Automated healing in progress | Active retry backoff underway, half-open circuit breaker probe active. |
| `unavailable` | Fatal service outage | PostgreSQL connection failure, or fatal core gateway fault. |
| `unknown` | State undetermined | Health check has not yet reported or has timed out. |

---

## 3. Pulse Telemetry Payload

`GET /api/pulse/status` returns the unified state:

```json
{
  "state": "healthy",
  "lastCheckedAt": "2026-10-09T14:00:00.000Z",
  "services": {
    "api-gateway": {
      "name": "API Gateway",
      "status": "healthy",
      "latencyMs": 1,
      "message": "Gateway operational and handling incoming requests",
      "lastCheckedAt": "2026-10-09T14:00:00.000Z"
    },
    "database": {
      "name": "Database (PostgreSQL)",
      "status": "healthy",
      "latencyMs": 4,
      "message": "Connected and accepting queries",
      "lastCheckedAt": "2026-10-09T14:00:00.000Z"
    },
    "ai-provider-openai": {
      "name": "AI Provider (openai)",
      "status": "healthy",
      "message": "Provider operational with normal error bounds.",
      "lastCheckedAt": "2026-10-09T14:00:00.000Z"
    }
  },
  "activeIncidents": [],
  "recentRecoveryEvents": [],
  "circuitBreakers": {
    "openai": {
      "serviceId": "openai",
      "state": "closed",
      "failures": 0,
      "threshold": 4,
      "cooldownMs": 30000
    }
  },
  "metrics": {
    "totalChecks": 12,
    "recoveredCount": 3,
    "failedCount": 0,
    "recoverySuccessRate": 100,
    "activeTasks": 0
  }
}
```

---

## 4. Operator Actions in Pulse Center

Within the `/pulse` dashboard, operators can:
1. **Trigger Instant Pulse Checks**: Re-evaluates PostgreSQL responsiveness and circuits.
2. **Reset Tripped Circuits**: Force a circuit breaker from `open` back to `closed` after resolving an external outage or billing lock.
3. **Resolve Incidents**: Manually acknowledge and clear historical diagnostic alarms.
4. **Audit Self-Healing Events**: Review step-by-step logs of automated exponential backoffs, circuit trips, and fallback model activations.
