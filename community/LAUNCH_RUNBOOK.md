# Community Launch Runbook

## Gate 1: project readiness

- [x] Community code and moderation policy exist.
- [x] Discord and Reddit structures are reviewed in source control.
- [x] Social avatar and banner have original-art provenance.
- [ ] GitHub Discussions is enabled and seeded with welcome, support, and roadmap posts.
- [ ] At least two trusted people can receive moderation and security escalations.
- [ ] Public release status is described honestly as an early developer preview.

## Gate 2: authenticated creation

1. Create the Discord server as the project owner and enable Community mode.
2. Apply `discord/server-blueprint.yml`, permissions, AutoMod, onboarding, and
   Server Guide; test with a non-staff account before publishing an invite.
3. Confirm `r/LuigiOS` is still available immediately before creation. Reddit
   community names cannot be changed or deleted after creation.
4. Create the public, non-18+ subreddit; apply rules, flair, removal reasons,
   Automoderator, avatar, banner, and seed posts.
5. Add final URLs to `community/channels.json`, `README.md`, and `SUPPORT.md` in a
   reviewed pull request. Do not publish placeholder or expiring invite links.

## Gate 3: soft launch

- Invite a small founding group of testers, artists, and Batocera/Linux contributors.
- Run seven days in invite-only promotion while measuring unanswered questions,
  false-positive moderation, and onboarding exits.
- Publish the first demo clip only after the install state, limitations, and
  source branch are clear.
- Open broad promotion after one tested release artifact and recovery path exist.

## First month cadence

| Day | Activity |
| --- | --- |
| Monday | Weekly build thread: what changed, what is blocked, what needs testing |
| Wednesday | Contributor spotlight or design/process note |
| Friday | Hardware test call with one narrow, reproducible target |
| Release day | Signed release notes, known issues, recovery instructions, source link |
| Monthly | Public moderation and community-health summary without personal data |

Success is measured by answered questions, returning contributors, tested hardware,
merged work, and healthy moderation load, not raw member count.
