# GeetorusAI Testing & Quality Assurance

## 1. Test Architecture

GeetorusAI utilizes [Vitest](https://vitest.dev) for fast unit and integration testing across server and UI packages.

### 1.1 Test Suites Created
1. `server/src/services/self-healing/self-healing.test.ts`:
   - Error classification of rate limits (`429`), auth (`401`/`403`), network timeouts, and server errors (`5xx`).
   - Token and key sanitization (preventing secret leaks in messages).
   - Circuit breaker threshold tripping, cooldown transitions, and manual resets.
   - Recovery engine exponential backoff, jitter calculation, and fallback model routing.
   - Preflight security validations, SSRF blocks (`169.254.169.254`), prompt emptiness, and context window limits.
2. `server/src/services/model-discovery/model-discovery.test.ts`:
   - OpenAI model enumeration and capability normalization.
   - Anthropic Claude 3.5 Sonnet / Opus 200k context window detection.
   - Google Gemini 1.5 Pro / Flash multimodal detection.
   - Live API caching vs. forced refresh.
   - Provider connection testing and latency measurement.
3. `server/src/__tests__/model-discovery-routes.test.ts`:
   - Supertest integration tests for `POST /models/preflight`.
   - Supertest integration tests for `POST /models/test-connection`.
   - Supertest integration tests for `POST /models/discover`.
4. `server/src/__tests__/pulse-routes.test.ts`:
   - Supertest integration tests for `GET /pulse/status`.
   - Supertest integration tests for `GET /pulse/circuit-breakers`.
   - Supertest integration tests for `POST /pulse/circuit-breakers/:provider/reset`.
   - Supertest integration tests for `GET /pulse/settings` and `PUT /pulse/settings`.
5. `ui/src/pages/PulseCenter.test.tsx`:
   - JSDOM React component tests for Pulse header, services rendering, and tab navigation.
6. `ui/src/pages/ModelExplorer.test.tsx`:
   - JSDOM React component tests for model cards rendering, capabilities display, and live query filtering.

---

## 2. Test Execution Commands

### 2.1 Server Unit & Integration Tests
```bash
pnpm --filter @geetorusai/server exec vitest run src/services/self-healing/self-healing.test.ts src/services/model-discovery/model-discovery.test.ts src/__tests__/model-discovery-routes.test.ts src/__tests__/pulse-routes.test.ts
```
**Result**: 30 passed (30 total tests), 0 failed.

### 2.2 UI Component Tests
```bash
pnpm --filter @geetorusai/ui exec vitest run src/pages/PulseCenter.test.tsx src/pages/ModelExplorer.test.tsx
```
**Result**: 4 passed (4 total tests), 0 failed.

### 2.3 UI Typecheck Verification
```bash
pnpm --filter @geetorusai/ui exec tsc --noEmit
```
**Result**: Clean exit code 0.

### 2.4 Design Token Gate Compliance
```bash
node scripts/check-token-gates.mjs
```
**Result**: Zero new violations in created UI modules.
