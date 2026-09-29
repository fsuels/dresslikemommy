# Organic Traffic Engine — playbook for the nonstop agent

Owner request (2026-09-28, chat): "I want to have an agent working non stop … bringing more customers to the website … organic free traffic from SEO … get me to the top of the organic search results." No paid ads, ever (`ops/marketing/spend_authorization.md` = `REVOKED_BY_OWNER`).

The scheduled task `organic-traffic-engine` runs this playbook every hour on Sonnet (owner: "Do it every 1 hour", 2026-09-28). Each run is fresh: this file, `BACKLOG.md` and `ENGINE_LOG.md` are its whole memory.

## North star

More **qualified** organic sessions that buy: rankings and clicks for matching-family shopping queries (Mommy & Me, family matching, Daddy & Me, couples, siblings, maternity, family pajamas, seasonal). Judge work by the queries it can rank for and whether the page leads to a live collection with real products. Quality beats volume: Google's helpful-content systems demote sites that mass-publish thin AI pages, so every page must be the best answer on the web for its query.

## Authority for unattended runs

Allowed live writes (standing CEO authority + owner request above), each reversible and logged:

| Write | Tool | Cap per run | Rollback |
|---|---|---|---|
| New Style Journal article (blog `news`) | `publish_blog_articles.py --execute --publish --handles <h>` | 1 (max 3 per UTC day) | unpublish the article |
| Repair body of a live article: dead links + unsupported claims | `organic_engine.py article-body --execute` | 5 | `before_body` in the receipt |
| SEO title/description of a live article | `organic_engine.py article-seo --execute` | 10 | receipt `rollback` values |
| Body update of an article this engine created | `publish_blog_articles.py --execute --update-existing --handles <h>` | 3 | previous file version in git/receipt |
| SEO title/description of a non-theme-owned collection | `organic_engine.py collection-seo --execute` | 5 | receipt `rollback` values |
| URL redirect for a dead URL | `organic_engine.py redirect --execute` | 10 | `urlRedirectDelete` on the created id |

