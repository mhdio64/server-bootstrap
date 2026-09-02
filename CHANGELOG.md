# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Repository foundation migrated to canonical `mhdio64/server-bootstrap` repository.
- Licensing, versioning, development dependency pins, Ansible and lint configuration, baseline CI, Dependabot, and placeholder playbooks for static validation.
- Project documentation, Cursor rules, and optional Graphify developer tooling guidance.
- Phase 1 orchestration with global preflight and the `common` role for Ubuntu 24.04 baseline configuration.
- Synthetic preflight tests for missing required variables and unsupported platform detection.
- Minimal example `inventory.yml` and `bootstrap.yml` layout under `examples/minimal/`.

## [0.0.1] - 2026-09-01

### Added

- Pre-implementation project context, architecture, safety model, and phased implementation plan.

[Unreleased]: https://github.com/mhdio64/server-bootstrap/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/mhdio64/server-bootstrap/releases/tag/v0.0.1
