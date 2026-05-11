# Historical Non-US Purchase Evidence Hunt

Generated: 2026-05-10

Lane: `measurement-browser-readback`

Problem: `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`

Mode: local-only evidence hunt. No browser, no checkout, no network, no payment/order/refund/cancel, and no external account writes.

## Decision

`GATE_CANNOT_CLOSE_FROM_EXISTING_EVIDENCE`

Existing repo evidence proves the official Shopify Google & YouTube app purchase path for US/USD orders only. It does not prove the app-fired `purchase` event currency/value for any non-US order.

The gate should remain open until one of these exists:

- a historical/genuine non-US `purchase` event capture showing transaction/order id, value, currency, Google Ads purchase request, paired GA4 purchase event, and no duplicate fire; or
- an owner-approved controlled non-US test purchase/refund/cancel capture.

## Scope Searched

Searched local-only evidence across:

- `ops/PROBLEM_TRACKER.md`
- `ops/AGENT_WORKLOG.md`
- `ops/GOOGLE_ADS_CONTINUITY.md`
- current May 10 measurement packets
- April 30 measurement-gate request-capture packets
- April 29 Shopify order/economics export packet
- Google Ads conversion setup/value gate packets
- measurement/capture scripts under `ops/scripts`
- relevant non-US checkout/currency packet reports and raw public HTML/request snapshots

## Key Commands Run

Context and active blocker readback:

```bash
sed -n '1,220p' ops/MEMORY_CONTINUITY_PROTOCOL.md
sed -n '1,260p' ops/PROBLEM_SOLVING_PROTOCOL.md
sed -n '1,220p' ops/AGENT_COORDINATION.md
sed -n '202,246p' ops/PROBLEM_TRACKER.md
sed -n '150,198p' ops/GOOGLE_ADS_CONTINUITY.md
sed -n '33440,33724p' ops/AGENT_WORKLOG.md
sed -n '27336,27572p' ops/AGENT_WORKLOG.md
```

Measurement/problem search:

```bash
rg -n "PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT|purchase event currency|purchase.*currency|currency/value|Tag Assistant|DebugView|GA4|Google Ads conversion|conversion activity|Shopify order|non-US purchase|non US purchase|test purchase|purchase proof" ops/PROBLEM_TRACKER.md ops/AGENT_WORKLOG.md ops/GOOGLE_ADS_CONTINUITY.md
find dresslikemommy-growth-2026/02_AUDIT_PACKETS -maxdepth 3 -type f | rg -n "(MEASUREMENT|measurement|GA4|ga4|TAG|tag|DEBUG|debug|PURCHASE|purchase|CONVERSION|conversion|CHECKOUT|checkout|ORDER|order|ADS|ads|readback|REPORT|report)"
rg -n "purchase[^\n]*(GBP|CAD|AUD|EUR|RON|PLN|CZK|SEK|CHF|DKK)|(?:GBP|CAD|AUD|EUR|RON|PLN|CZK|SEK|CHF|DKK)[^\n]*purchase|transaction_id[^\n]*(GBP|CAD|AUD|EUR|RON|PLN|CZK|SEK|CHF|DKK)|(?:GBP|CAD|AUD|EUR|RON|PLN|CZK|SEK|CHF|DKK)[^\n]*transaction_id" dresslikemommy-growth-2026 ops assets layout snippets sections templates
rg -n "Tag Assistant|DebugView|Realtime|g/collect|googleadservices|pagead/conversion|Google Shopping App Purchase|conversion action|purchase value|purchase currency|currency_code=|currency=|transaction_id|oid=" dresslikemommy-growth-2026/02_AUDIT_PACKETS ops/scripts ops/customer-events
```

Direct packet reads:

```bash
sed -n '1,260p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md
sed -n '1,240p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/LIVE_PAID_CHECKOUT_CAPTURE_REPORT.md
sed -n '1,90p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/final_paid_value_measurement_gate_summary.json
sed -n '1,130p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/raw/shopify_order_9476_admin_sanitized.json
sed -n '1,120p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-discount-checkout-capture/FINAL_MEASUREMENT_GATE_PASS_REPORT.md
sed -n '1,120p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-capture/PAID_ORDER_MEASUREMENT_CHECK_REPORT.md
sed -n '1,90p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-standard-checkout-capture/CONTROLLED_CHECKOUT_CAPTURE_REPORT.md
sed -n '1,220p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-ads-conversion-value-gate/google_ads_conversion_value_gate_report.md
sed -n '1,80p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-ads-conversion-value-gate/purchase_conversion_actions.csv
sed -n '1,160p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-google-ads-conversion-setup-review/CONVERSION_SETUP_REVIEW.md
```

