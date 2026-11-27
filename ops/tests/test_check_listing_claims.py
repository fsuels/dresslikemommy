#!/usr/bin/env python3
"""Offline tests for ops/scripts/check_listing_claims.py (pure functions on fixture strings)."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("dlm_check_listing_claims", ROOT / "ops/scripts/check_listing_claims.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def en(text, html=False):
    return m.scan_english_field(text, html)


def rules(findings):
    return {(f["category"], f["rule"]) for f in findings}


class EnglishRuleTests(unittest.TestCase):
    def test_each_category_has_a_positive(self):
        cases = {
            ("popularity", "bestseller"): "Our best seller this season.",
            ("popularity", "most-popular"): "The most popular matching set.",
            ("popularity", "trending"): "Trending now for summer.",
            ("popularity", "customer-favorite"): "A customer favorite, loved by moms.",
            ("stock_shipping", "in-stock"): "Always in stock and ready.",
            ("stock_shipping", "ships-today"): "Ships today from the US.",
            ("stock_shipping", "fast-shipping"): "Enjoy fast shipping.",
            ("stock_shipping", "warehouse-store"): "Shipped from our warehouse.",
            ("performance", "quick-dry"): "Quick-dry fabric for the beach.",
            ("performance", "uv-upf"): "UPF 50+ sun protection.",
            ("performance", "hypoallergenic"): "A hypoallergenic knit.",
            ("performance", "organic-eco"): "Made from organic cotton, eco-friendly.",
            ("performance", "premium-luxury"): "Premium luxury feel.",
            ("performance", "high-quality"): "High-quality stitching.",
            ("performance", "wrinkle"): "Wrinkle-free all day.",
            ("performance", "resistance"): "Shrink-resistant and fade resistant.",
            ("performance", "waterproof"): "Fully waterproof shell.",
            ("performance", "wicking"): "Moisture-wicking jersey.",
            ("performance", "perfect-fit"): "Adjustable straps ensure a perfect fit.",
            ("performance", "ensures"): "The soft knit ensures all-day comfort.",
            ("performance", "body-type-claim"): "A pattern that flatters all body types, creating a visual slimming effect; this set promises a fit.",
            ("performance", "long-lasting"): "Long-lasting and built to last.",
            ("performance", "certification"): "OEKO-TEX certified fabric.",
            ("performance", "fabric-behavior"): "Gets softer wash after wash.",
            ("health_skin", "gentle-skin"): "Gentle on little skin, dermatologist tested.",
            ("craft", "handmade"): "A hand-painted, handmade print.",
            ("reviews", "stars"): "Rated 5-star by thousands of happy moms.",
            ("internal_leak", "internal-note"): "Weight and waist measurements are not available.",
        }
        for key, text in cases.items():
            with self.subTest(rule=key):
                self.assertIn(key, rules(en(text)))

    def test_internal_note_words(self):
        for text in ("Ask the supplier for details.", "TODO fix this", "Source 1688 listing", "Lorem ipsum"):
            with self.subTest(text=text):
                self.assertIn(("internal_leak", "internal-note"), rules(en(text)))

    def test_allowlist_negatives(self):
        for text in (
            "Delivery estimates are not guarantees.",
            "Sizing is not guaranteed to match every body.",
            "We cannot guarantee exact colour on every screen.",
            "A bold organic shape print.",
            "Colour: UV print placement may vary.",
            "The gown is sewn after you order and is ready to ship in about 7 days, so please allow time.",
            "Girls' sizes run closer to true-to-size.",
            "Soft cotton blend, machine wash cold.",
            "Breathable and lightweight 100% cotton.",
        ):
            with self.subTest(text=text):
                self.assertEqual([], en(text))

    def test_find_perfect_fit_and_czech_variants_caught(self):
        self.assertIn(("performance", "perfect-fit"), rules(en("Find the perfect fit that flatters every curve.")))
        found = m.scan_translation_field("cs", "body_html", "<p>Zajišťuje perfektní střih.</p>")
        self.assertEqual({"translated_claim"}, {f["category"] for f in found})

    def test_allowlist_does_not_hide_other_claim_in_same_sentence(self):
        found = en("Not guaranteed, but a best seller.")
        self.assertIn(("popularity", "bestseller"), rules(found))

    def test_spanish_todo_is_not_a_leak(self):
        self.assertEqual([], m.scan_translation_field("es", "meta_description", "Cómodo durante todo el día."))

    def test_html_elements_split_and_tables_kept(self):
        elements = m.html_to_elements("<p>One &amp; two</p><ul><li>Soft</li><li>Warm</li></ul><table><tr><td>S</td><td>N/A</td></tr></table>")
        self.assertEqual(["One & two", "Soft", "Warm", "S", "N/A"], elements)

    def test_snippet_bounded(self):
        long = "word " * 60 + "best seller " + "word " * 60
        found = en(long)
        self.assertTrue(found)
        self.assertLessEqual(len(found[0]["snippet"]), m.SNIPPET_MAX + 2)
        self.assertLessEqual(len(found[0]["match"]), m.SNIPPET_MAX)


class UrlTests(unittest.TestCase):
    def test_vendor_host_masked_not_echoed(self):
        raw = '<p><img src="https://cbu01.alicdn.com/img/ibank/123.jpg"> see detail.1688.com/offer/9.html</p>'
        found = en(raw, html=True)
        hosts = [f for f in found if f["rule"] == "vendor-host"]
        self.assertTrue(hosts)
        blob = repr(found)
        self.assertNotIn("alicdn", blob)
        self.assertNotIn("1688.com", blob)
        self.assertTrue(all("***" in f["match"] for f in hosts))

    def test_own_and_cdn_hosts_allowed(self):
        raw = '<a href="https://www.dresslikemommy.com/pages/size-guide">chart</a><img src="https://cdn.shopify.com/s/x.jpg">'
        self.assertEqual([], [f for f in en(raw, html=True) if f["category"] == "internal_leak"])


class TranslationTests(unittest.TestCase):
    def test_glued_capital_latin(self):
        for word in ("EJede", "RCoeur", "PTisk", "AVzdušný"):
            with self.subTest(word=word):
                found = m.scan_glued_letter("Text " + word + " weiter", "de")
                self.assertEqual([word], [f["match"] for f in found])

    def test_glued_capital_negatives(self):
        for text in ("Jede Größe passt.", "Seine PDFs sind da.", "IJsbeer print", "Maat 26Wide fit", "Great T-shirt DIY set"):
            with self.subTest(text=text):
                self.assertEqual([], m.scan_glued_letter(text, "nl"))

    def test_glued_capital_before_non_latin(self):
        found = m.scan_glued_letter("E이지 케어", "ko")
        self.assertEqual(1, len(found))
        self.assertEqual([], m.scan_glued_letter("T셔츠 와 V넥", "ko"))
        self.assertEqual([], m.scan_glued_letter("E이지", "ja"))
        self.assertEqual([], m.scan_glued_letter("من US 2 إلى 26W، يُصنع", "ar"))

    def test_truncated_item(self):
        en_html = "<ul><li>Elastic waistband for comfort</li><li>Soft stretchy swimwear fabric</li></ul>"
        tr_html = "<ul><li>Cintura elástica para mayor comod.</li><li>Tejido suave y elástico para bañador.</li></ul>"
        vocab = m.build_vocab(["comodidad comodidad comodidad comodidad comodidad comodidad", "comod"])
        found = m.scan_truncated_items(en_html, tr_html, "es", vocab)
        self.assertEqual(["comod."], [f["match"] for f in found])

    def test_truncated_item_negatives(self):
        en_html = "<ul><li>Soft stretchy swimwear fabric</li></ul>"
        vocab = m.build_vocab(["comodidad " * 8, "tela tela tela"])
        # short real word at the end: no longer word starting with it -> not flagged
        self.assertEqual([], m.scan_truncated_items(en_html, "<ul><li>Tejido suave y elástico de tela.</li></ul>", "es", vocab))
        # item counts differ -> not aligned -> not flagged
        self.assertEqual([], m.scan_truncated_items(en_html, "<ul><li>a b comod.</li><li>x</li></ul>", "es", vocab))
        # no vocabulary -> never flagged; CJK skipped
        self.assertEqual([], m.scan_truncated_items(en_html, "<ul><li>Cintura elástica comod.</li></ul>", "es", None))
        self.assertEqual([], m.scan_truncated_items(en_html, "<ul><li>柔软 舒适 面料。</li></ul>", "ja", vocab))

    def test_brand_altered(self):
        altered = m.scan_brand("Dress Like Mommy picks", "Dress Like Mama Auswahl", "de")
        self.assertEqual(["Dress Like Mama"], [f["match"] for f in altered])
        self.assertEqual([], m.scan_brand("Dress Like Mommy picks", "Dress Like Mommy Auswahl", "de"))
        self.assertEqual([], m.scan_brand("see dresslikemommy.com", "siehe dresslikemommy.com", "de"))
        missing = m.scan_brand("Dress Like Mommy picks", "Unsere Auswahl", "de")
        self.assertEqual(["(missing)"], [f["match"] for f in missing])
        self.assertEqual([], m.scan_brand("Dress Like Mommy picks", "我们的精选", "zh-CN"))

    def test_language_terms(self):
        cases = {
            "es": "Tejido de secado rápido, alta calidad.",
            "de": "Unser Bestseller mit perfekter Passform.",
            "fr": "Notre meilleure vente, séchage rapide.",
            "it": "Il più venduto, asciugatura rapida.",
            "cs": "Rychleschnoucí a nejprodávanější.",
            "pl": "Szybkoschnący, wysokiej jakości.",
            "nl": "Sneldrogend en hoogwaardig.",
            "pt-BR": "O mais vendido, secagem rápida.",
        }
        for lang, text in cases.items():
            with self.subTest(lang=lang):
                self.assertTrue(m.scan_lang_terms([text], lang))

    def test_language_terms_negatives(self):
        self.assertEqual([], m.scan_lang_terms(["No garantizamos el color exacto; no se garantiza."], "es"))
        self.assertEqual([], m.scan_lang_terms(["Weiches Baumwollgemisch, maschinenwaschbar."], "de"))
        self.assertEqual([], m.scan_lang_terms(["Tejido de secado rápido."], "ko"))

    def test_english_leftover_in_translation(self):
        found = m.scan_translation_field("de", "body_html", "<p>Unser Best Seller und quick-dry Stoff.</p>")
        self.assertIn("english_leftover", {f["category"] for f in found})

    def test_polish_temu_not_flagged(self):
        self.assertEqual([], m.scan_translation_field("pl", "body_html", "<p>Dzięki temu zestawowi.</p>"))

    def test_scan_product_end_to_end(self):
        product = {
            "handle": "demo", "title": "Demo set", "descriptionHtml": "<p>A best seller.</p><ul><li>Soft fabric</li></ul>",
            "seo": {"title": "Demo", "description": "Fast shipping"},
            "translations": {"de": {"body_html": "<p>Unser Bestseller.</p><ul><li>EJede Größe</li></ul>"}},
        }
        rows = m.scan_product(product, ["de"])
        got = {(r["locale"], r["field"], r["rule"]) for r in rows}
        self.assertIn(("en", "body", "bestseller"), got)
        self.assertIn(("en", "seo_description", "fast-shipping"), got)
        self.assertIn(("de", "body", "glued-letter"), got)
        self.assertTrue(any(r["locale"] == "de" and r["category"] == "translated_claim" for r in rows))
        self.assertEqual(m.summarize(rows)["products_with_findings"], 1)

    def test_translated_size_chart_id_flagged(self):
        en_body = '<table id="size-chart" class="size-chart"><tr><td>S</td></tr></table>'
        bad = en_body.replace('id="size-chart"', 'id="tabella-taglie"')
        found = m.scan_translation_field("it", "body_html", bad, en_body)
        self.assertIn(("translation_defect", "table-id"), rules(found))
        self.assertEqual([], m.scan_table_ids(en_body, en_body.replace('"', "'")))
        self.assertEqual([], m.scan_table_ids("<table><tr></tr></table>", "<p>x</p>"))

    def test_clean_product_has_no_findings(self):
        product = {"handle": "ok", "title": "Blue floral dress", "descriptionHtml": "<p>Soft cotton blend dress.</p>",
                   "seo": {"title": "Blue dress", "description": "Matching dress for mom and daughter."}}
        self.assertEqual([], m.scan_product(product, []))


INDEX = {
    "products": {"live-dress": "ACTIVE", "old-dress": "ARCHIVED", "wip-dress": "DRAFT", "moved": "ARCHIVED", "dead-end": "ARCHIVED"},
    "collections": {"dresses": True, "hidden": False},
    "pages": {"faqs": True, "secret": False},
    "articles": {"news/good-guide": True, "news/draft-guide": False},
    "redirects": {"/products/moved": "/products/live-dress", "/products/dead-end": "/collections/gone",
                  "/collections/old": "https://www.dresslikemommy.com/collections/dresses?x=1"},
}


class CutSearchTitleTests(unittest.TestCase):
    NAME = "Pull familial assorti à motif nordique — Noël"

    def rules(self, meta_title):
        product = {"handle": "h", "title": "", "translations": {"fr": {"title": self.NAME, "meta_title": meta_title}}}
        return [r for r in m.scan_product(product, ["fr"]) if r["rule"] == "cut-search-title"]

    def test_cut_title_flagged_with_and_without_brand(self):
        self.assertEqual(len(self.rules("Pull familial assorti à motif | Dress Like Mommy")), 1)
        self.assertEqual(len(self.rules("Pull familial assorti à")), 1)

    def test_complete_or_different_title_not_flagged(self):
        self.assertEqual(self.rules("Pull familial assorti à motif nordique | Dress Like Mommy"), [])
        self.assertEqual(self.rules("Pulls de Noël pour la famille | Dress Like Mommy"), [])
        self.assertEqual(self.rules(""), [])

    def test_name_without_dash_is_skipped(self):
        self.assertEqual(m.scan_cut_search_title("Pull familial assorti", "Pull familial"), [])


class ContentRuleTests(unittest.TestCase):
    def test_trend_claims_flagged_and_plain_trend_word_not(self):
        found = m.scan_content_rules(["This season's hottest looks for mom.", "One of the biggest family fashion trends.",
                                      "Burgundy sets are a nice change."])
        self.assertEqual(2, len([f for f in found if f["rule"] == "trend-claim"]))
        self.assertEqual([], m.scan_content_rules(["Trend notes: floral prints return each spring."]))

    def test_size_up_needs_a_child_in_the_sentence_and_respects_negation(self):
        self.assertTrue(m.scan_content_rules(["For kids, sizing up one size leaves growing room."]))
        self.assertEqual([], m.scan_content_rules(["Adults who like a relaxed fit can size up."]))
        f = m.scan_content_text("<p>Do not automatically size up children's sleepwear to allow for growth.</p>", True, 2026)
        self.assertNotIn("size-up-kids", {x["rule"] for x in f})
        f = m.scan_content_text("<p>If your child is between sizes, size up.</p>", True, 2026)
        self.assertIn("size-up-kids", {x["rule"] for x in f})

    def test_true_to_size_advice_is_not_a_fit_claim_in_articles(self):
        f = m.scan_content_text("<p>Choose a size up for a relaxed fit or stay true to size for a neater look.</p>", True, 2026)
        self.assertNotIn("perfect-fit", {x["rule"] for x in f})

    def test_stale_year_narrow(self):
        self.assertTrue(m.find_stale_years("Best Mommy and Me Outfits 2025", 2026))
        self.assertTrue(m.find_stale_years("2025 Family Matching Trends", 2026))
        self.assertTrue(m.find_stale_years("Updated for 2025", 2026))
        self.assertEqual([], m.find_stale_years("Best outfits 2026", 2026))
        self.assertEqual([], m.find_stale_years("Our shop opened in 2019 and has grown since.", 2026))
        self.assertEqual([], m.find_stale_years("The best look since 2024.", 2026))
        self.assertEqual([], m.find_stale_years("2025-2026 guide", 2026))
        self.assertEqual([], m.find_stale_years("2025 and 2026 trends", 2026))
        self.assertEqual(1, len(m.find_stale_years("Photo taken in 2024", 2026, loose=True)))
        self.assertEqual("stale_year", m.scan_stale_years("Best of 2025", 2026)[0]["category"])

    def test_alt_text_extracted_and_scanned(self):
        raw = '<img src="a.jpg" alt="2025 trends matching outfit"><img alt=\'Plain photo\'><img src="b.jpg">'
        self.assertEqual(["2025 trends matching outfit", "Plain photo"], m.extract_alt_texts(raw))
        f = m.scan_content_text(raw, True, 2026)
        self.assertTrue(any(x["rule"] == "stale-year" and x["snippet"].startswith("alt: ") for x in f))

    def test_unanswered_questions(self):
        html = "<h2>Do they run small?</h2><h2>Shipping</h2><p>Text.</p><h3>Can I return it?</h3><p>Yes within 30 days.</p>"
        self.assertEqual(["Do they run small?"], m.find_unanswered_questions(html))
        parent = "<h2>Pajamas, Sweaters or Outfits?</h2><h3>Pajamas</h3><p>Soft.</p>"
        self.assertEqual([], m.find_unanswered_questions(parent))
        det = "<details><summary>How long is delivery?</summary></details><details><summary>Returns?</summary><p>30 days.</p></details>"
        self.assertEqual(["How long is delivery?"], m.find_unanswered_questions(det))
        dl = "<dl><dt>Is it soft?</dt><dd></dd><dt>Sizes?</dt><dd>S to XL</dd></dl>"
        self.assertEqual(["Is it soft?"], m.find_unanswered_questions(dl))
        self.assertEqual(["Is the last one empty?"], m.find_unanswered_questions("<h2>Is the last one empty?</h2><img src='x'>"))

    def test_duplicate_sentences(self):
        s = "Check the size chart on each product page and measure rather than guess."
        self.assertEqual([s], m.find_duplicate_sentences([s, "Other text here.", s]))
        self.assertEqual([], m.find_duplicate_sentences(["Short repeat.", "Short repeat."]))
        self.assertEqual([], m.find_duplicate_sentences(["Navy Orange Floral Mommy and Me Dresses Tiered Tie Strap Dress"] * 2))
        self.assertEqual([], m.find_duplicate_sentences([s, s], boilerplate={m._norm_sentence(s)}))
        self.assertEqual({m._norm_sentence(s)}, m.build_boilerplate(["<p>%s</p>" % s] * 3, min_resources=3))

    def test_normalize_and_extract_links(self):
        self.assertEqual("/products/live-dress", m.normalize_link("https://www.dresslikemommy.com/de/products/live-dress/?variant=1#x"))
        self.assertEqual("/collections/dresses", m.normalize_link("/en-gb/collections/dresses"))
        self.assertEqual("/pages/faqs", m.normalize_link("/pages/faqs"))
        self.assertIsNone(m.normalize_link("https://www.pinterest.com/x"))
        self.assertIsNone(m.normalize_link("mailto:a@b.com"))
        self.assertIsNone(m.normalize_link("#top"))
        raw = '<a href="/products/a">x</a><a href="/products/a">y</a><a href=\'/pages/faqs\'>z</a>'
        self.assertEqual(["/products/a", "/pages/faqs"], m.extract_internal_links(raw))

    def test_classify_path(self):
        self.assertEqual(("product", "p"), m.classify_path("/collections/c/products/p"))
        self.assertEqual(("collection", "c"), m.classify_path("/collections/c"))
        self.assertEqual(("page", "faqs"), m.classify_path("/pages/faqs"))
        self.assertIsNone(m.classify_path("/pages/search-results/some term"))
        self.assertEqual(("article", "news/g"), m.classify_path("/blogs/news/g"))
        self.assertIsNone(m.classify_path("/collections/all"))
        self.assertIsNone(m.classify_path("/cart"))

    def test_check_link(self):
        self.assertIsNone(m.check_link("/products/live-dress", INDEX))
        self.assertIsNone(m.check_link("/collections/dresses/products/live-dress", INDEX))
        self.assertIsNone(m.check_link("/blogs/news/good-guide", INDEX))
        self.assertEqual("link-inactive-product", m.check_link("/products/old-dress", INDEX)["rule"])
        self.assertEqual("link-inactive-product", m.check_link("/products/wip-dress", INDEX)["rule"])
        self.assertEqual("link-missing", m.check_link("/products/nope", INDEX)["rule"])
        self.assertEqual("link-unpublished", m.check_link("/collections/hidden", INDEX)["rule"])
        self.assertEqual("link-missing", m.check_link("/pages/nope", INDEX)["rule"])
        self.assertEqual("link-unpublished", m.check_link("/pages/secret", INDEX)["rule"])
        self.assertEqual("link-unpublished", m.check_link("/blogs/news/draft-guide", INDEX)["rule"])
        red = m.check_link("/products/moved", INDEX)
        self.assertEqual("link-redirected", red["rule"])
        self.assertEqual("/products/moved -> /products/live-dress", red["snippet"])
        self.assertEqual("/collections/old -> /collections/dresses", m.check_link("/collections/old", INDEX)["snippet"])
        self.assertEqual("link-redirect-dead", m.check_link("/products/dead-end", INDEX)["rule"])

    def test_scan_links_skips_known_paths(self):
        raw = '<a href="/products/old-dress">a</a><a href="/products/live-dress">b</a>'
        self.assertEqual(1, len(m.scan_links(raw, INDEX)))
        self.assertEqual([], m.scan_links(raw, INDEX, skip=["/products/old-dress"]))

    def test_content_resource_scan_and_noise_filters(self):
        art = {"handle": "g", "title": "Best Matching Looks 2025", "body": "<h2>Any tips?</h2><h2>More</h2><p>Order a size up for kids.</p>",
               "summary": "", "seo": {"title": "", "description": ""}, "translations": {
                   "ja": {"body_html": "<p>Dress Like Mommyでは家族の装いを提案します。</p>"},
                   "es": {"body_html": "<p>Pide una talla más para los niños.</p>"}}}
        rows = m.scan_content_resource("article", art, ["ja", "es"], 2026, None, INDEX)
        got = {(r["locale"], r["rule"]) for r in rows}
        self.assertIn(("en", "stale-year"), got)
        self.assertIn(("en", "unanswered-faq"), got)
        self.assertIn(("en", "size-up-kids"), got)
        self.assertIn(("es", "size-advice"), got)
        self.assertFalse([r for r in rows if r["rule"] == "brand-altered"])
        self.assertTrue(all(r["resource"] == "article" for r in rows))

    def test_group_rows_collapses_locale_copies(self):
        base = {"resource": "article", "handle": "g", "field": "body", "category": "translated_claim", "rule": "size-advice",
                "snippet": "x", "match": "una talla más"}
        groups = m.group_rows([dict(base, locale="es"), dict(base, locale="it", match="una taglia in più")])
        self.assertEqual(1, len(groups))
        self.assertEqual(["es", "it"], groups[0]["locales"])


if __name__ == "__main__":
    unittest.main()
