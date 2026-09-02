# Interview Decisions — v0.1.0

This file records product and architecture decisions confirmed during the pre-implementation interview. These decisions supplement `docs/07-DECISIONS.md`.

## Repository and delivery

- **Canonical repository:** `mhdio64/server-bootstrap`
- **Prior work disposition:** audit and selectively migrate from `ansible-server-bootstrap`; do not wholesale copy stale naming or generated state.
- **Distribution:** checkout a Git tag and run `./bootstrap` from that checkout.
- **Language:** all public repository artifacts in English.

## Firewall

- **Ownership model:** project-owned chains, limited jumps, and a dedicated restore fragment/service; never persist transient Docker chains.
- **Foreign policy:** strict stop on unknown consequential firewall policy in preflight.
- **Activation:** staged atomic apply with timed rollback until connectivity and policy health are confirmed.
- **Public port API:** individual TCP/UDP ports `1..65535` only; no ranges or source-based rules in v0.1.0.

## SSH

- **Activation safety:** on reconnect probe failure, rollback only the project-owned drop-in, reload, then fail with a clear error.
- **Default port semantics:** if `bootstrap_ssh_port` is unset, preserve the effective SSH port; port 22 is the fresh-host baseline only.
- **Host trust (v0.1.0):** wrapper must support `--expected-host-fingerprint` and interactive approval after out-of-band comparison; never silently trust a new host.

## Admin user and authentication

- **Authorized keys:** manage a project-owned block inside `authorized_keys`; preserve lines outside the block.
- **Existing admin:** classify first; preserve password, home, and consequential shell state; reconcile only sudo and the managed key block.
- **Connection transition:** do not switch Ansible connection mid-run; verify admin login/sudo independently; operator uses admin on subsequent runs.
- **Initial password auth:** interactive prompts only; passwords never in config, CLI, or logs.
- **Key identity requirement:** if no control-node identity/agent key matches configured admin public keys, preflight stops before SSH hardening.

## Docker

- **`latest` semantics:** install latest stable on fresh hosts; preserve compatible official existing installs without implicit upgrade.
- **Downgrade:** stop with actionable message; no automatic downgrade in v0.1.0.
- **`daemon.json`:** preserve valid existing files by default; fresh hosts may receive `{"log-driver":"local"}` after upstream revalidation.

## Wrapper and configuration

- **Implementation:** Python standard library only; no duplicated Ansible business logic.
- **Consumer layout:** `inventory.yml` for connection data and `bootstrap.yml` for desired `bootstrap_*` state.
- **Apply confirmation:** interactive runs require explicit confirmation; `--yes` for automation.
- **Invocation scope:** one target per invocation in v0.1.0.
- **Reboot opt-in:** controlled reboot, wait for SSH, then re-run critical verification.
- **Logs:** default to `${XDG_STATE_HOME:-~/.local/state}/server-bootstrap/logs` with restricted permissions.

## Defaults and opt-out

- **Component defaults:** common, users, SSH, firewall, security updates, and Docker are enabled by default.
- **Security opt-out:** explicit `false` is allowed; check/apply/summary must emit prominent warnings.

## Locale and check mode

- **Locale:** preserve valid existing locale; change only with explicit `bootstrap_locale`; use conservative fallback only when locale state is invalid.
- **Check mode:** skip post-apply verification with explicit `NOT RUN (check mode)`; unpredictable critical paths fail check; non-critical unknowns warn with `WARNING/UNKNOWN`.

## Validation evidence

- **Scenario 1 evidence:** repeatable local harness plus sanitized report; do not require private VM access in public CI.

## Control node toolchain

- **Python support:** 3.12, 3.13, and 3.14 officially supported; CI validates all three.
- **Pins:** retain exact Phase 0 pins until reviewed dependency PRs change them.
