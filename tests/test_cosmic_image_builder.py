import json
import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/build-cosmic-image"
VERSIONS = ROOT / "sdk/versions.env"
MANIFEST = ROOT / "product/desktop/cosmic-image-v1.json"


class CosmicImageBuilderTests(unittest.TestCase):
    def test_plan_is_pinned_and_never_mutates_device(self):
        result = subprocess.run(
            [str(BUILDER), "plan"], check=False, capture_output=True, text=True
        )
        plan = json.loads(result.stdout)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertRegex(plan["base_image"], r"@sha256:[0-9a-f]{64}$")
        self.assertRegex(plan["arch_snapshot"], r"^20\d\d/\d\d/\d\d$")
        self.assertFalse(plan["device_mutation"])
        self.assertTrue(plan["output"].endswith(plan["contract"]))

    def test_build_requires_explicit_apply(self):
        result = subprocess.run(
            [str(BUILDER), "build"], check=False, capture_output=True, text=True
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("dry run", result.stderr)

    def test_contract_contains_guest_runtime_dependencies(self):
        packages = json.loads(MANIFEST.read_text())["required_packages"]
        self.assertIn("util-linux", packages)
        self.assertIn("vulkan-radeon", packages)
        self.assertNotIn("cmst", packages)

    def test_versions_use_no_moving_cosmic_image_tag(self):
        versions = VERSIONS.read_text()
        self.assertRegex(versions, r"(?m)^COSMIC_ARCH_IMAGE=.*@sha256:[0-9a-f]{64}$")
        self.assertRegex(versions, r"(?m)^COSMIC_ARCH_SNAPSHOT=20\d\d/\d\d/\d\d$")

    def test_builder_has_no_device_deployment_path(self):
        text = BUILDER.read_text()
        self.assertNotIn("/userdata", text)
        self.assertNotRegex(text, r"\b(?:ssh|scp|rsync)\b")
        for pseudo_filesystem in ("dev", "proc", "run", "sys"):
            self.assertIn(f"--exclude='./{pseudo_filesystem}'", text)
        self.assertIn("TZ=UTC date", text)
        self.assertIn("sha256sum rootfs.tar.zst", text)


if __name__ == "__main__":
    unittest.main()
