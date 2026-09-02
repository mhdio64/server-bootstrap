# Agent Instructions — server-bootstrap

## Mission

Build a real, production-usable MVP for safely bootstrapping Ubuntu Server 24.04 LTS (amd64) with Ansible.

This repository is the first component of a future DevOps Toolkit. The MVP must stay small, safe, idempotent, reviewable, and usable on a real server.

## Authoritative context

At the beginning of a new task, read `docs/00-CONTEXT-INDEX.md` and then only the documents relevant to that task.

The architecture and product decisions in `docs/` are authoritative. If a requested implementation would conflict with them:

1. identify the conflict,
2. do not silently change the architecture,
3. explain the trade-off,
4. stop before making the conflicting architectural change unless the user explicitly approves it.

Do not invent future requirements.

## Non-negotiable MVP boundaries

- Target: Ubuntu Server 24.04 LTS, amd64 only.
- Control node: Linux only; Python 3.12–3.14.
- Ansible project, not an Ansible Collection for v0.1.0.
- Roles: `common`, `users`, `ssh`, `firewall`, `security`, `docker`.
- Public variables use the `bootstrap_*` prefix.
- No destructive overwrite of unknown consequential configuration.
- Second identical apply must produce `changed=0`.
- Useful and non-mutating check mode is required where technically possible.
- No automatic full rollback system.
- No direct push to `main`.
- No merge, tag, or GitHub Release without explicit human approval.
- No architecture, public API, security-policy, scope, or supported-platform change without explicit human approval.
- No significant new dependency without explicit approval.

## Engineering principles

- Prefer `ansible.builtin` modules.
- Keep business logic in Ansible, not in wrapper scripts.
- Fail before mutation when a dangerous or ambiguous state is detected.
- Known + owned state may be reconciled.
- Unknown + harmless state should be preserved.
- Unknown + consequential state must stop the run.
- Never destroy unknown configuration silently.
- Never disable SSH host-key checking globally.
- Never manage, copy, generate, or store user private SSH keys.
- Never use `curl | sh`-style installers.
- Never globally flush iptables rules.
- Never silently replace an existing conflicting Docker installation.

## Language

Repository code, comments, commit messages, documentation, variable names, tests, and user-facing CLI/error text should be written in English.

## Workflow

For an approved implementation phase, follow the project skill:

`.cursor/skills/implement-approved-phase/SKILL.md`

Before coding, inspect the repository and confirm the approved phase scope. After coding, run focused tests, then the full applicable validation suite, then inspect the diff.

Cursor may autonomously:
- create a feature branch,
- implement an approved phase,
- add/update tests,
- run local validation,
- make small atomic commits,
- push the feature branch,
- create/update a pull request,
- inspect and fix CI failures,
- return a review report.

Cursor must stop before:
- merge,
- tag,
- release,
- architectural change,
- scope expansion,
- security-policy change,
- supported-platform change,
- public API breaking change.

## Source freshness

Version-sensitive facts must be rechecked against current official upstream documentation before implementation. See `docs/09-VERSION-SOURCES.md`.

## Developer tooling

Graphify is an optional local developer tool for codebase navigation. It is not a bootstrap runtime dependency and is not required by CI. See `docs/12-GRAPHIFY.md`.
