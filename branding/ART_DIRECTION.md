# LuigiOS Art Direction

LuigiOS should feel like a dependable tool maintained by people who care about
games, repair, and preservation. The visual foundation is dark-neutral and
quiet. Green communicates focus, progress, health, and connection; it is not a
full-screen tint.

The player's library is the visual subject. LuigiOS identity provides continuity,
status, and recovery without behaving like an advertisement or competing with
game artwork. The visual expression of "Games first. Your device. Your choices."
is calm chrome, obvious focus, portable ownership cues, and no sponsored placement.

## Production language

- The core mark is an original framed `L` with two endpoint nodes. It must work
  without a mascot and remain legible at 16px.
- Icons use a 24x24 grid, 2px rounded strokes, clear silhouettes, and no vendor
  trade dress. Filled green nodes may call out state or network relationships.
- The caretaker raccoon appears in editorial art and selected transitions, not
  as decoration on every screen. Keep the character capable, calm, and small
  enough that the interface remains primary.
- Angel and demon state variants remain the same caretaker raccoon. Use the
  paired variants according to [MASCOT.md](MASCOT.md); they supplement explicit
  status and risk communication rather than replacing it.
- Wallpapers reserve quiet space for panels, launchers, and desktop files. Use
  the 48px handheld and 72px television safe areas from the design tokens.
- COSMIC, Game Mode, settings, and recovery share color and icon semantics while
  retaining layouts suited to their jobs.
- Use OLED black (`#000000`) for full-screen backgrounds and other dominant
  dark areas. Reserve charcoal surface tokens for panels, menus, selected rows,
  and controls where visible elevation improves navigation.
- Preserve clear boundaries on OLED black with restrained borders, shadows,
  spacing, and text hierarchy. Do not replace every dark tone with black or
  sacrifice focus, disabled, hover, and modal states for power savings.

## Exclusions

Do not use Nintendo or Mario-series visual language, Tux, protected hardware
trade dress, game box art, screenshots, console/storefront logos, or altered
vendor marks as LuigiOS identity. Upstream names and acknowledgements remain
where factual or license-required.

The original art-guidance ZIP and its composite concept boards are review inputs
only. They are not copied into release artifacts. Production assets must have an
exact entry in `PROVENANCE.json` and pass `./tools/graphics-audit verify-source`.

## Asset workflow

1. Edit semantic tokens or vector definitions in `tools/render-brand-assets`.
2. Keep generated raster masters under `branding/source/` with their prompt and
   source hash documented.
3. Run `./tools/render-brand-assets` twice and confirm the second run reports no
   changes.
4. Update exact hashes in `PROVENANCE.json`.
5. Run `./tools/brandctl validate` and the graphics audit before integration.
