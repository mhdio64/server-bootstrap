# Multi-Distribution Roadmap — `server-bootstrap`

## 1. Goal & Mission

Evolve `server-bootstrap` from a single-target project (Ubuntu Server 24.04 LTS) into a production-quality, multi-distribution Ansible bootstrap system for DevOps workloads.

The final supported matrix must be:

```text
Ubuntu Server 22.04 LTS — amd64
Ubuntu Server 24.04 LTS — amd64
Debian 13.x Stable "Trixie" — amd64
AlmaLinux 9.x — x86_64
AlmaLinux 10.x — x86_64
```

Each platform must achieve identical safety guarantees, idempotent execution (`changed=0` on second run), non-mutating check mode, post-reboot resilience, Docker readiness, and verification on real VirtualBox virtual machines.

---

## 2. Supported Scope

| Distribution | Release / Codename | Architecture | Package Manager | Firewall Backend | Security Update Backend | SELinux Mode |
|---|---|---|---|---|---|---|
| **Ubuntu Server 22.04 LTS** | 22.04 (Jammy Jellyfish) | amd64 (x86_64) | APT | `iptables-nft` / project chain | `unattended-upgrades` | N/A (AppArmor default) |
| **Ubuntu Server 24.04 LTS** | 24.04 (Noble Numbat) | amd64 (x86_64) | APT | `iptables-nft` / project chain | `unattended-upgrades` | N/A (AppArmor default) |
| **Debian 13.x Stable** | 13 (Trixie) | amd64 (x86_64) | APT (DEB822 / sources) | `iptables-nft` / project chain | `unattended-upgrades` | N/A (AppArmor default) |
| **AlmaLinux 9.x** | 9.x | x86_64 | DNF (v4) | `firewalld` (or native nftables) | `dnf-automatic` | Enforcing |
| **AlmaLinux 10.x** | 10.x | x86_64 | DNF (v5) | `firewalld` (or native nftables) | `dnf-automatic` | Enforcing |

---

## 3. Non-Goals

The following are strictly out of scope for this initiative:

- **Distributions**: No Rocky Linux, CentOS Stream, Fedora, RHEL directly, openSUSE, Alpine, Arch, or generic BSD support.
- **Architectures**: amd64 / x86_64 only. No ARM64 (aarch64), RISC-V, or 32-bit platforms.
- **Workloads & Stacks**: No application deployments, Kubernetes, Docker Swarm, web servers (Nginx/Caddy/Apache), reverse proxies, monitoring agents, or databases.
- **Infrastructure & Cloud**: No Terraform, OpenTofu, AWS/GCP/Azure modules, or cloud-init generators.
- **Secrets Management**: No HashiCorp Vault, cloud KMS, or runtime secret stores.
- **Control Node**: Linux only (Python 3.12–3.14). macOS and Windows control nodes remain unsupported.

---

## 4. Architectural Strategy

The project avoids scattering distribution conditionals (`when: ansible_distribution == ...`) across individual tasks. Instead, it adopts a clean, layered platform abstraction:

```text
                 Public bootstrap intent
               (bootstrap_* variables API)
                            |
                            v
                   Platform detection
            (distribution, version, family)
                            |
            +---------------+---------------+
            |                               |
            v                               v
     Debian-family layer          Enterprise Linux layer
     (APT, sudo group)              (DNF, wheel group)
            |                               |
       +----+----+                          |
       |         |                          |
       v         v                          v
    Ubuntu     Debian                   AlmaLinux
   (22 / 24)  (Trixie)                  (9 / 10)
```

### Core Abstraction Principles
1. **Public API Neutrality**: Variables describe operator intent (e.g. `bootstrap_firewall_allowed_tcp_ports`), never backend mechanisms (`bootstrap_iptables_ports` or `bootstrap_firewalld_ports`).
2. **Layered Variables**: Role defaults provide common baselines. Platform-specific variable files (`vars/Debian.yml`, `vars/RedHat.yml`, `vars/Ubuntu-24.04.yml`, etc.) define package names, service units, and configuration paths.
3. **Dedicated Sub-task Files**: When package managers or operational mechanics diverge (such as repository signing or firewall rule persistence), roles include dedicated implementation tasks rather than inline complex conditionals.
4. **Preservation of Safety Invariants**:
   - Known + owned state -> reconcile safely.
   - Unknown + harmless state -> preserve.
   - Unknown + consequential state -> stop and report.
5. **No Blind Flushing**: Never globally flush foreign iptables or firewalld rules.
6. **SELinux Invariant**: Operate cleanly within default `Enforcing` mode on Enterprise Linux; never disable or put SELinux into permissive mode without explicit authorization.

