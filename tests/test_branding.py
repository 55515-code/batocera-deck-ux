import json
import pathlib
import struct
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BRANDCTL = ROOT / "tools/brandctl"
MANIFEST = ROOT / "branding/brand-v1.json"


class BrandingTests(unittest.TestCase):
    def run_brandctl(self, *arguments, manifest=MANIFEST):
        return subprocess.run(
            [str(BRANDCTL), "--manifest", str(manifest), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_contract_is_valid_but_not_art_ready(self):
        result = self.run_brandctl("validate", "--format", "json")
        report = json.loads(result.stdout)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(report["valid"])
        self.assertGreater(len(report["missing_required"]), 0)

        ready = self.run_brandctl("validate", "--require-ready")
        self.assertEqual(2, ready.returncode)

    def test_demo_and_image_plans_use_separate_roots(self):
        demo = json.loads(self.run_brandctl("plan", "--scope", "demo", "--format", "json").stdout)
        image = json.loads(self.run_brandctl("plan", "--scope", "image", "--format", "json").stdout)

        self.assertTrue(demo)
        self.assertTrue(image)
        self.assertTrue(all(item["destination"].startswith("/userdata/") for item in demo))
        self.assertTrue(
            all(item["destination"].startswith(("/usr/share/", "/etc/")) for item in image)
        )

    def test_image_assets_cannot_be_deployed_into_a_live_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = self.run_brandctl(
                "deploy",
                "--scope",
                "image",
                "--root",
                temporary,
                "--allow-incomplete",
                "--apply",
            )

            self.assertEqual(1, result.returncode)
            self.assertIn("reproducible image build", result.stderr)

    def test_identity_install_is_explicit_and_atomic(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            dry_run = self.run_brandctl("identity", "--root", str(root))
            self.assertEqual(0, dry_run.returncode)
            self.assertFalse((root / "userdata/system/configs/luigios").exists())

            applied = self.run_brandctl("identity", "--root", str(root), "--apply")
            self.assertEqual(0, applied.returncode, applied.stderr)
            identity = json.loads(
                (root / "userdata/system/configs/luigios/identity.json").read_text()
            )
            self.assertEqual("LuigiOS", identity["name"])
            self.assertEqual("Batocera", identity["upstream"])

    def test_rejects_destination_escape(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = pathlib.Path(temporary)
            manifest = directory / "brand.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "product": {"display_name": "LuigiOS", "id": "luigios"},
                        "slots": [
                            {
                                "id": "bad.asset",
                                "kind": "file",
                                "source": "missing.svg",
                                "required_for_demo": False,
                                "deploy": [
                                    {"scope": "demo", "destination": "/etc/shadow"}
                                ],
                            }
                        ],
                    }
                )
            )
            result = self.run_brandctl("validate", manifest=manifest)
            self.assertEqual(1, result.returncode)
            self.assertIn("outside demo roots", result.stdout)

    def test_rejects_symlinked_assets(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = pathlib.Path(temporary)
            target = directory / "real.svg"
            target.write_text("<svg xmlns='http://www.w3.org/2000/svg'/>")
            (directory / "linked.svg").symlink_to(target)
            manifest = self.fixture_manifest(directory, "linked.svg", "/userdata/test.svg")

            result = self.run_brandctl("validate", manifest=manifest)
            self.assertEqual(1, result.returncode)
            self.assertIn("must not be a symlink", result.stdout)

    def test_png_dimensions_are_enforced(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = pathlib.Path(temporary)
            png = directory / "wallpaper.png"
            png.write_bytes(
                b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + struct.pack(">II", 16, 9)
            )
            manifest = self.fixture_manifest(
                directory,
                "wallpaper.png",
                "/userdata/wallpaper.png",
                constraints={"width": 1280, "height": 800},
            )

            result = self.run_brandctl("validate", manifest=manifest)
            self.assertEqual(1, result.returncode)
            self.assertIn("16x9", result.stdout)

    def test_deploy_backs_up_existing_asset_and_records_identity(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = pathlib.Path(temporary)
            source = directory / "logo.svg"
            source.write_text("<svg xmlns='http://www.w3.org/2000/svg'/>")
            manifest = self.fixture_manifest(directory, "logo.svg", "/userdata/themes/logo.svg")
            root = directory / "target"
            target = root / "userdata/themes/logo.svg"
            target.parent.mkdir(parents=True)
            target.write_text("old")

            result = self.run_brandctl(
                "deploy",
                "--scope",
                "demo",
                "--root",
                str(root),
                "--apply",
                manifest=manifest,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(source.read_text(), target.read_text())
            backups = list((root / "userdata/system/backups").glob("luigios-branding-*"))
            self.assertEqual(1, len(backups))
            self.assertEqual("old", (backups[0] / "userdata/themes/logo.svg").read_text())
            self.assertTrue((backups[0] / "deployment.json").is_file())
            self.assertTrue((root / "userdata/system/configs/luigios/identity.json").is_file())

    @staticmethod
    def fixture_manifest(directory, source, destination, constraints=None):
        manifest = directory / "brand.json"
        slot = {
            "id": "test.asset",
            "kind": "file",
            "source": source,
            "required_for_demo": True,
            "deploy": [{"scope": "demo", "destination": destination}],
        }
        if constraints:
            slot["constraints"] = constraints
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "product": {
                        "display_name": "LuigiOS",
                        "id": "luigios",
                        "variant": "Test",
                    },
                    "slots": [slot],
                }
            )
        )
        return manifest


if __name__ == "__main__":
    unittest.main()
