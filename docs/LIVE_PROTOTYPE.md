# Live Prototype State

Validated on a Steam Deck LCD running Batocera `44-dev-b96296b988` dated 2026-07-14.
This is a prototype on an unreleased channel, not a production image.

## Verified

- Internal SHARE and SD ROM/Steam library mounts persist after reboot.
- Plasma launches fullscreen at 1280x800 as a foreground Batocera Ports transaction.
- Plasma runs as UID 1000 `deck`; KDE apps, menu, Discover/Flathub, and persistent
  home are present.
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
