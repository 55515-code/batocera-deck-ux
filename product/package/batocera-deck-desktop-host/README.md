# Experimental desktop host package

`BR2_PACKAGE_BATOCERA_DECK_DESKTOP_HOST` installs only the Batocera-side
integration for Desktop Mode. It is disabled unless a product defconfig selects
it, and the launcher remains disabled until the image owner creates
`/userdata/system/configs/batocera-deck-desktop.enabled` after qualification.

The package owns its launch scripts, runtime service, PipeWire endpoint policy,
ConnMan D-Bus prototype policy, controller bridge, Ports entry, and file
manifest. Buildroot installs these files directly into the immutable image. No
boot-time service copies configuration from userdata into the live root.

The Plasma filesystem is a separate, reproducibly built artifact and is not
downloaded or embedded here. This package currently checks for a provisioned
filesystem at `/userdata/system/containers/arch-plasma/rootfs` and fails closed
when it is absent.

## Rollback boundary

`files/package-files.manifest` is the authoritative package-owned path list.
Rollback is performed by selecting a previous complete OS image, not by deleting
paths from a running immutable root. The manifest supports image-delta review,
package removal checks, and verification that a previous image no longer owns
these paths. Persistent desktop home data is outside this package and requires a
separate versioned migration and rollback policy.

## Security status

The current nested chroot is not a security boundary. The package avoids broad
recursive mounts of host `/run`, `/dev`, and `/sys`, launches Plasma as UID 1000
with `no_new_privs`, and keeps the controller bridge on the host. The temporary
ConnMan policy still grants more access than the intended typed settings broker;
therefore this package must remain experimental.
