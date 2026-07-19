#!/bin/bash
set -u

rootfs=/userdata/system/containers/arch-plasma/rootfs
mounts=/usr/libexec/batocera-deck-desktop/arch-plasma-mounts
controller=/usr/libexec/batocera-deck-desktop/desktop-controller
runtime=/run/batocera-deck-desktop
pidfile="$runtime/session.pid"
command_file="$runtime/command"
wayland_socket=/run/wayland-0
guest_runtime=/run/deck-desktop-runtime-1000
wrapper="$rootfs/usr/local/bin/kwin_wayland_wrapper"

valid_session_pid() {
    pid=${1:-0}
    expected_start=${2:-}
    case "$pid:$expected_start" in *[!0-9:]*|:|*:) return 1 ;; esac
    [ -d "/proc/$pid" ] || return 1
    [ "$(readlink "/proc/$pid/root" 2>/dev/null)" = "$rootfs" ] || return 1
    [ "$(awk '{print $22}' "/proc/$pid/stat" 2>/dev/null)" = "$expected_start" ]
}

read_session_state() {
    session_pid=
    session_start=
    [ -s "$pidfile" ] || return 1
    IFS=: read -r session_pid session_start <"$pidfile"
    valid_session_pid "$session_pid" "$session_start"
}

stop_session() {
    if read_session_state; then
        kill -TERM -- "-$session_pid" 2>/dev/null || kill -TERM "$session_pid" 2>/dev/null || true
        for _ in $(seq 1 20); do
            kill -0 "$session_pid" 2>/dev/null || break
            sleep 0.1
        done
        valid_session_pid "$session_pid" "$session_start" &&
            kill -KILL -- "-$session_pid" 2>/dev/null || true
    fi
    "$controller" stop >/dev/null 2>&1 || true
    rm -f "$pidfile" "$command_file"
    setfacl -x u:1000 "$wayland_socket" 2>/dev/null || true
    rm -rf "$rootfs$guest_runtime"
    "$mounts" stop >/dev/null 2>&1 || true
}

case "${1:-start}" in
    stop) stop_session; exit 0 ;;
    start) ;;
    *) printf 'Usage: %s {start|stop}\n' "$0" >&2; exit 2 ;;
esac

read_session_state && {
    echo "A Plasma session is already running" >&2
    exit 1
}
[ -S "$wayland_socket" ] || exit 1
[ -S "$runtime/audio/native" ] || exit 1
[ -x "$wrapper" ] || exit 1

session_pid=
session_start=
cleaned=false
cleanup() {
    [ "$cleaned" = false ] || return 0
    cleaned=true
    trap - EXIT INT TERM HUP
    stop_session
}
trap cleanup EXIT INT TERM HUP

"$mounts"
rm -rf "$rootfs$guest_runtime"
mkdir -p "$rootfs$guest_runtime"
chown 1000:1000 "$rootfs$guest_runtime"
chmod 0700 "$rootfs$guest_runtime"
setfacl -m u:1000:rwx "$wayland_socket"
: >"$command_file"
chown root:1000 "$command_file"
chmod 0660 "$command_file"

setsid chroot "$rootfs" /usr/bin/setpriv \
    --reuid=1000 --regid=1000 --init-groups --no-new-privs \
    /usr/bin/env -i \
    HOME=/home/deck USER=deck LOGNAME=deck SHELL=/bin/bash \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/bin \
    XDG_RUNTIME_DIR="$guest_runtime" XDG_SESSION_TYPE=wayland \
    XDG_SESSION_DESKTOP=KDE XDG_CURRENT_DESKTOP=KDE KDE_FULL_SESSION=true \
    XDG_CONFIG_DIRS=/etc/xdg \
    XDG_DATA_DIRS=/home/deck/.local/share/flatpak/exports/share:/usr/local/share:/usr/share \
    LUIGIOS_SESSION=desktop \
    LUIGIOS_BRAND_MANIFEST=/run/luigios-branding/brand-v1.json \
    DBUS_SYSTEM_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket \
    WAYLAND_DISPLAY=/run/wayland-0 QT_QPA_PLATFORM=wayland \
    PULSE_SERVER=unix:/run/batocera-deck-desktop/audio/native \
    /usr/bin/dbus-run-session -- /usr/bin/plasma_session &
session_pid=$!
session_start=$(awk '{print $22}' "/proc/$session_pid/stat")
printf '%s:%s\n' "$session_pid" "$session_start" >"$pidfile"

started=false
for _ in $(seq 1 80); do
    valid_session_pid "$session_pid" "$session_start" || break
    for process in /proc/[0-9]*; do
        case "$(cat "$process/comm" 2>/dev/null)" in kwin_wayland|kwin_wayland_wr) ;; *) continue ;; esac
        [ "$(readlink "$process/root" 2>/dev/null)" = "$rootfs" ] || continue
        started=true
        break
    done
    [ "$started" = false ] || break
    sleep 0.25
done
[ "$started" = true ] || exit 1
"$controller" start || exit 1

while valid_session_pid "$session_pid" "$session_start"; do
    if [ -s "$command_file" ]; then
        IFS= read -r command <"$command_file"
        : >"$command_file"
        case "$command" in
            return|steam-gamepadui|steam-bigpicture|steam-desktop|steam-app:*) break ;;
        esac
    fi
    sleep 0.25
done
