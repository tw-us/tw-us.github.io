"""Deterministic checks for the public static site artifact."""

from pathlib import Path
from html.parser import HTMLParser
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


class FieldGuideText(HTMLParser):
    """Collect reader-visible text inside the public field-guide surface only."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._guide_depth = 0
        self._ignored_depth = 0
        self.parts: list[str] = []
        self._void_tags = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = dict(attrs).get("class", "") or ""
        if self._guide_depth == 0 and "field-guide" in classes.split():
            self._guide_depth = 1
        elif self._guide_depth and tag not in self._void_tags:
            self._guide_depth += 1
        if self._guide_depth and tag in {"script", "style"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self._guide_depth and tag in {"script", "style"} and self._ignored_depth:
            self._ignored_depth -= 1
        if self._guide_depth and tag not in self._void_tags:
            self._guide_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._guide_depth and not self._ignored_depth:
            self.parts.append(data)


class MetaTags(HTMLParser):
    """Collect <meta> tags keyed by their property/name, order- and quote-insensitive.

    The minify plugin rewrites attribute order and strips optional quotes, so the
    built HTML must be parsed rather than matched with a literal string.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "meta":
            return
        attributes = dict(attrs)
        key = attributes.get("property") or attributes.get("name")
        if key:
            self.tags.setdefault(key, []).append(attributes.get("content") or "")


def meta_tags(body: str) -> dict[str, list[str]]:
    parser = MetaTags()
    parser.feed(body)
    parser.close()
    return parser.tags


def visible_field_guide_text(body: str) -> str:
    parser = FieldGuideText()
    parser.feed(body)
    parser.close()
    text = " ".join(parser.parts)
    assert text.strip(), "missing reader-visible field-guide text"
    return text

localized_pages = [
    f"{locale}/{page}index.html"
    for locale in ("zh", "en")
    for page in ("", "family-plan/", "community-support/", "when-things-change/")
]
required = ["index.html", "archive/index.html", *localized_pages]
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
        assert f"href={destination}" in body or f'href=\"{destination}\"' in body, f"missing journey destination {destination}: {relative}"
    assert "grid cards" not in body and "grid.cards" not in body, f"generic card grid found: {relative}"

landing = (SITE / "index.html").read_text(encoding="utf-8")
assert has_class(landing, "landing-page"), "root must be the Calm Field Guide landing page"
assert class_count(landing, "language-path") == 2, "landing must expose exactly two language paths"
for destination in ("zh/", "en/", "archive/"):
    assert destination in landing, f"landing missing destination: {destination}"
assert "Choose a language to begin" not in landing, "legacy language chooser copy remains at root"

archive = (SITE / "archive/index.html").read_text(encoding="utf-8")
assert has_class(archive, "archive-guide"), "archive needs an explicit archive guide shell"
for legacy_destination in ("/現在怎麼做/", "/緊急時怎麼做/", "/其他資源/"):
    assert legacy_destination in archive, f"archive missing retained legacy route: {legacy_destination}"

family_contracts = {
    "zh/family-plan/index.html": ("今天先做這三件事", "不用登入，也不會儲存你的聯絡人、文件或寫下的安排", "離線保存在家人都拿得到的地方"),
    "en/family-plan/index.html": ("Three things to do today", "do not store contacts, documents, or family plans", "without internet access"),
}
for relative, strings in family_contracts.items():
    body = (SITE / relative).read_text(encoding="utf-8")
    visible_text = visible_field_guide_text(body)
    assert has_class(body, "notebook-sheet"), f"missing notebook sheet: {relative}"
    assert class_count(body, "notebook-prompt") >= 3, f"missing notebook prompts: {relative}"
    field_guide_match = re.search(r'<(?:div|main) class=field-guide>(.*?)</(?:div|main)>', body, re.DOTALL)
    assert field_guide_match, f"missing field-guide scope: {relative}"
    assert "<form" not in field_guide_match.group(1).lower(), f"form surface is prohibited: {relative}"
    assert has_class(body, "source-record"), f"missing source record: {relative}"
    for text in strings:
        assert text in visible_text, f"missing visible family safety copy {text!r}: {relative}"

