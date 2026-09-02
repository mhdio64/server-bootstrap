# Accepted Decisions

This file records accepted product/architecture decisions so they are not silently revisited during implementation.

## D-001 — Repository split

The long-term DevOps Toolkit uses separate repositories:

```text
server-bootstrap          # canonical repository (mhdio64/server-bootstrap)
observability-stack
gitlab-ci-components
jenkins-shared-library
devops-starter
```

`devops-starter` is a lightweight composition/orchestration layer, not a monorepo.

## D-002 — MVP platform

v0.1.0 officially supports only:

- Ubuntu Server 24.04 LTS
- amd64
- Linux control node

## D-003 — Scope

v0.1.0 delivers:

- OS baseline
- admin user
- SSH hardening
- firewall
- unattended security updates
- Docker

No Kubernetes, monitoring, CI/CD runner, application deployment, reverse proxy, TLS, databases, or enterprise compliance.

## D-004 — Ansible project first

Use a standard Ansible project for the MVP.

Do not start as an Ansible Collection.

Keep boundaries clean enough to migrate later if justified.

## D-005 — Public variable namespace

Public variables use `bootstrap_*`.

Backend implementation names should not unnecessarily leak into the public API.

## D-006 — Existing configuration

Policy:

```text
Known + owned -> reconcile
Unknown + harmless -> preserve
Unknown + consequential -> stop
```

## D-007 — Admin model

Support initial connection through root or an existing sudo user.

Create one primary admin user.

Default admin authentication:

- SSH public key
- password locked/unset
- NOPASSWD sudo

Private keys are never managed.

## D-008 — SSH management

Use a project-owned sshd drop-in.

Do not replace the entire main sshd config.

Changing the SSH port is opt-in.

Validate before reload.

## D-009 — Firewall

Use `iptables-nft` for the MVP.

Do not use UFW.

Do not use `iptables-legacy`.

Do not use native Docker nftables backend for the MVP.

Keep public firewall variables generic to make a future backend migration possible.

## D-010 — Docker firewall boundary

Docker owns Docker-generated chains.

The bootstrap project does not globally flush firewall rules and does not implement workload-specific published-container-port policy.

## D-011 — Docker installation

Use the official Docker repository and explicit packages.

No convenience installer.

Default latest stable, optional exact pin.

Classify existing Docker state before mutation.

Do not silently uninstall/migrate conflicts.

## D-012 — Docker group

Default Docker user list is empty.

Adding a user to the `docker` group is explicit opt-in because it grants root-equivalent capability.

## D-013 — Package upgrade/reboot

Full system package upgrade: opt-in.

Automatic reboot: disabled by default.

Reboot required is reported as a successful warning state.

## D-014 — Swap and performance tuning

Preserve existing swap.

No generic performance/sysctl tuning in v0.1.0.

## D-015 — Idempotency

Second identical apply must produce `changed=0`.

## D-016 — Check mode

Useful non-mutating `--check --diff` support is required where technically honest.

## D-017 — Rollback

No generic full rollback.

Use transactional handling for critical config and safe idempotent rerun elsewhere.

## D-018 — Testing

Real Ubuntu 24.04 amd64 Scenario 1 VM validation is a release gate.

Molecule is not required for v0.1.0.

Real Scenario 2 existing-server VM validation is post-MVP.

## D-019 — Supply chain

Prefer `ansible.builtin`.

External dependencies require justification and pinning.

GitHub Actions should use full commit SHA pins.

Dependency PRs are reviewed; no dependency auto-merge.

## D-020 — Cursor autonomy

Cursor may automate implementation, testing, Git branches/commits/push/PR, and CI repair for approved phases.

Human approval is required for architecture changes, merge, tag, and release.

## D-021 — Repository visibility

Initial development may remain private.

Public release follows Scenario 1 validation, CI success, documentation cleanup, and review.

## D-022 — License

MIT.

## D-023 — Future distribution support

Do not write unused AlmaLinux/Rocky logic now.

When those distributions are added, revalidate current vendor behavior rather than assuming RHEL repository identity. Docker's upstream download infrastructure has previously exposed distro-specific AlmaLinux/Rocky repository trees; that fact must be freshly rechecked at implementation time.

## D-024 — Canonical repository name

The canonical GitHub repository is `mhdio64/server-bootstrap`.

Prior work in `ansible-server-bootstrap` is audit input only and must be selectively migrated with naming normalized to `server-bootstrap`.

## D-025 — Consumer configuration contract

Project configuration uses two files outside this toolkit repository:

- `inventory.yml` — connection and host data
- `bootstrap.yml` — desired `bootstrap_*` state

Public key file paths resolve relative to the directory containing `inventory.yml`. Absolute paths are also allowed.

## D-026 — Wrapper and host trust

v0.1.0 includes a thin Python stdlib wrapper with `check`, `apply`, and `verify` commands.

Host trust must support `--expected-host-fingerprint` and interactive approval. Silent trust-on-first-use is forbidden.

Interactive `apply` requires explicit confirmation; `--yes` enables automation.

Each invocation accepts exactly one target host.

## D-027 — Firewall ownership and activation

Firewall persistence uses project-owned chains and a dedicated restore mechanism. Unknown consequential foreign policy stops in preflight.

Activation uses staged apply with timed rollback until connectivity and policy health are confirmed.

## D-028 — SSH activation rollback

If SSH reconnect verification fails after activating the project drop-in, rollback the project-owned file, reload SSH, and fail with a clear error.

## D-029 — Docker version and daemon policy

`bootstrap_docker_version: latest` installs latest stable on fresh hosts and preserves compatible existing official installs without implicit upgrade.

Requested downgrades stop with an actionable message.

Valid existing `daemon.json` files are preserved by default. Fresh hosts may receive `log-driver: local` after upstream revalidation.

## D-030 — Control node Python

Officially supported control-node Python versions: 3.12, 3.13, and 3.14.
