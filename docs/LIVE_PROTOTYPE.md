# Live Prototype State

Validated on a Steam Deck LCD running Batocera `44-dev-b96296b988` dated 2026-07-14.
This is a prototype on an unreleased channel, not a production image.

## Verified

- Internal SHARE and SD ROM/Steam library mounts persist after reboot.
- Plasma launches fullscreen at 1280x800 as a foreground Batocera Ports transaction.
- Plasma runs as UID 1000 `deck`; KDE apps, menu, Discover/Flathub, and persistent
  home are present. Flatpak installation works, but application launch is blocked
  by the current Batocera kernel as described below.
- Steam Deck controller bridge starts only during Desktop Mode and supports dynamic
  SDL game-controller discovery, per-controller state, pointer, clicks, keys, and OSK.
- Normal desktop return and forced wrapper death leave no KWin, Plasma, bridge,
  container mount, temporary ACL, cursor, or ES wrapper leak.
- Dolphin GC/Wii save trees were regenerated and tested after quarantining corrupt state.
- Guide/Steam/PS plus Start exits through Batocera; Guide alone is not intercepted.
- Mainstream BIOS audit passes PS1, PS2, PS3, PSP, Vita, Dreamcast, Saturn, Xbox,
  GameCube/Wii, and configured Switch paths. No proprietary files were downloaded.
- 52 emulator configuration files parse; no broken links or stale migration paths.
- Private firmware bundle contains 6,837 files, about 1.95 GB, and verifies by SHA-256.
- Balanced power policy reduced observed idle temperature from 75/67 C to 46/46 C.
- The LuigiOS Game Mode theme is active and survived a supervised EmulationStation
  restart. The separate ROM SD mount remained untouched.

## Desktop direction

The Plasma environment described below is preserved only as historical prototype
evidence and an emergency compatibility reference. It is frozen: do not add LuigiOS
features, applications, settings integrations, or release dependencies to it.

The shipping desktop is COSMIC. Source packages target the pinned contract in
`product/desktop/cosmic-image-v1.json` and the image-owned root at
`/userdata/system/containers/arch-cosmic/rootfs`. The live Deck does not yet have that
rootfs. Provisioning it is blocked until the rootfs, package inventory, build
attestation, SBOM, Flatpak runtime, fullscreen behavior, controller bridge, and return
transaction pass offline validation with a tested watchdog rollback.

## Open release blockers

- Plasma takes roughly 30 seconds after cold service start to reach the settled desktop.
- The chroot has broad host mounts and unrestricted container sudo; neither may ship.
- Custom RunImage Steam remains in place pending migration to supported Batocera Steam.
- HDMI hotplug/TV modes and DualSense reconnect were not physically available for the
  final cold-boot test.
- Cemu's optional encrypted-content `keys.txt` was empty and quarantined; WUA/decrypted
  content is unaffected, but encrypted Wii U content requires the owner's valid file.
- CoCo/Dragon/MC-10, GP32, and Super A'Can BIOS families remain absent.
- The build, desktop rootfs, and update path are not yet reproducible or signed.
- Flatpak applications cannot launch because the running image's user-namespace
  policy rejects Bubblewrap, although the currently pinned x86 Batocera defconfig
  enables `CONFIG_USER_NS`. Do not make Bubblewrap setuid or globally weaken the
  policy as a workaround. Candidate images must prove namespace and Bubblewrap
  operation before advertising Flatpak support; Discovery should show an
  actionable unsupported state until then.

## Historical Plasma host integration

The prototype keeps Batocera as the sole owner of PipeWire/WirePlumber and ConnMan. Plasma's
`plasma-pa` connects to Batocera's Pulse-compatible socket; a boot service restricts that local
socket to root and desktop UID 1000 before granting access. Plasma must not start another audio
policy daemon.

Plasma's `plasma-nm` is not used because it requires NetworkManager. The live prototype uses
CMST as a temporary client of Batocera's host ConnMan over the system bus. NetworkManager,
container ConnMan, iwd, and container wpa_supplicant remain disabled. The shipping direction is
a typed project broker and native settings page rather than retaining an unmaintained tray app.

Desktop Mode remains a synchronous Ports launch. The session defensively preserves and mutes
any surviving EmulationStation Pulse stream, then restores its previous state on every exit
path; it never mutes the device sink.

The live acceptance cycle verifies more than process startup: launch Plasma, wait for a late ES
stream, confirm only that stream is muted, play a desktop sound, enumerate ConnMan services as
UID 1000, return through the desktop shortcut, confirm ES audio is restored, and launch Plasma
again. Flatpak acceptance additionally requires launching an installed graphical application;
a successful Discovery installation alone is not a pass.

## LuigiOS branding

The demo has a persistent LuigiOS identity and brand manifest under
`/userdata/system/configs/luigios`, hostname setting `LUIGIOS`, a canonical
`Return to LuigiOS Game Mode` desktop launcher, and a transactional asset staging
root at `/userdata/system/add-ons/luigios`. The previous Batocera configuration was
backed up before changing identity.

Required boot, Game Mode, desktop wallpaper, mascot, settings-icon, and recovery
assets now pass the brand contract and exact-provenance audit. They were staged and
deployed with byte-for-byte verification. Game Mode activation used a watchdog and
was retained only after EmulationStation restarted successfully. Relevant backups are
`/userdata/system/backups/luigios-branding-20260720-022330`,
`/userdata/system/backups/luigios-activation-20260720-022721`, and
`/userdata/system/backups/luigios-theme-v2-20260720-0232`.

The desktop wallpaper was checked in the disposable Plasma prototype only to validate
the generic asset and UID 1000 ownership contract. This does not qualify Plasma as a
LuigiOS release surface. COSMIC, settings, backup, and migration visuals remain release
blockers; Steam presentation and audio cues remain optional unfinished surfaces.
