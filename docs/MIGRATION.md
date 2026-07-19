# Migration Design

`deck-migrate` is the non-graphical reference implementation for the future
Backup, Restore, Library Import, and Firmware Center screens.

## Bundle separation

- **Private system bundle**: user firmware/BIOS/keys, emulator configs, and saves.
- **ROM bundle**: user game files only, generated and transferred separately.
- **Public release**: schemas, validators, path maps, UI, and placeholder guidance only.

Profiles are versioned JSON so path changes can be migrated between Batocera releases.
The manifest records every logical destination, size, SHA-256, source version, and
symlink. It deliberately contains no file bytes inline.

## Import transaction

1. Validate schema and constrain every destination below `/userdata`.
2. Verify the complete payload before changing the target.
3. Preview categories, changed files, capacity, and conflicts.
4. Back up every replaced destination under `system/config-backups`.
5. Copy to a same-directory temporary file and atomically rename it.
6. Run dependency and emulator-specific validators.
7. Refresh ES only after the transaction succeeds.

Import never deletes target files simply because they are absent from a bundle.
Future releases should add optional encryption, signatures, free-space reservation,
resume journals, per-emulator save maps, and removable-media udev integration.
