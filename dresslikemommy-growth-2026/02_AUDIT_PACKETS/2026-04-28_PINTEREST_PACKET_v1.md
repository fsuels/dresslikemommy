# PINTEREST_PACKET_v1

Generated: 2026-04-28
Platform: Pinterest
Mode: read-only authenticated browser capture. No platform or Shopify writes.

## Executive Summary

- The prior `403 Forbidden` blocker was a tooling/auth-context issue, not an account limitation. The same private Pinterest pages loaded successfully through an authenticated Chrome session.
- Catalog diagnostics are now captured. Distribution is mostly healthy: `97.18k` approved items, `309` not approved, and `0` limited ads-only.
- The visible distribution blocker is `Products out of stock`, impacting `309` items across Ads and Organic.
- Shopify catalog ingestion has `0` failed uploads, `5.97k` successful uploads, and `2.07k` warnings on the latest selected Shopify data source.
- Ads reporting shows `0 campaigns`, `0 ads`, `$0.00` spend, and `No data` for 30, 90, and 365 complete-day windows ending 2026-04-27.
- Pinterest conversion tracking is active from both Conversions API and Pinterest Tag. Event quality is `Fair`, not `Good`, on the conversion-health screen updated 2026-04-27.

## Raw Evidence Index

Raw capture folder:

- `dresslikemommy-growth-2026/01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/`

Key files:

- `catalog_distribution_diagnostics.txt`
- `catalog_ingestion_diagnostics.txt`
- `catalog_product_groups.txt`
- `catalog_data_sources.txt`
- `conversion_events_overview.txt`
- `conversion_health_expanded.txt`
- `ads_reporting_campaigns_30d.txt`
- `ads_reporting_campaigns_90d.txt`
- `ads_reporting_campaigns_365d.txt`
- `ads_reporting_ads_30d.txt`
- `ads_reporting_ads_90d.txt`
- `ads_reporting_ads_365d.txt`

## Catalog Diagnostics

Catalog: `Catalog_Retail`

Distribution overview:

- Not approved: `309` (`0.32%` of total catalog)
- Limited ads-only: `0` (`0%`)
- Approved: `97.18k` (`99.68%`)

Distribution issue:

- `Products out of stock`
- Impacting: Ads, Organic
- Pinterest guidance: products must be in stock to distribute
- Items: `309`

Latest ingestion for selected Shopify data source:

- Data source: `Shopify`, ID `3041760900274511922`
- Successful uploads: `5.97k` (`100%` of total data source)
- Failed to upload: `0`
- Warnings: `2.07k` (`34.7%`)
- Latest ingestion time: Apr 28 at 9:19 AM EDT

Ingestion warnings:

- `Warning 188`: sale_price values must be lower than original/list price; `2,010` occurrences.
- `Warning 1039`: description_html too long, item publishes without description_html; `114` occurrences.
- `Warning 126`: shallow google_product_category values may limit visibility; `4` occurrences.

## Data Sources

- `dresslikemommy.com` URL data source `3041760916127467912` failed on `sitemap_collections_1.xml`; latest ingestion Apr 28 at 3:30 AM EDT.
- Shopify localized feeds are present for multiple languages. Visible rows include several healthy `5,969` item feeds plus smaller warning deltas such as `5,937 / 32`, `5,943 / 26`, `5,945 / 24`, and `5,949 / 20`.
- The selected Shopify diagnostic source is United States / Portuguese (Brasil), ID `3041760900274511922`, `5,969` items, latest ingestion Apr 28 at 9:19 AM EDT.

## Product Groups

Metrics from: last 30 days.

Visible product groups all show `0` checkouts and `0` average order value. Top visible groups:

- All Products: `5,224` products, updated 4/11/2026.
- New Arrivals: `263` products, updated 4/28/2026.
- Best Deals: `917` products, updated 4/28/2026.
- Family Matching Sweaters & Jackets: `129` products, updated 4/28/2026.
- Daddy & Me Shirts: `276` products, updated 4/27/2026.
- Sundresses: `170` products, updated 4/27/2026.
- Family Matching Sets: `1,015` products, updated 4/27/2026.
- Family Matching Tops: `974` products, updated 4/27/2026.
- Dresses: `366` products, updated 4/27/2026.
- Mother Daughter Swimsuits: `987` products, updated 4/26/2026.

