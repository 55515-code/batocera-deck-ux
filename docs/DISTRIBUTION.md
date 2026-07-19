# Secure Community Distribution

Peers provide storage and bandwidth. They do not decide what software is trusted.
The Update Framework (TUF) is the sole release authority; every transport is an
untrusted source of bytes that must match TUF-authorized SHA-256 digests.

## Recommended stack

1. TUF delegates `steamdeck/stable`, `candidate`, `beta`, and `testing` channels.
2. Reproducible Buildroot jobs produce one immutable artifact per source commit.
3. Content-defined, independently compressed chunks maximize cross-release reuse.
4. BitTorrent v2 distributes chunk objects through peers, trackers, PEX, and
   optional DHT; HTTPS web seeds and OCI/static origins guarantee a fallback.
5. in-toto/SLSA provenance, SBOMs, and Sigstore bundles describe how the artifact
   was built. TUF threshold signatures still authorize channel installation.
6. The updater reconstructs and verifies the final image before staging it into
   an inactive Batocera A/B boot slot.

Primary specifications: [TUF](https://theupdateframework.github.io/specification/latest/),
[BEP 52](https://www.bittorrent.org/beps/bep_0052.html),
[BEP 19 web seeds](https://www.bittorrent.org/beps/bep_0019.html),
[OCI Distribution](https://github.com/opencontainers/distribution-spec),
[SLSA provenance](https://slsa.dev/spec/v1.2/build-provenance), and
[Sigstore bundles](https://docs.sigstore.dev/about/bundle/).

The initial protocol decision and reasons for deferring a second IPFS/libp2p data plane
are recorded in [ADR 0001](adr/0001-peer-distribution-stack.md). I2P remains a possible
opt-in privacy profile, not a claim that ordinary torrenting is anonymous.

## Trust and channels

- Embed the first TUF root in the factory image.
- Keep root and stable threshold keys offline and geographically separated.
- Give testing CI a narrowly delegated online key that cannot promote stable.
- Promote one artifact digest between channels; never rebuild on promotion.
- Persist monotonic metadata versions, security epoch, and channel sequence.
- Require a physical confirmation and recovery delegation for intentional downgrade.
- If metadata is expired or unavailable, continue booting the installed known-good
  release but do not install new software.

## Privacy modes

- **Off**: HTTPS/OCI only.
- **Private swarm**: project tracker, PEX, and hole punching; public DHT disabled.
- **Public swarm**: DHT enabled after a clear IP-address/privacy warning.

P2P is opt-in, quota-limited, disabled on battery and metered networks by default,
and never anonymous. Peer IDs rotate by swarm. No hardware serial, account,
telemetry identifier, or stable installation identifier enters peer discovery.

The seeder has access only to a dedicated update-object cache. It must never scan,
hash, announce, or serve `/userdata/roms`, `/userdata/bios`, private migration
bundles, saves, keys, firmware dumps, or arbitrary user files.

The initial machine-readable contract is
[`profiles/distribution-v1.json`](../profiles/distribution-v1.json). CI treats its
trust boundary, private-path exclusions, safe network defaults, and A/B recovery
requirements as invariants. Production confinement must additionally use a dedicated
unprivileged service account, mount namespace, read-only root, and a writable bind
mount containing only the update-object cache.

Community variants are signed catalogs of public configuration and extension objects,
not replacement trust roots. A variant may select a theme, controller profile, emulator
defaults, or optional package set, but it cannot weaken channel signatures, add a
seeding root, access private migration bundles, or silently replace the base OS.

## Batocera integration

Keep Batocera's Buildroot, SquashFS, configgen, ES, and `/userdata` model. Do not
install `bootc`, RPM-OSTree, DNF, or a Fedora updater inside Batocera. Borrow the
image lifecycle properties demonstrated by uBlue: build once, promote by digest,
stage before reboot, retain a known-good deployment, and expose rollback graphically.

Extend these upstream areas:

- `post-image-script.sh`: deterministic artifacts, hashes, provenance, slot image.
- GRUB/create-boot scripts: A/B slot selection and pending-attempt counters.
- initramfs: selected-slot mount, reset markers, and automatic fallback.
- `batocera-upgrade`: embedded updater only, TUF verification, inactive-slot staging.
- `batocera-upgrade-torrent`: signed torrent discovery, web seeds, quotas, digest gate.
- EmulationStation update GUI/API: channels, stage status, rollback, reset, P2P policy.
- late SysV health service: commit a pending slot only after storage and ES are healthy.

The current path that can fetch and execute an updater script from a moving GitHub
branch must be removed from the signed derivative.
