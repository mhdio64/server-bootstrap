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

## OpenSSH

Primary source for configuration semantics:

- https://man.openbsd.org/sshd_config.5

Implementation must validate both syntax and effective configuration.

## Rule for stale facts

When an upstream current fact differs from this snapshot:

1. do not silently rewrite product architecture,
2. distinguish "upstream changed" from "our decision changed",
3. determine whether the change is implementation-only or architectural,
4. implementation-only changes may be applied with documentation update,
5. architecture/security/public behavior changes require explicit human approval.
