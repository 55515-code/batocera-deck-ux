import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IDENTITY = json.loads((ROOT / "profiles/product-identity-v1.json").read_text())


class ProductIdentityTests(unittest.TestCase):
    def test_public_name_and_player_first_mission_are_stable(self):
        self.assertEqual("LuigiOS", IDENTITY["product"]["display_name"])
        self.assertEqual("Games first. Your device. Your choices.", IDENTITY["product"]["tagline"])
        self.assertTrue(IDENTITY["mission"]["player_controls_device"])
        self.assertFalse(IDENTITY["mission"]["company_controls_device"])

    def test_default_experience_has_no_project_lock_in_or_ads(self):
        defaults = IDENTITY["default_experience"]
        self.assertTrue(defaults["works_offline"])
        for key in (
            "mandatory_luigios_account",
            "mandatory_subscription",
            "advertising",
            "sponsored_ranking",
            "forced_storefront",
            "telemetry_enabled_by_default",
            "terminal_required",
        ):
            self.assertFalse(defaults[key], key)

    def test_vanilla_distribution_is_deployable_and_usable_offline(self):
        vanilla = IDENTITY["vanilla_distribution"]
        self.assertFalse(vanilla["deployment_requires_network"])
        self.assertTrue(vanilla["first_boot_network_optional"])
        self.assertFalse(vanilla["first_boot_requires_login"])
        self.assertFalse(vanilla["local_library_and_play_require_login"])
        self.assertFalse(vanilla["local_device_administration_requires_network"])
        self.assertFalse(vanilla["backup_restore_reset_and_recovery_require_login"])

    def test_owner_can_export_recover_customize_and_opt_out(self):
        rights = IDENTITY["owner_rights"]
        for key in (
            "choose_software_sources",
            "remove_optional_software",
            "export_user_data",
            "backup_restore_and_reset",
            "inspect_installed_components",
            "enable_developer_mode",
            "decline_peer_distribution",
            "decline_diagnostics_upload",
        ):
            self.assertTrue(rights[key], key)

    def test_commercial_relationships_cannot_bypass_trust(self):
        trust = IDENTITY["trust_boundaries"]
        self.assertTrue(trust["commercial_relationships_never_bypass_qa"])
        self.assertTrue(trust["commercial_relationships_never_bypass_release_trust"])
        self.assertTrue(trust["security_updates_remain_signed"])
        self.assertTrue(trust["third_party_services_remain_identified"])
        self.assertTrue(trust["proprietary_downstream_services_may_require_own_login"])
        self.assertTrue(trust["third_party_login_requirement_scoped_to_service"])
        self.assertTrue(trust["third_party_service_cannot_gate_vanilla_shell"])

    def test_brand_and_experience_contracts_use_the_same_identity(self):
        brand = json.loads((ROOT / "branding/brand-v1.json").read_text())
        experience = json.loads((ROOT / "profiles/experience-modes-v1.json").read_text())
        self.assertEqual("LuigiOS", brand["product"]["display_name"])
        self.assertEqual(IDENTITY["product"]["tagline"], brand["principles"]["tagline"])
        self.assertEqual("product-identity-v1.json", experience["product_identity_policy"])

    def test_primary_public_docs_use_canonical_name_and_player_promise(self):
        for path in (
            ROOT / "README.md",
            ROOT / "docs/PRODUCT_PRINCIPLES.md",
            ROOT / "community/README.md",
        ):
            text = path.read_text()
            self.assertIn("LuigiOS", text, path)
            self.assertIn("Games first. Your device. Your choices.", text, path)
            self.assertNotIn("Luigi OS", text, path)

        voice = (ROOT / "docs/IDENTITY_AND_VOICE.md").read_text()
        self.assertIn("Games first. Your device. Your choices.", voice)
        self.assertIn("Write the product name exactly as **LuigiOS**", voice)
        for forbidden in ("Luigi OS", "Lugios", "LuigiOs"):
            self.assertIn(f"`{forbidden}`", voice)

    def test_candidate_and_release_gates_enforce_identity(self):
        testing = (ROOT / "docs/TESTING.md").read_text()
        releasing = (ROOT / "docs/RELEASING.md").read_text()
        self.assertIn("profiles/product-identity-v1.json", testing)
        self.assertIn("without a LuigiOS account", testing)
        self.assertIn("no paid or sponsored placement", testing)
        self.assertIn("profiles/product-identity-v1.json", releasing)
        self.assertIn("cannot override test evidence or release authority", releasing)


if __name__ == "__main__":
    unittest.main()
