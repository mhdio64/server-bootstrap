# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.0.x (development) | Best effort |
| 0.1.x | Planned after first MVP release |

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

Out of scope for routine security response:

- unsupported operating systems or architectures documented in `docs/01-PROJECT-SPEC.md`,
- operator misconfiguration outside documented variables,
- third-party upstream defects outside this repository's control.

## Secure development practices

The repository uses static validation, secret scanning, and phased safety gates documented in `docs/03-SECURITY-SAFETY.md` and `docs/05-TESTING-RELEASE.md`.

Private keys, credentials, and customer inventories must never be committed to this repository.
