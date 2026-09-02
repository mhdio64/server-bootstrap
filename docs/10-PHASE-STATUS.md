# Phase Status

Target release: `v0.1.0`

Current state: **Phase 5 implemented on feature branch; VM validation in progress**

## Status table

| Phase | Name | Status |
|---|---|---|
| 0 | Repository foundation | MERGED |
| 1 | Orchestration + global preflight + common | MERGED |
| 2 | Admin user | MERGED |
| 3 | SSH hardening | MERGED |
| 4 | Firewall (`iptables-nft`) | MERGED |
| 5 | Security baseline | IMPLEMENTED (PR pending review) |
| 6A | Docker discovery/preflight | PENDING |
| 6B | Docker repository + installation | PENDING |
| 7 | Verification + summary + metadata | PENDING |
| 8 | Thin wrapper | PENDING |
| 9 | Scenario 1 real-VM validation | PENDING |
| 10 | Documentation + v0.1.0 release preparation | PENDING |

## Current approval boundary

Phase 5 implementation is complete on branch `feat/phase-5-security-baseline`.

Phase 5 delivers the `security` role only. Docker remains out of scope.

After Phase 5 PR review and merge, **Phase 6A requires separate human approval** before implementation begins.

The next phase is not automatically authorized by completion of the current phase.
