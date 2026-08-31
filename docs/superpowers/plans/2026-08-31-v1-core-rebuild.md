# TW-US Crisis Connect V1 Core Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the public site into a bilingual, static, source-transparent action guide for overseas Taiwanese supporting family in Taiwan, while replacing the stale legacy deployment pipeline with a reproducible GitHub Pages workflow.

**Architecture:** Preserve a static MkDocs Material site and public repository. Use explicit, first-class locale folders under `docs/zh/` and `docs/en/`, plus a neutral language chooser at `/`; this deliberately produces stable `/zh/` and `/en/` URLs without adding a frozen third-party locale plugin. The Chinese and English core flows are separately authored for their audiences; neither is machine-translated. GitHub Actions builds the site from `main` and publishes a Pages artifact; DNS remains unchanged.

**Tech Stack:** Python 3.12; MkDocs Material; Markdown locale folders; GitHub Actions; GitHub Pages; Cloudflare DNS only.

## Global Constraints

- The V1 audience is overseas Taiwanese preparing to support family in Taiwan; Taiwan-local survival tools and live crisis prediction are external resources, not features to recreate.
- Publish only `zh-TW` and `en-US`; use explicit `/zh/` and `/en/` URLs and a persistent visible language switcher.
- No account, database, analytics vendor, stored family plan, donation collection, crowdsourced reporting, background service, paid API, or new subscription.
- The site may link to a partner such as FAPA only with a precise role label; it must not describe advocacy as emergency relief or solicit/handle donations.
- All actionable claims need a cited first-party or official source plus a visible `Reviewed on` date; do not reproduce external reference handbooks wholesale.
- Soco-st-inspired illustration direction is a visual language, not permission to reuse an asset. Each committed asset needs source URL, creator/site, exact license snapshot, download date, and assigned page in `docs/assets/illustrations/ATTRIBUTION.md`.
- Keep `CNAME` as `tw-us.cc`; do not alter DNS, domain registration, certificates, paid plans, or Cloudflare settings.
- External writes remain bounded to the repository and GitHub Pages configuration. Do not send partner outreach or publish public announcements.

---

## Acceptance Criteria

1. `poetry run mkdocs build --strict` exits 0 from a clean checkout.
2. The built site exposes `/zh/` and `/en/`; each has an explicit language-switch link to its peer route.
3. The Chinese homepage has a primary family-plan CTA and a secondary community-support CTA; the English homepage has a preparedness / responsible-support CTA, not a direct translation of the Chinese hero.
4. Every core action page has: a three-action first screen, source links, a reviewed date, and a no-data-collection statement where a plan/checklist appears.
5. The partner page distinguishes advocacy, preparedness, and relief roles; FAPA is labelled advocacy/education only and links externally.
6. The repository contains a Pages workflow that runs strict build validation on pull requests and deploys only `main` through `actions/deploy-pages`.
7. GitHub Pages is configured to `build_type: workflow`; a deployed commit is confirmed by the live `https://tw-us.cc/` response and browser inspection.
8. All new illustration assets have attribution records and render with meaningful alt text; no unverified third-party asset is committed.

---

## File Structure

- Modify: `docs/index.md` and `docs/.nav.yml` — neutral chooser and V1-first navigation for explicit locale folders.
- Create: `.github/workflows/pages.yml` — test/build/deploy GitHub Pages workflow.
- Create: `docs/zh/index.md` — Chinese landing page for overseas Taiwanese.
- Create: `docs/zh/family-plan.md` — local-only family support plan.
- Create: `docs/zh/community-support.md` — responsible community-support path.
- Create: `docs/zh/when-things-change.md` — official-source-first escalation and verification guidance.
- Create: `docs/zh/partners.md` — role-separated partner directory.
- Create: equivalent `docs/en/*.md` pages, authored for U.S. allies and partners.
- Create: `docs/assets/illustrations/ATTRIBUTION.md` — reusable attribution ledger.
- Modify: `docs/stylesheets/extra.css` — accessible flow cards, action cards, language switcher, and reduced-motion styles.
- Modify: `README.md` — contributor guide, content source policy, local build, preview, and deployment truth.
- Create: `scripts/check-built-site.py` — deterministic assertions for expected locale output, language switches, no placeholder copy, and external-link labels.

