# Test Strategy

## Pull-request gate

`./tools/ci-check` is the only authoritative source gate. On a clean revision,
`./tools/qualify-source run` executes it and emits `report.json` plus a SHA-256-bound
log. GitHub Actions uploads that evidence for every pull request and main-branch build.
The report is bound to the Git commit, tree, dependency pins, and Buildroot package set.
It deliberately does not claim that an OS image was built or hardware-qualified.

- Python unit tests, JSON policy invariants, shell syntax, and warning-clean bridge build.
- Repository hygiene scan for private payloads, credentials, moving remote execution,
  and oversized accidental artifacts.
- Migration tamper, conflict-backup, and dry-run behavior.
- Validate `profiles/secure-implementation-v1.json`. Run warning-clean hardened native
  builds, dependency/static analysis, sanitizer coverage, and parser fuzz smoke tests as
  applicable to changed security-sensitive code.

## Candidate image gate

- Complete first boot, browse the library, launch and exit a local game, open settings,
  and enter recovery without a LuigiOS account, network connection, subscription,
  storefront, advertisement, or terminal.
- Run the same vanilla path with networking physically unavailable. Network setup must be
  skippable; backup, restore, reset, controller setup, and local administration must remain
  usable. A third-party login prompt may block only the service that owns it.
- Validate `profiles/interface-guidelines-v1.json` with controller-only handheld and TV
  runs, active-controller glyph changes, localization expansion, and visual comparison
  review for confusing similarity to proprietary console interfaces.
- Verify library order and recommendations contain no paid or sponsored placement.
  Optional third-party stores and services must remain clearly identified and removable.
- Export user data, create and restore a backup, reset the device, decline diagnostics,
  and decline peer distribution from controller-first interfaces. Neither opt-out may
  prevent offline play, updates through another supported transport, or local recovery.
- Clean image boot and first-boot storage initialization.
- Gaming Mode, COSMIC launch/return, forced-session recovery, suspend/resume, and reboot.
- Desktop audio must play through the host PipeWire graph while only the surviving ES
  stream is muted; return must restore its pre-session state even if PipeWire reindexes it.
- COSMIC networking must enumerate and change connections through the sole host ConnMan
  daemon; fail the image if NetworkManager or a container network daemon is active.
- In Developer Mode, establish SSH over Wi-Fi, verify the connectivity guard records the
  healthy service, simulate default-route loss without stopping ConnMan, and confirm a
  bounded reconnect request restores access. Verify it remains dormant in Gamer Mode,
  never restarts the network stack, and respects Wi-Fi that was off at session start.
- Install and launch a real Flatpak GUI application as UID 1000. Portals or package
  installation alone do not pass; verify user namespaces and Bubblewrap sandbox creation.
- Validate the LuigiOS brand manifest and artwork provenance. Check boot, ES, COSMIC,
  settings, recovery, and Steam handoff at 1280x800 and 1920x1080; verify fallback
  artwork, text legibility, icon recognition, and a transactional demo rollback.
- Generate graphics inventories for all policy roots, apply only exact-hash replacement
  overlays, then visually review every boot frame, theme, icon, launch screen, help
  overlay, preview, and recovery surface for unapproved third-party marks.
- Built-in controls plus DualSense connect, reconnect, cursor, clicks, OSK, and exit chord.
- Handheld 1280x800 plus HDMI dock/undock, TV overscan, audio route, and controller order.
- Representative emulator launches, save/load/state, hotkeys, and return to ES.
- Private firmware and ROM migration dry-run, import, verify, low-space, and interruption.
- Update stage, power loss, failed health check, automatic fallback, rollback, and reset.
- Btrfs restore-point create/prune/restore, metadata ENOSPC, nested subvolumes, and ext4 fallback.

Attach a hardware report to candidate pull requests. Record Deck model, BIOS, image digest,
dock/controller models, display mode, exact test cases, results, logs, and screenshots.
Passing one developer Deck is prototype evidence, not product qualification.

The candidate must match `profiles/product-identity-v1.json`. A commercial relationship,
store integration, or downstream request cannot waive an identity, QA, security, privacy,
or release-trust check.

The creator's live Deck is an experimental target governed by
`profiles/beta-qualification-v1.json`. Every SSH test begins and ends with the read-only
`tools/device-qa` probe. Remote tests must preserve the active SSH path and must never
write to the separately mounted ROM SD card.

Steam Deck is the reference platform, but each model, firmware, dock, and material
configuration still needs its own evidence. Reports for other devices are welcome and
must use the tier policy in `profiles/hardware-support-v1.json`. Community-tested,
downstream-maintained, experimental, and unverified hardware does not block core releases
unless a failure also affects the reference platform or a shared security invariant.

## Android compatibility stretch gate

- Verify kernel Binder support, container isolation, GPU acceleration, audio, network, input,
  touch, OSK, screen rotation, clipboard policy, and full-screen Wayland presentation.
- Test launch/exit, controller hotplug, dock/undock, suspend/resume, low storage, runtime reset,
  app-data backup/restore, and removal without affecting Batocera or COSMIC sessions.
- Maintain an app matrix separating x86-native, translated ARM, DRM/attestation-dependent, and
  unsupported hardware-dependent applications; passing a storefront launch is not sufficient.
- Never place GMS or Play Store artifacts in project CI, caches, source releases, or images
  unless a documented redistribution license and release approval explicitly cover them.
