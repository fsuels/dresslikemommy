# ES/IT No-Upload Final URL And Native Review Action Pack

Date: `2026-05-12`
Mode: local-only / review-only. No Google Ads preview, import, upload, account edit, status change, budget/bid change, Merchant, Pinterest, Shopify product/feed/conversion write, checkout payment/order, billing, credential, or destructive action occurred.

## Purpose

Move ES/IT toward launch quality without crossing platform-write guardrails.

The existing ES/IT native-review slice is ready to send, and a Golden Daisy country-qualified landing QA passed. This action pack closes a remaining local gap: the current ES/IT split CSVs use five product destinations per market, not only Golden Daisy. Those current destinations are now listed in a review-only URL map so the next operator knows exactly which URLs still need just-in-time QA before any platform use.

## Inputs Inspected

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/es_it_native_keyword_replacements_review_only.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/es_it_native_rsa_replacements_review_only.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/es_it_native_negative_replacements_review_only.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/es_it_native_locale_status_review_only.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/ES_IT_NATIVE_REVIEW_REQUEST.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/ES_IT_COUNTRY_QUALIFIED_LANDING_QA.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/ES_intl_search_paused_draft_web_bulk.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/IT_intl_search_paused_draft_web_bulk.csv`

## Current Review-Only Assets

| Asset | ES Rows | IT Rows | Upload Status |
|---|---:|---:|---|
| Native keyword replacements | 50 | 50 | `REVIEW_ONLY_NOT_UPLOAD` |
| Native RSA replacements | 5 | 5 | `REVIEW_ONLY_NOT_UPLOAD` |
| Negative keyword review rows | 14 | 16 | `REVIEW_ONLY_NOT_UPLOAD` |
| Locale status rows | 1 | 1 | `REVIEW_ONLY_NOT_UPLOAD` |

The existing Golden Daisy country-qualified landing QA passed:

- ES: `https://www.dresslikemommy.com/es/products/golden-daisy-mommy-and-me-set?country=ES`
- IT: `https://www.dresslikemommy.com/it/products/golden-daisy-mommy-and-me-set?country=IT`

Important limit: Golden Daisy QA does not cover the five current product destinations in the ES/IT split CSVs.

## New Local Artifact

Created:

`es_it_final_url_review_map_no_upload.csv`

Contents:

- 20 rows total.
- 10 ES ad groups and 10 IT ad groups.
- 5 unique current split-file product destinations per market.
- Every row is country-qualified (`?country=ES` or `?country=IT`).
- Every row is marked `REVIEW_ONLY_NOT_UPLOAD`.
- Every row is marked `NEEDS_JIT_URL_QA_FOR_THIS_DESTINATION`.

## Required Next Local QA Before Platform Use

For each unique ES/IT destination in `es_it_final_url_review_map_no_upload.csv`, run slow browser QA before any Ads preview/import/use:

1. PDP loads with HTTP `200`, no verification wall, no visible `429`.
2. HTML language and visible page text match the intended locale enough for paid traffic.
3. Currency/presentment matches the target market: ES/EUR, IT/EUR.
4. Cart preserves country/currency after add-to-cart.
5. Checkout reaches shipping step with the correct country selected and no payment/order.
6. Shipping/pricing copy does not imply returns are free or local inventory exists.
7. No supplier/source-domain tokens.
8. No stale Christmas/beach-mismatch blocker, especially if any destination is later swapped to the held Vacation Family URL.
9. No unsupported discount/review/social-proof claims.
10. Native reviewer verdict is `APPROVED_NATIVE` or `APPROVED_WITH_EDITS` with edits applied to a new review-only file.

## Public GET Destination QA Follow-Up

Worker follow-up ran slow public GET checks for the 10 unique current split-file destinations and saved:

- `es_it_split_destination_public_get_qa_summary.csv`
- `es_it_split_destination_public_get_qa_summary.json`
- `es_it_split_destination_public_get_qa_refined_summary.csv`
- `es_it_split_destination_public_get_qa_refined_summary.json`
- raw HTML under `es_it_destination_qa_raw/`

Result:

