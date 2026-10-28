# Geetorus — Technical Debt & Refactoring Opportunities

## 1. Technical Debt Register

| Debt Item | Affected Area | Severity | Impact | Recommended Refactoring |
| :--- | :--- | :--- | :--- | :--- |
| **Monolithic Route Spine** | `server/src/routes/issues.ts` (664KB) & `server/src/index.ts` (3,000 lines) | Medium | Slow IDE code navigation and high risk of regression when modifying task logic. | Refactor `issues.ts` into a modular router directory (`server/src/routes/issues/`) split into `crud.ts`, `comments.ts`, `approvals.ts`, and `workspaces.ts`. |
| **Frontend Token Allowlist Exceptions** | `ui/src/pages/` & `ui/src/components/` | Low | Minor style drift on demo/lab surfaces. | Execute Phase 4 of `DESIGN.md` to migrate remaining allowlisted inline styles into semantic tokens. |
| **Legacy Vitest Direct Invocation** | Monorepo root test scripts | Low | Running `npx vitest` directly from subfolders can fail without proper pnpm workspace resolution. | Standardize all test commands through `pnpm test:run` and package-scoped pnpm filters. |
| **Mocked Marketplace Checkout** | `geetorus-market/src/` | Medium | Users cannot currently complete paid transactions for community company templates. | Integrate Stripe Connect checkout sessions and webhook verification handlers. |
