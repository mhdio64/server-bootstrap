# Risks and Assumptions

## Accepted assumptions

### A-001 — Bare metal

The project should naturally work on compatible bare-metal Ubuntu Server, but v0.1.0 has no bare-metal-specific features or certification.

### A-002 — Locale

Preserve a valid existing locale. Change locale only when `bootstrap_locale` is explicitly set.

If locale state is invalid or missing, use a conservative Ubuntu-compatible fallback without surprising changes on otherwise valid hosts.

### A-003 — IPv6

If IPv6 is enabled on the host, the firewall baseline should protect IPv6 as well as IPv4.

An IPv4-only "secure firewall" is not acceptable.

### A-004 — Docker logging safety

A fresh Docker host should receive a sensible bounded/log-rotation-safe default only if current official Docker guidance supports it and the implementation can preserve existing daemon configuration safely.

The exact logging driver/settings are version-sensitive and must be revalidated before implementation.

### A-005 — Wrapper

A thin wrapper is useful but not a reason to delay the Ansible-native core.

Advanced generator UX is not a v0.1.0 release blocker.

## Open risks

### R-001 — Existing firewall coexistence

Interview decision: project-owned chains with dedicated persistence; strict stop on unknown consequential foreign policy.

Remaining implementation risk: classifier heuristics and atomic activation must be proven on the real VM.

### R-002 — Firewall atomicity / SSH lockout

The firewall implementation must minimize the chance that a partial apply locks out the active SSH session.

This requires real VM testing, not only synthetic tests.

### R-003 — SSH configuration precedence

Other sshd drop-ins may override or preempt intended values depending on OpenSSH parsing semantics.

The implementation must inspect effective configuration, not trust filenames alone.

### R-004 — Docker + firewall lifecycle

Docker creates/recreates firewall rules as networks/services change.

Project persistence/reload behavior must not compete with Docker-owned chains.

### R-005 — Docker daemon.json policy

Interview decision: preserve valid existing `daemon.json` by default; fresh hosts may receive `log-driver: local`.

Remaining implementation risk: defining malformed vs consequential conflict detection and fresh-host defaults at Phase 6B time with current upstream guidance.

### R-006 — Check-mode fidelity

Some system operations cannot be perfectly predicted.

The project must document honest limitations instead of implementing fake success.

### R-007 — Existing-server claim

Scenario 2 is not tested on a real preconfigured VM before v0.1.0.

Documentation must clearly distinguish synthetic existing-state coverage from real Scenario 1 validation.

### R-008 — Remote automation environment

GitHub repository creation, push, PR creation, and CI inspection depend on Cursor having appropriate Git/GitHub credentials/tools.

If unavailable, local work may continue, but remote completion must be reported as unavailable rather than simulated.

### R-009 — Toolchain drift

Pinned development versions age.

Version-sensitive dependencies must be updated through reviewed PRs and compatibility checks.

### R-010 — Overengineering

The biggest product risk is turning a focused MVP into a generic server-management framework.

Any feature outside the explicit MVP scope requires separate approval.
