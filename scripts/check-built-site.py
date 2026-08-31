"""Deterministic checks for the public static site artifact."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CSS = ROOT / "docs" / "stylesheets" / "extra.css"
LEDGER = ROOT / "docs" / "assets" / "illustrations" / "ATTRIBUTION.md"


def has_class(body: str, class_name: str) -> bool:
    """Match minified or quoted single-class attributes."""
    return re.search(rf'class=(?:["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\']|{re.escape(class_name)}(?:[ >]))', body) is not None


def class_count(body: str, class_name: str) -> int:
    return len(re.findall(rf'class=(?:["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\']|{re.escape(class_name)}(?:[ >]))', body))

localized_pages = [
    f"{locale}/{page}index.html"
    for locale in ("zh", "en")
    for page in ("", "family-plan/", "community-support/", "when-things-change/")
]
required = ["index.html", *localized_pages]
for relative in required:
    assert (SITE / relative).is_file(), f"missing built page: site/{relative}"

css = CSS.read_text(encoding="utf-8")
for selector in (
    ".field-guide",
    ".field-guide-header",
    ".route-marker",
    ".journey",
    ".journey-stop",
    ".notebook-sheet",
    ".source-record",
):
    assert selector in css, f"shared stylesheet missing selector: {selector}"
for token in ("#fbfaf4", "#edf2ea", "#31634b", "#e9785d", "#f2c65c", "#18211d", "#cbd4c8"):
    assert token in css.lower(), f"shared stylesheet missing design token: {token}"
for accessibility_rule in (":focus-visible", "prefers-reduced-motion"):
    assert accessibility_rule in css, f"shared stylesheet missing: {accessibility_rule}"

assert LEDGER.is_file(), "missing illustration attribution ledger"
ledger = LEDGER.read_text(encoding="utf-8")
for column in ("Source URL", "License / terms snapshot", "Checked date", "Page assignment"):
    assert column in ledger, f"attribution ledger missing column: {column}"

for relative, peer in (("zh/index.html", "/en/"), ("en/index.html", "/zh/")):
    body = (SITE / relative).read_text(encoding="utf-8")
    assert "field-guide" in body, f"missing field-guide root: {relative}"
    assert "language-switch" in body and peer in body, f"missing peer language route: {relative}"
    assert has_class(body, "journey"), f"missing journey: {relative}"
    assert class_count(body, "journey-stop") == 3, f"homepage must have three journey stops: {relative}"
    for destination in ("family-plan/", "community-support/", "when-things-change/"):
        assert f"href={destination}" in body or f'href="{destination}"' in body, f"missing journey destination {destination}: {relative}"
    assert "grid cards" not in body and "grid.cards" not in body, f"generic card grid found: {relative}"

family_contracts = {
    "zh/family-plan/index.html": ("今天先做這三件事", "本站不會要求登入，也不會儲存你的聯絡人、文件或家庭計畫", "離線保存"),
    "en/family-plan/index.html": ("Start with these three actions today", "does not ask you to sign in or store your contacts, documents, or family plan", "access offline"),
}
for relative, strings in family_contracts.items():
    body = (SITE / relative).read_text(encoding="utf-8")
    assert has_class(body, "notebook-sheet"), f"missing notebook sheet: {relative}"
    assert class_count(body, "notebook-prompt") >= 3, f"missing notebook prompts: {relative}"
    field_guide_match = re.search(r'<(?:div|main) class=field-guide>(.*?)</(?:div|main)>', body, re.DOTALL)
    assert field_guide_match, f"missing field-guide scope: {relative}"
    assert "<form" not in field_guide_match.group(1).lower(), f"form surface is prohibited: {relative}"
    assert has_class(body, "source-record"), f"missing source record: {relative}"
    for text in strings:
        assert text in body, f"missing family safety copy {text!r}: {relative}"

editorial_contracts = {
    "zh/community-support/index.html": ("先讓你與家人的聯絡計畫可運作", "分享已驗證的資訊", "不要透過本站自行募集款項、收集受災資訊或派遣救援", "不是緊急救援提供者"),
    "en/community-support/index.html": ("Prepare your own family connection first", "Share verified information", "does not collect donations, incident reports, or emergency dispatch requests", "not as an emergency-relief provider"),
    "zh/when-things-change/index.html": ("官方公告為準", "提高注意", "官方發布明確緊急指示", "不是台灣或美國政府的官方警報來源，也不能單獨決定"),
    "en/when-things-change/index.html": ("official announcements", "Heightened attention", "authorities issue a clear emergency instruction", "not an official Taiwan or U.S. government alert source and must not decide"),
}
for relative, strings in editorial_contracts.items():
    body = (SITE / relative).read_text(encoding="utf-8")
    assert has_class(body, "source-record"), f"missing source record: {relative}"
    for text in strings:
        assert text in body, f"missing editorial safety copy {text!r}: {relative}"

for relative in localized_pages:
    body = (SITE / relative).read_text(encoding="utf-8")
    assert "Reviewed on: 2026-08-31" in body or relative.endswith("/index.html") and relative.count("/") == 1, f"missing review date: {relative}"

workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
for workflow_contract in (
    "actions/configure-pages@v5", "actions/upload-pages-artifact@v4", "actions/deploy-pages@v4",
    "mkdocs build --strict", "check-built-site.py", "pages: write", "needs: build",
):
    assert workflow_contract in workflow, f"workflow missing: {workflow_contract}"

print("PASS: Calm Field Guide shell, bilingual journeys, and action-flow safety contracts are present")
