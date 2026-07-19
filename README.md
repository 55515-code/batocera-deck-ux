# LuigiOS

LuigiOS is an early Steam Deck-focused Batocera derivative project.
It adds controller-first desktop, storage, migration, validation, recovery, and
update experiences without distributing games, BIOS files, console firmware,
keys, or other proprietary payloads.

Current milestone: `0.1.0-dev.1`, a contributor source preview rather than an
installable end-user OS image. See the [changelog](CHANGELOG.md).

The project's priorities are [console-grade handheld UX, trusted peer distribution,
and sustainable community stewardship](docs/PRODUCT_PRINCIPLES.md), in that order.

The repository is split into three layers:

- `product/`: reproducible image and package integration (planned).
- `tools/`: testable host-side services and migration logic.
- `ui/`: graphical, controller-first clients of those services (planned).

User-owned data is always separate. `deck-migrate` creates private bundles for
firmware/config/save state and separate ROM bundles. Bundle payloads and local
manifests are ignored by Git and must never be committed or shipped.

Architecture and current status are documented in [Product Architecture](docs/ARCHITECTURE.md),
[Secure Distribution](docs/DISTRIBUTION.md), [Roadmap](docs/ROADMAP.md), and
[Live Prototype State](docs/LIVE_PROTOTYPE.md).

The versioned [LuigiOS brand system](branding/README.md) coordinates boot, Game Mode,
Plasma, settings, recovery, Steam handoff, icons, wallpapers, motion, and audio cues.
`./tools/brandctl validate --require-ready` is the asset-readiness gate; demo deployment
is transactional and keeps a complete backup under `/userdata/system/backups`.

The planned unified graphical settings experience extends Batocera's existing controller
control center through a typed, least-privilege provider API. Its navigation and safety
contract are documented in [ADR 0005](docs/adr/0005-unified-device-settings.md).

The enforceable distribution defaults live in
[`profiles/distribution-v1.json`](profiles/distribution-v1.json). They keep release
authorization separate from P2P transport and confine seeding to a dedicated cache.

The default image includes the independent GPL-3.0 Batocera Unofficial Add-Ons
store as an explicit, user-launched community software source. Its application is
pinned and hash-checked; catalog payloads remain outside the signed base OS. See
[Third-Party Software](THIRD_PARTY.md).

Contributors can start with [Contributing](CONTRIBUTING.md), then use the focused
issue forms and pull-request checklist. The complete local validation gate is
`./tools/ci-check`; product-level expectations are in [Testing](docs/TESTING.md).
Image contributors use the side-by-side [project SDK](sdk/README.md), which wraps
Batocera's pinned Buildroot source and official build container.

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
