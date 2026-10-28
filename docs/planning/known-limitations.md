# Geetorus — Known Product & Technical Limitations

## 1. Operating System & Concurrency Constraints

1. **Windows Embedded Postgres Process Locking**:
   - *Limitation*: When running with the embedded PostgreSQL runtime on Windows, an abnormal server process termination can leave the background `postgres.exe` running, locking the shared memory segment and blocking subsequent server launches.
   - *Workaround*: Run `Stop-Process -Name postgres -Force` before restarting.
2. **Local Runtime Sandboxing Isolation**:
   - *Limitation*: In local execution mode, agent shell executions execute with the process permissions of the host Node.js runner unless configured with Docker sandboxes or cloud providers (e2b, Daytona).
3. **Monolithic Route Handler Performance**:
   - *Limitation*: `server/src/routes/issues.ts` is ~664KB and contains extensive inline state machine logic, which increases hot-reload compilation time during active backend development.
