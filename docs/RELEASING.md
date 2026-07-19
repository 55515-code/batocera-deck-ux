# Release Process

Development source milestones are built reproducibly with `./tools/release-source`.
Their manifest explicitly identifies them as contributor source, not an end-user image.

1. Freeze source dependencies and regenerate license, SBOM, provenance, and notices.
2. Build twice in independent clean environments and compare intended artifacts.
3. Run CI, candidate-image tests, migration tests, update fault injection, and rollback.
4. Publish one immutable candidate digest and collect signed hardware test reports.
5. Review open security, data-loss, controller, display, boot, and recovery blockers.
6. Promote the exact digest by updating threshold-signed channel metadata.
7. Publish release notes, known issues, support window, recovery image, and source offer.
8. Seed only TUF-authorized public update objects; verify HTTPS/OCI fallback independently.

Stable promotion requires at least two release-authority approvals once multiple
maintainers exist. Signing ceremonies and revocation drills must use the documented
offline-key runbook; CI credentials cannot authorize stable releases alone.
