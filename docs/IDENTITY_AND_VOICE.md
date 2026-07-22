# LuigiOS Identity and Voice

**Games first. Your device. Your choices.**

LuigiOS exists to make owning and playing on a game device straightforward. The
foreground belongs to the person holding the controller: their library, saves,
settings, hardware, software choices, and time. Operating-system machinery,
storefront incentives, and vendor relationships must not become the center of
the experience.

This is a pro-player principle, not an anti-creator or anti-business posture.
Games, emulators, hardware, and upstream software are made by people whose work,
licenses, names, and services deserve honest treatment. Companies may build on,
sell, sponsor work around, or contribute to LuigiOS, but money or distribution
power cannot bypass the same trust, provenance, compatibility, and review rules
used for community contributions.

## Product promise

- Start with games and return cleanly to games.
- Work offline for local play and device administration.
- Require no LuigiOS account, subscription, advertising, or sponsored ranking.
- Let the owner choose optional apps, services, storefronts, update transport,
  community features, and diagnostics sharing.
- Keep saves, settings, libraries, and backups portable and recoverable.
- Provide graphical setup, maintenance, update, rollback, and reset workflows.
- Keep Developer Mode available to owners without making Linux administration a
  prerequisite for everyone else.

Third-party services may require their own accounts or network access. LuigiOS
states that requirement before handoff and never disguises a third-party surface
as an OS requirement. The requirement is confined to that optional service and
cannot block deployment, first boot, the local shell, local play, device settings,
backup, reset, or recovery in the vanilla LuigiOS distribution.

## Naming

- Write the product name exactly as **LuigiOS**. Do not use `Luigi OS`, `Lugios`,
  `LuigiOs`, or names that imply an official SteamOS or Batocera edition.
- Use **Game Mode**, **Desktop Mode**, **Settings**, **Library**, **Apps**,
  **Updates**, **Recovery**, **Gamer Mode**, and **Developer Mode** consistently.
- Preserve factual upstream names in credits, licenses, diagnostics, source
  packages, migration notes, and compatibility documentation.
- Historical QA documents may retain the interface and component names that were
  present during the recorded test.

## Interface voice

Use short, direct, calm task language. Lead with what the player can do and what
will happen next. `Move games`, `Pair controller`, `Create restore point`, and
`Try again offline` are better foreground labels than package, service, mount,
or implementation names.

Errors state the affected task, whether data is safe, and a recovery action.
Advanced details remain available in an expandable Diagnostics section and in
Developer Mode. Do not hide upstream attribution or security facts merely to
make the interface appear simpler.

## Visual character

LuigiOS is dark-neutral, OLED-aware, colorful at points of action, and readable
from handheld and television distances. The caretaker raccoon represents repair,
preservation, and stewardship. Angel and demon variants communicate protected
and expert-risk paths while remaining the same character. The interface should
feel playful enough for games and restrained enough for storage, updates, and
recovery.

The machine-readable product promise is
[`profiles/product-identity-v1.json`](../profiles/product-identity-v1.json).
Interaction, layout, offline, and service-handoff rules are defined in
[LuigiOS Interface Guidelines](INTERFACE_GUIDELINES.md) and
[`profiles/interface-guidelines-v1.json`](../profiles/interface-guidelines-v1.json).
Brand assets and visual rules remain governed by `branding/`.
