import json
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "profiles" / "distribution-v1.json"


def is_within(path, parent):
    path = PurePosixPath(path)
    parent = PurePosixPath(parent)
    return path == parent or parent in path.parents


class DistributionPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))

    def test_transport_cannot_authorize_installation(self):
        auth = self.policy["authorization"]
        self.assertEqual(auth["authority"], "tuf")
        self.assertFalse(auth["allow_transport_to_authorize"])
        self.assertIn("sha256", auth["hash_algorithms"])

    def test_seeder_is_confined_to_dedicated_cache(self):
        seeding = self.policy["seeding"]
        cache_root = seeding["cache_root"]
        self.assertTrue(seeding["allow_roots"])
        for allowed in seeding["allow_roots"]:
            self.assertTrue(is_within(allowed, cache_root))
        for denied in seeding["deny_roots"]:
            self.assertFalse(is_within(cache_root, denied))
            self.assertFalse(is_within(denied, cache_root))

    def test_release_safety_defaults(self):
        transport = self.policy["transport"]
        self.assertEqual(transport["p2p_default"], "off")
        self.assertFalse(transport["seed_on_battery"])
        self.assertFalse(transport["seed_on_metered_network"])
        install = self.policy["installation"]
        self.assertEqual(install["strategy"], "inactive-ab-slot")
        self.assertTrue(install["verify_final_artifact_before_stage"])
        self.assertTrue(install["require_health_commit"])
        self.assertTrue(install["automatic_fallback"])

    def test_upstream_swarms_are_federated_without_impersonation(self):
        federation = self.policy["upstream_federation"]
        self.assertTrue(federation["preserve_upstream_swarm_for_identical_artifacts"])
        self.assertFalse(federation["repackage_unchanged_upstream_artifacts"])
        self.assertTrue(federation["cross_seed_only_on_complete_content_match"])
        self.assertTrue(federation["preserve_recognized_vanilla_torrent_state"])
        self.assertTrue(federation["share_objects_by_digest_across_catalogs"])
        self.assertTrue(federation["require_upstream_provenance"])
        self.assertTrue(federation["respect_upstream_revocation_and_opt_out"])


if __name__ == "__main__":
    unittest.main()
