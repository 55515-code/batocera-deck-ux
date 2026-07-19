# ADR 0002: Btrfs User-Data Restore Points

Status: proposed

## Context

Batocera already supports a Btrfs SHARE filesystem on x86_64, includes `btrfs-progs`,
loads the Btrfs kernel module, and applies optional compression. It does not currently
organize `/userdata` into a restore-point product or expose snapshot lifecycle controls.

Btrfs snapshots are not backups, do not recursively include nested subvolumes, and can
retain substantial changed data. Copy-on-write metadata can also produce ENOSPC before a
simple free-space display reaches zero. Restore behavior must account for all three facts.

## Proposed Product Model

The Storage and Recovery UI offers **Restore Points** only on compatible Btrfs layouts.
It remains distinct from immutable OS update rollback and from external backup:

- OS rollback selects a prior signed A/B system image.
- Restore points revert selected local configuration and user-data subvolumes quickly.
- Backup copies verified data to another device and survives internal-drive failure.

The managed layout uses explicit subvolumes for configuration, saves, firmware/BIOS,
artwork, and optional ROM libraries. Downloads, caches, swap, update objects, containers,
and temporary files are excluded. ROM snapshots are off by default because large mutable
disc images can pin unexpected space. Existing flat SHARE filesystems require a journaled,
power-loss-tested migration with a free-space preflight; no in-place conversion is silent.

## UX Contract

- Manual named restore points with description, scope, estimated retained space, and date.
- Automatic pre-update, pre-import, pre-reset, and pre-risky-setting restore points.
- A simple default retention policy plus an advanced space budget and pin control.
- File-level browsing/recovery and whole-scope restore previews.
- Low-space warnings based on Btrfs allocation/metadata, not only `df`.
- Restore runs as an offline or quiesced transaction with a recovery marker and rollback.
- Every screen states that restore points are not a substitute for an external backup.

## Implementation Direction

Use upstream `btrfs-progs` for snapshot, subvolume, qgroup, send/receive, and scrub
operations behind the same narrow privileged broker as Storage and Recovery. Evaluate
Snapper's proven retention/configuration behavior before implementing policy logic, but do
not ship a desktop-oriented frontend or pull in a second privilege architecture merely to
gain a scheduler. The GUI consumes a versioned API and never constructs shell commands.

Read-only snapshots intended for replication remain read-only. External Btrfs backup may
later use incremental `btrfs send`, but `btrfs receive` accepts only locally authenticated
backup streams in an isolated destination; untrusted network send streams are forbidden.

## Qualification

Tests must cover nested subvolumes, open emulator databases, interrupted create/delete,
metadata pressure, full disk, qgroup rescan, snapshot pruning, suspend during work, power
loss during restore, ext4 fallback, external backup, and recovery when the normal UI cannot
boot. Snapshot actions are blocked while a game or desktop transaction cannot quiesce.
