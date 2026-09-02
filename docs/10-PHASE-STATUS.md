# Phase Status

Target release: `v0.1.0`

Current state: **Phase 4 implemented on feature branch; awaiting review and merge**

## Status table

| Phase | Name | Status |
|---|---|---|
| 0 | Repository foundation | MERGED |
| 1 | Orchestration + global preflight + common | MERGED |
| 2 | Admin user | MERGED |
| 3 | SSH hardening | MERGED |
| 4 | Firewall (`iptables-nft`) | IMPLEMENTED (PR pending review) |
| 5 | Security baseline | PENDING |
| 6A | Docker discovery/preflight | PENDING |
| 6B | Docker repository + installation | PENDING |
| 7 | Verification + summary + metadata | PENDING |
| 8 | Thin wrapper | PENDING |
| 9 | Scenario 1 real-VM validation | PENDING |
| 10 | Documentation + v0.1.0 release preparation | PENDING |

## Current approval boundary

Phase 4 implementation is complete on branch `feat/phase-4-firewall`.

Phase 4 delivers the `firewall` role only. Security updates and Docker remain out of scope.

After Phase 4 PR review and merge, **Phase 5 requires separate human approval** before implementation begins.

The next phase is not automatically authorized by completion of the current phase.
