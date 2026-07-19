# Test Strategy

## Pull-request gate

- Python unit tests, JSON policy invariants, shell syntax, and warning-clean bridge build.
- Repository hygiene scan for private payloads, credentials, moving remote execution,
  and oversized accidental artifacts.
- Migration tamper, conflict-backup, and dry-run behavior.

## Candidate image gate

- Clean image boot and first-boot storage initialization.
- Gaming Mode, Plasma launch/return, forced-session recovery, suspend/resume, and reboot.
- Desktop audio must play through the host PipeWire graph while only the surviving ES
  stream is muted; return must restore its pre-session state even if PipeWire reindexes it.
- Plasma networking must enumerate and change connections through the sole host ConnMan
  daemon; fail the image if NetworkManager or a container network daemon is active.
- Install and launch a real Flatpak GUI application as UID 1000. Portals or package
  installation alone do not pass; verify user namespaces and Bubblewrap sandbox creation.
- Built-in controls plus DualSense connect, reconnect, cursor, clicks, OSK, and exit chord.
- Handheld 1280x800 plus HDMI dock/undock, TV overscan, audio route, and controller order.
- Representative emulator launches, save/load/state, hotkeys, and return to ES.
- Private firmware and ROM migration dry-run, import, verify, low-space, and interruption.
- Update stage, power loss, failed health check, automatic fallback, rollback, and reset.
- Btrfs restore-point create/prune/restore, metadata ENOSPC, nested subvolumes, and ext4 fallback.

Attach a hardware report to candidate pull requests. Record Deck model, BIOS, image digest,
dock/controller models, display mode, exact test cases, results, logs, and screenshots.
Passing one developer Deck is prototype evidence, not product qualification.

## Android compatibility stretch gate

- Verify kernel Binder support, container isolation, GPU acceleration, audio, network, input,
  touch, OSK, screen rotation, clipboard policy, and full-screen Wayland presentation.
- Test launch/exit, controller hotplug, dock/undock, suspend/resume, low storage, runtime reset,
  app-data backup/restore, and removal without affecting Batocera or Plasma sessions.
- Maintain an app matrix separating x86-native, translated ARM, DRM/attestation-dependent, and
  unsupported hardware-dependent applications; passing a storefront launch is not sufficient.
- Never place GMS or Play Store artifacts in project CI, caches, source releases, or images
  unless a documented redistribution license and release approval explicitly cover them.
