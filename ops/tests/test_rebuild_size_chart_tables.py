import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import rebuild_size_chart_tables as m  # noqa: E402

G = {
    "de": {"size": "Größe", "age": "Alter", "height": "Körpergröße", "weight": "Gewicht", "chest": "Brust",
           "garment": "Gesamtlänge", "hip": "Hüfte", "waist": "Taille", "child": "Kind", "adult": "Erwachsene",
           "mother": "Mama", "father": "Papa", "girl": "Mädchen", "boy": "Junge", "years": "Jahre", "or": "oder",
           "pant": "Hose/Shorts", "sleeve": "Ärmel", "skirt": "Rocklänge", "shoulder": "Schulterbreite",
           "pants": "Hosenlänge"},
    "ja": {"size": "サイズ", "age": "年齢", "child": "子ども", "mother": "ママ", "years": "歳", "chest": "胸囲"},
    "pl": {"size": "Rozmiar", "child": "Dziecko", "years": "*pl"},
    "_singular": {"de": "Jahr", "ja": "歳", "pl": "rok"},
    "_extra": {},
}
EN = ('<table id="size-chart" class="size-chart" data-x="1"><thead><tr><th>Size</th><th>Age</th>'
      '<th>Height (cm/in)</th><th>Chest/Bust (cm)</th></tr></thead><tbody>'
      '<tr><td>Child 2 Years</td><td>2</td><td>92 cm / 36.2 in</td><td>-</td></tr>'
      '<tr><td>Child 1 Year</td><td>1</td><td>85-95 cm / 33.5-37.4 in</td><td>22.05 cm</td></tr>'
      '<tr><td>Mother 2XL</td><td>—</td><td>-</td><td>112 cm</td></tr></tbody></table>')


class Rebuild(unittest.TestCase):
    def test_glossary_applied_and_structure_kept(self):
        out, unc = m.rebuild_table(EN, "de", G)
        self.assertEqual(unc, [])
        self.assertIn("<th>Größe</th>", out)
        self.assertIn("<th>Körpergröße (cm/in)</th>", out)
        self.assertIn("<th>Brust (cm)</th>", out)
        self.assertIn("<td>Kind 2 Jahre</td>", out)
        self.assertIn("<td>Kind 1 Jahr</td>", out)
        self.assertIn("<td>Mama 2XL</td>", out)
        self.assertEqual(m.tag_skeleton(out), m.tag_skeleton(EN))
        self.assertTrue(out.startswith('<table id="size-chart" class="size-chart" data-x="1">'))

    def test_numbers_units_codes_identical(self):
        out, _ = m.rebuild_table(EN, "de", G)
        self.assertEqual(m.invariant_stream(out), m.invariant_stream(EN))
        for s in ("85-95 cm / 33.5-37.4 in", "22.05 cm", "92 cm / 36.2 in", "112 cm"):
            self.assertIn(s, out)

    def test_ja_age_unit_attaches(self):
        out, unc = m.rebuild_table(EN.replace("Height (cm/in)", "Size"), "ja", G)
        self.assertIn("<td>子ども 2歳</td>", out)

    def test_polish_plural(self):
        t = "<table id='size-chart'><tr><th>Size</th></tr><tr><td>Child 5 Years</td></tr><tr><td>Child 2 Years</td></tr></table>"
        out, unc = m.rebuild_table(t, "pl", G)
        self.assertEqual(unc, [])
        self.assertIn("Dziecko 5 lat", out)
        self.assertIn("Dziecko 2 lata", out)

    def test_uncovered_token_recorded(self):
        t = EN.replace("<th>Age</th>", "<th>Recommended Age</th>")
        out, unc = m.rebuild_table(t, "de", G)
        self.assertIn("Recommended", unc)

    def test_body_skips_on_uncovered(self):
        en = "<p>Hi</p>" + EN.replace("<th>Age</th>", "<th>Recommended Age</th>")
        tr = "<p>Hallo</p>" + EN
        r = m.rebuild_body(en, tr, "de", G)
        self.assertEqual(r["status"], "uncovered")
        self.assertIsNone(r["body"])

    def test_body_replaces_only_table(self):
        old_tbl = EN.replace("Size", "Size Size")
        tr = "<p>Hallo <b>Welt</b></p>\n" + old_tbl + "\n<p>Ende</p>"
        r = m.rebuild_body("<p>Hi</p>" + EN, tr, "de", G)
        self.assertEqual(r["status"], "ok")
        self.assertTrue(m.bytes_outside_tables_equal(tr, r["body"]))
        self.assertTrue(r["body"].startswith("<p>Hallo <b>Welt</b></p>\n<table"))
        self.assertTrue(r["body"].endswith("</table>\n<p>Ende</p>"))

    def test_table_count_mismatch_skipped(self):
        r = m.rebuild_body(EN + EN.replace("size-chart", "other"), EN, "de", G)
        self.assertEqual(r["status"], "table_count")

    def test_no_translation(self):
        self.assertEqual(m.rebuild_body(EN, "", "de", G)["status"], "no_translation")


