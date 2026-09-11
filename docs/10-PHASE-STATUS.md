# Phase Status

Target release: `v0.1.0`

Current state: **Phase 10 implemented on feature branch; release prepared, not tagged**

## Status table

| Phase | Name | Status |
|---|---|---|
| 0 | Repository foundation | MERGED |
| 1 | Orchestration + global preflight + common | MERGED |
| 2 | Admin user | MERGED |
| 3 | SSH hardening | MERGED |
| 4 | Firewall (`iptables-nft`) | MERGED |
| 5 | Security baseline | MERGED |
| 6A | Docker discovery/preflight | MERGED |
| 6B | Docker repository + installation | MERGED |
| 7 | Verification + summary + metadata | MERGED |
| 8 | Thin wrapper | MERGED |
| 9 | Scenario 1 real-VM validation | MERGED |
| 10 | Documentation + v0.1.0 release preparation | MERGED |

## Multi-Distribution Initiative (MD Phases)

Target: Production multi-distribution support across Ubuntu 22.04, Ubuntu 24.04, Debian 13, AlmaLinux 9, and AlmaLinux 10.

| Phase | Name | Target | Status | Branch | VM Box | Result | Next Phase |
|---|---|---|---|---|---|---|---|
| **MD-0** | Baseline Audit, Roadmap & Vagrant Harness | Ubuntu 24.04 | COMPLETE | `feature/multi-distro-support` | `bento/ubuntu-24.04` | PASS | MD-1 |
| **MD-1** | Platform Abstraction | Ubuntu 24.04 | COMPLETE | `feature/multi-distro-support` | `bento/ubuntu-24.04` | PASS | MD-2 |
| **MD-2** | Ubuntu Server 22.04 LTS Support | Ubuntu 22.04 | COMPLETE | `feature/multi-distro-support` | `bento/ubuntu-22.04` | PASS | MD-3 |
| **MD-3** | Debian 13 Stable "Trixie" Support | Debian 13 | COMPLETE | `feature/multi-distro-support` | `bento/debian-13` | PASS | MD-4 |
| **MD-4** | Enterprise Linux & AlmaLinux 9 Support | AlmaLinux 9 | COMPLETE | `feature/multi-distro-support` | `almalinux/9` | PASS | MD-5 |
| **MD-5** | AlmaLinux 10 Support | AlmaLinux 10 | READY TO START | `feature/multi-distro-support` | `almalinux/10` | — | MD-6 |
| **MD-6** | Full 5-Platform Matrix Acceptance | All 5 targets | NOT STARTED | `feature/multi-distro-support` | All 5 boxes | — | MD-7 |
| **MD-7** | Final Documentation & Release Readiness | All 5 targets | NOT STARTED | `feature/multi-distro-support` | — | — | v0.2.0 Release |

### MD Phase Detail Tracking

#### Phase MD-0
- **Status**: COMPLETE / READY FOR REVIEW
- **Objective**: Full workspace audit, multi-distro roadmap (`docs/16-MULTI-DISTRO-ROADMAP.md`), reusable Vagrant test harness (`tests/vagrant/`), upstream sources update (`docs/09-VERSION-SOURCES.md`), and fresh Ubuntu 24.04 real-VM baseline acceptance across all 14 gates.
- **Branch**: `feature/multi-distro-support`
- **Starting commit**: `66fcb37caa7b1c592e2c72072f4f15348b7ea0ac`
- **Ending commit**: `398f44d03923d51b32d203991278ff56f4d2579b`
- **Important files changed**:
  - `docs/16-MULTI-DISTRO-ROADMAP.md`
  - `docs/10-PHASE-STATUS.md`
  - `docs/00-CONTEXT-INDEX.md`
  - `docs/09-VERSION-SOURCES.md`
  - `AGENTS.md`
  - `.gitignore`
  - `.yamllint`
  - `roles/common/tasks/verify.yml`
  - `roles/docker/handlers/main.yml`
  - `roles/docker/tasks/install_packages.yml`
  - `roles/ssh/tasks/validate_control_node_identity.yml`
  - `roles/users/tasks/build_authorized_keys.yml`
  - `roles/users/tasks/verify.yml`
  - `tasks/preflight/global.yml`
  - `tests/vagrant/Vagrantfile`
  - `tests/vagrant/run`
  - `tests/vagrant/README.md`
  - `tests/vagrant/evidence/ubuntu2404-acceptance-report.md`
