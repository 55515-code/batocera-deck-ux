import hashlib
import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
AUDIT = ROOT / "tools/graphics-audit"
BASE_POLICY = json.loads((ROOT / "branding/graphics-policy-v1.json").read_text())


class GraphicsAuditTests(unittest.TestCase):
    def fixture(self, directory, asset_text="<svg xmlns='http://www.w3.org/2000/svg'/>", record=None):
        assets = directory / "assets"
        assets.mkdir()
        asset = assets / "icon.svg"
        asset.write_text(asset_text)
        if record:
            for value in record.values():
                value["sha256"] = hashlib.sha256(asset.read_bytes()).hexdigest()
        policy = directory / "policy.json"
        provenance = directory / "provenance.json"
        replacements = directory / "replacements.json"
        policy.write_text(json.dumps(BASE_POLICY))
        provenance.write_text(json.dumps({"schema_version": 1, "assets": record or {}}))
        replacements.write_text(json.dumps({"schema_version": 1, "replacements": []}))
        return assets, asset, policy, provenance, replacements

    def run_audit(self, policy, provenance, replacements, *arguments):
        return subprocess.run(
            [str(AUDIT), "--policy", str(policy), "--provenance", str(provenance),
             "--replacements", str(replacements), *arguments],
            check=False, capture_output=True, text=True,
        )

    @staticmethod
    def approved_record(**updates):
        record = {
            "creator": "LuigiOS contributors",
            "source": "original",
            "sha256": "set-by-fixture",
            "spdx_license": "CC-BY-SA-4.0",
            "copyright": "2026 LuigiOS contributors",
            "classification": "luigios-original",
            "trademark_review": "not-applicable",
            "derivative_of": None,
        }
        record.update(updates)
        return record

    def test_undeclared_source_asset_fails_strict_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            assets, _, policy, provenance, replacements = self.fixture(root)
            result = self.run_audit(policy, provenance, replacements, "verify-source", "--root", str(assets))
            self.assertEqual(1, result.returncode)
            self.assertIn("missing provenance", result.stdout)

    def test_declared_original_asset_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            assets, _, policy, provenance, replacements = self.fixture(
                root, record={"icon.svg": self.approved_record()}
            )
            result = self.run_audit(policy, provenance, replacements, "verify-source", "--root", str(assets))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_reserved_term_requires_explicit_review(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            assets, _, policy, provenance, replacements = self.fixture(
                root,
                "<svg xmlns='http://www.w3.org/2000/svg'><title>Nintendo system</title></svg>",
                {"icon.svg": self.approved_record()},
            )
            result = self.run_audit(policy, provenance, replacements, "verify-source", "--root", str(assets))
            self.assertEqual(1, result.returncode)
            self.assertIn("reserved terms require explicit trademark review", result.stdout)

    def test_exact_hash_denylist_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            assets, asset, policy, provenance, replacements = self.fixture(
                root, record={"icon.svg": self.approved_record()}
            )
            data = json.loads(policy.read_text())
            data["exact_hash_denylist"] = [hashlib.sha256(asset.read_bytes()).hexdigest()]
            policy.write_text(json.dumps(data))
            result = self.run_audit(policy, provenance, replacements, "verify-source", "--root", str(assets))
            self.assertEqual(1, result.returncode)
            self.assertIn("exact hash is denied", result.stdout)

    def test_svg_external_reference_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            assets, _, policy, provenance, replacements = self.fixture(
                root,
                "<svg xmlns='http://www.w3.org/2000/svg'><image href='https://example.test/a.png'/></svg>",
                {"icon.svg": self.approved_record()},
            )
            result = self.run_audit(policy, provenance, replacements, "verify-source", "--root", str(assets))
            self.assertEqual(1, result.returncode)
            self.assertIn("external or embedded references", result.stdout)

    def test_replacement_requires_both_exact_hashes_and_is_atomic(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "branding") as source_temp, tempfile.TemporaryDirectory() as image_temp:
            source_dir = pathlib.Path(source_temp)
            source = source_dir / "replacement.svg"
            source.write_text("<svg xmlns='http://www.w3.org/2000/svg'><path/></svg>")
            source_key = source.relative_to(ROOT / "branding").as_posix()
            image = pathlib.Path(image_temp)
            target = image / "usr/share/pixmaps/vendor.svg"
            target.parent.mkdir(parents=True)
            target.write_text("upstream")
            policy = source_dir / "policy.json"
            provenance = source_dir / "provenance.json"
            replacements = source_dir / "replacements.json"
            policy.write_text(json.dumps(BASE_POLICY))
            provenance.write_text(json.dumps({"schema_version": 1, "assets": {
                source_key: self.approved_record(
                    sha256=hashlib.sha256(source.read_bytes()).hexdigest()
                )
            }}))
            rule = {
                "id": "vendor-generic",
                "destination": "/usr/share/pixmaps/vendor.svg",
                "expected_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "source": source_key,
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "semantic_icon": "emulator",
                "reason": "distribution-owned presentation",
            }
            replacements.write_text(json.dumps({"schema_version": 1, "replacements": [rule]}))

            dry = self.run_audit(policy, provenance, replacements, "apply-replacements", "--root", str(image))
            self.assertEqual(0, dry.returncode, dry.stdout)
            self.assertEqual("upstream", target.read_text())
            applied = self.run_audit(policy, provenance, replacements, "apply-replacements", "--root", str(image), "--apply")
            self.assertEqual(0, applied.returncode, applied.stdout)
            self.assertEqual(source.read_text(), target.read_text())

            target.write_text("changed upstream")
            refused = self.run_audit(policy, provenance, replacements, "apply-replacements", "--root", str(image), "--apply")
            self.assertEqual(1, refused.returncode)
            self.assertEqual("changed upstream", target.read_text())

    def test_image_scan_visits_configured_roots(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            icon = root / "usr/share/pixmaps/example.png"
            icon.parent.mkdir(parents=True)
            icon.write_bytes(b"not-a-real-png-but-still-an-inventoried-binary")
            policy = root / "policy.json"
            provenance = root / "provenance.json"
            replacements = root / "replacements.json"
            policy.write_text(json.dumps(BASE_POLICY))
            provenance.write_text(json.dumps({"schema_version": 1, "assets": {}}))
            replacements.write_text(json.dumps({"schema_version": 1, "replacements": []}))

            result = self.run_audit(policy, provenance, replacements, "scan-image", "--root", str(root), "--format", "json")
            report = json.loads(result.stdout)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("/usr/share/pixmaps/example.png", report["assets"][0]["path"])
            self.assertEqual("/usr/share/pixmaps/example.png", report["assets"][0]["provenance_key"])
            self.assertIn("missing provenance", report["warnings"][0])

    def test_repository_graphics_have_exact_provenance(self):
        result = subprocess.run(
            [str(AUDIT), "verify-repository", "--format", "json"],
            check=False, capture_output=True, text=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)
        self.assertIn("third_party/bua/icon.png", [item["path"] for item in report["assets"]])

    def test_repository_scan_ignores_declared_sdk_checkout(self):
        result = subprocess.run(
            [str(AUDIT), "verify-repository", "--format", "json"],
            check=False, capture_output=True, text=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse(any(item["path"].startswith(".sdk/") for item in report["assets"]))

    def test_repository_scan_ignores_generated_dist_artifacts(self):
        result = subprocess.run(
            [str(AUDIT), "verify-repository", "--format", "json"],
            check=False, capture_output=True, text=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse(any(item["path"].startswith("dist/") for item in report["assets"]))


if __name__ == "__main__":
    unittest.main()
