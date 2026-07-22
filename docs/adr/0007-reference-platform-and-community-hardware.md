# ADR 0007: Reference Platform and Community Hardware

Status: accepted product direction

## Context

The project creator's core development device is a Steam Deck. That physical
access makes the Deck the only honest baseline for day-to-day integration and
release qualification. LuigiOS should still be useful to developers working on
other handhelds, mini PCs, and gaming devices, but accepting their profiles or
test reports must not imply that core maintainers own hardware they cannot test
or promise ongoing support they cannot provide.

## Decision

Steam Deck is the LuigiOS **reference platform** and core release gate. This is
a platform direction, not a blanket claim that every Deck revision, dock,
firmware version, accessory, or storage configuration has passed every release.
Each material variant still requires identified evidence.

Hardware integration remains capability-driven and profile-based. Contributors
may add isolated device detection, controller, display, audio, power, storage,
thermal, suspend, recovery, and image configuration for hardware they possess.
A profile may be merged when it is testable, fails closed on other devices, has
rollback or removal behavior, and does not regress the reference platform. Core
acceptance does not transfer support ownership to LuigiOS.

The machine-readable policy is
[`profiles/hardware-support-v1.json`](../../profiles/hardware-support-v1.json).

## Evidence tiers

- **Reference**: core-maintained, physically available, and release-blocking
  within the explicitly documented configuration scope.
- **Community-tested**: a current report exists for a precise image digest and
  hardware tuple. Results are useful evidence but carry no support promise.
- **Downstream-maintained**: a named project or vendor owns the profile and
  support relationship. Sold devices require a public support contact.
- **Experimental**: enablement exists but evidence or maintenance continuity is
  incomplete. It is non-blocking and may regress.
- **Unverified**: no compatibility claim is made.

Listings show the tier, image digest, hardware revision, firmware version,
evidence date, limitations, and responsible support party. A report for one
model never implies support for a family. Listings age out when material changes
make their evidence stale.

## Contribution boundary

Device contributors do not need to donate hardware or commit to indefinite
maintenance. They should identify the hardware they actually tested, submit the
smallest reusable profile, and state whether they will remain a contact. If no
maintainer remains, the profile can stay experimental when it is isolated and
does not burden reference releases, or be retired when it becomes unsafe.

Core maintainers may help review architecture, reproduce shared-layer bugs, and
upstream reusable work. They may decline device-specific release blocking,
support requests, emergency fixes, or compatibility claims without access to
the affected hardware.

## User communication

Use tiered, evidence-based language instead of an unqualified "supported" badge.
Compatibility entries are not certification, warranty, endorsement, or a promise
of future releases. Downstreams selling hardware remain responsible for their
customers, warranties, regulatory obligations, and bundled image.