## Task 1: Establish explicit static locale routes and reproducible local validation

**Files:**
- Modify: `docs/index.md`
- Modify: `docs/.nav.yml`
- Create: `docs/zh/index.md`
- Create: `docs/en/index.md`
- Create: `scripts/check-built-site.py`

**Interfaces:**
- Consumes: the existing MkDocs Material configuration and folder-based documentation tree.
- Produces: a neutral root chooser at `site/index.html`, explicit `site/zh/index.html` and `site/en/index.html`, and a zero-exit validation command.

- [ ] **Step 1: Add the failing output contract checker**

Create `scripts/check-built-site.py` with assertions for:

```python
from pathlib import Path

required = [
    "site/index.html", "site/zh/index.html", "site/en/index.html",
]
for path in required:
    assert Path(path).is_file(), f"missing built page: {path}"
for path in ["site/zh/index.html", "site/en/index.html"]:
    body = Path(path).read_text(encoding="utf-8")
    assert 'class="language-switch"' in body, f"missing switcher: {path}"
```

Run:

```bash
poetry run python scripts/check-built-site.py
```

Expected: FAIL because locale pages and switchers do not exist.

- [ ] **Step 2: Create explicit route folders and a neutral root chooser**

Replace `docs/index.md` with only two direct choices:

```markdown
# TW-US Crisis Connect

Choose your language.

- [繁中：台美緊急連線](zh/)
- [English: TW-US Crisis Connect](en/)
```

Create `docs/zh/index.md` and `docs/en/index.md`. Each must include `<nav class="language-switch">` with an absolute peer route (`/en/` from Chinese and `/zh/` from English) and a direct link to its own `family-plan/` page.

- [ ] **Step 3: Set navigation to expose only the V1 routes as primary paths**

Update `docs/.nav.yml` so its first three groups are `Start`, `繁中`, and `English`; link them to `index.md`, `zh/index.md`, and `en/index.md`. Keep existing archive content reachable only through an `Archive` group and do not list it before the V1 paths.

- [ ] **Step 4: Build and validate explicit locale output**

Run:

```bash
rm -rf site
poetry run mkdocs build --strict
poetry run python scripts/check-built-site.py
```

Expected: PASS; no third-party locale plugin or dependency change is required.

- [ ] **Step 5: Commit the route foundation**

```bash
git add docs/index.md docs/.nav.yml docs/zh/index.md docs/en/index.md scripts/check-built-site.py
git commit -m "feat: add explicit Chinese and English site routes"
```

## Task 2: Build the Chinese overseas-family action flow

**Files:**
- Modify: `docs/zh/index.md`
- Create: `docs/zh/family-plan.md`
- Create: `docs/zh/community-support.md`
- Create: `docs/zh/when-things-change.md`

**Interfaces:**
- Consumes: locale routes from Task 1 and official / partner source URLs.
- Produces: Chinese primary and secondary CTAs that end in source-backed action pages.

- [ ] **Step 1: Write the failing content contract**

Extend `scripts/check-built-site.py` to require these Chinese strings in built output:

```python
checks = {
  "site/zh/index.html": ["建立家人支援計畫", "把你的支援能力帶進社群"],
  "site/zh/family-plan/index.html": ["今天先做這三件事", "本站不會儲存你的資料"],
  "site/zh/when-things-change/index.html": ["以官方公告為準", "提高注意"],
}
```

Run the checker. Expected: FAIL before content is written.

- [ ] **Step 2: Implement the Chinese homepage**

Write a primary hero directed at overseas Taiwanese, with exactly two flow cards:

- `建立家人支援計畫` → `/zh/family-plan/`
- `把你的支援能力帶進社群` → `/zh/community-support/`

Add a tertiary text link to `/zh/when-things-change/` called `查證情勢與下一步`.

- [ ] **Step 3: Implement a local-only family plan**

