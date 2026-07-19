# Production Roadmap

Phases are gated in product-priority order. Peer infrastructure does not delay basic
recovery, input, display, storage, and desktop reliability.

## Phase 0: Prototype stabilization

- Finish game/desktop lifecycle fault tests and controller hotplug tests.
- Replace custom RunImage Steam with Batocera's supported Steam integration.
- Remove unrestricted chroot sudo and broad host mounts from the shipping profile.
- Reduce Plasma cold-start time and pin the desktop image/package set.
- Turn every live script into a versioned package with install, migration, and uninstall.

## Phase 1: Reproducible product image

- Add a Steam Deck board/config fragment and pinned build container.
- Produce deterministic artifacts, SBOM, license report, provenance, and checksums.
- Run clean independent rebuild comparison in GitHub Actions/self-hosted builders.
- Publish immutable candidate artifacts; no P2P installation yet.

## Phase 2: Graphical appliance UX

- First Boot, Storage, Firmware Center, Library Import, Backup/Restore, Recovery,
  Update/Rollback, Controller, Display, and Diagnostics screens.
- Add Btrfs Restore Points after the managed subvolume migration and power-loss tests pass;
  retain equivalent backup/restore workflows for ext4.
- Expose privileged work through a narrow versioned broker, never GUI sudo.
- Make every destructive action previewable, cancellable, and recoverable.

## Phase 3: Trusted updates and rollback

- TUF repository and threshold key ceremony.
- Native A/B boot slots, boot-attempt counter, health commit, automatic fallback.
- Stable/candidate/beta/testing promotion by digest and graphical rollback/reset.

## Phase 4: Community P2P

- Content-defined chunk store and HTTPS/OCI origins.
- TUF-signed BitTorrent v2 metadata, web seeds, project tracker, quotas, privacy modes.
- Opt-in seeding, battery/metered policy, cache garbage collection, revocation drills.
- Benchmark BitTorrent-only discovery before approving a second IPFS/libp2p stack.
- Prototype I2P only as an isolated opt-in privacy profile after the default path is stable.
- Import recognized vanilla Batocera torrent state and verify cross-community seeding by
  complete content identity without disturbing unknown personal torrents.

## Phase 5: Product qualification

- Hardware compatibility matrix and 100-cycle lifecycle/fault suites.
- Suspend, dock/undock, TV power, Bluetooth reconnect, disk-full, interrupted update,
  factory reset, and rollback qualification.
- Secure Boot/measured-boot decision, threat model review, penetration test, support
  policy, warranty/recovery documentation, release signing runbook, and legal review.

## Later: Trusted Vaults

- Controller-first mutual pairing and non-transitive per-vault grants using Syncthing.
- Storage-only encrypted backups, recovery ceremony, revocation, and restore drills.
- Static/private addressing first; evaluate I2P SAM only after isolated transport tests.
- No public index, stranger discovery, public-update cache reuse, or anonymity promise.
- Per-system and collection sharing derived from Batocera system definitions, with staged
  hash verification, conflict preview, atomic library import, and declarative safe presets.

## Stretch: Android application compatibility

- Run a Waydroid feasibility spike on the product Wayland session, reusing its upstream LXC,
  namespace, Binder, x86_64, AMD Mesa, full-screen, and application-integration design.
- Package a pinned AOSP/LineageOS-compatible runtime through Buildroot integration rather than
  installing a mutable second distribution or downloading executable setup scripts at runtime.
- Add controller-first Android app discovery and launch entries, per-app control profiles,
  touch mapping, OSK, audio, rotation, suspend/resume, and clean return to Gaming Mode.
- Keep Android application data in a bounded user-data subvolume with graphical storage,
  permission, backup, reset, runtime repair, and complete removal controls.
- Qualify native x86/x86_64 apps first. Treat ARM translation, DRM, integrity attestation,
  anti-cheat, camera, telephony, and location-dependent software as unsupported until proven.
- Ship a functional FOSS/AOSP path without proprietary Google components. Investigate Android
  CDD/CTS qualification and Google Mobile Services licensing as the only product path for a
  preinstalled Play Store; do not redistribute Play Store or GMS outside applicable licenses.
- If licensing is unavailable, permit a clearly unsupported expert workflow for user-provided
  compatible images without project hosting, extraction, or circumvention of proprietary files.

This goal remains behind image reproducibility, recovery, input/display reliability, and the
security model. Waydroid's [official architecture](https://waydro.id/) confirms the relevant
Wayland/container approach; Google's [Android compatibility program](https://source.android.com/docs/compatibility/overview)
defines compatibility and GMS licensing as separate gates.
