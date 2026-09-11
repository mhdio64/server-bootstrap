# Version and Upstream Source Snapshot

Snapshot date: **2026-09-01**

This file is a starting point, not permission to assume versions are still current later.

Before implementing a version-sensitive phase, recheck the official upstream source.

## Ansible Core

Approved line for the MVP:

```text
ansible-core 2.21.x
```

Snapshot exact release:

```text
ansible-core 2.21.3
Released: 2026-08-10
Requires Python >= 3.12
```

Source:

- https://pypi.org/project/ansible-core/
- https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html

Control node Python support for ansible-core 2.21.x: **3.12–3.14**.

Phase 0 pins `ansible-core==2.21.3` after revalidation on 2026-09-02.

## ansible-lint

Snapshot:

```text
ansible-lint 26.8.0
Released: 2026-08-12
```

Source:

- https://pypi.org/project/ansible-lint/

## yamllint

Snapshot:

```text
yamllint 1.38.0
Released: 2026-01-13
```

Source:

- https://pypi.org/project/yamllint/

## Cursor project rules

Current Cursor documentation states:

- Project Rules live under `.cursor/rules/`.
- Project Rules use `.mdc`.
- `AGENTS.md` is supported as a simpler Markdown instruction mechanism.
- Rules are intended for persistent/scoped project guidance.

Source:

- https://cursor.com/docs/rules

## Cursor Agent Skills

Current Cursor documentation states:

- project skills may live under `.cursor/skills/`
- each skill directory contains a `SKILL.md`
- skills are intended for reusable multi-step workflows
- skills can include scripts/references/assets and are loaded progressively

Source:

- https://cursor.com/docs/skills

## Docker Engine on Ubuntu

Implementation must use current official Docker documentation when Phase 6 begins.

Primary sources:

- https://docs.docker.com/engine/install/ubuntu/
- https://docs.docker.com/engine/network/packet-filtering-firewalls/
- https://docs.docker.com/engine/network/firewall-iptables/
- https://docs.docker.com/engine/network/firewall-nftables/
- https://docs.docker.com/engine/logging/configure/

Current architectural policy:

- use the official Docker Ubuntu repository
- do not use the convenience installer
- preserve Docker-owned firewall chains
- MVP host firewall is `iptables-nft`
- native Docker nftables backend is not part of v0.1.0
- Docker daemon logging defaults/settings must be revalidated at implementation time

## Docker Engine Across Target Distributions

Primary sources:
- Ubuntu: https://docs.docker.com/engine/install/ubuntu/
- Debian: https://docs.docker.com/engine/install/debian/
- RHEL / CentOS / AlmaLinux:
  - https://docs.docker.com/engine/install/rhel/
  - https://docs.docker.com/engine/install/centos/
  - https://wiki.almalinux.org/documentation/docker.html

Repository & Key URLs:
- Ubuntu APT repo: `https://download.docker.com/linux/ubuntu` (GPG: `https://download.docker.com/linux/ubuntu/gpg`)
- Debian APT repo: `https://download.docker.com/linux/debian` (GPG: `https://download.docker.com/linux/debian/gpg`)
- AlmaLinux DNF repo: `https://download.docker.com/linux/centos/docker-ce.repo` (GPG: `https://download.docker.com/linux/centos/gpg`)

## Target Operating Systems & Upstream Sources

### Ubuntu Server (22.04 LTS & 24.04 LTS)
- Ubuntu 22.04 LTS (Jammy Jellyfish): https://releases.ubuntu.com/jammy/
- Ubuntu 24.04 LTS (Noble Numbat): https://releases.ubuntu.com/noble/
- Unattended upgrades: https://help.ubuntu.com/community/AutomaticSecurityUpdates
- Firewall stack: `iptables` / `iptables-nft` via netfilter

### Debian 13 "Trixie" (Stable Target)
- Debian Testing / Trixie Release: https://www.debian.org/releases/trixie/
- Debian Security Tracker: https://security-tracker.debian.org/
- Debian UnattendedUpgrades: https://wiki.debian.org/UnattendedUpgrades
- Differences from Ubuntu: Minimal installations may lack `sudo` (must be installed via `apt`); user group is `sudo`; DEB822 format in `/etc/apt/sources.list.d/`.

### AlmaLinux 9 & 10
- AlmaLinux 9 Documentation: https://wiki.almalinux.org/release-notes/9.html
- AlmaLinux 10 Documentation: https://wiki.almalinux.org/
- Red Hat Enterprise Linux 9 / 10 Documentation: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/
- Automatic Security Updates: `dnf-automatic` (`/etc/dnf/automatic.conf`, service timer `dnf-automatic.timer`).
- Firewall: `firewalld` managing nftables backend.
- SELinux: Enforcing by default; policies managed via `policycoreutils` and `setools-console`.

## Vagrant Test Boxes (Verified VirtualBox Providers)

- `ubuntu2404`: `bento/ubuntu-24.04` (https://app.vagrantup.com/bento/boxes/ubuntu-24.04)
- `ubuntu2204`: `bento/ubuntu-22.04` (https://app.vagrantup.com/bento/boxes/ubuntu-22.04)
- `debian13`: `generic/debian13` (https://app.vagrantup.com/generic/boxes/debian13)
- `alma9`: `almalinux/9` (https://app.vagrantup.com/almalinux/boxes/9)
- `alma10`: `almalinux/10` (https://app.vagrantup.com/almalinux/boxes/10)

## Rule for stale facts

When an upstream current fact differs from this snapshot:

1. do not silently rewrite product architecture,
2. distinguish "upstream changed" from "our decision changed",
3. determine whether the change is implementation-only or architectural,
4. implementation-only changes may be applied with documentation update,
5. architecture/security/public behavior changes require explicit human approval.
