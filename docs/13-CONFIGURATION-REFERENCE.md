# Configuration Reference

This document describes the public `bootstrap_*` configuration API for `server-bootstrap`.

Source of truth for desired state is your project `bootstrap.yml`. Connection data belongs in `inventory.yml`.

## Layout

```text
your-project/
├── inventory.yml    # Ansible connection and host data
└── bootstrap.yml    # desired bootstrap_* state
```

Paths in `bootstrap_admin_authorized_key_files` resolve relative to the directory containing `inventory.yml` unless absolute.

## Required variables

| Variable | Type | Description |
|---|---|---|
| `bootstrap_admin_user` | string | Primary admin account name (must not be `root`). |
| `bootstrap_admin_authorized_keys` and/or `bootstrap_admin_authorized_key_files` | list | At least one SSH public key source for the admin account. |

## Feature flags

All major capabilities are enabled by default. Set a flag to `false` only with deliberate intent; check, apply, and summary emit prominent warnings when a security-related component is disabled.

| Variable | Default | Description |
|---|---|---|
| `bootstrap_common_enabled` | `true` | OS baseline, timezone, packages, time sync. |
| `bootstrap_users_enabled` | `true` | Admin user, privilege escalation (`sudo`/`wheel`), authorized keys. |
| `bootstrap_ssh_enabled` | `true` | SSH hardening via project-owned drop-in. |
| `bootstrap_firewall_enabled` | `true` | Project-owned host firewall (`iptables-nft` on Debian/Ubuntu, `firewalld` on EL). |
| `bootstrap_security_enabled` | `true` | Unattended security updates (`unattended-upgrades` on Debian/Ubuntu, `dnf-automatic` on EL). |
| `bootstrap_docker_enabled` | `true` | Official Docker CE installation from upstream repositories. |

## Common baseline

| Variable | Default | Description |
|---|---|---|
| `bootstrap_timezone` | `UTC` | System timezone (`timedatectl`). |
| `bootstrap_upgrade_packages` | `false` | When `true`, run a full distribution upgrade (`apt dist-upgrade` on Debian/Ubuntu, `dnf upgrade` on Enterprise Linux). |
| `bootstrap_reboot_if_required` | `false` | When `true`, reboot if a reboot is pending after changes (`/var/run/reboot-required` on Debian/Ubuntu, `needs-restarting -r` on Enterprise Linux). |
| `bootstrap_common_packages` | see role defaults | Baseline package set managed by the project. |
| `bootstrap_common_packages_extra` | `[]` | Additional packages to install with the baseline set. |
| `bootstrap_hostname` | unset | Optional hostname. When unset, preserve the current hostname. |
| `bootstrap_locale` | unset | Optional locale (for example `en_US.UTF-8`). When unset, preserve a valid existing locale. |

## Admin user

| Variable | Default | Description |
|---|---|---|
| `bootstrap_admin_authorized_key_files` | `[]` | Local public key files on the control node. |
| `bootstrap_admin_shell` | `/bin/bash` | Shell used when creating a new admin account. |

Existing admin accounts are classified before mutation. Password, home, and consequential shell state are preserved unless explicitly incompatible. The admin user is granted passwordless privilege escalation via the `sudo` group on Debian/Ubuntu and the `wheel` group on Enterprise Linux.

## SSH

| Variable | Default | Description |
|---|---|---|
| `bootstrap_ssh_port` | unset | Optional SSH port. When unset, preserve the effective port on the target. Fresh hosts typically use port 22. |

SSH hardening uses a project-owned drop-in under `/etc/ssh/sshd_config.d/`. Password authentication is disabled; public-key access is required. Service reload uses `ssh` on Debian/Ubuntu and `sshd` on Enterprise Linux.

## Firewall

| Variable | Default | Description |
|---|---|---|
| `bootstrap_firewall_allowed_tcp_ports` | `[]` | Additional allowed inbound TCP ports (`1..65535`). SSH is always allowed. |
| `bootstrap_firewall_allowed_udp_ports` | `[]` | Additional allowed inbound UDP ports (`1..65535`). |

Backend specifics:
- **Debian / Ubuntu**: Uses dedicated project-owned `iptables-nft` chains with an emergency rollback watchdog.
- **Enterprise Linux (AlmaLinux 9 / 10)**: Uses permanent rich-rules and service allowances through `firewalld`.

Public API accepts individual ports only. Ranges and source-based rules are out of scope for the current baseline.

## Security updates

Automatic reboot after unattended upgrades is disabled by default.

- **Debian / Ubuntu**: Configures `unattended-upgrades` targeting official distribution security suites.
- **Enterprise Linux (AlmaLinux 9 / 10)**: Configures `dnf-automatic` with security update filters and enabled systemd timer.

## Docker

| Variable | Default | Description |
|---|---|---|
| `bootstrap_docker_version` | `latest` | On fresh hosts, install latest stable from official upstream Docker repositories (APT for Debian/Ubuntu, DNF/RPM for Enterprise Linux). On compatible existing official installs, preserve without implicit upgrade. Exact pins may upgrade; downgrades stop with an error. |
| `bootstrap_docker_users` | `[]` | Users to add to the `docker` group. Empty by default because group membership grants root-equivalent access. |

## Target metadata

After a successful apply, the toolkit may write:

```text
/var/lib/server-bootstrap/metadata.json
```

This file records the bootstrap toolkit version only. It is troubleshooting metadata, not source of truth. A second identical apply does not rewrite it unless the toolkit version changes.

## Example

See `examples/minimal/bootstrap.yml` and `examples/minimal/inventory.yml`.
