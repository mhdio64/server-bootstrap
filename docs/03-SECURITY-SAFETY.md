# Security and Safety Model

## Core safety invariant

```text
Known + owned -> reconcile
Unknown + harmless -> preserve
Unknown + consequential -> stop
```

Never destroy unknown configuration silently.

## Preflight before mutation

Critical checks should happen before apply whenever possible:

- supported target OS/version
- supported architecture
- required privilege escalation
- remote Python availability
- required public configuration
- admin SSH key availability
- effective SSH port
- firewall backend/state classification
- APT/dpkg readiness
- critical upstream reachability when needed
- Docker installation/repository classification when Docker is enabled

Dangerous configuration fails before mutation.

## SSH safety

Requirements:

- do not replace the full `/etc/ssh/sshd_config`
- own a dedicated project drop-in
- verify at least one usable admin public key before disabling password-based access
- validate candidate configuration before activation
- inspect effective configuration, not just the managed file
- detect consequential conflicting drop-ins
- reload only after validation
- verify reconnection after a change that could affect access
- changing SSH port requires explicit configuration

Host-key checking must not be disabled globally.

New-host trust must be explicit. A future wrapper may display the presented fingerprint and ask the user to approve it before updating known_hosts.

## Admin credentials

Allowed:

- distribute public SSH keys

Forbidden:

- store user private keys
- copy user private keys
- generate user private keys on the user's behalf
- commit passwords/tokens
- print credentials in logs

The default admin account has:

- public-key SSH login
- password locked/unset
- NOPASSWD sudo

## Firewall safety

MVP backend: `iptables-nft`.

Requirements:

- verify expected backend
- preserve SSH access before activation
- model both IPv4 and IPv6 when IPv6 is enabled
- never globally `iptables -F`
- never globally `iptables -X`
- never blindly restore a full ruleset that includes Docker-managed chains
- do not mutate Docker-owned chains
- ambiguous consequential foreign policy -> fail before mutation

Conceptual baseline:

```text
INPUT   DROP
FORWARD DROP
OUTPUT  ACCEPT
```

Allow:

- loopback
- ESTABLISHED/RELATED
- required ICMP/ICMPv6
- effective SSH port
- explicitly configured ports

Container published-port policy is outside MVP scope.

## Docker safety

Install only through an explicit auditable official-repository flow.

Forbidden:

```text
curl ... | sh
```

Existing state must be classified before apply.

Do not automatically remove conflicting packages or migrate an unknown Docker installation.

Repository/configuration that merely looks correct in text should not be considered valid when a native APT/repository validation can be performed.

Docker success requires functional verification, not only package presence.

## APT/dpkg safety

If the package manager is busy:

- wait for a bounded time,
- do not kill the package-manager process,
- do not delete lock files,
- fail with an actionable message if the lock remains.

Transient network/repository errors may receive bounded retry.

## External artifacts

Use:

- official vendor source,
- HTTPS,
- signature/checksum verification when upstream provides a meaningful mechanism.

Avoid unknown mirrors and arbitrary installer scripts.

## Secrets and logging

- no private keys
- no tokens/passwords in logs
- use `no_log` only for truly sensitive tasks
- do not make all tasks opaque to debugging
- do not place credentials in command-line arguments when avoidable
- CI artifacts must not leak secrets

## Failure behavior

- warning -> exit 0 when the desired state is otherwise valid
- safety/preflight failure -> non-zero
- configuration/task failure -> non-zero
- critical verification failure -> non-zero
- reboot required -> warning + successful result

## Rollback model

No generic automatic full rollback.

Use transactional patterns for critical config:

```text
render candidate
-> validate
-> activate atomically where practical
-> reload
-> verify
```

For general package/config convergence, rely on idempotent safe rerun.

## Supply-chain policy

Prefer `ansible.builtin`.

A new external Collection or material dependency requires explicit justification and approval.

GitHub Actions should be pinned to full commit SHAs and updated through reviewed dependency PRs.

Dependency bots may open PRs but must not auto-merge.
