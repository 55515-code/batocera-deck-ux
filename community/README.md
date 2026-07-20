# LuigiOS Community

**Games first. Your device. Your choices.**

The community layer connects users, artists, testers, and contributors without
making chat platforms the source of truth for the operating system.

- GitHub issues own reproducible bugs, hardware reports, and scoped features.
- GitHub Discussions owns durable design conversation and setup knowledge.
- Discord provides real-time help, contributor coordination, and community events.
- Reddit provides public showcases, release conversation, and broad discovery.

Project decisions, release evidence, security policy, and accepted changes always
return to GitHub. Discord and Reddit must not become required archives for build
instructions or design decisions.

Community spaces should help people play, repair, preserve, learn, and shape the
devices they own. They are not advertising channels: paid placement, sponsored
rankings, and undisclosed promotional support are outside the project identity.
Creators and companies remain welcome when affiliations are disclosed and their
work follows the same contribution, provenance, and moderation rules.

Downstream distributions and device makers are part of this community even when
they remove LuigiOS branding or keep product-specific changes private. The
[downstream and OEM policy](../DOWNSTREAM.md) explains the no-promotion-required
position and the compatibility, QA, and visibility benefits available to groups
that choose to collaborate upstream. The evidence and listing process is defined
in the [downstream compatibility program](OEM_COMPATIBILITY.md).

## Status

- Community code, moderation handbook, platform blueprints, launch copy, and
  original social graphics are ready in this repository.
- Discord is in a controlled soft launch at <https://discord.gg/BDfCJPUeVG>.
  Community mode and onboarding are enabled. Review the latest audit before broad
  promotion because the live configuration still has documented drift.
- Reddit blocked the authenticated `r/LuigiOS` creation attempt on 2026-07-19.
  No attempt was made to evade the platform block; its configuration remains ready.

See [Launch Runbook](LAUNCH_RUNBOOK.md), [Moderation](MODERATION.md), the
[Discord setup](discord/SETUP.md), and the [Reddit setup](reddit/SETUP.md).

## Reproducible review

The desired Reddit configuration is stored in `reddit/community.json`; the desired
Discord configuration is stored in `discord/server-blueprint.yml`. Public URLs and
platform lifecycle state live in `channels.json`. No credential, browser profile,
token, webhook, recovery code, or private moderation record belongs in Git.

Run `./tools/communityctl validate` before every community change. Run
`./tools/communityctl audit --write community/audits/YYYY-MM-DD.json` to capture a
reviewable public-state probe. Authenticated configuration must be checked against
the desired files after platform changes because platform exports are incomplete
and may contain private member or moderation data.