Current non-US measurement-gate reads:

```bash
sed -n '1,260p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/measurement-conversion-gap/MEASUREMENT_CONVERSION_GAP_REPORT.md
sed -n '1,240p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/public-measurement-preflight/PURCHASE_EVENT_CURRENCY_GATE_STATUS_UPDATE.md
sed -n '1,260p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/lanes/measurement-gate-recheck/PURCHASE_EVENT_CURRENCY_GATE_RECHECK.md
sed -n '1,260p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-goal-orchestrated-followup/lanes/measurement-preenable-gate/MEASUREMENT_PREENABLE_GATE.md
sed -n '1,220p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/public-measurement-preflight/PUBLIC_MEASUREMENT_PREFLIGHT_REPORT.md
```

Order/export and script checks:

```bash
awk -F, 'NR==1{for(i=1;i<=NF;i++) if($i=="currency") c=i; next} c {count[$c]++} END {for (k in count) print k, count[k]}' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-shopify-margin-cac-export-pack/orders_readonly_sanitized.csv
find ops/scripts -maxdepth 2 -type f | rg -n "(conversion|measure|ga4|tag|order|purchase|shopify|ads|capture|gate|debug)"
nl -ba ops/scripts/run_google_ads_paid_checkout_capture.py | sed -n '25,70p;220,285p;320,390p'
nl -ba ops/scripts/capture_existing_checkout_measurement.py | sed -n '1,45p;85,175p'
nl -ba ops/scripts/build_google_ads_conversion_value_gate_packet.py | sed -n '1,45p;300,335p;500,525p'
```

Non-US pre-purchase/currency packet checks:

```bash
sed -n '1,140p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/market-activation-priority/MARKET_ACTIVATION_PRIORITY_SCORECARD.md
sed -n '1,120p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/roas/country_budget_guardrails.csv
rg -n "target_country|Google Shopping App Purchase|Google & YouTube|purchase\"|currencyCode|currency" dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-de-nl-checkout-safe-advance/lanes/de-nl-landing-policy/raw/de_product.html | head -20
```

## Findings

### 1. Strong proof exists for US/USD purchase measurement

The April 30 paid-value gate packet is the strongest measurement evidence in the repo:

- Shopify order `#9476`, order id `6575644803169`, paid total `19.99 USD`.
- Google Ads purchase request:
  - endpoint `www.googleadservices.com/pagead/conversion/853411529/`
  - label `UbkpCN-fhogBEMmN-JYD`
  - event `purchase`
  - value `19.99`
  - currency `USD`
  - dedupe/order id `6575644803169`
- GA4 / Google measurement request:
  - measurement id `G-N4EQNK0MMB`
  - event `purchase`
  - value `19.99`
  - currency `USD`
  - transaction id `6575644803169`
- Duplicate check passed: reload did not produce a new distinct purchase order id.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/LIVE_PAID_CHECKOUT_CAPTURE_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/final_paid_value_measurement_gate_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/raw/shopify_order_9476_admin_sanitized.json`

This is US/USD proof only. It cannot answer whether a non-US order would send presentment currency, FX-converted USD, or a mismatched USD label with unconverted presentment numeric value.

### 2. Other April 30 purchase-related packets are also US/USD or incomplete

The 100% discounted controlled order packet proves the runtime field path existed for a discounted USD order:

- Shopify order/transaction id `6575594274913`
- Google Ads purchase event accepted
- value `0`
- currency `USD`
- GA4 value/currency `0` / `USD`
- no duplicate purchase on reload

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-discount-checkout-capture/FINAL_MEASUREMENT_GATE_PASS_REPORT.md`

Limit: discounted USD order; not nonzero paid revenue and not non-US.

The paid order `#9475` packet proves a Shopify paid order existed at `32.98 USD`, but no runtime Google Ads purchase request was captured:

- order `#9475`
- order id `6575609118817`
- paid total `32.98 USD`
- capture found page-view/scroll requests only and `0` paid `purchase` events

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-capture/PAID_ORDER_MEASUREMENT_CHECK_REPORT.md`

Limit: USD Shopify order only; not a purchase request proof packet and not non-US.

The earlier controlled checkout capture stopped at CAPTCHA:

- pre-purchase events showed USD values (`add_to_cart`, `begin_checkout`, `add_payment_info`)
- `purchase`: `0`
- no thank-you page
- no order

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-standard-checkout-capture/CONTROLLED_CHECKOUT_CAPTURE_REPORT.md`