editorial_contracts = {
    "zh/community-support/index.html": ("先確定你和家人聯絡得上", "原始來源", "不是募款、回報災情或安排救援的管道", "不提供緊急救援"),
    "en/community-support/index.html": ("Start with your family’s contact plan", "original source", "does not collect donations or incident reports", "does not provide emergency relief"),
    "zh/when-things-change/index.html": ("台灣官方公告", "消息有變化時", "官方發布明確緊急指示", "不是台灣或美國政府的官方警報來源"),
    "en/when-things-change/index.html": ("authorities in Taiwan", "When concerning news appears", "authorities issue a clear emergency instruction", "not an official alert source of the Taiwan or U.S. government"),
}
for relative, strings in editorial_contracts.items():
    body = (SITE / relative).read_text(encoding="utf-8")
    visible_text = visible_field_guide_text(body)
    assert has_class(body, "source-record"), f"missing source record: {relative}"
    for text in strings:
        assert text in visible_text, f"missing visible editorial safety copy {text!r}: {relative}"

for relative in localized_pages:
    body = (SITE / relative).read_text(encoding="utf-8")
    assert "Reviewed on: 2026-08-31" in body or relative.endswith("/index.html") and relative.count("/") == 1, f"missing review date: {relative}"

OG_IMAGE_URL = "https://tw-us.cc/assets/og-image.png"
OG_IMAGE_WIDTH = "1731"
OG_IMAGE_HEIGHT = "909"

og_asset = SITE / "assets" / "og-image.png"
assert og_asset.is_file(), "missing built social preview asset: site/assets/og-image.png"
header = og_asset.read_bytes()[:24]
assert header[:8] == b"\x89PNG\r\n\x1a\n", "social preview asset is not a PNG"
assert header[12:16] == b"IHDR", "social preview asset has no PNG header chunk"
built_width = int.from_bytes(header[16:20], "big")
built_height = int.from_bytes(header[20:24], "big")
assert (built_width, built_height) == (int(OG_IMAGE_WIDTH), int(OG_IMAGE_HEIGHT)), (
    f"social preview asset must stay {OG_IMAGE_WIDTH}x{OG_IMAGE_HEIGHT}, got {built_width}x{built_height}"
)

social_pages = [
    "index.html",
    "zh/index.html",
    "en/family-plan/index.html",
    "archive/index.html",
]
for relative in social_pages:
    body = (SITE / relative).read_text(encoding="utf-8")
    tags = meta_tags(body)
    for key, expected in (
        ("og:type", "website"),
        ("og:image", OG_IMAGE_URL),
        ("og:image:secure_url", OG_IMAGE_URL),
        ("og:image:type", "image/png"),
        ("og:image:width", OG_IMAGE_WIDTH),
        ("og:image:height", OG_IMAGE_HEIGHT),
        ("twitter:card", "summary_large_image"),
        ("twitter:image", OG_IMAGE_URL),
    ):
        values = tags.get(key, [])
        assert len(values) == 1, f"expected exactly one {key} tag, got {len(values)}: {relative}"
        assert values[0] == expected, f"{key} must be {expected!r}, got {values[0]!r}: {relative}"
    for alt_key in ("og:image:alt", "twitter:image:alt"):
        alts = tags.get(alt_key, [])
        assert len(alts) == 1, f"expected exactly one {alt_key} tag, got {len(alts)}: {relative}"
        assert "台美緊急連線" in alts[0] and "TW–US Crisis Connect" in alts[0], (
            f"{alt_key} must name the brand in both languages: {relative}"
        )
    titles = tags.get("og:title", [])
    assert len(titles) == 1 and titles[0].strip(), f"missing single og:title: {relative}"
    urls = tags.get("og:url", [])
    assert len(urls) == 1 and urls[0].startswith("https://tw-us.cc/"), f"og:url must be absolute: {relative}"
    assert "<link href=https://tw-us.cc/" in body or 'rel="canonical"' in body, f"missing canonical link: {relative}"
    assert "<title>" in body, f"missing title element: {relative}"
    assert "assets/og-image.png" not in body.replace(OG_IMAGE_URL, ""), (
        f"social preview image must never be referenced by a relative path: {relative}"
    )

workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
for workflow_contract in (
    "actions/configure-pages@v5", "actions/upload-pages-artifact@v4", "actions/deploy-pages@v4",
    "mkdocs build --strict", "check-built-site.py", "pages: write", "needs: build",
):
    assert workflow_contract in workflow, f"workflow missing: {workflow_contract}"

print("PASS: Calm Field Guide shell, bilingual journeys, and action-flow safety contracts are present")
