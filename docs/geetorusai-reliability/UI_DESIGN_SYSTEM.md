# GeetorusAI UI Design System: Minimal with Selective Brutalism

## 1. Design Direction

The UI philosophy of GeetorusAI balances **clean, minimal elegance** across general navigation, task feeds, and settings with **selective brutalism** for operational telemetry, system health, and diagnostic recovery panels.

### 1.1 Why Minimal?
- Focuses user attention on task completion, agent execution, and artifacts.
- Employs generous whitespace, high-legibility typography (`InterVariable`), and subtle borders (`border-border`).
- Avoids visual clutter, unnecessary gradient blobs, floating cards, or gimmicky artificial decorations.

### 1.2 Why Selective Brutalism?
- Critical system states (Pulse health, tripped circuit breakers, outage banners, telemetry counters) must communicate technical truth directly and unambiguously.
- Uses monospaced typography (`font-mono`), squared high-contrast status panels (`rounded-none`, `border-2`), and clear semantic status pills (`HEALTHY`, `DEGRADED`, `OUTAGE`).

---

## 2. Design Tokens Policy

All styling complies strictly with the design tokens configured in `ui/src/index.css`.
- **Zero Raw Hex Colors**: Direct `#hex` literals are prohibited in application components.
- **Zero Arbitrary Bracket Values**: Classes like `bg-[rgba(...)]` are rejected by `pnpm check:token-gates`.
- **Theme Variables**:
  - `bg-background` / `text-foreground`
  - `bg-card` / `text-card-foreground`
  - `bg-muted` / `text-muted-foreground`
  - `border-border`
  - `bg-primary` / `text-primary-foreground`
  - `bg-secondary` / `text-secondary-foreground`
  - `bg-destructive` / `text-destructive-foreground`
  - `font-mono` / `font-sans`

---

## 3. Screen Breakdown

### 3.1 Main Dashboard (`/dashboard`)
- Executive summary of active agents, month spend, in-progress tasks, and pending approvals.
- High-visibility **Pulse & Dynamic Models Quick Overview Widget**:
  - Live system state badge with ping animation during recovery.
  - Incident counts and operational indicators.
  - Quick action links navigating to `/pulse` and `/models`.

### 3.2 Pulse Center (`/pulse`)
- Four dedicated operational tabs:
  1. **Services & Providers**: Real-time status cards for API Gateway, PostgreSQL, and AI Providers.
  2. **Circuit Breakers**: Individual breaker status, failure counters, cooldown timers, and manual reset buttons.
  3. **Incidents**: Active error summaries with severity badges (`CRITICAL`, `HIGH`, `MEDIUM`) and "Mark Resolved" buttons.
  4. **Recovery Audit Log**: Monospaced event history recording auto-recovery actions, retry counts, and outcomes.

### 3.3 Model Explorer (`/models`)
- Search bar with live multi-field filtering.
- Filter chips for providers: `all`, `openai`, `anthropic`, `google`, `openrouter`, `ollama`.
- Capability filter chips: `Tool Calling`, `Vision`, `Streaming`, `JSON Output`.
- Model metadata tiles showing token context limits, max completions, and live/cached provenance.
- "Connect & Discover" interactive modal with live latency testing and catalog hydration.
