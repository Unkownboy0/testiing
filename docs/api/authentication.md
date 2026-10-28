# Geetorus — Authentication & Scopes

## 1. Authentication Mechanisms

Geetorus supports four authentication models tailored to different interaction interfaces:

1. **User Session Authentication**:
   - Standard session tokens generated during login or onboarding.
   - Passed via `Authorization: Bearer <session_token>` header or httpOnly cookies.
2. **Company / Board API Keys**:
   - Long-lived programmatic API keys (`board_api_keys` / `agent_api_keys` tables).
   - Scoped strictly to specific companies and designated role privileges.
3. **CLI Auth Challenges**:
   - Secure temporary handshake protocol (`cli_auth_challenges` table) used by `geetorusai login` and `companies.sh`.
4. **Agent Internal Runtime Tokens**:
   - Ephemeral single-turn tokens generated dynamically for sandboxed agent tasks, granting restricted access only to authorized MCP tools.

---

## 2. Role-Based Access Control (RBAC)

| Role | Scope | Permissions |
| :--- | :--- | :--- |
| **Owner / Admin** | Company-Wide | Full administrative control: billing, budget policies, secret management, agent roster modifications, and company deletion. |
| **Operator / Member** | Company-Wide | Create and assign tasks, approve tool requests, inspect live sessions, and view audit activity. |
| **Viewer / Auditor** | Read-Only | Read-only inspection of tasks, org charts, and activity logs. Cannot approve actions or create tasks. |
| **Agent Principal** | Task-Scoped | Read assigned task requirements, emit turn logs, invoke whitelisted MCP tools within allocated budget. |
