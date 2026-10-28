# Geetorus — Monitoring, Health Probes & Metrics

## 1. Health Probe Endpoints

Geetorus exposes comprehensive system health probes for uptime monitoring and container orchestrator readiness checks:

```http
GET /api/health
```
Response:
```json
{
  "status": "ok",
  "uptime": 14200,
  "db": "healthy",
  "version": "2026.325.0",
  "memory": {
    "rss": 115343360,
    "heapTotal": 67108864,
    "heapUsed": 45219840
  },
  "runners": {
    "activeHeartbeats": 2,
    "queuedWakeups": 0
  }
}
```

---

## 2. Operational Metrics & Tracing

- **Token & Cost Tracking**: Logged in `cost_events` and aggregated per company, agent, and task.
- **Provider Latency**: Logged in `provider_trace_records` to identify API rate limit slowdowns.
- **Watchdog Intervention Frequency**: Tracked in `issue_watchdogs` to detect unstable tool calls.
