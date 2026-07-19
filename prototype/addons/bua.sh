#!/bin/sh
set -eu

readonly app=/userdata/system/add-ons/bua/bua_installerx86.py
readonly expected=0d64d158b0954a7a3011c5a6883c802fb0812c580c319057eb78af19fbf88a0f

if ! printf '%s  %s\n' "$expected" "$app" | sha256sum -c - >/dev/null 2>&1; then
    echo "BUA integrity check failed. Restore the reviewed application file." >&2
    exit 1
fi

export DISPLAY="${DISPLAY:-:0.0}"
exec python3 "$app" "$@"