Limit: no purchase event; USD-only pre-purchase evidence.

### 3. Shopify order export did not provide non-US currency evidence

The local sanitized Shopify order export checked here contains `89` rows, all with `currency=USD`.

Command result:

```text
USD 89
```

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-shopify-margin-cac-export-pack/orders_readonly_sanitized.csv`

Limit: this export does not prove any non-US Shopify order currency, and it does not include measurement request payloads.

### 4. Google Ads conversion-action history is aggregate, not non-US purchase proof

The April 29 Google Ads conversion-value gate shows:

- `Google Shopping App Purchase` is the primary account-level purchase action.
- Dynamic value is configured: `Use different values. If there's no value, use 0.`
- Raw historical conversions/value exist: `5.0` conversions / `193.9` value.
- The target action currency in the raw CSV is `XXX`, which is aggregate/unspecified in this packet, not evidence of a particular order currency.
- The visible date range had `0.0` purchase results.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-ads-conversion-value-gate/google_ads_conversion_value_gate_report.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-ads-conversion-value-gate/purchase_conversion_actions.csv`

Limit: no country, transaction id, order id, request currency, or non-US segmentation. This cannot prove non-US purchase event currency/value.

The May 6 conversion setup review confirms the desired configuration stayed intact:

- Shopify Google & YouTube app / app pixel is the supported Google measurement path.
- `Google Shopping App Purchase` remains the only primary account-level purchase action.
- Purchase remains dynamic/enhanced.
- The prior hard request proof cited there is still the same April 30 `#9476` USD order.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-google-ads-conversion-setup-review/CONVERSION_SETUP_REVIEW.md`

Limit: setup proof, not non-US purchase request proof.

### 5. Non-US storefront and checkout evidence supports pre-purchase currency only

Existing packets show non-US product/cart/checkout-to-shipping presentment across many markets:

- `GB`: GBP no-payment checkout evidence.
- `CA`: CAD no-payment checkout evidence.
- `AU`: AUD no-payment checkout evidence.
- `ES`, `IT`, `PT`: EUR product/cart/checkout evidence.
- `RO`: RON product/cart/checkout evidence.
- `PL`: PLN cart/shipping evidence.
- `CZ`: CZK cart/shipping evidence.
- `GR`: EUR cart/shipping evidence.
- `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`: currency/readiness packets describe pre-purchase presentment and remain approval-gated.

Evidence examples:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-safe-followup/lanes/localization-gb-ca-au/GB_CA_AU_CHECKOUT_READINESS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-se-pl-cz-gr-checkout-safe-advance/`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/market-activation-priority/MARKET_ACTIVATION_PRIORITY_SCORECARD.md`

Limit: these stop before purchase/payment. They are useful pre-purchase evidence, but they do not prove the app-fired checkout `purchase` payload.

### 6. Raw non-US storefront HTML shows non-US product/web-pixel context, but no purchase event

One raw DE product HTML snapshot contains:

