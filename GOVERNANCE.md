# Governance

The project uses a lightweight maintainer model designed for a part-time lead and a
growing contributor group.

## Decisions

- Routine fixes and documentation use pull requests and normal review.
- Trust, update, boot, storage, privilege, telemetry, and compatibility changes require
  a short RFC, a public review window, and explicit maintainer approval.
- Stable artifacts are promoted by digest after test evidence; they are never rebuilt
  merely to change channels.
- Security response can be private until a coordinated fix is available.

## Review

At least one approving maintainer and green required checks are expected before merge.
Authors do not approve their own pull requests once another maintainer is available.
Early in the project, the founding maintainer may merge reviewed emergency work while
recording the rationale and follow-up test debt.

Maintainers are selected from sustained contributors who demonstrate sound review,
care with user data, and constructive community conduct. Inactive maintainers can step
back without ceremony and return later. Permissions should remain narrow and releases
must not depend on one person's online signing key.

## Community Code

Community submissions stay attributable to their authors. Large third-party components
remain separate pinned dependencies when practical, keeping upstream history, license,
security reporting, and update paths intact. The project does not silently absorb or
rebrand another community's work.