- `10/10` loaded with HTTP `200`, country-qualified final URL, expected `html lang`, EUR signals, and expected localized text signals.
- `10/10` remain blocked for paid use because raw HTML contains source/supplier wording such as `supplier source table` / supplier fallback strings.
- `2/10` additionally expose the blocked beach/Vacation Family handle in related-products links:
  - ES light-blue family destination.
  - IT light-blue family destination.
- The initial strict checker also detected Shopify's normal `captcha-bootstrap` script; the refined summary does not treat that script alone as a visible verification wall, but it keeps the source/supplier and blocked beach-handle findings as real paid-use blockers until fixed or disproven with visual/browser QA.

Current decision: ES/IT split-file destinations are not paid-use-ready. Native review can still proceed, but no ES/IT Ads preview/import/use should happen until the destination blockers are resolved or the URL map is replaced with destinations that pass public and browser QA.

## Golden Daisy Checkout Alternative Follow-Up

Parent follow-up then created a separate isolated-browser no-payment checkout verifier for the country-qualified Golden Daisy URLs:

- `lanes/es-it-golden-daisy-checkout/es_it_golden_daisy_checkout_to_shipping.py`
- `lanes/es-it-golden-daisy-checkout/ES_IT_GOLDEN_DAISY_CHECKOUT_TO_SHIPPING.md`
- `lanes/es-it-golden-daisy-checkout/es_it_golden_daisy_checkout_to_shipping_summary.json`

Result:

- ES Golden Daisy URL reached product `html lang` `es`, cart currency `EUR`, selected checkout country `Spain`, Standard Delivery `FREE`, Express Delivery `€11.95`, no verification wall, and no order-confirmation text.
- IT Golden Daisy URL reached product `html lang` `it`, cart currency `EUR`, selected checkout country `Italy`, Standard Delivery `FREE`, Express Delivery `€11.95`, no verification wall, and no order-confirmation text.
- No payment data was entered, no Pay Now / Place Order click occurred, and no order was created.

Decision:

- Golden Daisy is the cleaner ES/IT localized launch-candidate URL path after real native-speaker signoff.
- The current five-destination ES/IT split map remains blocked for paid use until source/supplier wording and blocked related-link issues are cleaned or the destination map is replaced.

Follow-up review-only microtest files now exist:

- `ES_IT_GOLDEN_DAISY_MICROTEST_REVIEW_ONLY.md`
- `es_it_golden_daisy_microtest_keywords_review_only.csv`
- `es_it_golden_daisy_microtest_rsa_review_only.csv`

These files narrow the candidate to `3` exact keywords and `1` RSA per market, all `REVIEW_ONLY_NOT_UPLOAD`, for native review only.

## Exact Next Safe Action

Send the existing ES/IT native-review package plus `es_it_final_url_review_map_no_upload.csv` to a real native reviewer, but label current destinations as blocked pending landing cleanup/reselection. Do not upload any row.

In parallel, the next local operator should prepare a Golden Daisy-only ES/IT micro-test structure after native signoff, or request exact owner approval for the narrow storefront/theme/product-copy cleanup needed to remove source/supplier wording and blocked related-product links from the current split destinations. Only after native signoff and destination QA pass should the parent prepare a fresh exact approval phrase for either:

- an ES/IT paused preview/import, or
- a tightly controlled ES/IT live test.

## Commands Run

- `python3 - <<'PY' ...` inspected ES/IT native review CSV headers/counts/sample rows.
- `sed -n '1,220p' .../ES_IT_NATIVE_REVIEW_REQUEST.md`
- `sed -n '1,220p' .../ES_IT_COUNTRY_QUALIFIED_LANDING_QA.md`
- `python3 - <<'PY' ...` extracted current ES/IT split-file ad-group to final-URL mappings.
- `python3 - <<'PY' ...` ran slow public GET destination checks for 10 unique ES/IT split-file URLs.
- `python3 - <<'PY' ...` produced refined destination blocker classification from saved raw HTML.

## Guardrails

This is a review/action-pack artifact only. It does not authorize Google Ads upload, preview, import, campaign/ad group/ad/keyword/status/budget/bid edits, live spend, Merchant/Pinterest/Shopify product/feed/conversion writes, checkout payment/order/refund/cancel, billing/account/credential changes, or destructive actions.
