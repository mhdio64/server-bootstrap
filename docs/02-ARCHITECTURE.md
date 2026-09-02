# Architecture — v0.1.0 MVP

## Repository model

v0.1.0 is a standard Ansible project, not an Ansible Collection.

The structure should remain clean enough that a later migration to a Collection is possible without polluting the public API today.

Expected high-level structure after implementation:

```text
server-bootstrap/
├── ansible.cfg
├── site.yml
├── verify.yml
├── VERSION
├── roles/
│   ├── common/
│   ├── users/
│   ├── ssh/
│   ├── firewall/
│   ├── security/
│   └── docker/
├── examples/
│   └── minimal/
├── tests/
├── scripts/
├── requirements-dev.txt
├── .github/
├── README.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```

Exact file layout may evolve during implementation if the same boundaries are preserved.

## Orchestration model

The desired logical flow is:

```text
PLAY 1: read-only global + component preflight
    -> if all critical checks pass

PLAY 2: apply enabled roles
    -> if apply succeeds

PLAY 3: critical verification + summary
```

The central safety property is that a late component should not discover an obvious fatal incompatibility only after earlier roles already mutated the host.

Component-specific classifiers may therefore expose read-only preflight tasks that run before the apply stage.

In check mode, post-apply verification that depends on unapplied changes should not create false failures.

## Roles and ownership

### `common`

Owns:

- OS/version/architecture validation
- APT baseline behavior
- baseline packages
- timezone
- locale
- optional hostname
- time synchronization
- reboot-required detection

Does not own:

- users
- SSH
- firewall
- security policy beyond its own prerequisites
- Docker
- performance tuning

### `users`

Owns:

- one bootstrap/admin user
- home directory
- shell
- sudo integration
- authorized public keys

Does not become a generic user-management framework.

### `ssh`

Owns a dedicated sshd drop-in, not the complete main sshd configuration.

Candidate path:

```text
/etc/ssh/sshd_config.d/00-server-bootstrap.conf
```

The exact filename is implementation-level, but it must preserve reliable OpenSSH precedence and remain clearly project-owned.

Critical validation includes syntax and effective configuration.

### `firewall`

Owns project-created host-firewall policy only.

Backend for MVP: `iptables-nft`.

Public API must not expose backend names unnecessarily.

Never take ownership of Docker-generated chains.

Never globally flush rules.

Persistence must not save/restore a complete snapshot containing transient Docker-managed chains.

### `security`

Intentionally small.

Owns unattended security update policy and a limited set of universally safe security defaults.

### `docker`

Owns:

- existing-state discovery/classification
- approved official repository configuration
- package installation
- service enable/start
- optional approved daemon settings
- optional docker-group membership
- post-install verification

Does not own:

- Swarm
- application containers
- Compose applications
- private registry credentials
- reverse proxy
- TLS
- custom storage architecture
- workload networking
- rootless Docker

## Public configuration API

All user-facing variables use:

```text
bootstrap_*
```

Examples:

```yaml
bootstrap_admin_user:
bootstrap_timezone:
bootstrap_docker_enabled:
bootstrap_firewall_enabled:
bootstrap_firewall_allowed_tcp_ports:
bootstrap_firewall_allowed_udp_ports:
```

Role-internal variables are not public API.

The public API should describe intent rather than implementation backend where possible.

Example:

Preferred:

```yaml
bootstrap_firewall_allowed_tcp_ports:
  - 443
```

Avoid:

```yaml
bootstrap_iptables_rules:
```

## Consumer configuration

Real customer/project inventories and configuration live outside this toolkit repository.

This repository only includes examples.

v0.1.0 consumer layout:

```text
project/
├── inventory.yml    # connection and host data
└── bootstrap.yml    # desired bootstrap_* state
```

Public key file paths in `bootstrap.yml` resolve relative to the directory containing `inventory.yml`.

Long-term:

```text
customer/project config
    -> devops-starter
       -> versioned server-bootstrap
       -> versioned observability-stack
       -> versioned CI/CD components
```

`devops-starter` is intended to be a lightweight composition/orchestration layer, not a monorepo that duplicates component logic.

## Wrapper boundary

A thin wrapper may later offer commands such as:

```text
bootstrap check
bootstrap apply
bootstrap verify
```

The wrapper may:

- validate arguments,
- help with host-key enrollment,
- set log paths,
- run the correct Ansible command,
- preserve exit status.

It must not duplicate configuration-management business logic from Ansible.

## Metadata

A small project-owned target metadata file may record the bootstrap version for troubleshooting.

It is not source of truth.

The Ansible desired-state configuration remains source of truth.

Any metadata timestamp must not cause a second identical run to report changes.
