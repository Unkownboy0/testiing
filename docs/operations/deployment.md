# Geetorus — Deployment Guide & Production Operations

## 1. Deployment Topology Options

Geetorus supports three production deployment topologies:

1. **Multi-Container Docker / Compose (Recommended)**:
   - Backend API server + React UI static build + Dedicated PostgreSQL container.
   - Orchestrated via `Dockerfile` and `docker-compose.yml`.
2. **Self-Hosted Virtual Machine (Ubuntu 22.04 LTS / Debian 12)**:
   - Node.js 24 runtime managed by systemd or PM2, reverse-proxied by Nginx or Caddy.
   - Connected to managed PostgreSQL (AWS RDS / Supabase / Neon).
3. **Cloudflare Workers & D1/Hyperdrive (`geetorus-docs` / edge services)**:
   - Edge-rendered documentation and proxy endpoints.

---

## 2. Production Docker Deployment

### Step 1: Build the Production Container
```bash
docker build -t geetorus:latest .
```

### Step 2: Run with Docker Compose
```yaml
version: '3.8'
services:
  geetorus-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: geetorus
      POSTGRES_USER: geetorus_admin
      POSTGRES_PASSWORD: secure_db_password_here
    volumes:
      - geetorus_data:/var/lib/postgresql/data
    restart: unless-stopped

  geetorus-app:
    image: geetorus:latest
    ports:
      - "3100:3100"
    environment:
      NODE_ENV: production
      DATABASE_URL: postgres://geetorus_admin:secure_db_password_here@geetorus-db:5432/geetorus
      GEETORUS_SECRET_KEY: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - geetorus-db
    restart: unless-stopped

volumes:
  geetorus_data:
```
Launch the stack:
```bash
docker compose up -d
```
