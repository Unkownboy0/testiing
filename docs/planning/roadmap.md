# Geetorus — Prioritized Product Roadmap (P0 – P3)

This roadmap outlines the prioritized engineering and product development plan based on our comprehensive codebase audit.

---

## 1. Roadmap Initiatives Matrix

| Priority | Initiative | Problem Solved | Effort | Acceptance Criteria | ROI / Business Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P0** | **Route Monolith Deconstruction** | Refactor `server/src/routes/issues.ts` (664KB) into modular routers. | **M** | All existing Vitest and Playwright test suites pass; zero regression in task lifecycle. | Dramatically improves backend maintainability and reduces PR merge conflicts. |
| **P0** | **Strict Secret Key Startup Guard** | Prevent server from booting with weak/fallback `GEETORUS_SECRET_KEY` in production. | **S** | Server exits with code 1 and logs error if key is missing or <32 bytes when `NODE_ENV=production`. | Closes a critical potential credential exposure vulnerability. |
| **P1** | **Durable Vector Memory (pgvector)** | Agents currently lack long-term semantic memory recall across multiple tasks. | **L** | Integrate `pgvector` extension in `@geetorusai/db` to index and retrieve past task solutions and docs. | Increases task completion accuracy on large, recurring codebases. |
| **P1** | **Automated Stripe Checkout for Marketplace** | `geetorus-market` currently has mocked checkout flows for template creators. | **M** | Creators can link Stripe Express accounts; buyers can purchase templates with instant import token. | Unlocks immediate creator monetization flywheel. |
| **P2** | **Distributed Queue Integration (BullMQ/Redis)** | Heavy concurrent heartbeats on single-node instances can queue up during peak turns. | **L** | Heartbeat jobs execute via Redis-backed BullMQ with configurable concurrency per tenant. | Enables seamless multi-node horizontal scaling for enterprise deployments. |
| **P3** | **Interactive Webhook & Slack/Discord Bot** | Teams want to create and approve tasks directly from Slack or Discord channels. | **M** | Bi-directional Slack app that posts amber approval cards with interactive "Approve" buttons. | Increases operator responsiveness to approval gates. |
