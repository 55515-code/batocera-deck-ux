# Graphics Compliance and Debranding

LuigiOS treats every visible image in source and in a candidate image as a
reviewed release artifact. The goal is a coherent, freely redistributable
interface without concealing compatibility or pretending that third-party
software belongs to LuigiOS.

This is an engineering policy, not a legal opinion. Copyright and trademark
review remains a release responsibility.

## Rules

- Replace distribution-owned presentation and unlicensed bundled marks with
  original LuigiOS semantic icons.
- Do not trace, distort, recolor, or make a near-copy of a vendor logo. Similar
  function is fine; similar protected visual identity is not the design goal.
- Keep truthful product or emulator names where they are needed to identify a
  third-party component. Classify those uses as `nominative-third-party` and
  explicitly approve them during review.
- Preserve upstream notices and attribution. A visual replacement does not
  remove an upstream license obligation.
- Never infer permission from an image being publicly downloadable.

## Asset intake

Add finished artwork under `branding/assets/`, then add an exact path entry to
`branding/PROVENANCE.json`. Each entry records creator, source, exact SHA-256, SPDX license,
copyright, classification, trademark review, and whether it derives from
another work. Binary images need their own record; a repository-wide text
license is not enough to establish their origin.

Use semantic categories from `semantic-icons-v1.json` for systems and actions.
Manufacturer silhouettes, wordmarks, controller trade dress, and console case
shapes are not semantic icon templates.

```bash
./tools/graphics-audit validate-policy
./tools/graphics-audit verify-source
./tools/graphics-audit verify-repository
```

## Candidate image sweep

Mount or unpack the candidate root filesystem and scan each graphics-bearing
root. A report contains stable paths, hashes, dimensions, metadata indicators,
reserved-name review hints, SVG references, and provenance state.

```bash
./tools/graphics-audit scan-image --root /path/to/image-root --output build/graphics-inventory.json
```

The term detector creates a review queue; it cannot decide whether pixels form
a protected mark. Release review must inspect every visible image, including
boot frames, themes, emulator launch screens, help overlays, icons, wallpapers,
video previews, and recovery UI. OCR or ScanCode reports may be attached as
supplemental evidence, but they do not replace visual review.

## Replacement overlays

`replacements-v1.json` identifies an exact destination, expected upstream
SHA-256, replacement source, and replacement SHA-256. Application is dry-run by
default and is intended for a disposable image staging root:

```bash
./tools/graphics-audit apply-replacements --root build/rootfs
./tools/graphics-audit apply-replacements --root build/rootfs --apply
```

The operation fails closed if upstream changed, the destination is outside an
audited graphics root, the replacement lacks approved provenance, either file
is a symlink, or either hash differs. Do not apply image overlays directly to a
customer device; rebuild and test the image.

## Release evidence

Archive the source audit, candidate image inventories, replacement report,
human review sign-off, screenshots from every OS context, and the image digest.
Store custom license texts in `LICENSES/` using SPDX or `LicenseRef-*` identifiers.
Re-run the complete sweep whenever Batocera, KDE, an emulator, a theme, or an
add-on changes.

The metadata model follows the [REUSE Specification 3.3](https://reuse.software/spec/)
and uses identifiers from the [SPDX License List](https://spdx.org/licenses/).
ScanCode can provide supplemental machine-readable license evidence for a
candidate image; LuigiOS's exact graphics inventory and visual review remain
separate required gates.
