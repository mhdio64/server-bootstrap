# Phase Status

Target release: `v0.1.0`

Current state: **Phase 10 implemented on feature branch; release prepared, not tagged**

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
| 9 | Scenario 1 real-VM validation | MERGED |
| 10 | Documentation + v0.1.0 release preparation | IMPLEMENTED (PR pending review) |

## Current approval boundary

Phase 10 implementation is complete on branch `feat/phase-10-docs-v0.1.0-release-prep`.

Phase 10 delivers user-facing documentation, release evidence, `VERSION` set to `0.1.0`, and a proposed release checklist.

**Git tag and GitHub Release for `v0.1.0` require explicit human approval** and are intentionally not created by this phase.
