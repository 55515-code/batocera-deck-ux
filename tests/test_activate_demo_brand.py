import importlib.machinery
import importlib.util
import os
import tempfile
import stat
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader(
    "activate_demo_brand", str(ROOT / "tools/activate-demo-brand")
)
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)


class ActivateDemoBrandTests(unittest.TestCase):
    def test_watchdog_requires_confirmation_before_skipping_rollback(self):
        watchdog = (ROOT / "tools/brand-activation-watchdog").read_text()
        self.assertIn('test -f "$backup/confirmed" && exit 0', watchdog)
        self.assertIn('rollback --backup "$backup"', watchdog)
        self.assertIn("batocera-es-swissknife --restart", watchdog)

        theme_watchdog = (ROOT / "tools/brand-theme-watchdog").read_text()
        self.assertIn('test -f "$backup/confirmed" && exit 0', theme_watchdog)
        self.assertIn('mv "$backup/theme" "$target"', theme_watchdog)
        self.assertNotIn("rm ", theme_watchdog)

    def fixture(self, directory):
        root = Path(directory)
        es = root / module.ES_SETTINGS.lstrip("/")
        theme = root / module.ES_THEME.lstrip("/")
        home = root / module.DESKTOP_HOME.lstrip("/")
        plasma = home / module.PLASMA_CONFIG
        wallpaper = home / module.WALLPAPER
        for path in (es, theme, plasma, wallpaper):
            path.parent.mkdir(parents=True, exist_ok=True)
        es.write_text('<config><string name="ThemeSet" value="old" /></config>')
        theme.write_text("<theme><formatVersion>7</formatVersion></theme>")
        plasma.write_text("[Containments][1]\nwallpaperplugin=org.kde.image\n")
        plasma.chmod(0o640)
        wallpaper.write_bytes(b"png")
        return root, es, plasma

    def test_theme_and_wallpaper_updates_are_deterministic(self):
        es = module.es_with_theme(
            b'<config><string name="ThemeSet" value="old" /></config>', "luigios"
        )
        self.assertIn(b'value="luigios"', es)
        plasma = module.kconfig_with_wallpaper("[Containments][1]\n", "/home/deck/w.png")
        self.assertIn("Image=file:///home/deck/w.png", plasma)
        self.assertEqual(1, plasma.count(module.WALLPAPER_SECTION))
        self.assertEqual(plasma, module.kconfig_with_wallpaper(plasma, "/home/deck/w.png"))

    def test_apply_requires_explicit_flag_and_rollback_restores_both_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root, es, plasma = self.fixture(directory)
            args = type("Args", (), {"root": root, "desktop_home": module.DESKTOP_HOME, "theme": "luigios", "apply": False})
            self.assertEqual(0, module.apply(args))
            self.assertIn('value="old"', es.read_text())
            args.apply = True
            self.assertEqual(0, module.apply(args))
            self.assertIn('value="luigios"', es.read_text())
            self.assertEqual(0o640, stat.S_IMODE(plasma.stat().st_mode))
            self.assertEqual(os.getuid(), plasma.stat().st_uid)
            backup = next((root / "userdata/system/backups").iterdir())
            restore = type("Args", (), {"root": root, "backup": backup})
            self.assertEqual(0, module.rollback(restore))
            self.assertIn('value="old"', es.read_text())
            self.assertNotIn("Image=", plasma.read_text())
            self.assertEqual(0o640, stat.S_IMODE(plasma.stat().st_mode))


if __name__ == "__main__":
    unittest.main()
