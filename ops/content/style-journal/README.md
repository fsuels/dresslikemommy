# Style Journal Publishing Kit

This folder is the repo-side workflow for blog content that should eventually
live in Shopify under `/blogs/news`.

What is here:

- `strategy.md`
  - Search and conversion strategy for the blog.
- `editorial-calendar-q2-2026.md`
  - Recommended publish order and refresh cadence.
- `custom-data.md`
  - Shopify Admin metafields that override the repo-side fallback link mapping.
- `article-template.html`
  - Reusable structure for future articles.
- `articles/*.html`
  - Publish-ready article drafts with frontmatter metadata plus body HTML.

Publishing workflow:

1. Review a draft in `articles/`.
2. Replace the `featured_image_prompt` note with a real article image URL if you have one.
3. Run a dry run:

```bash
python3 ops/scripts/publish_blog_articles.py
```

4. Publish a specific article after review:

```bash
SHOPIFY_STORE_DOMAIN=your-store.myshopify.com \
SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx \
python3 ops/scripts/publish_blog_articles.py \
  --handles family-vacation-outfits-beach-cruise-resort \
  --execute \
  --publish
```

5. Update an existing live article with a rewrite draft:

```bash
SHOPIFY_STORE_DOMAIN=your-store.myshopify.com \
SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx \
python3 ops/scripts/publish_blog_articles.py \
  --handles the-complete-guide-to-family-matching-outfits \
  --execute \
  --update-existing \
  --publish
```

6. Audit or publish the priority gap-fill batch:

```bash
python3 ops/scripts/publish_style_journal_group.py --group gap_fill
```

With credentials:

```bash
SHOPIFY_STORE_DOMAIN=your-store.myshopify.com \
SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx \
python3 ops/scripts/publish_style_journal_group.py \
  --group gap_fill \
  --execute \
  --publish
```

7. Build a localization queue only after English winners are confirmed:

```bash
python3 ops/scripts/build_style_journal_localization_queue.py \
  --winner-handles best-family-swimsuits-for-beach-vacations-and-pool-days,how-to-choose-mommy-and-me-matching-outfits-for-family-photos
```

Notes:

- The current shell may have Shopify credentials loaded but still lack
  article/content scopes. Live publish requires content access such as
  `read_content` / `write_content`.
- On the current Admin GraphQL version used by this repo, `articleCreate` and
  `articleUpdate` accept both `seo` and `image` inputs. The publish script will
  send `seo_title`, `seo_description`, `image_url`, and `image_alt`
  automatically when they are present in frontmatter.
- Several priority drafts started with blank `image_url` values. Keep using the
  current cadence, but do not publish any draft until a real article image URL
  is in place.
- The theme now hides the `Blog` header link by default, so article discovery
  should come from the homepage journal section, internal links, footer/support
  links, and search indexing instead of the primary conversion nav.
- Do not bulk-publish many posts on the same day. Spread them out weekly.
