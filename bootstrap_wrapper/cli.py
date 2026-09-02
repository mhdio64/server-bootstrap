"""Command-line interface for the server-bootstrap wrapper."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from bootstrap_wrapper.errors import BootstrapWrapperError
from bootstrap_wrapper.host_trust import ensure_host_trust
from bootstrap_wrapper.inventory import require_single_target_host, resolve_connection_target
from bootstrap_wrapper.paths import new_log_path, read_toolkit_version, toolkit_root
from bootstrap_wrapper.runner import build_playbook_command, run_ansible_command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bootstrap",
        description="Thin wrapper for server-bootstrap Ansible playbooks.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"server-bootstrap {read_toolkit_version()}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-i",
        "--inventory",
        required=True,
        help="Path to inventory.yml with connection data for exactly one target host.",
    )
    common.add_argument(
        "-e",
        "--extra-vars",
        help=(
            "Path to bootstrap.yml with desired bootstrap_* state. "
            "Defaults to bootstrap.yml beside the inventory file."
        ),
    )
    common.add_argument(
        "--expected-host-fingerprint",
        help=(
            "Expected SSH host-key fingerprint (SHA256:...). "
            "Required for non-interactive first-time host trust."
        ),
    )

    subparsers.add_parser(
        "check",
        parents=[common],
        help="Run preflight and apply playbooks in check mode without mutation.",
    )
    apply_parser = subparsers.add_parser(
        "apply",
        parents=[common],
        help="Run preflight and apply playbooks on the target host.",
    )
    apply_parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip interactive apply confirmation.",
    )
    subparsers.add_parser(
        "verify",
        parents=[common],
        help="Run post-apply critical verification and summary.",
    )
    return parser


def resolve_extra_vars_path(inventory_path: Path, extra_vars: str | None) -> Path:
    if extra_vars is not None:
        extra_vars_path = Path(extra_vars)
    else:
        extra_vars_path = inventory_path.parent / "bootstrap.yml"
    if not extra_vars_path.is_file():
        raise BootstrapWrapperError(
            f"Extra-vars file not found: {extra_vars_path}. "
            "Provide --extra-vars or place bootstrap.yml beside inventory.yml."
        )
    return extra_vars_path.resolve()


def confirm_apply(host_name: str, connect_host: str, port: int) -> None:
    target = f"{host_name} ({connect_host}:{port})"
    answer = input(
        f"This will apply server-bootstrap to {target}.\nContinue? [y/N]: "
    ).strip()
    if answer.lower() not in {"y", "yes"}:
        raise BootstrapWrapperError("Apply cancelled by operator.")


def run_command(args: argparse.Namespace) -> int:
    root = toolkit_root()
    inventory_path = Path(args.inventory).resolve()
    if not inventory_path.is_file():
        raise BootstrapWrapperError(f"Inventory file not found: {inventory_path}")

    extra_vars_path = resolve_extra_vars_path(inventory_path, args.extra_vars)
    host_name = require_single_target_host(inventory_path, root)
    connect_host, port = resolve_connection_target(inventory_path, root, host_name)

    allow_interactive = sys.stdin.isatty()
    ensure_host_trust(
        connect_host,
        port,
        expected_fingerprint=args.expected_host_fingerprint,
        allow_interactive=allow_interactive,
    )

    if args.command == "apply" and not args.yes:
        if not allow_interactive:
            raise BootstrapWrapperError(
                "Interactive apply confirmation requires a TTY. Re-run with --yes "
                "for non-interactive automation."
            )
        confirm_apply(host_name, connect_host, port)

    playbook = "site.yml" if args.command in {"check", "apply"} else "verify.yml"
    command = build_playbook_command(
        toolkit_root=root,
        playbook=playbook,
        inventory_path=inventory_path,
        extra_vars_path=extra_vars_path,
        check_mode=args.command == "check",
    )

    log_path = new_log_path(args.command)
    print(f"Logging to {log_path}")
    return run_ansible_command(command, toolkit_root=root, log_path=log_path)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run_command(args)
    except BootstrapWrapperError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
