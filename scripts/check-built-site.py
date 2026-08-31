"""Deterministic checks for the public static site artifact."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

required = [
    SITE / "index.html",
    SITE / "zh" / "index.html",
    SITE / "en" / "index.html",
]
for path in required:
    assert path.is_file(), f"missing built page: {path.relative_to(ROOT)}"

for relative, peer in [("zh/index.html", "/en/"), ("en/index.html", "/zh/")]:
    body = (SITE / relative).read_text(encoding="utf-8")
    assert "language-switch" in body, f"missing language switcher: {relative}"
    assert peer in body, f"missing peer language route {peer}: {relative}"

expected_copy = {
    "zh/index.html": ["建立家人支援計畫", "把你的支援能力帶進社群"],
    "zh/family-plan/index.html": ["今天先做這三件事", "本站不會要求登入"],
    "zh/when-things-change/index.html": ["官方公告為準", "提高注意"],
    "en/index.html": ["Build a family support plan", "Support responsibly"],
    "en/community-support/index.html": ["does not collect donations"],
}
for relative, strings in expected_copy.items():
    body = (SITE / relative).read_text(encoding="utf-8")
    for text in strings:
        assert text in body, f"missing expected copy {text!r}: {relative}"

workflow = Path('.github/workflows/pages.yml').read_text(encoding='utf-8')
for required in [
    'actions/configure-pages@v5',
    'actions/upload-pages-artifact@v4',
    'actions/deploy-pages@v4',
    'mkdocs build --strict',
    'check-built-site.py',
    'pages: write',
    'needs: build',
]:
    assert required in workflow, f"workflow missing: {required}"

print("PASS: core zh/en routes, language switches, and action-copy contracts are present")
