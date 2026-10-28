# Changelog

All notable changes to the Geetorus ecosystem are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2026.325.0] - 2026-10-09

### Added
- **Comprehensive Documentation Hub**: Complete architecture, engineering, API, security, data, and business documentation under `docs/`.
- **Model Context Protocol (MCP) Gateway**: Centralized tool routing, permission matrix, and connection intent deliveries.
- **Tailwind v4 Token Gates**: CI automated linting (`scripts/check-token-gates.mjs`) preventing frontend style drift.
- **Company Templates (`geetorus-companies`)**: 17 turnkey virtual company configurations for instant onboarding.
- **Self-Healing Turn Recovery**: Automated watchdog loop intervention and safe turn replacement for stalled agent tasks.

### Changed
- Refactored task session inspector with real-time SSE streaming.
- Enhanced encrypted secret vault with per-agent least-privilege bindings.
