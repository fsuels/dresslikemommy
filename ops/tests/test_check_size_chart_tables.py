import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_size_chart_tables as m  # noqa: E402

G_DE = {"mother": "Mama", "father": "Papa", "child": "Kind", "girl": "Mädchen", "boy": "Junge", "adult": "Erwachsene",
        "height": "Körpergröße", "shoulder": "Schulterbreite", "size": "Größe", "garment": "Gesamtlänge"}


def table(rows, tid="size-chart"):
    def tr(cells, tag):
        return "<tr>" + "".join("<%s>%s</%s>" % (tag, c, tag) for c in cells) + "</tr>"
    return '<table id="%s">%s</table>' % (tid, tr(rows[0], "th") + "".join(tr(r, "td") for r in rows[1:]))


class Numbers(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(m.compare_numbers("107 cm / 42.1 in", "107 cm / 42.1 インチ")[0], "ok")

    def test_mismatch(self):
        self.assertEqual(m.compare_numbers("107 cm / 42.1 in", "109 cm / 42.1 in")[0], "numeric_mismatch")

    def test_decimal_comma_is_info(self):
        self.assertEqual(m.compare_numbers("42.5-50 kg", "42,5-50 kg")[0], "decimal_comma")

    def test_dropped_imperial(self):
        self.assertEqual(m.compare_numbers("85-95 cm / 33.5-37.4 in", "85-95 cm")[0], "numeric_dropped")

    def test_rounded(self):
        self.assertEqual(m.compare_numbers("22.05-29.76 lbs", "22,0462-29,7624 lbs")[0], "numeric_rounded")

    def test_reordered(self):
        self.assertEqual(m.compare_numbers("11-13 kg", "13-11 kg")[0], "numeric_reordered")

    def test_native_digits(self):
        self.assertEqual(m.compare_numbers("6-7", "٦-٧")[0], "native_digits")

    def test_size_code_digit_is_not_a_number(self):
        self.assertEqual(m.compare_numbers("Father 2XL", "Papa 2XL")[0], "ok")

    def test_dual_age_word(self):
        self.assertTrue(m.is_dual_age_word("Child 2 Years", "طفل سنتين", "ar"))
        self.assertFalse(m.is_dual_age_word("Child 2 Years", "Kind", "de"))


class Codes(unittest.TestCase):
    def test_same(self):
        self.assertIsNone(m.compare_size_codes("Mother S", "Mère S"))
        self.assertIsNone(m.compare_size_codes("Father 3XL", "父 3XL"))
        self.assertIsNone(m.compare_size_codes("Mother M", "母M"))

    def test_converted_pt(self):
        r = m.compare_size_codes("S-3XL", "P-3GG")
        self.assertEqual(r["kind"], "converted")

    def test_missing_code(self):
        self.assertEqual(m.compare_size_codes("Mother S", "母さん")["kind"], "mismatch")

    def test_cyrillic_lookalike(self):
        self.assertEqual(m.compare_size_codes("Father M", "Отец М")["kind"], "converted")


class Text(unittest.TestCase):
    def test_residue(self):
        self.assertEqual(m.english_residue("Mother S", "de", set()), ["Mother"])
        self.assertEqual(m.english_residue("Mama S", "de", set()), [])
        self.assertEqual(m.english_residue("Baby 0-6 Monate", "de", set()), [])
        self.assertEqual(m.english_residue("Bust", "ro", set()), [])

    def test_age_year_word(self):
        self.assertEqual(m.age_unit_issue("Child 6-7 Years", "子供 6-7年", "ja"), ("wrong", "年"))
        self.assertIsNone(m.age_unit_issue("Child 6-7 Years", "子供 6-7歳", "ja"))
        self.assertEqual(m.age_unit_issue("Child 6-7 Years", "어린이 6-7연도", "ko"), ("wrong", "연도"))
        self.assertIsNone(m.age_unit_issue("Child 6-7 Years", "어린이 6-7세", "ko"))
        self.assertIsNone(m.age_unit_issue("Child", "子供", "ja"))

    def test_duplicated_header(self):
        en = ["Size", "Bust", "Chest"]
        self.assertEqual(len(m.duplicated_headers(en, ["사이즈", "가슴", "가슴"])), 1)
        self.assertEqual(len(m.duplicated_headers(["Size", "Bust/Chest"], ["사이즈", "가슴/가슴"])), 1)
        self.assertEqual(m.duplicated_headers(["Size", "Bust"], ["Größe", "Brust"]), [])
        self.assertEqual(m.duplicated_headers(["Size", "Bust", "Bust"], ["a", "b", "b"]), [])

    def test_label_swap(self):
        self.assertEqual(m.label_swapped("Mother S", "Kind S", G_DE), "child")
        self.assertIsNone(m.label_swapped("Mother S", "Mama S", G_DE))
        self.assertIsNone(m.label_swapped("Child 3-4 Years", "Mädchen 3-4 Jahre", G_DE))
        self.assertEqual(m.label_swapped("Father M", "Mama M", G_DE), "mother")
        self.assertIsNone(m.label_swapped("Mother S", "Mutter S", G_DE))  # unknown synonym: not a swap

    def test_header_keys_and_glossary(self):
        self.assertEqual(m.en_header_key("Suggested Height (cm/in)"), "height")
        self.assertEqual(m.en_header_key("Bust (cm/in)"), "chest")
        self.assertEqual(m.en_header_key("Shoulder Width"), "shoulder")
        self.assertTrue(m.header_matches_glossary("height", "Empfohlene Körpergröße (cm)", G_DE))
        self.assertFalse(m.header_matches_glossary("garment", "Kleidungslänge", G_DE))

    def test_year_words(self):
        self.assertTrue(m.has_year_word("子供 歳", ["歳"]))
        self.assertFalse(m.has_year_word("lapsi vuotta", ["v"]))  # single letters match whole tokens only
        self.assertTrue(m.has_year_word("lapsi v", ["v"]))


class Tables(unittest.TestCase):
    EN = table([["Size", "Length (cm/in)"], ["Mother S", "107 cm / 42.1 in"], ["Child 3-4 Years", "59 cm / 23.2 in"]])

    def test_parse_and_match_by_id(self):
        other = "<table id='x'><tr><td>1</td></tr></table>"
        pairs, n_en, n_tr = m.match_tables(self.EN, other + self.EN)
        self.assertEqual(n_en, 1)
        self.assertEqual(n_tr, 2)
        self.assertEqual(pairs[0][2]["id"], "size-chart")
        self.assertEqual(len(pairs[0][2]["rows"]), 3)

    def test_audit_clean_and_wrong(self):
        tr = table([["Größe", "Gesamtlänge (cm/in)"], ["Mama S", "107 cm / 42.1 in"], ["Kind 3-4 Jahre", "59 cm / 23.2 in"]])
        pairs, _, _ = m.match_tables(self.EN, tr)
        ng, info = m.defaultdict(list), m.Counter()
        self.assertEqual([f["type"] for f in m.audit_table("h", "de", 0, pairs[0][1], pairs[0][2], G_DE, ng, info)], [])
        bad = table([["Größe", "Kleidungslänge (cm/in)"], ["Kind S", "109 cm / 42.1 in"], ["Kind 3-4 Jahre", "59 cm / 23.2 in"]])
        pairs, _, _ = m.match_tables(self.EN, bad)
        f = m.audit_table("h", "de", 0, pairs[0][1], pairs[0][2], G_DE, ng, info)
        types = {x["type"] for x in f}
        self.assertIn("numeric_mismatch", types)
        self.assertIn("label_swapped", types)
        self.assertTrue(any(k[1] == "header:garment" for k in ng))

    def test_row_and_col_count(self):
        tr = table([["Größe", "Gesamtlänge"], ["Mama S", "107 cm / 42.1 in", "x"]])
        pairs, _, _ = m.match_tables(self.EN, tr)
        f = m.audit_table("h", "de", 0, pairs[0][1], pairs[0][2], G_DE, m.defaultdict(list), m.Counter())
        types = {x["type"] for x in f}
        self.assertIn("row_count", types)
        self.assertIn("col_count", types)

    def test_missing_table(self):
        f = m.audit_table("h", "de", 0, m.parse_tables(self.EN)[0], None, G_DE, m.defaultdict(list), m.Counter())
        self.assertEqual(f[0]["type"], "table_missing")


if __name__ == "__main__":
    unittest.main()
