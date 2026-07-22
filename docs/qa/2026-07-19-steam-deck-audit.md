# Steam Deck Prototype QA - 2026-07-19

Target: Steam Deck LCD, Batocera `44-dev-b96296b988`. All QA probes were
read-only. The active Plasma session was not interrupted by audit agents.

## Release decision

The prototype is suitable for supervised local play and continued development.
It is not ready for redistribution or customer devices. The chroot is a process
packaging convenience, not a security boundary, and the update/rollback path is
not yet reproducible.

## Release blockers

| Priority | Finding | Required exit condition |
| --- | --- | --- |
| P0 | UID 1000 has unrestricted sudo inside a chroot with broad host `/dev`, `/sys`, and `/run` access. | Replace sudo and broad mounts with typed helpers, least-privilege device access, filtered D-Bus, capability dropping, and `NoNewPrivs`. |
| P0 | Flatpak installs succeed but Bubblewrap cannot create a user namespace under the running image policy. | Candidate preflight passes namespace, Bubblewrap, portal, and real GUI launch checks before Discovery is enabled. |
| P0 | Desktop Mode is mutable live state rather than a source-built artifact. | Ship package-owned host integration and a pinned Plasma artifact with digest, SBOM, licenses, current/previous selection, and migration schema. |
| P1 | ES control API and multiple file-sharing services expose a broad LAN surface without an effective firewall policy. | Bind local control to loopback or authenticate it; default remote services off; add a tested firewall profile. |
| P1 | Recovery `status` can mutate the session and stale PID validation is weak. | Make status observational, bind state to PID plus start time, constrain cleanup ownership, and pass fault-injection tests. |
| P1 | No complete, checksummed restore bundle, A/B update, or filesystem snapshot exists; boot reported an unclean FAT volume. | Pass filesystem health, verified rollback, interrupted-update, and graphical recovery tests. |
| P1 | Plasma user-service and Polkit integration log failures. | Pass user-session, authorization-dialog, portal, application lifecycle, and cleanup health checks. |
| P1 | Host system D-Bus and ConnMan access remain broad; CMST is unmaintained prototype glue. | Replace CMST with a typed network broker and native KDE settings client. |
| P1 | The current PCSX2 libretro core recorded an invalid-opcode crash. | Default PS2 to standalone PCSX2 and pass representative launch, exit, save, and resume tests before re-enabling the core. |
| P1 | Fifteen required firmware entries are absent across five systems; 706 checked declarations had no digest mismatches. | Import only user-supplied lawful files, rerun Batocera's validator, and retain an aggregate audit report without private payloads. |
| P1 | 6,881 broken save symlinks are concentrated in one compatibility-prefix root. | Back up the complete save root, identify the stale prefix mapping, dry-run a targeted repair, and verify rollback before changing links. |
| P1 | Nineteen active RPCS3 XML files are malformed, with matching malformed private-bundle copies. | Quarantine only after backup, regenerate from known-good defaults, and validate RPCS3 launch/save behavior. |
| P2 | Plasma exposes nonfunctional NetworkManager and power actions; host ConnMan has no login1-style power contract. | Hide unsupported applets/actions and add typed host network, display, and power brokers. |
| P2 | PowerDevil repeatedly probes inaccessible I2C devices. | Disable nested-session DDC probing or grant only display-associated adapters; never grant blanket I2C access. |
| P2 | Two add-on JSON files are malformed, the unofficial add-on repository is absent, and Flatpak has no configured remote. | Validate configuration schemas and make repository enrollment an explicit, provenance-checked graphical action. |

## Passed invariants

- Desktop Mode remains synchronous under Batocera `emulatorlauncher`.
- Plasma, KWin, CMST, and the controller bridge run as UID 1000.
- Exactly one ConnMan and one WirePlumber policy daemon are active; PipeWire and
  its Pulse protocol server remain host-owned.
- Plasma audio reaches the host speaker sink through a dedicated local socket.
- Returning through the desktop shortcut restores ES audio, and re-entry works.
- Internal userdata and microSD each retained roughly one third free space.
- All 255 system definitions contain required fields; Batocera, ES settings, ES
  input, and two controller profiles parse without duplicate keys or GUIDs.
- Flatpak user and system repair checks completed successfully in dry-run mode.
- The repository CI gate passed before implementation-wave changes.

## Implementation wave

1. Replace ES index-only audio state with stable logical identities, per-stream
   baselines, immediate instance revalidation, and behavioral fake-Pulse tests.
2. Add a non-mutating Flatpak preflight with distinct supported, unsupported,
   and inconclusive results. Never set Bubblewrap setuid or weaken policy.
3. Add deterministic application-entry synchronization with generated-file
   ownership, atomic updates, malformed-entry rejection, and stale cleanup.
4. Source-package the desktop host integration as experimental and disabled by
   default; do not embed the mutable Arch rootfs.
5. Make recovery status observational and bind transactions to PID start time.

## Next gates

- Re-run repository CI and review every generated package file.
- Deploy only reviewed prototype scripts with a complete backup and manifest.
- Repeat launch, late ES stream, desktop sound, ConnMan enumeration, return,
  ES restore, and re-entry tests.
- Run Flatpak preflight as UID 1000 and retain its JSON report.
- Perform physical DualSense reconnect, HDMI hotplug/audio-route, suspend/resume,
  and visible-cursor/OSK tests; these cannot be inferred from process state.
- Re-run the interrupted emulator/data audit only after charging. Investigate
  aggregate firmware gaps, save-link concentration, malformed RPCS3 XML, ROM
  directory-name drift, add-on JSON, and world-writable files without reading,
  hashing, or downloading private game payloads.
- Do not promote an image until P0 findings are closed and P1 risks have owners,
  automated gates, and rollback evidence.
