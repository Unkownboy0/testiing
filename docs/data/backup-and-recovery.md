# Geetorus — Database Backup & Recovery Procedures

## 1. Automated Database Backups

Geetorus provides automated database backup scripts for PostgreSQL instances:

```bash
# Execute local database dump
pnpm db:backup
```
The backup utility (`scripts/backup-db.sh` and `server/src/routes/instance-database-backups.ts`) generates timestamped, gzip-compressed SQL dumps:
```
backups/geetorus_backup_YYYYMMDD_HHMMSS.sql.gz
```

---

## 2. Disaster Restoration Procedure

To restore a Geetorus instance from a previous backup:

1. Stop running dev/production services:
   ```bash
   pnpm dev:stop
   ```
2. Restore database from dump:
   ```bash
   gunzip -c backups/geetorus_backup_latest.sql.gz | psql "$DATABASE_URL"
   ```
3. Run migrations to ensure schema parity:
   ```bash
   pnpm db:migrate
   ```
4. Restart the Geetorus control plane:
   ```bash
   pnpm dev
   ```
