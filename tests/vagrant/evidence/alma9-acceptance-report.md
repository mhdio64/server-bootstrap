# Acceptance Report: alma9

Sanitized real-VM acceptance evidence for target `alma9`.

## Environment Metadata

| Field | Value |
|---|---|
| Target identifier | `alma9` |
| Toolkit version | `0.1.0` |
| Git commit | `13a783ba61025796a2a181a3bdf4d98d265f10d4` |
| Vagrant box | `almalinux/9` |
| Vagrant version | `Vagrant 2.4.9` |
| VirtualBox version | `7.2.16r174877` |
| Ansible version | `ansible [core 2.20.1]` |
| Python version | `Python 3.14.4` |
| Started at (UTC) | 2026-09-11T12:04:26Z |
| Finished at (UTC) | 2026-09-11T12:13:00Z |

## Acceptance Gate Results

| Check / Gate | Result |
|---|---|
| Fresh VM creation & boot | PASS |
| SSH host-key trust enrollment | PASS |
| Ansible check mode execution | PASS |
| Check mode zero-mutation assertion | PASS |
| First bootstrap apply | PASS |
| Post-apply critical verification | PASS |
| Second bootstrap apply (changed=0) | PASS |
| VM reboot & SSH reconnect recovery | PASS |
| Post-reboot verification | PASS |
| Firewall persistence across reboot | PASS |
| Security update service verified | PASS |
| Docker engine service verified | PASS |
| Docker Compose verified | PASS |
| Docker hello-world smoke test | PASS |

## Attestation

- [x] Tested on a fresh, isolated VirtualBox VM via Vagrant harness.
- [x] All 14 required gates completed with zero errors.
- [x] No private credentials, internal hostnames, or customer secrets are contained in this report.
