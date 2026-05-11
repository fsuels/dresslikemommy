# Measurement / Conversion Gap Report (Lane B)

Generated: 2026-05-10
Lane: `measurement-conversion-gap`
Parent packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/`
Anchor it answers to: `2026-05-10-paid-growth-orchestrator-safe-resume`

## Scope and constraints

- Cowork session, no browser access. No Google Ads, GA4, Merchant, Pinterest, Shopify Admin, or theme writes were made.
- This lane is read-only against the repo. Every claim about theme/repo state below is backed by a bash grep command and a `file:line` cite. Anything that would require browser access to verify is explicitly tagged `unknown without browser access`.
- This lane only catalogs current state for Lane C (`pinterest-event-quality-fix-plan`) and Lane D (`first-enable-runbook`). It does not propose theme edits or live writes.

---

## 1. Cross-market conversion goal risk (`Account-default: Purchases`)

### Inheritance chain (from repo evidence)

`grep -n "Conversion goal\|Account-default" /sessions/amazing-determined-turing/mnt/dresslikemommy/ops/GOOGLE_ADS_CONTINUITY.md`

- `ops/GOOGLE_ADS_CONTINUITY.md:223` Standard Shopping `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` `23802638621` uses `Conversion goals: Account-default`.
- `ops/GOOGLE_ADS_CONTINUITY.md:224` The single Primary purchase action verified at the account level is `Google Shopping App Purchase`, with `Purchases, Primary action`, dynamic value enabled, enhanced conversions enabled.
- `ops/GOOGLE_ADS_CONTINUITY.md:284` Brand Search `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` uses `Conversion goal: Account-default Purchases`.
- `ops/AGENT_WORKLOG.md:11900` durable rule: keep `Google Shopping App Purchase` as the only Primary / account-level goal conversion in Google Ads.
- `ops/AGENT_WORKLOG.md:25928` "exactly one primary account-level purchase action, `Google Shopping App Purchase`".
- `ops/AGENT_WORKLOG.md:26263` value setting `Use different values. If there's no value, use 0.`; raw historical conversions/value `5.0` / `193.9`.
- The 9 paused non-US Search campaigns (`GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`) were created under the canonical TEST BUILD approval which forbade conversion-goal changes; they therefore inherit `Account-default: Purchases`, which currently resolves to the same single Primary `Google Shopping App Purchase` action.

So the inheritance chain is: campaign -> `Account-default` conversion goal at account level -> single Primary purchase action `Google Shopping App Purchase` -> Shopify-side Google & YouTube app firing `purchase` from any market on `/checkout/thank_you`.

### Behavior of `Google Shopping App Purchase` for non-US traffic

- The `Google Shopping App Purchase` action is configured at the Google Ads account level, not at the campaign level. Google Ads attributes a conversion to a campaign when there is a click ID match on a click that came from that campaign in its lookback window, regardless of the country of the buyer.
- This means: if a non-US Search campaign drives a non-US visitor who later completes a Shopify purchase on the storefront, and the Shopify Google & YouTube app pixel fires `purchase` with the matching `gclid`, Google Ads will count that conversion against the non-US campaign. Currency handling is covered separately in section 4.
- Conversion counting itself is therefore not blocked for non-US Search campaigns. The risks are: (a) value/currency reporting fidelity and (b) the conversion action not being country-segmented, so non-US conversions and US conversions land in the same bucket and can be hard to compare on equal footing.
- `unknown without browser access`: whether `Google Shopping App Purchase` has any country-restricted "Include in Conversions" or geo filter applied at the action level. The repo evidence does not record any such filter, but the only authoritative read is in Google Ads UI, Tools and settings -> Conversions -> `Google Shopping App Purchase` -> Settings.

### Risk if a non-US campaign drives a non-US purchase

- Counted-but-mis-currencied risk: if the Google & YouTube app or Google Tag converts the storefront-presented currency to USD silently, the non-US campaign will book a USD-stamped value while the customer paid in EUR/SEK/CHF/RON/etc. ROAS comparisons across markets become apples-to-oranges, and the `650%` ROAS North-Star math (`ops/GROWTH_NORTH_STAR.md` line "Maintain or move toward about `650% ROAS`") becomes unreliable per market.
- Cross-attribution risk: if the same buyer interacts with both US Standard Shopping and a non-US Search campaign (for example a UK shopper who clicked a US Brand Search ad on a US-IP VPN and later bought from GB), the single Primary action will attribute on Google Ads' default rules without any visible market segmentation. Today this risk is small because non-US Search is paused and Standard Shopping is presence-only US, but it grows the moment any non-US Search campaign is enabled.
- No-conversion-counted risk (least likely): only if the account-level action has a hidden geo restriction that this Cowork session cannot read. This must be verified before enable.

