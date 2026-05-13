# ES/IT Golden Daisy Microtest Review-Only Packet

Date: `2026-05-12`
Status: `REVIEW_ONLY_NOT_UPLOAD`

## Purpose

Prepare the smallest ES/IT localized Search candidate that can move forward after native-speaker signoff without relying on the currently blocked five-destination ES/IT split map.

This is local-only. It is not a Google Ads bulk upload, preview, import, status edit, budget edit, bid edit, or approval request.

## Candidate Scope

| Market | Working campaign | Ad group | Keywords | RSA | Final URL |
|---|---|---|---:|---:|---|
| `ES` | `DLM_ES_SEARCH_GOLDEN_DAISY_NATIVE_REVIEW_ONLY_20260512` | `Golden Daisy Mommy & Me - Exact` | `3` exact | `1` | `https://www.dresslikemommy.com/es/products/golden-daisy-mommy-and-me-set?variant=44197959499873&country=ES` |
| `IT` | `DLM_IT_SEARCH_GOLDEN_DAISY_NATIVE_REVIEW_ONLY_20260512` | `Golden Daisy Mommy & Me - Exact` | `3` exact | `1` | `https://www.dresslikemommy.com/it/products/golden-daisy-mommy-and-me-set?variant=44197959499873&country=IT` |

Created files:

- `es_it_golden_daisy_microtest_keywords_review_only.csv`
- `es_it_golden_daisy_microtest_rsa_review_only.csv`
- `validate_es_it_golden_daisy_microtest.py`
- `es_it_golden_daisy_microtest_validation_summary.json`

## Local Validation

The local verifier passed:

`python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/validate_es_it_golden_daisy_microtest.py`

Result:

- Status: `PASS`.
- Checks: `44`.
- Failed checks: `0`.
- Verified keyword rows: `6`, exactly `3` ES and `3` IT.
- Verified RSA rows: `2`, exactly `1` ES and `1` IT.
- Verified all rows are `REVIEW_ONLY_NOT_UPLOAD` and `NATIVE_REVIEW_REQUIRED`.
- Verified all keywords are `Exact`.
- Verified all microtest keywords and RSAs exist in the source ES/IT native review packet under `Mommy & Me Dresses`.
- Verified ES/IT final URLs are the country-qualified Golden Daisy URLs with variant `44197959499873`.
- Verified landing QA decisions passed for ES and IT with no forbidden or stale hits.
- Verified checkout-to-shipping decisions passed for ES and IT, cart currency `EUR`, shipping UI pass, no verification wall, and no payment/order created.

## Evidence Already Passed

- ES Golden Daisy landing: HTTP `200`, `html lang` `es`, EUR signals, expected Spanish shopper words, no verification/429, no supplier/source-domain hits.
- IT Golden Daisy landing: HTTP `200`, `html lang` `it`, EUR signals, expected Italian shopper words, no verification/429, no supplier/source-domain hits.
- ES checkout shipping: selected country `Spain`, cart currency `EUR`, Standard Delivery `FREE`, Express Delivery `€11.95`, no verification wall, no order-confirmation text.
- IT checkout shipping: selected country `Italy`, cart currency `EUR`, Standard Delivery `FREE`, Express Delivery `€11.95`, no verification wall, no order-confirmation text.

Evidence files:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/ES_IT_COUNTRY_QUALIFIED_LANDING_QA.md`
- `lanes/es-it-golden-daisy-checkout/ES_IT_GOLDEN_DAISY_CHECKOUT_TO_SHIPPING.md`

## Native Reviewer Questions

For each market, return one verdict: `APPROVED_NATIVE`, `APPROVED_WITH_EDITS`, or `REJECTED_REWRITE_REQUIRED`.

Review the candidate for:

- Natural buyer language for mother-daughter / mommy-and-me outfits.
- Whether the three exact keywords are high-intent enough for a low-budget launch.
- Whether the RSA copy sounds native and claim-safe.
- Whether any phrase should be swapped before platform use.
- Whether negatives should stay as a watchlist until search-term evidence exists.

Do not approve wording that implies physical store operations, stocked/local inventory, pickup, guaranteed delivery, guaranteed discounts beyond the verified 2+ item automatic promo, unsupported review counts, or best-seller claims.

## Current Blocked Alternative

The broader ES/IT split-file destination map is still blocked for paid use. Public GET QA showed core language/currency presentment passed, but raw HTML exposed source/supplier wording on all 10 current destinations and two light-blue family destinations exposed the held beach/Vacation Family related link.

Use Golden Daisy as the clean candidate path unless the blocked split destinations are cleaned or replaced.

## Next Gate

No Ads platform action is allowed from this packet alone.

Required before any ES/IT Google Ads preview/import/use:

1. Real native-speaker signoff on these rows.
2. Any edits written to a new review-only file.
3. Fresh country-qualified URL and checkout readback if the final URL changes.
4. Exact owner action-time approval naming the ES/IT Google Ads action.

## Guardrails

No Google Ads upload, preview, import, campaign/ad group/ad/keyword/status/budget/bid edit, live spend, Merchant/Pinterest/Shopify product/feed/conversion write, checkout payment/order/refund/cancel, billing/account/credential edit, or destructive action occurred.
