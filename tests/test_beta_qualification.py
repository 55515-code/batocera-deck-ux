import importlib.machinery
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "profiles/beta-qualification-v1.json").read_text())
loader = importlib.machinery.SourceFileLoader("device_qa", str(ROOT / "tools/device-qa"))
spec = importlib.util.spec_from_loader(loader.name, loader)
device_qa = importlib.util.module_from_spec(spec)
loader.exec_module(device_qa)


class BetaQualificationTests(unittest.TestCase):
    def test_project_remains_experimental_and_beta_requires_complete_product(self):
        self.assertEqual("experimental", POLICY["current_channel"])
        self.assertTrue(POLICY["beta_entry"]["all_required"])
        gates = set(POLICY["beta_entry"]["gates"])
        self.assertTrue(
            {
                "complete-brand-surfaces",
                "desktop-session",
                "developer-connectivity-protection",
                "settings-application",
                "backup-restore",
                "migration",
                "offline-no-account-vanilla",
                "original-interface-review",
                "secure-implementation-review",
            }
            <= gates
        )
        interface = POLICY["beta_entry"]["interface_acceptance"]
        self.assertEqual("interface-guidelines-v1.json", interface["policy"])
        self.assertTrue(interface["offline_first_boot_and_local_play"])
        self.assertTrue(interface["third_party_login_scoped_to_service"])
        self.assertTrue(interface["proprietary_trade_dress_review"])
        secure = POLICY["beta_entry"]["secure_implementation_acceptance"]
        self.assertEqual("secure-implementation-v1.json", secure["policy"])
        self.assertTrue(secure["memory_safe_default_for_new_sensitive_code"])
        self.assertTrue(secure["native_binary_hardening_verified"])
        self.assertTrue(secure["least_privilege_runtime_review"])

    def test_rom_storage_is_hard_excluded_and_removed_during_install(self):
        qa = POLICY["device_qa"]
        install = POLICY["fresh_install"]
        private_profile = json.loads(
            (ROOT / "profiles/private-system-v1.json").read_text()
        )
        self.assertIn("/userdata/roms", qa["hard_deny_write_roots"])
        self.assertTrue(install["physically_remove_rom_sd_during_install"])
        self.assertTrue(install["never_format_or_initialize_existing_rom_sd"])
        self.assertFalse(install["backup_rom_payloads"])
        for component in private_profile["components"]:
            self.assertFalse(
                component["path"] == "/userdata/roms"
                or component["path"].startswith("/userdata/roms/"),
                component,
            )

    def test_remote_probe_contains_no_mutating_commands(self):
        probe = device_qa.REMOTE_PROBE
        for forbidden in (
            "rm ",
            "mv ",
            "cp ",
            "chmod ",
            "chown ",
            "mount ",
            "umount ",
            "reboot",
            "poweroff",
            "systemctl",
            "batocera-settings-set",
        ):
            self.assertNotIn(forbidden, probe)

    def test_probe_evaluation_requires_separate_removable_rom_storage(self):
        values = {
            "HOSTNAME": "LUIGIOS",
            "USERDATA_SOURCE": "/dev/nvme0n1p2",
            "USERDATA_OPTIONS": "rw,relatime",
            "USERDATA_TOTAL_KIB": "100000000",
            "USERDATA_AVAILABLE_KIB": "30000000",
            "ROM_SOURCE": "/dev/mmcblk0p1[/batocera/roms]",
            "USERDATA_DEVICE_ID": "1",
            "ROM_DEVICE_ID": "2",
            "SSH_DAEMON_COUNT": "2",
        }
        checks = device_qa.evaluate(values, POLICY)
        blocking = [
            item for item in checks if item["blocking"] and item["status"] != "pass"
        ]
        self.assertEqual([], blocking)


if __name__ == "__main__":
    unittest.main()
