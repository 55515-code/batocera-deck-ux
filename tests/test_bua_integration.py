import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "third_party" / "bua"


class BuaIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.upstream = json.loads((VENDOR / "UPSTREAM.json").read_text(encoding="utf-8"))

    def test_vendored_files_match_reviewed_hashes(self):
        for name, tagged_digest in self.upstream["files"].items():
            algorithm, expected = tagged_digest.split(":", 1)
            self.assertEqual(algorithm, "sha256")
            actual = hashlib.sha256((VENDOR / name).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, name)

    def test_launcher_uses_bundled_source(self):
        launcher = (
            ROOT / "product/package/batocera-deck-bua/files/bua"
        ).read_text(encoding="utf-8")
        self.assertIn("/usr/share/luigios/bua/bua_installerx86.py", launcher)
        self.assertIn(self.upstream["files"]["bua_installerx86.py"].split(":", 1)[1], launcher)
        self.assertNotIn("curl", launcher)
        self.assertNotIn("refs/heads", launcher)

    def test_store_is_not_started_as_a_service(self):
        package_root = ROOT / "product/package/batocera-deck-bua"
        all_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in package_root.rglob("*")
            if path.is_file()
        )
        self.assertNotIn("custom.sh", all_text)
        self.assertNotIn("batocera-services enable", all_text)


if __name__ == "__main__":
    unittest.main()
