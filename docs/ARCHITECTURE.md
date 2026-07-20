# Product Architecture

The non-negotiable product contract is defined in
[Product Principles](PRODUCT_PRINCIPLES.md). Network and developer machinery must not
make the foreground console experience slower, noisier, or harder to recover.
LuigiOS-authored services also follow the memory-safety, native hardening, privilege,
dependency, and verification contract in [Secure Implementation](SECURE_IMPLEMENTATION.md).

## Product contract

- Controller-first appliance UX; terminal and desktop are optional expert tools.
- Gamer Mode is the reset/default presentation; Developer Mode reversibly reveals
  implementation detail without weakening update trust or the privilege broker.
- Steam Deck is the reference build and qualification platform; additional hardware
  uses isolated capability profiles and explicit non-support evidence tiers.
- No ROMs, proprietary BIOS, firmware, console keys, or copyrighted artwork in releases.
- Reproducible, signed image and add-on builds with a tested compatibility tuple.
- Atomic upgrades with a known-good rollback and graphical factory/user-data reset.
- All mutable user data lives outside the immutable product image.
- Local play and administration require no LuigiOS account; ads, sponsored ranking,
  forced storefronts, and telemetry-by-default are outside the product contract.
- Vanilla deployment and first boot work without network access or login. Optional
  proprietary services may gate only their own surface, never the local shell.

## Layers

1. **Batocera base**: upstream game lifecycle, configgen, ES, hardware support.
2. **LuigiOS product packages**: display policy, controller bridge, recovery supervisor,
   storage broker, migration service, and graphical settings pages.
3. **Versioned desktop image**: immutable, pinned Arch COSMIC artifact presented
   fullscreen through Batocera's Wayland session; only home and user Flatpaks persist.
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

The complete settings information architecture and privilege boundary are defined in
[ADR 0005](adr/0005-unified-device-settings.md). The initial machine contract is
[`profiles/settings-registry-v1.json`](../profiles/settings-registry-v1.json).
Progressive disclosure and app visibility are defined in [ADR 0006](adr/0006-progressive-disclosure-and-developer-mode.md)
and [`profiles/experience-modes-v1.json`](../profiles/experience-modes-v1.json).
Hardware ownership, evidence, and maintenance tiers are defined in
[ADR 0007](adr/0007-reference-platform-and-community-hardware.md) and
[`profiles/hardware-support-v1.json`](../profiles/hardware-support-v1.json).
Original controller, layout, motion, offline, and third-party handoff rules are defined in
[Interface Guidelines](INTERFACE_GUIDELINES.md) and
[`profiles/interface-guidelines-v1.json`](../profiles/interface-guidelines-v1.json).

Privileged operations run through a narrow host broker with a documented command
schema. The UI never receives unrestricted sudo or host `/dev`, `/proc`, `/sys`,
or `/run` access.
