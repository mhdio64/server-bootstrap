"""Toolkit and log path helpers."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path


def toolkit_root() -> Path:
    return Path(__file__).resolve().parent.parent


def read_toolkit_version(root: Path | None = None) -> str:
    version_file = (root or toolkit_root()) / "VERSION"
    return version_file.read_text(encoding="utf-8").strip()


def default_log_dir() -> Path:
    state_home = os.environ.get("XDG_STATE_HOME")
    if state_home:
        base = Path(state_home)
    else:
        base = Path.home() / ".local" / "state"
    log_dir = base / "server-bootstrap" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(log_dir, 0o700)
    return log_dir


def new_log_path(command: str, log_dir: Path | None = None) -> Path:
    directory = log_dir or default_log_dir()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = directory / f"{command}-{timestamp}.log"
    log_path.touch(mode=0o600)
    os.chmod(log_path, 0o600)
    return log_path