### What the operator must verify in Google Ads UI before any non-US enable

1. Tools and settings -> Conversions -> Conversion actions -> open `Google Shopping App Purchase`. Confirm: Source app/web, Category `Purchase`, Counting `One/Every` per current spec, Value `Use different values. If there's no value, use 0.`, Click-through window, Attribution model, Include in `Conversions` `Yes`, and any geo/locale filter is `none` (or equivalent "no restriction").
2. Same screen, Activity tab. Filter Activity by Country and confirm whether non-US purchases have already arrived in this action historically. If yes, currency value distribution gives a clue about whether the upstream pixel sends presentment or USD.
3. In each non-US Search campaign, Settings -> Goals -> confirm `Account-default` resolves to a list that contains exactly the single Primary `Google Shopping App Purchase` and not stale GA4-imported purchase actions. If any duplicate purchase action is Primary at account level, a non-US enable will inflate counts.
4. Google Ads -> Conversions overview, segment by Country, last 30 days. Confirm whether non-US Country rows already have any non-zero conversions/value before non-US Search is even enabled. This baselines what Standard Shopping or organic referral has already driven.
5. Reports -> Predefined -> Conversions, segmented by Conversion action and Country, to confirm there is no surprise non-US attribution from Standard Shopping (which is presence-only US).

### Owner-approval phrase needed to add a separate non-US conversion goal (if that ends up being the right move)

Do not run this in this session. Do not run this until at least the verification list above has been read back and the owner has been briefed. The exact phrase the operator should request from the owner before any non-US-specific conversion-goal change is:

`APPROVE NON-US CONVERSION-GOAL SEGMENTATION FOR PAUSED NON-US SEARCH CAMPAIGNS ONLY: CREATE A NEW CONVERSION ACTION SCOPED TO NON-US PURCHASES (CATEGORY=PURCHASE, VALUE=DYNAMIC PRESENTMENT-CURRENCY, ATTRIBUTION=ACCOUNT-DEFAULT, INCLUDE IN CONVERSIONS=YES) AND APPLY IT AS A CAMPAIGN-LEVEL CONVERSION GOAL TO GB/CA/AU/CH/DK/DE/NL/SE/ES PAUSED SEARCH CAMPAIGNS ONLY; KEEP DLM_US_STANDARD_SHOPPING_TEST_PAID_READY AND DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429 ON ACCOUNT-DEFAULT WITH GOOGLE SHOPPING APP PURCHASE UNCHANGED; NO CAMPAIGN ENABLE, NO BUDGET, NO BID, NO PRODUCT-SCOPE, NO FEED-LABEL, NO PRODUCT-GROUP, NO MERCHANT, NO PINTEREST, NO SHOPIFY, NO THEME, AND NO PURCHASE-PIXEL CHANGES; READ BACK BEFORE AND AFTER.`

The simpler safer alternative, which Lane D's runbook should default to first, is to leave the conversion goal alone and only segment by Country in reports/optimization scores. That requires no owner approval and no live Ads write.

---

## 2. GA4 / Google Tag readbacks needed before any non-US enable

The following are read-only, no-write checks. They cannot be done in this Cowork session because there is no logged-in browser. They are written here so the next browser-enabled session executes them in this exact order.

### GA4 Realtime (Reports -> Realtime)

1. With no filter: confirm `purchase` events appear at all when test orders happen. Confirm `currency` parameter is populated and not `(not set)`.
2. Add a comparison filter: Country `exactly matches` `Italy`. Walk a synthetic IT add-to-cart-to-shipping flow on a test/staging context (do NOT submit payment). Confirm `view_item`, `add_to_cart`, `view_cart`, `begin_checkout` all fire and that `currency` reports `EUR` (not `USD`). Repeat for `Spain` (`EUR`), `Romania` (`RON`), `Sweden` (`SEK`), `Switzerland` (`CHF`), `Denmark` (`DKK`), `Germany` (`EUR`), `Netherlands` (`EUR`), `United Kingdom` (`GBP`), `Canada` (`CAD`), `Australia` (`AUD`), `Poland` (`PLN`), `Czechia` (`CZK`), `Greece` (`EUR`), `Portugal` (`EUR`), `France` (`EUR`), `Belgium` (`EUR`).
3. After a known real (non-paid, organic) purchase from a non-US country, return to Realtime and confirm `purchase` fires with the buyer's presentment currency. Capture screenshot and `event` parameter detail (event count, value, currency, transaction_id, items array).

