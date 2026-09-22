# GA4 purchase receipt and Microsoft attribution audit

Status: LIVE_VERIFIED_WITH_LIMITS. Read-only audit on September 22, 2026, approximately 13:55–14:08 UTC. Operator `/root/ga4_check` used its newly created background IAB browser 2/tab 1 (session-scoped handle), property 330266838/account 88409806, dresslikemommy.com - GA4. No user tab was bound. Only report dates, dimensions and purchase metric selection changed; no settings, saved exploration, tracking or event writes.

## Property and reporting controls

Property details freshly read: reporting timezone `(GMT-04:00) New York Time`; displayed currency `US Dollar ($)`. Settings Save was disabled; no field was edited. Acquisition data quality popup states unsampled, 100% of available data, intraday and daily data, and missing/unprocessed attribution for `(data not available)`. It separately states `(not set)` means no dimension data received. Current-day values remain provisional. The key-events selector contains purchase, view_item, add_to_cart, begin_checkout and add_payment_info: an all-key-events total is not a purchase count.

## Live results

Traffic acquisition, All Users, Session source / medium; Key events explicitly selected `purchase`:

| Exact New York reporting window | Total sessions | Purchase key events | Total revenue displayed | bing / cpc sessions | bing / cpc purchase events / revenue |
|---|---:|---:|---:|---:|---:|
| September 17–22 inclusive | 660 | 3 | USD200.32 | 160 | 0 / USD0.00 |
| September 19–22 inclusive | 482 | 2 | USD135.34 | 129 | 0 / USD0.00 |

September17–22 source rows: Direct150sessions/2purchases/USD131.96; data-not-available73sessions/1purchase/USD68.36; google/organic156sessions/0purchase/USD0; google/cpc39sessions/0purchase/USD0; bing/organic3sessions/0purchase/USD0. Bing/cpc has87 engaged sessions,54.37% engagement,37seconds average engagement and812 events: diagnostic evidence of capture, not profitability.

September19–22 source rows: Direct115sessions/1purchase/USD66.98; data-not-available73sessions/1purchase/USD68.36. Session campaign breakdown shows named Microsoft US111sessions, Canada16 and Australia2, each0purchase/USD0. The unavailable source aggregate appears under campaign `(cross-network)` with73sessions/1purchase/USD68.36. That label does not prove Microsoft or Google paid attribution. Session totals are reported directly and must not be reconstructed by adding overlapping dimensional rows.

## Same-order reconciliation

Native Transactions report, September17–22, Transaction ID + Session source/medium, shows exactly3rows, each1ecommerce purchase, total purchase revenueUSD200.32. The independent Shopify lane compared full13digit numeric order IDs privately using FNV1a64 fingerprints calculated independently on the full strings; all3matched. This is practical full-identifier reconciliation rather than a suffix-only or amount-only join. Raw IDs/fingerprints are deliberately omitted from this packet; collision-free cryptographic identity was not asserted.

| Shopify creation date (New York) | GA4 ecommerce purchases | GA4 purchase revenue USD | GA4 session source/medium | Independent Shopify result |
|---|---:|---:|---|---|
| September18 | 1 | 64.98 | (direct) / (none) | Same order, USD64.98 |
| September19 | 1 | 66.98 | (direct) / (none) | Same order, USD66.98, Direct journey |
| September22 | 1 | 68.36 | (data not available) | Same order, AUD96 presentment / USD68.20 shop money, Google/SEO first and last visits |

Therefore all3 recent Shopify orders are represented once in this GA4 transaction report. This does not certify every purchase payload, every sender, every consent region, every historic order, or Microsoft UET receipt. The newest order has a confirmed USD0.16 GA4/Shopify value difference; FX conversion is a plausible explanation, not verified cause. Transaction currency was not available in the ordinary dimension picker, so raw event amount/currency remains unverified. Shopify's Google/SEO journey does not support assigning this order to Microsoft; GA4's missing attribution does not override that evidence.

## Decision and measurement limits

Since yesterday there is one newly created Shopify order represented in GA4, with GA4USD68.36 / ShopifyUSD68.20 and Shopify Google/SEO attribution. Verified Microsoft-paid purchases remain unestablished; displayed Bing-paid purchase events/revenue are0. CPA cannot be estimated from zero verified paid purchases. An observed-report ROAS would be0% if divided by a separately matched positive Microsoft spend denominator, but true campaign ROAS and contribution profit remain unknown; this lane did not read spend. No supported improvement toward ~650% ROAS or ~$10.77 CPA can be claimed, and incremental/anti-cannibalization economics are unproved.

Next action: reconcile native Microsoft UET purchase receipt, actual revenue/currency parameters and paid-goal attribution against this three-order cohort, then isolate attribution/consent continuity only where receipt evidence fails. Do not replace tracking, replay purchases or credit the cross-network row based on its label. Current report proves GA4 receipt for the cohort and a newest-order attribution gap, not complete Microsoft purchase tracking.

## Provenance

- [Transaction report](https://analytics.google.com/analytics/web/#/a88409806p330266838/reports/explorer?ruid=019f8def-dfd0-4785-a638-262fce4dc7be&restoreUserState=true&r=transaction-id-report&params=_u.comparisonOption%3Ddisabled%26_u.date00%3D20260917%26_u.date01%3D20260922%26_u..nav%3Dmaui%26_r.explorerCard..seldim%3D%5B%22transactionId%22,%22sessionSourceMedium%22%5D&collectionId=11131314159)
- [Purchase-specific traffic report](https://analytics.google.com/analytics/web/#/a88409806p330266838/reports/explorer?ruid=9e76d775-fa38-4693-8f67-6988e6b98a76&restoreUserState=true&r=lifecycle-traffic-acquisition-v2&params=_u.comparisonOption%3Ddisabled%26_u.date00%3D20260917%26_u.date01%3D20260922%26_r.explorerCard..columnFilters%3D%7B%22conversionEvent%22:%22purchase%22%7D)
- [Property clock/currency readback](https://analytics.google.com/analytics/web/#/a88409806p330266838/admin/property/settings?restoreUserState=true)

Evidence derives from settled rendered native report tables and property controls; no screenshot or export was retained. Private table IDs were used transiently for reconciliation. Shopify facts above are independently reported by `/root/shopify_orders`; parent owns cross-platform final acceptance.
