"""Inventory helpers for single-target enforcement."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from bootstrap_wrapper.errors import InventoryError


def ansible_env(toolkit_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["ANSIBLE_CONFIG"] = str(toolkit_root / "ansible.cfg")
    return env


def list_inventory_hosts(inventory_path: Path, toolkit_root: Path) -> list[str]:
    result = subprocess.run(
        ["ansible", "all", "--list-hosts", "-i", str(inventory_path)],
        capture_output=True,
        text=True,
        check=False,
        cwd=toolkit_root,
        env=ansible_env(toolkit_root),
    )
    if result.returncode != 0:
        raise InventoryError(
            "Failed to read inventory "
            f"{inventory_path}: {result.stderr.strip() or result.stdout.strip()}"
        )

    hosts: list[str] = []
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("hosts ("):
            continue
        hosts.append(stripped)
    return hosts


def require_single_target_host(inventory_path: Path, toolkit_root: Path) -> str:
    hosts = list_inventory_hosts(inventory_path, toolkit_root)
    if len(hosts) == 0:
        raise InventoryError(
            f"Inventory {inventory_path} does not define any hosts for pattern 'all'."
        )
    if len(hosts) > 1:
        raise InventoryError(
            "server-bootstrap v0.1.0 supports exactly one target per invocation. "
            f"Inventory {inventory_path} resolved {len(hosts)} hosts: {', '.join(hosts)}"
        )
    return hosts[0]


def get_host_connection_info(
    inventory_path: Path,
    toolkit_root: Path,
    host_name: str,
) -> dict[str, object]:
    result = subprocess.run(
        [
            "ansible-inventory",
            "-i",
            str(inventory_path),
            "--host",
            host_name,
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=toolkit_root,
        env=ansible_env(toolkit_root),
    )
    if result.returncode != 0:
        raise InventoryError(
            f"Failed to resolve host variables for {host_name}: "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise InventoryError(
            f"Failed to parse inventory host data for {host_name}: {exc}"
        ) from exc


def resolve_connection_target(
    inventory_path: Path,
    toolkit_root: Path,
    host_name: str,
) -> tuple[str, int]:
    host_vars = get_host_connection_info(inventory_path, toolkit_root, host_name)
    connect_host = str(host_vars.get("ansible_host", host_name))
    port_raw = host_vars.get("ansible_port", 22)
    try:
        port = int(port_raw)
    except (TypeError, ValueError) as exc:
        raise InventoryError(
            f"Invalid ansible_port for host {host_name}: {port_raw!r}"
        ) from exc
    if port < 1 or port > 65535:
        raise InventoryError(
            f"Invalid ansible_port for host {host_name}: {port}"
        )
    return connect_host, port