- `og:price:currency` = `EUR`
- `Shopify.currency.active` = `EUR`
- Shopify Web Pixels Manager Google app config including purchase action labels for `G-N4EQNK0MMB`, `AW-853411529/UbkpCN-fhogBEMmN-JYD`, and `MC-MQ104D130Y`
- product variant data with `currencyCode: EUR`
- queued `product_viewed` event data with EUR currency

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-de-nl-checkout-safe-advance/lanes/de-nl-landing-policy/raw/de_product.html`

Important limitation:

- This is a product-page/web-pixel setup snapshot, not a thank-you/order-status purchase request.
- It does not show a non-US `purchase` event.
- The same Web Pixels config exposes `target_country:"US"`, which reinforces the need for a real non-US purchase readback rather than assuming product-page EUR context determines the purchase request currency.

### 7. Scripts can capture non-US evidence in principle, but no historical non-US capture exists

Relevant scripts:

- `ops/scripts/run_google_ads_paid_checkout_capture.py`
- `ops/scripts/capture_existing_checkout_measurement.py`
- `ops/scripts/build_google_ads_conversion_value_gate_packet.py`

What they show:

- The live checkout capture script sanitizes `value`, `currency`, `currency_code`, `transaction_id`, and `oid` from Google/GA/Merchant requests.
- The existing-checkout capture script attaches to already-open checkout/web-pixel targets and stores sanitized Google/GA/Merchant measurement requests without navigating, adding products, or submitting payment.
- The conversion-value gate script records Google Ads conversion setup and historical aggregate value evidence.

Important limitation:

- `run_google_ads_paid_checkout_capture.py` currently marks `nonzero_google_ads_purchase_proven` only when the captured Google Ads purchase has `currency == "USD"`. Raw request rows would still show a non-US currency if captured, but the helper's PASS boolean is US-focused.
- No existing packet found by this hunt contains a non-US raw purchase request produced by these scripts.

### 8. Current May 10 measurement packets all say the non-US gate remains open

The active problem tracker and May 10 lane reports repeatedly distinguish:

- proven: theme/storefront pre-purchase presentment;
- unproven: app-fired non-US `purchase` value/currency from checkout thank-you/order status.

Evidence:

- `ops/PROBLEM_TRACKER.md`, entry `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/measurement-conversion-gap/MEASUREMENT_CONVERSION_GAP_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/public-measurement-preflight/PURCHASE_EVENT_CURRENCY_GATE_STATUS_UPDATE.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/lanes/measurement-gate-recheck/PURCHASE_EVENT_CURRENCY_GATE_RECHECK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-goal-orchestrated-followup/lanes/measurement-preenable-gate/MEASUREMENT_PREENABLE_GATE.md`

These reports found no historical non-US purchase event evidence. This independent hunt did not find one either.

## Evidence Classification

| Evidence type | Found? | Currency/country | Can close non-US purchase gate? | Notes |
|---|---:|---|---:|---|
| Google Ads purchase request with value/currency/order id | Yes | `USD` / US order `#9476` | No | Strong US proof only. |
| GA4 paired purchase request with value/currency/order id | Yes | `USD` / US order `#9476` | No | Strong US proof only. |
| Shopify paid order evidence | Yes | `USD` only in checked order packets/export | No | Does not prove non-US or request payload. |
| Discounted purchase request proof | Yes | `0 USD` | No | Field-path proof only; not non-US. |
| Google Ads conversion action dynamic setup | Yes | aggregate / `XXX` for primary action | No | Setup evidence only, not order-level non-US currency. |
| Tag Assistant non-US purchase event note | No | none found | No | Only recipes/checklists found. |
| GA4 DebugView/Realtimes non-US purchase note | No | none found | No | Only recommended future path found. |
| Non-US pre-purchase storefront/cart/checkout currency | Yes | GBP/CAD/AUD/EUR/RON/PLN/CZK/SEK/CHF/DKK evidence in packets | No | Supports only pre-payment layers. |
| Raw non-US product page web-pixel setup | Yes | Example DE/EUR product context | No | Not a `purchase` event/request. |
| Capture scripts capable of preserving currency | Yes | capability only | No | No historical non-US purchase capture produced by scripts. |

## Gate Conclusion

The gate cannot close from existing evidence.

What is proven:

- US/USD app-fired purchase measurement worked for order `#9476`.
- Non-US storefront/cart/checkout-to-shipping presentment works before purchase for many target markets.
- Google Ads conversion setup is generally configured for dynamic purchase value.

What is not proven:

- actual non-US `purchase.currency`;
- actual non-US `purchase.value`;
- whether a non-US order sends presentment currency, FX-converted USD, or a bad USD/presentment mismatch;
- whether GA4 and Google Ads agree for a non-US order;
- whether a non-US order dedupes cleanly across Google Ads and GA4.

Therefore `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT` should remain `OWNER_APPROVAL_REQUIRED_FOR_PURCHASE_EVENT_PROOF` / open until the browser-enabled measurement readback or approved controlled test purchase supplies order-level non-US proof.

## Next Best Local/Operator Action

Run the browser-enabled readback already specified in the May 10 measurement packets:

1. Open Tag Assistant, GA4 DebugView/Realtime, Google Ads conversion diagnostics, and DevTools Network in a logged-in browser session.
2. First search for any genuine/historical non-US `purchase` event in GA4/Google Ads activity. If found, capture sanitized transaction id, value, currency, item detail, and Google Ads request details.
3. If no historical non-US purchase exists, stop and request the existing exact owner approval for one controlled low-value non-US test purchase/refund/cancel.
4. Use `GB` first if the owner wants the strongest non-USD single-market test, because GBP is non-USD and GB has prior no-payment checkout UI evidence.

No local-only evidence in this hunt justifies enabling non-US Search spend.

## Guardrails Honored

- No browser use.
- No checkout.
- No network request.
- No payment, order, refund, or cancel.
- No external account write.
- No Shopify Admin, Google Ads, GA4/GTM, Merchant, Pinterest, theme, prompt, script, tracker, worklog, coordination, or `AGENTS.md` edit.
- Only this assigned report file was written.
