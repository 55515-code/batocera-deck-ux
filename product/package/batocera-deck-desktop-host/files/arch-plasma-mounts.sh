#!/bin/bash
set -euo pipefail

rootfs=/userdata/system/containers/arch-plasma/rootfs
home=/userdata/system/containers/arch-plasma/home/deck

mounted() {
    findmnt -rn -o TARGET --target "$1" 2>/dev/null | grep -Fxq "$1"
}

bind_dir() {
    source_path=$1
    target_path=$2
    mode=${3:-rw}
    [ -d "$source_path" ] || return 0
    mkdir -p "$target_path"
    mounted "$target_path" || mount --rbind "$source_path" "$target_path"
    mount --make-rslave "$target_path"
    [ "$mode" != ro ] || mount -o remount,bind,ro "$target_path"
}

bind_file() {
    source_path=$1
    target_path=$2
    [ -e "$source_path" ] || return 1
    mkdir -p "$(dirname "$target_path")"
    if ! mounted "$target_path"; then
        : >"$target_path"
        mount --bind "$source_path" "$target_path"
    fi
}

unmount_path() {
    mounted "$1" || return 0
    umount -R "$1" 2>/dev/null || umount -l "$1" 2>/dev/null || true
}

stop_mounts() {
    unmount_path "$rootfs/home/deck"
    for name in bios saves screenshots themes music; do
        unmount_path "$rootfs/mnt/batocera/$name"
    done
    unmount_path "$rootfs/mnt/roms"
    unmount_path "$rootfs/run/batocera-deck-desktop/audio"
    unmount_path "$rootfs/run/dbus/system_bus_socket"
    unmount_path "$rootfs/run/wayland-0"
    unmount_path "$rootfs/dev/shm"
    unmount_path "$rootfs/dev/dri"
    for device in urandom random zero null; do
        unmount_path "$rootfs/dev/$device"
    done
    unmount_path "$rootfs/proc"
}

case "${1:-start}" in
    start) ;;
    stop) stop_mounts; exit 0 ;;
    *) printf 'Usage: %s {start|stop}\n' "$0" >&2; exit 2 ;;
esac

[ -x "$rootfs/usr/bin/plasmashell" ] || {
    echo "Provisioned Plasma filesystem is unavailable" >&2
    exit 1
}

mkdir -p "$home" "$rootfs/mnt/batocera"
chown 1000:1000 "$home"
chmod 0700 "$home"

mounted "$rootfs/proc" || mount -t proc proc "$rootfs/proc"
for device in null zero random urandom; do
    bind_file "/dev/$device" "$rootfs/dev/$device"
done
bind_dir /dev/dri "$rootfs/dev/dri"
bind_dir /dev/shm "$rootfs/dev/shm"
bind_file /run/wayland-0 "$rootfs/run/wayland-0"
bind_file /run/dbus/system_bus_socket "$rootfs/run/dbus/system_bus_socket"
bind_dir /run/batocera-deck-desktop/audio \
    "$rootfs/run/batocera-deck-desktop/audio"
bind_dir /userdata/roms "$rootfs/mnt/roms"
for name in bios saves screenshots themes music; do
    bind_dir "/userdata/$name" "$rootfs/mnt/batocera/$name"
done
bind_dir "$home" "$rootfs/home/deck"
