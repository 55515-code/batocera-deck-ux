# Test Strategy

## Pull-request gate

- Python unit tests, JSON policy invariants, shell syntax, and warning-clean bridge build.
- Repository hygiene scan for private payloads, credentials, moving remote execution,
  and oversized accidental artifacts.
- Migration tamper, conflict-backup, and dry-run behavior.

## Candidate image gate

- Clean image boot and first-boot storage initialization.
- Gaming Mode, Plasma launch/return, forced-session recovery, suspend/resume, and reboot.
- Built-in controls plus DualSense connect, reconnect, cursor, clicks, OSK, and exit chord.
- Handheld 1280x800 plus HDMI dock/undock, TV overscan, audio route, and controller order.
- Representative emulator launches, save/load/state, hotkeys, and return to ES.
- Private firmware and ROM migration dry-run, import, verify, low-space, and interruption.
- Update stage, power loss, failed health check, automatic fallback, rollback, and reset.
- Btrfs restore-point create/prune/restore, metadata ENOSPC, nested subvolumes, and ext4 fallback.

Attach a hardware report to candidate pull requests. Record Deck model, BIOS, image digest,
dock/controller models, display mode, exact test cases, results, logs, and screenshots.
Passing one developer Deck is prototype evidence, not product qualification.
