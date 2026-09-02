# Project Specification — v0.1.0 MVP

## Product

`server-bootstrap` is a reusable Ansible project for quickly and safely preparing real Linux servers for DevOps workloads.

It is the first component of a future DevOps Toolkit. Other repositories will later handle observability, GitLab CI components, Jenkins shared libraries, and lightweight orchestration through `devops-starter`.

The MVP is not an enterprise hardening framework. It must reach a production-usable baseline quickly without becoming a toy.

## Primary user

A DevOps engineer who receives a fresh VM/VPS or a safely compatible existing server and wants a repeatable baseline without manually configuring the machine.

## Single most important success criterion

Given a reasonably fresh Ubuntu Server 24.04 amd64 host, the operator can provide minimal configuration and run a controlled Ansible workflow that produces a secure, manageable, Docker-ready baseline without manual configuration inside the target.

A second identical apply must produce `changed=0`.

If the target state is dangerous or ambiguous, the project must stop rather than guess.

## Supported platform for v0.1.0

Officially supported:

- Ubuntu Server 24.04 LTS
- amd64 / x86_64
- Linux control node

Not supported in v0.1.0:

- Ubuntu 22.04
- Debian
- AlmaLinux
- Rocky Linux
- RHEL
- ARM64
- macOS control node

The architecture should avoid unnecessary Ubuntu-specific public APIs, but no unused code for future distributions should be written now.

## Primary journey

```text
project configuration
    -> host trust/enrollment
    -> preflight
    -> check/preview
    -> apply
    -> critical verification
    -> summary
```

`check` is strongly recommended but not mandatory.

## Initial access

The first Ansible connection may use:

- `root`, or
- an existing sudo-capable user.

After bootstrap, the created admin user is the recommended identity for ongoing administration.

Root is not deleted or fully locked by default, but routine use is discouraged.

## Minimum configuration

At minimum the operator supplies:

```yaml
bootstrap_admin_user: deploy

bootstrap_admin_authorized_keys:
  - "ssh-ed25519 ..."
```

Authorized public keys may also be sourced from local files.

User private SSH keys are never managed by this repository.

## Default capabilities

The normal bootstrap enables:

- common OS baseline
- admin user
- SSH hardening
- firewall
- security updates
- Docker

High-level feature flags may disable a major capability, but the public API must not become a collection of tiny booleans.

## Common baseline

The `common` capability owns:

- supported OS/version/architecture validation
- APT cache refresh
- practical baseline packages
- timezone
- locale
- optional hostname
- time synchronization
- reboot-required detection
- optional package upgrade only when explicitly enabled

Default timezone: `UTC`.

Default full package upgrade: disabled.

Default automatic reboot: disabled.

Swap state is preserved.

No generic performance tuning, sysctl tuning, or workload-specific limits are applied.

## Admin user

The MVP manages one primary bootstrap/admin user, not a generic IAM system.

Default behavior:

- create if absent
- create/manage home directory
- default shell suitable for administration
- sudo access
- `NOPASSWD` sudo
- authorized public keys
- password locked/unset by default

Existing unrelated users are not removed.

Existing authorized keys are not silently removed.

## SSH

Goals:

- secure defaults
- preserve access
- no risky port-changing trick
- no takeover of the whole main config

Default port: 22.

Changing the port requires explicit configuration.

The implementation owns a dedicated drop-in rather than replacing `/etc/ssh/sshd_config`.

Critical changes must be syntax/effective-config validated before activation.

## Firewall

MVP implementation backend: `iptables-nft`.

Public configuration must remain backend-generic.

Conceptual defaults:

- INPUT: DROP
- FORWARD: DROP
- OUTPUT: ACCEPT
- allow loopback
- allow ESTABLISHED/RELATED
- allow required ICMP/ICMPv6
- automatically allow the effective SSH port
- allow explicitly configured TCP/UDP ports

Docker-owned chains must not be modified or globally flushed.

Published container-port policy is not managed by the MVP.

## Security

MVP security scope is intentionally small:

- unattended security updates
- safe, general-purpose security defaults
- SSH hardening in the SSH role
- firewall policy in the firewall role

Explicitly out of scope:

- CIS compliance
- custom auditd policy
- FIPS
- AIDE
- malware scanning
- custom AppArmor profiles
- enterprise compliance
- aggressive kernel hardening

## Docker

Docker is installed from the official Docker repository.

Expected components:

- Docker Engine
- Docker CLI
- containerd
- Buildx plugin
- Compose plugin (`docker compose`)

Default version policy: latest stable available from the approved repository.

An exact version must be optionally pinnable.

Existing Docker state must be classified before mutation:

- absent -> install is allowed
- compatible official Docker CE -> preserve/reconcile safely
- partial/conflicting/ambiguous -> fail with an actionable message

The project must not silently uninstall/replace a conflicting Docker installation.

Membership in the `docker` group is opt-in.

No `curl | sh` convenience installer.

## Existing-server policy

Core rule:

```text
Known + owned -> reconcile
Unknown + harmless -> preserve
Unknown + consequential -> stop
```

Never destroy unknown configuration silently.

## Check mode

`--check --diff` should be useful and non-mutating wherever technically possible.

Do not fake predictions for operations that cannot be safely predicted.

## Failure recovery

No generic full rollback system.

Use:

- transactional safety for critical configuration changes,
- backups where appropriate,
- idempotent reruns to converge after recoverable partial failures.

## Reboot

Default automatic reboot: disabled.

A required reboot is a warning and successful execution state, not a failure.

## User-facing errors

Safety/preflight errors must be actionable:

- what was detected,
- why execution stopped,
- what the operator should do next.

Public severities are kept simple:

- INFO
- WARNING
- ERROR

## Out of scope for v0.1.0

- AlmaLinux / Rocky Linux
- Ubuntu 22.04
- ARM64
- Kubernetes
- Docker Swarm
- monitoring agents
- CI/CD agents
- application deployment
- reverse proxy
- TLS management
- VPN
- database setup
- generic user management
- CIS compliance
- SELinux logic
- custom AppArmor
- advanced sysctl tuning
- native nftables backend
- rootless Docker
- Ansible Vault workflow
- Molecule
- Terraform/cloud provisioning
- full rollback
- web UI
- TUI
- advanced project generator