Write `family-plan.md` with sections:

1. `今天先做這三件事` — identify a primary and backup contact, agree a check-in protocol, locate documents and emergency support methods.
2. `建立你的聯絡卡` — printable / copyable prompts only; no form input or JavaScript persistence.
3. `訊息中斷時` — direct readers to official applications and official guidance.
4. `資料與隱私` — exact statement: `本站不會要求登入，也不會儲存你的聯絡人、文件或家庭計畫。`
5. `來源與覆核` — official links and a `Reviewed on: 2026-08-31` label.

- [ ] **Step 4: Implement responsible community support and escalation guidance**

`community-support.md` must order actions as family readiness → verified information sharing → existing organization participation. It must state that users should not operate unaffiliated fundraising or emergency dispatch through this site.

`when-things-change.md` must define `常態準備`, `提高注意`, and `立即應變` as action modes. Only an explicit official instruction or confirmed direct impact may trigger the last mode. World Monitor may be linked as an external observation tool with a clear non-authoritative label.

- [ ] **Step 5: Build and test**

```bash
rm -rf site
poetry run mkdocs build --strict
poetry run python scripts/check-built-site.py
```

Expected: PASS and all Chinese links resolve in the generated output.

- [ ] **Step 6: Commit the Chinese flow**

```bash
git add docs/zh scripts/check-built-site.py
git commit -m "feat: add overseas family preparedness flow"
```

## Task 3: Build distinct English public-support flow

**Files:**
- Modify: `docs/en/index.md`
- Create: `docs/en/family-plan.md`
- Create: `docs/en/community-support.md`
- Create: `docs/en/when-things-change.md`

**Interfaces:**
- Consumes: static i18n routes from Task 1 and source policy from Task 2.
- Produces: non-translated English content for U.S. allies, partners, and Taiwanese-American households.

- [ ] **Step 1: Extend the failing content checker**

Require in `site/en/index.html`:

```python
["Taiwan preparedness", "Support responsibly", "Build a family support plan"]
```

Run the checker. Expected: FAIL before the English content is written.

- [ ] **Step 2: Implement English information architecture**

Use the English homepage headline:

```text
Prepared families strengthen Taiwan’s resilience.
```

Use these cards:

- `Build a family support plan` → `/en/family-plan/`
- `Support responsibly` → `/en/community-support/`

Use this supporting statement:

```text
This site does not predict conflict or collect emergency information. It helps people prepare, verify, and support established organizations responsibly.
```

- [ ] **Step 3: Write English pages as audience-native copy**

`family-plan.md` should explain the cross-border family-support role, not translate Taiwan-local evacuation advice.

`community-support.md` should provide four bounded paths: share verified information, connect with an established organization, offer a relevant skill, and support an identified partner once its use of funds is clear. It must say the site does not process donations.

`when-things-change.md` must preserve the same official-source-first escalation rules as Chinese copy.

- [ ] **Step 4: Build and test**

```bash
rm -rf site
poetry run mkdocs build --strict
poetry run python scripts/check-built-site.py
```

Expected: PASS.

- [ ] **Step 5: Commit the English flow**

```bash
git add docs/en scripts/check-built-site.py
git commit -m "feat: add English preparedness and support flow"
```

## Task 4: Add accountable partner directory and illustration governance

**Files:**
- Create: `docs/zh/partners.md`
- Create: `docs/en/partners.md`
- Create: `docs/assets/illustrations/ATTRIBUTION.md`
- Modify: `scripts/check-built-site.py`

**Interfaces:**
- Consumes: vetted public partner URLs and licensed illustration files.
- Produces: role-specific partner cards and a verified asset ledger.

- [ ] **Step 1: Write failing partner-role checks**

Require these labels in both localized partner pages:

```text
Advocacy and public education
Preparedness and community resilience
Humanitarian relief
```

Require `FAPA` and `fapa.org` in both pages, plus the statement `FAPA is not an emergency-relief provider on this site.` in English and its Chinese equivalent.

- [ ] **Step 2: Create partner directory copy**

