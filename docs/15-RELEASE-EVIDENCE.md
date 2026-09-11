# Release Evidence — Multi-Distribution Expansion

This document summarizes release-gate evidence for the multi-distribution baseline. It does **not** create a Git tag or GitHub Release.

## Release Readiness

Tagging and publishing require explicit human approval per `AGENTS.md`.

## Supported matrix

| Component | Supported |
|---|---|
| Target OS | Ubuntu Server 24.04 LTS (Noble)<br>Ubuntu Server 22.04 LTS (Jammy)<br>Debian 13.x (Trixie)<br>AlmaLinux 9.x<br>AlmaLinux 10.x |
| Target architecture | amd64 / x86_64 |
| Control node OS | Linux |
| Control node Python | 3.12, 3.13, 3.14 |
| Ansible | `ansible-core` 2.21.x (pinned in `requirements-dev.txt`) |

Not supported: ARM64, Windows/macOS control nodes, Kubernetes, monitoring agents, application deployment, foreign firewall managers outside project-owned rules (e.g., UFW), Docker Swarm, rootless Docker.

## Static validation (CI)

GitHub Actions on `main` runs, per Python 3.12/3.13/3.14:

- dependency install sanity
- `yamllint`
- `ansible-lint` (166 files across roles, playbooks, and tasks)
- Ansible syntax checks for `site.yml` and `verify.yml`
- secret scanning and negative secret-gate test
- synthetic multi-distro variable resolution tests (`test_platform_vars_resolution.yml`)
- synthetic classifier/preflight tests (`run-phase1-preflight-tests.sh`)
- wrapper unit tests (`python3 -m unittest discover tests/unit`)
- `git diff --check`

## Full 5-Platform Acceptance Matrix

All 5 platforms are certified on clean, isolated virtual machines using the automated Vagrant harness in `tests/vagrant/`.

Consolidated report:
- `tests/vagrant/evidence/full-matrix-acceptance-report.md`

Target-specific acceptance reports:
- Ubuntu Server 24.04 LTS: `tests/vagrant/evidence/ubuntu2404-acceptance-report.md`
- Ubuntu Server 22.04 LTS: `tests/vagrant/evidence/ubuntu2204-acceptance-report.md`
- Debian 13 (Trixie): `tests/vagrant/evidence/debian13-acceptance-report.md`
- AlmaLinux 9.x: `tests/vagrant/evidence/alma9-acceptance-report.md`
- AlmaLinux 10.x: `tests/vagrant/evidence/alma10-acceptance-report.md`

### 14 Acceptance Gates per Target (70 / 70 Gates Passed)

Every target independently passed the full 14-gate acceptance flow:

| # | Acceptance Gate | Verification | Result |
|---|---|---|---|
| 1 | Box availability & initialization | Vagrant provision & inventory generation | PASS |
| 2 | Preflight syntax & connection | Ping and fact discovery | PASS |
| 3 | Safe check mode preview | Execution with zero host mutation | PASS |
| 4 | First bootstrap apply | Full run with expected tasks changed | PASS |
| 5 | Admin SSH & privilege escalation | Key authentication & passwordless sudo/wheel | PASS |
| 6 | Direct root SSH disabled | Root key/password login rejected | PASS |
| 7 | Password authentication disabled | Password-based login rejected | PASS |
| 8 | Host firewall active | `iptables-nft` or `firewalld` active, ports verified | PASS |
| 9 | Automatic security updates | `unattended-upgrades` or `dnf-automatic` active | PASS |
| 10 | Docker CE engine & Compose | Engine and Compose operational | PASS |
| 11 | Post-apply verification playbook | All verify assertions pass | PASS |
| 12 | Second apply idempotency | Playbook runs with `changed=0` | PASS |
| 13 | Reboot recovery | VM reboots and returns to healthy state | PASS |
| 14 | Post-reboot verify & Docker smoke | All assertions pass; `hello-world` container runs | PASS |

### Enterprise Linux & SELinux Compliance

On AlmaLinux 9 and 10:
- Verified with SELinux in default `Enforcing` mode.
- Zero SELinux policy violations or access denials encountered.
- Docker daemon bridge and overlay networking verified with appropriate kernel modules (`kernel-modules-extra` on EL10).

## Known limitations

- Single target per invocation for explicit operator oversight.
- Automatic rollback guards protect critical access points (SSH and firewall); general convergence relies on idempotent rerun.
- Firewall manages project-owned policy only (`iptables-nft` chains on Debian/Ubuntu, dedicated rich-rules/services in `firewalld` on EL); Docker-generated chains and published container ports are out of scope.
- `bootstrap_docker_version: latest` preserves compatible existing installs without implicit upgrade.

## Human release checklist

Before tagging a release:

1. Confirm `main` CI is green across Python 3.12, 3.13, and 3.14.
2. Confirm `./tests/vagrant/run all test` passed and matrix evidence is recorded.
3. Review `CHANGELOG.md`, `README.md`, and `README.fa.md`.
4. Explicitly approve Git tag and GitHub Release creation per `AGENTS.md`.
