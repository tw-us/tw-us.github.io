# Calm Field Guide Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current documentation-shell visual language with the approved Calm Field Guide system while preserving the three bilingual action flows and static-site safety boundary.

**Architecture:** Keep MkDocs Material only as a static renderer. Replace its visible docs treatment through a scoped CSS system and semantic page markup: shared masthead/route marker, narrative hero, journey modules, and notebook prompts. Use original inline SVG only for cross-border narrative illustrations; do not commit unverified third-party assets.

**Tech Stack:** Python 3.12, MkDocs Material, Markdown with semantic HTML, CSS, inline SVG, GitHub Pages.

## Global Constraints

- Canonical design: `docs/superpowers/specs/2026-08-31-calm-field-guide-design.md`.
- Preserve `/`, `/zh/`, `/en/`, family-plan, community-support, and when-things-change routes.
- No database, account, analytics, donation, prediction, external API, or form persistence.
- Do not use unverified Soco-st files; create ledger and use original inline SVG only in this slice.
- Must pass strict build and built-site checker; desktop + mobile browser QA is required.

---

### Task 1: Establish the shared Calm Field Guide shell

**Files:**
- Modify: `mkdocs.yml`
- Replace: `docs/stylesheets/extra.css`
- Create: `docs/assets/illustrations/ATTRIBUTION.md`
- Modify: `scripts/check-built-site.py`

**Interfaces:**
- Produces shared CSS classes: `field-guide`, `field-guide-header`, `route-marker`, `journey`, `journey-stop`, `notebook-sheet`, `source-record`.
- Each V1 page consumes these semantic classes; archive pages retain a readable fallback.

- [ ] Remove `navigation.tabs` and `toc.integrate` from `mkdocs.yml`; retain search and awesome-nav.
- [ ] Replace legacy orange/theme/card rules with the approved paper/mist/moss/coral/sun/ink tokens; hide the Material navigation and sidebars only on V1 routes; give V1 pages a narrow reading column, persistent masthead, accessible focus, mobile single-column behavior, and `prefers-reduced-motion` behavior.
- [ ] Create an empty attribution ledger with required source/license/check-date/page columns.
- [ ] Extend the checker to require the shared selectors and the attribution ledger.
- [ ] Run `poetry run mkdocs build --strict` and `poetry run python scripts/check-built-site.py`; commit `feat: establish calm field guide shell`.

### Task 2: Rebuild both localized homepages as a narrative journey

**Files:**
- Replace: `docs/zh/index.md`
- Replace: `docs/en/index.md`

**Interfaces:**
- Each homepage supplies `field-guide` root, peer-language link, original inline SVG hero, and three linked journey stops.
- Chinese primary copy remains family-first; English copy remains preparedness/responsible-support native copy.

- [ ] Replace generic card markup with a compact masthead, narrative headline, SVG family-connection scene, and three sequential `journey-stop` links.
- [ ] Use required visible links to `family-plan/`, `community-support/`, and `when-things-change/`; retain peer locale link.
- [ ] Extend the checker to require `journey`, no `.grid.cards` markup in localized homepages, and all three route destinations.
- [ ] Run strict build/check and inspect both generated HTML documents; commit `feat: rebuild bilingual preparedness journey`.

### Task 3: Rebuild action pages as notebook and editorial field guides

**Files:**
- Replace: `docs/zh/family-plan.md`, `docs/en/family-plan.md`
- Replace: `docs/zh/community-support.md`, `docs/en/community-support.md`
- Replace: `docs/zh/when-things-change.md`, `docs/en/when-things-change.md`
- Modify: `scripts/check-built-site.py`

**Interfaces:**
- Family pages use `notebook-sheet` prompts and local-only privacy statement.
- Community/signal pages use `source-record` blocks with their existing authority boundaries.

- [ ] Convert the two family-plan pages into print-friendly notebook prompts. Preserve the three actions, local-only privacy statement, official sources, review date, and no-form behavior.
- [ ] Convert community-support and signal pages into editorial field-guide sections. Preserve family-first ordering, no unaffiliated fundraising/dispatch, official-source-first escalation, and non-authoritative World Monitor labelling.
- [ ] Add checker assertions for notebook prompts, source records, and required safety copy in each locale.
- [ ] Run strict build/check; commit `feat: rebuild action flows as field guides`.

### Task 4: Visual acceptance and release evidence

**Files:**
- Create: `docs/RELEASE-CHECKLIST.md`
- Modify: `README.md`

- [ ] Add the design-specific release checks: live root/zh/en pages, peer language route, no generic card grid, visible focus, mobile no clipping, no unledgered external illustrations, and no prohibited backend/collection surface.
- [ ] Serve/build locally and capture desktop plus mobile screenshots for `/zh/`, `/zh/family-plan/`, `/en/`, `/en/community-support/`; correct visual defects before commit.
- [ ] Push via the repository-scoped `us-tw` SSH identity; wait for GitHub Actions success and inspect the live custom-domain routes.
- [ ] Commit `docs: add field guide release checks` and record live verification evidence in the final report.