### GA4 Acquisition / Monetization

4. Reports -> Life cycle -> Monetization -> Ecommerce purchases. Add a Country dimension and segment value by Country for the last 30 days. Verify `Total revenue` per Country sums match Shopify Admin Orders revenue per Country within rounding tolerance. Currency unit must be visible (top-right `Reporting identity` and `Currency` settings). If GA4 has been left on a single-currency property, this is the place where USD bleed will show first.
5. Reports -> Life cycle -> Acquisition -> Traffic acquisition. Filter by `Session source / medium` `google / cpc`, segment by Country. Confirm `Total revenue` and `Conversions` per Country are not concentrated only in `United States`.
6. Admin -> Property settings -> Currency. Record the property's reporting currency. If it is `USD`, every non-USD `purchase` event will be FX-converted by GA4 using the daily Google rate. That is acceptable for GA4 reporting but must be reconciled separately when comparing to Google Ads.

### Google Tag Assistant / Tag Assistant Companion

7. Open `https://tagassistant.google.com/` and start a new tag preview against `https://www.dresslikemommy.com/`. Confirm a `Google Tag (gtag.js)` is detected, sourced from the Google & YouTube Shopify app (not a duplicate from theme).
8. Walk through `/products/<paid-eligible product>?country=GB` (and IT, ES, RO, AU). After each `add to cart` and `view cart` step, inspect Tag Assistant's event log. Confirm `currency` parameter on `view_item`, `add_to_cart`, `view_cart`, and `begin_checkout` matches the storefront-displayed currency.
9. Tag Assistant -> Tags -> `purchase` event detail (only on a real test purchase): confirm one `Google Tag` purchase fire and one `Google Ads conversion` purchase fire share the same `transaction_id`. Confirm there is no duplicate `purchase` request to `googleadservices.com/pagead/conversion/853411529/` (single-fire). The 2026-04-30 paid-value gate evidence (`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md` lines 13, 24, 30) shows the USD case passed cleanly; non-US must pass equivalently.

### Google Ads UI (Tools -> Conversions)

10. Open `Google Shopping App Purchase`. Confirm `Last received` timestamp is recent. Confirm `Status` is `Recording conversions`. Confirm any `Diagnostics` warnings about currency-mismatch or stale value are absent.
11. Tools -> Conversions -> Diagnostics. Filter by conversion action `Google Shopping App Purchase`. Confirm `Tag status` `Active and recording` and that there is no message about currency code mismatch.

### Search Console (only if Search campaigns will be enabled)

12. `https://search.google.com/search-console/` -> property `https://www.dresslikemommy.com/`. Performance -> Filter Country `Italy` (and ES/RO/SE/CH/DK/DE/NL/GB/CA/AU/PT/PL/CZ/GR/FR/BE). Confirm clicks/impressions are non-zero so paid Search has organic baseline coverage. Compare Top queries to the `88` keyword block in each non-US split CSV to spot obvious mismatches.
13. URL Inspection on `/products/<paid-candidate handle>` for one non-US locale (`/es/products/...`). Confirm `Page is on Google` and `Crawled as: Smartphone` so a non-US ad does not land on a noindex/blocked page.

### Currency-presentment baseline (already partly done)

14. Re-read `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/PAID_GROWTH_CURRENCY_PRESENTMENT_READBACK_REPORT.md` lines 27-32: ES/IT cart EUR, RO cart RON, PT cart EUR. The presentment-side currency story is documented at the storefront layer; the GA4/Google Ads pixel side has NOT yet been read back per market. That is the gap this readback list closes.

---

## 3. Pinterest Event Quality Fair handoff to Lane C

This section is a state catalog for Lane C (`pinterest-event-quality-fix-plan`) only. It does NOT propose theme edits.

### Where Pinterest events fire today

