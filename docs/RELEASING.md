# Release Process

Development source milestones are built reproducibly with `./tools/release-source`.
Their manifest explicitly identifies them as contributor source, not an end-user image.
Pushing a matching `v$(cat VERSION)` tag creates a draft source release; a maintainer must
inspect and publish it. See [Maintainer Setup](MAINTAINER_SETUP.md).

Every candidate source revision first produces a clean-tree qualification bundle with
`./tools/qualify-source run`. Verify downloaded CI evidence with
`./tools/qualify-source verify --detached PATH`; detached verification proves the report/log
binding, while verification in the source checkout additionally requires the exact commit,
tree, and dependency pins. Source qualification never substitutes for the two clean image
builds and reference-device tests below.

Experimental builds cannot be labeled beta until all gates in
`profiles/beta-qualification-v1.json` pass on the exact candidate artifact. A fresh
install of the creator's Deck happens only after beta entry, verified non-ROM backup,
and a restore rehearsal; the existing ROM SD card is physically removed during install.

1. Freeze source dependencies and regenerate license, SBOM, provenance, and notices.
   Validate the canonical LuigiOS name, tagline, and player-control contract against
   `profiles/product-identity-v1.json`; distinguish every third-party service and mark.
   Prove the vanilla image completes deployment, local first boot, play, settings, backup,
   reset, and recovery with networking unavailable and no account configured. Validate
   `profiles/interface-guidelines-v1.json` and its proprietary-trade-dress review evidence.
   Validate `profiles/secure-implementation-v1.json`, native hardening evidence, dependency
   audit, sanitizer results, fuzz coverage, and documented unsafe/FFI exceptions.
2. Build twice in independent clean environments and compare intended artifacts.
3. Run CI, candidate-image tests, migration tests, update fault injection, and rollback.
4. Publish one immutable candidate digest and collect signed hardware test reports.
   Steam Deck reference failures are release-blocking within the declared test scope;
   other-device reports retain their community, downstream, experimental, or unverified tier.
5. Review open security, data-loss, controller, display, boot, recovery, privacy, and
   product-identity blockers. Paid placement, sponsorship, OEM requests, and store
   relationships cannot override test evidence or release authority.
6. Promote the exact digest by updating threshold-signed channel metadata.
7. Publish release notes, known issues, support window, recovery image, and source offer.
8. Seed only TUF-authorized public update objects; verify HTTPS/OCI fallback independently.

Stable promotion requires at least two release-authority approvals once multiple
maintainers exist. Signing ceremonies and revocation drills must use the documented
offline-key runbook; CI credentials cannot authorize stable releases alone.
