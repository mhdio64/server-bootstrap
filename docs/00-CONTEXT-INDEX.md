# Context Index

This directory is the source of truth for the v0.1.0 MVP.

## Reading order for a new agent/session

Read these first:

1. `../AGENTS.md`
2. `01-PROJECT-SPEC.md`
3. `02-ARCHITECTURE.md`
4. the document relevant to the current task
5. `10-PHASE-STATUS.md`

Do not load every document into context unless necessary.

## Documents

| File | Purpose |
|---|---|
| `01-PROJECT-SPEC.md` | Product, users, scope, supported platform, UX, public behavior |
| `02-ARCHITECTURE.md` | Roles, orchestration, ownership boundaries, data/config flow |
| `03-SECURITY-SAFETY.md` | Safety invariants, SSH/firewall/Docker policies, failure behavior |
| `04-IMPLEMENTATION-PLAN.md` | Approved phased implementation sequence |
| `05-TESTING-RELEASE.md` | Test strategy, VM validation, CI and release gates |
| `06-CURSOR-WORKFLOW.md` | Cursor autonomy, Git/PR/CI workflow, review report contract |
| `07-DECISIONS.md` | Accepted architectural/product decisions |
| `08-RISKS-ASSUMPTIONS.md` | Assumptions and open risks that still require implementation care |
| `09-VERSION-SOURCES.md` | Version snapshot and upstream sources that must be revalidated |
| `10-PHASE-STATUS.md` | Current implementation phase and approval state |
| `11-INTERVIEW-DECISIONS.md` | Interview-confirmed product/architecture decisions |
| `12-GRAPHIFY.md` | Optional Graphify developer tooling policy |
| `13-CONFIGURATION-REFERENCE.md` | Public `bootstrap_*` configuration API |
| `14-TROUBLESHOOTING.md` | Operator troubleshooting guide |
| `15-RELEASE-EVIDENCE.md` | v0.1.0 release gate evidence and checklist |
| `16-MULTI-DISTRO-ROADMAP.md` | Multi-distribution initiative architecture, roadmap, and phase definitions |

## Conflict policy

If implementation pressure conflicts with an accepted decision:

- do not silently reinterpret the decision;
- report the conflict;
- propose concrete alternatives and trade-offs;
- wait for explicit approval before changing architecture, scope, security policy, public API, or supported-platform policy.
