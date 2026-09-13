from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from bootstrap_wrapper.cli import build_parser, resolve_extra_vars_path, run_command
from bootstrap_wrapper.errors import BootstrapWrapperError, InventoryError
from bootstrap_wrapper.host_trust import (
    fingerprint_matches_expected,
    known_hosts_marker,
    normalize_fingerprint,
    select_primary_fingerprint,
)
from bootstrap_wrapper.inventory import require_single_target_host
from bootstrap_wrapper.paths import toolkit_root
from bootstrap_wrapper.runner import build_playbook_command


class WrapperCliTests(unittest.TestCase):
    def test_build_parser_requires_subcommand(self) -> None:
        with self.assertRaises(SystemExit):
            build_parser().parse_args([])

    def test_resolve_extra_vars_defaults_beside_inventory(self) -> None:
        with mock.patch("pathlib.Path.is_file", return_value=True):
            path = resolve_extra_vars_path(Path("/tmp/project/inventory.yml"), None)
        self.assertEqual(path, Path("/tmp/project/bootstrap.yml").resolve())

    def test_parser_accepts_ask_pass_and_ask_become_pass(self) -> None:
        for cmd in ["check", "apply", "verify"]:
            args = build_parser().parse_args([cmd, "-i", "inventory.yml", "-k", "-K"])
            self.assertTrue(args.ask_pass)
            self.assertTrue(args.ask_become_pass)

            args_long = build_parser().parse_args(
                [cmd, "-i", "inventory.yml", "--ask-pass", "--ask-become-pass"]
            )
            self.assertTrue(args_long.ask_pass)
            self.assertTrue(args_long.ask_become_pass)

    def test_run_command_requires_tty_for_password_prompts(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["check", "-i", "inventory.yml", "-k"])
        with mock.patch("pathlib.Path.is_file", return_value=True), \
             mock.patch("bootstrap_wrapper.cli.resolve_extra_vars_path", return_value=Path("/tmp/bootstrap.yml")), \
             mock.patch("bootstrap_wrapper.cli.require_single_target_host", return_value="target"), \
             mock.patch("bootstrap_wrapper.cli.resolve_connection_target", return_value=("192.0.2.1", 22)), \
             mock.patch("sys.stdin.isatty", return_value=False):
            with self.assertRaises(BootstrapWrapperError) as ctx:
                run_command(args)
            self.assertIn("require an interactive terminal (TTY)", str(ctx.exception))

    def test_run_command_requires_sshpass_for_ask_pass(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["check", "-i", "inventory.yml", "-k"])
        with mock.patch("pathlib.Path.is_file", return_value=True), \
             mock.patch("bootstrap_wrapper.cli.resolve_extra_vars_path", return_value=Path("/tmp/bootstrap.yml")), \
             mock.patch("bootstrap_wrapper.cli.require_single_target_host", return_value="target"), \
             mock.patch("bootstrap_wrapper.cli.resolve_connection_target", return_value=("192.0.2.1", 22)), \
             mock.patch("sys.stdin.isatty", return_value=True), \
             mock.patch("shutil.which", return_value=None):
            with self.assertRaises(BootstrapWrapperError) as ctx:
                run_command(args)
            self.assertIn("requires 'sshpass' to be installed", str(ctx.exception))


class WrapperHostTrustTests(unittest.TestCase):
    def test_normalize_fingerprint_sha256(self) -> None:
        self.assertEqual(
            normalize_fingerprint("SHA256:AbCdEfGh"),
            "SHA256:abcdefgh",
        )

    def test_fingerprint_matches_expected(self) -> None:
        self.assertTrue(
            fingerprint_matches_expected(
                "SHA256:abcDEF",
                "sha256:abcdef",
            )
        )

    def test_select_primary_fingerprint_prefers_sha256(self) -> None:
        selected = select_primary_fingerprint(
            ["MD5:aa:bb:cc", "SHA256:preferred"]
        )
        self.assertEqual(selected, "SHA256:preferred")

    def test_known_hosts_marker_non_default_port(self) -> None:
        self.assertEqual(known_hosts_marker("203.0.113.10", 2222), "[203.0.113.10]:2222")


class WrapperInventoryTests(unittest.TestCase):
    def test_require_single_target_host_rejects_multiple_hosts(self) -> None:
        with mock.patch(
            "bootstrap_wrapper.inventory.list_inventory_hosts",
            return_value=["one", "two"],
        ):
            with self.assertRaises(InventoryError):
                require_single_target_host(Path("inventory.yml"), toolkit_root())


class WrapperRunnerTests(unittest.TestCase):
    def test_build_playbook_command_for_check_mode(self) -> None:
        root = toolkit_root()
        command = build_playbook_command(
            toolkit_root=root,
            playbook="site.yml",
            inventory_path=Path("/tmp/project/inventory.yml"),
            extra_vars_path=Path("/tmp/project/bootstrap.yml"),
            check_mode=True,
        )
        self.assertEqual(command[0], "ansible-playbook")
        self.assertIn("--check", command)
        self.assertIn("--diff", command)
        self.assertIn("-e", command)
        self.assertIn("@/tmp/project/bootstrap.yml", command)
        self.assertIn("inventory_dir=/tmp/project", command)

    def test_build_playbook_command_with_passwords(self) -> None:
        root = toolkit_root()
        command = build_playbook_command(
            toolkit_root=root,
            playbook="site.yml",
            inventory_path=Path("/tmp/project/inventory.yml"),
            extra_vars_path=Path("/tmp/project/bootstrap.yml"),
            ask_pass=True,
            ask_become_pass=True,
        )
        self.assertEqual(command[0], "ansible-playbook")
        self.assertIn("--ask-pass", command)
        self.assertIn("--ask-become-pass", command)


if __name__ == "__main__":
    unittest.main()
