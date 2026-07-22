#!/usr/bin/env python3
"""Synchronize trusted application launchers into the persistent Plasma menu."""

from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import os
import re
import shlex
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_ROOTFS = Path("/userdata/system/containers/arch-plasma/rootfs")
DEFAULT_HOME = Path("/userdata/system/containers/arch-plasma/home/deck")
GENERATED_DIRECTORY = "batocera-deck-generated"
MANIFEST_NAME = "manifest.json"
MAX_ENTRY_SIZE = 1024 * 1024
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*\.desktop$")
FIELD_CODE = re.compile(r"%(?:[fFuUdDnNickvm]|%)")
UNSAFE_EXECUTABLES = {
    "bash",
    "dash",
    "fish",
    "sh",
    "sudo",
    "su",
    "zsh",
}
DEFAULT_APPROVED_BATOCERA = (
    "batocera-config.desktop",
    "batocera-file-manager.desktop",
    "batocera-settings.desktop",
    "return-to-luigios.desktop",
    "return-to-batocera.desktop",
    "steam-big-picture.desktop",
)


class EntryError(ValueError):
    pass


@dataclass(frozen=True)
class Candidate:
    desktop_id: str
    source_kind: str
    source_path: Path
    content: bytes
    digest: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rootfs", type=Path, default=DEFAULT_ROOTFS)
    parser.add_argument("--home", type=Path, default=DEFAULT_HOME)
    parser.add_argument(
        "--system-dir",
        action="append",
        type=Path,
        help="Rootfs-relative application directory; may be repeated",
    )
    parser.add_argument(
        "--flatpak-dir",
        type=Path,
        help="Flatpak export application directory (defaults below --home)",
    )
    parser.add_argument(
        "--batocera-dir",
        type=Path,
        help="Approved Batocera launcher directory (defaults below --rootfs)",
    )
    parser.add_argument(
        "--approved-batocera",
        action="append",
        default=None,
        metavar="DESKTOP_ID",
        help="Approved Batocera desktop ID; may be repeated",
    )
    parser.add_argument("--uid", type=int, default=1000)
    parser.add_argument("--gid", type=int, default=1000)
    return parser.parse_args()


