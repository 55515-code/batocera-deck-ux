import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "profiles/interface-guidelines-v1.json").read_text())


class InterfaceGuidelinesTests(unittest.TestCase):
    def test_interface_is_original_without_rejecting_familiar_usability(self):
        origin = POLICY["design_origin"]
        self.assertTrue(origin["original_luigios_system_required"])
        self.assertTrue(origin["third_party_products_may_be_studied_for_general_usability"])
        for key in (
            "copy_proprietary_trade_dress",
            "copy_proprietary_assets_or_sounds",
            "copy_proprietary_screen_geometry",
        ):
            self.assertFalse(origin[key], key)

    def test_navigation_and_layout_are_controller_first(self):
        navigation = POLICY["navigation"]
        self.assertTrue(navigation["controller_complete"])
        self.assertTrue(navigation["single_visible_focus"])
        self.assertFalse(navigation["pointer_only_actions_allowed"])
        self.assertFalse(navigation["focus_traps_allowed"])
        self.assertGreaterEqual(POLICY["layout"]["minimum_touch_target_logical_px"], 44)

    def test_vanilla_distribution_never_requires_network_or_login(self):
        offline = POLICY["vanilla_offline_contract"]
        self.assertTrue(offline["network_setup_skippable"])
        for key, value in offline.items():
            if key != "network_setup_skippable":
                self.assertFalse(value, key)

    def test_optional_services_cannot_gate_vanilla_luigios(self):
        services = POLICY["optional_service_contract"]
        self.assertTrue(services["third_party_service_may_require_own_login"])
        self.assertTrue(services["third_party_service_may_require_network"])
        self.assertTrue(services["requirement_scoped_to_optional_service"])
        self.assertFalse(services["vanilla_shell_blocked_by_service"])
        self.assertFalse(services["local_device_controls_blocked_by_service"])

    def test_human_guideline_contains_clean_room_and_offline_gates(self):
        text = (ROOT / "docs/INTERFACE_GUIDELINES.md").read_text()
        self.assertIn("must not copy", text)
        self.assertIn("without an internet connection or login", text)
        self.assertIn("Network setup is always skippable", text)
        self.assertIn("visual comparison", text)


if __name__ == "__main__":
    unittest.main()
