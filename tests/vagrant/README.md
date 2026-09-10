# Vagrant Multi-Distribution Acceptance Testing Harness

This directory contains the repeatable local harness for multi-distribution release acceptance on real virtual machines orchestrated with Vagrant and VirtualBox.

## Overview

The harness defines isolated, project-owned VirtualBox VMs for each supported distribution target:

| Target Identifier | Distribution | Vagrant Box | Network IP |
|---|---|---|---|
| `ubuntu2404` | Ubuntu Server 24.04 LTS (amd64) | `bento/ubuntu-24.04` | `192.168.56.24` |
| `ubuntu2204` | Ubuntu Server 22.04 LTS (amd64) | `bento/ubuntu-22.04` | `192.168.56.22` |
| `debian13`   | Debian 13.x Stable "Trixie" (amd64) | `generic/debian13` | `192.168.56.13` |
| `alma9`      | AlmaLinux 9.x (x86_64) | `almalinux/9` | `192.168.56.90` |
| `alma10`     | AlmaLinux 10.x (x86_64) | `almalinux/10` | `192.168.56.10` |

## Prerequisites

- Linux control node (Python 3.12–3.14)
- Vagrant (`>= 2.4.0`)
- Oracle VirtualBox (`>= 7.0`)
- VirtualBox Host-Only network adapter configured for `192.168.56.0/24` (created by default as `vboxnet0`)

## Usage

### Run Full Acceptance Pipeline
To run the full 14-gate acceptance workflow on a fresh VM from scratch:

```bash
./tests/vagrant/run ubuntu2404
# or explicitly:
./tests/vagrant/run ubuntu2404 test
```

This autonomously performs:
1. Safe destruction of any dirty previous VM state for that target
2. Fresh VM provisioning and boot
3. Non-interactive SSH host-key trust enrollment
4. Pre-check host checksum capture (`/etc/hostname`, `/etc/localtime`, etc.)
5. `./bootstrap check` execution
6. Assertion of non-mutation (checksums verified identical)
7. First `./bootstrap apply --yes` execution
8. Critical verification (`./bootstrap verify`)
9. Second `./bootstrap apply --yes` execution (asserting `changed=0`)
10. Target VM reboot and SSH reachability recovery
11. Post-reboot verification (`./bootstrap verify`)
12. Docker engine & Docker Compose verification
13. Docker smoke test (`docker run --rm hello-world`)
14. Writing sanitized acceptance evidence report to `tests/vagrant/evidence/<target>-acceptance-report.md`

### Lifecycle Subcommands
For debugging or focused verification:

```bash
./tests/vagrant/run ubuntu2404 up        # Boot VM
./tests/vagrant/run ubuntu2404 check     # Run check mode
./tests/vagrant/run ubuntu2404 apply     # Run apply
./tests/vagrant/run ubuntu2404 verify    # Run verify
./tests/vagrant/run ubuntu2404 reboot    # Reboot target and wait for SSH
./tests/vagrant/run ubuntu2404 smoke     # Run Docker hello-world smoke test
./tests/vagrant/run ubuntu2404 destroy   # Destroy VM
./tests/vagrant/run ubuntu2404 ssh       # Open interactive SSH shell
./tests/vagrant/run ubuntu2404 status    # Check VM status
```

### Full Matrix Regression
To run acceptance across all 5 targets in sequence:

```bash
./tests/vagrant/run all test
```

## Safety Guarantees

1. **Strict Project Scoping**: All VM names are prefixed (`sb-test-*`) and managed exclusively through `tests/vagrant/Vagrantfile`. Unrelated VirtualBox VMs on the host machine are never affected.
2. **Network Isolation**: The shared `/vagrant` host filesystem folder is disabled. Communication occurs strictly over SSH to emulate a remote physical or cloud server.
3. **No Secret Leakage**: Private keys and dynamic temporary inventories are stored in `tests/vagrant/tmp/` (gitignored). Generated evidence reports in `evidence/` are sanitized and contain no passwords, private keys, or internal customer data.
