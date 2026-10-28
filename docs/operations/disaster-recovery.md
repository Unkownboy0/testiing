# Geetorus — Disaster Recovery & Business Continuity

## 1. Recovery Objectives
- **Recovery Time Objective (RTO)**: `< 15 minutes` for complete service recreation via Docker Compose.
- **Recovery Point Objective (RPO)**: `< 1 hour` based on automated PostgreSQL snapshot intervals.

---

## 2. Full System Rebuild Procedure

In the event of a catastrophic server hardware loss:

1. **Provision New Host**: Provision a clean Ubuntu 22.04 LTS instance with Docker and Docker Compose.
2. **Clone Monorepo**:
   ```bash
   git clone https://github.com/geetorusai/geetorus.git
   cd geetorus
   ```
3. **Restore Database Snapshot**: Pull latest S3/local backup and pipe into PostgreSQL container:
   ```bash
   gunzip -c backup_latest.sql.gz | docker exec -i geetorus_db psql -U geetorus_admin -d geetorus
   ```
4. **Restore Secrets & Master Key**: Populate `.env` with the original `GEETORUS_SECRET_KEY` and LLM credentials.
5. **Launch Stack**:
   ```bash
   docker compose up -d --build
   ```
6. **Verify Health**: Query `curl http://localhost:3100/api/health` to confirm healthy database connection and runner status.