- **Tests executed**: Full static validation suite (yamllint, ansible-lint, playbook syntax checks, secret scanning, synthetic preflight tests, Python unit tests, git diff check), real-VM fresh Ubuntu 24.04 acceptance flow.
- **VM target**: `ubuntu2404`
- **Vagrant box**: `bento/ubuntu-24.04`
- **Box version**: `202510.26.0`
- **Test result**: PASS (all 14 acceptance gates passed on fresh VM, evidence captured)
- **Known limitations**: None. Baseline Ubuntu 24.04 is solid, idempotent, and non-mutating in check mode.
- **Unresolved issues**: None.
- **Next phase**: MD-1 (Platform Abstraction) — in progress.
- **Last updated**: 2026-09-11

#### Phase MD-1
- **Status**: COMPLETE / READY FOR REVIEW
- **Objective**: Establish platform abstraction layer across roles, dynamically load OS-family/distro variables, isolate package manager and backend operational mechanics, preserve zero regression for Ubuntu Server 24.04.
- **Branch**: `feature/multi-distro-support`
- **Starting commit**: `d936fa76cc6490938e09e9f71cb75b14ad8c97b0`
- **Important files changed**:
  - `roles/common/` (vars, package_manager sub-tasks, load_platform_vars)
  - `roles/users/` (vars, sudo group abstraction, load_platform_vars)
  - `roles/ssh/` (vars, service name abstraction, load_platform_vars)
  - `roles/firewall/` (vars, backend abstraction, load_platform_vars)
  - `roles/security/` (vars, unattended-upgrades backend sub-tasks, load_platform_vars)
  - `roles/docker/` (vars, repository and package backend sub-tasks, load_platform_vars)
  - `tests/synthetic/playbooks/test_platform_vars_resolution.yml`
  - `tests/synthetic/run-phase1-preflight-tests.sh`
  - `tests/vagrant/evidence/ubuntu2404-acceptance-report.md`
- **Tests executed**: Full static validation suite (yamllint, ansible-lint, playbook syntax checks, secret scanning, synthetic preflight tests, Python unit tests, git diff check), real-VM fresh Ubuntu 24.04 acceptance flow.
- **VM target**: `ubuntu2404`
- **Vagrant box**: `bento/ubuntu-24.04`
- **Test result**: PASS (all 14 acceptance gates passed on fresh VM, evidence captured)
- **Known limitations**: None. Ubuntu 24.04 baseline functionality preserved with zero regression, idempotency verified (`changed=0`), non-mutating check mode verified.
- **Unresolved issues**: None.
- **Next phase**: MD-2 (Ubuntu Server 22.04 LTS Support) — COMPLETE.
- **Last updated**: 2026-09-11

#### Phase MD-2
- **Status**: COMPLETE / READY FOR REVIEW
- **Objective**: Add and certify Ubuntu Server 22.04 LTS ("Jammy", amd64) support across roles, metadata, and assertions without behavior regressions for Ubuntu 24.04.
- **Branch**: `feature/multi-distro-support`
- **Starting commit**: `f2ab7a34c3d31173eccb709aae26ec45b03bcd97`
- **Important files changed**:
  - `roles/common/defaults/main.yml` (`common_supported_distribution_versions: ["22.04", "24.04"]`)
  - `roles/common/tasks/assert_platform.yml` (multi-version assertion support)
  - `roles/*/meta/main.yml` (added `jammy` to all 6 roles)
  - `tests/synthetic/playbooks/test_platform_vars_resolution.yml` (added Ubuntu 22.04 test play)
  - `tests/vagrant/evidence/ubuntu2204-acceptance-report.md` (14-gate acceptance report)
- **Tests executed**: Full static validation suite (yamllint, ansible-lint, playbook syntax checks, secret scanning, synthetic preflight tests, Python unit tests, git diff check), real-VM fresh Ubuntu 22.04 acceptance flow.
- **VM target**: `ubuntu2204`
- **Vagrant box**: `bento/ubuntu-22.04`
- **Box version**: `202510.26.0`
- **Test result**: PASS (all 14 acceptance gates passed on fresh VM, evidence captured)
- **Known limitations**: None. Ubuntu 22.04 LTS fully verified with zero errors, idempotency verified (`changed=0`), non-mutating check mode verified.
- **Unresolved issues**: None.
- **Next phase**: MD-3 (Debian 13 Stable "Trixie" Support) — COMPLETE.
- **Last updated**: 2026-09-11

