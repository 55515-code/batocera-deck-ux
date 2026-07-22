# Beta Qualification

LuigiOS remains an experimental development build until every gate in
`profiles/beta-qualification-v1.json` passes on a source-built candidate image.
Passing isolated tests on the creator's Deck does not promote the project by itself.

## Remote device discipline

`tools/device-qa` is the first and last step of every supervised SSH session. Its
remote probe is read-only. A deployment must preserve the active SSH process and
Dropbear configuration, must not restart networking, and must have a timed automatic
rollback before changing a session launcher. Changes are staged only under the policy's
allowed roots and are promoted by atomic rename after local CI and a remote dry-run pass.

The following roots are hard deployment exclusions: `/userdata/roms`, `/media`, and
`/boot`. General-purpose `rsync --delete`, recursive ownership changes, filesystem tools,
partitioning tools, and package-manager mutation are forbidden in a remote deployment.

Run the baseline probe from the development workstation:

```bash
./tools/device-qa \
  --host root@192.168.1.208 \
  --identity-file ~/.ssh/batocera_192_168_1_208_ed25519 \
  --output dist/device-qa/latest.json
```

## Beta entry definition

Beta begins only when a reproducible image provides all required LuigiOS art surfaces,
a reliable unprivileged desktop, the graphical settings application, verified backup and
migration workflows, and image rollback. Desktop qualification includes handheld and HDMI
fullscreen behavior, built-in and DualSense input, visible cursor, OSK, sound, networking,
Flatpak GUI launch, suspend/reconnect, and clean return to Game Mode.

No prototype marker, mutable container, or manually repaired live state counts as a beta
artifact. The settings registry alone does not count as a settings application. Backup
export alone does not pass: restore must be rehearsed into a disposable target and its
result verified before the creator's Deck is reinstalled.

Source qualification is the reproducible starting point, not beta entry. The
`source-qualification-v1` report proves that one clean Git tree passed the authoritative
source gate with immutable upstream and container pins. It explicitly records false for
image, hardware, and beta qualification until separately bound candidate-image and device
evidence exist.

## Fresh-install rehearsal

Fresh installation is a post-beta operation, not a shortcut to reach beta.

1. Record the internal disk and ROM SD source, filesystem type, size, and filesystem UUID.
2. Export the private system profile to an external destination. This includes owned
   firmware, emulator settings, and saves, but excludes `/userdata/roms`.
3. Verify every bundle checksum and perform a restore rehearsal into a disposable target.
4. Shut the Deck down and physically remove the ROM SD card.
5. Install only to the verified internal target, then boot and rerun device QA.
6. Reinsert the ROM SD card only after the new system is stable. Never initialize, format,
   repair, relabel, or repartition it as part of import.
7. Compare the SD filesystem UUID, type, and capacity with the recorded baseline before use.
   On mismatch, stop. Mount the existing filesystem without formatting.
8. Dry-run and then apply the verified private-system restore. Back up every replacement.
9. Point the library at the existing SD ROM tree and refresh metadata. Do not copy, rename,
   normalize, deduplicate, or delete ROM files during initial import.
10. Complete the full reference-device regression suite before calling the redeploy usable.

The ROM SD card is an existing user-data source, never installation media or disposable
workspace. Physical removal during installation is the primary protection against choosing
the wrong block device; software path checks are secondary safeguards.
