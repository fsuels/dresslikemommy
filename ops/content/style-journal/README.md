# Style Journal Publishing Kit

This folder is the repo-side workflow for blog content that should eventually
live in Shopify under `/blogs/news`.

What is here:

- `strategy.md`
  - Search and conversion strategy for the blog.
- `editorial-calendar-q2-2026.md`
  - Recommended publish order and refresh cadence.
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

Notes:

- The current shell does not expose Shopify admin credentials, so these drafts
  were prepared but not published live in this session.
- Shopify's current `articleCreate` and `articleUpdate` inputs do not expose
  article SEO title/meta description fields. Keep `seo_title` and
  `seo_description` in frontmatter as editorial guidance, and enter those
  manually in Shopify admin when publishing if needed.
- The theme now hides the `Blog` header link by default, so article discovery
  should come from the homepage journal section, internal links, footer/support
  links, and search indexing instead of the primary conversion nav.
- Do not bulk-publish many posts on the same day. Spread them out weekly.