- The theme contains zero Pinterest tag/CAPI code. Confirmed by:
  - `grep -rln "pintrk\|epik\|/v3/conversions\|click_id" /sessions/amazing-determined-turing/mnt/dresslikemommy/{assets,snippets,layout,sections,templates}` returned no client-tracking matches. The only Pinterest-named hits in `assets/snippets/sections` are the social-share/icon links: `snippets/icon-pinterest.liquid:1`, `snippets/header-drawer.liquid:285-289`, `snippets/jsonld-seo.liquid:13,32`, `snippets/social-icons.liquid:53-57`, `sections/main-password-footer.liquid:21-25`, `sections/footer.liquid:14`, `sections/announcement-bar.liquid:6`, `sections/header.liquid:247`, `snippets/product-schema-extra.liquid:61`. None of these emit a `pintrk` call or write to Pinterest CAPI; they are all visible UI/JSON-LD references.
  - The deprecated custom-pixel file `ops/customer-events/ga4-checkout-ecommerce-pixel.js:1-9` confirms the policy: "Do not deploy Google measurement through Shopify custom pixels from this repo. The supported path for dresslikemommy.com is the Shopify Google & YouTube app." This same posture holds for Pinterest per `ops/AGENT_COORDINATION.md:75` "Do not add duplicate theme-level Pinterest tag, do not add custom CAPI/token code".

### Pinterest tag/CAPI integration today

- Source of truth is the official Pinterest Shopify app, configured in Shopify Admin -> Settings -> Customer events. Captured in `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-pinterest-event-quality-fix/PINTEREST_EVENT_QUALITY_FIX_RECHECK.md` lines 105-117: Pinterest app pixel ID `22577249`, app ID `3009811`, tag config `tagID:2620007050621`. After the 2026-05-06 owner-approved fix, the app pixel is set to `Always on` / `share all events` per `ops/PROBLEM_TRACKER.md:801` and `ops/AGENT_COORDINATION.md:75`.
- After that fix, the `2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md:58-66` readback still showed Event Quality `Fair` overall, with Pinterest Tag latest `2026-05-08T05:50:56.502Z`, Conversions API latest `2026-05-08T05:51:13.760Z`, Verified Merchant Program `PASS`, Automatic Enhanced Match `PASS`, Enhanced Match `ERROR`.
- The three remaining action items reported by Pinterest (`PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md:74-77`) are:
  1. `product_id__ADD_PAYMENT_INFO` missing
  2. `hashed_email__ADD_TO_CART` missing
  3. `click_id_epik__CHECKOUT` missing

### Theme dataLayer state Lane C should know

These are the theme-side ingredients Pinterest's official app may or may not be reading off the dataLayer. They are NOT Pinterest events themselves. Lane C must assume Pinterest's official app sources its events from Shopify Customer Events / checkout extension, not the theme dataLayer. Lane C should still note these for any cross-verification:

- `assets/analytics.js:1` initializes `window.dataLayer`.
- `assets/analytics.js:126-139` `getCurrency()` reads from `meta[property="og:price:currency"]` first, then `Shopify.currency.active`, then defaults `'USD'`.
- `assets/analytics.js:382-406` `buildBaseItem()` assembles the GA4 ecommerce item: `item_id` (resolves to product or variant ID at `assets/analytics.js:387`), `item_name`, `item_brand`, `price`, `currency`, plus taxonomy fields. There is NO `email`, NO `epik`/`click_id`, NO `event_id`.
- `assets/analytics.js:408-435` `buildEcommerceItem()` resolves variant.
- `assets/analytics.js:447-468` `buildEcommercePayload()` returns `{ currency, items, value }`. No `event_id`, no `transaction_id`.
- `assets/analytics.js:912-934` `pushViewCartEvent` fires `view_cart`. Includes `cart_context` plus `getShippingCountryCheckerSessionContext()` (`assets/analytics.js:202-205`), no email, no Pinterest IDs.
- `assets/analytics.js:936-959` `pushBeginCheckoutEvent` fires `begin_checkout`. Includes `checkout_source`. Same omissions.
- `assets/analytics.js:962-970` `pushViewItemOnce` fires `view_item`.
- `assets/analytics.js:972-985` `pushAddToCartEvent` fires `add_to_cart`.
- `assets/analytics.js` does NOT contain a `purchase` event push. Confirmed by `grep -n "purchase\b" /sessions/amazing-determined-turing/mnt/dresslikemommy/assets/analytics.js` returning no JS-side hits. Purchase fires only from Shopify's checkout extension via the official Google & YouTube app and the official Pinterest app.
- Shipping-country-checker dataLayer pushes are in `snippets/shipping-country-checker-modal.liquid:144-153,196-201,206-211,250-253,272-275`. Events: `shipping_country_checker_open`, `shipping_country_checker_search`, `shipping_country_checker_no_results`, `shipping_country_checker_close`. Useful as paid-funnel diagnostic but unrelated to Pinterest event quality.
- `layout/theme.liquid:301-308` initializes `window.dataLayer`, sets `dlmAnalyticsContext.site_language`, and pushes one `{ site_language }` row. Then `layout/theme.liquid:319-340` lazily injects `assets/analytics.js`.