#### Phase MD-3
- **Status**: COMPLETE / READY FOR REVIEW
- **Objective**: Add and certify Debian 13 Stable ("Trixie", amd64) support across roles, metadata, security update origins, and privilege escalation handling without behavior regressions for Ubuntu 22.04 or 24.04.
- **Branch**: `feature/multi-distro-support`
- **Starting commit**: `78e10bc75f10b7f8373b5eb4833ae819e6ec1d15`
- **Important files changed**:
  - `roles/common/defaults/main.yml` (added Debian to supported distributions and 13 to versions)
  - `roles/common/tasks/assert_platform.yml` (multi-distribution and multi-version assertion)
  - `roles/users/vars/Debian.yml` & `vars/default.yml` (`users_sudo_package: sudo`)
  - `roles/users/tasks/main.yml` (ensured sudo package installed before user management)
  - `roles/security/templates/50server-bootstrap-unattended-upgrades.j2` (Debian security origins)
  - `roles/firewall/tasks/discover_state.yml` (resilient iptables-save detection on minimal images)
  - `roles/firewall/tasks/classify_state.yml` (resilient ufw and iptables version checks)
  - `roles/*/meta/main.yml` (added Debian trixie to all 6 roles)
  - `tests/vagrant/Vagrantfile` (configured `bento/debian-13`)
  - `tests/synthetic/playbooks/test_platform_vars_resolution.yml` (added Debian 13 test play)
  - `tests/vagrant/evidence/debian13-acceptance-report.md` (14-gate acceptance report)
- **Tests executed**: Full static validation suite (yamllint, ansible-lint, playbook syntax checks, secret scanning, synthetic preflight tests, Python unit tests, git diff check), real-VM fresh Debian 13 acceptance flow.
- **VM target**: `debian13`
- **Vagrant box**: `bento/debian-13`
- **Box version**: `202510.26.0`
- **Test result**: PASS (all 14 acceptance gates passed on fresh VM, evidence captured)
- **Known limitations**: None. Debian 13 fully verified with zero errors, idempotency verified (`changed=0`), non-mutating check mode verified.
- **Unresolved issues**: None.
- **Next phase**: MD-4 (Enterprise Linux Architecture & AlmaLinux 9 Support) — COMPLETE.
- **Last updated**: 2026-09-11

#### Phase MD-4
- **Status**: COMPLETE / READY FOR REVIEW
- **Objective**: Add Enterprise Linux architecture support and certify AlmaLinux 9.x (x86_64) across roles, metadata, package manager (DNF), firewall (`firewalld`), security updates (`dnf-automatic`), and Docker CE upstream repository while maintaining SELinux in default Enforcing mode and zero regressions on existing distributions.
- **Branch**: `feature/multi-distro-support`
- **Starting commit**: `13a783ba61025796a2a181a3bdf4d98d265f10d4`
- **Important files changed**:
  - `roles/common/vars/RedHat.yml` & tasks (`dnf_preflight.yml`, `dnf_install.yml`, `assert_platform.yml`, `verify.yml`)
  - `roles/users/vars/RedHat.yml` (`wheel` privilege group)
  - `roles/ssh/vars/RedHat.yml` (`sshd` service name) & `tasks/main.yml` (common SSH args support)
  - `roles/firewall/vars/RedHat.yml` & `tasks/backends/firewalld/` (`firewalld` backend support, check-mode resilience, verify tasks)
  - `roles/security/vars/RedHat.yml`, template `server-bootstrap-automatic.conf.j2`, & tasks (`dnf_automatic.yml`, `dnf_automatic_verify.yml`)
  - `roles/docker/vars/RedHat.yml` & tasks (`backends/dnf/repository.yml`, `backends/dnf/packages.yml`, `discover_state.yml`, `install_packages.yml`, `verify.yml`)
  - `roles/*/meta/main.yml` (added `EL 9` to all 6 roles)
  - `tests/synthetic/playbooks/test_platform_vars_resolution.yml` (added AlmaLinux 9 test play)
  - `tests/vagrant/evidence/alma9-acceptance-report.md` (14-gate acceptance report)
- **Tests executed**: Full static validation suite (yamllint, ansible-lint, playbook syntax checks, secret scanning, synthetic preflight tests, Python unit tests, git diff check), real-VM fresh AlmaLinux 9 acceptance flow.
- **VM target**: `alma9`
- **Vagrant box**: `almalinux/9`
- **Test result**: PASS (all 14 acceptance gates passed on fresh VM, evidence captured)
- **Known limitations**: None. AlmaLinux 9.x fully verified with zero errors, idempotency verified (`changed=0`), non-mutating check mode verified, SELinux enforcing verified.
- **Unresolved issues**: None.
- **Next phase**: MD-5 (AlmaLinux 10 Support) — awaits human authorization.
- **Last updated**: 2026-09-11

