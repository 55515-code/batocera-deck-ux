# Discord Setup

Create a new server from the project owner's account, upload
`branding/assets/community/avatar-512.png`, then enable Community in Server
Settings. Keep the server private until a second account passes onboarding,
channel visibility, posting, report, timeout, and appeal tests.

Apply [server-blueprint.yml](server-blueprint.yml) from top to bottom. Discord's
current Community Onboarding requires at least seven default channels, five of
which allow everyone to view and send; the blueprint meets that constraint with
a deliberately compact public front door. Configure specialist channels through
role-select questions so new members are not presented with the entire server.
[Discord documents the onboarding requirements here](https://support.discord.com/hc/en-us/articles/11074987197975-Community-Onboarding-FAQ).

Use forum channels for help and development so answers remain discoverable.
Discord forum channels support AutoMod and slow mode, and require Community mode.
[Discord's forum guide](https://support.discord.com/hc/en-us/articles/6208479917079-Forum-Channels-FAQ)
is the operational reference.

## Owner checkpoint

The owner must perform server creation, authentication, CAPTCHA, Community-mode
consent, and final invite publication. Never place a user token, bot token, webhook
secret, backup code, or session cookie in this repository or an automation prompt.

After setup, enable built-in spam and mention-spam protection, route alerts to the
private `mod-alerts` channel, and avoid third-party moderation bots until a missing
capability is documented. Discord's built-in AutoMod can cover text, threads, and
forum surfaces and centralize alerts in a private channel.
