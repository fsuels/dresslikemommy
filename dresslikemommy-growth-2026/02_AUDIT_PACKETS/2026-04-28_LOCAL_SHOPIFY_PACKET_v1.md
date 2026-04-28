# LOCAL_SHOPIFY_PACKET_v1

Generated: 2026-04-28
Store: dresslikemommy.com / dresslikemommy-com.myshopify.com
Mode: read-only Shopify/API/theme/public-site audit. No Shopify writes. No theme implementation edits.

## 1. Executive Summary

- Catalog scope: 793 total products, 335 active products, 19661 total variants, 7324 active variants.
- Paid eligibility result after the economics gate: SCALE_PAID = 0, TEST_PAID = 0, ORGANIC_ONLY = 0, FIX_BEFORE_PAID = 1414, EXCLUDE_PAID = 5910.
- Cost/margin gate: 5928 active variants still lack variant unitCost, 1396 active variants have unitCost, and 1414 active variants have a reliable cost basis from variant unitCost or operator-approved product margin tier. Only 64 active variants with 365-day sales also have known variant unitCost.
- Financial guardrail: minimum paid ROAS is 6.67; max CAC is AOV × 0.15. Last-30-day AOV is $71.91, so max CAC is $10.79.
- Public validation: `/collections/bottoms` returned 200 with 3 unique product links, so it is not validated as empty. The sampled Spanish PDP returned 1 live translation-missing hit.
- Main blocker to paid scaling: exact SKU/variant costs and feed readiness. No active variant qualifies for paid scale/test under the hard rules.

## 2. Financial Tables

|date_range|start_inclusive|end_exclusive|orders_non_cancelled|revenue|aov|discounts|refunds|shipping_charged|taxes|payment_fees|units_sold|marketing_cap_15pct|max_cac|refund_rate_revenue_pct|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|last_30_days|2026-03-29|2026-04-28|15|1078.59|71.91|0.00|0.00|39.19|0.00|63.12|52|161.79|10.79|0.00|
|last_90_days|2026-01-28|2026-04-28|36|2469.79|68.61|0.00|43.98|65.17|0.00|135.74|112|370.47|10.29|1.78|
|last_365_days|2025-04-28|2026-04-28|81|6057.22|74.78|5.49|43.98|131.16|0.00|334.03|274|908.58|11.22|0.73|

Financial notes:
- Revenue uses Shopify order `totalPriceSet` for non-canceled orders.
- Payment fees were available from Shopify transaction fees and included as totals, not allocated by variant.
- Variant contribution uses known Shopify `inventoryItem.unitCost` only; unknown costs remain UNKNOWN_MARGIN.
- INSUFFICIENT_EVIDENCE: ad spend, ad conversion value, GA4 ecommerce attribution, and campaign-level ROAS/CAC exports are not present.

