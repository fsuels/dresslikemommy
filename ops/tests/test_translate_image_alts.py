"""Image alt translations: detect stale/missing locales, validate translations, plan safe writes."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ops.scripts import translate_image_alts as t  # noqa: E402

SOURCE = "Family of four in matching green Jingle Bells Santa sweaters by the Christmas tree"
ES = "Familia de cuatro con suéteres verdes a juego de Papá Noel Jingle Bells junto al árbol de Navidad"


def resource(translations=None, digest="d-new", source=SOURCE, rid="gid://shopify/MediaImage/1"):
    return {"resource_id": rid, "source": source, "digest": digest, "translations": translations or {}}


class MissingLocaleTests(unittest.TestCase):
    def test_absent_and_outdated_translations_are_missing(self):
        res = resource({"es": {"value": ES, "outdated": False}, "fr": {"value": "Famille assortie", "outdated": True}})
        self.assertEqual(t.missing_locales(res, ["es", "fr", "de"]), ["fr", "de"])

    def test_stale_translation_left_current_by_shopify_is_missing(self):
        # Seen live: an old "...-dresslikemommy.com" translation survived the alt rewrite with outdated=false.
        res = resource({"it": {"value": "Costume da bagno abbinato-dresslikemommy.com", "outdated": False}})
        self.assertEqual(t.missing_locales(res, ["it"]), ["it"])

    def test_translation_from_an_older_english_alt_is_missing(self):
        res = resource({"es": {"value": ES, "outdated": False}}, digest="d-new")
        self.assertEqual(t.missing_locales(res, ["es"], {res["resource_id"]: {"es": "d-old"}}), ["es"])
        self.assertEqual(t.missing_locales(res, ["es"], {res["resource_id"]: {"es": "d-new"}}), [])


class ValidationTests(unittest.TestCase):
    def test_accepts_a_clean_translation(self):
        self.assertEqual(t.validate_translation(SOURCE, ES, "es"), [])

    def test_rejects_english_copy_markup_brand_and_length(self):
        self.assertIn("same_as_english", t.validate_translation(SOURCE, SOURCE, "de"))
        self.assertIn("markup_or_placeholder", t.validate_translation(SOURCE, "<b>Familia</b> a juego", "es"))
        self.assertIn("banned_term", t.validate_translation(SOURCE, "Familia a juego - dresslikemommy.com", "es"))
        self.assertIn("too_long", t.validate_translation(SOURCE, "a" * 201, "es"))
        self.assertIn("untrimmed_or_multiline", t.validate_translation(SOURCE, "Familia\na juego", "es"))
        self.assertEqual(t.validate_translation(SOURCE, "", "es"), ["empty"])


class PlanTests(unittest.TestCase):
    def test_only_translations_keyed_by_the_live_english_are_written(self):
        resources = {
            "gid://shopify/MediaImage/1": resource(),
            "gid://shopify/MediaImage/2": resource(source="Flat lay of four green sweaters", digest="d2", rid="gid://shopify/MediaImage/2"),
        }
        translations = {"es": {SOURCE: ES, "An alt that was edited after the queue": "Otro texto"}}
        writes, rejected, counts = t.plan_writes(resources, ["es"], translations)
        self.assertEqual(list(writes), ["gid://shopify/MediaImage/1"])
        self.assertEqual(
            writes["gid://shopify/MediaImage/1"],
            [{"locale": "es", "key": "alt", "value": ES, "translatableContentDigest": "d-new"}],
        )
        self.assertEqual(rejected, [])
        self.assertEqual(counts["untranslated"], 1)

    def test_invalid_translations_are_rejected_not_written(self):
        writes, rejected, counts = t.plan_writes({"gid://shopify/MediaImage/1": resource()}, ["fr"], {"fr": {SOURCE: SOURCE}})
        self.assertEqual(writes, {})
        self.assertEqual(rejected[0]["issues"], ["same_as_english"])
        self.assertEqual(counts["rejected"], 1)

    def test_current_translations_are_left_alone(self):
        res = resource({"es": {"value": ES, "outdated": False}})
        writes, _, counts = t.plan_writes({res["resource_id"]: res}, ["es"], {"es": {SOURCE: "Otra traducción"}})
        self.assertEqual(writes, {})
        self.assertEqual(counts.get("planned", 0), 0)


class QueryTests(unittest.TestCase):
    def test_locale_aliases_are_valid_graphql_names(self):
        self.assertEqual(t.locale_alias("pt-BR"), "t_pt_BR")
        self.assertIn('t_pt_BR: translations(locale: "pt-BR")', t.resources_query(["pt-BR"]))

    def test_register_mutation_batches_resources(self):
        mutation = t.register_mutation(2)
        self.assertIn("r0: translationsRegister(resourceId: $id0, translations: $t0)", mutation)
        self.assertIn("$id1: ID!, $t1: [TranslationInput!]!", mutation)


if __name__ == "__main__":
    unittest.main()
