# TW–US Logo 2a — Implementation Contract

**Decision:** K2 selected **2a / Two-tone** from the final Claude Design handoff on 2026-09-01.

## Canonical source

- Original handoff: `/tmp/tw-us-logo-handoff/tw-us-crisis-connect-logo-system/project/TW-US Symbol Exploration.dc.html`
- Relevant definition: symbol `m2t`, lines 22–25; selected 2a presentation, lines 45–90.
- The handoff is reference material. Do not copy its prototype runtime or add its dependencies to this MkDocs site.

## Mark geometry

The primary mark uses a `100 × 100` viewBox and exactly two filled polygons:

- Upper segment: `50,0 96,46 48,46 56,34 70,34 50,14 30,34 44,34 36,46 4,46`
- Lower segment: `4,54 52,54 44,66 30,66 50,86 70,66 56,66 64,54 96,54 50,100`

The negative path is structural: upper inner triangle → upper slit → central gap → lower slit → lower inner triangle. It must remain transparent, not be implemented as an overlaid stroke.

## Color contract

- Ink navy: `#17223B` (upper segment on the primary mark)
- Vermilion: `#C8442B` (lower segment on the primary mark)
- Paper: `#F4EFE6`

For a dark surface, use the designed reversed treatment from 2a: upper segment paper, lower segment vermilion. Do not introduce gradients.

## Scope

1. Add production SVG assets for the primary and reversed 2a symbol. SVGs must be accessible and have no external dependency.
2. Replace the existing `docs/assets/logo.png` use in MkDocs configuration with the primary SVG.
3. Add a favicon using the mark, preferably a dedicated SVG with a navy square field and the high-contrast reversed symbol; use a PNG fallback only if MkDocs/browser support needs it.
4. Replace all V1 field-guide and archive text-only `TW–US` masthead links with a compact mark + `TW–US` lockup. Keep accessible text and existing destination URLs. Do not change navigation labels or page copy.
5. Extend the existing stylesheet only as needed. The desktop header must stay compact; on a 390px viewport the mark must not cause horizontal overflow or crowd the route navigation.
6. Do not modify archived content beyond the archive masthead, routing, site copy, colors unrelated to the logo, external fonts, dependencies, or deployment configuration.

## Acceptance criteria

- `docs/assets/tw-us-mark.svg` renders the selected two-tone geometry exactly using the two polygons above.
- A dark-background/reversed variant exists and uses paper upper + vermilion lower segments.
- The public site config references the SVG primary logo rather than the legacy PNG.
- The root landing, `/zh/`, `/en/`, all six field-guide subpages, and `/archive/` show an accessible logo lockup while retaining their links.
- The mark is recognizable at 24px and does not clip or blur in a browser.
- `poetry run mkdocs build --strict`, `poetry run python scripts/check-built-site.py`, and `git diff --check` all pass.
- Browser QA at desktop and 390px confirms no horizontal overflow on root, one Chinese guide page, one English guide page, and archive.