Full tables:
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_financial_summary.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_variant_financials.csv`

## 3. Product Eligibility Table

Summary:

|Paid status|Active variant count|
|---|---:|
|SCALE_PAID|0|
|TEST_PAID|0|
|ORGANIC_ONLY|0|
|FIX_BEFORE_PAID|1414|
|EXCLUDE_PAID|5910|

Sample rows by 365-day revenue:

|handle|variant_id|sku|revenue_365d|units_365d|unit_cost|margin_status|inventory_quantity|paid_status|paid_status_reasons|
|---|---|---|---|---|---|---|---|---|---|
|chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit|41493869101153|4939515852335-Color:Sequin;Size:Child 3T;|46.41|2|5.62|HIGH_MARGIN|806|FIX_BEFORE_PAID|PRODUCT_DATA_DEFECTS:image_dimensions/size|
|men-kids-matching-tropical-leaf-print-cotton-short-sleeve-shirt-cream-green|43731176063073||45.98|2||UNKNOWN_MARGIN|98|EXCLUDE_PAID|ECONOMICS_GATE:UNKNOWN_COST_NO_RELIABLE_COST_BASIS;UNKNOWN_MARGIN;PRODUCT_DATA_DEFECTS:image_dimensions/size;VARIANT_DEFECTS:gtin_barcode_missing/sku_missing/unit_cost_missing|
|matching-mother-and-daughter-beach-dresses-elegant-cream-chiffon-maxi-dress-set|41871777693793|4987553113359-01|34.73|1|10.12|HIGH_MARGIN|2520|FIX_BEFORE_PAID|PRODUCT_DATA_DEFECTS:image_dimensions|
|chic-family-tides-mother-daughter-matching-two-piece-swimsuit-with-skirt-vibrant-versatile-swimwear-collection|41497976799329|5374260266719-Size:Mother S;Color:Pink;|33.98|2|7.31|GOOD_MARGIN|196|FIX_BEFORE_PAID|PRODUCT_DATA_DEFECTS:color/image_dimensions/size|
|matching-mother-and-daughter-heart-knit-cardigans-cream-and-black-sweaters-for-mommy-me|41871763964001|5260557579041-01|33.61|1|10.97|HIGH_MARGIN|118|FIX_BEFORE_PAID|PRODUCT_DATA_DEFECTS:image_dimensions;VARIANT_DEFECTS:variant_image_missing|
|mommy-daughter-matching-tie-dye-dress|40321240891489|14:175#1pc;5:361385#Mother L|32.99|1||UNKNOWN_MARGIN|12362|EXCLUDE_PAID|ECONOMICS_GATE:UNKNOWN_COST_NO_RELIABLE_COST_BASIS;UNKNOWN_MARGIN;PRODUCT_DATA_DEFECTS:image_dimensions;VARIANT_DEFECTS:gtin_barcode_missing/unit_cost_missing|
|mommy-daughter-matching-tie-dye-dress|40321240924257|14:175#1pc;5:100014065#Mother XL|32.99|1||UNKNOWN_MARGIN|12384|EXCLUDE_PAID|ECONOMICS_GATE:UNKNOWN_COST_NO_RELIABLE_COST_BASIS;UNKNOWN_MARGIN;PRODUCT_DATA_DEFECTS:image_dimensions;VARIANT_DEFECTS:gtin_barcode_missing/unit_cost_missing|
|gradient-ombre-family-matching-outfits-pink-blue-t-shirts-with-white-shorts-set|41878478356577|5457112755516-01|32.44|2|2.81|HIGH_MARGIN|9985|FIX_BEFORE_PAID|PRODUCT_DATA_DEFECTS:color/image_dimensions/size|
|green-tropical-leaf-daddy-and-me-matching-swim-shorts-for-pool-days|43768831311969|5207291341771-Size:XL;Color:Green leaf beach pants;|31.98|2|5.06|HIGH_MARGIN|252|FIX_BEFORE_PAID|PRODUCT_DATA_DEFECTS:color/image_dimensions/size|
|matching-family-denim-button-up-shirts-casual-unisex-jean-jackets-for-parents-and-kids|41872740155489|4955682869423-01|30.78|1|9.28|HIGH_MARGIN|973|FIX_BEFORE_PAID|PRODUCT_DATA_DEFECTS:image_count/image_dimensions|
|+ 7314 more rows in CSV||||||||||

Full table: `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_product_eligibility.csv`

## 4. Custom-Label Table

Recommended labels were generated locally only, not written to Shopify or feed fields.

|Label|Meaning|Counts|
|---|---|---|
|custom_label_0|margin_tier|{"GOOD_MARGIN": 52, "HIGH_MARGIN": 1332, "MID_MARGIN": 12, "UNKNOWN_MARGIN": 5928}|
|custom_label_1|sales_velocity|{"HISTORICAL_ONLY": 132, "LOW_90D": 1, "MEDIUM_30D": 4, "NO_SALES": 7187}|
|custom_label_2|inventory_status|{"IN_STOCK": 7227, "OUT_OF_STOCK": 97}|
|custom_label_3|price_bucket|{"25_50": 1661, "50_75": 3, "UNDER_25": 5660}|
|custom_label_4|paid_status|{"EXCLUDE_PAID": 5910, "FIX_BEFORE_PAID": 1414}|

Full table: `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_custom_labels.csv`

## 5. Feed Defect Table

Severity counts: {"HIGH": 6102, "LOW": 77, "MEDIUM": 8329}

Top defect counts:

|field|count|
|---|---|
|unit_cost_missing|5928|
|gtin_barcode_missing|5897|
|sku_missing|1604|
|image_dimensions|308|
|size|202|
|color|167|
|variant_image_missing|128|
|out_of_stock|97|
|alt_text|77|
|market_availability|48|
|description|23|
|age_group|18|
|image_count|4|
|seo_title|2|
|seo_meta_description|2|
|google_product_category|1|
|gender|1|
|collection_page_readiness|1|

Full table: `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_feed_defects.csv`

## 6. Localization Defect Table

Published locales: ar, cs, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, nl, no, pl, pt-BR, ro, ru, sv

|locale|active_products_checked|missing_title|missing_body_html|missing_meta_description|outdated_title|outdated_body_html|outdated_meta_description|english_fragment_hits|severity|
|---|---|---|---|---|---|---|---|---|---|
|ar|335|0|3|2|8|30|135|128|HIGH|
|cs|335|0|3|2|8|29|6|342|HIGH|
|da|335|0|3|2|8|26|3|391|HIGH|
|de|335|0|3|2|8|29|6|534|HIGH|
|el|335|0|3|2|8|26|3|398|HIGH|
|es|335|0|3|2|8|26|3|265|HIGH|
|fi|335|0|3|2|8|26|3|344|HIGH|
|fr|335|0|3|2|9|50|109|155|HIGH|
|he|335|0|3|2|8|26|3|304|HIGH|
|hi|335|0|3|2|8|27|4|251|HIGH|
|it|335|0|3|2|8|28|134|159|HIGH|
|ja|335|0|3|2|8|28|134|53|HIGH|
|ko|335|0|3|2|8|27|4|342|HIGH|
|nl|335|0|3|2|8|28|134|233|HIGH|
|no|335|0|3|2|8|26|3|421|HIGH|
|pl|335|0|3|2|8|28|134|166|HIGH|
|pt-BR|335|0|3|2|8|27|3|297|HIGH|
|ro|335|0|3|2|8|26|3|347|HIGH|
|ru|335|249|228|249|8|27|3|10|HIGH|
|sv|335|249|252|249|8|26|3|116|HIGH|

Live/public validation added:
- Spanish sample PDP translation-missing hits: 1.
- Local theme locale JSON files for published locales had 0 missing keys in this static key comparison, so the Spanish issue appears to be live section/settings translation or non-standard key usage, not a missing local JSON file key.

Full table: `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_localization_defects.csv`

## 7. Theme/Tracking Defect Table

|scope|severity|evidence|profit_or_feed_impact|recommended_fix_plan|rollback_method|
|---|---|---|---|---|---|
|tracking_owner|MEDIUM|layout/theme.liquid initializes window.dataLayer and assets/analytics.js only; ops/customer-events/ga4-checkout-ecommerce-pixel.js is a deprecation stub. Public home showed gtag_js_hits=0, gtm_hits=0, google_ads_hits=8, shopify_web_pixel_hits=5.|Paid ROAS/CAC cannot be trusted until Google & YouTube app / ad-platform conversion settings are verified outside the theme.|Export/verify Google Ads conversion actions and Shopify Google & YouTube app status before any paid scaling.|No code rollback needed for audit; do not add duplicate GTM/gtag scripts.|
|schema_shipping_policy_mismatch|HIGH|snippets/jsonld-seo.liquid hardcodes handlingTime 2 days and transitTime 7-10 days; live shipping policy says processing 1-3 business days, US 7-15, CA/UK 10-20, AU 12-25.|Structured-data shipping promises can conflict with actual policy and paid landing-page expectations.|Dry-run schema update to align JSON-LD delivery windows with policy/market-specific shipping settings.|Revert snippet change or restore previous jsonld-seo.liquid from git.|
|reviews_consistency|MEDIUM|templates/product.json has Judge.me preview_badge and review_widget app blocks; sections/main-product.liquid also has native rating block. Public sample PDP has no_reviews_hits=1 and customer_photo_reviews_hits=3.|Review trust can look inconsistent if app badge says no reviews while custom headings/prompts are shown.|Visually verify PDP review states and make one source of truth for empty state, badge, review widget, and schema rating.|Disable/revert only the selected review block/settings change after screenshot comparison.|
|localization_live_missing_key|HIGH|Public Spanish PDP has translation_missing_hits=1; observed footer key text includes Translation missing for customer care heading.|Paid non-English traffic can land on visibly broken localized pages.|Fix live theme/section translation source for Spanish footer/customer-care heading before paid ES traffic.|Restore previous locale/section setting or remove paid language targeting.|
|country_currency_scope|MEDIUM|Public pages expose about 304 country option markers; Shopify export shows 6 active markets, 21 published languages, and shipping zones include named Epacket countries plus Rest of world wildcard.|Large country/currency selector can imply full readiness across countries where shipping speed/returns expectations may be weaker.|Create paid-country allowlist until shipping promises, policy copy, and localization are validated by country.|Revert paid location targeting; no theme rollback needed unless selector settings are changed.|
|speed_payload|MEDIUM|Public page HTML sizes: home=888550 bytes, collection all=1613964 bytes, sample PDP=930305 bytes; Judge.me app embed active in config/settings_data.json.|Large HTML/app payloads can depress conversion rate and paid landing-page quality.|Profile app embeds, country selector payload, and review scripts before paid scale.|Disable reverted app embed/settings changes if conversion or reviews regress.|
|subscription_text_validation|LOW|Public sample PDP has subscription_word_hits=10 but selling_plan_hits=16 and deferred_purchase_hits=0; context is Shopify wallet internals, not visible product subscription copy from this static read.|No visible subscription/deferred-purchase text confirmed in static HTML, but browser visual QA is still needed.|Use browser screenshot/DOM QA on 3 PDPs before marking resolved.|No rollback unless a visible copy fix is approved later.|
|cart_drawer|LOW|snippets/cart-drawer.liquid is present and uses cart.js/quantity-popover; no live cart interaction was performed in this read-only audit.|Cart issues can affect conversion, but this pass did not mutate or test checkout flow.|Run manual/browser cart drawer QA with one add-to-cart, quantity update, remove, and checkout click in a future approved test.|No rollback for read-only QA.|

Public validation table: `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_public_site_validation.csv`

## 8. Pages/Products To Exclude From Paid

- Exclude/Fix-before-paid rows: 7324 active variant rows across 335 active product handles; 5910 are hard `EXCLUDE_PAID` after the economics gate and 1414 remain `FIX_BEFORE_PAID`.
- `/collections/bottoms`: not excluded as empty from this audit; status 200 with 3 unique product links.
- Exclude all non-English paid campaigns until product translation defects are fixed or allowlisted by locale; Russian and Swedish have the most severe missing product translation coverage in this export.
- Exclude all variants with unknown cost/no reliable cost basis, out-of-stock state, missing critical feed fields, or image/readiness defects until corrected. Missing unitCost can only pass the economics gate when product-level margin tier provides an operator-approved reliable cost basis.

Full exclude table: `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_exclude_from_paid.csv`

## 9. Highest-Impact Fixes

1. Cost/margin backfill dry run
   - Expected impact: unlock paid eligibility decisions for up to 5928 UNKNOWN_MARGIN active variants.
   - Risk: wrong costs create unprofitable scaling decisions.
   - Verification: readback unitCost, recompute custom_label_0 and paid_status, spot-check sold variants.
   - Rollback: restore prior unitCost values from export/backup before write.

2. Feed attribute cleanup dry run
   - Expected impact: reduce 5897 barcode/GTIN defects, 5928 unit-cost defects, 1604 SKU defects, 308 image-dimension defects.
   - Risk: bad feed attributes can disapprove products or misclassify traffic.
   - Verification: Shopify readback plus Merchant Center item diagnostics after feed refresh.
   - Rollback: restore previous metafields/variant fields from raw export.

3. Shipping schema alignment dry run
   - Expected impact: removes mismatch between JSON-LD delivery promises and public shipping policy.
   - Risk: schema changes can affect rich-result interpretation.
   - Verification: rendered HTML JSON-LD parse, Rich Results/schema validator, public policy comparison.
   - Rollback: revert `snippets/jsonld-seo.liquid`.

4. Localization paid allowlist
   - Expected impact: prevents paid traffic to visibly broken or partially English localized pages.
   - Risk: narrower market reach.
   - Verification: locale CSV defects, public page checks, screenshots before enabling paid language/country groups.
   - Rollback: restore broader targeting only after translation defects are fixed.

5. Tracking proof export
   - Expected impact: makes ROAS/CAC enforceable against the 6.67 / AOV×0.15 rules.
   - Risk: duplicate conversion actions or undercounting can mislead bidding.
   - Verification: Google Ads conversion actions, Shopify Google & YouTube app, GA4 purchase parity, test order/event trace.
   - Rollback: keep only the approved primary purchase action; do not add duplicate theme GTM/gtag.

## 10. Required Files/Settings For Fixes

- Shopify Admin cost/unitCost export or source-of-truth COGS file by variant SKU/id.
- Google Ads export: campaign, cost, conversions, conversion value, conversion action, clicks, impressions for the same 30/90/365 windows.
- GA4 ecommerce acquisition export by source/medium/campaign for purchases and revenue.
- Merchant Center item diagnostics after next feed refresh.
- Shopify Google & YouTube app conversion action screen/settings.
- Translation source for live footer/section settings, especially Spanish customer-care footer heading.
- Browser screenshots for product reviews, localization selector, cart drawer, and PDP selling-plan visual state.

## 11. Backup/Rollback Plan

- Before any Shopify write, create a dated raw readback export for touched products/variants/metafields.
- For theme fixes, create a branch and rely on git diff/revert for `snippets/jsonld-seo.liquid`, `sections/main-product.liquid`, locale files, or cart snippets.
- For feed label writes, keep old/new CSV and writeback report with variant/product IDs.
- For paid-platform changes, export current campaign/settings state and use platform change history to revert budgets, targeting, and conversion-action status.
- For localization, export current theme locale JSON and live section settings before editing.

## 12. JSON Block

```json
{
  "platform": "LOCAL_SHOPIFY",
  "date_ranges": {
    "last_30_days": {
      "start_inclusive": "2026-03-29T00:00:00-04:00",
      "end_exclusive": "2026-04-28T00:00:00-04:00"
    },
    "last_90_days": {
      "start_inclusive": "2026-01-28T00:00:00-05:00",
      "end_exclusive": "2026-04-28T00:00:00-04:00"
    },
    "last_365_days": {
      "start_inclusive": "2025-04-28T00:00:00-04:00",
      "end_exclusive": "2026-04-28T00:00:00-04:00"
    }
  },
  "financial_summary": [
    {
      "date_range": "last_30_days",
      "start_inclusive": "2026-03-29",
      "end_exclusive": "2026-04-28",
      "orders_processed": "16",
      "orders_non_cancelled": "15",
      "orders_cancelled": "1",
      "revenue": "1078.59",
      "subtotal": "1039.40",
      "discounts": "0.00",
      "refunds": "0.00",
      "shipping_charged": "39.19",
      "taxes": "0.00",
      "payment_fees_available": "YES",
      "payment_fees": "63.12",
      "units_sold": "52",
      "aov": "71.91",
      "refund_rate_revenue_pct": "0.00",
      "gross_margin_before_marketing_50pct_est": "539.30",
      "marketing_cap_15pct": "161.79",
      "max_cac": "10.79",
      "min_roas": "6.67",
      "contribution_after_marketing_35pct_before_other_costs": "377.51",
      "source_counts": "{\"web\": 16}",
      "currency_counts": "{\"USD\": 16}",
      "orders_with_unpaginated_line_items": "0",
      "refunds_with_unpaginated_line_items": "0"
    },
    {
      "date_range": "last_90_days",
      "start_inclusive": "2026-01-28",
      "end_exclusive": "2026-04-28",
      "orders_processed": "38",
      "orders_non_cancelled": "36",
      "orders_cancelled": "2",
      "revenue": "2469.79",
      "subtotal": "2404.62",
      "discounts": "0.00",
      "refunds": "43.98",
      "shipping_charged": "65.17",
      "taxes": "0.00",
      "payment_fees_available": "YES",
      "payment_fees": "135.74",
      "units_sold": "112",
      "aov": "68.61",
      "refund_rate_revenue_pct": "1.78",
      "gross_margin_before_marketing_50pct_est": "1234.90",
      "marketing_cap_15pct": "370.47",
      "max_cac": "10.29",
      "min_roas": "6.67",
      "contribution_after_marketing_35pct_before_other_costs": "864.43",
      "source_counts": "{\"web\": 38}",
      "currency_counts": "{\"USD\": 38}",
      "orders_with_unpaginated_line_items": "0",
      "refunds_with_unpaginated_line_items": "0"
    },
    {
      "date_range": "last_365_days",
      "start_inclusive": "2025-04-28",
      "end_exclusive": "2026-04-28",
      "orders_processed": "87",
      "orders_non_cancelled": "81",
      "orders_cancelled": "6",
      "revenue": "6057.22",
      "subtotal": "5926.06",
      "discounts": "5.49",
      "refunds": "43.98",
      "shipping_charged": "131.16",
      "taxes": "0.00",
      "payment_fees_available": "YES",
      "payment_fees": "334.03",
      "units_sold": "274",
      "aov": "74.78",
      "refund_rate_revenue_pct": "0.73",
      "gross_margin_before_marketing_50pct_est": "3028.61",
      "marketing_cap_15pct": "908.58",
      "max_cac": "11.22",
      "min_roas": "6.67",
      "contribution_after_marketing_35pct_before_other_costs": "2120.03",
      "source_counts": "{\"web\": 87}",
      "currency_counts": "{\"USD\": 87}",
      "orders_with_unpaginated_line_items": "0",
      "refunds_with_unpaginated_line_items": "0"
    }
  ],
  "active_products": 335,
  "active_variants": 7324,
  "paid_eligibility_counts": {
    "EXCLUDE_PAID": 5910,
    "FIX_BEFORE_PAID": 1414
  },
  "unknown_cost_active_variants": 5928,
  "known_cost_active_variants": 1396,
  "active_variants_with_365d_sales": 137,
  "known_cost_active_variants_with_365d_sales": 64,
  "feed_defect_counts": {
    "size": 202,
    "image_dimensions": 308,
    "google_product_category": 1,
    "color": 167,
    "gender": 1,
    "age_group": 18,
    "collection_page_readiness": 1,
    "market_availability": 48,
    "description": 23,
    "image_count": 4,
    "seo_title": 2,
    "seo_meta_description": 2,
    "alt_text": 77,
    "gtin_barcode_missing": 5897,
    "unit_cost_missing": 5928,
    "out_of_stock": 97,
    "sku_missing": 1604,
    "variant_image_missing": 128
  },
  "localization_defect_locale_count": 20,
  "theme_tracking_defect_count": 8,
  "exclude_from_paid_variant_rows": 7324,
  "exclude_from_paid_unique_product_handles": 335,
  "minimum_roas": 6.67,
  "max_cac_formula": "AOV * 0.15",
  "shopify_write_status": "NO_SHOPIFY_WRITES",
  "theme_write_status": "NO_THEME_CODE_CHANGES"
}
```
