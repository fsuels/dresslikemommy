import copy
import json
from pathlib import Path
import tempfile
import unittest

from offline_translation import numbers, reuse, verify_rows, verify_text


class OfflineVerificationTests(unittest.TestCase):
    def base(self, source="<p>100% cotton; length 12.5 cm.</p>"):
        return {"resourceId": "gid://shopify/Product/1", "locale": "da", "key": "body_html",
                "source": source, "sourceDigest": "opaque-live-digest", "before": None}

    def test_localized_decimals_and_equivalent_units(self):
        result = verify_text("<p>12.5 cm; 2 inches; 1,000 kg.</p>",
                             "<p>12,5 см; 2 дюйма; 1 000 кг.</p>", "ru")
        self.assertEqual(result["errors"], [])
        result = verify_text("<p>12.5 cm; 2 inches; 1,000 kg.</p>",
                             "<p>12,5 cm; 2 tommer; 1.000 kg.</p>", "da")
        self.assertEqual(result["errors"], [])

    def test_arabic_digits_and_decimal_mark(self):
        self.assertEqual(numbers("١٢٫٥", "ar"), ["12.5"])
        self.assertEqual(numbers("١٬٠٠٠", "ar"), ["1000"])

    def test_negative_and_range_are_distinct(self):
        self.assertEqual(numbers("-5 and 1-3 and 1 – 3"), ["-5", "1", "3", "1", "3"])
        self.assertIn("numeric_values_changed", verify_text("-5 cm", "5 cm", "da")["errors"])

    def test_attached_units_cannot_change(self):
        self.assertIn("measurement_units_changed_or_unrecognized", verify_text("2cm", "2mm", "da")["errors"])

    def test_table_cell_swap_caught_even_when_global_values_same(self):
        source = '<table id="size-chart"><tr><th>Chest (cm)</th><th>Length (cm)</th></tr><tr><td>60</td><td>80</td></tr></table>'
        target = '<table id="size-chart"><tr><th>Bryst (cm)</th><th>Længde (cm)</th></tr><tr><td>80</td><td>60</td></tr></table>'
        self.assertIn("table_cell_numbers_units_or_shape_changed", verify_text(source, target, "da")["errors"])

    def test_missing_table_or_row_caught(self):
        source = '<table><tr><td>60</td></tr><tr><td>80</td></tr></table>'
        target = '<table><tr><td>60 80</td></tr></table>'
        self.assertIn("table_cell_numbers_units_or_shape_changed", verify_text(source, target, "da")["errors"])

    def test_table_size_codes_cannot_change(self):
        self.assertIn("table_cell_numbers_units_or_shape_changed", verify_text(
            '<table><tr><td>Mother S</td><td>60</td></tr></table>',
            '<table><tr><td>Mor M</td><td>60</td></tr></table>', "da")["errors"])

    def test_html_attributes_with_angle_bracket_parsed_correctly(self):
        source = '<p title="x > y"><a href="/pages/help?a=1&amp;b=2">Help</a></p>'
        target = '<p title="x > y"><a href="/pages/help?a=1&amp;b=2">Hjælp</a></p>'
        self.assertEqual(verify_text(source, target, "da")["errors"], [])
        changed = target.replace('/pages/help', '/pages/other')
        self.assertIn("html_structure_or_attributes_changed", verify_text(source, changed, "da")["errors"])

    def test_tokens_and_scripts_cannot_change(self):
        self.assertIn("liquid_tokens_changed", verify_text("Size {{ size }}", "Størrelse {{ other }}", "da")["errors"])
        self.assertIn("translation_placeholder_residue", verify_text("Hello", "QZXTOKEN00001QXZ", "da")["errors"])
        self.assertIn("script_or_style_content_changed", verify_text("<script>x=1</script>", "<script>x=2</script>", "da")["errors"])

    def test_fresh_digest_does_not_rescue_old_source_or_changed_before(self):
        baseline = self.base()
        candidate = {**baseline, "source": "old source", "value": "gammel kilde"}
        result = verify_rows([candidate], [baseline])
        self.assertIn("baseline_mismatch:source", result["rows"][0]["errors"])
        candidate = {**baseline, "before": {"value": "new concurrent edit"}, "value": "<p>100% bomuld; længde 12,5 cm.</p>"}
        self.assertIn("baseline_mismatch:before", verify_rows([candidate], [baseline])["rows"][0]["errors"])

    def test_missing_digest_and_duplicate_rows_fail(self):
        b = self.base(); c = {**b, "value": b["source"], "sourceDigest": ""}
        result = verify_rows([c, c], [b])
        self.assertEqual(result["failedRows"], 2)
        self.assertIn("duplicate_candidate_key", result["rows"][1]["errors"])

    def test_explicit_reviewed_material_fact(self):
        source = "100% cotton"
        rules = [{"id": "cotton-material", "locale": "da", "source": "cotton", "target": "bomuld"}]
        self.assertIn("explicit_fact_mismatch:cotton-material", verify_text(source, "100% polyester", "da", rules)["errors"])
        self.assertEqual(verify_text(source, "100% bomuld", "da", rules)["errors"], [])
        # Without a reviewed bilingual fact, code explicitly declines semantic certification.
        self.assertIn("semantic_equivalence_requires_independent_review", verify_text(source, "100% polyester", "da")["warnings"])

    def test_offline_cache_conflicts_nulls_and_exact_source_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            p, q = Path(tmp)/"a.json", Path(tmp)/"b.json"
            p.write_text(json.dumps({"da": {"Hello": "Hej", "Missing": None, "Token": "DLMTOKEN1", "Conflict": "A"}}))
            q.write_text(json.dumps({"da": {"Hello": "Hej", "Conflict": "B"}}))
            before = p.read_bytes(), q.read_bytes()
            rows = [{**self.base(s), "key": "title", "resourceId": "gid://shopify/Product/"+str(i)}
                    for i, s in enumerate(["Hello", "Missing", "Token", "Conflict", "Hello "])]
            result = reuse(rows, [p, q])
            self.assertEqual(len(result["rows"]), 1)
            self.assertEqual(len(result["unresolved"]), 4)
            self.assertEqual([r["reason"] for r in result["unresolved"]].count("CACHE_CONFLICT"), 1)
            self.assertEqual(before, (p.read_bytes(), q.read_bytes()))
            self.assertEqual(len(result["rows"][0]["cacheProvenance"]), 2)


if __name__ == "__main__":
    unittest.main()
