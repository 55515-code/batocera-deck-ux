# Reddit Setup

`r/LuigiOS` appeared unclaimed when checked on 2026-07-19. Confirm availability
again immediately before creation. Reddit community names must be 3-21 characters,
cannot be changed after creation, and communities cannot later be deleted; the
project owner therefore approves the final creation action. See Reddit's current
[creation guide](https://support.reddithelp.com/hc/en-us/articles/15484258409492-How-to-create-a-community)
and [deletion limitations](https://support.reddithelp.com/hc/en-us/articles/15484241265684-How-do-I-delete-a-community).

## Creation values

The canonical machine-readable values are in [community.json](community.json).
This page explains the owner workflow; do not maintain a second divergent copy.

- Name: `LuigiOS`
- Type: Public
- Mature/18+: Off
- Description: `LuigiOS is a community-built, controller-first gaming OS: games first, your device, your choices. It focuses on dependable handheld play, preservation, repair, and open development.`
- Topics: Linux, Gaming, Open Source
- Avatar: `branding/assets/community/avatar-512.png`
- Banner: `branding/assets/community/banner-1920x480.png`

## Rules

1. Be kind and discuss the work, not the person's worth.
2. Keep posts relevant to LuigiOS, Batocera integration, handheld Linux, or project development.
3. No ROM, BIOS, firmware, key, credential, or private-data trading.
4. No piracy requests, DRM-bypass instructions, malware, spam, or undisclosed promotion.
5. Use descriptive titles and the closest post flair.
6. Move reproducible bugs and security reports to the correct private or GitHub workflow.
7. Respect licenses, attribution, privacy, and moderator direction.

Post flair: `Release`, `Build Log`, `Help`, `Hardware Test`, `Showcase`, `Development`,
`Art & UX`, `Discussion`, and `Solved`. User flair should be optional and limited to
contribution interests, not status hierarchy.

Add removal reasons that mirror each rule plus `Duplicate / continue existing thread`
and `Needs reproducible details`. Install the minimal [Automoderator config](automoderator.yml),
then test every rule in a private test community before production. Reddit's current
[Automoderator guide](https://support.reddithelp.com/hc/en-us/articles/15484574206484-Automoderator)
documents version history and rollback.

## Seed posts

Publish and pin the three canonical posts in `community.json` from their versioned
Markdown sources under `community/content/`. Add weekly build, hardware-lab, and
art-direction threads only when there is concrete work or evidence to discuss.
