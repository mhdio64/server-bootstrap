# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Multi-distribution expansion delivering full support and real-VM certification across 5 target operating systems.

### Added

- **Multi-Distribution Platform Support**:
  - Ubuntu Server 24.04 LTS (Noble Numbat, amd64)
  - Ubuntu Server 22.04 LTS (Jammy Jellyfish, amd64)
  - Debian 13.x Stable (Trixie, amd64)
  - AlmaLinux 9.x (x86_64)
  - AlmaLinux 10.x (x86_64)
- **Platform Abstraction Layer**:
  - Dynamic loading of OS-family and OS-distribution variable hierarchies across all six roles (`roles/*/tasks/load_platform_vars.yml`).
  - Package management abstraction supporting APT and DNF/DNF5.
  - Service management abstraction (`ssh` on Debian-family, `sshd` on RedHat-family).
  - Privilege escalation abstraction (`sudo` group on Debian-family, `wheel` group on RedHat-family).
- **Enterprise Linux (AlmaLinux 9 & 10) Architecture**:
  - Host firewall role integration with `firewalld` using dedicated permanent rich rules and service allowances.
  - Unattended security updates using `dnf-automatic` with dedicated systemd timer activation.
  - Docker CE official RPM repository setup and engine installation.
  - Automated resolution of required kernel netfilter modules (`kernel-modules-extra` on EL10) for Docker bridge/overlay networking.
  - Full compatibility with SELinux in default `Enforcing` mode with zero policy denials.
- **Debian 13 (Trixie) Architecture**:
  - Security update origins configured for Debian Trixie suites in `unattended-upgrades`.
  - Explicit `sudo` package installation ensured prior to admin user management.
- **Testing and Verification Harness**:
  - Reusable Vagrant test harness (`tests/vagrant/`) supporting fresh multi-machine provisioning for all 5 targets.
  - Automated matrix runner script (`tests/vagrant/run`) with sequential execution, intermediate VM destruction to conserve host memory, and consolidated matrix reporting.
  - Quick-boot optimization (`GRUB_RECORDFAIL_TIMEOUT=0`) and adaptive SSH reachability timeouts.
  - Full matrix acceptance evidence (`tests/vagrant/evidence/full-matrix-acceptance-report.md`) verifying 70 out of 70 acceptance gates passed (14 per platform, 100% PASS).
  - Synthetic multi-distro variable resolution test playbook (`tests/synthetic/playbooks/test_platform_vars_resolution.yml`).
- **Documentation**:
  - Updated `README.md` and `README.fa.md` with complete bilingual parity for all 5 distributions, backends, and caveats.
  - Updated `docs/15-RELEASE-EVIDENCE.md` with multi-distro real-VM matrix results.
  - Updated `docs/14-TROUBLESHOOTING.md` and `docs/13-CONFIGURATION-REFERENCE.md` for multi-platform operations.
  - Multi-distribution roadmap and phased status tracking in `docs/16-MULTI-DISTRO-ROADMAP.md` and `docs/10-PHASE-STATUS.md`.

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
