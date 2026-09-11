# Acceptance Report: debian13

Sanitized real-VM acceptance evidence for target `debian13`.

## Environment Metadata

| Field | Value |
|---|---|
| Target identifier | `debian13` |
| Toolkit version | `0.1.0` |
| Git commit | `78e10bc92e6cc3c63f68ecbab80ff2ce52d69141` |
| Vagrant box | `bento/debian-13` |
| Vagrant version | `Vagrant 2.4.9` |
| VirtualBox version | `7.2.16r174877` |
| Ansible version | `ansible [core 2.20.1]` |
| Python version | `Python 3.14.4` |
| Started at (UTC) | 2026-09-11T11:00:09Z |
| Finished at (UTC) | 2026-09-11T11:08:15Z |

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
