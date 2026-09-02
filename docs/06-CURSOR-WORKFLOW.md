# Cursor Workflow Contract

## Role of Cursor

Cursor is a high-autonomy implementation agent, not an autonomous product architect.

Architecture, product scope, supported platforms, public API policy, and security boundaries are human-approved.

Cursor should automate repetitive engineering work aggressively within an approved phase.


## One-time bootstrap exception for a repository with no Git history

If Phase 0 starts from this context-pack folder before Git has been initialized, Cursor may perform this one-time bootstrap sequence:

1. initialize Git with `main`,
2. create a **context-only baseline commit** containing the pre-implementation context pack,
3. if GitHub access is available, create the private repository and push that context-only `main`,
4. create `chore/repository-foundation`,
5. implement all Phase 0 tooling/foundation changes on that feature branch,
6. create a PR back to `main`,
7. stop before merge.

This exception exists only to establish a PR base. No Phase 0 implementation code/tooling may be smuggled into the baseline `main` commit.

After the baseline exists, the normal rule applies: no direct implementation pushes to `main`.

## Cursor may do autonomously

For an approved phase:

- inspect the current repository
- inspect Git status/history
- create a narrowly scoped feature branch
- implement the approved scope
- add or update tests
- run focused tests
- run the full applicable validation suite
- debug implementation failures
- create small atomic commits
- push the feature branch
- create or update a pull request
- inspect GitHub Actions results
- fix CI failures caused by the phase
- push follow-up fixes
- produce a review report

## Cursor must not do without explicit approval

- push directly to `main`
- merge a pull request
- tag a version
- publish a GitHub Release
- expand the approved phase scope
- change supported platforms
- change architecture boundaries
- change security policy
- change public API semantics
- introduce a significant dependency
- weaken a safety invariant to make tests pass

## Implementation-detail freedom

Cursor may choose ordinary implementation details when they do not affect public behavior or architecture.

Examples:

Allowed autonomously:

- internal variable names
- test helper structure
- small refactors
- lint fixes
- CI caching
- assertion implementation
- file organization within an approved boundary

Requires approval:

- changing `bootstrap_*` public variables
- changing firewall policy
- changing SSH security defaults
- changing Docker installation policy
- changing supported OS/architecture
- adding a Collection/dependency with meaningful maintenance cost
- removing/preserving existing configuration differently
- changing release or human-approval gates

## Required phase workflow

```text
inspect
-> confirm clean worktree
-> read relevant context
-> branch
-> implement approved scope
-> focused tests
-> full local validation
-> diff review
-> atomic commit(s)
-> push
-> PR
-> CI
-> fix until green
-> review report
-> STOP before merge
```

If GitHub access is unavailable, Cursor should complete all local steps and report exactly which remote steps could not be performed. It must not pretend they happened.

## Review report format

Every completed phase should report:

```text
Summary
Files changed
Behavior added/changed
Tests added/changed
Focused test results
Full local validation results
CI/PR status
Commits
git diff --stat
Security/safety observations
Known limitations
Items requiring human review
```

Include exact failing commands if anything remains red.

## Architectural conflict protocol

If implementation reveals a conflict with the approved design:

1. stop the conflicting part,
2. describe the observed constraint,
3. show 2-3 concrete options,
4. recommend one,
5. explain compatibility/security trade-offs,
6. wait for human approval before changing the architecture.

Do not "fix" the specification silently.

## Git discipline

Prefer small, coherent commits with conventional-style messages where useful.

Examples:

```text
chore(ci): add baseline validation
feat(common): add Ubuntu 24.04 preflight
test(docker): cover conflicting repository state
```

Do not mix unrelated cleanup with a phase.

## Documentation discipline

If a phase changes an approved user-facing behavior, update the relevant docs in the same phase only when that behavior was already approved.

If the change would alter a decision rather than merely document it, stop and request approval.
