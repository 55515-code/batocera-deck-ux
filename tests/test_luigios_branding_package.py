import json
import os
import pathlib
import struct
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "product/package/batocera-luigios-branding"
SETUP = ROOT / "product/package/batocera-deck-desktop-host/files/cosmic-brand-setup"


class LuigiOSBrandingPackageTests(unittest.TestCase):
    def test_buildroot_package_is_wired_and_installs_reviewed_contract(self):
        config = (ROOT / "Config.in").read_text()
        makefile = (PACKAGE / "batocera-luigios-branding.mk").read_text()
        self.assertIn("batocera-luigios-branding/Config.in", config)
        self.assertIn("CC-BY-SA-4.0", makefile)
        for name in ("assets", "brand-v1.json", "design-tokens-v1.json", "PROVENANCE.json"):
            self.assertIn(name, makefile)
        self.assertNotRegex(makefile, r"(?i)\b(curl|wget)\b")

    def test_cosmic_brand_setup_is_idempotent_and_preserves_user_choice(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            rootfs = root / "rootfs"
            home = root / "home"
            wallpaper = rootfs / "usr/share/luigios/branding/assets/desktop/wallpapers/luigios/1280x800.png"
            wallpaper.parent.mkdir(parents=True)
            wallpaper.write_bytes(b"reviewed-wallpaper")
            environment = {
                **os.environ,
                "LUIGIOS_COSMIC_HOME": str(home),
                "LUIGIOS_COSMIC_ROOTFS": str(rootfs),
            }
            first = subprocess.run([str(SETUP)], env=environment, check=False, capture_output=True, text=True)
            self.assertEqual(0, first.returncode, first.stderr)
            config = home / ".config/cosmic/com.system76.CosmicBackground/v1/all"
            self.assertIn("/usr/share/luigios/branding/", config.read_text())

            config.write_text("user-selected-wallpaper\n")
            second = subprocess.run([str(SETUP)], env=environment, check=False, capture_output=True, text=True)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertEqual("user-selected-wallpaper\n", config.read_text())

    def test_cosmic_brand_setup_fails_without_packaged_wallpaper(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            result = subprocess.run(
                [str(SETUP)],
                env={**os.environ, "LUIGIOS_COSMIC_HOME": str(root / "home"),
                     "LUIGIOS_COSMIC_ROOTFS": str(root / "rootfs")},
                check=False, capture_output=True, text=True,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("not mounted", result.stderr)

    def test_mascot_variants_are_packaged_rgba_assets_with_distinct_semantics(self):
        manifest = json.loads((ROOT / "branding/brand-v1.json").read_text())
        slots = {slot["id"]: slot for slot in manifest["slots"]}
        self.assertIn("recommended", slots["mascot.angel"]["surfaces"])
        self.assertIn("destructive", slots["mascot.demon"]["surfaces"])

        for name in ("caretaker-angel.png", "caretaker-demon.png"):
            header = (ROOT / "branding/assets/mascot" / name).read_bytes()[:26]
            self.assertEqual(b"\x89PNG\r\n\x1a\n", header[:8])
            self.assertEqual((1024, 1024), struct.unpack(">II", header[16:24]))
            self.assertEqual(6, header[25], "mascot asset must use RGBA PNG color type")


if __name__ == "__main__":
    unittest.main()
