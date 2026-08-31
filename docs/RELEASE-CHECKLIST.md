# Calm Field Guide Release Checklist

## Static and safety gate

- [ ] `poetry run mkdocs build --strict` exits 0.
- [ ] `poetry run python scripts/check-built-site.py` exits 0.
- [ ] `git diff --check` exits 0.
- [ ] No V1 route contains more than one `<main>` landmark.
- [ ] No V1 family-plan route contains a form, sign-in, data collection, or browser persistence surface.
- [ ] No unledgered third-party illustration is committed.
- [ ] No donation CTA, incident-report form, risk score, or prediction claim appears.

## Browser gate

- [ ] `/`, `/zh/`, `/en/`, `/zh/family-plan/`, and `/en/community-support/` return a visible page.
- [ ] `/zh/` and `/en/` show exactly three preparation journey links and a visible peer-language link.
- [ ] Family-plan pages show the notebook prompt pattern and the local-only privacy statement.
- [ ] Community and signal guidance retain the official-source-first safety language.
- [ ] Desktop and 390px mobile widths have no horizontal overflow or clipped primary route.
- [ ] Keyboard focus is visibly outlined on interactive elements.

## Hosted gate

- [ ] GitHub Pages workflow is terminal `success` for the release commit.
- [ ] `https://tw-us.cc/zh/` and `https://tw-us.cc/en/` visibly show the Calm Field Guide shell rather than the prior documentation/card shell.
