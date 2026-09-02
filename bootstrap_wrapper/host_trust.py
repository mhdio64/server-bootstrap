"""Explicit SSH host-key trust handling."""

from __future__ import annotations

import subprocess
from pathlib import Path

from bootstrap_wrapper.errors import HostTrustError


def normalize_fingerprint(fingerprint: str) -> str:
    value = fingerprint.strip()
    if value.upper().startswith("SHA256:"):
        return "SHA256:" + value.split(":", 1)[1].lower()
    return value.lower()


def known_hosts_path() -> Path:
    return Path.home() / ".ssh" / "known_hosts"


def known_hosts_marker(connect_host: str, port: int) -> str:
    if port == 22:
        return connect_host
    return f"[{connect_host}]:{port}"


def host_is_known(connect_host: str, port: int) -> bool:
    marker = known_hosts_marker(connect_host, port)
    result = subprocess.run(
        ["ssh-keygen", "-F", marker],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def scan_host_keys(connect_host: str, port: int) -> str:
    result = subprocess.run(
        ["ssh-keyscan", "-p", str(port), "-H", connect_host],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise HostTrustError(
            f"Could not retrieve SSH host keys for {connect_host}:{port}. "
            f"{result.stderr.strip()}"
        )
    return result.stdout


def fingerprints_from_keyscan(keyscan_output: str) -> list[str]:
    result = subprocess.run(
        ["ssh-keygen", "-lf", "-"],
        input=keyscan_output,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise HostTrustError(
            "Could not compute SSH host-key fingerprints from ssh-keyscan output."
        )

    fingerprints: list[str] = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            fingerprints.append(parts[1])
    if not fingerprints:
        raise HostTrustError("No SSH host-key fingerprints were returned by ssh-keygen.")
    return fingerprints


def select_primary_fingerprint(fingerprints: list[str]) -> str:
    for fingerprint in fingerprints:
        if fingerprint.upper().startswith("SHA256:"):
            return fingerprint
    return fingerprints[0]


def fingerprint_matches_expected(presented: str, expected: str) -> bool:
    return normalize_fingerprint(presented) == normalize_fingerprint(expected)


def append_host_keys(keyscan_output: str) -> None:
    known_hosts = known_hosts_path()
    known_hosts.parent.mkdir(parents=True, exist_ok=True)
    if not known_hosts.exists():
        known_hosts.touch(mode=0o600)
    with known_hosts.open("a", encoding="utf-8") as handle:
        handle.write(keyscan_output)
        if not keyscan_output.endswith("\n"):
            handle.write("\n")
    known_hosts.chmod(0o600)


def prompt_for_trust(connect_host: str, port: int, fingerprint: str) -> bool:
    target = f"{connect_host}:{port}"
    answer = input(
        "The SSH host key for "
        f"{target} is not in your known_hosts file.\n"
        f"Presented fingerprint: {fingerprint}\n"
        "Add this host key and continue? [y/N]: "
    ).strip()
    return answer.lower() in {"y", "yes"}


def ensure_host_trust(
    connect_host: str,
    port: int,
    *,
    expected_fingerprint: str | None,
    allow_interactive: bool,
) -> None:
    keyscan_output = scan_host_keys(connect_host, port)
    fingerprints = fingerprints_from_keyscan(keyscan_output)
    primary_fingerprint = select_primary_fingerprint(fingerprints)

    if expected_fingerprint is not None:
        if not any(
            fingerprint_matches_expected(candidate, expected_fingerprint)
            for candidate in fingerprints
        ):
            raise HostTrustError(
                "SSH host-key verification failed. Presented fingerprint "
                f"{primary_fingerprint} does not match the expected fingerprint "
                f"{expected_fingerprint}."
            )

    if host_is_known(connect_host, port):
        return

    if expected_fingerprint is not None:
        append_host_keys(keyscan_output)
        return

    if not allow_interactive:
        raise HostTrustError(
            "SSH host key for "
            f"{connect_host}:{port} is not trusted. Provide "
            "--expected-host-fingerprint after out-of-band verification, or run "
            "interactively to approve the presented key."
        )

    if not prompt_for_trust(connect_host, port, primary_fingerprint):
        raise HostTrustError(
            "SSH host-key enrollment was rejected. Bootstrap stopped before mutation."
        )

    append_host_keys(keyscan_output)
