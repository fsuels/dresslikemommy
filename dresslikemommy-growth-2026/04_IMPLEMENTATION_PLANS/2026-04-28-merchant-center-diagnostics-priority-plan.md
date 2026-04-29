# Merchant Center Diagnostics Priority Plan

Date: 2026-04-28
Mode: read-only triage plus review-only draft artifacts. No Merchant Center, Shopify, feed, or ads write is approved by this document.

## Current Snapshot

Merchant Center account: `124884876`

Diagnostics page: `Products > Needs attention > Show all fixes`

Current evidence files:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-merchant-diagnostics-priority-triage/merchant_center_diagnostics_priority_snapshot.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-merchant-diagnostics-priority-triage/merchant_center_diagnostics_priority_snapshot.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-merchant-diagnostics-priority-triage/downloads/products_2026-04-28_17-26-54.zip`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-merchant-diagnostics-priority-triage/merchant_center_all_products_export_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-merchant-diagnostics-priority-triage/shopping_ads_non_us_country_exclusions_REVIEW_ONLY.tsv`

Merchant Center UI evidence:

- Diagnostics last updated: `Last updated at 10:59 PM Apr 28, 2026`.
- Issues captured: `17`.
- The missing `age_group` issue is now a warning with click potential `Not supported`; do not run another age_group upload in this pass.
- Highest active issue by Merchant Center rank is `Over capacity for Shopping ads (outside of CSS program)`.

All-products export evidence:

- Export rows parsed: `442,091`.
- Unique Shopify-style variant IDs parsed from `id`: `7,063`.
- Channel: `Online` for all parsed rows.
- The row explosion is country/currency/language duplication, not 442K unique Shopify variants.
- US feed label rows: `12,899`, covering `6,751` unique IDs, with `6,451` English rows and `6,448` Spanish rows.
- Top non-US country/currency feed labels include `EUR_544800865`, `CHF_544800865`, `MAD_544866401`, `LBP_544866401`, `KRW_544866401`, `JPY_544866401`, and many others.

Official Google references:

- Product quota limits: `https://support.google.com/merchants/answer/12658070`
- Excluded countries for Shopping ads `[shopping_ads_excluded_country]`: `https://support.google.com/merchants/answer/9837523`
- Missing inventory data: `https://support.google.com/merchants/answer/14980864`
- Product data specification destination attributes: `https://support.google.com/google-ads/answer/7052112`

## Current Issue Ranking

| Rank | Severity | Issue | Products | Percent | Priority interpretation |
| --- | --- | --- | ---: | ---: | --- |
| 1 | Error | Over capacity for Shopping ads (outside of CSS program) | 135,891 | 30.7% | P0 feed/destination-scope problem. |
| 2 | Error | Missing inventory data | 12,921 | 2.9% | P1 local-inventory / physical-store marketing method problem. |
| 3 | Error | Missing Korean business registration number | 12,903 | 2.9% | P1 Korea destination/registration problem. |
| 4 | Error | Product page unavailable | 5,435 | 1.2% | P2 landing-page and localization crawl problem. |
| 5 | Error | Missing product image | 4,015 | <1% | P2 feed/image pipeline problem. |
| 6 | Error | Over capacity for Shopping ads (in CSS program) | 3,503 | <1% | P0/P1 same capacity family, EEA/CSS side. |
| 7 | Error | Unsupported image type `[image_link]` | 422 | <1% | P2 image URL/file-format cleanup. |
| 8 | Error | Mismatched product price | 376 | <1% | P2 feed/landing price sync cleanup. |
| 9 | Error | Invalid price | 32 | <1% | P2 product/feed price cleanup. |
| 10 | Error | Image too small | 23 | <1% | P2 image asset cleanup. |
| 11 | Error | Sale of live animals | 2 | <1% | P2 policy false-positive or copy/product cleanup. |
| 12 | Error | Personalized advertising: personal hardships | 3,062 | <1% | P2 ad-policy/copy review. |
| 13 | Error | Personalized advertising: Identity and belief | 32 | <1% | P2 ad-policy/copy review. |
| 14 | Warning | Missing age group | 23,184 | 5.2% | Defer per operator instruction: no more age_group upload now. |
| 15 | Warning | Missing color | 15,638 | 3.5% | P3 quality warning, not a visibility-first fix. |
| 16 | Warning | Missing gender | 2,297 | <1% | P3 quality warning, Merchant Center can suggest fixes. |
| 17 | Warning | Missing size | 350 | <1% | P3 quality warning. |

