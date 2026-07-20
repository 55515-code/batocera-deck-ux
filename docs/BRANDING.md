# Unified Brand and Transition UX

LuigiOS uses one product identity across boot, Game Mode, Desktop Mode, settings,
recovery, and optional Steam surfaces. Unity comes from shared visual tokens,
language, focus behavior, and transition rules. It does not require forcing every
surface into the same layout.

The identity promise is **Games first. Your device. Your choices.** Branding must
clarify ownership and context, not turn the operating system into an advertisement.
Game art and third-party storefront identity remain attributable to their actual
owners; LuigiOS chrome stays quiet enough that the player's library is primary.

## Context model

- **Game Mode** is controller-first, full-screen, and optimized for browsing and
  launching a library from a distance.
- **Desktop Mode** is work-focused COSMIC with pointer, touch, keyboard, and
  controller parity. It retains the same mark, colors, icon geometry, and terms.
- **Settings** uses stable categories and the same labels whether opened from Game
  Mode or Desktop Mode. A setting must not appear to change ownership across modes.
- **Recovery** is quiet and high-contrast. It uses the core mark and vocabulary but
  removes decorative motion and nonessential choices.
- **Steam handoff** uses matching shortcut art and a short neutral transition. Steam
  remains visibly Steam; LuigiOS should not impersonate third-party interfaces.

## Continuity rules

- Use `Game Mode`, `Desktop Mode`, `Settings`, `Library`, `Updates`, and `Recovery`
  consistently. Avoid alternating between Batocera, Big Picture, dashboard, and
  frontend when the user-facing concept is the same.
- Write the product name exactly as `LuigiOS`. Follow the task-language and upstream
  attribution rules in [Identity and Voice](IDENTITY_AND_VOICE.md).
- Preserve controller focus through dialogs and return focus to the item that opened
  a secondary surface. Touch or pointer input must not permanently steal focus mode.
- Keep routine context transitions at or below 300 ms. Respect reduced-motion
  settings and avoid stacking LuigiOS animation over an application's own splash.
- Use a shared neutral background during handoff so aspect-ratio or display-mode
  changes do not flash unrelated branding.
- Never strand the user on a black screen. Every full-screen context needs a tested
  controller-only return path and a watchdog-owned fallback to Game Mode.
- Keep status semantics stable: progress, success, warning, destructive action, and
  offline state use the same icon and color meaning on every surface.

## Asset review

1. Run `./tools/brandctl validate --require-ready`.
2. Review 1280x800 handheld and 1920x1080 TV compositions without viewport-scaled
   typography or clipped marks.
3. Check the symbolic mark at 16, 24, 32, and 48 px on light and dark backgrounds.
4. Verify controller focus, touch targets, pointer visibility, reduced motion, and
   readable error states in Game Mode, COSMIC, settings, and recovery.
5. Regenerate managed art with `./tools/check-rendered-brand-assets render`, then run
   `./tools/check-rendered-brand-assets check` to rebuild and compare it in the same
   pinned, read-only renderer container. Host ImageMagick output is not release
   evidence even when its version string appears identical.
6. Run a demo deployment dry-run, apply it transactionally, reboot, test every
   transition, and restore the generated backup.
7. Record provenance and redistribution rights before an asset enters an image.

The machine-readable slot inventory is [brand-v1.json](../branding/brand-v1.json).
