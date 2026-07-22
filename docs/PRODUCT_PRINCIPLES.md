# Product Principles

**Games first. Your device. Your choices.**

## 1. The handheld comes first

The product is a dependable, attractive SteamOS alternative built around Batocera's
excellent console experience. A person should be able to install it, add lawful content,
manage storage, pair controllers, enter a full COSMIC desktop, update, repair, reset, and
restore the device without knowing Linux or opening a terminal.

- Controller-only workflows are complete; touch and keyboard are enhancements.
- Gaming Mode is immediate, readable, and calm on the Deck and a television.
- Desktop Mode feels integrated, returns reliably, and never leaks over games.
- Destructive actions explain impact, preview affected data, and offer recovery.
- Defaults are conservative; advanced controls reveal detail without cluttering basics.
- Hardware support is capability-driven so contributors can add other handhelds cleanly.
- Steam Deck is the core reference platform and release gate. Other devices may carry
  community or downstream evidence without implying core-project support ownership.
- A feature is not polished until loading, empty, offline, interrupted, and failure states
  are designed and tested.

The quality bar is a dedicated game console: coherent visual language, predictable input,
fast recovery, and no requirement that the owner become the system administrator.

## 1a. Simple by default, open by choice

The factory experience is Gamer Mode: one controller-first app library, one unified
settings experience, task-oriented language, safe presets, and no requirement to
understand packages, services, mount paths, root, or terminals. It should be approachable
enough for a child to use while retaining clear confirmations and optional owner controls.

Developer Mode is an intentional, reversible progressive-disclosure switch. It reveals
development applications, terminals, raw diagnostics, filesystem detail, and unsupported
controls while preserving the graphical workflows and security invariants of Gamer Mode.
It never silently enables itself or disables signed updates. The complete contract is
[ADR 0006](adr/0006-progressive-disclosure-and-developer-mode.md).
Reference-platform and third-party hardware boundaries are defined in
[ADR 0007](adr/0007-reference-platform-and-community-hardware.md).

## 2. Peers carry the community

Public OS images, updates, extensions, configuration packs, artwork made for distribution,
and public documentation archives should be content-addressed and retrievable from peers.
Small project origins may bootstrap availability, but the system must continue working as
individual mirrors disappear.

Decentralized transport does not decentralize trust accidentally. TUF threshold roles
authorize base OS releases; delegated community catalogs authorize narrower namespaces;
every reconstructed artifact is verified before use. Personal ROMs, firmware, BIOS, saves,
credentials, and migration bundles never enter the public object network.

## 3. Sustainable stewardship

The project is designed for a part-time lead, automation, and trusted community maintainers.
Documentation, tests, provenance, and release records are product features. Routine work is
automated, consequential changes receive human review, and permissions remain narrow.

Existing, maintained community software is preferred over local reinvention. Integrations
pin source, preserve upstream attribution and licenses, expose clean rollback, and remain
replaceable. AI tools may prepare research, code, tests, and reviews, but signed releases and
high-impact merges require accountable human approval and reproducible evidence.

## 4. The player owns the experience

LuigiOS serves the person using the device rather than a storefront, hardware vendor,
publisher, analytics system, or project account. Local play and administration work
offline. The OS has no mandatory account, subscription, advertising, sponsored ranking,
forced storefront, or telemetry enabled by default. Optional network services identify
their owner and terms before handoff.

The vanilla LuigiOS-branded distribution must remain deployable and usable without an
internet connection or login. Network setup is skippable, and local first boot, library
import, play, settings, controller setup, backup, restore, reset, and recovery remain
available offline. A proprietary downstream application or optional third-party service
may require its own account or network connection, but that requirement is scoped to the
service and cannot gate the vanilla shell or local administration.

Player control includes choosing optional software sources, exporting saves and settings,
removing add-ons, declining peer distribution and diagnostics upload, restoring or resetting
the device, and intentionally enabling Developer Mode. This does not erase the rights of
artists, game developers, upstream projects, or service operators: attribution, licenses,
security boundaries, and lawful distribution remain explicit.

Commercial contributors use the same QA and release-trust path as everyone else. No paid
relationship may silently change defaults, rank software, bypass signatures, or make an
external service compulsory. The complete language and ownership contract is
[LuigiOS Identity and Voice](IDENTITY_AND_VOICE.md).

The original interaction and visual rules are defined in
[LuigiOS Interface Guidelines](INTERFACE_GUIDELINES.md) and the machine-readable
[`profiles/interface-guidelines-v1.json`](../profiles/interface-guidelines-v1.json).
