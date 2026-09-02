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

**Phase 6B — Docker installation** is in progress on the development branch.

Phases 0–6A are merged on `main`. Phase 6B adds official Docker CE installation, daemon policy, and verification.

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
./scripts/secret-scan.sh
./scripts/test-secret-gate-negative.sh
git diff --check
```

## Repository layout (Phase 1)

```text
server-bootstrap/
├── ansible.cfg
├── site.yml              # preflight + apply orchestration
├── verify.yml            # post-apply verification (common only for now)
├── roles/
│   ├── common/
│   └── users/
├── tasks/preflight/
├── examples/minimal/
├── tests/synthetic/
├── inventory/
├── requirements-dev.txt
├── .ansible-lint
├── .yamllint
├── VERSION
├── LICENSE
├── SECURITY.md
├── CHANGELOG.md
└── docs/
```

Roles, wrapper scripts, and full verification are added in later approved phases.

## Optional developer tooling

Graphify is an optional local tool for codebase navigation. It is not required for bootstrap or CI. See `docs/12-GRAPHIFY.md`.

## License

MIT — see [LICENSE](LICENSE).

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting and scope notes.
