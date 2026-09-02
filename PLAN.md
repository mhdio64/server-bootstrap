# Phase 0 Foundation Plan

## Scope and guardrails

- Work only in this repository on a feature branch; never push implementation directly to `main`.
- Treat the prior `ansible-server-bootstrap` repository as audit input, not a second source of truth.
- Keep Phase 0 limited to repository/tooling foundations. Roles, target mutation, SSH/firewall/Docker implementation, and Phase 1 orchestration remain out of scope.

## 1. Persist the approved specification

- Record this approved Phase 0 plan, phase boundary, source-of-truth decision, and Graphify policy.
- Transfer and normalize architecture, security, testing, decisions, risks, version-source, and phase-status documents into `docs/`.
- Add project-local Cursor guidance under `.cursor/rules/`.

## 2. Audit and migrate the Phase 0 foundation

- Review prior Phase 0 commits and selectively recreate valid artifacts.
- Retain exact pins: `ansible-core==2.21.3`, `ansible-lint==26.8.0`, `yamllint==1.38.0`, `detect-secrets==1.5.0`.
- Document Python 3.12–3.14 control-node support.
- Ensure placeholders perform no target bootstrap behavior and examples contain no real hosts, customer data, credentials, or private keys.

## 3. Restore supply-chain and CI gates

- Secret scanning with a committed baseline that CI never regenerates, plus a negative synthetic test.
- GitHub Actions and Dependabot with third-party actions pinned to immutable full SHAs.
- Enforce: dependency installation, yamllint, ansible-lint, syntax checks, secret scanning, negative secret-gate test, and `git diff --check`.

## 4. Add Graphify at the useful Phase 0 checkpoint

- Install the official `graphifyy` CLI in an isolated user tool environment, pinned to reviewed release `0.9.53`.
- Do not add Graphify to bootstrap runtime or mandatory CI dependencies.
- Install Graphify's Cursor integration project-scoped.
- Build the initial graph in local/code-only mode so no project content is sent to an external model.
- Do not install Graphify Git hooks or global aliases in Phase 0.

## 5. Validate, review, and hand off

- Run focused checks while migrating, then the complete local Phase 0 validation suite.
- Inspect the full diff for stale naming, secrets, generated noise, unsafe examples, action pinning, and accidental post-Phase-0 behavior.
- Create atomic commits on the feature branch, push, open a PR, inspect CI, and fix Phase 0 defects until green.
- Produce the required phase report and stop before Phase 1.
