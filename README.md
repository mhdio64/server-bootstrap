[English](README.md) | [فارسی](README.fa.md)

# server-bootstrap

> Safely bootstrap Ubuntu Server 24.04 LTS (amd64) hosts into a secure, manageable, Docker-ready baseline with Ansible.

`server-bootstrap` is the first component of a personal DevOps Toolkit. v0.1.0 delivers a narrow, production-usable MVP:

- OS baseline and time sync
- admin user with SSH public keys and passwordless sudo
- SSH hardening via a project-owned drop-in
- host firewall using `iptables-nft`
- unattended security updates
- official Docker CE + Compose plugin

## Supported platforms

| | Supported |
|---|---|
| Target OS | Ubuntu Server 24.04 LTS |
| Target architecture | amd64 / x86_64 |
| Control node | Linux, Python 3.12–3.14 |
| Ansible | `ansible-core` 2.21.x |

See `docs/15-RELEASE-EVIDENCE.md` for the full matrix and limitations.

## Quick start

1. Checkout this repository (proposed release: `v0.1.0`).
2. Create your project config outside the toolkit repo:

```text
your-project/
├── inventory.yml
└── bootstrap.yml
```

3. Start from `examples/minimal/` and edit host connection data and public keys.
4. Run from the toolkit checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

./bootstrap check  -i /path/to/inventory.yml
./bootstrap apply  -i /path/to/inventory.yml
./bootstrap verify -i /path/to/inventory.yml
```

`bootstrap.yml` is expected beside `inventory.yml` unless you pass `--extra-vars`.

### Wrapper safety

- First-time SSH host trust requires interactive approval or `--expected-host-fingerprint`.
- Interactive `apply` requires confirmation; use `--yes` for automation.
- Logs: `${XDG_STATE_HOME:-~/.local/state}/server-bootstrap/logs`.

## Configuration

Public variables use the `bootstrap_*` prefix. Minimum required configuration:

```yaml
bootstrap_admin_user: deploy
bootstrap_admin_authorized_keys:
  - "ssh-ed25519 AAAA... user@example"
```

Full reference: `docs/13-CONFIGURATION-REFERENCE.md`.

## Quality bar

- second identical apply must produce `changed=0`
- useful non-mutating check mode where technically honest
- critical post-apply verification
- Scenario 1 real-VM validation harness under `tests/scenario1/`

## Important caveats

### Firewall

- Uses project-owned `iptables-nft` chains only; never globally flushes rules.
- Does not manage Docker-generated chains or published container ports.
- Stops on unknown consequential foreign firewall policy (for example active UFW).

### Docker

- Installs from the official Docker APT repository only.
- Classifies existing Docker state; does not silently replace conflicting installs.
- `bootstrap_docker_version: latest` preserves compatible existing official installs without implicit upgrade.
- `docker` group membership is opt-in via `bootstrap_docker_users`.

### Limitations

- one target host per invocation
- no generic full rollback system
- no Kubernetes, monitoring agents, reverse proxy, TLS, or application deployment
- Scenario 2 existing-server validation is post-MVP

## Documentation

| Document | Purpose |
|---|---|
| `docs/13-CONFIGURATION-REFERENCE.md` | Public `bootstrap_*` API |
| `docs/14-TROUBLESHOOTING.md` | Common failures and recovery |
| `docs/15-RELEASE-EVIDENCE.md` | v0.1.0 release gate evidence |
| `docs/03-SECURITY-SAFETY.md` | Safety invariants |
| `docs/05-TESTING-RELEASE.md` | Testing and release strategy |
| `AGENTS.md` | Contributor/agent instructions |

## Development

```bash
yamllint .
ansible-lint
ansible-playbook site.yml --syntax-check
ansible-playbook verify.yml --syntax-check
python -m unittest discover -s tests/unit -p 'test_*.py'
./tests/synthetic/run-phase1-preflight-tests.sh
./scripts/secret-scan.sh
./scripts/test-secret-gate-negative.sh
git diff --check
```

Optional codebase navigation: `docs/12-GRAPHIFY.md`.

## Repository layout

```text
server-bootstrap/
├── bootstrap
├── bootstrap_wrapper/
├── site.yml
├── verify.yml
├── roles/
├── tasks/
├── tests/
├── examples/minimal/
└── docs/
```

Target metadata: `/var/lib/server-bootstrap/metadata.json` (bootstrap version only).

## License

MIT — see [LICENSE](LICENSE).

## Security

See [SECURITY.md](SECURITY.md) for supported versions and vulnerability reporting.