## Priority Decision

The top Merchant Center problem is not an ordinary missing-attribute correction. It is that too many market/country/language rows are eligible for Shopping ads.

Google's own quota guidance says products count against quota when shown/listed/advertised, and after a quota limit is reached additional products for that use are not processed. Google lists two recovery paths: remove older products to make room or request a quota increase.

For this store, the conservative recovery path is:

1. Keep free listings broad if desired.
2. Restrict Shopping ads to the intended paid test market: United States only.
3. Keep the paid buildout paused until the clean subset passes Merchant Center, PDP, shipping, return, margin, and tracking gates.

## Proposed P0 Fix, Pending Approval

Preferred no-surprise approach:

- Do not replace `supplemental_feed_pilot.txt`.
- Do not upload another age_group file.
- Create a separate Merchant Center supplemental source for Shopping-ads country exclusions, or adjust Google & YouTube / Merchant Center source settings if the UI exposes a safer country/destination toggle.
- Use `shopping_ads_excluded_country` to exclude non-US Shopping ads countries while preserving US Shopping ads eligibility.
- Keep `Free_listings` untouched unless the owner separately approves free-listing reductions.

Review-only draft:

- `shopping_ads_non_us_country_exclusions_REVIEW_ONLY.tsv`
- Rows with non-US exclusions: `7,063`.
- IDs with US country evidence: `6,751`.
- IDs without US country evidence: `312`.
- Non-US country count: `42`.

Important caution:

- The draft includes `review_note` and `sample_title`, so it is intentionally not upload-ready.
- If a live feed is approved, generate a new upload file with only supported Merchant Center columns.
- If the existing supplemental source is reused, preserve the currently working `custom_label_4` and `age_group` behavior. The safer option is a separate supplemental source for country exclusions.

Rollback:

- Remove the new supplemental source, or upload a replacement file that clears `shopping_ads_excluded_country` for the affected IDs.
- Recheck Merchant Center source processing and diagnostics after the next refresh.

## Proposed P1 Fixes, Pending Read-Only Confirmation

### Missing Inventory Data

Google's help page says this issue is tied to local inventory data and can occur when local inventory ads/free local listings are opted in for products without matching local product inventory. For an online-only Shopify store, the likely safe direction is to turn off physical-store marketing methods or fix/remove stale local inventory data sources.

Next read-only check:

- Open Merchant Center `Marketing methods` and data source settings.
- Confirm whether `Local_inventory_ads`, `Free_local_listings`, or physical-store marketing methods are active.
- Confirm whether a local product inventory source exists and whether it has stale/mismatched IDs.
- Do not change settings until owner approval because this can affect local/free visibility.

### Missing Korean Business Registration Number

The current product export shows `KR` / `KRW` rows at approximately the same scale as the Korean registration issue. If Korea is not an intentional paid market, this should be solved by excluding South Korea from Shopping ads or removing Korea from the relevant paid target settings. If Korea remains a selling market, the owner must provide the registration requirement rather than faking it.

Next read-only check:

- Confirm whether Korea is selected as a target country/source destination in Merchant Center or Google & YouTube.
- Confirm whether Korea is active in Shopify Markets.
- Decide between `exclude KR from Shopping ads` and `provide registration`.

## Proposed P2 Cleanup Order

After capacity and destination scope are corrected, address individual product/data issues in this order:

1. Product page unavailable: download/view affected products, group by country/feed label/language, and first determine whether they are non-US localized rows that will be removed from Shopping ads by the P0 fix.
2. Missing product image and unsupported image type: group by image host/file extension and prioritize current US rows.
3. Mismatched price and invalid price: group by feed label/currency and verify Shopify/Google app sync timing before editing products.
4. Personalized advertising and sale-of-live-animals: inspect affected item titles/descriptions for false positives. Fix copy or request review only after confirming exact affected products.
5. Missing color/gender/size: treat as quality cleanup. It can improve data quality, but Merchant Center marks click potential as not supported, so it should not outrank active error fixes.

## Stop Rules

- No further `age_group` upload in this pass.
- No replacement upload to `supplemental_feed_pilot.txt` unless the upload file preserves current working columns and the owner approves.
- No Google Ads campaign creation or enablement.
- No broad country/market/feed setting change without a specific rollback note.
- No product-copy edits for policy issues until affected product IDs are exported and reviewed.
