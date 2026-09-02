# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-09-02

First usable MVP for safely bootstrapping Ubuntu Server 24.04 LTS (amd64) hosts.

### Added

- Repository foundation for canonical `mhdio64/server-bootstrap` with CI, secret scanning, and pinned tooling.
- Orchestration with global preflight, apply, and verification playbooks.
- Roles: `common`, `users`, `ssh`, `firewall`, `security`, `docker`.
- Python stdlib `./bootstrap` wrapper with `check`, `apply`, and `verify`.
- Public `bootstrap_*` configuration API and minimal examples.
- Verification summary, component opt-out warnings, reboot-required warnings, and target metadata.
- Synthetic classifier tests and wrapper unit tests.
- Scenario 1 real-VM validation harness and sanitized release evidence.
- User documentation: configuration reference, troubleshooting, and release evidence.

### Safety

- Fail-before-mutation policy for unknown consequential state.
- SSH hardening with effective-config validation, reconnect checks, and rollback.
- Project-owned `iptables-nft` firewall with foreign-policy detection.
- Official Docker installation with existing-state classification.
- Explicit SSH host-key trust; no silent trust-on-first-use.

## [0.0.1] - 2026-09-01

### Added

- Pre-implementation project context, architecture, safety model, and phased implementation plan.

[Unreleased]: https://github.com/mhdio64/server-bootstrap/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/mhdio64/server-bootstrap/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/mhdio64/server-bootstrap/releases/tag/v0.0.1
