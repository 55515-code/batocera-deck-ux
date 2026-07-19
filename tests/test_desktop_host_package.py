import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "product/package/batocera-deck-desktop-host"
FILES = PACKAGE / "files"


class DesktopHostPackageTests(unittest.TestCase):
    def read(self, relative):
        return (PACKAGE / relative).read_text(encoding="utf-8")

    def test_package_is_wired_and_experimental_by_default(self):
        top_config = (ROOT / "Config.in").read_text(encoding="utf-8")
        config = self.read("Config.in")

        self.assertIn("batocera-deck-desktop-host/Config.in", top_config)
        self.assertIn("config BR2_PACKAGE_BATOCERA_DECK_DESKTOP_HOST", config)
        self.assertIn("experimental", config.lower())
        self.assertNotRegex(config, r"(?m)^\s*default\s+y\s*$")
        self.assertIn("does not download or embed", config)
        self.assertIn("not a production security boundary", config)
        external_makefile = (ROOT / "external.mk").read_text(encoding="utf-8")
        self.assertIn("product/package/*/*.mk", external_makefile)

    def test_build_uses_target_toolchain_and_declares_dependencies(self):
        makefile = self.read("batocera-deck-desktop-host.mk")

        self.assertIn("$(TARGET_CC)", makefile)
        self.assertIn("$(TARGET_CFLAGS)", makefile)
        self.assertIn("$(TARGET_LDFLAGS)", makefile)
        self.assertIn("-Wall -Wextra -Werror", makefile)
        for dependency in ("acl", "dbus", "jq", "pipewire", "sdl2", "util-linux"):
            self.assertRegex(makefile, rf"DEPENDENCIES\s*=.*\b{re.escape(dependency)}\b")

    def test_package_is_self_contained_and_has_no_mutable_rootfs(self):
        all_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in PACKAGE.rglob("*")
            if path.is_file()
        )

        self.assertNotIn("prototype/", all_text)
        self.assertNotIn("/userdata/system/add-ons", all_text)
        self.assertNotRegex(all_text, r"(?i)\b(curl|wget)\b")
        self.assertNotRegex(all_text, r"(?i)(archlinux-bootstrap|rootfs\.(tar|img))")
        self.assertFalse(any(path.suffix in {".tar", ".gz", ".img"} for path in PACKAGE.rglob("*")))

    def test_image_install_replaces_live_root_copying(self):
        makefile = self.read("batocera-deck-desktop-host.mk")
        service = self.read("files/desktop-host-service")

        self.assertIn("$(TARGET_DIR)/etc/dbus-1/system.d/deck-desktop-connman.conf", makefile)
        self.assertIn("$(TARGET_DIR)/usr/share/pipewire/pipewire-pulse.conf.d/90-deck-desktop-pulse.conf", makefile)
        self.assertNotIn("install_changed", service)
        self.assertNotIn("cp ", service)
        self.assertNotIn("S06audio restart", service)

    def test_package_manifest_matches_installed_owned_files(self):
        makefile = self.read("batocera-deck-desktop-host.mk")
        manifest_lines = [
            line for line in self.read("files/package-files.manifest").splitlines()
            if line
        ]
        manifest = set(manifest_lines)
        installed = set(re.findall(r"\$\(TARGET_DIR\)(/[A-Za-z0-9_./-]+)", makefile))
        installed.discard("/usr/share/batocera/datainit/roms/ports/Desktop")
        installed.add("/usr/share/batocera/datainit/roms/ports/Desktop Mode.sh")

        self.assertEqual(manifest, installed)
        self.assertEqual(len(manifest), len(manifest_lines))

    def test_status_is_observational_and_process_state_is_validated(self):
        service = self.read("files/desktop-host-service")
        session = self.read("files/arch-plasma-session.sh")
        status_body = service.split('status)', 1)[1].split(';;', 1)[0]

        for mutator in ("rm ", "kill", "mount", "setfacl", "chmod"):
            self.assertNotIn(mutator, status_body)
        self.assertIn("/proc/$pid/stat", session)
        self.assertIn("readlink \"/proc/$pid/root\"", session)
        self.assertIn("--no-new-privs", session)

    def test_mounts_do_not_recursively_expose_host_runtime_or_sysfs(self):
        mounts = self.read("files/arch-plasma-mounts.sh")
        package_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in PACKAGE.rglob("*") if path.is_file()
        )

        for broad_mount in (
            'bind_dir /run "$rootfs/run"',
            'bind_dir /dev "$rootfs/dev"',
            'bind_dir /sys "$rootfs/sys"',
            'mount --rbind /run',
            'mount --rbind /dev',
            'mount --rbind /sys',
        ):
            self.assertNotIn(broad_mount, mounts)
        self.assertNotIn("NOPASSWD", package_text)
        self.assertNotIn("sudoers", package_text)
        self.assertIn(
            'bind_dir /userdata/system/configs/luigios "$rootfs/run/luigios-branding" ro',
            mounts,
        )
        self.assertNotIn(
            'bind_dir /userdata/system/configs "$rootfs/run/luigios-branding"',
            mounts,
        )

    def test_shell_files_parse(self):
        scripts = [
            path for path in FILES.iterdir()
            if path.name not in {
                "90-deck-desktop-pulse.conf",
                "deck-desktop-connman.conf",
                "package-files.manifest",
            }
        ]
        for script in scripts:
            result = subprocess.run(
                ["bash", "-n", script], capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, f"{script}: {result.stderr}")

    @unittest.skipUnless(shutil.which("sdl2-config"), "SDL2 development files unavailable")
    def test_controller_bridge_compiles_with_warnings_as_errors(self):
        source = PACKAGE / "src/plasma-gamepad-bridge.c"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "bridge"
            cflags = subprocess.check_output(["sdl2-config", "--cflags"], text=True).split()
            libs = subprocess.check_output(["sdl2-config", "--libs"], text=True).split()
            result = subprocess.run(
                ["cc", "-Wall", "-Wextra", "-Werror", *cflags, source,
                 *libs, "-lm", "-o", output],
                capture_output=True,
                text=True,
                env={**os.environ, "LC_ALL": "C"},
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
