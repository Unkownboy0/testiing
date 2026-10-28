# Geetorus — Database Migrations & Evolution

## 1. Migration Workflow (Drizzle Kit)

Database schema evolution is managed via **Drizzle Kit** within `@geetorusai/db`.

### Step 1: Modify TypeScript Schema
Edit the schema definitions in `packages/db/src/schema/*.ts`.

### Step 2: Generate SQL Migration
Generate the incremental SQL migration files:
```bash
pnpm db:generate
```
This generates standard SQL files under `packages/db/drizzle/` containing exact `CREATE TABLE`, `ALTER TABLE`, and index modifications.

### Step 3: Apply Migrations
Apply pending migrations to the active database:
```bash
pnpm db:migrate
```

---

## 2. Embedded Postgres Runtime for Local Development

To allow instant developer onboarding without installing PostgreSQL or Docker, Geetorus includes an embedded migration runtime (`packages/db/src/migration-runtime.ts`).

When `pnpm dev` starts:
1. The runtime checks if `DATABASE_URL` is provided.
2. If omitted, it initializes an isolated embedded PostgreSQL instance.
3. Automatically executes all pending migrations before starting the API server.
