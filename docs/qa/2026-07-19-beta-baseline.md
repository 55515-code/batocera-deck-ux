# Steam Deck Experimental Beta Baseline - 2026-07-19

Target: Steam Deck LCD at `root@192.168.1.208`. This is an experimental-device
record, not beta qualification.

## Successful read-only preflight

- Hostname: `LUIGIOS`.
- Batocera: `44-dev-b96296b988`, built 2026-07-14.
- Kernel: `7.1.3`.
- SSH: Dropbear active; the device-specific Ed25519 key authenticated successfully.
- Internal userdata: `/dev/nvme0n1p2`, ext4, mounted read-write with about 77 GB free.
- ROM library: `/dev/mmcblk0p1[/batocera/roms]`, ext4, separately mounted at
  `/userdata/roms` with about 336 GB free.
- Source-package desktop enable marker: absent.

The probe changed no remote state. It did not read ROM payloads.

## Follow-up result

After `tools/device-qa` and its safety tests were added, the Deck stopped answering on
port 22. The connection timed out before a remote shell started; the address was absent
from the workstation neighbor cache and `batocera.local` did not resolve. No recovery,
network restart, key deletion, or remote mutation was attempted. Rerun the checked-in
probe after the Deck is awake and connected.

The Deck later returned without intervention. The checked-in probe then passed every
blocking preflight invariant and saved its workstation-side report under ignored `dist/`:

- SSH remained active with two Dropbear processes.
- Internal userdata had 32% free.
- `/userdata/roms` remained a separate removable-device filesystem.
- LuigiOS identity and brand manifests were present.
- The legacy Plasma marker and rootfs were present.
- The source-package desktop marker, COSMIC rootfs, settings app, installed migration
  tool, and backup UI were absent.

The successful probe changed no device state. The device is safe for further supervised,
reversible experimental testing, but it is not beta-ready.

## Decision

Do not deploy the source COSMIC package over the live device. The live prototype is a
mutable Plasma environment, while the reviewed source package expects a provisioned
COSMIC rootfs and an immutable image-owned host integration. The mismatch, incomplete
required brand surfaces, missing settings application, and unrehearsed restore path are
beta blockers.

## Supervised branding pass

After the baseline decision, required LuigiOS assets passed deterministic rendering,
dimension, OLED-black, provenance, and brand-contract checks. They were deployed from
a staging tree with backups and byte-for-byte destination verification. The Game Mode
theme was activated behind an automatic rollback watchdog, EmulationStation restarted,
and a 1280x800 screenshot confirmed readable layout without overlap. A subsequent
read-only probe confirmed SSH, userdata, and the separate SD ROM mount remained healthy.

The Plasma session was launched once through EmulationStation's registered-game API to
validate generic wallpaper ownership and fullscreen presentation, then returned cleanly
to Game Mode. That session is now frozen and is not the product desktop. Directly
invoking `emulatorlauncher` from a plain SSH shell is not a valid desktop QA path because
it lacks the active display transaction.

The decision remains unchanged: the device is a branded Game Mode prototype, not a beta
image. COSMIC must be built from the pinned contract and qualified offline before any
live replacement of the legacy desktop environment.
