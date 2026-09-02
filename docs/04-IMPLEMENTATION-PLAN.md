# Implementation Plan — v0.1.0

Implementation is phased. Each meaningful phase should normally be isolated on a feature branch and reviewed before merge.

Do not implement future phases opportunistically.

## Phase 0 — Repository foundation

Goal: establish repository/tooling/CI guardrails without target-host mutation.

Expected work:

- initialize Git repository if not already initialized
- preserve all existing context files
- private GitHub repository setup if GitHub access is available
- MIT `LICENSE`
- `.gitignore`
- `VERSION` with an internal `0.0.x` value
- `requirements-dev.txt`
- `ansible.cfg`
- initial `site.yml`/`verify.yml` placeholders only if they are useful for syntax validation and do not imply unapproved architecture
- `.ansible-lint`
- `.yamllint`
- README/SECURITY/CHANGELOG foundation
- GitHub Actions CI
- Dependabot configuration

Baseline version snapshot is in `09-VERSION-SOURCES.md`. Revalidate before pinning.

Initial CI should include:

- dependency installation sanity
- yamllint
- ansible-lint
- Ansible syntax check when applicable
- secret scanning
- `git diff --check`

Third-party GitHub Actions should be pinned to full commit SHAs.

Gate:

```text
clean checkout
-> development dependencies install
-> all local static validation passes
-> GitHub CI passes
```

Stop before merge.

## Phase 1 — Orchestration, global preflight, common

Implement:

- global preflight flow
- supported platform checks
- required variable validation
- remote Python/privilege checks
- baseline packages
- timezone
- locale
- optional hostname
- time synchronization
- reboot-required detection
- optional explicit package upgrade

Expected defaults:

```text
timezone = UTC
upgrade all packages = false
automatic reboot = false
```

A practical initial package set may include:

- ca-certificates
- curl
- git
- gnupg
- htop
- jq
- nano
- unzip
- vim
- wget

The exact list is implementation-level and must remain small.

Gate:

- expected first-run changes
- second identical run `changed=0`
- useful non-mutating check mode
- unsupported target fails before mutation
- missing critical configuration fails before mutation

## Phase 2 — Admin user

Implement one bootstrap/admin user:

- create if absent
- home
- administrative shell
- sudo group/access
- project-owned sudoers drop-in
- public authorized keys
- NOPASSWD sudo
- default password locked/unset
- `visudo` validation

Preserve unrelated users and authorized keys.

Gate:

- admin exists
- expected public key present
- non-interactive sudo works
- second identical run `changed=0`

## Phase 3 — SSH hardening

Implement a project-owned drop-in.

Baseline intent:

- PubkeyAuthentication yes
- PermitEmptyPasswords no
- PasswordAuthentication no
- KbdInteractiveAuthentication no
- PermitRootLogin prohibit-password

Changing port is opt-in.

Safety flow:

```text
discover effective current state
-> validate admin-key safety
-> inspect consequential conflicts
-> render candidate
-> sshd syntax validation
-> effective config validation
-> atomic activation
-> reload
-> reconnect verification
```

Gate: no lockout, no invalid activation, second run `changed=0`.

## Phase 4 — Firewall

Backend: `iptables-nft`.

Implement read-only state classifier before mutation.

Expected acceptable categories:

- fresh/default
- project-owned
- Docker-owned compatible state

Consequential foreign policy -> stop.

Implement IPv4 and IPv6 protection when IPv6 is enabled.

Never globally flush the ruleset.

Persistence must not capture transient Docker-owned chains as project-owned state.

Gate on real VM:

- SSH remains reachable
- expected host port filtering works
- persistence survives reboot
- second run `changed=0`
- foreign consequential policy fails closed

## Phase 5 — Security baseline

Keep small:

- unattended security upgrades
- APT periodic policy
- no automatic reboot by default
- effective configuration verification

Do not expand into CIS/auditd/FIPS/custom kernel hardening.

Gate: expected security-update policy active and idempotent.

## Phase 6A — Docker discovery/preflight

Read-only classifier first.

States:

- absent
- official-compatible
- partial
- conflicting
- ambiguous

Only absent and safely compatible states may proceed.

Check installed packages and repository configuration.

Do not uninstall conflicts automatically.

Gate: synthetic fixtures cover every classifier state and prove read-only behavior.

## Phase 6B — Docker repository/install

Use the official Docker Ubuntu repository.

Install the approved components:

- docker-ce
- docker-ce-cli
- containerd.io
- docker-buildx-plugin
- docker-compose-plugin

Default: latest stable.

Allow exact version pinning.

Own project-specific repository/key files only when creating the repository. Preserve compatible official configuration where practical.

No convenience script.

Docker users list default: empty.

Daemon configuration:

- never blindly overwrite existing `daemon.json`
- malformed/ambiguous/conflicting configuration should stop
- a fresh-host logging-safety default may be implemented only after validating current Docker guidance

Verification:

- Docker service active
- containerd active
- `docker version`
- `docker compose version`
- `docker info`
- effective approved daemon settings

Gate: functional success and idempotency.

## Phase 7 — Verification, summary, metadata

Add independent critical verification for:

- platform
- admin/sudo
- SSH
- firewall
- time/security services as applicable
- Docker
- Docker Compose
- reboot-required status

Prefer Ansible-native reporting first; avoid an unnecessary custom callback plugin.

Target metadata may record bootstrap version without changing every run.

## Phase 8 — Thin wrapper

Only after the Ansible-native interface is stable.

Possible commands:

```text
bootstrap check
bootstrap apply
bootstrap verify
```

Wrapper handles orchestration UX only.

No duplicated Ansible business logic.

Logs should live outside the repository, preferably under XDG state directories.

## Phase 9 — Scenario 1 real-VM validation

Required release test on the available Ubuntu Server 24.04 amd64 VM:

```text
fresh snapshot/state
-> host trust
-> check
-> apply
-> verify
-> second apply
-> reboot
-> verify again
```

Required:

- check does not mutate
- apply passes
- verify passes
- second apply `changed=0`
- reboot recovers
- SSH works
- firewall persists
- Docker works
- Compose works
- one explicit Docker smoke test may pull/run a vendor-approved test image

Scenario 2 (real existing configured server) is post-MVP.

## Phase 10 — Documentation and v0.1.0 release preparation

Complete:

- README
- SECURITY
- CHANGELOG
- configuration reference
- limitations
- Docker/firewall caveats
- troubleshooting
- supported matrix
- release evidence

Propose `v0.1.0`.

Do not tag or publish without explicit approval.
