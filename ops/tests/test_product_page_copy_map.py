"""Product-page copy map: each locale renders only its language family plus the English fallback."""

from pathlib import Path
import json
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ops.scripts import build_product_page_copy_map as b  # noqa: E402

SNIPPET = ROOT / "snippets" / "product-page-copy-map.liquid"
GUARD = re.compile(r"\{%- if dlm_copy_root == '([a-z]+)' %\}\n(.*?)\{%- endif %\}\n", re.S)


def root_for(iso_code):
    """Mirror of the snippet's Liquid root assignment."""
    root = iso_code.lower().replace("_", "-").split("-")[0]
    return "no" if root == "nb" else root


def render_for(text, iso_code):
    """Minimal stand-in for Liquid: keep only the branches that match this locale's root."""
    root = root_for(iso_code)
    text = GUARD.sub(lambda m: m.group(2) if m.group(1) == root else "", text)
    text = re.sub(r"\{% comment %\}.*?\{% endcomment %\}", "", text, flags=re.S)
    text = re.sub(r"\{%- liquid.*?-%\}", "", text, flags=re.S)
    return json.loads(text)


def lookup(copy_map, locale):
    """Port of getProductPageCopy() in assets/global.js and its three copies."""
    locale = locale.replace("_", "-").lower()
    root = locale.split("-")[0]
    candidates = [locale]
    if root and root != locale:
        candidates.append(root)
    if root == "pt":
        candidates += ["pt-BR", "pt-PT"]
    if root == "ro":
        candidates += ["ro", "ro-RO"]
    if root == "no":
        candidates += ["no", "nb"]
    for candidate in candidates:
        for key in copy_map:
            if key.lower() == candidate.lower():
                return copy_map[key]
    return copy_map.get("en")


class CopyMapSnippetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SNIPPET.read_text(encoding="utf-8")
        cls.full = b.read_snippet(cls.text)

    def test_every_locale_resolves_to_the_same_copy_as_the_full_map(self):
        for iso in ["en", "de", "fr", "ar", "pt-BR", "pt-PT", "nb", "no", "ro", "ro-RO", "zh-CN", "zh-TW", "hr-HR", "ja"]:
            with self.subTest(iso=iso):
                rendered = render_for(self.text, iso)
                self.assertEqual(lookup(rendered, iso), lookup(self.full, iso))
                self.assertIn("en", rendered)

    def test_rendered_page_carries_only_its_language_family(self):
        self.assertEqual(sorted(render_for(self.text, "de")), ["de", "en"])
        self.assertEqual(sorted(render_for(self.text, "en")), ["en"])
        self.assertEqual(sorted(render_for(self.text, "pt-BR")), ["en", "pt-BR", "pt-PT"])
        self.assertEqual(sorted(render_for(self.text, "nb")), ["en", "nb", "no"])

    def test_unknown_locale_falls_back_to_english(self):
        rendered = render_for(self.text, "fr-CA-x")
        self.assertEqual(lookup(rendered, "xx"), self.full["en"])

    def test_render_round_trips_through_read_snippet(self):
        self.assertEqual(b.read_snippet(b.render_snippet(self.full)), self.full)
        self.assertEqual(b.render_snippet(self.full), self.text)

    def test_script_close_tag_is_escaped(self):
        rendered = b.render_snippet({"en": {"k": "a</script>b"}})
        self.assertNotIn("</script", rendered)
        self.assertEqual(b.read_snippet(rendered)["en"]["k"], "a</script>b")


if __name__ == "__main__":
    unittest.main()
