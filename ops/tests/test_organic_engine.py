import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ops.scripts import organic_engine as engine  # noqa: E402

INVENTORY = {
    "collections": [
        {"handle": "family-sweaters", "products": 40},
        {"handle": "christmas-pajamas", "products": 12},
        {"handle": "mommy-and-me", "products": 400},
        {"handle": "family-swimsuits", "products": 0},
    ],
    "articles": [{"handle": "already-live"}],
}


def article(body_words=750, links=("family-sweaters", "christmas-pajamas", "mommy-and-me"), extra="", handle="new-guide"):
    anchors = " ".join(f'<a href="/collections/{h}">{h}</a>' for h in links)
    body = "<h2>A</h2><h2>B</h2><h2>C</h2><p>" + " ".join(["word"] * body_words) + f" {anchors} {extra}</p>"
    return (
        "---\n"
        "title: Family Christmas Photo Outfit Ideas\n"
        f"handle: {handle}\n"
        "summary: Ideas for coordinated family Christmas photos.\n"
        "tags: christmas, family photos\n"
        "seo_title: Family Christmas Photo Outfit Ideas for 2026\n"
        "seo_description: " + "Coordinated family Christmas photo outfit ideas for mom, dad, kids and baby, with color palettes, sizing tips and links." + "\n"
        "---\n" + body
    )


class LintArticleTest(unittest.TestCase):
    def lint(self, text):
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as handle:
            handle.write(text)
        return engine.lint_article(Path(handle.name), INVENTORY)

    def test_good_article_passes(self):
        result = self.lint(article())
        self.assertTrue(result["pass"], result["errors"])

    def test_short_article_fails(self):
        self.assertIn("body", " ".join(self.lint(article(body_words=300))["errors"]))

    def test_needs_three_collection_links(self):
        self.assertFalse(self.lint(article(links=("family-sweaters",)))["pass"])

    def test_thin_or_missing_collection_link_fails(self):
        errors = " ".join(self.lint(article(links=("family-sweaters", "mommy-and-me", "family-swimsuits", "nope")))["errors"])
        self.assertIn("thin collection", errors)
        self.assertIn("missing collection", errors)

    def test_unsupported_claims_fail(self):
        for claim in ("Order by December 8 for Christmas", "arrives if you order by Dec 5",
                      "Fast shipping on every order", "our best sellers", "ships from our warehouse", "sourced on 1688", "matching dog sweater"):
            with self.subTest(claim=claim):
                self.assertIn("banned", " ".join(self.lint(article(extra=claim))["errors"]))

    def test_external_links_fail(self):
        self.assertFalse(self.lint(article(extra='<a href="https://example.com/x">x</a>'))["pass"])

    def test_existing_handle_warns(self):
        self.assertTrue(self.lint(article(handle="already-live"))["warnings"])


class MetaGuardTest(unittest.TestCase):
    def test_lengths_and_claims(self):
        self.assertEqual(engine.check_meta("Matching Family Christmas Sweaters", "x" * 130), [])
        self.assertTrue(engine.check_meta("Short", None))
        self.assertTrue(engine.check_meta(None, "x" * 200))
        self.assertTrue(engine.check_meta("Bestseller Family Sweaters Ship Fast", None))

    def test_theme_owned_collection_refused(self):
        class Args:
            handle = "mommy-and-me"
        self.assertEqual(engine.cmd_collection_seo(Args), 2)


class LinkHealthTest(unittest.TestCase):
    def test_dead_links_and_claims(self):
        body = ('<a href="/products/live-one">a</a> <a href="https://www.dresslikemommy.com/products/gone?variant=1">b</a> '
                '<a href="/de/collections/xmas/products/gone-too">c</a> <a href="/collections/family-matching">d</a> '
                '<a href="/collections/christmas-pajamas">e</a> One of our bestsellers with a happiness guarantee.')
        health = engine.link_health(body, {"live-one"}, {"christmas-pajamas"})
        self.assertEqual(health["dead_products"], ["gone", "gone-too"])
        self.assertEqual(health["dead_collections"], ["family-matching"])
        self.assertIn("happiness guarantee", health["banned_claims"])
        self.assertIn("bestsellers", health["banned_claims"])

    def test_clean_body(self):
        body = '<a href="/products/live-one">a</a> <a href="/collections/christmas-pajamas">b</a> Standard shipping included.'
        self.assertFalse(any(engine.link_health(body, {"live-one"}, {"christmas-pajamas"}).values()))


class TranslationCheckTest(unittest.TestCase):
    SRC = '<h2>Pick</h2><p>Start with <a href="/collections/couples">couples</a> and <a href="/blogs/news/guide">the guide</a>.</p>'

    def test_localized_links_pass(self):
        good = '<h2>Επιλογή</h2><p>Ξεκινήστε με <a href="/el/collections/couples">ζευγάρια</a> και <a href="/el/blogs/news/guide">τον οδηγό</a>.</p>'
        self.assertEqual(engine.check_translation("body_html", self.SRC, good, "el"), [])

    def test_unprefixed_or_dropped_links_fail(self):
        bad = '<h2>Επιλογή</h2><p>Ξεκινήστε με <a href="/collections/couples">ζευγάρια</a> και τον οδηγό.</p>'
        problems = " ".join(engine.check_translation("body_html", self.SRC, bad, "el"))
        self.assertIn("<a> count", problems)
        self.assertIn("hrefs differ", problems)

    def test_pt_br_uses_pt_folder(self):
        self.assertEqual(engine.locale_prefix("pt-BR"), "/pt")
        self.assertIn('href="/pt/collections/x"', engine.localize_hrefs('<a href="/collections/x">x</a>', "pt-BR"))

    def test_meta_length_caps(self):
        self.assertTrue(engine.check_translation("meta_description", "x" * 150, "y" * 170, "de"))


if __name__ == "__main__":
    unittest.main()
