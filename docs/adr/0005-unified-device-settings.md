# ADR 0005: Unified Device Settings

Status: proposed

## Context

Batocera already provides controller-aware settings through EmulationStation, command-line
wrappers, `batocera-settings`, configgen, and the newer XML-driven
`batocera-controlcenter`. LuigiOS needs a deeper, searchable settings application
without creating a competing configuration database or exposing root shell commands to a UI.

## Decision

Extend upstream `batocera-controlcenter` as the shared UI and input foundation. Preserve its
quick overlay for in-game controls and add a separate full-screen **Device Settings** mode for
administration. Both modes use the same visual components, controller focus rules, touch and
keyboard support, localization, and 1280x800/television layout tests.

Settings are declared in a versioned registry. A typed host broker exposes reviewed providers
for state, validation, mutation, progress, cancellation, and rollback. Registry entries name a
provider operation and typed arguments; they cannot contain shell, executables, or arbitrary
paths. The broker maps operations to existing Batocera facilities:

- `batocera-settings` and mini_settings for durable product configuration.
- Batocera networking and ConnMan wrappers for Wi-Fi and network state.
- BlueZ and Batocera controller wrappers for pairing and device management.
- Existing audio, display, configgen, emulator, storage, update, and service interfaces.
- Deck-owned recovery, migration, restore-point, and trusted-vault brokers.

The initial information architecture is Home, Network, Bluetooth and Controllers, Display and
Audio, Gaming and Emulation, Storage, Desktop and Apps, Updates, Backup and Restore, Trusted
Vaults, Privacy and Security, Accessibility, About and Diagnostics, and Developer Mode.
Developer controls are hidden until deliberately enabled and never weaken update verification.

## Interaction Contract

Every value has a type, current state, default, validation rule, search terms, and source of
truth. Mutations declare whether they are privileged, disruptive, reversible, or require a UI
restart, session restart, game restart, or reboot. The confirmation page explains impact before
disruptive operations. Long-running work reports progress and survives navigation.

Pending changes remain visible. Reversible changes offer undo; risky storage, reset, or update
operations create or require a restore point where supported. A failed mutation returns a
stable error code and recovery action, not terminal output. Offline, unavailable hardware, and
read-only filesystem states have explicit UI representations.

Controller focus and back behavior must be deterministic. The same action mapping works with
the built-in Deck controls and an external controller after reconnect. Touch targets, text
scaling, screen-reader labels, contrast, and reduced motion are part of acceptance testing.

## Security Boundary

The UI runs unprivileged. The broker authenticates the local session, allowlists every
operation, validates all arguments again, and records security-sensitive changes without
logging secrets. It receives narrowly scoped privilege rather than unrestricted sudo. Raw BIOS,
firmware, keys, credentials, ROM paths, and arbitrary emulator configuration are not exposed
through generic setting providers.

Third-party pages cannot register privileged operations. Add-ons may link to their own
unprivileged UI and publish read-only status through a documented extension contract. Provider
compatibility is versioned so an unavailable or mismatched provider disables its page cleanly.

## Delivery

`profiles/settings-registry-v1.json` is the first machine-readable navigation and policy
contract. The next implementation slice should add a read-only provider adapter and render the
Home, Network, Controllers, Storage, Updates, and Recovery pages before enabling mutations.
Upstreamable UI and accessibility changes should remain separable from Deck-specific providers.
