#!/bin/bash
set -euo pipefail

bridge=/usr/libexec/batocera-deck-desktop/plasma-gamepad-bridge
runtime=/run/batocera-deck-desktop
pidfile="$runtime/controller.pid"
log=/userdata/system/logs/batocera-deck-controller.log

valid_pid() {
    pid=${1:-0}
    case "$pid" in ''|*[!0-9]*) return 1 ;; esac
    [ -r "/proc/$pid/exe" ] && [ "$(readlink "/proc/$pid/exe")" = "$bridge" ]
}

start_mapper() {
    [ -f "$runtime/desktop.active" ] || return 1
    if [ -s "$pidfile" ] && valid_pid "$(cat "$pidfile")"; then
        return 0
    fi
    rm -f "$pidfile"
    mkdir -p "$(dirname "$log")"
    [ -x "$bridge" ] && [ -c /dev/uinput ] || return 1
    setfacl -m u:1000:rw /dev/uinput
    start-stop-daemon -S -b -m -p "$pidfile" -x /usr/bin/setpriv -- \
        --reuid=1000 --regid=1000 --init-groups --no-new-privs \
        "$bridge" >>"$log" 2>&1
}

stop_mapper() {
    if [ -s "$pidfile" ] && valid_pid "$(cat "$pidfile")"; then
        start-stop-daemon -K -p "$pidfile" -x "$bridge" --retry TERM/2/KILL/1 || true
    fi
    rm -f "$pidfile"
    setfacl -x u:1000 /dev/uinput 2>/dev/null || true
}

case "${1:-}" in
    start) start_mapper ;;
    stop) stop_mapper ;;
    restart) stop_mapper; start_mapper ;;
    *) printf 'Usage: %s {start|stop|restart}\n' "$0" >&2; exit 2 ;;
esac
