# TW–US Calm Field Guide — Design Specification

## Decision

Rebuild the V1 public presentation while preserving the three approved flows and existing `/zh/` and `/en/` routes:

1. family support plan;
2. responsible community support;
3. verify signals and choose the next step.

The site is for overseas Taiwanese supporting family in Taiwan. It is not a crisis prediction dashboard, a local evacuation app, a fundraising platform, or a user-data service.

## Product feeling

A calm, warm Japanese public-service field guide that makes preparation feel possible. It must invite exploration without turning safety information into a game. The emotional arc is: **connection → preparation → contribution**.

## Page architecture

### Shared shell

- Remove documentation-shell hierarchy from V1 pages: no top navigation tabs, no left documentation sidebar, no table-of-contents rail on the action flows.
- A compact masthead contains `TW–US`, three route labels, and a persistent peer-language link.
- The archive remains reachable but visually secondary in the footer.
- The main column is intentionally narrow for reading; featured illustrations may break wider than text.

### Home

- Hero: a cross-border family illustration and the promise “先把彼此找得到的方式準備好。” / audience-native English equivalent.
- The only dominant interactive structure is a three-stop preparation journey: contact, prepare, extend support.
- The primary stop links to the family plan; the other stops link to community support and verified-signal guidance.
- Do not use a dashboard, risk score, map, stacked generic cards, war imagery, or fear-oriented copy.

### Family plan

- Present as a print-friendly family notebook: short prompts, visible completion rhythm, local-only statement, and source/review record.
- It contains no login, form collection, local browser persistence, or external data call.

### Community support and signal guidance

- Use an editorial field-guide layout: an illustrated opening, concise action blocks, and labelled external sources.
- Community support must preserve the ordering family readiness → verified information → existing organization participation.
- Signal guidance must keep official-source-first escalation semantics.

## Visual system

| Token | Value | Use |
| --- | --- | --- |
| Paper | `#FBFAF4` | primary page ground |
| Mist | `#EDF2EA` | quiet section surface |
| Moss | `#31634B` | actions, route marker, trust |
| Coral | `#E9785D` | warm emphasis and people |
| Sun | `#F2C65C` | journey node and completion |
| Ink | `#18211D` | reading text |
| Rule | `#CBD4C8` | borders and dividers |

- Typography uses a characterful serif display stack only for short narrative headings, and an accessible system sans stack for all instructions and body copy. No runtime font dependency is required.
- Large rounded cards are prohibited as a default layout primitive. Rounded containers are reserved for illustrations, notebook surfaces, and action callouts.
- Interaction feedback is restrained: clear focus states, subtle color/border changes, no hover-only affordance, and reduced-motion support.
- Mobile is a single, readable column; no compressed desktop navigation.

## Illustration system

- Soco-st is the primary source. Each shipped external asset must have an exact attribution ledger row with source URL, license/terms snapshot, checked date, and page assignment.
- Where Soco-st cannot express a cross-border family action, use an original inline SVG with the same low-detail, calm outline language. It must not imitate a specific copyrighted asset.
- Every illustration explains one action. Decorative images may not convey safety-critical content alone.
- Do not use fire, explosions, military aircraft, weapons, or distress imagery as primary decoration.

## Accessibility and acceptance

- Clear visible keyboard focus; semantic headings and link labels; supplementary illustration alt text.
- High contrast for all actionable copy; reduced-motion path; responsive no-clipping checks at mobile and desktop widths.
- `poetry run mkdocs build --strict` and `poetry run python scripts/check-built-site.py` remain mandatory.
- Browser QA must show the live `/`, `/zh/`, `/zh/family-plan/`, `/en/`, and `/en/community-support/` routes with visible path entry points and working language peer links.

## Explicit non-goals

- No new backend, account, analytics, payment, donation, prediction, or crowdsourced-reporting capability.
- No unverified third-party illustration committed merely to make a page look finished.
- No redesign of the three approved action-flow content contracts.