Make partner records structured as cards with these fields: `Role`, `What it does`, `How to engage`, `Source`, and `Reviewed on`.

Create a FAPA card only under advocacy / public education. Its engagement CTA may say `Visit FAPA` and open FAPA externally; it must not use `Donate` or imply that FAPA funds emergency relief.

Leave humanitarian relief as an explanatory category until a specific partner, use-of-funds statement, and review date are independently verified. Do not add a fundraising CTA.

- [ ] **Step 3: Add the illustration ledger before assets**

Create `docs/assets/illustrations/ATTRIBUTION.md` with table headings:

```markdown
| Asset path | Page | Source URL | Creator/site | License | License checked on | Modifications |
| --- | --- | --- | --- | --- | --- | --- |
```

Add no row and no binary asset until a source page’s exact terms have been captured and reviewed. This is intentional: unlicensed decorative images must not block the action-flow release.

- [ ] **Step 4: Build and test**

```bash
rm -rf site
poetry run mkdocs build --strict
poetry run python scripts/check-built-site.py
```

Expected: PASS.

- [ ] **Step 5: Commit governance and partner directory**

```bash
git add docs/zh/partners.md docs/en/partners.md docs/assets/illustrations/ATTRIBUTION.md scripts/check-built-site.py
git commit -m "feat: add accountable partner directory"
```

## Task 5: Implement accessible visual system without unverified image dependencies

**Files:**
- Modify: `docs/stylesheets/extra.css`
- Modify: all `docs/zh/*.md` and `docs/en/*.md` V1 pages

**Interfaces:**
- Consumes: semantic classes applied by locale pages.
- Produces: responsive, high-contrast action cards and a persistent language switcher.

- [ ] **Step 1: Add a CSS smoke-test contract**

Extend `scripts/check-built-site.py` to read `docs/stylesheets/extra.css` and assert it includes:

```python
for selector in [".action-flow", ".action-card", ".language-switch", "prefers-reduced-motion"]:
    assert selector in css, f"missing required accessibility selector: {selector}"
```

Run the checker. Expected: FAIL before styles are added.

- [ ] **Step 2: Implement semantic card markup**

Use `<section class="action-flow">` for page flow containers and `<article class="action-card">` for each CTA. Each CTA has a text label that names the action; illustration `alt` text is supplementary rather than the only instruction.

- [ ] **Step 3: Implement CSS constraints**

Add styles that:

- keep primary card text at WCAG-oriented high contrast;
- give keyboard focus a visible 3px outline;
- prevent card hover transforms for `prefers-reduced-motion: reduce`;
- use a single-column mobile layout below 768px;
- make `.language-switch` visible without relying on hover;
- use no war, explosion, or aircraft decorative imagery.

- [ ] **Step 4: Run local visual verification**

```bash
poetry run mkdocs serve --dev-addr 127.0.0.1:8000
```

Use a browser to verify desktop and mobile-width screenshots for `/zh/`, `/zh/family-plan/`, `/en/`, and `/en/community-support/`. Confirm labels are visible, keyboard focus is visible, and no card clips or overlaps.

- [ ] **Step 5: Commit the visual system**

```bash
git add docs/stylesheets/extra.css docs/zh docs/en scripts/check-built-site.py
git commit -m "feat: add accessible action-flow visual system"
```

## Task 6: Replace legacy Pages deployment with GitHub Actions

**Files:**
- Create: `.github/workflows/pages.yml`
- Modify: `README.md`

**Interfaces:**
- Consumes: the strict build and checker commands from Tasks 1–5.
- Produces: pull-request validation and a `main` deployment artifact.

- [ ] **Step 1: Write the workflow**

Create `.github/workflows/pages.yml` with these permission and deployment requirements:

```yaml
name: Build and deploy site
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: false
```

Use `actions/checkout@v4`, `actions/setup-python@v5` with Python `3.12`, install with `pip install .`, run `mkdocs build --strict`, run `python scripts/check-built-site.py`, upload the `site` artifact with `actions/upload-pages-artifact@v3`, and deploy only when `github.ref == 'refs/heads/main'` with `actions/deploy-pages@v4`.

