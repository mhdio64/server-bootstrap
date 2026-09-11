# Full Platform Matrix Acceptance Report

Sanitized full-matrix real-VM acceptance evidence for `server-bootstrap` across all 5 supported operating system targets.

## Execution Metadata

| Field | Value |
|---|---|
| Toolkit version | `0.1.0` |
| Git commit | `edc5eaea7e0ea56a8b441ab7fe93de5d2e2f8956` |
| Matrix run started at (UTC) | 2026-09-11T15:18:42Z |
| Matrix run finished at (UTC) | 2026-09-11T16:26:55Z |
| Vagrant version | `Vagrant 2.4.9` |
| VirtualBox version | `7.2.16r174877` |
| Ansible version | `ansible [core 2.20.1]` |
| Control node Python | `Python 3.14.4` |

## Consolidated Matrix Results

| Gate # | Check / Gate | `ubuntu2404` | `ubuntu2204` | `debian13` | `alma9` | `alma10` |
|:---:|---|:---:|:---:|:---:|:---:|:---:|
| 1 | Fresh VM creation & boot | PASS | PASS | PASS | PASS | PASS |
| 2 | SSH host-key trust enrollment | PASS | PASS | PASS | PASS | PASS |
| 3 | Ansible check mode execution | PASS | PASS | PASS | PASS | PASS |
| 4 | Check mode zero-mutation assertion | PASS | PASS | PASS | PASS | PASS |
| 5 | Preflight idempotence verification | PASS | PASS | PASS | PASS | PASS |
| 6 | First bootstrap apply | PASS | PASS | PASS | PASS | PASS |
| 7 | Post-apply critical verification (`changed=0`) | PASS | PASS | PASS | PASS | PASS |
| 8 | Second bootstrap apply (`changed=0`) | PASS | PASS | PASS | PASS | PASS |
| 9 | VM reboot & SSH reconnect recovery | PASS | PASS | PASS | PASS | PASS |
| 10 | Post-reboot verification (`changed=0`) | PASS | PASS | PASS | PASS | PASS |
| 11 | Firewall persistence across reboot | PASS | PASS | PASS | PASS | PASS |
| 12 | Security update service verified | PASS | PASS | PASS | PASS | PASS |
| 13 | Docker engine & Compose verified | PASS | PASS | PASS | PASS | PASS |
| 14 | Docker `hello-world` smoke test | PASS | PASS | PASS | PASS | PASS |

## Platform Summary

| Target | Vagrant Box | OS / Codename | Architecture | Package Mgr | Firewall | Updates | SELinux | Total Gates | Status |
|---|---|---|---|---|---|---|---|:---:|:---:|
| `ubuntu2404` | `bento/ubuntu-24.04` | Ubuntu 24.04 LTS (Noble) | amd64 | APT | iptables-nft | unattended-upgrades | N/A | 14 / 14 | **PASS** |
| `ubuntu2204` | `bento/ubuntu-22.04` | Ubuntu 22.04 LTS (Jammy) | amd64 | APT | iptables-nft | unattended-upgrades | N/A | 14 / 14 | **PASS** |
| `debian13` | `bento/debian-13` | Debian 13 (Trixie) | amd64 | APT | iptables-nft | unattended-upgrades | N/A | 14 / 14 | **PASS** |
| `alma9` | `almalinux/9` | AlmaLinux 9.x | x86_64 | DNF | firewalld | dnf-automatic | Enforcing | 14 / 14 | **PASS** |
| `alma10` | `almalinux/10` | AlmaLinux 10.x | x86_64 | DNF | firewalld | dnf-automatic | Enforcing | 14 / 14 | **PASS** |

## Attestation

- [x] All 5 platforms independently verified on clean, isolated VirtualBox virtual machines.
- [x] 70 out of 70 acceptance gates passed with zero errors.
- [x] Strict zero-mutation check mode and `changed=0` idempotency validated on every platform.
- [x] Docker engine, Compose plugin, and container execution verified on every platform.
- [x] Enterprise Linux platforms operated cleanly under default SELinux `Enforcing` mode.
- [x] No credentials, private hostnames, or secrets contained in this evidence report.
