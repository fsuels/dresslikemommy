# ES/IT Native QA No-Upload Slice Report

Date: 2026-05-12

Decision: `LOCAL_REVIEW_SLICE_READY_NO_UPLOAD`

## Executive Verdict

ES and IT are the cleanest localized Google Ads candidates after the English-first GB/CA/AU micro-cohort, but they are not upload-ready. This packet extracts only the ES/IT native replacement rows for review and keeps every row `REVIEW_ONLY_NOT_UPLOAD`.

No Google Ads import, preview, upload, campaign edit, status change, budget/bid change, or account write was made.

## Extracted Review Slices

| File | Rows | Markets | Upload status |
|---|---:|---|---|
| `es_it_native_keyword_replacements_review_only.csv` | `100` | ES, IT | `REVIEW_ONLY_NOT_UPLOAD` |
| `es_it_native_rsa_replacements_review_only.csv` | `10` | ES, IT | `REVIEW_ONLY_NOT_UPLOAD` |
| `es_it_native_negative_replacements_review_only.csv` | `30` | ES, IT | `REVIEW_ONLY_NOT_UPLOAD` |
| `es_it_native_locale_status_review_only.csv` | `2` | ES, IT | `REVIEW_ONLY_NOT_UPLOAD` |

Expected split:

- ES: `50` keyword rows, `5` RSA rows, `14` negative-review rows.
- IT: `50` keyword rows, `5` RSA rows, `16` negative-review rows.

Source packet:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation/`

## Required Landing URL Rule

Do not use bare `/es` or `/it` product routes for paid traffic by default. Prior evidence showed bare language paths can land as English / United States / USD.

Use country-qualified localized product URLs:

- ES: `/es/products/<handle>?country=ES`
- IT: `/it/products/<handle>?country=IT`

Prior evidence supports ES/IT product/cart/checkout-to-shipping presentment after localization, with EUR carried and no payment/order, but each final paid URL still needs a slow just-in-time browser QA pass before platform use.

## Remaining Blockers

- Native-speaker review is still required for ES/IT keyword, RSA, and negative-review rows.
- Country-qualified landing-language QA is still required for the exact final URL map before any Ads preview/import/use.
- Checkout can remain partly English (`en-ES` / `en-IT`) even when PDP/cart are localized; do not overstate full native checkout.
- Current ES/IT rows are review-only; do not import or enable them.
- Live ES/IT expansion still requires exact owner approval and readbacks.

## Exact Next Safe Action

1. Send the four extracted CSVs for ES/IT native review.
2. Build a final URL map using only country-qualified localized routes.
3. Run one slow browser QA per market through PDP, cart, and checkout shipping step with no payment/order:
   - Language behavior.
   - EUR presentment.
   - Correct selected country.
   - Shipping/pricing copy.
   - No source/supplier-token exposure.
   - No stale blocked product URL.
4. Only after native review plus landing QA passes, prepare an exact approval phrase for a paused preview/import or a controlled live test.

## Guardrails Preserved

No Google Ads upload/preview/import/account write, no campaign/ad group/ad/keyword/status/budget/bid change, no Merchant/Pinterest/Shopify product/feed/conversion write, no payment/order/refund/cancel, no credential/account/billing edit, no live theme push, and no destructive filesystem action occurred.
