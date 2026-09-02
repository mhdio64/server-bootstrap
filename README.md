# server-bootstrap

> Ansible project for safely bootstrapping Ubuntu Server 24.04 LTS (amd64) hosts.

`server-bootstrap` will bootstrap a fresh or safely compatible Ubuntu Server 24.04 LTS amd64 host into a secure, manageable, Docker-ready baseline using Ansible.

This repository is the first reusable component in a larger personal DevOps Toolkit:

```text
mhdio64/
├── server-bootstrap
├── observability-stack
├── gitlab-ci-components
├── jenkins-shared-library
└── devops-starter
```

The MVP is intentionally narrow. It must be real and safe enough for actual DevOps work, while avoiding enterprise-only complexity.

## Current status

**Phase 9 — Scenario 1 real-VM validation** is in progress on the development branch.

Phases 0–8 are merged on `main`. Phase 9 adds the repeatable Scenario 1 harness and sanitized release-gate evidence from a real Ubuntu Server 24.04 amd64 VM.

Start with:

- `AGENTS.md`
- `docs/00-CONTEXT-INDEX.md`
- `docs/10-PHASE-STATUS.md`

## MVP target

- Target OS: Ubuntu Server 24.04 LTS
- Architecture: amd64 / x86_64
- Control node: Linux (Python 3.12–3.14)
- Configuration management: Ansible (`ansible-core` 2.21.x)
- Output: secure OS baseline + Docker Engine
- Quality bar: safe reruns, `changed=0` on the second identical apply, useful check mode, critical verification, and real VM validation

## Development setup

Requirements:

- Linux control node
- Python 3.12, 3.13, or 3.14
- Git

Install pinned development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

Run local static validation:

```bash
yamllint .
ansible-lint
ansible-playbook site.yml --syntax-check
ansible-playbook verify.yml --syntax-check
python -m unittest discover -s tests/unit -p 'test_*.py'
./scripts/secret-scan.sh
./scripts/test-secret-gate-negative.sh
git diff --check
```

## Bootstrap wrapper

From a checkout of this repository, run the thin Python stdlib wrapper against your own project configuration:

```bash
./bootstrap check -i /path/to/inventory.yml
./bootstrap apply -i /path/to/inventory.yml
./bootstrap verify -i /path/to/inventory.yml
```

`bootstrap.yml` is expected beside `inventory.yml` unless you pass `--extra-vars`.

First-time SSH host trust requires interactive approval or `--expected-host-fingerprint` after out-of-band verification. Silent trust-on-first-use is forbidden.

Interactive `apply` requires explicit confirmation; use `--yes` for automation.

Logs are written under `${XDG_STATE_HOME:-~/.local/state}/server-bootstrap/logs`.

## Scenario 1 validation

Real-VM release validation is run locally with:

```bash
./tests/scenario1/run-scenario1.sh
```

See `tests/scenario1/README.md` for required environment variables. Sanitized evidence is recorded under `tests/scenario1/evidence/`.

## Repository layout

```text
server-bootstrap/
├── bootstrap             # thin Python stdlib CLI wrapper
├── bootstrap_wrapper/
├── ansible.cfg
├── site.yml              # preflight + apply orchestration
├── verify.yml            # post-apply verification and summary
├── roles/
│   ├── common/
│   ├── users/
│   ├── ssh/
│   ├── firewall/
│   ├── security/
│   └── docker/
├── tasks/
│   ├── preflight/
│   ├── post_apply/
│   └── summary/
├── vars/
├── examples/minimal/
├── tests/synthetic/
├── requirements-dev.txt
├── .ansible-lint
├── .yamllint
├── VERSION
├── LICENSE
├── SECURITY.md
├── CHANGELOG.md
└── docs/
```

Target metadata is recorded at `/var/lib/server-bootstrap/metadata.json` (bootstrap version only; no per-run timestamps).

## Optional developer tooling

Graphify is an optional local tool for codebase navigation. It is not required for bootstrap or CI. See `docs/12-GRAPHIFY.md`.

## License

MIT — see [LICENSE](LICENSE).

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting and scope notes.
