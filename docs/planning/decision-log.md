# Geetorus — Architecture & Product Decision Log

This log tracks key product and engineering decisions in chronological order.

---

## Decision Entries

### 2026-10-09: Universal Documentation Hub Consolidation
- **Decision**: Establish a single, comprehensive documentation system rooted under `docs/` covering product, architecture, engineering, APIs, AI systems, data schemas, security audits, operations, market research, and business strategy.
- **Rationale**: Eliminates documentation fragmentation across disparate markdown files and provides a code-backed reference for developers, operators, and investors.

### 2026-03-24: Standardized Design Token Discipline
- **Decision**: Adopt `ui/src/index.css` as the sole source of truth for visual tokens with automated CI validation via `scripts/check-token-gates.mjs`.
- **Rationale**: Prevents UI style drift and ensures high-density operational scanning.

### 2026-02-15: Native Model Context Protocol (MCP) Adoption
- **Decision**: Standardize all agent-to-tool communication on the Model Context Protocol (MCP) rather than custom function definitions.
- **Rationale**: Unlocks interoperability with the entire open-source MCP ecosystem.
