import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "profiles" / "experience-modes-v1.json"


class ExperienceModesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))

    def test_gamer_mode_is_the_locked_down_graphical_default(self):
        self.assertEqual("gamer", self.policy["default_mode"])
        gamer = self.policy["modes"]["gamer"]
        self.assertTrue(gamer["controller_first"])
        self.assertTrue(gamer["full_device_configuration_gui"])
        self.assertFalse(gamer["show_terminal"])
        self.assertFalse(gamer["show_root_filesystem"])
        self.assertFalse(gamer["show_package_manager_internals"])

    def test_developer_mode_adds_detail_without_replacing_gui(self):
        developer = self.policy["modes"]["developer"]
        self.assertEqual("gamer", developer["inherits"])
        self.assertTrue(developer["full_device_configuration_gui"])
        self.assertTrue(developer["show_terminal"])
        self.assertTrue(developer["show_raw_service_logs"])
        self.assertTrue(self.policy["presentation"]["developer_tools_remain_gui_discoverable"])
        self.assertTrue(self.policy["presentation"]["terminal_is_never_required_for_supported_workflows"])

    def test_activation_is_explicit_reversible_and_never_silent(self):
        activation = self.policy["activation"]
        self.assertTrue(activation["requires_explicit_confirmation"])
        self.assertFalse(activation["may_be_enabled_silently"])
        self.assertTrue(activation["requires_session_restart"])
        self.assertTrue(activation["recovery_can_disable"])

    def test_developer_mode_does_not_weaken_security_invariants(self):
        security = self.policy["security_invariants"]
        self.assertFalse(security["ui_runs_as_root"])
        self.assertFalse(security["allow_arbitrary_privileged_commands"])
        self.assertTrue(security["signed_update_verification_always_enabled"])
        self.assertTrue(security["base_image_immutable"])
        self.assertTrue(security["typed_privilege_broker_required"])

    def test_developer_connectivity_protects_ssh_without_owning_network_policy(self):
        connectivity = self.policy["developer_connectivity"]
        self.assertTrue(connectivity["protect_active_ssh_sessions"])
        self.assertTrue(connectivity["monitor_default_route"])
        self.assertTrue(connectivity["remember_last_healthy_wifi_service"])
        self.assertTrue(connectivity["reconnect_through_existing_connman"])
        self.assertFalse(connectivity["restart_network_stack"])
        self.assertFalse(connectivity["replace_network_policy"])
        self.assertFalse(connectivity["active_outside_developer_mode"])
        self.assertLessEqual(connectivity["maximum_retry_backoff_seconds"], 120)


if __name__ == "__main__":
    unittest.main()
