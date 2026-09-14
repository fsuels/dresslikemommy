# Google Shopping Parent-Outfit Source 10664235992 Not-Winning Diagnosis

Generated: `2026-05-21T14:58:29Z`

## Scope

This is a read-only diagnosis after the narrow Spanish blank-label supplemental source was created. No Merchant, Shopify, Google Ads, Google & YouTube, campaign, budget, bid, status, product-group, conversion, billing, source reset, broad sync, or product-data write occurred.

## Gate Rerun

Read-only parent-outfit counts/images/no-catchall gate:

- Gate JSON: `google_shopping_parent_outfit_merchant_feed_gate_20260521T145604Z.json`
- Gate passed: `false`
- Reason: `FAIL_CLOSED__MERCHANT_FEED_LABEL_IMAGE_READBACK_NOT_LIVE`
- Expected rows: `4,531`
- Ready rows: `4,392`
- Bad catchall units: `0`
- Campaign status ok: `true`
- Old test campaign paused: `true`

Read-only eligibility diagnostic:

- Diagnostic JSON: `google_shopping_parent_outfit_eligibility_diagnostic_20260521T145651Z.json`
- Ads-present expected rows: `4,460`
- Ads-ready-label rows: `4,392`
- Ads-present non-ready-label rows: `68`
- Ads-missing expected rows: `71`
- Availability counts: `IN_STOCK=4,440`, `OUT_OF_STOCK=20`

## Exact 68-Row Probe

Targeted Ads Shopping-product probe for the exact TSV rows uploaded to Merchant source `10664235992`:

- Probe JSON: `google_shopping_parent_outfit_spanish_blank_label_source_10664235992_ads_surface_probe_20260521T145829Z.json`
- Probe CSV: `google_shopping_parent_outfit_spanish_blank_label_source_10664235992_ads_surface_probe_20260521T145829Z.csv`
- Overlay rows checked: `68`
- Ads rows returned: `68`
- Unique Ads item IDs returned: `68`
- Overlay IDs missing from Ads surface: `0`
- Language counts: `es=68`
- Target country counts: `US=68`
- Status counts: `NOT_ELIGIBLE=68`
- Availability counts: `IN_STOCK=68`
- Actual label tuple counts: blank labels `|||| = 68`
- Expected label tuple counts:
  - `paid_eligible|mommy_and_me|swimwear|parent_outfit|us_parent_outfit_ready_v20260520 = 60`
  - `paid_eligible|mommy_and_me|tops_shirts|parent_outfit|us_parent_outfit_ready_v20260520 = 6`
  - `paid_eligible|mommy_and_me|dresses|parent_outfit|us_parent_outfit_ready_v20260520 = 2`
- Overlay label match counts: `false=68`
- Overlay image match counts: `false=68`

## Diagnosis

Source `10664235992` is not failing because the uploaded offer IDs are absent from the Ads Shopping-product surface. All `68` exact offer IDs are present as `US` / Spanish (`es`) rows.

It is also not a partial label-only failure. None of the overlay attributes appear to have materialized into the Ads Shopping-product surface: all five custom labels remain blank for all `68` rows, and all `68` image links still differ from the uploaded overlay image links.

The narrow conclusion is: Merchant source `10664235992` matched and processed at source level, but its supplemental attributes are not yet winning/materialized on the final `US/es` product rows exposed through Google Ads. The remaining explanation is either normal Merchant-to-Ads attribute propagation delay or a Merchant supplemental-source application/precedence setting that is not visible from the current local API scope.

## Guardrails Preserved

- All parent-outfit V2 Shopping campaigns stayed paused.
- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` stayed paused.
- No Google Ads mutate operation occurred.
- No Merchant write occurred in this diagnostic step.
- No Shopify product, publication, inventory, title, price, handle, body, or SEO write occurred.
- No broad Google & YouTube sync, source reset, product recreation, or primary-source repair occurred.

## Next Valid Action

Do one more read-only gate after a longer Merchant-to-Ads propagation window. If the exact `68` rows still show blank labels and non-overlay images, the next action should be a read-only authenticated Merchant UI inspection of source `10664235992` and the affected `US/es` product rows to find the source-application/precedence setting. Do not upload another file, repeat English uploads, trigger broad sync, reset sources, recreate products, or change Shopify product data.
