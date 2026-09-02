# Phase Status

Target release: `v0.1.0`

Current state: **Phase 1 implemented on feature branch; awaiting review and merge**

## Status table

| Phase | Name | Status |
|---|---|---|
| 0 | Repository foundation | MERGED |
| 1 | Orchestration + global preflight + common | IMPLEMENTED (PR pending review) |
| 2 | Admin user | PENDING |
| 3 | SSH hardening | PENDING |
| 4 | Firewall (`iptables-nft`) | PENDING |
| 5 | Security baseline | PENDING |
| 6A | Docker discovery/preflight | PENDING |
| 6B | Docker repository + installation | PENDING |
| 7 | Verification + summary + metadata | PENDING |
| 8 | Thin wrapper | PENDING |
| 9 | Scenario 1 real-VM validation | PENDING |
| 10 | Documentation + v0.1.0 release preparation | PENDING |

## Current approval boundary

Phase 1 implementation is complete on branch `feat/phase-1-orchestration-common`.

Phase 1 delivers orchestration, global preflight, and the `common` role only.

After Phase 1 PR review and merge, **Phase 2 requires separate human approval** before implementation begins.

The next phase is not automatically authorized by completion of the current phase.
