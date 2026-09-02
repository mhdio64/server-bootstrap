"""Ansible subprocess execution helpers."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from bootstrap_wrapper.inventory import ansible_env


def build_playbook_command(
    *,
    toolkit_root: Path,
    playbook: str,
    inventory_path: Path,
    extra_vars_path: Path,
    check_mode: bool = False,
) -> list[str]:
    command = [
        "ansible-playbook",
        str(toolkit_root / playbook),
        "-i",
        str(inventory_path),
        "-e",
        f"@{extra_vars_path}",
        "-e",
        f"inventory_dir={inventory_path.parent}",
    ]
    if check_mode:
        command.extend(["--check", "--diff"])
    return command


def run_ansible_command(command: list[str], *, toolkit_root: Path, log_path: Path) -> int:
    with log_path.open("a", encoding="utf-8") as log_handle:
        log_handle.write("$ " + " ".join(command) + "\n")
        log_handle.flush()
        process = subprocess.Popen(
            command,
            cwd=toolkit_root,
            env=ansible_env(toolkit_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        assert process.stdout is not None
        for line in process.stdout:
            sys.stdout.write(line)
            log_handle.write(line)
        return process.wait()