### What Lane C now has to work with

- `product_id__ADD_PAYMENT_INFO`: theme has nothing to do with `add_payment_info`. That event is fired by Shopify's checkout extension, not the theme. The fix has to come from the official Pinterest app's Shopify Customer Events configuration or from a Shopify checkout extension setting that maps the cart's product IDs into the AddPaymentInfo Pinterest event. There is no theme-side hook to add. Confirmed: `grep -rn "add_payment_info\|AddPaymentInfo" /sessions/amazing-determined-turing/mnt/dresslikemommy/{assets,snippets,layout,sections,templates}` returns no matches.
- `hashed_email__ADD_TO_CART`: the theme `add_to_cart` event in `assets/analytics.js:984` does not include any email. Even if it did, the theme dataLayer is not what the Pinterest app reads. The Pinterest app reads Shopify Customer Events. The relevant gap is whether the storefront supplies an email at the moment AddToCart fires, which is mostly a logged-in vs guest issue. Email is generally not present pre-checkout. The realistic Lane C plan is documented Enhanced Match (Automatic) reliance and acceptance that pre-checkout AddToCart often will not have hashed_email.
- `click_id_epik__CHECKOUT`: per `2026-05-06-pinterest-event-quality-fix/PINTEREST_EVENT_QUALITY_FIX_RECHECK.md:24,82-83,298`, the `_epik` cookie is generated from real Pinterest ad clicks, and the account currently has zero campaigns serving. So the `click_id_epik__CHECKOUT` gap will only close once real paid Pinterest traffic is flowing. It cannot be repaired theme-side or via more app config. It is a chicken-and-egg gap: the metric improves only after the operator runs a small approved paused-draft -> enabled campaign and gets real ad clicks.

### Hand-off summary for Lane C (no theme edits proposed)

Lane C should write the fix plan against:

- The Shopify Customer Events Pinterest app pixel (already `Always on` / `share all events`).
- The Shopify Pinterest channel/app catalog and Enhanced Match settings (Automatic is `PASS`, Enhanced Match is `ERROR` per `PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md:67-68`).
- The Pinterest Ads platform side: a tiny paused -> enabled retargeting smoke test under approved scope to generate `_epik` traffic.
- The theme stays untouched. Adding `pintrk` to the theme would create a duplicate-event/dedupe risk against the official app and is explicitly forbidden by `ops/AGENT_COORDINATION.md:75` and the 2026-05-06 owner approval phrase in `PINTEREST_EVENT_QUALITY_FIX_RECHECK.md:147-149`.

---

## 4. Currency presentment risk for non-US revenue attribution

### What the theme dataLayer does

- `assets/analytics.js:126-139` `getCurrency()`:
  1. Read `<meta property="og:price:currency">` content if present.
  2. Else read `window.Shopify.currency.active` if present.
  3. Else default to `'USD'`.
- `assets/analytics.js:392` `buildBaseItem` sets each item's `currency: getCurrency()`.
- `assets/analytics.js:462` `buildEcommercePayload` sets the event-level `currency: getCurrency()`.
- `assets/analytics.js:820` cart-snapshot items also set `currency: getCurrency()`.
- Therefore the theme dataLayer carries the user's PRESENTMENT currency for `view_item`, `add_to_cart`, `view_cart`, `begin_checkout`, `select_item`, and `view_item_list`. It is NOT USD-converted theme-side. The default `'USD'` only triggers if both the OG meta and `window.Shopify.currency.active` are missing, which would itself be a separate breakage to investigate.
- Storefront browser evidence confirms presentment is correct for ES (EUR), IT (EUR), RO (RON), and PT (EUR cart): `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/PAID_GROWTH_CURRENCY_PRESENTMENT_READBACK_REPORT.md:27-32`. Non-US Search target markets GB/CA/AU/CH/DK/DE/NL/SE/FR/BE/PL/CZ/GR also have storefront presentment captures in the worklog (`ops/AGENT_WORKLOG.md:32094, 32289, 32510, 32593` etc.), each in their own currency code.

