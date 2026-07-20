import hashlib
import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOADER = importlib.machinery.SourceFileLoader(
    "qualify_source", str(ROOT / "tools/qualify-source")
)
SPEC = importlib.util.spec_from_loader("qualify_source", LOADER)
QUALIFY = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(QUALIFY)


class SourceQualificationTests(unittest.TestCase):
    def test_source_contract_uses_only_immutable_dependency_pins(self):
        inspection = QUALIFY.inspect_source()
        self.assertEqual([], inspection["errors"])
        self.assertTrue(inspection["ok"])
        self.assertIn("batocera-deck-desktop-host", inspection["buildroot_packages"])
        self.assertRegex(inspection["dependency_pins"]["BATOCERA_COMMIT"], r"^[0-9a-f]{40}$")
        for key in ("BATOCERA_BUILD_IMAGE", "COSMIC_ARCH_IMAGE"):
            self.assertRegex(inspection["dependency_pins"][key], r"@sha256:[0-9a-f]{64}$")

    def test_source_evidence_cannot_claim_image_beta_or_hardware_qualification(self):
        claims = QUALIFY.inspect_source()["claims"]
        self.assertFalse(claims["end_user_os_image_built"])
        self.assertFalse(claims["beta_qualified"])
        self.assertFalse(claims["hardware_qualified"])

    def test_bundle_verification_detects_gate_log_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory)
            log = bundle / "ci-check.log"
            log.write_text("all checks passed\n", encoding="utf-8")
            identity = QUALIFY.source_identity(ROOT)
            report = {
                "schema_version": 1,
                "artifact_kind": "source-qualification",
                "status": "pass",
                "source": identity,
                "inspection": QUALIFY.inspect_source(),
                "gate": {
                    "exit_code": 0,
                    "log": log.name,
                    "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
                },
            }
            (bundle / "report.json").write_text(json.dumps(report), encoding="utf-8")
            self.assertEqual([], QUALIFY.verify_bundle(bundle, require_current_source=False))
            log.write_text("changed\n", encoding="utf-8")
            self.assertIn(
                "gate log digest mismatch",
                QUALIFY.verify_bundle(bundle, require_current_source=False),
            )


if __name__ == "__main__":
    unittest.main()
