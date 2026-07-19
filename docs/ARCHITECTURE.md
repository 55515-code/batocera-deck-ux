# Product Architecture

The non-negotiable product contract is defined in
[Product Principles](PRODUCT_PRINCIPLES.md). Network and developer machinery must not
make the foreground console experience slower, noisier, or harder to recover.

## Product contract

- Controller-first appliance UX; terminal and desktop are optional expert tools.
- No ROMs, proprietary BIOS, firmware, console keys, or copyrighted artwork in releases.
- Reproducible, signed image and add-on builds with a tested compatibility tuple.
- Atomic upgrades with a known-good rollback and graphical factory/user-data reset.
- All mutable user data lives outside the immutable product image.

## Layers

1. **Batocera base**: upstream game lifecycle, configgen, ES, hardware support.
2. **Deck product packages**: display policy, controller bridge, recovery supervisor,
   storage broker, migration service, and graphical settings pages.
3. **Versioned desktop image**: immutable, pinned Plasma artifact; only home and
   user Flatpaks persist.
4. **Private user data**: separately generated firmware/config/save and ROM bundles.

The target resembles image-based projects such as uBlue in repeatability and
release promotion, but should use Batocera-native Buildroot packages and boot/update
mechanisms rather than layering a second operating-system updater over Batocera.

## Graphical UX

- First Boot: language, network, display, controllers, storage, legal ownership notice.
- Library Import: detect media, preview systems, validate formats/hashes, copy/move plan.
- Firmware Center: required/optional/missing/invalid/installed state without downloads.
- Storage: initialize/adopt/eject media, library placement, capacity and health.
- Backup and Restore: category selection, verification, conflict preview, rollback.
- Restore Points: optional Btrfs snapshots, retention, file recovery, and offline restore.
- Trusted Vaults: explicit peer pairing, private backup, readable grants, and revocation.
- Recovery: restart UI, reset one emulator, reset desktop, user-data reset, factory reset.
- Updates: stable/candidate channels, release notes, health gate, rollback action.

Privileged operations run through a narrow host broker with a documented command
schema. The UI never receives unrestricted sudo or host `/dev`, `/proc`, `/sys`,
or `/run` access.
