import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "profiles/hardware-support-v1.json").read_text())


class HardwareSupportPolicyTests(unittest.TestCase):
    def test_steam_deck_is_reference_without_blanket_family_claim(self):
        reference = POLICY["reference_platform"]
        self.assertEqual("steam-deck", reference["id"])
        self.assertTrue(reference["core_project_release_gate"])
        self.assertTrue(reference["variants_require_independent_evidence"])
        self.assertFalse(reference["blanket_compatibility_claim"])

    def test_only_reference_hardware_is_core_release_blocking(self):
        tiers = POLICY["tiers"]
        self.assertTrue(tiers["reference"]["release_blocking"])
        for name in ("community-tested", "downstream-maintained", "experimental", "unverified"):
            self.assertFalse(tiers[name]["release_blocking"])
            self.assertFalse(tiers[name]["core_project_maintained"])

    def test_third_party_evidence_does_not_imply_core_support(self):
        tiers = POLICY["tiers"]
        self.assertEqual("none", tiers["community-tested"]["support_promise"])
        self.assertEqual("provided-by-downstream", tiers["downstream-maintained"]["support_promise"])
        self.assertEqual("none", tiers["experimental"]["support_promise"])
        self.assertFalse(tiers["unverified"]["compatibility_claim"])

    def test_profiles_fail_closed_and_preserve_reference_device(self):
        acceptance = POLICY["device_profile_acceptance"]
        self.assertTrue(acceptance["must_fail_closed_on_wrong_hardware"])
        self.assertTrue(acceptance["must_not_regress_reference_platform"])
        self.assertTrue(acceptance["core_project_may_merge_without_support_ownership"])
        self.assertFalse(POLICY["evidence"]["one_variant_implies_family_support"])

    def test_hardware_report_discloses_relationship_and_non_support_boundary(self):
        issue_form = (ROOT / ".github/ISSUE_TEMPLATE/hardware-test.yml").read_text()
        self.assertIn("id: relationship", issue_form)
        self.assertIn("Community owner or tester", issue_form)
        self.assertIn("core-project support promise", issue_form)


if __name__ == "__main__":
    unittest.main()
