"""Do not certify stale translation text against a newer source digest."""

from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import sync_shopify_translations as sync
import poll_shopify_product_translations as poll


class SourceFreshnessTests(unittest.TestCase):
    def test_export_from_old_source_never_reaches_translator(self):
        candidate = {"type": "PRODUCT", "id": "1", "field": "title", "locale": "da", "default": "Cotton family shirt"}
        live = {("PRODUCT", "1"): {"resource_id": "gid://shopify/Product/1", "keys": {"title": {"digest": "new", "value": "Linen family shirt"}}}}
        translator = Mock()
        payload, skipped, _, _ = sync.build_payload([candidate], live, translator)
        self.assertFalse(payload)
        self.assertEqual(skipped["source_changed:PRODUCT:title"], 1)
        translator.translate_many.assert_not_called()

    def test_stale_body_is_translated_from_current_source(self):
        source = "<p>A linen shirt for family occasions.</p>"
        translated = "<p>En hørskjorte til familiens særlige stunder.</p>"
        snapshot = poll.ResourceSnapshot(
            resource_id="gid://shopify/Product/1", resource_type="Product",
            translatable_content=[{"key": "body_html", "value": source, "digest": "new", "locale": "en"}],
            existing_translations={("da", "body_html"): poll.ExistingTranslation(locale="da", key="body_html", value="<p>En bomuldsskjorte.</p>", outdated=True)},
        )
        translator = Mock()
        translator.translate_many.return_value = {source: translated}
        with patch.object(poll, "repair_product_html_translation", side_effect=lambda source, value, *a, **kw: value):
            payload, _ = poll.build_translation_payload([snapshot], ["da"], translator, progress_prefix="test")
        self.assertEqual(translator.translate_many.call_args.args, ("da", [source]))
        self.assertEqual(payload[snapshot.resource_id][0]["value"], translated)
        self.assertEqual(payload[snapshot.resource_id][0]["translatableContentDigest"], "new")

    def test_deterministic_only_mode_holds_stale_body(self):
        snapshot = poll.ResourceSnapshot(
            resource_id="gid://shopify/Product/1", resource_type="Product",
            translatable_content=[{"key": "body_html", "value": "<p>A linen family shirt.</p>", "digest": "new", "locale": "en"}],
            existing_translations={("da", "body_html"): poll.ExistingTranslation(locale="da", key="body_html", value="<p>En bomuldsskjorte.</p>", outdated=True)},
        )
        translator = Mock()
        payload, _ = poll.build_translation_payload([snapshot], ["da"], translator, progress_prefix="test", deterministic_repairs_only=True)
        self.assertFalse(payload)
        translator.translate_many.assert_not_called()


if __name__ == "__main__":
    unittest.main()
