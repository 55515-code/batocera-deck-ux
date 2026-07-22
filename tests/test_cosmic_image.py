import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/cosmic-image"
MANIFEST = ROOT / "product/desktop/cosmic-image-v1.json"


class CosmicImageTests(unittest.TestCase):
    def run_tool(self, *arguments):
        return subprocess.run(
            [str(TOOL), *arguments], check=False, capture_output=True, text=True
        )

    def test_contract_is_valid(self):
        result = self.run_tool("validate")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("COSMIC image: PASS", result.stdout)

    def test_missing_rootfs_fails_closed(self):
        result = self.run_tool(
            "preflight", "--root", "/definitely/missing/luigios-cosmic", "--format", "json"
        )
        report = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        self.assertFalse(report["valid"])
        self.assertIn("rootfs is missing or unsafe", report["errors"][0])

    def test_complete_fixture_passes_with_attestations(self):
        manifest = json.loads(MANIFEST.read_text())
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            for executable in manifest["required_executables"]:
                path = root / executable.lstrip("/")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("#!/bin/sh\n")
                path.chmod(0o755)
            database = root / "var/lib/pacman/local"
            for package in manifest["required_packages"]:
                desc = database / f"{package}-1.3.0-1/desc"
                desc.parent.mkdir(parents=True, exist_ok=True)
                desc.write_text(f"%NAME%\n{package}\n\n%VERSION%\n1.3.0-1\n")
            passwd = root / "etc/passwd"
            passwd.parent.mkdir(parents=True, exist_ok=True)
            passwd.write_text("deck:x:1000:1000:LuigiOS Desktop:/home/deck:/bin/bash\n")
            for path in manifest["attestation"].values():
                target = root / path.lstrip("/")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}\n")

            result = self.run_tool("preflight", "--root", str(root), "--format", "json")
            report = json.loads(result.stdout)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue(report["valid"])
            self.assertFalse(report["errors"])

    def test_package_lookup_does_not_accept_prefix_collision(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            desc = root / "var/lib/pacman/local/cosmic-settings-daemon-1.3.0-1/desc"
            desc.parent.mkdir(parents=True)
            desc.write_text("%NAME%\ncosmic-settings-daemon\n\n%VERSION%\n1.3.0-1\n")
            manifest = json.loads(MANIFEST.read_text())
            manifest["required_packages"] = ["cosmic-settings"]
            manifest["required_executables"] = ["/usr/bin/cosmic-settings"]
            custom = root / "contract.json"
            custom.write_text(json.dumps(manifest))
            executable = root / "usr/bin/cosmic-settings"
            executable.parent.mkdir(parents=True)
            executable.write_text("#!/bin/sh\n")
            executable.chmod(0o755)
            passwd = root / "etc/passwd"
            passwd.parent.mkdir(parents=True)
            passwd.write_text("deck:x:1000:1000::/home/deck:/bin/bash\n")

            result = subprocess.run(
                [str(TOOL), "--manifest", str(custom), "preflight", "--root", str(root),
                 "--allow-unattested", "--format", "json"],
                check=False, capture_output=True, text=True,
            )
            report = json.loads(result.stdout)
            self.assertEqual(1, result.returncode)
            self.assertIn("required Arch package is absent: cosmic-settings", report["errors"])


if __name__ == "__main__":
    unittest.main()
