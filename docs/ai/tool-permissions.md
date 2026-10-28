# Geetorus — Tool Permissions & MCP Gateway

## 1. Model Context Protocol (MCP) Governance

Geetorus governs all tool interactions through a centralized **MCP Tool Gateway (`server/src/routes/tool-gateway.ts`)**. Rather than giving agents raw shell or database access, every tool must be registered as a standard MCP server.

```
Agent Turn Request ──► MCP Tool Gateway ──► Policy & Risk Filter ──► MCP Server ──► External System
                                                    │
                                                    ▼ (If High Risk)
                                            Approval Modal (Human)
```

---

## 2. Risk Classification & Gating Policies

| Risk Level | Tool Examples | Gating Behavior | Audit Record |
| :--- | :--- | :--- | :--- |
| **Low / Safe** | `read_file`, `grep_search`, `list_dir`, `fetch_web_doc` | Executed immediately without human interruption. | Logged to `activity_log`. |
| **Medium** | `write_to_file`, `replace_file_content`, `create_git_branch` | Executed automatically in sandbox; workspace diff recorded. | Full diff logged. |
| **High / Critical** | `run_shell_command`, `git_push`, `db_drop_table`, `stripe_charge` | **Blocked**. Generates pending record in `approvals.ts`. Requires human operator approval in UI. | Immutable signature & operator user ID logged. |

---

## 3. Secret Resolution & Scoped Injection

When an agent invokes a tool requiring external credentials (e.g., GitHub Personal Access Token or Slack Bot Token):
1. The tool definition declares required secret keys (`company_secret_bindings.ts`).
2. The MCP Gateway decrypts the secret at runtime using `GEETORUS_SECRET_KEY`.
3. The credential is dynamically injected into the tool process environment without ever exposing the raw secret string to the LLM context or prompt history.
