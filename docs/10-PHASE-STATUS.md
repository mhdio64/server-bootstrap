# Phase Status

Target release: `v0.1.0`

Current state: **Phase 3 implemented on feature branch; awaiting review and merge**

## Status table

| Phase | Name | Status |
|---|---|---|
| 0 | Repository foundation | MERGED |
| 1 | Orchestration + global preflight + common | MERGED |
| 2 | Admin user | MERGED |
| 3 | SSH hardening | IMPLEMENTED (PR pending review) |
| 4 | Firewall (`iptables-nft`) | PENDING |
| 5 | Security baseline | PENDING |
| 6A | Docker discovery/preflight | PENDING |
| 6B | Docker repository + installation | PENDING |
| 7 | Verification + summary + metadata | PENDING |
| 8 | Thin wrapper | PENDING |
| 9 | Scenario 1 real-VM validation | PENDING |
| 10 | Documentation + v0.1.0 release preparation | PENDING |

## Current approval boundary

Phase 3 implementation is complete on branch `feat/phase-3-ssh-hardening`.

Phase 3 delivers the `ssh` role only. Firewall, security, and Docker remain out of scope.

After Phase 3 PR review and merge, **Phase 4 requires separate human approval** before implementation begins.

The next phase is not automatically authorized by completion of the current phase.
