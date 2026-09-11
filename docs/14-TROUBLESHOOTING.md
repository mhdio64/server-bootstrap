# Troubleshooting

## Quick checks

1. Confirm platform support: Ubuntu Server 22.04 / 24.04 LTS, Debian 13, AlmaLinux 9 / 10 (amd64 / x86_64).
2. Confirm control node Python 3.12–3.14 and Ansible from `requirements-dev.txt`.
3. Run `./bootstrap check -i inventory.yml` before apply when practical.
4. Run `./bootstrap verify -i inventory.yml` after apply.
5. Inspect wrapper logs under `${XDG_STATE_HOME:-~/.local/state}/server-bootstrap/logs`.

## SSH and access

### Host key trust rejected or blocked

The wrapper never silently trusts a new host.

- Compare the presented fingerprint out-of-band.
- Re-run with `--expected-host-fingerprint SHA256:...`, or approve interactively when prompted.

### No control-node identity matches admin keys

Preflight stops before SSH hardening if no loaded control-node key matches `bootstrap_admin_authorized_keys`.

- Set `ansible_ssh_private_key_file` in `inventory.yml`, or load the matching key into `ssh-agent`.
- Ensure the public key in `bootstrap.yml` matches the private key you use to connect.

### Locked out after SSH changes

The SSH role rolls back the project-owned drop-in if reconnect verification fails. If you are locked out:

- Use provider console or out-of-band access.
- Remove or fix `/etc/ssh/sshd_config.d/00-server-bootstrap.conf`.
- Reload SSH (`systemctl reload ssh` on Debian/Ubuntu, `systemctl reload sshd` on Enterprise Linux) and restore key-based access before retrying.

## Firewall

### Preflight stops on foreign firewall policy (Debian / Ubuntu)

Unknown consequential firewall state stops before mutation. Common causes:

- active UFW enforcement,
- unexpected `iptables` policy outside project-owned chains,
- non-`iptables-nft` backend.

Disable conflicting managers only after understanding the impact. This project does not globally flush rules.

### Enterprise Linux (`firewalld` backend)

On AlmaLinux 9 and 10, the firewall role configures dedicated permanent rich-rules and service allowances through `firewalld`:

- Verify service status: `systemctl status firewalld`.
- Inspect active rules: `firewall-cmd --list-all`.
- Ensure external interfaces are assigned to the default zone or explicit allowed zones.

### SSH works but other ports do not

Only ports listed in `bootstrap_firewall_allowed_tcp_ports` / `bootstrap_firewall_allowed_udp_ports` are opened, plus SSH. Published Docker container ports are not managed by this baseline.

## Automatic Security Updates

### Debian / Ubuntu (`unattended-upgrades`)

- Check service: `systemctl status unattended-upgrades`.
- Inspect update logs: `/var/log/unattended-upgrades/unattended-upgrades.log`.

### Enterprise Linux (`dnf-automatic`)

- Check timer: `systemctl status dnf-automatic.timer` (or `dnf-automatic-install.timer`).
- Verify configuration: `/etc/dnf/automatic.conf`.

## Docker

### Conflicting or partial Docker installation

Preflight classifies existing Docker state. Only `absent` and `official_compatible` may proceed automatically.

- Remove conflicting packages such as distribution-packaged `docker.io` or `podman-docker` manually, or
- reconcile to an official compatible install before retrying.

### Kernel modules on Enterprise Linux 10

Docker requires bridge and NAT netfilter modules (`xt_addrtype`, `br_netfilter`). On AlmaLinux 10, ensure `kernel-modules-extra` is installed for the running kernel (`roles/docker` installs this automatically).

### Downgrade requested

`bootstrap_docker_version` cannot request a version older than the installed `docker-ce` package. Upgrade intentionally with a higher pin instead.

### `docker` group membership

Users are not added to the `docker` group unless listed in `bootstrap_docker_users`.

## SELinux on Enterprise Linux

The toolkit is designed to run with SELinux in default `Enforcing` mode on AlmaLinux 9 and 10:

- If permission issues occur with custom paths outside standard system locations, check the audit log:
  ```bash
  ausearch -m avc -ts recent
  ```
- Ensure file security contexts are restored if files are copied manually outside Ansible (`restorecon -Rv /path`).

## Idempotency and check mode

### Second apply reports changes

Inspect the PLAY RECAP and task names. Common causes:

- metadata or file content drift outside project ownership,
- upstream package updates when not pinned,
- timestamp-only rewrites (report as a defect).

### Check mode appears to fail on discovery tasks

Read-only preflight and discovery run outside Ansible check mode so validation remains honest. Check mode should still not mutate the host.

## Reboot required

If `/var/run/reboot-required` (Debian/Ubuntu) or `needs-restarting -r` (Enterprise Linux) indicates a reboot is pending after package upgrades, bootstrap completes successfully with a warning. Reboot manually or set `bootstrap_reboot_if_required: true` on a subsequent run.

## Getting more help

- Configuration: `docs/13-CONFIGURATION-REFERENCE.md`
- Safety model: `docs/03-SECURITY-SAFETY.md`
- Release evidence: `docs/15-RELEASE-EVIDENCE.md`
- Security reports: `SECURITY.md`
