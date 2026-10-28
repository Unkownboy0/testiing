# Geetorus — Privacy & Data Handling Policies

## 1. Personally Identifiable Information (PII) & Telemetry

- **No Third-Party Analytics Tracking**: Geetorus does not inject invasive client-side tracking scripts or sell user activity data.
- **Opt-In Feedback Telemetry**: Operator feedback and vote exports (`feedback_exports.ts`) require explicit administrator export commands.
- **External AI Provider Data Flow**: Prompts and code diffs dispatched to upstream LLMs (Anthropic, OpenAI) are governed by the enterprise terms of those respective model providers. Geetorus supports zero-data-retention endpoints (e.g., Anthropic Zero Data Retention, Azure OpenAI, and local Ollama execution).

---

## 2. Data Retention & Tenant Deletion

- **Soft & Hard Deletion**: Company records can be archived or permanently purged along with all associated agents, tasks, secret bindings, and execution logs.
- **Audit Ledger Integrity**: Internal audit activity logs (`activity_log.ts`) maintain tamper-resistant timestamps for compliance reporting.
