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

## Security updates and hardening

Automatic reboot after unattended upgrades is disabled by default.

- **Debian / Ubuntu**: Configures `unattended-upgrades` targeting official distribution security suites.
- **Enterprise Linux (AlmaLinux 9 / 10)**: Configures `dnf-automatic` with security update filters and enabled systemd timer.

### Hardening controls

| Variable | Default | Description |
|---|---|---|
| `bootstrap_security_auditd_enabled` | `true` | Installs and enables `auditd` with rules monitoring critical authentication and system configuration files. |
| `bootstrap_security_sysctl_enabled` | `true` | Deploys `/etc/sysctl.d/99-server-bootstrap-hardening.conf` (SYN cookies, reverse path filtering, martian logging, redirect disabling, ASLR/ptrace restrictions) while preserving container bridge forwarding. |
| `bootstrap_security_modprobe_blacklist_enabled` | `true` | Blacklists uncommon legacy protocols (`dccp`, `sctp`, `rds`, `tipc`) and obsolete filesystems (`cramfs`, `freevxfs`, `jffs2`, `hfs`, `hfsplus`, `udf`) and `usb-storage`. |
| `bootstrap_security_coredump_disabled` | `true` | Disables core dumps for all users via `/etc/security/limits.d/10-server-bootstrap-limits.conf`. |
| `bootstrap_security_login_defs_enabled` | `true` | Configures `UMASK 027`, password aging policies (`PASS_MAX_DAYS 90`), and cryptographic rounds (`SHA_CRYPT_MIN_ROUNDS 5000`) in `/etc/login.defs`. |
| `bootstrap_security_banner_enabled` | `true` | Deploys legal warning notices to `/etc/issue` and `/etc/issue.net`. |
| `bootstrap_security_file_permissions_enabled` | `true` | Restricts permissions on sensitive system files (`/etc/crontab` to 0600, `/etc/cron.*` to 0700, `/etc/ssh/sshd_config` to 0600). |
| `bootstrap_security_fail2ban_enabled` | `true` | Installs and enables `fail2ban` service on supported distributions (Debian/Ubuntu). |

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

## Wrapper CLI (`./bootstrap`)

The wrapper provides a controlled interface to run Ansible playbooks with safety and host trust checks. Supported subcommands: `check`, `apply`, and `verify`.

| Option | Short | Subcommands | Description |
|---|---|---|---|
| `--inventory` | `-i` | `check`, `apply`, `verify` | Path to inventory file with connection data for exactly one target host (required). |
| `--extra-vars` | `-e` | `check`, `apply`, `verify` | Path to `bootstrap.yml` (defaults to `bootstrap.yml` beside `inventory.yml`). |
| `--expected-host-fingerprint` | | `check`, `apply`, `verify` | Expected SSH host-key fingerprint (`SHA256:...`) for out-of-band trust enrollment. |
| `--ask-pass` | `-k` | `check`, `apply`, `verify` | Prompt for SSH connection password (requires `sshpass` on control node). |
| `--ask-become-pass` | `-K` | `check`, `apply`, `verify` | Prompt for privilege escalation (`sudo`) password. |
| `--yes` | | `apply` | Skip interactive apply confirmation. |

### Common CLI invocations

- **Standard run (key-based SSH with root or passwordless sudo):**
  ```bash
  ./bootstrap apply -i inventory.yml
  ```
- **Initial run with non-root user and password (prompts for SSH & sudo passwords):**
  ```bash
  ./bootstrap apply -i inventory.yml -k -K
  ```
- **SSH key login, but non-root user requires sudo password:**
  ```bash
  ./bootstrap apply -i inventory.yml -K
  ```

## Example

See `examples/minimal/bootstrap.yml` and `examples/minimal/inventory.yml`.