---

## 5. Phase Definitions & Progression

The multi-distribution initiative is partitioned into 8 sequential phases:

```text
[MD-0] Baseline Audit & Vagrant Harness
   |
[MD-1] Platform Abstraction (Ubuntu 24.04 only)
   |
[MD-2] Ubuntu Server 22.04 LTS Support
   |
[MD-3] Debian 13 Stable Support
   |
[MD-4] Enterprise Linux Architecture + AlmaLinux 9
   |
[MD-5] AlmaLinux 10 Support
   |
[MD-6] Full 5-Platform Matrix Acceptance
   |
[MD-7] Final Documentation & Release Readiness
```

### Phase Details

#### MD-0: Baseline Audit, Multi-Distro Roadmap & Vagrant Harness
- **Scope**: Audit workspace, set up persistent tracking (`docs/10-PHASE-STATUS.md`), draft durable roadmap (`docs/16-MULTI-DISTRO-ROADMAP.md`), update version sources (`docs/09-VERSION-SOURCES.md`), build reusable Vagrant test harness in `tests/vagrant/`, and validate the existing Ubuntu 24.04 baseline on a fresh VM.
- **Exit Gate**: Static tests pass; fresh Ubuntu 24.04 VM passes full 9-step acceptance flow; sanitized baseline report committed.

#### MD-1: Platform Abstraction Layer
- **Scope**: Restructure roles to load OS-family and OS-specific variables, isolate package manager and service name definitions, and prepare task boundaries for multi-distro backends. Official support remains Ubuntu 24.04 only during this phase.
- **Exit Gate**: All static tests pass; Ubuntu 24.04 re-tested on fresh VM with zero behavior regressions; second apply produces `changed=0`.

#### MD-2: Ubuntu Server 22.04 LTS Support
- **Scope**: Add Ubuntu 22.04 LTS (Jammy) support. Validate kernel/nftables versions, APT repository behavior, Docker repository differences, and unattended-upgrades.
- **Exit Gate**: Fresh Ubuntu 22.04 VM passes full acceptance; Ubuntu 24.04 regression passes.

#### MD-3: Debian 13 Stable "Trixie" Support
- **Scope**: Add Debian 13 support. Research Debian-specific defaults (`sudo` group and availability, DEB822 repository format, security update origins, OpenSSH defaults, systemd service names).
- **Exit Gate**: Fresh Debian 13 VM passes full acceptance; Ubuntu 22.04 and 24.04 regressions pass.

#### MD-4: Enterprise Linux Architecture & AlmaLinux 9 Support
- **Scope**: Build the Enterprise Linux layer. Implement DNF package management, `wheel` group administration, `firewalld` backend integration, `dnf-automatic` security updates, and Docker CE repository for EL9. Ensure full compatibility with SELinux in Enforcing mode.
- **Exit Gate**: Fresh AlmaLinux 9 VM passes full acceptance; Debian-family regressions pass.

#### MD-5: AlmaLinux 10 Support
- **Scope**: Extend the Enterprise Linux layer to AlmaLinux 10 (DNF 5, updated crypto policies, OpenSSH drop-in changes, EL10 Docker repo).
- **Exit Gate**: Fresh AlmaLinux 10 VM passes full acceptance; AlmaLinux 9 and Debian-family regressions pass.

#### MD-6: Full Five-Platform Matrix Acceptance
- **Scope**: Execute autonomous, end-to-end fresh VM acceptance across all 5 targets:
  `ubuntu2204`, `ubuntu2404`, `debian13`, `alma9`, `alma10`.
- **Exit Gate**: 5 out of 5 platforms independently pass the complete acceptance flow.

#### MD-7: Final Documentation & Release Readiness
- **Scope**: Final documentation alignment (`README.md`, `README.fa.md`, architecture guides, configuration references, release evidence, changelog). Verify zero stale references.
- **Exit Gate**: Clean Git worktree; full static validation clean; release evidence package complete.

---

## 6. Vagrant VM Testing Strategy

Final acceptance on every supported target requires validation on a REAL virtual machine using Vagrant and VirtualBox.

### Reusable Testing Layout: `tests/vagrant/`
```text
tests/vagrant/
├── Vagrantfile               # Multi-machine definition for all 5 targets
├── run                       # Unified executable runner script
├── README.md                 # Usage instructions & safety guidelines
├── config/                   # Target-specific inventory and bootstrap configs
│   ├── ubuntu2404/
│   ├── ubuntu2204/
│   ├── debian13/
│   ├── alma9/
│   └── alma10/
└── evidence/                 # Sanitized real-VM acceptance reports
```

