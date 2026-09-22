# Microsoft live readback — September 22, 2026

Status: VERIFIED_WITH_LIMITS. Parent read-only native IAB browser2/tab4; account477439/customer770182/UET36005151. Observations approximately13:54–14:10UTC. This task created a separate background tab; user tabs were not edited. No business Save or tracking change. A goal editor was inspected and Cancel closed it with no warning or field edits.

## Campaign reports

Native reporting timezone label: Eastern Time (U.S. & Canada). September22 is partial; UI warns of up to two hours of unreported recent UET conversions.

| Report dates, inclusive | Spend USD | Clicks | Impressions | Reported conversions | Reported revenue USD |
|---|---:|---:|---:|---:|---:|
| Sep17–22 | 28.04 | 211 | 9,729 | 0 | 0 |
| Sep19–22 | 23.60 | 174 | 8,455 | 0 | 0 |

Windows overlap; do not add them. September1–22 chart shows first nonzero clicks September17:3; September18:34,19:65,20:54,21:47,22:8. This establishes reported click dates, not exact campaign activation time.

Sep17–22 split: Search68clicks/USD7.80; Audience143/USD20.24. Sep19–22 split: Search51/USD6.10; Audience123/USD17.50. Six visible campaigns enabled, three paused. No campaign status, bid, budget or placement change. Zero reported values do not prove zero actual attributed sales or valid economic ROAS.

## Goal and tagging checks

- UET ShopifyImport36005151 Active; header Consent Need Attention.
- Primary ShopifyCheckoutCompleteEventTracking: Active, categoryPurchase, Custom event, Action Equals purchase, ShopifyImport tag, variable value, USD0.00 fallback, CountAll, account scope477439, click window30days, view-through1day, Lastclick, auto-biddingYes. Enhanced conversion tracking unchecked. No defect identified in those matching settings.
- Primary status No recent conversions; legacy ShopifyCheckoutCompleteTracking and Purchases URL goals excluded from auto-bidding. Smart goal excluded. ShopifyAddToCart is Recording conversions but excluded from auto-bidding; it is not a purchase metric.
- Native Account level options: Add Microsoft Click ID (MSCLKID) to URLs checked; UTM auto-tagging checked, Replace all existing tags selected. Account tracking template and final URL suffix blank. Lower-level overrides were not exhaustively audited.

## UET receiver and consent limits

- Sep17–22 settled table:3Custom purchase events; Sep19–22 settled table:2. September1–22 has5. Counts are receiver events, not identifiable or deduplicated orders and not ad attribution.
- Sep19–22: pageview2,432; view_item278; home52; begin_checkout1; add_to_cart33; search3. Different event counts do not establish a broken checkout funnel; no controlled identical-population journey was measured.
- Purchase parameter summary GoalValue and3others; prior exact popup records Currency,PageType,ProductId. Current UI did not expose exact purchase values/currency/order identifiers. No aggregate count matching was promoted to an order join.
- Purchase Healthy tooltip was opened: no EEA/UK/Switzerland events detected. It is not global consent validation.
- Current begin_checkout Missing tooltip opened:0% of events from EEA/UK/Switzerland had a consent signal in last7days; other regions excluded and denominator absent. It measures signal presence, not consent granted and not all-country/all-sender correctness. view_item/add_to_cart also display Missing; pageviews Moderate.
- Publisher code remains byte-identical with cookie defect, per SOURCE_REFRESH.md. Actual recent-order click-ID loss and production duplicates remain unproved.

## Sources and actions

[Campaigns](https://ui.ads.microsoft.com/campaign/vnext/campaigns?aid=477439&cid=770182), [UET](https://ui.ads.microsoft.com/campaign/vnext/uettag?tagId=36005151&aid=477439&cid=770182), [Account level options](https://ui.ads.microsoft.com/campaign/vnext/accountsettings?aid=477439&cid=770182). Native UI AX/DOM observations are summarized above without account email/address or customer data.

Report filters changed only in the disposable task tab. No click-ID fabrication, ad clicking, event replay, test purchase, consent change, enhanced-conversion enablement, tracking installation, support send or campaign mutation. Existing sole account writer and shared canonical writer retain ownership.
