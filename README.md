# LuigiOS

**Games first. Your device. Your choices.**

LuigiOS is an early Steam Deck-focused Batocera derivative project.
It adds controller-first desktop, storage, migration, validation, recovery, and
update experiences without distributing games, BIOS files, console firmware,
keys, or other proprietary payloads.

Steam Deck is the creator's core development device and LuigiOS reference platform.
The architecture welcomes isolated profiles and test evidence for other hardware without
promising core-project support; those relationships use explicit evidence and maintenance
tiers defined by [ADR 0007](docs/adr/0007-reference-platform-and-community-hardware.md).

Current milestone: `0.1.0-dev.1`, a contributor source preview rather than an
installable end-user OS image. See the [changelog](CHANGELOG.md).
The current channel is **experimental**. Promotion to beta requires every gate in
the [Beta Qualification](docs/BETA_QUALIFICATION.md) contract, including complete
theming, a tested desktop and settings app, verified backup and migration, and a
reference-device regression pass.

The project's priorities are [console-grade handheld UX, trusted peer distribution,
and sustainable community stewardship](docs/PRODUCT_PRINCIPLES.md), in that order.
Its [identity and voice](docs/IDENTITY_AND_VOICE.md) put simple game playing and
device ownership in the hands of the person holding the controller: no mandatory
LuigiOS account, advertising, sponsored ranking, forced storefront, or telemetry
enabled by default.

The repository is split into three layers:

- `product/`: Buildroot packages and pinned desktop-image integration.
- `tools/`: testable host-side services and migration logic.
- `ui/`: graphical, controller-first clients of those services (planned).
- `profiles/`: machine-readable product, interface, trust, and compatibility contracts.

The [LuigiOS Interface Guidelines](docs/INTERFACE_GUIDELINES.md) define the original
controller-first visual system, offline vanilla experience, and optional third-party
service boundaries.
The [Secure Implementation Policy](docs/SECURE_IMPLEMENTATION.md) defines memory-safe
language defaults, native hardening, least privilege, and security verification for
LuigiOS-authored code.

User-owned data is always separate. `deck-migrate` creates private bundles for
firmware/config/save state and separate ROM bundles. Bundle payloads and local
manifests are ignored by Git and must never be committed or shipped.

Architecture and current status are documented in [Product Architecture](docs/ARCHITECTURE.md),
[Secure Distribution](docs/DISTRIBUTION.md), [Roadmap](docs/ROADMAP.md), and
[Live Prototype State](docs/LIVE_PROTOTYPE.md).

The versioned [LuigiOS brand system](branding/README.md) coordinates boot, Game Mode,
COSMIC, settings, recovery, Steam handoff, icons, wallpapers, motion, and audio cues.
`./tools/brandctl validate --require-ready` is the asset-readiness gate; demo deployment
is transactional and keeps a complete backup under `/userdata/system/backups`.
The first original marks, semantic icons, boot stills, and caretaker-network
wallpapers are governed by the [art direction](branding/ART_DIRECTION.md) and
reproduced with `./tools/render-brand-assets`.

The planned unified graphical settings experience extends Batocera's existing controller
control center through a typed, least-privilege provider API. Its navigation and safety
contract are documented in [ADR 0005](docs/adr/0005-unified-device-settings.md).
LuigiOS resets into a console-like Gamer Mode and intentionally reveals terminals,
raw diagnostics, and unsupported controls through a reversible Developer Mode. The
progressive-disclosure contract is [ADR 0006](docs/adr/0006-progressive-disclosure-and-developer-mode.md).

The enforceable distribution defaults live in
[`profiles/distribution-v1.json`](profiles/distribution-v1.json). They keep release
authorization separate from P2P transport and confine seeding to a dedicated cache.
The player-first product contract lives in
[`profiles/product-identity-v1.json`](profiles/product-identity-v1.json), and the
Gamer/Developer Mode boundary lives in
[`profiles/experience-modes-v1.json`](profiles/experience-modes-v1.json). CI checks
these policies alongside the public documentation so naming and user-control promises
cannot drift silently.

The default image includes the independent GPL-3.0 Batocera Unofficial Add-Ons
store as an explicit, user-launched community software source. Its application is
pinned and hash-checked; catalog payloads remain outside the signed base OS. See
[Third-Party Software](THIRD_PARTY.md).

Contributors can start with [Contributing](CONTRIBUTING.md), then use the focused
issue forms and pull-request checklist. The complete local validation gate is
`./tools/ci-check`; product-level expectations are in [Testing](docs/TESTING.md).
`./tools/sdk qualify` runs that gate from a clean revision and creates a verifiable,
commit-bound source evidence bundle without mislabeling source QA as image or hardware
qualification.
Image contributors use the side-by-side [project SDK](sdk/README.md), which wraps
Batocera's pinned Buildroot source and official build container.
The [community launch kit](community/README.md) defines Discord, Reddit, moderation,
and onboarding without allowing chat services to replace durable GitHub decisions.
The [downstream and OEM policy](DOWNSTREAM.md) welcomes unbranded and commercial
forks without requiring promotional credit, while preserving each component's
actual open-source license obligations.

Project-authored code and documentation are licensed under GPL-3.0. Third-party
components retain the licenses recorded in [Third-Party Software](THIRD_PARTY.md).
Project and upstream acknowledgements are maintained in [Credits](CREDITS.md).

## Migration quick start

Preview the private system bundle:

```bash
python3 tools/deck_migrate.py export \
  --profile profiles/private-system-v1.json \
  --output /userdata/backups/my-deck-private --dry-run
```

Create it after reviewing the size and source list:

```bash
python3 tools/deck_migrate.py export \
  --profile profiles/private-system-v1.json \
  --output /userdata/backups/my-deck-private
```

Verify or import on a fresh Deck:

```bash
python3 tools/deck_migrate.py verify /path/to/my-deck-private
python3 tools/deck_migrate.py import /path/to/my-deck-private --dry-run
python3 tools/deck_migrate.py import /path/to/my-deck-private --apply
```

Every changed destination is backed up before replacement. Import is additive:
it does not delete files absent from the bundle.
