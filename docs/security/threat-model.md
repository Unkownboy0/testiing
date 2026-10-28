# Geetorus — Threat Model (STRIDE Framework)

## 1. Security Boundaries & STRIDE Analysis

Operating autonomous AI agents that execute code, manipulate files, and call external APIs introduces unique threat vectors. Geetorus models these threats systematically using the **STRIDE** methodology.

| Threat Category | Potential Attack Vector | Geetorus Mitigation Architecture |
| :--- | :--- | :--- |
| **Spoofing** | Unauthorized user or agent impersonating another principal or forging task turns. | Session tokens, HMAC challenge handshakes (`cli_auth_challenges`), and per-task agent runtime tokens. |
| **Tampering** | Rogue agent modifying audit records or tampering with parent task requirements. | Immutable append-only audit ledger (`activity_log.ts`); read-only system prompt injections; foreign key constraints. |
| **Repudiation** | Operator or agent denying executing a destructive command or financial spend. | Complete action attribution: all tool calls, approval decisions, and budget transactions carry user/agent UUIDs and timestamps. |
| **Information Disclosure** | LLM prompt leaking production API keys or cross-tenant company data. | AES-256 encrypted secret vault (`company_secrets`); runtime secret injection into tool environments without prompt exposure; mandatory company-scope filtering. |
| **Denial of Service** | Infinite agent execution loop consuming API quota or locking host CPU. | Strict daily dollar budget caps; per-task token limits; watchdog monitor that terminates stalled/looping turns. |
| **Elevation of Privilege** | Agent executing unauthorized shell commands or modifying database tables. | Governed MCP Tool Gateway; human-in-the-loop approval gates for high-risk tools; sandbox isolation (Docker/e2b/Daytona). |