Never, in an unattended run: theme files, git commit/push, products, prices, inventory, feeds, translations, menus, collection membership, discounts, emails/messages, ads, spend, republishing old unpublished articles (they were retired on purpose by the blog consolidation), or posting anywhere off-site. Those go to `BACKLOG.md` tagged `MAIN` (a main CEO session does them) or `OWNER` (needs the owner's yes).

## Every run

0. Clock and lock: get the real time with `date -u +%Y-%m-%dT%H:%MZ` (never guess it). Read `ops/organic/RUN_LOCK`. If it holds a UTC timestamp less than 50 minutes old, another run is active: stop without logging. Otherwise Write the current UTC timestamp into it. At the end of the run (success or stop), Write `free` into it.
1. Read this file, `BACKLOG.md`, and the last 5 entries of `ENGINE_LOG.md`. Skip backlog rows tagged `HOLD` (other sessions register holds there).
2. Refresh the Shopify token (`refresh_shopify_admin_token.py --if-needed`), then `organic_engine.py inventory --output WORK/inventory.json` and Read the compact `WORK/inventory.md` it writes (the JSON is large; Read it only with offset/limit or Grep it).
3. Pick work in this order, doing at most **one BUILD item and one FIX batch**:
   - **BUILD:** the highest open `ENGINE` item in `BACKLOG.md` (usually a new article for a season-clock query). If none is open, run RESEARCH instead.
   - **FIX batch, first priority until the report is empty — article repair:** `organic_engine.py article-links --output WORK/links.json --bodies-dir WORK/bodies`, take the top 5 rows, and for each: Read `WORK/bodies/<handle>.html`, Write a repaired copy to `WORK/fixed/<handle>.html`, dry-run `article-body --handle <h> --body-file WORK/fixed/<h>.html --receipt ops/organic/receipts/<date>/body-<h>.json`, fix any problem, then `--execute`. Repair rules: point every dead `/products/...` link at the closest live collection with ≥3 products (collection links do not rot; keep the anchor text natural and true); point dead collection links at the closest live collection (`family-matching` → `matching-outfits`, `headbands` → `mommy-and-me` unless a better match exists); rewrite sentences with unsupported claims ("one of our bestsellers" → describe the item; "happiness guarantee" and "customer reviews" lines → delete or replace with "check the size chart on each product page"; "free shipping on all orders" → "standard shipping included"; drop brand/character names such as Disney). Keep everything else, including length (the tool refuses a >15% shrink), and update any stale year only when the sentence is about the current season.
   - **FIX batch otherwise:** missing/weak SEO meta on live articles or collections, internal links from engine-created articles to newer collections, or dead-URL redirects listed in the backlog.
   - **RESEARCH** (when the backlog has fewer than 5 open ENGINE items): up to 5 WebSearch queries to find buyer queries we have no page for (seasonal, occasion × relationship, sizing and gift questions). Add each as a backlog row with the target query, intent, and which live collections it would link to.
4. Verify every write: tool readback plus `organic_engine.py check` on the live URL (≤12 URLs per run; the site rate-limits).
5. Update `BACKLOG.md` (status, date) and append one entry to `ENGINE_LOG.md`.

## Quality bar for a new article

- Targets one real query cluster with buying intent that has no live page yet (check inventory titles/handles first; never cannibalize a collection that already ranks for the head term — support it with a link instead).
- 900–1,600 words of genuinely useful guidance: specific outfit/palette combinations, how to size a whole family, photo tips, timing ("order early; each product page shows its delivery estimate"). Answer the question in the first paragraph. Use 3–6 `<h2>` sections and a short FAQ `<h2>` with 3–4 questions at the end.
- 3–8 links to live collections with ≥3 products (lint enforces), plus 1–2 links to related live articles. No external links.
- Frontmatter: `title`, `handle` (lowercase-hyphenated, query-shaped), `summary`, `tags`, `seo_title` (≤65 chars, query first), `seo_description` (110–160 chars), `image_url` = a real product image from a linked collection (get it from `https://www.dresslikemommy.com/collections/<handle>/products.json?limit=5` saved with `curl -s -o`), `image_alt` describing that photo, `author: Dress Like Mommy Team`, `is_published: true`.
- Honesty: dropshipping store. No stock/warehouse/local/fast-shipping/arrival-date/bestseller/review/rating/#1 claims, no supplier names, no pets, no invented statistics, no fake first-person stories. Delivery = "each product page shows its estimated delivery window."
- Must pass `organic_engine.py lint-article --inventory WORK/inventory.json` with 0 errors, then a dry run of `publish_blog_articles.py`, before `--execute`.
- Save the article in `ops/content/style-journal/articles/<handle>.html`.

## Season clock (Google needs weeks to rank a new page — publish early)

| Moment | Date | Pages should be live by | Notes |
|---|---|---|---|
| Christmas (pajamas, sweaters, photo outfits, card photos) | Dec 25; last safe US order ~Dec 5 | **now → mid-Oct** | biggest revenue season; 4–7 piece family orders are the most profitable |
| Thanksgiving | Nov 26 | now | family photo + dinner outfits |
| New Year's Eve | Dec 31 | late Oct | family/couples sparkle outfits |
| Valentine's Day | Feb 14 | early Dec | mommy & me, couples, daddy & daughter |
| Easter / spring photos | Apr 5, 2027 | early Feb | |
| Mother's Day | May 9, 2027 | early Mar | mommy & me core |
| Summer / swim / vacation | Jun–Aug | Apr | swim, beach, cruise |
| Father's Day | Jun 20, 2027 | Apr | daddy & me core |

Evergreen clusters to fill between seasons: family photo outfit ideas by setting (beach, fall, studio, field), what colors to wear for family photos, how to size a whole family, maternity + family photos, sibling matching, couples matching, birthday matching outfits, kids-to-adult size conversion guide (linkable asset).

## Logging format (`ENGINE_LOG.md`, newest last)

```
## <UTC timestamp> run
- Build: <what> → <live URL> (VERIFIED|FAILED|SKIPPED: reason)
- Fix: <n> items (<type>) — receipts: <paths>
- Research: <queries added>
- Flags for MAIN/OWNER: <one line each or none>
```

Receipts go to `ops/organic/receipts/<UTC date>/`.

## Stop conditions

Stop and log (do not work around): token/401 errors, Shopify userErrors on a retry, CAPTCHA/login, lint failing twice on the same article, any 5xx/429 storm, or evidence that a change broke a live page.
