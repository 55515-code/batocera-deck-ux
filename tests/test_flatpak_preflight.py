import json
import os
import pathlib
import stat
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "prototype/desktop/flatpak-preflight"


class FlatpakPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.fixture = pathlib.Path(self.tempdir.name)
        self.bin_dir = self.fixture / "bin"
        self.bin_dir.mkdir()
        self.kernel_config = self.fixture / "kernel.config"
        self.kernel_config.write_text("CONFIG_USER_NS=y\n")
        self.namespace_limit = self.fixture / "max_user_namespaces"
        self.namespace_limit.write_text("4096\n")
        for command in (
            "unshare",
            "bwrap",
            "flatpak",
            "xdg-desktop-portal",
            "xdg-desktop-portal-kde",
            "xdg-desktop-portal-cosmic",
        ):
            self.fake_command(command)

    def fake_command(self, name, body="exit 0"):
        path = self.bin_dir / name
        path.write_text(f"#!/bin/sh\n{body}\n")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def run_preflight(self, *extra, kernel_config=True):
        command = [
            str(PREFLIGHT),
            "--format",
            "json",
            "--userns-sysctl",
            str(self.namespace_limit),
            "--portal-dir",
            str(self.bin_dir),
        ]
        if kernel_config:
            command.extend(("--kernel-config", str(self.kernel_config)))
        command.extend(extra)
        env = os.environ.copy()
        env["PATH"] = f"{self.bin_dir}:/usr/bin:/bin"
        result = subprocess.run(command, check=False, capture_output=True, text=True, env=env)
        return result, json.loads(result.stdout)

    def test_supported_result_is_machine_readable(self):
        result, report = self.run_preflight()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("supported", report["status"])
        self.assertEqual(0, report["exit_code"])
        self.assertTrue(all(item["status"] == "supported" for item in report["probes"]))

    def test_missing_kernel_evidence_is_inconclusive(self):
        missing = self.fixture / "missing.config"
        result, report = self.run_preflight("--kernel-config", str(missing), kernel_config=False)

        self.assertEqual(2, result.returncode)
        self.assertEqual("inconclusive", report["status"])
        kernel = next(item for item in report["probes"] if item["name"] == "kernel_config")
        self.assertEqual("inconclusive", kernel["status"])
        self.assertIn("unavailable", kernel["summary"])

    def test_denied_runtime_namespace_is_unsupported(self):
        self.fake_command("unshare", 'echo "unshare: Operation not permitted" >&2\nexit 1')
        result, report = self.run_preflight()

        self.assertEqual(1, result.returncode)
        self.assertEqual("unsupported", report["status"])
        namespace = next(item for item in report["probes"] if item["name"] == "user_namespace_runtime")
        self.assertIn("Operation not permitted", namespace["summary"])
        self.assertTrue(namespace["action"])

    def test_bubblewrap_failure_is_reported_separately(self):
        self.fake_command("bwrap", 'echo "bwrap: namespace setup failed" >&2\nexit 1')
        result, report = self.run_preflight()

        self.assertEqual(1, result.returncode)
        bubblewrap = next(item for item in report["probes"] if item["name"] == "bubblewrap")
        self.assertEqual("unsupported", bubblewrap["status"])
        self.assertIn("namespace setup failed", bubblewrap["summary"])

    def test_portal_frontend_and_backend_are_required(self):
        (self.bin_dir / "xdg-desktop-portal-kde").unlink()
        (self.bin_dir / "xdg-desktop-portal-cosmic").unlink()
        result, report = self.run_preflight()

        self.assertEqual(1, result.returncode)
        portals = next(item for item in report["probes"] if item["name"] == "desktop_portals")
        self.assertEqual("unsupported", portals["status"])
        self.assertIn("portal backend", portals["summary"])

    def test_app_launch_only_occurs_when_explicitly_requested(self):
        log = self.fixture / "flatpak.log"
        self.fake_command("flatpak", f'printf "%s\\n" "$*" >>"{log}"\nexit 0')

        result, _ = self.run_preflight()
        self.assertEqual(0, result.returncode)
        self.assertFalse(log.exists())

        result, report = self.run_preflight("--launch-app", "org.example.Test", "--launch-wait", "0.2")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["info org.example.Test", "run org.example.Test"], log.read_text().splitlines())
        launch = next(item for item in report["probes"] if item["name"] == "app_launch")
        self.assertEqual("supported", launch["status"])

    def test_implementation_does_not_weaken_runtime_policy(self):
        source = PREFLIGHT.read_text()
        for forbidden in ("sysctl -w", "chmod u+s", "setcap ", "aa-disable", "apparmor_parser"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
