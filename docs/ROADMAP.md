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

## Phase 5: Product qualification

- Hardware compatibility matrix and 100-cycle lifecycle/fault suites.
- Suspend, dock/undock, TV power, Bluetooth reconnect, disk-full, interrupted update,
  factory reset, and rollback qualification.
- Secure Boot/measured-boot decision, threat model review, penetration test, support
  policy, warranty/recovery documentation, release signing runbook, and legal review.
