# Google Shopping Multilingual Expansion Queue

Generated: 2026-05-15 05:12 EDT
Mode: repo-local strategy and read-only queue only. No Google Ads, Merchant, Shopify, feed, title, product-group, budget, bid, status, campaign, or conversion write occurred.

## Why This Exists

The user is right that growth cannot wait only on non-US Search keyword validation. Standard Shopping and Shopping-ready multilingual/feed lanes need their own fast path, but they still cannot be mutated from stale Merchant exports, concept copy, or unreviewed localized feed/title assumptions.

This packet creates the safe aggressive path: prepare Shopping expansions and exact read-only exports now, then turn only proven clean/high-intent rows into approval packets.

## Immediate Shopping Lanes

| Priority | Market/language | Lane | Why it can move traffic | Safe next action | Live-write gate |
|---|---|---|---|---|---|
| P1 | `US / en` | Existing Standard Shopping optimization | It is already enabled/eligible and had `17` impressions in the saved readback, so it is the fastest Shopping learning lane | Run authenticated read-only item-level export for campaign `23802638621`, then join it to the `18` public-clean rows using the existing export join prep | No title, feed, product-group, negative, bid, budget, scope, or status write until item-level export proves relevance and rows pass approval |
| P1 | `US / es` | Spanish US Shopping readiness | Merchant US/es was sampled current-clear for age_group, and Spanish storefront/category fixes have prior public proof, so this is the first non-English Shopping lane to test by readback | Obtain a current exact Merchant `US` / `es` product export for source `10627981690`, intersect with active paid-eligible clean products, and classify titles/landing URLs before any campaign or feed action | No Shopping campaign/product/feed/title action from the stale May 8 CSV; no native-language title/ad claims without current feed and landing QA |
| P1 | `CA / en` | Canada English Shopping feasibility | Canada Search CPC head terms are too expensive; Shopping may capture high-intent product demand without new Search keywords | Read-only Merchant/Ads export: confirm feed label/country eligibility, shipping/currency, product disapprovals, and item-level impressions/queries for paid-eligible products | No CA Shopping campaign, country/feed-label, product group, bid, or budget change until Merchant country/feed proof exists |
| P1 | `GB / en` | UK English Shopping feasibility | GB Search head terms are too expensive; Shopping can test product-level demand with localized currency/country proof | Read-only Merchant/Ads export: confirm UK eligibility, shipping/currency, product disapprovals, and query/item fit for paid-eligible products | No GB Shopping campaign, country/feed-label, product group, bid, or budget change until Merchant country/feed proof exists |
| P2 | `AU / en` | AU English Shopping feasibility | AU has market vocabulary and country-qualified landings but needs Merchant eligibility proof | Read-only Merchant/Ads export after GB/CA because the immediate Shopping proof path should avoid spreading too thin | No AU Shopping write until country/feed proof and economics are clean |
| P2 | `ES/IT/FR/DE/NL/PT/RO/...` | Non-English Shopping concepts | These may expand reach later, but Search native signoff does not automatically prove Shopping feed/title/landing quality | Build only local concept matrices after native landing/title review and current Merchant feed proof | No native-language Shopping campaign/feed/title action until native review, current feed export, and exact approval |

## Required Read-Only Exports

1. Google Ads Standard Shopping item export for campaign `23802638621`.
   - Required columns: item ID, product title, product group/custom label, impressions, clicks, cost, search term/query where available, conversion value, landing URL.
   - Join with: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/run_us_shopping_auth_export_join_prep.py`

2. Merchant US/es exact export for source `10627981690`.
   - Required columns: item ID, title, link, language, country, feed label, source, product status, issue IDs, age_group value/effective attribute, availability, price, image link.
   - Must be current. Do not use the stale `product_issues_2026-05-08_02-52-49.csv` as action authority.

3. Merchant country/feed eligibility readbacks for `CA/en`, `GB/en`, and then `AU/en`.
   - Required proof: active/approved product count, disapproval count, shipping/currency country compatibility, paid-eligible cohort intersection, and any capacity warning intersection.

## Aggressive But Controlled Operating Rule

Run these read-only exports in parallel with the Google Ads API Basic Access wait. Do not let the Basic Access review freeze Shopping or Pinterest. However, do not create Shopping campaigns or mutate feed/title/product groups until the readbacks prove active, clean, high-intent products and the owner gives exact approval for the smallest live write.

## Decision

Fastest safe traffic path after this packet:

1. If owner gives the exact Pinterest approval phrase, create the Pinterest 333-row paused draft only.
2. Run authenticated read-only Standard Shopping item export and join it to the public-clean US packet.
3. Run exact Merchant US/es export and classify Spanish Shopping readiness.
4. Run CA/GB Shopping eligibility readbacks before any non-US Shopping build.

This is sales-moving prep because it converts the user's "other languages / Shopping" concern into exact export actions and approval gates instead of another vague audit.