## Conversion Tracking

Events overview shows deduplicated data from all sources:

- PageVisit: Api + Tag, `13,183`, last received 2026-04-28 09:18 PM UTC.
- ViewCategory: Api + Tag, `3,130`, last received 2026-04-28 09:18 PM UTC.
- AddToCart: Api + Tag, `533`, last received 2026-04-28 05:44 PM UTC.
- InitiateCheckout: Api + Tag, `83`, last received 2026-04-28 06:01 PM UTC.
- Search: Api + Tag, `37`, last received 2026-04-27 09:28 PM UTC.
- Checkout: Api + Tag, `11`, last received 2026-04-28 05:56 PM UTC.
- AddPaymentInfo: Api + Tag, `8`, last received 2026-04-25 11:55 PM UTC.

Conversion health:

- Event quality score: `Fair`
- Updated: 2026-04-27
- Event source: Conversions API and Pinterest Tag
- Date range shown: Last 14 days / Last 1 day

Parameters to improve:

- Customer information: `Email` for AddToCart; `Click ID` for Checkout, AddToCart, InitiateCheckout, AddPaymentInfo, PageVisit, Search, and ViewCategory.
- Event insights: `Product ID` for AddPaymentInfo.
- Duplicate events: `Event ID` for PageVisit.

Parameters in good health:

- IP Address, User Agent, and External ID for core web events.
- Source URL for core web events.
- Order Value for Checkout, AddToCart, InitiateCheckout, and AddPaymentInfo.
- Order ID for Checkout.

## Ads Reporting

Windows captured:

- 30 complete days: 2026-03-29 through 2026-04-27.
- 90 complete days: 2026-01-28 through 2026-04-27.
- 365 complete days: 2025-04-28 through 2026-04-27.

Campaign view:

- 30d: `0 campaigns`, `0 currently being served`, `$0.00` spend, `No data`.
- 90d: `0 campaigns`, `0 currently being served`, `$0.00` spend, `No data`.
- 365d: `0 campaigns`, `0 currently being served`, `$0.00` spend, `No data`.

Ad view:

- 30d: `0 ads`, `0 currently being served`, `$0.00` spend, `No data`.
- 90d: `0 ads`, `0 currently being served`, `$0.00` spend, `No data`.
- 365d: `0 ads`, `0 currently being served`, `$0.00` spend, `No data`.

Targeting / optimization evidence:

- Reporting screen shows `Targeting breakdown: None`.
- Because there are no campaigns/ad groups/ads in any captured window, there is no active country targeting, budget, objective, optimization goal, creative destination URL, CPA, ROAS, or paid-Pinterest CAC to export.

## CAC Guardrail

Existing local Shopify packet provides AOV and max-CAC guardrails:

- 30 complete days: AOV `$71.91`, max CAC `$10.79`.
- 90 complete days: AOV `$68.61`, max CAC `$10.29`.
- 365 complete days: AOV `$74.78`, max CAC `$11.22`.

Pinterest paid CAC/ROAS cannot be calculated from spend because Pinterest Ads reporting shows `$0.00` spend and no campaign/ad rows for all captured windows.

## Remaining Actual Fixes

No live fixes were applied in this Pinterest pass. These are the actionable items left:

- Decide whether the `309` out-of-stock items are intentional exclusions or should be restocked/hidden from Pinterest.
- Apply or refresh the existing Shopify compare-at-price fix plan before the next Pinterest ingestion if clearing `Warning 188` is approved.
- Trim or suppress overlong `description_html` for the `114` `Warning 1039` occurrences if Pinterest description visibility is important.
- Deepen google_product_category values for the `4` `Warning 126` occurrences.
- Investigate the failed `sitemap_collections_1.xml` URL data source; it appears separate from the active Shopify product feed.
- Improve event quality by sending missing AddToCart email/enhanced-match data where consent-compliant, click ID across web events, Product ID for AddPaymentInfo, and Event ID for PageVisit deduplication.
