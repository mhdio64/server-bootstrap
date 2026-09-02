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
- Phase 2 `users` role for bootstrap admin account, sudoers drop-in, and project-managed authorized_keys block.
- Synthetic tests for root admin rejection, missing authorized keys, and system UID classification.
- Phase 3 `ssh` role with project-owned sshd drop-in, effective-config validation, reconnect verification, and rollback on failure.
- Synthetic tests for invalid SSH port, drop-in content rendering, and missing control-node identity rejection.
- Phase 4 `firewall` role with project-owned iptables-nft chains, foreign-policy classifier, timed rollback, and persistence restore service.
- Synthetic tests for invalid firewall ports and firewall state classification.
- Phase 5 `security` role for unattended security upgrades with automatic reboot disabled.
- VM validation fixes for UFW detection, SSH PermitRootLogin semantics, firewall idempotency, and users sudo verification.
- Phase 6A `docker` role read-only discovery/classifier for absent, official-compatible, partial, conflicting, and ambiguous states.
- Synthetic tests for all Docker classifier states and conflicting preflight rejection.

## [0.0.1] - 2026-09-01

### Added

- Pre-implementation project context, architecture, safety model, and phased implementation plan.

[Unreleased]: https://github.com/mhdio64/server-bootstrap/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/mhdio64/server-bootstrap/releases/tag/v0.0.1