- [ ] **Step 2: Add a failing local workflow-shape check**

Add to `scripts/check-built-site.py`:

```python
workflow = Path('.github/workflows/pages.yml').read_text(encoding='utf-8')
for required in ['actions/deploy-pages@v4', 'mkdocs build --strict', 'check-built-site.py', 'pages: write']:
    assert required in workflow, f"workflow missing: {required}"
```

Run the checker. Expected: PASS after the workflow is created.

- [ ] **Step 3: Correct contributor documentation**

Replace `poetry run mkdocs gh-deploy --force --clean` in `README.md` with:

```text
Do not run mkdocs gh-deploy. GitHub Actions builds and deploys main to GitHub Pages after validation.
```

Document `poetry run mkdocs build --strict` and `poetry run python scripts/check-built-site.py` as required before a PR.

- [ ] **Step 4: Commit and push**

```bash
git add .github/workflows/pages.yml README.md scripts/check-built-site.py
git commit -m "ci: deploy validated site through GitHub Pages"
git push origin main
```

- [ ] **Step 5: Switch Pages to workflow source and verify**

After the workflow is present on `main`, run:

```bash
gh api --method PUT repos/tw-us/tw-us.github.io/pages -f build_type=workflow
```

Then inspect the workflow run and Pages configuration:

```bash
gh run list --repo tw-us/tw-us.github.io --workflow pages.yml --limit 1
gh api repos/tw-us/tw-us.github.io/pages --jq '{build_type,status,html_url}'
```

Expected: `build_type` equals `workflow` and the latest run concludes `success`.

- [ ] **Step 6: Run hosted acceptance**

Load `https://tw-us.cc/zh/` and `https://tw-us.cc/en/` in a browser. Verify 200 responses, visible language switching, correct primary CTAs, and a visible build timestamp or committed release identifier. Verify the response content matches the new deployment rather than legacy `gh-pages` output.

## Task 7: Final QA and release record

**Files:**
- Modify: `README.md`
- Create: `docs/RELEASE-CHECKLIST.md`

**Interfaces:**
- Consumes: deployed V1 output.
- Produces: repeatable release checks with real hosted evidence.

- [ ] **Step 1: Add release checklist**

Create `docs/RELEASE-CHECKLIST.md` with exact checks:

```markdown
- [ ] `poetry run mkdocs build --strict` exits 0
- [ ] `poetry run python scripts/check-built-site.py` exits 0
- [ ] `/zh/` and `/en/` return HTTP 200
- [ ] Each locale’s language switch goes to the peer locale
- [ ] FAPA appears only as advocacy / public education
- [ ] No donation CTA, data-collection form, or prediction score appears
- [ ] Every committed illustration has an attribution ledger row
- [ ] Desktop and mobile screenshots show no clipped CTA or unreadable text
```

- [ ] **Step 2: Execute the entire checklist**

Run the two local commands, inspect the generated site, then inspect production in a browser at desktop and mobile widths. Record PASS/FAIL evidence in the pull request or commit description.

- [ ] **Step 3: Commit release documentation**

```bash
git add README.md docs/RELEASE-CHECKLIST.md
git commit -m "docs: add repeatable release checks"
git push origin main
```

## Visible Blockers

1. **Repository authorization:** the active GitHub CLI identity currently reports `viewerPermission: READ` and `viewerCanAdminister: false`. It cannot push commits, create/update Actions configuration, or switch GitHub Pages from legacy to workflow deployment. An organization admin must grant write/admin access to the GitHub identity used on this machine, or K2 must authenticate this machine with an account that has that access.
2. **Illustration assets:** the visual language is selected, but no individual Soco-st asset is yet approved under a captured exact license record. The action flow can ship without decorative assets; final illustration selection is blocked until individual assets and their terms are logged.
3. **Partner taxonomy:** FAPA is verified for advocacy/education. Any future preparedness or humanitarian-relief partner requires a specific organization, a verified public mission, a source URL, and a review date before it can be represented as a recommended destination.
