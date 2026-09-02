# Phase Status

Target release: `v0.1.0`

Current state: **Phase 6A implemented on feature branch; awaiting review and merge**

## Status table

| Phase | Name | Status |
|---|---|---|
| 0 | Repository foundation | MERGED |
| 1 | Orchestration + global preflight + common | MERGED |
| 2 | Admin user | MERGED |
| 3 | SSH hardening | MERGED |
| 4 | Firewall (`iptables-nft`) | MERGED |
| 5 | Security baseline | MERGED |
| 6A | Docker discovery/preflight | IMPLEMENTED (PR pending review) |
| 6B | Docker repository + installation | PENDING |
| 7 | Verification + summary + metadata | PENDING |
| 8 | Thin wrapper | PENDING |
| 9 | Scenario 1 real-VM validation | PENDING |
| 10 | Documentation + v0.1.0 release preparation | PENDING |

## Current approval boundary

Phase 6A implementation is complete on branch `feat/phase-6a-docker-preflight`.

Phase 6A delivers read-only Docker discovery and preflight classification only. No Docker installation or daemon mutation yet.

After Phase 6A PR review and merge, **Phase 6B requires separate human approval** before implementation begins.

The next phase is not automatically authorized by completion of the current phase.
