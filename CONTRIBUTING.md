# Contributing to Geetorus

We welcome contributions from the community! To maintain architectural integrity, high code quality, and security, please review the following guidelines before submitting pull requests.

---

## Development Workflow

1. **Prerequisites**: Node.js `>= 24.11.0` and PNPM `>= 9.4.0`.
2. **Fork & Branch**: Create a feature branch off `main` (e.g., `feat/mcp-auth-headers` or `fix/task-hold-release`).
3. **Design Tokens**: All frontend code in `ui/` must strictly use tokens from `ui/src/index.css`. Never introduce raw hex colors or arbitrary pixel spacings. Run `pnpm check:token-gates`.
4. **Database Changes**: Modify schemas in `packages/db/src/schema/*.ts`, export them from `index.ts`, and run `pnpm db:generate`.
5. **Testing**: Run relevant unit and recovery test suites:
   ```bash
   pnpm --filter @geetorusai/shared test
   pnpm check:token-gates
   ```
6. **Pull Request**: Open a PR with clear acceptance criteria and screenshots or test logs.
