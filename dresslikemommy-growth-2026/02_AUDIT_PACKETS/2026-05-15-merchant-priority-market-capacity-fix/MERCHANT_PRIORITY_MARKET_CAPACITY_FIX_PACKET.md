# Merchant Priority Market Capacity Fix Packet

Generated: 2026-05-15 06:31 EDT

Mode: local/read-only packet from the current Merchant all-products browser RPC export. No Merchant, Shopify, Google Ads, Pinterest, feed, product, product-group, bid, budget, status, capacity, billing, credential, or conversion writes were made.

## Owner Priority Order

The owner clarified the market priority:

1. USA English.
2. USA Spanish.
3. Canada English and Canada French.
4. England / GB English.
5. Other Europe later.

The owner also directed that Asian, African, and South American country coverage should be removed to open Merchant capacity for the priority markets.

## Current Merchant Footprint

Current all-products rows: `351,007`.

| Bucket | Current rows | Decision |
|---|---:|---|
| USA English | `5,491` | Protect |
| USA Spanish | `5,412` | Protect |
| Canada English/French | `0` | Target market missing; enable only after capacity cleanup |
| GB English | `0` | Target market missing; enable only after capacity cleanup |
| Europe later | `134,932` | Keep for later review because owner named Europe as a later priority |
| Asia / Middle East | `129,112` | Remove from Merchant/Google publishing scope |
| Africa | `37,511` | Remove from Merchant/Google publishing scope |
| South America | `8,818` | Remove from Merchant/Google publishing scope |
| Non-US USD groups | `24,243` | Remove-review-first; not the protected `US` feed label |
| Oceania / NZD | `5,488` | Hold as not-current-priority; remove only if more capacity is still needed |

Recommended first cleanup removes `199,684` rows from non-priority Asian/Middle East, African, South American, and non-US-USD groups while preserving USA English, USA Spanish, and Europe-later groups.

## Shopify Markets Readback

Read-only Shopify Admin GraphQL markets readback found the likely control surface:

| Shopify market | Status | Regions |
|---|---|---:|
| United States | `ACTIVE` / primary | `1` |
| Canada | `ACTIVE` | `1` |
| United Kingdom | `ACTIVE` | `1` |
| Eurozone | `ACTIVE` | `43` |
| Australia | `ACTIVE` | `1` |
| International | `ACTIVE` | `73` |

The `International` market contains many of the non-priority regions that map to the Merchant row explosion, including Asia/Middle East, Africa, and South America. This makes the likely live cleanup target Shopify Markets / `International` region membership or the equivalent Google & YouTube publishing scope. Do not disable or remove a whole market blindly; first confirm the live preview preserves the separate `United States`, `Canada`, `United Kingdom`, and Europe/Eurozone coverage.

## Exact Removal Candidate Groups

Use `merchant_capacity_removal_candidate_groups.csv` as the authoritative local candidate list for the first capacity cleanup. It contains only feed/language/currency groups classified as:

- `REMOVE_ASIA_MIDDLE_EAST`
- `REMOVE_AFRICA`
- `REMOVE_SOUTH_AMERICA`
- `REMOVE_NON_US_USD_REVIEW_FIRST`

Do not delete Shopify products. Do not remove the `US|en|USD` or `US|es|USD` groups. Do not treat Canada or GB as working yet; they are absent from the current Merchant export and need feed/source enablement after capacity pressure is reduced.

## Safe Execution Boundary

The live action must be market/feed-country scoping only. It must not:

- delete products
- change Shopify titles, prices, inventory, variants, vendors, product types, or source data
- change Google Ads campaigns, bids, budgets, product groups, conversion goals, or status
- request capacity before pruning non-priority markets
- remove Europe in the first pass
- remove USA English or USA Spanish

Before any `Save`, `Apply`, `Sync`, `Upload`, or equivalent live action, the operator must read back the exact platform control surface and confirm the selected removal set matches the candidate CSV, with USA English/Spanish preserved.

## After-State Readback Required

After the scoped market/feed-country cleanup, capture a fresh Merchant all-products export and verify:

- total Merchant rows drop from `351,007`
- USA English rows remain present
- USA Spanish source `10627981690` rows remain present
- Asian/Middle East, African, South American, and non-US-USD candidate groups are gone or disabled
- Canada English/French and GB English can then be enabled/exported in the expected CAD/GBP rows
- `US/es` issue/capacity state is rechecked before any Shopping build

## Files

- `merchant_priority_market_capacity_fix_summary.json`
- `merchant_feed_language_currency_capacity_groups.csv`
- `merchant_capacity_removal_candidate_groups.csv`
- `merchant_priority_keep_or_enable_groups.csv`
- `shopify_markets_readback_sanitized.json`
- `shopify_markets_regions_sanitized.csv`

## Decision

The capacity problem is not caused by only `160` active Shopify products. It is caused by Merchant row multiplication across variants, language, currency, country/feed labels, and non-priority market feeds. The sales-moving fix is to prune non-priority country/feed coverage first, then restore/verify priority rows for USA English, USA Spanish, Canada English/French, and GB English before any Shopping campaign or product-group decision.
