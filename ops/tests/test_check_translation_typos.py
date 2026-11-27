#!/usr/bin/env python3
"""Offline tests for ops/scripts/check_translation_typos.py (pure functions on fixture strings)."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("dlm_check_translation_typos", ROOT / "ops/scripts/check_translation_typos.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def checks(text, loc="es"):
    return {f["check"] for f in m.scan_text(text, loc)}


class TypoTests(unittest.TestCase):
    def test_repeats(self):
        self.assertIn("repeat", checks("La camisa La camisa Blue Monstera aporta un aire fresco."))
        self.assertIn("repeat", checks("Sie ist wie wie gemacht für den Strand.", "de"))
        self.assertNotIn("repeat", checks("Sí, sí, es perfecto."))
        self.assertNotIn("repeat", checks("Tallas 2-3 3-4 años."))
        self.assertNotIn("repeat", checks("Mixen Sie sie mit Basics.", "de"))
        self.assertNotIn("repeat", checks("Que vous vous détendiez au bord de la piscine.", "fr"))
        self.assertNotIn("unbalanced", checks("Imprimeu: „Autumn Woodland Bunny” cu iepurași.", "ro"))

    def test_punctuation(self):
        self.assertIn("space-punct", checks("Un vestido ligero , fresco."))
        self.assertIn("double-punct", checks("Un vestido ligero,, fresco."))
        self.assertNotIn("double-punct", checks("Y mucho más..."))
        self.assertIn("comma-glued", checks("Rosa,azul y verde."))
        self.assertNotIn("comma-glued", checks("Mide 1,5 cm."))
        # French needs a (non-breaking) space before ; : ! ?
        self.assertNotIn("space-punct", checks("Détails du modèle : robe.", "fr"))

    def test_unbalanced_and_lower_start(self):
        self.assertIn("unbalanced", checks("Algodón (suave y ligero."))
        self.assertIn("unbalanced", checks("Pyžamo „Koledu, nebo vám provedu je černé.", "cs"))
        self.assertNotIn("unbalanced", checks("Pyžamo „Koledu, nebo vám provedu“ je černé.", "cs"))
        self.assertIn("lower-start", checks("Es ligero. y fresco."))
        self.assertNotIn("lower-start", checks("Medidas aprox. en cm."))
        self.assertNotIn("lower-start", checks("Con la scritta BOO! a pantaloni a righe.", "it"))

    def test_cs_comma(self):
        self.assertIn("cs-comma", checks("Vytváří paletu která je skvělá na focení.", "cs"))
        self.assertNotIn("cs-comma", checks("Vytváří paletu, která je skvělá na focení.", "cs"))
        self.assertNotIn("cs-comma", checks("Je lehká a když prší, schne rychle.", "cs"))
        self.assertNotIn("cs-comma", checks("Nosí šaty, ve kterých se snadno pohybují.", "cs"))

    def test_cs_comma_more_conjunctions(self):
        for w in ("zatímco", "pokud", "kde", "což", "takže", "protože", "aby", "že"):
            self.assertIn("cs-comma", checks("Šaty jsou lehké %s se dobře nosí." % w, "cs"), w)
        self.assertNotIn("cs-comma", checks("Pokud chcete, vyberte větší velikost.", "cs"))
        self.assertNotIn("cs-comma", checks("Je to pohodlné, takže se dobře nosí.", "cs"))
        self.assertNotIn("cs-comma", checks("Uvádíme rozsah, takže pokud si nejste jistá, napište nám.", "cs"))

    def test_cs_vocalisation(self):
        self.assertIn("cs-vocal", checks("Nosí se v sladěných outfitech.", "cs"))
        self.assertIn("cs-vocal", checks("Top v vzdušném střihu.", "cs"))
        self.assertIn("cs-vocal", checks("Košile s sedmikráskami.", "cs"))
        self.assertIn("cs-vocal", checks("Vyrobeno z zelené látky.", "cs"))
        self.assertIn("cs-vocal", checks("Patří k kalhotám.", "cs"))
        for ok in ("Nosí se ve sladěných outfitech.", "Košile s černými proužky.", "Šaty v modré barvě.",
                   "Šaty s volány a výstřihem do V s kapsami.", "Velikosti od S do 2XL.", "Ruce v teple."):
            self.assertNotIn("cs-vocal", checks(ok, "cs"), ok)
        self.assertIn("cs-spelling", checks("Sušte na plocho.", "cs"))
        self.assertNotIn("cs-spelling", checks("Sušte naplocho.", "cs"))

    def test_alt_texts_scanned(self):
        body = '<p>Bez chyby.</p><img src="x.jpg" alt="Sladěné šaty v sladěných barvách"><img alt="La camisa La camisa">'
        found = m.scan_body(body, "cs")
        self.assertTrue(any(f["check"] == "cs-vocal" and f["text"].startswith("[alt]") for f in found))
        self.assertTrue(any(f["check"] == "repeat" for f in found))

    def test_blocks_skip_tables(self):
        body = "<p>Hola hola mundo.</p><table><tr><td>S S</td></tr></table>"
        found = m.scan_body(body, "es")
        self.assertEqual([f["check"] for f in found], ["repeat"])


if __name__ == "__main__":
    unittest.main()
