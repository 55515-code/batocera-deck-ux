import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads(
    (ROOT / "profiles/trusted-vault-v1.json").read_text(encoding="utf-8")
)


class TrustedVaultPolicyTests(unittest.TestCase):
    def test_trust_is_explicit_and_non_transitive(self):
        trust = POLICY["trust"]
        self.assertTrue(trust["mutual_device_approval"])
        self.assertFalse(trust["transitive_trust"])
        self.assertFalse(trust["introducer_default"])
        self.assertTrue(trust["single_use_invites"])
        self.assertTrue(trust["rights_confirmation_required"])
        self.assertFalse(trust["revocation_erases_recipient_copies"])

    def test_no_public_discovery_surface(self):
        discovery = POLICY["discovery"]
        self.assertFalse(discovery["global_catalog"])
        self.assertFalse(discovery["public_search"])
        self.assertFalse(discovery["stranger_matching"])
        self.assertFalse(discovery["global_discovery_default"])
        self.assertFalse(discovery["public_relays_default"])

    def test_private_and_public_networks_are_isolated(self):
        isolation = POLICY["isolation"]
        self.assertTrue(isolation["separate_from_public_update_service"])
        self.assertTrue(isolation["explicit_source_roots_only"])
        self.assertIn("/userdata/system/private-bundles", isolation["deny_roots"])
        self.assertIn("/userdata/bios", isolation["deny_roots"])

    def test_experimental_features_are_not_stable_defaults(self):
        backends = POLICY["backends"]
        self.assertEqual(backends["trusted_sync"], "syncthing")
        self.assertEqual(backends["storage_only_backup"], "restic")
        self.assertEqual(backends["syncthing_untrusted_mode"], "experimental")
        self.assertEqual(backends["i2p_sam_transport"], "experimental")
        self.assertFalse(POLICY["privacy"]["claim_anonymity"])
        self.assertFalse(POLICY["privacy"]["clearnet_fallback_from_i2p"])


if __name__ == "__main__":
    unittest.main()