### What the theme dataLayer does NOT do (and the resulting risk)

- The theme has no `purchase` event. `grep -n "purchase\b" /sessions/amazing-determined-turing/mnt/dresslikemommy/assets/analytics.js` returns no hits. `grep -rn "thank_you\|order_complete\|order.id\|checkout_completed" /sessions/amazing-determined-turing/mnt/dresslikemommy/{assets,snippets,layout,sections,templates}` returns nothing. Purchase events come exclusively from the official Shopify Google & YouTube app and the official Pinterest app pixel, which run as Shopify Customer Events / Web Pixels Manager subscribers.
- Therefore the currency stamped on the `purchase` request to `googleadservices.com/pagead/conversion/853411529/` and to `G-N4EQNK0MMB` is determined by the Google & YouTube app, not by the theme dataLayer. The 2026-04-30 paid-value gate (`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md:13,24,30`) only proved this for a US/USD order. Non-US currency behavior of the official app's purchase request is `unknown without browser access`.
- Plausible behaviors (must be verified by the Google Tag Assistant readback in section 2 step 9):
  1. Google & YouTube app sends `currency=<presentment>` (best case). Then Google Ads receives e.g. `EUR 24.95` and applies its own FX to USD for unified reporting. ROAS comparisons need either reporting currency consistency or per-market reports.
  2. Google & YouTube app sends `currency=USD` with a converted value (FX done on the storefront/app side before send). Then Google Ads receives e.g. `27.32 USD` for a EUR order; ROAS appears clean inside Ads but is opaque vs Shopify's revenue-in-presentment.
  3. Google & YouTube app sends `currency=<shop primary>` (always USD on this store) with the presentment-currency numeric value (worst case). Google Ads then books `24.95 USD` for a `24.95 EUR` order, materially under-reporting non-USD ROAS.
- Same uncertainty applies to GA4. GA4's reporting currency is set in Admin -> Property settings; the property may be `USD`, in which case GA4 internally FX-converts the `value` parameter from each event using the daily Google rate. That is acceptable internally to GA4 if and only if the `purchase` event arrives with the correct presentment `currency` parameter.

### Concrete confirmation/refutation

- CONFIRMED: theme dataLayer carries presentment currency for non-purchase ecommerce events. Files and lines: `assets/analytics.js:126-139`, `:392`, `:462`, `:820`.
- REFUTED: there is NO theme-side `purchase` push, so the theme dataLayer cannot be cited for the purchase-currency question.
- UNKNOWN WITHOUT BROWSER: the actual `currency` parameter on the live Google Ads conversion request and the GA4 `purchase` event fired from the Google & YouTube Shopify app for a non-US order. This is the gap the section-2 readback list closes.

---

## 5. Tag / CAPI dedupe (`event_id`)

### Theme search

- `grep -rln "event_id\|eventID" /sessions/amazing-determined-turing/mnt/dresslikemommy/{assets,snippets,layout,sections,templates}` returned only false positives: the matches in `assets/section-main-product.css`, `assets/component-pickup-availability.css`, `assets/base.css`, `assets/theme-inline-body-static-03.css` are CSS not JS. The matches in `snippets/country-localization.liquid:61`, `snippets/language-localization.liquid:34`, `snippets/header-search.liquid:68`, `snippets/visible-header-search.liquid:34`, `snippets/shipping-country-checker-modal.liquid:60`, `sections/main-addresses.liquid:144`, `:309` are the HTML attribute `autocapitalize`. None of these is a Pinterest dedupe `event_id`.
- `grep -n "event_id\|order_id\|transaction_id" /sessions/amazing-determined-turing/mnt/dresslikemommy/assets/analytics.js` returned no matches. The theme does not stamp any Pinterest dedupe `event_id` on its dataLayer events.
- This is correct given the integration model: the theme is not authoring Pinterest tag or CAPI calls. The official Pinterest Shopify app authors both, and Pinterest Conversions API documentation (cited in `2026-05-06-pinterest-event-quality-fix/PINTEREST_EVENT_QUALITY_FIX_RECHECK.md:24`) says the app must send a matching `event_id` on the tag and the CAPI request to deduplicate the pair. The expectation is that the official app does this internally; it is not a theme responsibility.

