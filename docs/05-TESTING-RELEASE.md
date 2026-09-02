# Testing, CI, and Release Strategy

## Quality definition

The MVP is complete only when it is usable on a real Ubuntu Server 24.04 amd64 VM.

"Ansible ran successfully once" is not enough.

## Idempotency

Hard gate:

> A second identical apply must produce `changed=0`.

Tasks that update timestamps or rewrite equivalent files on every run are defects unless there is an explicitly approved reason.

## Check mode

Goal:

```text
ansible-playbook ... --check --diff
```

should predict meaningful changes without target mutation where technically possible.

Do not fabricate check-mode behavior for actions that cannot be safely predicted.

Tests should detect accidental mutation during check mode.

## Test layers

### Static

- YAML lint
- ansible-lint
- Ansible syntax checks
- shell linting when shell scripts exist
- `git diff --check`
- secret scanning

### Synthetic/unit-style

Use fixtures and test helpers for read-only classifiers and state-decision logic, especially:

- firewall existing-state classification
- Docker package/repository classification
- dangerous variable combinations
- configuration conflict detection

### Integration

Use the real Ubuntu Server 24.04 amd64 VM for system-level behavior that cannot be trusted in a lightweight container:

- systemd
- SSH reload/reconnect
- firewall
- reboot persistence
- Docker daemon
- end-to-end idempotency

Molecule is not required for v0.1.0.

## Required Scenario 1

Fresh Ubuntu Server 24.04 amd64.

Run:

1. trust/enroll host key
2. check mode
3. first apply
4. verify
5. second apply
6. reboot
7. verify again

Required result:

```text
check mode            PASS / no mutation
first apply           PASS
critical verification PASS
second apply          changed=0
reboot                PASS
SSH                    PASS
firewall persistence  PASS
Docker                 PASS
Compose                PASS
```

## Scenario 2

A real preconfigured Ubuntu host is not currently available.

For v0.1.0:

- cover existing-state behavior with synthetic tests and explicit limitations,
- do not overclaim real-world existing-server validation.

Real Scenario 2 VM testing is a post-MVP priority.

## CI on pull requests

Minimum intended checks:

- install declared development dependencies
- yamllint
- ansible-lint
- syntax check
- synthetic safety tests
- check-mode tests where practical
- secret scan
- `git diff --check`

Do not mutate a GitHub-hosted runner into a fake production server just to claim system integration coverage.

## Release hard gates

A release must stop on:

- lint failure
- syntax failure
- test failure
- idempotency failure
- detected check-mode mutation
- SSH safety failure
- firewall safety failure
- Docker verification failure
- secret scan finding
- dirty/unreviewed release diff
- Scenario 1 VM failure

Warnings that do not fail a valid state may include:

- reboot required
- explicitly non-critical documentation warning

## Versioning

Semantic Versioning from the beginning.

Intended lifecycle:

```text
0.0.x   internal development
v0.1.0  first real public/usable MVP
0.x     API still evolving, but avoid gratuitous breakage
1.0.0   stable public contract
```

Even during `0.x`, avoid unnecessary breaking changes.

When practical, deprecated public variables should have a transition period.

## Release flow

```text
all required checks green
-> Cursor prepares release evidence and notes
-> human review
-> explicit approval
-> tag
-> GitHub Release
```

Cursor never tags/releases by default.
