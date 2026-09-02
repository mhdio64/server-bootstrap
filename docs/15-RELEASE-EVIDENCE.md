# Release Evidence — proposed v0.1.0

This document summarizes release-gate evidence for the first usable MVP. It does **not** create a Git tag or GitHub Release.

## Proposed version

```text
v0.1.0
```

`VERSION` in the repository root is set to `0.1.0` as release preparation only. Tagging and publishing require explicit human approval.

## Supported matrix

| Component | Supported in v0.1.0 |
|---|---|
| Target OS | Ubuntu Server 24.04 LTS |
| Target architecture | amd64 / x86_64 |
| Control node OS | Linux |
| Control node Python | 3.12, 3.13, 3.14 |
| Ansible | `ansible-core` 2.21.x (pinned in `requirements-dev.txt`) |

Not supported in v0.1.0: Ubuntu 22.04, ARM64, Windows/macOS control nodes, Kubernetes, monitoring agents, application deployment, UFW-managed hosts, Docker Swarm, rootless Docker.

## Static validation (CI)

GitHub Actions on `main` runs, per Python 3.12/3.13/3.14:

- dependency install sanity
- `yamllint`
- `ansible-lint`
- Ansible syntax checks for `site.yml` and `verify.yml`
- secret scanning and negative secret-gate test
- synthetic classifier/preflight tests
- wrapper unit tests
- `git diff --check`

## Synthetic coverage

`tests/synthetic/run-phase1-preflight-tests.sh` covers:

- missing required configuration
- unsupported platform rejection
- SSH, firewall, and Docker classifier logic
- summary and metadata helpers

## Scenario 1 real-VM validation

Sanitized evidence:

- `tests/scenario1/evidence/scenario1-report.md`
- harness: `tests/scenario1/run-scenario1.sh`

Required Scenario 1 results recorded as **PASS**:

- check mode without host mutation
- first apply
- first verify
- second apply `changed=0`
- reboot recovery
- post-reboot verify
- Docker `hello-world` smoke test

Scenario 2 (existing configured production-like host) is explicitly post-MVP.

## Known limitations

- Single target per invocation.
- No automatic full rollback system.
- Firewall manages project-owned policy only; Docker-generated chains and published container ports are out of scope.
- `bootstrap_docker_version: latest` preserves compatible existing installs without implicit upgrade.
- Existing-server behavior beyond Scenario 1 is covered synthetically, not by a second real VM.

## Human release checklist

Before tagging `v0.1.0`:

1. Confirm `main` CI is green.
2. Re-run `./tests/scenario1/run-scenario1.sh` on a fresh or approved VM snapshot if material changes landed after the recorded evidence.
3. Review `CHANGELOG.md` and `README.md`.
4. Explicitly approve Git tag and GitHub Release creation.
