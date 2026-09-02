# Phase Status

Target release: `v0.1.0`

Current state: **Phase 0 implemented on feature branch; awaiting review and merge**

## Status table

| Phase | Name | Status |
|---|---|---|
| 0 | Repository foundation | IMPLEMENTED (PR pending review) |
| 1 | Orchestration + global preflight + common | PENDING |
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

Phase 0 implementation is complete on branch `chore/repository-foundation`.

Phase 0 does not implement target-host bootstrap behavior from later phases.

After Phase 0 PR review and merge, **Phase 1 requires separate human approval** before implementation begins.

The next phase is not automatically authorized by completion of the current phase.

## Migration note

Prior Phase 0 work existed in `ansible-server-bootstrap` on branch `chore/repository-foundation`. That work was audited and selectively migrated into this canonical repository with updated naming and interview decisions incorporated.