if __name__ == "__main__":
    unittest.main()


class Arabic(unittest.TestCase):
    def test_ar_number_rule(self):
        g = {"ar": {"years": "*ar"}, "_singular": {"ar": "سنة"}}
        self.assertEqual(m.years_word("ar", g, "1"), "سنة")
        self.assertEqual(m.years_word("ar", g, "2"), "سنوات")
        self.assertEqual(m.years_word("ar", g, "5"), "سنوات")
        self.assertEqual(m.years_word("ar", g, "12"), "سنة")
        self.assertEqual(m.years_word("ar", g, "1-2"), "سنوات")
        self.assertEqual(m.years_word("ar", g, "11-12"), "سنة")


class MonthsPlurals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = m.load_glossary()

    def mw(self, loc, n):
        return m.months_word(loc, self.g, n)

    def test_ar(self):
        self.assertEqual([self.mw("ar", x) for x in ("1", "2", "3", "10", "11", "12")],
                         ["شهر", "أشهر", "أشهر", "أشهر", "شهرًا", "شهرًا"])

    def test_ru(self):
        self.assertEqual([self.mw("ru", x) for x in ("1", "2", "4", "5", "11", "12", "14", "21", "22")],
                         ["месяц", "месяца", "месяца", "месяцев", "месяцев", "месяцев", "месяцев", "месяц", "месяца"])

    def test_pl(self):
        self.assertEqual([self.mw("pl", x) for x in ("1", "2", "4", "5", "12", "14", "22")],
                         ["miesiąc", "miesiące", "miesiące", "miesięcy", "miesięcy", "miesięcy", "miesiące"])

    def test_cs(self):
        self.assertEqual([self.mw("cs", x) for x in ("1", "2", "4", "5", "12")],
                         ["měsíc", "měsíce", "měsíce", "měsíců", "měsíců"])

    def test_ro_he_el(self):
        self.assertEqual([self.mw("ro", x) for x in ("1", "6", "19", "20")], ["lună", "luni", "luni", "de luni"])
        self.assertEqual([self.mw("he", x) for x in ("1", "2", "3")], ["חודש", "חודשים", "חודשים"])
        self.assertEqual(self.mw("el", "1"), "μηνός")

    def test_cell_and_attach(self):
        self.assertEqual(m.translate_text("Baby 3-6 months", "ja", self.g)[0], "ベビー 3-6ヶ月")
        self.assertEqual(m.translate_text("Child 6-12 Months", "ru", self.g)[0], "Ребёнок 6-12 месяцев")

    def test_codes_copied_and_free_text_skipped(self):
        self.assertEqual(m.translate_text("US 4W", "de", self.g), ("US 4W", []))
        self.assertEqual(m.translate_text("75ABC-80AB", "de", self.g), ("75ABC-80AB", []))
        out, unc = m.translate_text("Please check the label", "de", self.g)
        self.assertTrue(unc)

    def test_measure_patterns(self):
        self.assertEqual(m.translate_text("up to 15 kg / up to 33 lbs", "de", self.g)[0], "bis 15 kg / bis 33 lbs")
        self.assertEqual(m.translate_text("110 cm and below", "es", self.g)[0], "110 cm o menos")
