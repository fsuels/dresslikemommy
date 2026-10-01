import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ops" / "scripts"))

from ops.scripts import publish_blog_articles as publisher  # noqa: E402


def draft(is_published=True):
    return publisher.ArticleDraft(**{
        **{name: None for name in publisher.ArticleDraft.__dataclass_fields__},
        "title": "Guide", "handle": "guide", "body_html": "<p>x</p>", "summary": "s",
        "tags": [], "author": "Dress Like Mommy Team", "is_published": is_published,
    })


class PublishStateTest(unittest.TestCase):
    def test_update_without_publish_flag_keeps_live_state(self):
        article = publisher.build_article_input(draft(), publish_override=None, preserve_live_state=True)
        self.assertNotIn("isPublished", article)

    def test_publish_flag_forces_publish(self):
        article = publisher.build_article_input(draft(False), publish_override=True, preserve_live_state=True)
        self.assertTrue(article["isPublished"])

    def test_create_follows_frontmatter(self):
        self.assertTrue(publisher.build_article_input(draft(True))["isPublished"])
        self.assertFalse(publisher.build_article_input(draft(False))["isPublished"])


if __name__ == "__main__":
    unittest.main()
