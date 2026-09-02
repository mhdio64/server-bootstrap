---
name: implement-approved-phase
description: Execute one explicitly approved server-bootstrap implementation phase end-to-end: inspect, branch, implement, test, commit, push/PR when available, repair CI, report, and stop before merge. Use when the user asks to implement or continue an approved numbered phase.
---

# Implement Approved Phase

Use this skill only for a phase that is explicitly marked as approved in `docs/10-PHASE-STATUS.md` or explicitly approved by the user in the current conversation.

## 1. Establish scope

Read:

- `AGENTS.md`
- `docs/00-CONTEXT-INDEX.md`
- `docs/04-IMPLEMENTATION-PLAN.md`
- `docs/10-PHASE-STATUS.md`
- relevant architecture/security/testing documents for the phase

State the exact phase boundary internally before editing.

Do not implement future phases opportunistically.

## 2. Inspect repository

Check:

- current branch
- `git status`
- recent history
- existing implementation/tests
- current tool versions/config
- whether the worktree is clean

If unrelated uncommitted work exists, preserve it and avoid destructive cleanup.

## 3. Freshness check

For any version-sensitive upstream behavior used by the phase:

- verify current official upstream documentation,
- compare it with `docs/09-VERSION-SOURCES.md`.

If upstream changed only an implementation detail, adapt and update the source snapshot as needed.

If upstream change would alter architecture, security policy, supported platform, or public behavior, stop and ask for approval.

## 4. Branch

Create a narrow feature branch from the appropriate base branch.

Do not work directly on `main`.

For the special case where Phase 0 starts with no Git history at all, follow the one-time context-only baseline exception documented in `docs/06-CURSOR-WORKFLOW.md`, then create `chore/repository-foundation`.

Use a descriptive branch name consistent with the phase.

## 5. Implement

Implement only the approved phase.

Follow:

- `docs/02-ARCHITECTURE.md`
- `docs/03-SECURITY-SAFETY.md`
- project rules

Prefer the smallest correct change that satisfies the phase.

Do not add speculative abstractions for future distributions/features.

## 6. Test

Add or update tests as part of the same work.

Run:

1. focused tests for the changed behavior,
2. applicable lint/syntax checks,
3. full local validation suite available at this phase,
4. `git diff --check`.

For stateful capabilities, explicitly test idempotency and safe failure behavior as soon as the phase supports it.

Never weaken a gate just to pass.

## 7. Review the diff

Before commit:

- inspect `git diff`,
- confirm no secrets/customer data/logs,
- confirm no scope creep,
- confirm no accidental architecture/public API change,
- inspect `git diff --stat`,
- confirm documentation is consistent with approved behavior.

## 8. Commit

Create small atomic commit(s).

Use clear conventional-style messages when helpful.

Do not mix unrelated cleanup.

## 9. Push and PR

If authenticated Git/GitHub access is available:

- push the feature branch,
- create or update a PR,
- include scope and validation evidence,
- inspect required checks.

If remote access is unavailable, do not simulate it. Report the limitation and continue with the local review report.

## 10. CI repair loop

If CI fails because of the phase:

- inspect the exact failing log,
- fix the root cause,
- rerun relevant local validation,
- commit the correction,
- push,
- recheck CI.

Repeat until green or until an architectural/security decision is required.

Do not change architecture or weaken tests autonomously.

## 11. Final review report

Return:

### Summary
What the phase implemented.

### Files changed
Exact files or concise grouped list.

### Behavior
User-visible and internal behavior added/changed.

### Tests
Tests added/changed.

### Validation
Exact focused/full commands and PASS/FAIL totals where available.

### Git / PR / CI
Branch, commits, PR, CI status.

### Diff
`git diff --stat` summary.

### Safety observations
Any relevant security/idempotency/existing-state findings.

### Limitations
Anything intentionally not handled.

### Human review items
Anything the user should inspect carefully.

## 12. Stop

Do not:

- merge,
- tag,
- release,
- start the next phase.

Wait for explicit human approval.
