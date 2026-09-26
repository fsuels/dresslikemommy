"""Image SEO guard: classify weak alt text, validate reviewed alt text, and plan safe renames."""

from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ops.scripts import image_seo  # noqa: E402

NOW = datetime(2026, 9, 26, 18, 0, tzinfo=timezone.utc)


def product(handle="jingle-bells-santa-family-matching-sweaters", created="2026-09-26T00:02:00Z", media=None, options=None):
    return {
        "id": "gid://shopify/Product/1",
        "handle": handle,
        "title": "Jingle Bells Santa Family Matching Sweaters",
        "status": "ACTIVE",
        "productType": "Sweaters",
        "createdAt": created,
        "options": options or [{"name": "Size", "values": ["S", "M"]}],
        "media": {"nodes": media or []},
    }


def image(media_id, filename, alt=""):
    return {
        "id": media_id,
        "alt": alt,
        "mediaContentType": "IMAGE",
        "image": {"url": f"https://cdn.shopify.com/s/files/1/1/files/{filename}?v=1", "width": 1024, "height": 1024},
    }


class AltIssueTests(unittest.TestCase):
    def test_flags_the_weak_patterns_found_on_the_live_store(self):
        self.assertEqual(image_seo.alt_issues(""), ["empty"])
        self.assertIn("template_lead", image_seo.alt_issues("Alternate image of mommy and me bikini sets with matching style"))
        self.assertIn("numbered", image_seo.alt_issues("Mommy and Me French Halter Neck Tiered Dress in White photo 3"))
        self.assertIn("same_as_title", image_seo.alt_issues("Blue Daisy Swimsuits", product_title="Blue Daisy Swimsuits"))
        self.assertIn("banned_term", image_seo.alt_issues("Matching dresses from dresslikemommy.com store"))
        self.assertIn("duplicate_in_product", image_seo.alt_issues("Mother and daughter in pink dresses", duplicate=True))

    def test_keeps_descriptive_alt(self):
        self.assertEqual(image_seo.alt_issues("Mother and daughter in matching sunflower print dresses on a beach"), [])


class ValidateNewAltTests(unittest.TestCase):
    def test_accepts_a_good_description(self):
        alt = "Family of four in matching red Jingle Bells Santa knit sweaters by a Christmas tree"
        self.assertEqual(image_seo.validate_new_alt(alt), [])

    def test_rejects_claims_stuffing_length_and_siblings(self):
        self.assertTrue(image_seo.validate_new_alt("Matching family sweaters in stock with free shipping"))
        self.assertIn("too_long", image_seo.validate_new_alt("x " * 80))
        self.assertTrue(any(p.startswith("keyword_stuffing") for p in image_seo.validate_new_alt(
            "Matching sweaters matching family matching Christmas sweaters sweaters"
        )))
        self.assertIn("duplicate_in_product", image_seo.validate_new_alt(
            "Mother and son in red reindeer sweaters", sibling_alts=["Mother and son in red reindeer sweaters"]
        ))
        self.assertIn("starts_with_image_of", image_seo.validate_new_alt("Image of a family in matching sweaters"))


class GuardPlanTests(unittest.TestCase):
    def test_new_listing_gets_baseline_alt_and_clean_filename(self):
        products = [product(media=[image("m1", "ChatGPT_Image_Sep_25_2026_07_39_14_PM.png")])]
        updates, plan = image_seo.plan_guard(products, "", now=NOW, rename_window_hours=72)
        self.assertEqual(updates, [{
            "id": "m1",
            "alt": "Jingle Bells Santa Family Matching Sweaters",
            "filename": "jingle-bells-santa-family-matching-sweaters-01.png",
        }])
        self.assertEqual(plan[0]["reasons"], ["baseline_alt", "rename_new_listing"])

    def test_older_listing_is_never_renamed_and_descriptive_alt_is_kept(self):
        products = [product(created="2026-05-01T00:00:00Z", media=[
            image("m1", "pomelli-image_30.png", alt="Mother and daughter in matching royal blue halter swimsuits"),
        ])]
        updates, plan = image_seo.plan_guard(products, "", now=NOW, rename_window_hours=72)
        self.assertEqual(updates, [])
        self.assertEqual(plan, [])

    def test_file_embedded_in_a_blog_post_is_not_renamed(self):
        products = [product(media=[image("m1", "ChatGPT_Image_Sep_25_2026_07_39_14_PM.png", alt="Family in matching Santa sweaters by the tree")])]
        body = '<img src="https://cdn.shopify.com/s/files/1/1/files/ChatGPT_Image_Sep_25_2026_07_39_14_PM.png">'
        updates, plan = image_seo.plan_guard(products, body, now=NOW, rename_window_hours=72)
        self.assertEqual(updates, [])
        self.assertEqual(plan[0]["reasons"], ["rename_skipped_referenced_in_article"])

    def test_handle_based_filename_is_left_alone(self):
        products = [product(media=[image("m1", "jingle-bells-santa-family-matching-sweaters-01.png", alt="Family in matching Santa sweaters")])]
        updates, _ = image_seo.plan_guard(products, "", now=NOW, rename_window_hours=72)
        self.assertEqual(updates, [])

    def test_single_color_option_is_added_to_baseline(self):
        item = product(options=[{"name": "Color", "values": ["Burgundy"]}])
        self.assertEqual(image_seo.baseline_alt(item), "Jingle Bells Santa Family Matching Sweaters in Burgundy")


if __name__ == "__main__":
    unittest.main()
