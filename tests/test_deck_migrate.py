import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).parents[1]
TOOL = ROOT / "tools/deck_migrate.py"


def run(*args):
    return subprocess.run(
        [sys.executable, TOOL, *map(str, args)], capture_output=True, text=True
    )


class DeckMigrateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.bios = self.source / "userdata/bios"
        self.bios.mkdir(parents=True)
        self.profile = self.root / "profile.json"
        self.profile.write_text(json.dumps({
            "schema": 1,
            "name": "test-private",
            "components": [{"category": "firmware", "path": "/userdata/bios"}],
        }))

    def tearDown(self):
        self.temporary.cleanup()

    def export(self, contents=b"owned-firmware"):
        (self.bios / "owned.bin").write_bytes(contents)
        bundle = self.root / "bundle"
        result = run(
            "export", "--profile", self.profile, "--output", bundle,
            "--source-root", self.source,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return bundle

    def test_export_verify_import_and_backup(self):
        bundle = self.export()
        self.assertEqual(run("verify", bundle).returncode, 0)

        target = self.root / "target"
        existing = target / "userdata/bios/owned.bin"
        existing.parent.mkdir(parents=True)
        existing.write_bytes(b"old")
        preview = run("import", bundle, "--target-root", target, "--dry-run")
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(existing.read_bytes(), b"old")
        applied = run("import", bundle, "--target-root", target, "--apply")
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertEqual(existing.read_bytes(), b"owned-firmware")
        backups = list((target / "userdata/system/config-backups").glob(
            "deck-migrate-*/userdata/bios/owned.bin"
        ))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), b"old")

    def test_checksum_failure_blocks_import(self):
        bundle = self.export(b"good")
        (bundle / "payload/userdata/bios/owned.bin").write_bytes(b"tampered")
        self.assertEqual(run("verify", bundle).returncode, 1)
        result = run(
            "import", bundle, "--target-root", self.root / "target", "--apply"
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
