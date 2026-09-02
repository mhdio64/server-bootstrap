# Phase Status

Target release: `v0.1.0`

Current state: **Phase 8 implemented on feature branch; awaiting review and merge**

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
| 8 | Thin wrapper | IMPLEMENTED (PR pending review) |
| 9 | Scenario 1 real-VM validation | PENDING |
| 10 | Documentation + v0.1.0 release preparation | PENDING |

## Current approval boundary

Phase 8 implementation is complete on branch `feat/phase-8-thin-wrapper`.

Phase 8 delivers the Python stdlib `./bootstrap` wrapper with `check`, `apply`, and `verify`, explicit host-key trust, apply confirmation, and XDG log paths.

After Phase 8 PR review and merge, **Phase 9 requires separate human approval** before implementation begins.

The next phase is not automatically authorized by completion of the current phase.
