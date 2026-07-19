# Maintainer Setup

The repository is intentionally usable by one maintainer without bypassing its validation
gate. Protect `main` with the `validate` status check, conversation resolution, force-push
protection, and deletion protection. Do not require an approving review until a second active
maintainer exists; doing so would make routine maintenance depend on an administrator bypass.

When a second maintainer joins, require one approving CODEOWNER review and dismiss stale
reviews when the diff changes. Stable release authority remains separate from GitHub merge
authority and eventually requires threshold approval as described in the release process.

## Publishing a source milestone

1. Merge a pull request that updates `VERSION`, the changelog, and dependency records.
2. Confirm `validate` succeeds on the exact `main` commit.
3. Create and push a signed `v$(cat VERSION)` tag for that commit.
4. Inspect the automatically created draft release, source manifest, and checksum.
5. Publish the draft only after the release checklist is complete.

The automated workflow can create drafts but cannot promote channels, sign an OS image, or
publish a draft. A source milestone is not a bootable image.

## Dependency updates

GitHub Actions are pinned to reviewed commit hashes. Dependabot may propose digest updates,
but a green check is not sufficient evidence by itself: verify the action repository, release
notes, and tag-to-commit relationship before merging. Other third-party source pins follow the
same review rule and must retain license and provenance records.
