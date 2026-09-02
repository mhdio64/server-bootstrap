# Phase Status

Target release: `v0.1.0`

Current state: **Phase 6B implemented on feature branch; awaiting review and merge**

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
| 6B | Docker repository + installation | IMPLEMENTED (PR pending review) |
| 7 | Verification + summary + metadata | PENDING |
| 8 | Thin wrapper | PENDING |
| 9 | Scenario 1 real-VM validation | PENDING |
| 10 | Documentation + v0.1.0 release preparation | PENDING |

## Current approval boundary

Phase 6B implementation is complete on branch `feat/phase-6b-docker-install`.

Phase 6B delivers Docker repository setup, package installation, daemon policy, and verification.

After Phase 6B PR review and merge, **Phase 7 requires separate human approval** before implementation begins.

The next phase is not automatically authorized by completion of the current phase.
