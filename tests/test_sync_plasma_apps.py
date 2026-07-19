import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "prototype/desktop/sync-plasma-apps.py"
SPEC = importlib.util.spec_from_file_location("sync_plasma_apps", SCRIPT)
SYNC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SYNC
SPEC.loader.exec_module(SYNC)


def entry(name, command, **values):
    fields = {"Type": "Application", "Name": name, "Exec": command, **values}
    body = "\n".join(f"{key}={value}" for key, value in fields.items())
    return f"[Desktop Entry]\n{body}\n"


class PlasmaApplicationSyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = pathlib.Path(self.temporary.name)
        self.rootfs = self.base / "rootfs"
        self.home = self.base / "home/deck"
        self.system = self.rootfs / "usr/share/applications"
        self.local = self.rootfs / "usr/local/share/applications"
        self.flatpak = self.home / ".local/share/flatpak/exports/share/applications"
        self.batocera = self.rootfs / "mnt/batocera/desktop-shortcuts"
        for directory in (self.system, self.local, self.flatpak, self.batocera):
            directory.mkdir(parents=True)

    def tearDown(self):
        self.temporary.cleanup()

    @property
    def generated(self):
        return self.home / ".local/share/applications"

    @property
    def manifest_path(self):
        return self.generated / "batocera-deck-generated/manifest.json"

    def write(self, directory, desktop_id, content):
        path = directory / desktop_id
        path.write_text(content, encoding="utf-8")
        return path

    def run_sync(self, approved=()):
        return SYNC.synchronize(
            rootfs=self.rootfs,
            home=self.home,
            system_dirs=[pathlib.Path("usr/share/applications"), pathlib.Path("usr/local/share/applications")],
            flatpak_dir=self.flatpak,
            batocera_dir=self.batocera,
            approved_batocera=set(approved),
            uid=os.getuid(),
            gid=os.getgid(),
        )

    def test_syncs_sources_with_deterministic_precedence(self):
        self.write(self.system, "shared.desktop", entry("System", "/usr/bin/system-tool"))
        self.write(self.local, "shared.desktop", entry("Local", "/usr/bin/local-tool"))
        self.write(
            self.flatpak,
            "shared.desktop",
            entry("Flatpak", "/usr/bin/flatpak run org.example.App"),
        )
        self.write(self.batocera, "shared.desktop", entry("Batocera", "/usr/bin/batocera-tool"))

        manifest = self.run_sync(approved={"shared.desktop"})

        self.assertIn("Name=Batocera", (self.generated / "shared.desktop").read_text())
        self.assertEqual(manifest["shared.desktop"]["source"], "batocera")

    def test_is_idempotent_and_uses_atomic_writes(self):
        self.write(self.system, "tool.desktop", entry("Tool", "/usr/bin/tool"))
        self.run_sync()
        target = self.generated / "tool.desktop"
        first_stat = target.stat()

        self.run_sync()

        self.assertEqual(first_stat.st_ino, target.stat().st_ino)
        self.assertEqual([], list(self.generated.glob(".*.desktop.*")))
        manifest = json.loads(self.manifest_path.read_text())
        self.assertEqual(1, manifest["version"])

    def test_removes_only_unmodified_stale_generated_entries(self):
        source = self.write(self.system, "old.desktop", entry("Old", "/usr/bin/old"))
        self.run_sync()
        source.unlink()

        self.run_sync()

        self.assertFalse((self.generated / "old.desktop").exists())

    def test_preserves_user_owned_and_user_modified_entries(self):
        user_entry = self.generated / "personal.desktop"
        user_entry.parent.mkdir(parents=True)
        user_entry.write_text(entry("Personal", "/usr/bin/personal"))
        source = self.write(self.system, "tool.desktop", entry("Tool", "/usr/bin/tool"))
        self.run_sync()
        target = self.generated / "tool.desktop"
        target.write_text(entry("My Tool", "/usr/bin/my-tool"))
        source.unlink()

        manifest = self.run_sync()

        self.assertTrue(user_entry.exists())
        self.assertIn("Name=My Tool", target.read_text())
        self.assertNotIn("tool.desktop", manifest)

    def test_rejects_malformed_hidden_and_unsafe_entries(self):
        self.write(self.system, "duplicate.desktop", "[Desktop Entry]\nName=A\nName=B\nType=Application\nExec=app\n")
        self.write(self.system, "hidden.desktop", entry("Hidden", "app", Hidden="true"))
        self.write(self.system, "shell.desktop", entry("Shell", "/bin/sh -c payload"))
        self.write(self.system, "bad-field.desktop", entry("Bad", "app %Q"))
        symlink = self.system / "linked.desktop"
        symlink.symlink_to(self.write(self.base, "payload.desktop", entry("Link", "app")))

        manifest = self.run_sync()

        self.assertEqual({}, manifest)
        self.assertEqual(
            ["batocera-deck-generated"],
            sorted(path.name for path in self.generated.iterdir()),
        )

    def test_requires_allowlist_for_batocera_entries(self):
        self.write(self.batocera, "approved.desktop", entry("Approved", "/usr/bin/approved"))
        self.write(self.batocera, "unknown.desktop", entry("Unknown", "/usr/bin/unknown"))

        self.run_sync(approved={"approved.desktop"})

        self.assertTrue((self.generated / "approved.desktop").exists())
        self.assertFalse((self.generated / "unknown.desktop").exists())

    def test_flatpak_exports_must_launch_through_flatpak(self):
        self.write(self.flatpak, "valid.desktop", entry("Valid", "/usr/bin/flatpak run org.example.Valid"))
        self.write(self.flatpak, "payload.desktop", entry("Payload", "/tmp/payload"))

        manifest = self.run_sync()

        self.assertEqual({"valid.desktop"}, set(manifest))

    def test_validates_and_preserves_desktop_actions(self):
        content = entry("Browser", "/usr/bin/browser") + (
            "[Desktop Action private]\n"
            "Name=Private Window\n"
            "Exec=/usr/bin/browser --private\n"
        )
        self.write(self.system, "browser.desktop", content)

        self.run_sync()

        self.assertEqual(content, (self.generated / "browser.desktop").read_text())

    def test_cli_rejects_absolute_system_source(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--rootfs",
                str(self.rootfs),
                "--home",
                str(self.home),
                "--system-dir",
                "/tmp/applications",
                "--uid",
                str(os.getuid()),
                "--gid",
                str(os.getgid()),
            ],
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("must be relative", result.stderr)

    def test_cli_rejects_system_source_traversal(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--rootfs",
                str(self.rootfs),
                "--home",
                str(self.home),
                "--system-dir",
                "../applications",
                "--uid",
                str(os.getuid()),
                "--gid",
                str(os.getgid()),
            ],
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("must be relative", result.stderr)

    def test_rejects_symlinked_generated_directory(self):
        applications = self.home / ".local/share/applications"
        applications.mkdir(parents=True, exist_ok=True)
        (applications / "batocera-deck-generated").symlink_to(self.base)

        with self.assertRaises(SYNC.EntryError):
            self.run_sync()


if __name__ == "__main__":
    unittest.main()
