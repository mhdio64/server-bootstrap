# Scenario 1 Validation Report

This report is intentionally sanitized. It records release-gate evidence without private hostnames, IP addresses, credentials, or customer data.

## Metadata

| Field | Value |
|---|---|
| Toolkit version | 0.0.1 |
| Started (UTC) | 2026-09-02T18:41:14Z |
| Finished (UTC) | 2026-09-02T18:44:42Z |
| Inventory source | operator-provided local file |
| Bootstrap source | operator-provided local file |

## Required results

| Step | Result |
|---|---|
| check mode / no mutation | PASS |
| first apply | PASS |
| first verify | PASS |
| second apply changed=0 | PASS |
| reboot recovery | PASS |
| post-reboot verify | PASS |
| docker smoke (hello-world) | PASS |

## Notes

- Host platform validated locally as Ubuntu Server 24.04 amd64 during harness execution.
- SSH, firewall persistence, Docker, and Docker Compose are covered by bootstrap verify plus hello-world smoke test.
- Detailed command output is stored outside the repository in the operator XDG log directory created by `./bootstrap`.

## Operator attestation

- [x] Scenario 1 harness completed successfully on a real Ubuntu Server 24.04 amd64 VM.
- [x] No secrets or private network identifiers are included in this committed report.
