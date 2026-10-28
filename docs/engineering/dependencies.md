# Geetorus — Dependencies & Technology Manifest

## 1. Core Runtime Dependencies

| Package / Module | Version | Purpose & Usage |
| :--- | :--- | :--- |
| **Node.js** | `>= 24.11.0` | Server runtime, native ES Modules, web crypto APIs. |
| **Express** | `^4.21.2` | High-throughput REST API server and SSE streaming router. |
| **Drizzle ORM** | `^0.39.0` | Type-safe SQL query builder and schema manager. |
| **PostgreSQL (pg / PGlite)** | `^8.13.0` | Primary relational persistence layer and embedded dev DB. |
| **React** | `^19.0.0` | UI component tree and state rendering. |
| **Vite** | `^6.1.0` | Frontend bundler and rapid HMR development server. |
| **Tailwind CSS** | `^4.0.0` | Modern CSS-variable token engine (`@theme`). |
| **@clack/prompts** | `^0.10.1` | Interactive CLI user experience in `companies-tool`. |
| **Commander** | `^13.1.0` | CLI argument and flag parser. |

---

## 2. Development & Testing Dependencies

| Tool | Version | Category |
| :--- | :--- | :--- |
| **TypeScript** | `^7.0.2` (Monorepo) / `^5.8.2` | Static type checking and compiler. |
| **Vitest** | `^4.1.11` | Fast unit and integration test runner. |
| **Playwright** | `^1.62.1` | End-to-end browser and visual regression test framework. |
| **Storybook** | `^8.5.0` | Component isolation and design token visual workbench. |
| **Promptfoo** | `0.103.3` | LLM evaluation and prompt regression harness. |
| **ESBuild** | `^0.28.2` | Lightning-fast TypeScript bundle compiler for CLI scripts. |
