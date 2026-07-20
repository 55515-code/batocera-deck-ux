# LuigiOS Interface Guidelines
LuigiOS uses familiar, well-tested handheld-console principles while presenting an
original visual and interaction system. Contemporary devices such as Steam Deck and
Nintendo Switch 2 may be studied for broad usability lessons, but they are not templates.
LuigiOS must not copy their screen composition, artwork, icons, sounds, animation timing,
wording, controller silhouettes, or other recognizable trade dress.

These guidelines apply to Game Mode, quick settings, recovery, first boot, and LuigiOS
system applications. Third-party applications retain their own identity inside clearly
bounded application surfaces.

## Experience model

- **Play is home.** Start on the local library, preserve the last useful position, and
  make launching a game the shortest path in the interface.
- **One focus, one action.** Controller focus is always visible. Every screen has one
  visually dominant next action and a predictable back path.
- **Layers preserve context.** Short tasks use sheets or overlays that keep the current
  game or library visible. Full pages are reserved for browsing and complex settings.
- **Status is quiet.** Time, battery, network, storage warnings, and active downloads use
  a restrained status rail. Persistent status must not compete with game artwork.
- **Commands stay stable.** Contextual controller commands occupy a consistent command
  rail and update immediately when focus changes.
- **The desktop is a capability, not a second product.** COSMIC uses the same color,
  icon, language, account, recovery, and controller rules as Game Mode.

## Original visual language

- Use LuigiOS design tokens, semantic icons, type hierarchy, and original artwork.
- Favor true OLED black for dominant dark surfaces, with charcoal elevation and more
  than one accent family for state, warning, recovery, and expert-risk semantics.
- Do not recreate a third party's exact navigation bars, tile proportions, focus rings,
  menu transitions, quick-settings geometry, boot sequence, or system sounds.
- Do not use platform wordmarks, controller trade dress, or manufacturer button art as
  decoration. Nominative names and neutral input labels are allowed where compatibility
  or instructions genuinely require them.
- Keep upstream branding inside the upstream application or credits. LuigiOS wrappers
  must not imply that third-party software is a LuigiOS-owned service.
- All sounds, haptics, illustrations, animation curves, and icons shipped by LuigiOS
  require provenance and a redistribution-compatible license.

## Controller and touch

- Every supported workflow is complete with a controller. Touch, mouse, and keyboard are
  additional input paths and never the only way to reach an action.
- Use semantic actions such as **Confirm**, **Back**, **Menu**, and **Quick Settings**.
  Resolve physical glyphs from the active controller profile rather than hard-coding one
  manufacturer's layout.
- Confirm and Back mappings follow the user's selected regional/input preference across
  every LuigiOS surface. Remapping changes prompts at the same time.
- Directional navigation is deterministic, reversible, and spatially sensible. Hidden
  focus traps, focus loss after refresh, and pointer-only hover actions are release bugs.
- Touch targets are at least 44 by 44 logical pixels. Focus targets are never smaller
  than their touch target, and target size does not shift when selected.
- Text entry invokes the OSK from controller and touch, preserves the field value when
  dismissed, and never blocks controller navigation behind the keyboard.

## Handheld and television layout

- Qualify at 1280x800 handheld and 1920x1080 television layouts, including overscan-safe
  presentation. Support other ratios through constraints, not viewport-scaled type.
- Primary text remains readable at arm's length on handheld and across a room on TV.
- Keep page titles compact inside tools and settings. Reserve large display type for true
  full-screen moments such as first boot, recovery confirmation, or an empty library.
- Fixed-format rails, tiles, dialogs, and controller prompts use stable dimensions so
  loading, metadata, and focus changes do not move surrounding content.
- HDMI mode changes and controller reconnects preserve focus, dialog state, and the
  current task. Content never opens behind an active modal or outside the visible output.

## Motion, sound, and performance

- Input feedback begins within 100 ms. Navigation animation normally completes within
  200 ms and remains interruptible; launching and destructive transactions show honest
  progress instead of decorative delay.
- Respect reduced-motion, high-contrast, text-size, caption, and muted-interface settings.
- Sounds and haptics confirm meaningful state changes, not every focus movement. They are
  independently adjustable and silent during configured quiet hours.
- The shell must remain responsive while artwork, metadata, network data, or stores load.
  Local library and settings content render before optional online enrichment.

## Local-first and account boundaries

- The vanilla LuigiOS distribution installs, boots, completes first boot, imports local
  content, launches local games, changes device settings, pairs controllers, backs up,
  restores, resets, and enters recovery without an internet connection or login.
- Network setup is always skippable. Offline state is a normal designed state, not an
  error screen or reduced trial mode.
- LuigiOS has no mandatory project account. Local profiles remain local unless the owner
  deliberately enables a clearly identified synchronization service.
- A downstream proprietary application or optional third-party service may require its
  own network connection and account. That requirement must be disclosed before launch,
  scoped to that service, and must never block the vanilla shell or local device controls.
- Sign-in prompts must identify the service operator, explain why sign-in is needed, offer
  **Not now** when leaving the optional service is safe, and provide a visible sign-out and
  local-data removal path.
- Online artwork, stores, multiplayer, cloud saves, diagnostics, and peer distribution
  fail independently. Their outage must not prevent local play or recovery.

## Safety and validation

- Destructive actions state what changes, what remains, and where recovery is available.
  Require hold-to-confirm or an explicit second step for reset, erase, and overwrite.
- Loading, empty, offline, denied, interrupted, partial-success, and rollback states are
  designed before a workflow is considered complete.
- Candidate review includes controller-only video or screenshots at handheld and TV
  sizes, an offline first-boot run, a no-account local-play run, and a visual comparison
  review that rejects confusing similarity to proprietary console interfaces.
- Accessibility, localization expansion, active-controller glyph changes, sleep/resume,
  and return-to-Game-Mode behavior are release gates, not post-release polish.
