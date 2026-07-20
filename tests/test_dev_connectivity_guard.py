import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "product/package/batocera-luigios-dev-connectivity"
GUARD = PACKAGE / "files/luigios-dev-connectivity-guard"
INIT = PACKAGE / "files/S07luigios-dev-connectivity"


class DevConnectivityGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.runtime = self.base / "runtime"
        self.marker = self.base / "developer-mode.enabled"
        self.state = self.base / "state"
        self.bin = self.base / "bin"
        self.state.mkdir()
        self.bin.mkdir()
        (self.state / "route").write_text("healthy\n")
        (self.state / "power").write_text("on\n")
        (self.state / "commands").write_text("")
        self.write_mock(
            "ip",
            """#!/bin/sh
if [ "$(cat "$MOCK_STATE/route")" = healthy ]; then
    echo 'default via 192.0.2.1 dev wlan0'
fi
""",
        )
        self.write_mock(
            "connmanctl",
            """#!/bin/sh
case "$1" in
  technologies)
    echo '  Name = WiFi'
    if [ "$(cat "$MOCK_STATE/power")" = on ]; then
      echo '  Powered = True'
    else
      echo '  Powered = False'
    fi
    ;;
  services) echo '*AO Lab WiFi wifi_aabbccddeeff_lab_managed_psk' ;;
  enable|connect) printf '%s\n' "$*" >>"$MOCK_STATE/commands" ;;
esac
""",
        )
        self.write_mock(
            "logger",
            "#!/bin/sh\nprintf 'logger %s\n' \"$*\" >>\"$MOCK_STATE/commands\"\n",
        )

    def tearDown(self):
        self.temporary.cleanup()

    def write_mock(self, name, body):
        path = self.bin / name
        path.write_text(body)
        path.chmod(0o755)

    def run_guard(self, active_ssh="0"):
        return subprocess.run(
            [str(GUARD), "once"],
            check=False,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "PATH": f"{self.bin}:{os.environ['PATH']}",
                "MOCK_STATE": str(self.state),
                "LUIGIOS_DEVELOPER_MODE_MARKER": str(self.marker),
                "LUIGIOS_DEV_CONNECTIVITY_RUNTIME": str(self.runtime),
                "LUIGIOS_DEV_CONNECTIVITY_ACTIVE_SSH": active_ssh,
            },
        )

    def status(self):
        values = {}
        for line in (self.runtime / "status").read_text().splitlines():
            key, value = line.split("=", 1)
            values[key] = value
        return values

    def commands(self):
        return (self.state / "commands").read_text().splitlines()

    def begin_protected_session(self):
        self.marker.touch()
        result = self.run_guard(active_ssh="1")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("protected", self.status()["state"])
        self.assertEqual(
            "wifi_aabbccddeeff_lab_managed_psk",
            (self.runtime / "last-wifi-service").read_text().strip(),
        )

    def test_guard_is_dormant_outside_developer_mode(self):
        result = self.run_guard(active_ssh="1")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("dormant", self.status()["state"])
        self.assertEqual([], self.commands())

    def test_route_loss_reconnects_last_healthy_service_with_backoff(self):
        self.begin_protected_session()
        (self.state / "route").write_text("down\n")
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn(
            "connect wifi_aabbccddeeff_lab_managed_psk", self.commands()
        )
        first_count = len([line for line in self.commands() if line.startswith("connect ")])
        self.run_guard()
        second_count = len([line for line in self.commands() if line.startswith("connect ")])
        self.assertEqual(first_count, second_count)

    def test_radio_is_reenabled_only_when_it_was_on_at_session_start(self):
        self.begin_protected_session()
        (self.state / "route").write_text("down\n")
        (self.state / "power").write_text("off\n")
        self.run_guard()
        self.assertIn("enable wifi", self.commands())

        shutil.rmtree(self.runtime)
        (self.state / "commands").write_text("")
        (self.state / "route").write_text("healthy\n")
        (self.state / "power").write_text("off\n")
        self.begin_protected_session()
        (self.state / "route").write_text("down\n")
        self.run_guard()
        self.assertNotIn("enable wifi", self.commands())

    def test_package_is_wired_and_never_restarts_network_stack(self):
        top = (ROOT / "Config.in").read_text()
        makefile = (PACKAGE / "batocera-luigios-dev-connectivity.mk").read_text()
        guard = GUARD.read_text()
        self.assertIn("batocera-luigios-dev-connectivity/Config.in", top)
        self.assertIn("BATOCERA_LUIGIOS_DEV_CONNECTIVITY_DEPENDENCIES = connman", makefile)
        self.assertIn("connmanctl connect", guard)
        for forbidden in ("systemctl", "service connman", "S30connman restart", "NetworkManager"):
            self.assertNotIn(forbidden, guard)

    def test_shell_files_parse(self):
        for script in (GUARD, INIT):
            result = subprocess.run(
                ["sh", "-n", script], check=False, capture_output=True, text=True
            )
            self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
