# Downstream and OEM Policy

LuigiOS follows **Games first. Your device. Your choices.** Downstreams may build
commercial hardware and services around the project, but LuigiOS does not sell
default placement, sponsored ranking, release trust, or compatibility results.

LuigiOS is intended to be useful beyond the LuigiOS-branded Steam Deck image.
Device makers, repair shops, community distributions, and individual developers
are welcome to adapt it for other gaming hardware, ship commercial products, or
maintain private deployments.

## Permission and branding

- You may fork, modify, redistribute, and sell covered work under its applicable
  open-source license.
- You may remove every LuigiOS name, mark, mascot, and visual asset. LuigiOS does
  not require promotional credit or a "powered by" badge.
- Unbranded or differently branded products must not imply endorsement by the
  LuigiOS project.
- Third-party components keep their own licenses and notices. The repository's
  GPL-3.0 code, corresponding-source obligations, and any asset-specific licenses
  still apply. This policy adds no restrictions and waives no upstream terms.
- LuigiOS trademarks, if established, identify official project releases. They
  do not prevent compatible forks; downstreams should choose a distinct name and
  artwork when presenting a modified image as their own product.

An OEM that removes LuigiOS artwork can use the branding manifest and graphics
audit as a practical checklist for replacing every surface. Brand-neutral APIs,
schemas, tests, and hardware contracts should remain reusable wherever feasible.
Steam Deck remains the LuigiOS reference platform; merging a profile for other
hardware does not imply that core maintainers provide support for that device.

## Accounts and offline use

The vanilla LuigiOS-branded distribution must be deployable and useful without internet
access, a LuigiOS account, or a third-party account. Its shell, local library and play,
device settings, controller setup, backup, restore, reset, and recovery cannot depend on
a remote login.

A downstream may add a proprietary application or service that requires its own account
or network connection. The requirement must be disclosed as belonging to that service,
must be confined to the service, and must not block the vanilla LuigiOS shell or local
device administration. A downstream that makes its entire product account-dependent may
do so where licenses permit, but it must not present that behavior as the vanilla LuigiOS
experience or pass the LuigiOS-branded release qualification gates.

## Optional upstream relationship

Credit, public source links beyond license requirements, and returned patches are
appreciated but are not conditions of collaboration. Downstreams that choose to
work in public can receive practical benefits from the shared project:

- a compatibility entry for tested devices and controller configurations;
- coordinated QA against release candidates and documented regression results;
- links to downstream hardware, images, or support pages from compatibility docs;
- early review of reusable hardware-enablement patches;
- shared issue reproduction and test-matrix coverage; and
- participation in design and packaging discussions on equal technical terms.

Listings are evidence-based, not paid endorsements. Hardware must pass the
published compatibility checks, disclose material limitations, and identify who
provides device support. Security fixes and reproducible test evidence receive
priority regardless of whether a downstream uses LuigiOS branding.

## Healthy downstreams

The preferred relationship is lightweight:

1. Keep a machine-readable record of the upstream commit and local patch set.
2. Publish corresponding source and notices whenever the governing licenses
   require it.
3. Run the LuigiOS compatibility suite and contribute non-sensitive results.
4. Report security issues through `SECURITY.md` before public disclosure.
5. Decide independently whether a change belongs upstream; private changes are
   allowed where their licenses permit them.

This document describes project intent, not legal advice. When it conflicts with
a component's license, the component license controls.
