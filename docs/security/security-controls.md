# Geetorus — Security Controls & Defense-in-Depth

## 1. Multi-Tenant Isolation Controls

Every database query in the Express API is gated by **Company-Scope Middleware (`server/src/middleware/company-scope.ts`)**. Access is validated before executing any SQL query. Multi-tenant data leakage is prevented via:
1. Hard foreign keys to `companies.id` across all 137 schema tables.
2. Tenant ID validation on all REST route parameters and request bodies.
3. Automated test verification (`tests/e2e/multiuser-authenticated.config.ts`).

---

## 2. Secrets Management & Key Cryptography

- Secrets are encrypted at rest using AES-256-GCM.
- Encryption keys are derived from the server environment variable `GEETORUS_SECRET_KEY`.
- Raw secret strings are **never** returned in API responses (only metadata like `createdAt` and `name`).
- Secrets are bound to agents on a least-privilege basis (`company_secret_bindings.ts`) and injected directly into child tool processes rather than LLM prompts.

---

## 3. Human Approval Gates for High-Risk Actions

Actions classified as high-risk automatically halt the agent turn and generate an approval ticket:
- Shell commands containing destructive patterns (`rm -rf`, `git push --force`, `drop table`).
- Invocation of external payment, deployment, or infrastructure modification tools.
- Tasks requesting spend exceeding configured per-task budget thresholds.
