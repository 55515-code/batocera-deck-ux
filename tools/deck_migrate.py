#!/usr/bin/env python3
"""Create and apply private, manifest-verified Batocera migration bundles."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

SCHEMA = 1
MANIFEST = "manifest.json"
PAYLOAD = "payload"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def batocera_version() -> str:
    try:
        return subprocess.run(
            ["batocera-version"], check=False, capture_output=True, text=True
        ).stdout.strip()
    except OSError:
        return "unavailable"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def validate_absolute_userdata(path: str) -> Path:
    value = Path(path)
    if not value.is_absolute() or value.parts[:2] != ("/", "userdata"):
        raise ValueError(f"path must be below /userdata: {path}")
    if ".." in value.parts:
        raise ValueError(f"unsafe path: {path}")
    return value


def excluded(relative: Path, patterns: list[str]) -> bool:
    name = relative.as_posix()
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)


def walk_component(component: dict, source_root: Path):
    logical = validate_absolute_userdata(component["path"])
    source = source_root / logical.relative_to("/")
    patterns = component.get("exclude", [])
    if not source.exists() and not source.is_symlink():
        return
    candidates = [source] if not source.is_dir() else source.rglob("*")
    for item in candidates:
        relative = item.relative_to(source) if item != source else Path(item.name)
        if excluded(relative, patterns):
            continue
        logical_item = logical if item == source else logical / relative
        if item.is_symlink():
            yield logical_item, item, "symlink"
        elif item.is_file():
            yield logical_item, item, "file"


def selected_components(profile: dict, categories: set[str]) -> list[dict]:
    components = profile.get("components", [])
    if categories:
        components = [item for item in components if item["category"] in categories]
    return components


def export_bundle(args) -> int:
    profile = load_json(args.profile)
    if profile.get("schema") != SCHEMA:
        raise ValueError("unsupported profile schema")
    output = args.output.resolve()
    source_root = args.source_root.resolve()
    entries = []
    total = 0
    seen = set()
    for component in selected_components(profile, set(args.category or [])):
        for logical, source, kind in walk_component(component, source_root):
            key = logical.as_posix()
            if key in seen:
                continue
            seen.add(key)
            entry = {"path": key, "category": component["category"], "type": kind}
            if kind == "file":
                entry.update(size=source.stat().st_size, sha256=sha256(source))
                total += entry["size"]
            else:
                target = os.readlink(source)
                if os.path.isabs(target) and not target.startswith("/userdata/"):
                    raise ValueError(f"symlink escapes /userdata: {logical} -> {target}")
                entry["target"] = target
            entries.append((entry, source))

    print(json.dumps({"files": len(entries), "bytes": total, "output": str(output)}))
    if args.dry_run:
        return 0
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output is not empty: {output}")
    (output / PAYLOAD).mkdir(parents=True, exist_ok=True)
    manifest_entries = []
    for entry, source in entries:
        destination = output / PAYLOAD / entry["path"].lstrip("/")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if entry["type"] == "file":
            shutil.copy2(source, destination)
        else:
            destination.symlink_to(entry["target"])
        manifest_entries.append(entry)
    manifest = {
        "schema": SCHEMA,
        "kind": "private-user-data",
        "profile": profile["name"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": {"batocera": batocera_version(), "kernel": platform.release()},
        "entries": manifest_entries,
        "total_bytes": total,
    }
    temporary = output / f".{MANIFEST}.tmp"
    temporary.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output / MANIFEST)
    return 0


def load_bundle(bundle: Path) -> dict:
    manifest = load_json(bundle / MANIFEST)
    if manifest.get("schema") != SCHEMA or manifest.get("kind") != "private-user-data":
        raise ValueError("unsupported or non-private bundle")
    return manifest


def payload_path(bundle: Path, logical: str) -> Path:
    safe = validate_absolute_userdata(logical)
    return bundle / PAYLOAD / safe.relative_to("/")


def verify_bundle(bundle: Path, manifest: dict) -> list[str]:
    errors = []
    for entry in manifest["entries"]:
        source = payload_path(bundle, entry["path"])
        if entry["type"] == "file":
            if not source.is_file() or source.is_symlink():
                errors.append(f"missing file: {entry['path']}")
            elif source.stat().st_size != entry["size"] or sha256(source) != entry["sha256"]:
                errors.append(f"checksum mismatch: {entry['path']}")
        elif entry["type"] == "symlink":
            if not source.is_symlink() or os.readlink(source) != entry["target"]:
                errors.append(f"symlink mismatch: {entry['path']}")
        else:
            errors.append(f"unsupported entry type: {entry['path']}")
    return errors


def verify_command(args) -> int:
    bundle = args.bundle.resolve()
    errors = verify_bundle(bundle, load_bundle(bundle))
    for error in errors:
        print(error, file=sys.stderr)
    print(json.dumps({"valid": not errors, "errors": len(errors)}))
    return 1 if errors else 0


def backup_existing(destination: Path, backup_root: Path, target_root: Path) -> None:
    logical = destination.relative_to(target_root)
    backup = backup_root / logical
    backup.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        backup.symlink_to(os.readlink(destination))
    else:
        shutil.copy2(destination, backup)


def import_bundle(args) -> int:
    bundle = args.bundle.resolve()
    manifest = load_bundle(bundle)
    errors = verify_bundle(bundle, manifest)
    if errors:
        raise ValueError(f"bundle verification failed ({len(errors)} errors)")
    target_root = args.target_root.resolve()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = target_root / "userdata/system/config-backups" / f"deck-migrate-{stamp}"
    changes = []
    for entry in manifest["entries"]:
        if args.category and entry["category"] not in args.category:
            continue
        source = payload_path(bundle, entry["path"])
        destination = target_root / entry["path"].lstrip("/")
        same = False
        if entry["type"] == "file" and destination.is_file() and not destination.is_symlink():
            same = destination.stat().st_size == entry["size"] and sha256(destination) == entry["sha256"]
        elif entry["type"] == "symlink" and destination.is_symlink():
            same = os.readlink(destination) == entry["target"]
        if not same:
            changes.append((entry, source, destination))
    print(json.dumps({"changes": len(changes), "backup": str(backup_root)}))
    if not args.apply:
        return 0
    for entry, source, destination in changes:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() or destination.is_symlink():
            backup_existing(destination, backup_root, target_root)
            destination.unlink()
        if entry["type"] == "symlink":
            destination.symlink_to(entry["target"])
        else:
            with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as stream:
                temporary = Path(stream.name)
            try:
                shutil.copy2(source, temporary)
                temporary.replace(destination)
            finally:
                temporary.unlink(missing_ok=True)
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="deck-migrate")
    commands = root.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export")
    export.add_argument("--profile", type=Path, required=True)
    export.add_argument("--output", type=Path, required=True)
    export.add_argument("--source-root", type=Path, default=Path("/"))
    export.add_argument("--category", action="append")
    export.add_argument("--dry-run", action="store_true")
    export.set_defaults(function=export_bundle)
    verify = commands.add_parser("verify")
    verify.add_argument("bundle", type=Path)
    verify.set_defaults(function=verify_command)
    restore = commands.add_parser("import")
    restore.add_argument("bundle", type=Path)
    restore.add_argument("--target-root", type=Path, default=Path("/"))
    restore.add_argument("--category", action="append")
    restore.add_argument("--dry-run", action="store_true")
    restore.add_argument("--apply", action="store_true")
    restore.set_defaults(function=import_bundle)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        if getattr(args, "dry_run", False) and getattr(args, "apply", False):
            raise ValueError("--dry-run and --apply cannot be combined")
        return args.function(args)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"deck-migrate: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
