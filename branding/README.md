# LuigiOS Brand System

This directory is the source contract for a visually unified LuigiOS. Artwork is
kept separate from deployment logic so boot, Game Mode, Plasma, Steam handoff,
settings, and recovery can change context without appearing to change products.
Interaction and transition rules are documented in
[Unified Brand and Transition UX](../docs/BRANDING.md).

Place generated work under `branding/assets/` using the paths in
`brand-v1.json`. Run:

```bash
./tools/brandctl validate
./tools/brandctl validate --require-ready
./tools/brandctl plan --scope demo
./tools/brandctl plan --scope image
./tools/graphics-audit validate-policy
./tools/graphics-audit verify-source
./tools/graphics-audit verify-repository
```

The normal validation command checks the manifest and any artwork already
present. `--require-ready` additionally fails until every demo-required slot is
populated. Missing optional variants remain visible in the report.

Every graphics file also needs an exact-path entry in `PROVENANCE.json`.
`graphics-policy-v1.json` defines the release classifications and review rules,
`semantic-icons-v1.json` reserves original vendor-neutral icon categories, and
`replacements-v1.json` holds exact-hash build overlay rules. See
[Graphics Compliance and Debranding](../docs/GRAPHICS_COMPLIANCE.md).

## Design contract

- Use the same core mark, icon geometry, vocabulary, and motion timing everywhere.
- Keep layouts adapted to context: controller-first Game Mode, work-focused Plasma,
  and quiet recovery screens should be related without being identical.
- Supply both 1280x800 handheld and 1920x1080 TV assets. Add 4K variants when the
  composition differs rather than relying on a blind crop.
- Keep essential marks legible at 24 px and in monochrome. Avoid text baked into
  icons that will be localized later.
- Do not include console-vendor, game, emulator, or third-party store artwork
  without documented redistribution permission. Do not make altered copies of
  vendor logos; use original LuigiOS semantic icons. LuigiOS artwork needs its
  own provenance and license record before release.
- Complete trademark clearance for the LuigiOS name and marks before public or
  commercial distribution; repository adoption is not legal clearance.
- Image-scope targets are immutable build inputs. Demo-scope targets live under
  `/userdata` or the persistent Plasma home and must be deployed transactionally.

No placeholder artwork is shown on the device. Until a slot is ready, upstream
Batocera or KDE artwork remains the explicit fallback.
