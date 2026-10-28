# 17 — Deployment and Production Infrastructure

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Verified from `geetorusai/scripts/test-install-sh-docker.sh`, `server/src/index.ts`, and `packages/db`.

---

## 1. Deployment Architecture Options

Geetorus supports two primary deployment topologies depending on enterprise compliance requirements:

```
+---------------------------------------------------------------------------------------------------+
|                                  DEPLOYMENT TOPOLOGY MODES                                        |
|                                                                                                   |
|  [Mode A: Self-Hosted Appliance (Single Node / Edge)]                                             |
|  • Ideal for hackathons, startups, and developer workstations.                                     |
|  • Single server process running Express API + embedded PostgreSQL + Vite UI on Port 3100.        |
|  • Tasks execute in local Git worktrees (`.geetorus/worktrees/`).                                  |
|                                                                                                   |
|  [Mode B: Hardened Enterprise Cluster (Distributed Sandboxes)]                                    |
|  • Express API deployed in Docker / Kubernetes with autoscaling.                                   |
|  • External Managed PostgreSQL 16+ (AWS RDS / Neon / Supabase).                                    |
|  • Cloud Execution Sandboxes (e2b / Daytona / Modal) providing kernel-isolated microVMs.           |
|  • Nginx / Cloudflare reverse proxy terminating TLS and handling WebSockets.                     |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Production Docker Deployment

A production container bundles the compiled Express server and built static React UI:

```dockerfile
# Multi-stage production build
FROM node:24-bullseye-slim AS builder
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@9.15.4 --activate
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY packages/ ./packages/
COPY server/ ./server/
COPY ui/ ./ui/
RUN pnpm install --frozen-lockfile
RUN pnpm --filter @geetorusai/ui build
RUN pnpm --filter @geetorusai/server build

FROM node:24-bullseye-slim AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3100
ENV SERVE_UI=true
COPY --from=builder /app /app
EXPOSE 3100
CMD ["node", "server/dist/index.js"]
```

---

## 3. Reverse Proxy Configuration (Nginx Example)

Because Geetorus relies on both REST endpoints and real-time WebSockets (`/api/live-events`), Nginx must explicitly configure connection upgrading:

```nginx
server {
    listen 80;
    server_name geetorus.internal.company.com;

    location / {
        proxy_pass http://127.0.0.1:3100;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 4. Production Hardening Checklist

1. **Replace Master Secret**: Ensure `GEETORUS_SECRET_KEY` is a securely generated 32-byte hex string (e.g., `openssl rand -hex 32`).
2. **Externalize Database**: Set `DATABASE_URL` to a high-availability PostgreSQL 16+ cluster with automated WAL archiving.
3. **Sandbox Isolation**: Configure `E2B_API_KEY` or `DAYTONA_API_KEY` if agents will execute untrusted or arbitrary shell code.
