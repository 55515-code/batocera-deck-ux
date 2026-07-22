# Contributing

## Secure implementation

New privileged brokers, network services, parsers, update clients, and long-running native
components default to memory-safe Rust. C or C++ additions require a documented hardware,
kernel, ABI, or upstream-integration reason and full hardening/dynamic-analysis evidence.
Python is for unprivileged tools; shell remains small orchestration. Do not invent custom
cryptography or rewrite maintained dependencies without a demonstrated security benefit.
Follow [Secure Implementation](docs/SECURE_IMPLEMENTATION.md) and
[`profiles/secure-implementation-v1.json`](profiles/secure-implementation-v1.json).

Thanks for helping make a friendly, controller-first Batocera experience for Steam
Deck hardware. Small, tested changes are welcome; opening an issue first is useful
for image architecture, update security, storage layout, and user-data migrations.
Participation is governed by the [LuigiOS Community Code](CODE_OF_CONDUCT.md).

## Good first contributions

- Reproduce and document a hardware or controller issue.
- Add an isolated device profile for hardware you physically possess; community
  contributions do not require the core project to promise support for that device.
- Add focused tests around migration, lifecycle, or policy behavior.
- Improve a graphical workflow without adding a terminal-only requirement.
- Package an existing maintained upstream project with pinned source and licensing.
- Improve translations, accessibility, diagnostics, or recovery documentation.

## Pull requests

1. Keep proprietary games, BIOS, firmware, keys, saves, credentials, and private
   migration bundles out of commits, fixtures, logs, screenshots, and Actions artifacts.
2. Prefer established upstream projects and Batocera extension points. Explain why a
   new implementation is needed when no maintained component fits.
3. Include automated tests and the smallest relevant physical-device test record.
4. Describe rollback and migration behavior for persistent `/userdata` changes.
5. Preserve controller-only operation at 1280x800 and on a docked television.
6. For non-Deck device profiles, identify the exact hardware and firmware tested,
   choose an evidence tier, fail closed elsewhere, and state who owns ongoing support.

Run the local gate before opening a pull request:

```bash
./tools/ci-check
```

For image and package work, use the side-by-side [project SDK](sdk/README.md). It
wraps the pinned upstream Batocera Buildroot and official build container.

Commits must include a Developer Certificate of Origin sign-off created with
`git commit -s`. The [DCO](DCO) keeps contribution rights clear without requiring
a separate contributor agreement.

Use draft pull requests early. Maintainers may ask for a design note under `docs/rfcs/`
before accepting a change that alters trust, boot, update, storage, or privilege boundaries.

Contributors are credited through Git history, release notes, and substantial-project
acknowledgements. Use the name you want shown publicly in your Git commit author field and
run `./tools/update-credits` before opening the pull request.
