# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.1.0 | Yes |
| 0.0.x | Development only; no routine security support |
| < 0.1.0 tags | Unsupported |

Only the latest patch release of a supported minor line receives routine security attention.

## Reporting a vulnerability

Do not open a public GitHub issue for security-sensitive reports.

Report security issues privately to the repository owner through GitHub Security Advisories or direct contact with the maintainer listed in the repository profile.

Include:

- affected version or commit,
- supported platform and environment,
- clear reproduction steps or proof of concept,
- impact assessment when known.

## Response expectations

- Acknowledgment target: within 7 days for valid reports.
- Fix or mitigation plan: as soon as practical for confirmed issues affecting supported versions.
- Coordinated disclosure is preferred when the issue is not already public.

## Scope notes for v0.1.0

This project configures real servers (SSH, firewall, packages, Docker). Treat misconfiguration or unsafe defaults as security-relevant even when they are not traditional software vulnerabilities.

In scope for v0.1.0:

- Ubuntu Server 24.04 LTS amd64 targets,
- documented `bootstrap_*` configuration,
- wrapper host-key trust behavior,
- SSH, firewall, Docker, and admin-user safety properties in `docs/03-SECURITY-SAFETY.md`.

Out of scope for routine security response:

- unsupported operating systems or architectures,
- operator misconfiguration outside documented variables,
- third-party upstream defects outside this repository's control,
- workload container images and application security beyond the Docker engine baseline.

## Secure development practices

The repository uses static validation, secret scanning, phased safety gates, and Scenario 1 VM validation documented in `docs/03-SECURITY-SAFETY.md`, `docs/05-TESTING-RELEASE.md`, and `docs/15-RELEASE-EVIDENCE.md`.

Private keys, credentials, and customer inventories must never be committed to this repository.
