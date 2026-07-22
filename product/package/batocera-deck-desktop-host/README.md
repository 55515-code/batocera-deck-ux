# Experimental desktop host package

`BR2_PACKAGE_BATOCERA_DECK_DESKTOP_HOST` installs only the Batocera-side
integration for Desktop Mode. It is disabled unless a product defconfig selects
it, and the launcher remains disabled until the image owner creates
`/userdata/system/configs/batocera-deck-desktop.enabled` after qualification.

The package owns its launch scripts, runtime service, PipeWire endpoint policy,
ConnMan D-Bus prototype policy, controller bridge, Ports entry, and file
manifest. Buildroot installs these files directly into the immutable image. No
boot-time service copies configuration from userdata into the live root.

The COSMIC filesystem is a separate, reproducibly built artifact and is not
downloaded or embedded here. This package currently checks for a provisioned
filesystem at `/userdata/system/containers/arch-cosmic/rootfs` and fails closed
when it is absent.

Build it on a workstation with `./tools/build-cosmic-image build --apply`. The
builder uses the immutable OCI digest and dated Arch Linux Archive snapshot in
`sdk/versions.env`, emits exact package inventory and SPDX files, runs the COSMIC
preflight, and writes only to ignored `dist/cosmic`. Building does not deploy or
enable Desktop Mode on a device.

## Rollback boundary

`files/package-files.manifest` is the authoritative package-owned path list.
Rollback is performed by selecting a previous complete OS image, not by deleting
paths from a running immutable root. The manifest supports image-delta review,
package removal checks, and verification that a previous image no longer owns
these paths. Persistent desktop home data is outside this package and requires a
separate versioned migration and rollback policy.

## Security status

The current nested chroot is not a security boundary. The package avoids broad
recursive mounts of host `/run`, `/dev`, and `/sys`, launches COSMIC as UID 1000
with `no_new_privs`, and keeps the controller bridge on the host. The temporary
ConnMan policy still grants more access than the intended typed settings broker,
and the COSMIC image intentionally excludes the unofficial CMST package. Network
controls remain a release blocker until the typed broker and native LuigiOS
settings page are present; therefore this package must remain experimental.

The host controller bridge remains a small C boundary because it integrates directly
with Batocera's SDL2 controller ABI and Linux input/uinput interfaces. It owns no network
or artifact parsing, compiles warning-clean with stack protection and PIE, and links with
full RELRO, immediate binding, and a non-executable stack. New privileged brokers and
network services follow `docs/SECURE_IMPLEMENTATION.md` and default to memory-safe Rust;
future replacement of this bridge should be evaluated when a maintained Rust SDL/input
integration reduces risk without regressing controller support.
