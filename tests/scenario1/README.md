# Scenario 1 — Real VM validation harness

This directory contains the repeatable local harness for Scenario 1 release validation on a real Ubuntu Server 24.04 amd64 VM.

Public CI does **not** run this harness. Operators run it locally against their own VM inventory.

## Prerequisites

- Linux control node with Python 3.12–3.14
- Development dependencies installed (`pip install -r requirements-dev.txt`)
- A reachable Ubuntu Server 24.04 amd64 target
- Local project configuration outside this repository:

```text
/path/to/project/
├── inventory.yml
└── bootstrap.yml
```

For local development, this repository keeps an example under `local/vm-test/` (gitignored).

## Run

```bash
export SCENARIO1_INVENTORY=/path/to/inventory.yml
export SCENARIO1_BOOTSTRAP=/path/to/bootstrap.yml   # optional if beside inventory
export SCENARIO1_EXPECTED_HOST_FINGERPRINT='SHA256:...'  # optional for non-interactive trust

./tests/scenario1/run-scenario1.sh
```

Optional environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `SCENARIO1_INVENTORY` | `local/vm-test/inventory.yml` if present | Target inventory |
| `SCENARIO1_BOOTSTRAP` | beside inventory | Desired-state file |
| `SCENARIO1_EXPECTED_HOST_FINGERPRINT` | unset | Non-interactive SSH host-key trust |
| `SCENARIO1_REPORT` | `tests/scenario1/evidence/scenario1-report.md` | Sanitized report output |
| `SCENARIO1_SKIP_REBOOT` | `0` | Set to `1` to skip reboot step |

## Scenario flow

1. Capture lightweight host state checksums
2. `./bootstrap check`
3. Assert check mode did not mutate the host
4. `./bootstrap apply --yes`
5. `./bootstrap verify`
6. Second `./bootstrap apply --yes` with `changed=0`
7. Reboot target and wait for SSH
8. `./bootstrap verify`
9. Docker smoke test (`hello-world`)

## Evidence

Sanitized reports are written to `tests/scenario1/evidence/`. Reports must not contain private IPs, hostnames, credentials, or customer data.