### Current observable state

- `2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md:62-63`: Pinterest Tag latest `2026-05-08T05:50:56.502Z`, Conversions API latest `2026-05-08T05:51:13.760Z`. The 17.258 second gap between the two for similar event types is consistent with a tag fire from the browser plus a server-side CAPI fire that batches and forwards. This pattern is exactly what Pinterest's app-level dedupe via shared `event_id` is designed to handle. Whether the dedupe is actually working at the Pinterest backend is `unknown without browser access` and would require Pinterest Ads Manager -> Events Manager -> Event Quality -> the per-event detail panel showing `Deduplicated: Yes`.

### Conclusion for Lane C and Lane D

- Theme has no dedupe IDs to manage; this is correct. Do not add a custom `event_id` in the theme. Doing so would create a parallel non-deduped pair against the official app.
- Verification of Pinterest tag/CAPI dedupe must be done in Pinterest Ads Manager -> Conversions -> Events Quality. If `Deduplicated` is `No` for shared `event_name`, escalate to the official Pinterest Shopify app support, not theme code.

---

## 6. Recommended pre-enable measurement gate

This checklist is written in the same gate format as Lane D's first-enable runbook so they integrate cleanly. It is the MEASUREMENT-side gate only. Lane D adds the budget/economics/spend gate.

### Pre-enable measurement gate (must pass for any non-US Search campaign)

`MEASUREMENT_GATE_FOR_NON_US_SEARCH_ENABLE` items:

- `M1` Conversion goal verification. In Google Ads -> Tools -> Conversions -> `Google Shopping App Purchase`: Status `Recording conversions`, Last received within 7 days, Value setting `Use different values. If there's no value, use 0.`, Include in Conversions `Yes`, no geo restriction. Evidence: screenshot capture filed under the next packet's `lanes/<lane>/raw/conversion_action_settings.png`.
- `M2` Account-default goal scope. In each non-US Search campaign Settings -> Goals: confirm `Account-default` resolves to exactly the single Primary `Google Shopping App Purchase`. No stale GA4-imported purchase actions are Primary. Evidence: per-campaign settings screenshot.
- `M3` GA4 Realtime non-US verification. With a synthetic IT/ES/CH/DK/DE/NL/SE/PT/PL/CZ/GR/FR/BE/RO and live GB/CA/AU walk through `view_item` -> `add_to_cart` -> `view_cart` -> `begin_checkout`, with NO payment. Each event must show in Realtime with `currency` matching the storefront presentment. Evidence: Realtime panel screenshot per market filtered by Country.
- `M4` Tag Assistant non-US verification. Same per-market walks above with Tag Assistant attached. Confirm `currency` parameter on each event matches presentment.
- `M5` Real-purchase currency proof. After the next genuine non-US organic purchase (or one approved synthetic test order), capture the `purchase` request in DevTools Network or Tag Assistant and confirm `currency=<presentment>` and `value=<presentment-amount>`. If `currency=USD` with a non-US presentment value, STOP, do not enable any non-US Search campaign, and request the owner-approval phrase in section 1 to add a per-currency conversion goal or to fix the upstream pixel.
- `M6` GA4 reporting-currency awareness. Record GA4 property reporting currency. If the property is USD and the `purchase` event arrives with presentment currency, this is acceptable; document the FX-conversion expectation. If the property is USD and the `purchase` event also arrives in USD with a converted value, document this as `lossy reporting` and treat per-market ROAS in Google Ads only.
- `M7` Search Console baseline. Each non-US Country has non-zero impressions/clicks for the last 28 days on at least one product or collection URL.
- `M8` Pinterest dedupe baseline (only if a Pinterest paused-draft will be enabled in parallel). In Pinterest Ads Manager -> Conversions -> Event Quality, confirm `Deduplicated=Yes` for the most-recent `add_to_cart` and `checkout` event pair. If `Deduplicated=No`, do NOT enable Pinterest spend even if approved.
- `M9` Standard Shopping no-cross-attribution check. Google Ads -> Reports -> Conversions, segmented by Country and by Campaign. Confirm `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` (`23802638621`) shows 0 conversions for non-US countries before any non-US Search is enabled. If non-US conversions are already attributed to US Standard Shopping, the conversion goal is leaking and must be fixed before any non-US enable.
- `M10` Beach-SEO bad-handle exclusion still in force. The held `1496`-row CSV exclusion (`PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`) must still exclude `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` for the enable-target country.
- `M11` Pinterest event-quality posture acknowledged. If Event Quality is still `Fair` at enable-time and the operator chooses to enable Pinterest spend anyway, an explicit owner approval phrase must reference the `Fair` status. Default for this gate is: do not enable Pinterest spend with Event Quality `Fair`. Lane C owns the fix-plan side.

