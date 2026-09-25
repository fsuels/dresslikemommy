# Family matching outfits: one target page (2026-09-24)

Goal (owner request): rank for the Google query "family matching outfits". The owner reported 1,662 impressions a month, an average position of about 14.5 and 6 clicks. That GSC figure comes from the owner and was not re-read here, because GSC needed a Google sign-in in the in-app browser. The 50–100+ clicks a month is the owner's estimate, not a measurement.

## Decision

Target page: `/collections/new-women-outfits` (Shopify collection `33122287713`, H1 "Family Matching Outfits").

- Its 86 live products are all whole-family "Family Matching Set / Tops / Sweaters" items.
- It already had the sitewide "Family Matching" menu link, 7 homepage links, the PDP breadcrumb/back links, the Pinterest `family_matching` lane and the Google Ads headline links.
- Alternative rejected: `/collections/matching-outfits` (`377555589`). Its first products are dad-and-son shirts and mommy-and-me dresses, so it fits the query less well. Its better handle alone was not enough to justify moving links, ads and feeds.

Problem found: both collections had the same H1 ("Family Matching Outfits") and near-identical titles, so they were competing for the same query. Every page also rendered a second H1, "Shipping Policy", from the policy body embedded in the cart drawer.

## Changes

Theme: commit `b3950ea` on `main`. The GitHub sync did not apply it for 9+ minutes, the same stall seen on 2026-09-22. Live files were first confirmed identical to `b19a219`, then the same 6 committed files were written with `themeFilesUpsert` to MAIN `133290917985`. The readback shows all 6 live MD5 checksums match `b3950ea`.

- `locales/en.default.json` and `snippets/collection-seo-fallback.liquid` (English fallbacks):
  - Target: title "Family Matching Outfits for Mom, Dad and Kids | Dress Like Mommy", a new meta description, and 253 visible words of new buyer copy (intro, "How to choose family matching outfits", tips, 5 sub-collection links).
  - `matching-outfits`: retitled to H1 "Matching Outfits for Mom, Dad and Kids" plus a matching title and description, and it now links to the target with the anchor "Shop family matching outfits".
- `snippets/collection-seo-content.liquid`: adds the `family_matching_outfits_url` variable.
- `templates/index.json` and `sections/hero-banner.liquid`: the homepage hero button now reads "Shop Family Matching Outfits"; non-English localization of the label is kept.
- `snippets/cart-drawer.liquid`: the shipping policy `<h1>` in the drawer now renders as `<h2>`.
- Non-English locale strings were left unchanged.

Blog: 10 English articles each got one contextual link on the first unlinked "family matching outfits" in the intro paragraph → `/collections/new-women-outfits`. Only `body_html` translations that the edit made outdated were re-registered, with the new digest and the same value; translations that were already outdated were left as they were. See `article_link_receipts.json` (before bodies, the translation before/after state and the per-article status; all 10 are `VERIFIED`).

## Verification

- `shopify theme check` (nvm Node 22, because Homebrew node lacks `libsimdjson`): 0 offenses across the whole theme. `git diff --check` passes.
- Live HTML:
  - The target has the new title, meta and copy, 1 H1 and a CollectionPage schema name of "Family Matching Outfits".
  - `matching-outfits` has the new H1, title and schema name, plus the link to the target.
  - The homepage has the new button label.
  - The Spanish collection is unchanged.
- In the browser, desktop and a 375px mobile width render correctly with no horizontal overflow, and the drawer policy heading is H2.
- The English articles contain the link. German and Spanish article pages still serve their translated bodies.
- The `&amp;amp;` entities on these pages predate this change (3 were in the before-HTML).

## Rollback

- Theme: `git revert b3950ea` and push, or `themeFilesUpsert` the files in `theme_before_b19a219/`.
- Articles: restore `before.article.body` from `article_link_receipts.json`, then re-register the translations with the resulting digest.

## Follow-ups (not done)

- Re-read GSC for the query and page in about 4 weeks: position, clicks, and which URL ranks.
- `popular-family-matching` has the same product rule as the target (tag `Family Matching`) and a similar H1. Monitor it for cannibalization.
- Changing the target's handle to `family-matching-outfits` was deliberately not done, to avoid breaking paid and Pinterest URLs. That handle currently redirects to `matching-outfits`.
- The Shopify-native SEO title and description fields on both collections are overridden by the theme and were left unchanged.

## Pass 2: product-page links (2026-09-25 UTC)

- `bfe9f22` changes the English "Family Matching" breadcrumb and pill label to "Family Matching Outfits". Product-page breadcrumbs, collection breadcrumbs and branch pills now link to the target with the exact phrase. The article button and the dress and vacation hub links now point to the target.
- It was upserted to MAIN after the sync stalled; checksums verified. The previous live versions are in `theme_live_before_bfe9f22/`.
- The Shopify SEO fields on both collections now match the theme text; see `collections_seo_{before,after}.json`. Rollback: `collectionUpdate` with the before values.
- Incident: Shopify's sync-back commit `04aa621` reverted peer commit `0135453`. It was restored by `cb6f0ea`. See `PROB-2026-09-24-GITHUB-THEME-SYNC-STALL-AND-SYNC-BACK-REVERT`.
