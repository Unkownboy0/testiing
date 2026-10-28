# 16 — Testing and Quality Validation Guide

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Source Verification**: Verified from `geetorusai/package.json` scripts, `vitest.config.ts`, and `playwright.config.ts`.

---

## 1. Multi-Tier Testing Architecture

Geetorus employs a 5-tier testing and verification framework to ensure backend stability, frontend visual consistency, and agent reasoning fidelity:

```
+---------------------------------------------------------------------------------------------------+
|                                      5-TIER QUALITY ARCHITECTURE                                  |
|                                                                                                   |
|  [Tier 1: Unit & Service Tests]                                                                   |
|  • Vitest Test Runner (`vitest run`) ──▶ Fast in-memory unit tests across services & adapters.    |
|                                                                                                   |
|  [Tier 2: Token Gate & Boundary Checkers]                                                         |
|  • `check:tokens` / `check:token-gates` ──▶ Enforces UI design token purity (no raw hex/px).      |
|  • `check:module-boundaries` ──▶ Enforces clean separation between server and client packages.    |
|                                                                                                   |
|  [Tier 3: E2E Integration Tests]                                                                  |
|  • Playwright Browser Automation (`tests/e2e/`) ──▶ Full user flow tests in headless Chrome.     |
|                                                                                                   |
|  [Tier 4: Visual Regression Testing]                                                              |
|  • Storybook Visual Baseline (`tests/storybook-visual/`) ──▶ Pixel-level visual regression diffs. |
|                                                                                                   |
|  [Tier 5: Agentic Evaluation Harnesses]                                                           |
|  • Promptfoo Evaluation Suite (`evals/promptfoo`) ──▶ Evaluates LLM prompt drift and benchmarks. |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Test Execution Commands Reference

### Fast Unit Testing (Vitest)
```bash
# Run all unit tests across the monorepo
pnpm test

# Run tests in watch mode during development
pnpm test:watch

# Run narrow test on a specific service
pnpm --filter @geetorusai/server exec vitest run src/services/heartbeat.test.ts
```

---

### UI Design Token Gate Validation
Geetorus strictly prohibits raw CSS hex codes (e.g. `#1a2b3c`) or ad-hoc pixel values in React components. All colors and spacing must derive from semantic tokens in `ui/src/index.css`.
```bash
# Verify no forbidden raw color tokens exist in UI components
pnpm check:tokens

# Validate strict token gates
pnpm check:token-gates
```

---

### End-to-End Browser Testing (Playwright)
```bash
# Run all headless Playwright tests
pnpm test:e2e

# Run Playwright in headed mode with browser visible (ideal for visual demo verification)
pnpm test:e2e:headed
```

---

### Agent Reasoning Evals (Promptfoo)
```bash
# Run LLM benchmark and evaluation matrix
pnpm evals:smoke
```
