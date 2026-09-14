Confidence: H for configured rates/zones; automatic-import acceptance and delivery accuracy remain unverified.

# Merchant513542500 — current Shopify shipping configuration

**Conditional automatic-import candidate; not yet proof of accurate coverage.** Current source is **2026-09-08 21:27:50 UTC** for zones/rates and **21:28:32 UTC** for exact weight bounds. Shopify15571635 / Dress Like Mommy / `dresslikemommy-com.myshopify.com` / USD match.

One **General profile10664050785**, default=true/version4; **zero custom profiles**, one location group, two zones, four active flat rates. The API reports two origin locations and zero locations without rates; private location details were neither requested nor saved.

| Zone | Returned region definition | Active methods |
|---|---|---|
| Countries Epacket | **US, AU, CA, FR, IL, NO, RU, SA, UA, GB**; province-code entries US62/AU8/CA13/RU82/GB5 | Free Standard Shipping **USD0.00**, unconditional. Priority Shipping **USD12.99**, total weight **0–5lb inclusive**. |
| Rest of world | Explicit restOfWorld=true entry | Same two methods and exact conditions. |

“Countries Epacket” is the configured zone label, not carrier/dispatch evidence. The profile's **zoneCountryCount244** is an API aggregate; the returned explicit set is ten country codes plus Rest of world. This does not establish244 eligible Google destinations or live country/product checkout paths. [JSON](MERCHANT_513542500_SHOPIFY_SHIPPING_CONFIG_20260908.json) preserves exact region codes and method IDs.

**Pagination complete:** one profile page, one zone page, two method pages; profile/location-group/country/province lists fully returned. Four active returned methods reconcile to the profile count. Two priority methods were separately read by exact IDs to resolve all four numeric weight conditions.

**Transit remains UNKNOWN.** Every method description is empty; names contain no numeric delivery range. Exposed DeliveryMethodDefinition and DeliveryRateDefinition types contain no numeric transit field; no alternative/private API was attempted. This does not prove that no native transit setting exists. The [policy readback](MERCHANT_513542500_SHOPIFY_POLICY_READBACK_20260908.md) separately states1–3business-day processing, possible1–2additional days, and checkout-dependent transit; cutoff/calendar remain unknown.

[Shopify's current requirements](https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google/requirements) allow import from the General profile for supported target countries with a shipping zone; the app tests importability. Explicit custom-flat-rate transit settings can supply timing. Otherwise regional typical transit and average Shopify merchant handling may be used. Accordingly, this single-General/static-rate configuration supports trying automatic import, but app acceptance and imported service accuracy still require readback. Default averages do not verify DLM fulfillment times.

**Root's next action:** test the existing automatic-import option within the exact intended countries, then inspect Merchant service regions, zero-price standard rate, USD12.99 priority0–5lb conditions and timing. Compare intended destinations with actual checkout/product eligibility. Hold any unsupported transit promise; do not create global free shipping from Rest of world or invent delivery days.

Execution: three successful read queries. One earlier detail request was rejected before data because its static cost2236 exceeded1000; a validated smaller-page revision succeeded. No quota depletion, authentication or field-permission failure. Eight narrow schema type reads supported the query. All eight source checks pass; no shipping, market, feed, billing or other external write. Root owns Merchant/browser integration and reported Verified/Claimed domain evidence; this lane did not reverify Google.

Continue using the existing account setup and these exact source facts; no new shipping system or storefront change is needed for this readback.
