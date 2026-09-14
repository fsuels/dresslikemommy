# Pinterest Post-Owner-Publish Readback

Timestamp: 2026-05-18 18:20 EDT.

Scope: read-only Pinterest Ads Manager readback after the owner reported manually publishing and changing max CPC to `0.10` and daily budget to `$10`.

## Readback Summary

- Advertiser: `549756244483`
- Account: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
- Reporting date range used for the decisive readback: `Today`, `2026-05-18` to `2026-05-18`
- Time zone shown by Pinterest: `UTC`

## Campaigns

Today readback showed:

- `2 campaigns`
- `1 currently being served`

Visible campaign rows:

| Status | Campaign | Objective / ID | Today spend | Today impressions | Today clicks |
|---|---|---|---:|---:|---:|
| Active | `DLM_PIN_US_CATALOG_333_EXACT_20260518` | Catalog sales, ID `626758581530` | `$0.00` | `0` | `0` |
| Archived | `Halloween Family Matching Pajamas for Adult Kids` | `[SHOPIFY] Consideration`, ID `626746948539` | `$0.00` | `0` | `0` |

The first reporting URL opened with `Last 14 days` ending `2026-05-17`, so it showed `0 campaigns / No data`. The current-day readback corrected that false negative.

## Ad Group

Readback for campaign `626758581530` showed:

- `1 ad group`
- `0 currently being served`
- Ad group: `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518`
- Objective / ID: Catalog sales, ID `2680090307739`
- Status: `Not started`
- Bid: `$0.10`
- Today spend: `$0.00`
- Today impressions: `0`
- Today clicks: `0`

The owner reported changing the daily campaign budget to `$10`. The reporting table did not expose the campaign budget amount clearly in this readback, and the ad-group budget fields were blank because the setup appears to use campaign-level budget.

## Product Groups

Readback for ad group `2680090307739` showed:

- `Ad Group: DLM_PIN_US_CATALOG_333_EXACT_20260518: 3 product groups`

| Status | Product group | Reporting product group ID | Products | Format |
|---|---|---:|---:|---|
| Active | `DLM_PIN_US_SHOPPING_MOMMY_ME_333` | `4260609808230` | 201 | Shopping |
| Active | `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333` | `4260609808229` | 103 | Shopping |
| Active | `DLM_PIN_US_SHOPPING_PAJAMAS_333` | `4260609808228` | 29 | Shopping |

This confirms broad `All Products` was not the current ad-group product-group scope in the readback.

## Ads

Direct readback for ad group `2680090307739` showed:

- `Ad Group: DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518: 0 ads`
- `0 currently being served`
- Table result: `No data`

For standard shopping/catalog sales, Pinterest help says shopping campaigns are built from product groups in the catalog; however, the reporting surface currently showing `0 ads` plus the ad group status `Not started` means delivery should be treated as not proven until a later serving/readback shows impressions or approved/distributed shopping objects.

## Keywords

Positive keyword readback for ad group `2680090307739` showed:

- `Ad Group: DLM_PIN_US_CATALOG_333_EXACT_20260518: 0 keywords`
- Table result: `No data`

Negative keyword readback showed:

- Negative keywords tab available
- Table result: `No data`

This is not automatically wrong for Pinterest Catalog sales: Pinterest Business help states that keyword or interest targeting is not necessary for catalog sales campaigns, and that Pinterest uses product data from the data source to show relevant products to people browsing product Pins. It does mean there is no keyword/negative-keyword control layer currently installed on this ad group.

## Market Scope

This is the U.S. English Pinterest test lane:

- Campaign and ad group names contain `US`.
- The selected product groups are the `DLM_PIN_US_SHOPPING_*_333` groups.
- These groups were created from clean source `DLM Cloudflare Grouped Feed 2026-05-18`, source `3041760873378113572`, configured for United States / English (US).

Canada, GB, AU, EU, and other language/market lanes should not be mixed into this campaign. Each market should have its own campaign/source or tightly isolated market-specific structure after feed/source eligibility and landing/currency proof pass.

## Expert-Level Assessment

Current state is better than broad launch, but not yet an expert finished build:

- Good: exact product-group scope is active at `201/103/29`; broad `All Products` is not visible in the ad-group product-group readback.
- Good: bid readback shows owner-adjusted max CPC `$0.10`, which lowers downside risk.
- Good: no spend has occurred yet.
- Concern: ad group status is `Not started`.
- Concern: ads readback shows `0 ads` and `0 currently being served`.
- Concern: positive keywords and negative keywords are empty.
- Concern: no conversion/ROAS evidence exists yet.

Recommended next actions are read-only first:

1. Re-read this campaign after Pinterest review/propagation, ideally after the ad review window, to confirm whether status changes from `Not started` and whether impressions begin.
2. If still `0 currently being served`, inspect the campaign/ad-group edit screens read-only for delivery blockers, ads/shopping object creation state, budget, schedule, location, language, and review status.
3. Keep the first campaign as U.S. English exact product-group shopping only. Do not add other markets into this campaign.
4. Build separate market lanes only after each market has feed/source, landing route, currency/shipping, and tracking proof.
5. Use keyword and negative keyword controls only when they serve a clear role: either a separate keyword-led consideration/search-intent Pinterest ad group/campaign, or evidence-backed negatives after search/query/reporting shows waste. Do not add negatives by hunch.

No external write occurred during this readback.
