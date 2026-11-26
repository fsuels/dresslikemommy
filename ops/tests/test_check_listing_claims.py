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
            "Use the size chart to find your perfect fit.",
            "A bold organic shape print.",
            "Colour: UV print placement may vary.",
            "The gown is sewn after you order and is ready to ship in about 7 days, so please allow time.",
            "Girls' sizes run closer to true-to-size.",
            "Soft cotton blend, machine wash cold.",
            "Breathable and lightweight 100% cotton.",
        ):
            with self.subTest(text=text):
                self.assertEqual([], en(text))

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

    def test_clean_product_has_no_findings(self):
        product = {"handle": "ok", "title": "Blue floral dress", "descriptionHtml": "<p>Soft cotton blend dress.</p>",
                   "seo": {"title": "Blue dress", "description": "Matching dress for mom and daughter."}}
        self.assertEqual([], m.scan_product(product, []))


if __name__ == "__main__":
    unittest.main()