`PASS` requires all of `M1`-`M7` and `M9`-`M10` for a Search-only enable; `M8` and `M11` are required only if Pinterest spend is being enabled in the same window.

### Integration note for Lane D (`first-enable-runbook`)

- Lane D's runbook should call this measurement gate BEFORE any `first enable click`. The order is:
  1. Lane D budget/economics gate (Lane D's responsibility, references `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md`).
  2. THIS measurement gate `M1`-`M11`.
  3. Just-in-time Ads readback for the specific campaign (paused, presence-only, content/YouTube off, approved budget).
  4. Owner approval phrase for that one specific country enable.
  5. The single enable click.
  6. Post-enable readback (campaign Eligible, no policy disapprovals, conversion tracking still recording).

---

## File and line citations summary (for audit)

Theme side, all confirmed via `grep` from the repo root `/sessions/amazing-determined-turing/mnt/dresslikemommy/`:

- Theme dataLayer init: `layout/theme.liquid:301-308`, lazy analytics loader: `layout/theme.liquid:319-340`.
- Theme analytics module: `assets/analytics.js:1`, `:99-103`, `:111-119`, `:122-123`.
- Currency resolver (presentment-aware): `assets/analytics.js:126-139`.
- Item builder with currency: `assets/analytics.js:382-406`, `:408-435`, `:447-468`.
- Cart-snapshot item with currency: `assets/analytics.js:810-822`.
- `view_cart`: `assets/analytics.js:912-934`.
- `begin_checkout`: `assets/analytics.js:936-959`.
- `view_item`: `assets/analytics.js:962-970`.
- `add_to_cart`: `assets/analytics.js:972-985`.
- No purchase event: `grep -n "purchase\b" assets/analytics.js` returns zero.
- No Pinterest tag/CAPI/dedupe code: `grep -rn "pintrk\|epik\|/v3/conversions\|click_id\|event_id" {assets,snippets,layout,sections,templates}` returns zero meaningful matches.
- Deprecated custom-pixel banner forbidding theme measurement: `ops/customer-events/ga4-checkout-ecommerce-pixel.js:1-9`.
- Shipping-country-checker dataLayer events: `snippets/shipping-country-checker-modal.liquid:144-153,196-211,250-275`.
- Shipping-country-checker session context surfaced into events: `assets/analytics.js:202-205`.

Conversion / measurement memory side:

- Account-default conversion goal usage: `ops/GOOGLE_ADS_CONTINUITY.md:223-224`, `:284-289`, `:294`.
- Single Primary purchase action: `ops/AGENT_WORKLOG.md:11892-11900`, `:25928`, `:26263`, `:27358`, `:27460`.
- 2026-04-30 paid-value gate USD proof: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md:13,24,30`.
- 2026-05-07 currency-presentment storefront proof for ES/IT/RO/PT: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/PAID_GROWTH_CURRENCY_PRESENTMENT_READBACK_REPORT.md:27-32`.
- Pinterest official app pixel state and remaining gaps: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md:58-77`.
- Pinterest event-quality fix history and approval phrase: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-pinterest-event-quality-fix/PINTEREST_EVENT_QUALITY_FIX_RECHECK.md:24,82-83,105-117,147-149,253-298`.
- Forbidden-action rules used to constrain Lane C's plan: `ops/AGENT_COORDINATION.md:75`.

---

## Guardrails honored by this report

- No Google Ads, Merchant Center, Pinterest, GA4, Shopify Admin, or theme writes were made or proposed.
- No conversion goal, conversion action, attribution, or pixel change was made.
- No campaign enable, budget, bid, or status change was made or proposed.
- The only file written by this lane is this report file.
- Every claim about theme/repo state is grep-cited with `file:line`.
- Items requiring browser access are explicitly tagged `unknown without browser access`.
