import importlib.machinery
import importlib.util
import json
import tarfile
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOADER = importlib.machinery.SourceFileLoader(
    "release_source", str(ROOT / "tools/release-source")
)
SPEC = importlib.util.spec_from_loader("release_source", LOADER)
RELEASE = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(RELEASE)


class SourceReleaseTests(unittest.TestCase):
    def test_release_is_reproducible_and_identifies_source_only(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            archive_a, _, manifest_a = RELEASE.build_release(
                Path(first), require_clean=False
            )
            archive_b, _, _ = RELEASE.build_release(Path(second), require_clean=False)
            self.assertEqual(archive_a.read_bytes(), archive_b.read_bytes())
            manifest = json.loads(manifest_a.read_text(encoding="utf-8"))
            self.assertEqual(manifest["artifact_kind"], "contributor-source")
            self.assertFalse(manifest["end_user_os_image"])
            with tarfile.open(archive_a, "r:gz") as bundle:
                names = bundle.getnames()
            prefix = f"luigios-{manifest['version']}"
            self.assertIn(f"{prefix}/LICENSE", names)
            self.assertIn(f"{prefix}/sdk/README.md", names)
            self.assertFalse(any("private-bundles" in name for name in names))


if __name__ == "__main__":
    unittest.main()
