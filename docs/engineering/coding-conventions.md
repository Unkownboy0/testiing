# Geetorus — Coding Conventions & Architectural Guidelines

## 1. Design Token Discipline (`ui/src/index.css`)

All visual presentation across the React frontend is governed by `DESIGN.md` and enforced via `scripts/check-token-gates.mjs`.

### Strict Invariants:
1. **Zero Raw Hex Colors**: Never use `#ffffff`, `#1e293b`, or `#000000` in JSX/TSX. Use semantic tokens: `var(--background)`, `var(--card)`, `var(--primary)`, `var(--muted)`.
2. **Zero Arbitrary Pixel Spacing**: Do not write arbitrary Tailwind classes like `p-[14px]` or `top-[22px]`. Use standard spacing scales or CSS variables.
3. **Machine Values Look Machine-Made**: Always apply `font-mono` and uniform formatters for UUIDs, hashes, token counts, timestamps, and pricing numbers.
4. **Canonical Copy**: The user-facing term is **Task** (never *issue* or *ticket* in labels, buttons, or toasts).

---

## 2. TypeScript & API Route Standards

### Mandatory Company-Scope Check
Every API route in `server/src/routes/*.ts` must verify that the requesting session has valid access to the target `companyId`:
```typescript
// Standard company validation pattern
const companyId = req.params.companyId || req.body.companyId || req.query.companyId;
if (!companyId) {
  return res.status(400).json({ error: "Missing required company context." });
}
await requireCompanyAccess(req.user, companyId);
```

### Schema & Entity Exports
When introducing a new database table:
1. Define the table schema in `packages/db/src/schema/<table_name>.ts`.
2. Export the schema and types in `packages/db/src/schema/index.ts`.
3. Run `pnpm db:generate` to produce the SQL migration.
4. Export shared DTO validation schemas in `packages/shared/src/`.

---

## 3. Error Handling & Logging

- Use standardized HTTP error status codes (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, `500 Internal Server Error`).
- Never return raw database stack traces in production API responses.
- Write structured operational logs to the central audit ledger via `packages/db/src/schema/activity_log.ts`.