def regular_file(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and not path.is_symlink()


def load_entry(path: Path, source_kind: str) -> Candidate:
    if not SAFE_ID.fullmatch(path.name):
        raise EntryError("unsafe desktop ID")
    if not regular_file(path):
        raise EntryError("not a regular file")
    if path.stat().st_size > MAX_ENTRY_SIZE:
        raise EntryError("entry is too large")

    content = path.read_bytes()
    if b"\x00" in content:
        raise EntryError("entry contains NUL")
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise EntryError("entry is not UTF-8") from error

    parser = configparser.ConfigParser(
        interpolation=None,
        strict=True,
        delimiters=("=",),
        comment_prefixes=("#",),
        inline_comment_prefixes=None,
    )
    parser.optionxform = str
    try:
        parser.read_string(text)
    except configparser.Error as error:
        raise EntryError(f"malformed desktop entry: {error}") from error
    sections = set(parser.sections())
    if "Desktop Entry" not in sections or any(
        section != "Desktop Entry" and not section.startswith("Desktop Action ")
        for section in sections
    ):
        raise EntryError("unexpected or missing section")

    entry = parser["Desktop Entry"]
    if entry.get("Type") != "Application" or not entry.get("Name", "").strip():
        raise EntryError("entry is not a named application")
    if _desktop_boolean(entry.get("Hidden")) or _desktop_boolean(entry.get("NoDisplay")):
        raise EntryError("entry is hidden")
    executable = validate_exec(entry.get("Exec", ""))
    if source_kind == "flatpak" and not is_flatpak_exec(executable):
        raise EntryError("Flatpak export does not launch through Flatpak")
    for section_name in sorted(sections - {"Desktop Entry"}):
        action = parser[section_name]
        if not action.get("Name", "").strip():
            raise EntryError("desktop action has no name")
        action_executable = validate_exec(action.get("Exec", ""))
        if source_kind == "flatpak" and not is_flatpak_exec(action_executable):
            raise EntryError("Flatpak action does not launch through Flatpak")

    digest = hashlib.sha256(content).hexdigest()
    return Candidate(path.name, source_kind, path, content, digest)


def _desktop_boolean(value: str | None) -> bool:
    return value is not None and value.strip().lower() == "true"


def validate_exec(value: str) -> list[str]:
    if not value or "\n" in value or "\r" in value:
        raise EntryError("missing or multiline Exec")
    try:
        words = shlex.split(value, posix=True)
    except ValueError as error:
        raise EntryError("malformed Exec quoting") from error
    if not words:
        raise EntryError("empty Exec")

    executable = words[0]
    if executable.startswith("-") or os.path.basename(executable) in UNSAFE_EXECUTABLES:
        raise EntryError("unsafe executable wrapper")
    for word in words:
        remainder = FIELD_CODE.sub("", word)
        if "%" in remainder or any(ord(character) < 32 for character in remainder):
            raise EntryError("invalid Exec field code")
    return words


def is_flatpak_exec(words: list[str]) -> bool:
    executable = os.path.basename(words[0])
    if executable != "flatpak":
        return False
    try:
        run_index = words.index("run", 1)
    except ValueError:
        return False
    return run_index > 0 and run_index + 1 < len(words)


def discover(directory: Path, source_kind: str) -> Iterable[Candidate]:
    if not directory.is_dir():
        return
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        if path.suffix != ".desktop":
            continue
        try:
            yield load_entry(path, source_kind)
        except (EntryError, OSError) as error:
            print(f"skip {source_kind} entry {path}: {error}")


def read_manifest(path: Path) -> dict[str, dict[str, str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, dict):
        return {}
    return {
        desktop_id: metadata
        for desktop_id, metadata in entries.items()
        if SAFE_ID.fullmatch(desktop_id) and isinstance(metadata, dict)
    }


def atomic_write(path: Path, content: bytes, mode: int, uid: int, gid: int) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        try:
            os.chown(temporary, uid, gid)
        except PermissionError:
            if (uid, gid) != (os.getuid(), os.getgid()):
                raise
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def file_digest(path: Path) -> str | None:
    if not regular_file(path):
        return None
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def ensure_private_tree(home: Path, uid: int, gid: int) -> tuple[Path, Path]:
    if not regular_directory(home):
        raise EntryError(f"persistent home is not a regular directory: {home}")
    current = home
    for component in (".local", "share", "applications"):
        current = current / component
        if current.exists() or current.is_symlink():
            if not regular_directory(current):
                raise EntryError(f"unsafe generated directory: {current}")
        else:
            current.mkdir(mode=0o755)
            os.chown(current, uid, gid)
    destination = current
    manifest_directory = destination / GENERATED_DIRECTORY
    if manifest_directory.exists() or manifest_directory.is_symlink():
        if not regular_directory(manifest_directory):
            raise EntryError(f"unsafe manifest directory: {manifest_directory}")
    else:
        manifest_directory.mkdir(mode=0o700)
    os.chown(manifest_directory, uid, gid)
    os.chmod(manifest_directory, 0o700)
    return destination, manifest_directory


def regular_directory(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISDIR(mode) and not path.is_symlink()


def synchronize(
    rootfs: Path,
    home: Path,
    system_dirs: list[Path],
    flatpak_dir: Path,
    batocera_dir: Path,
    approved_batocera: set[str],
    uid: int,
    gid: int,
) -> dict[str, dict[str, str]]:
    destination, manifest_directory = ensure_private_tree(home, uid, gid)
    try:
        os.chown(destination, uid, gid)
    except PermissionError:
        if (uid, gid) != (os.getuid(), os.getgid()):
            raise
    os.chmod(destination, 0o755)

    manifest_path = manifest_directory / MANIFEST_NAME
    previous = read_manifest(manifest_path)
    candidates: dict[str, Candidate] = {}
    for directory in system_dirs:
        candidates.update((item.desktop_id, item) for item in discover(rootfs / directory, "system"))
    candidates.update((item.desktop_id, item) for item in discover(flatpak_dir, "flatpak"))
    for item in discover(batocera_dir, "batocera"):
        if item.desktop_id in approved_batocera:
            candidates[item.desktop_id] = item

    generated: dict[str, dict[str, str]] = {}
    for desktop_id, candidate in sorted(candidates.items()):
        target = destination / desktop_id
        old = previous.get(desktop_id, {})
        current_digest = file_digest(target)
        owned = current_digest is None or current_digest == old.get("digest")
        if not owned:
            print(f"preserve user-modified entry {target}")
            continue
        if current_digest != candidate.digest:
            atomic_write(target, candidate.content, 0o644, uid, gid)
        generated[desktop_id] = {
            "digest": candidate.digest,
            "source": candidate.source_kind,
            "source_path": str(candidate.source_path),
        }

    for desktop_id, metadata in sorted(previous.items()):
        if desktop_id in generated:
            continue
        target = destination / desktop_id
        if file_digest(target) == metadata.get("digest"):
            target.unlink(missing_ok=True)
            directory_descriptor = os.open(destination, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        elif target.exists():
            print(f"preserve user-modified stale entry {target}")

    manifest = {"entries": generated, "version": 1}
    manifest_content = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    atomic_write(manifest_path, manifest_content, 0o644, uid, gid)
    return generated


def main() -> int:
    args = parse_args()
    system_dirs = args.system_dir or [
        Path("usr/share/applications"),
        Path("usr/local/share/applications"),
    ]
    for directory in system_dirs:
        if directory.is_absolute() or ".." in directory.parts:
            raise SystemExit("--system-dir must be relative to --rootfs")
    flatpak_dir = args.flatpak_dir or (
        args.home / ".local/share/flatpak/exports/share/applications"
    )
    batocera_dir = args.batocera_dir or (
        args.rootfs / "mnt/batocera/desktop-shortcuts"
    )
    approved = set(args.approved_batocera or DEFAULT_APPROVED_BATOCERA)
    if any(not SAFE_ID.fullmatch(item) for item in approved):
        raise SystemExit("approved Batocera entries must be safe desktop IDs")
    generated = synchronize(
        rootfs=args.rootfs,
        home=args.home,
        system_dirs=system_dirs,
        flatpak_dir=flatpak_dir,
        batocera_dir=batocera_dir,
        approved_batocera=approved,
        uid=args.uid,
        gid=args.gid,
    )
    print(f"synchronized {len(generated)} Plasma application entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
