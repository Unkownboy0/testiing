# Geetorus — Testing & Quality Assurance Architecture

## 1. Quality Gates & Test Pyramid

Geetorus enforces a comprehensive, multi-layer quality assurance pyramid to ensure zero visual regressions, strict schema integrity, and resilient agent turn execution.

```
                  ┌───────────────────────┐
                  │ Playwright E2E Tests  │  (Multi-user auth, task lifecycle,
                  │   (tests/e2e/*.ts)    │   MCP user journeys)
                  ├───────────────────────┤
                  │ Storybook Visual Reg  │  (Snapshot baselines, token
                  │  (tests/storybook)    │   drift gates)
                  ├───────────────────────┤
                  │  Runner & Recovery    │  (Stalled codex turn recovery,
                  │ (services/native-rt)  │   safe replacement evidence)
                  ├───────────────────────┤
                  │  Package Unit Tests   │  (Vitest for @geetorusai/shared,
                  │    (Vitest Suite)     │   adapters, server routes)
                  └───────────────────────┘
```

---

## 2. Test Suites & Execution Commands

### Package Unit & Integration Tests
Execute fast unit tests across individual packages:
```bash
# Test shared package types and validators
pnpm --filter @geetorusai/shared test

# Run runner acceptance and turn recovery test suites
pnpm test:runner-acceptance
pnpm test:runner-recovery
```

### Visual Regression & Design Token Gates
Verify that UI components remain strictly compliant with design tokens:
```bash
# Validate zero raw hex / arbitrary spacing in UI codebase
pnpm check:token-gates

# Run Playwright visual snapshot tests against Storybook baseline
pnpm test:storybook-visual
```

### End-to-End (E2E) Browser Tests
Run automated user journeys covering company creation, agent task assignment, and approval modals:
```bash
pnpm test:e2e
```

### Prompt & LLM Evaluation Harness
Evaluate prompt stability and output schemas using Promptfoo:
```bash
pnpm evals:smoke
```

---

## 3. Verified Execution Evidence

During our codebase audit, running package-level test suites confirmed passing status on core packages:
- **`@geetorusai/shared`**: Unit test suite passed with Exit Code `0`.
- **Token Gates (`check-token-gates.mjs`)**: Verified token validation script enforcing `@theme` custom properties.