### VM Target Matrix

| Target Name | Vagrant Box | Provider | Box Status / Source |
|---|---|---|---|
| `ubuntu2404` | `bento/ubuntu-24.04` | VirtualBox | Official Bento Ubuntu 24.04 |
| `ubuntu2204` | `bento/ubuntu-22.04` | VirtualBox | Official Bento Ubuntu 22.04 (locally cached) |
| `debian13`   | `generic/debian13`   | VirtualBox | Robox generic Debian 13 Trixie |
| `alma9`      | `almalinux/9`        | VirtualBox | Official AlmaLinux OS Foundation |
| `alma10`     | `almalinux/10`       | VirtualBox | Official AlmaLinux OS Foundation |

### Unified Runner Interface (`tests/vagrant/run`)
```bash
# Test a specific platform from fresh VM to final Docker smoke test:
./tests/vagrant/run ubuntu2404 test

# Run specific lifecycle steps:
./tests/vagrant/run ubuntu2404 up
./tests/vagrant/run ubuntu2404 check
./tests/vagrant/run ubuntu2404 apply
./tests/vagrant/run ubuntu2404 verify
./tests/vagrant/run ubuntu2404 reboot
./tests/vagrant/run ubuntu2404 destroy

# Execute full matrix regression:
./tests/vagrant/run all test
```

### VM Safety & Scoping Rules
1. The runner only acts on VMs declared inside `tests/vagrant/Vagrantfile`.
2. Machine names are explicitly prefixed and scoped (`sb-test-*`).
3. Host network interfaces, host firewall rules, and unrelated VirtualBox VMs are never modified or destroyed.
4. Dirty or failed test VMs must be destroyed and recreated cleanly before certifying acceptance.

---

## 7. Required Acceptance Sequence for Platform Certification

Every supported target must complete this exact sequence:

```text
1. Fresh VM creation & boot                PASS
2. SSH host-key trust enrollment          PASS
3. Pre-check host checksum capture         PASS
4. Ansible check mode                      PASS
5. Check mode non-mutation assertion       PASS (checksums match)
6. First bootstrap apply                   PASS
7. Critical verification (verify.yml)      PASS
8. Second bootstrap apply                  PASS
9. Idempotency assertion                   PASS (changed=0)
10. Target VM reboot                       PASS
11. SSH reconnection recovery              PASS
12. Post-reboot verification               PASS
13. Firewall persistence verification      PASS
14. Security update service verification   PASS
15. Docker service & CLI verification      PASS
16. Docker Compose verification            PASS
17. Docker smoke test (hello-world)        PASS
```

---

## 8. Technical Risks & Mitigation

| Risk | Impact | Mitigation Strategy |
|---|---|---|
| **Enterprise Linux Firewall Divergence** | `firewalld` and `iptables-nft` can conflict or overwrite existing rules | Treat EL firewall through dedicated `firewalld` state management; never flush foreign zones; verify port rules across reboots. |
| **SELinux Denials** | Strict SELinux policies on EL9/10 may block custom SSH ports, Docker sockets, or system services | Keep SELinux in `Enforcing` mode; apply proper file contexts and boolean flags where necessary; reject proposals to disable SELinux. |
| **Docker Repository Incompatibilities** | Upstream Docker paths differ between Debian, Ubuntu, and CentOS/RHEL | Use distro-native Docker CE repositories verified against upstream sources; enforce conflict preflight before installing. |
| **Debian Minimal Image Differences** | Minimal Debian images may lack `sudo` or standard admin groups | Preflight detects missing prerequisites; platform layer manages `sudo` package installation and configures the `sudo` group. |
| **DNF 4 vs DNF 5 Differences** | AlmaLinux 10 adopts DNF 5 with altered CLI syntax and plugin architecture | Abstract package operations using `ansible.builtin.dnf` and verify module compatibility across EL9 and EL10. |

---

## 9. Completion Criteria

The multi-distribution initiative is considered complete when:
1. All 5 platform targets have verified platform backend implementations.
2. Fresh VM validation passes 100% on all 5 targets with `changed=0` on second apply.
3. Post-reboot verification and Docker smoke tests succeed on all 5 targets.
4. Static validation (yamllint, ansible-lint, syntax checks, unit tests, secret scanning, synthetic preflight tests) is clean.
5. All documentation, configuration references, and bilingual READMEs accurately describe the 5-target support matrix.
