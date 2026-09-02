# Phase Status

Target release: `v0.1.0`

Current state: **Phase 9 implemented on feature branch; awaiting review and merge**

## Status table

| Phase | Name | Status |
|---|---|---|
| 0 | Repository foundation | MERGED |
| 1 | Orchestration + global preflight + common | MERGED |
| 2 | Admin user | MERGED |
| 3 | SSH hardening | MERGED |
| 4 | Firewall (`iptables-nft`) | MERGED |
| 5 | Security baseline | MERGED |
| 6A | Docker discovery/preflight | MERGED |
| 6B | Docker repository + installation | MERGED |
| 7 | Verification + summary + metadata | MERGED |
| 8 | Thin wrapper | MERGED |
| 9 | Scenario 1 real-VM validation | IMPLEMENTED (PR pending review) |
| 10 | Documentation + v0.1.0 release preparation | PENDING |

## Current approval boundary

Phase 9 implementation is complete on branch `feat/phase-9-scenario1-vm-validation`.

Phase 9 delivers the repeatable Scenario 1 harness, sanitized evidence report, check-mode preflight fixes, and successful real-VM validation on Ubuntu Server 24.04 amd64.

After Phase 9 PR review and merge, **Phase 10 requires separate human approval** before implementation begins.

The next phase is not automatically authorized by completion of the current phase.
