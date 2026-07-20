import json
import pathlib
import shutil
import struct
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RENDERER = ROOT / "tools/render-brand-assets"


class PinnedRendererContractTests(unittest.TestCase):
    def test_pinned_renderer_plan_is_immutable_and_read_only(self):
        checker = (ROOT / "tools/check-rendered-brand-assets").read_text()
        gate = (ROOT / "tools/ci-check").read_text()
        versions = (ROOT / "sdk/versions.env").read_text()
        self.assertRegex(versions, r"COSMIC_ARCH_IMAGE=.*@sha256:[0-9a-f]{64}")
        self.assertIn("COSMIC_ARCH_SNAPSHOT", checker)
        self.assertIn('$ROOT:/repo:ro', checker)
        self.assertNotIn("--privileged", checker)
        self.assertIn("./tools/check-rendered-brand-assets check", gate)

    def test_splash_fallback_is_the_deterministic_handheld_wallpaper(self):
        wallpaper = ROOT / "branding/assets/desktop/wallpapers/luigios/1280x800.png"
        frame = ROOT / "branding/assets/boot/luigios-splash-frame.png"
        provenance = json.loads((ROOT / "branding/PROVENANCE.json").read_text())
        self.assertEqual(wallpaper.read_bytes(), frame.read_bytes())
        self.assertIn("assets/boot/luigios-splash-frame.png", provenance["assets"])


@unittest.skipUnless(shutil.which("magick"), "ImageMagick is unavailable")
class BrandAssetRendererTests(unittest.TestCase):

    def test_wallpaper_dimensions_match_handheld_and_tv_contracts(self):
        expected = {
            "1280x800.png": (1280, 800),
            "1920x1080.png": (1920, 1080),
        }
        directory = ROOT / "branding/assets/desktop/wallpapers/luigios"
        for name, dimensions in expected.items():
            header = (directory / name).read_bytes()[:24]
            self.assertEqual(b"\x89PNG\r\n\x1a\n", header[:8])
            self.assertEqual(dimensions, struct.unpack(">II", header[16:24]))

    def test_dominant_surface_is_oled_black_with_elevated_charcoal(self):
        tokens = json.loads((ROOT / "branding/design-tokens-v1.json").read_text())
        self.assertEqual("#000000", tokens["colors"]["surface_950"])
        self.assertNotEqual("#000000", tokens["colors"]["surface_900"])

    def test_full_canvas_assets_have_true_black_background_pixels(self):
        assets = [
            ROOT / "branding/assets/boot/boot-logo-1280x800.png",
            ROOT / "branding/assets/desktop/wallpapers/luigios/1280x800.png",
            ROOT / "branding/assets/desktop/wallpapers/luigios/1920x1080.png",
        ]
        for asset in assets:
            result = subprocess.run(
                ["magick", str(asset), "-format", "%[pixel:p{0,0}]", "info:"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertRegex(result.stdout, r"^s?rgba?\(0,0,0(?:,1)?\)$")

    def test_game_mode_theme_and_splash_match_batocera_contract(self):
        theme = ROOT / "branding/assets/game-mode/theme/theme.xml"
        parsed = subprocess.run(
            ["xmllint", "--noout", str(theme)], capture_output=True, text=True
        )
        self.assertEqual(0, parsed.returncode, parsed.stderr)
        text = theme.read_text()
        self.assertIn("<formatVersion>7</formatVersion>", text)
        self.assertIn('view name="system"', text)
        self.assertIn('view name="menu"', text)

        splash = ROOT / "branding/assets/boot/luigios-splash.mp4"
        result = subprocess.run(
            [
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=codec_name,width,height,pix_fmt",
                "-of", "json", str(splash),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        stream = json.loads(result.stdout)["streams"][0]
        self.assertEqual("mpeg4", stream["codec_name"])
        self.assertEqual((1280, 800), (stream["width"], stream["height"]))
        self.assertEqual("yuv420p", stream["pix_fmt"])


if __name__ == "__main__":
    unittest.main()
