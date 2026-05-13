# ES/IT Golden Daisy Native Review Signoff Bundle

Date: `2026-05-12`
Status: `PENDING_NATIVE_REVIEW__REVIEW_ONLY_NOT_UPLOAD`

## Purpose

This bundle turns the ES/IT Golden Daisy microtest into a concrete native-review work item. It does not authorize Google Ads platform use.

Reviewer output should be recorded in:

- `ES_IT_GOLDEN_DAISY_NATIVE_REVIEW_SIGNOFF_FORM.csv`

## Review Verdicts

Allowed verdicts:

- `APPROVED_NATIVE`
- `APPROVED_WITH_EDITS`
- `REJECTED_REWRITE_REQUIRED`

Current placeholder:

- `PENDING_NATIVE_REVIEW`

Platform use remains blocked until every row is either `APPROVED_NATIVE` or `APPROVED_WITH_EDITS`, and any `APPROVED_WITH_EDITS` row includes replacement text.

## Review Scope

| Market | Rows | Assets |
|---|---:|---|
| `ES` / `es-ES` | `4` | `3` exact keywords, `1` RSA |
| `IT` / `it-IT` | `4` | `3` exact keywords, `1` RSA |

Source files:

- `ES_IT_GOLDEN_DAISY_MICROTEST_REVIEW_ONLY.md`
- `es_it_golden_daisy_microtest_keywords_review_only.csv`
- `es_it_golden_daisy_microtest_rsa_review_only.csv`
- `validate_es_it_golden_daisy_microtest.py`
- `es_it_golden_daisy_microtest_validation_summary.json`

## Hard Review Rules

Do not approve copy that implies:

- physical store operations
- local inventory, warehouse stock, guaranteed on-hand stock, or pickup
- unsupported delivery dates or shipping-speed promises
- unsupported discount claims beyond the verified automatic 2+ item discount
- unsupported review counts, best-seller claims, or platform/source claims
- supplier, source, marketplace, wholesale, or dropshipping-origin language

## Existing Local Evidence

The local microtest verifier passed `44` checks:

- `6` exact keyword rows and `2` RSA rows.
- All rows are `REVIEW_ONLY_NOT_UPLOAD`.
- All rows are `NATIVE_REVIEW_REQUIRED`.
- ES and IT Golden Daisy final URLs are country-qualified.
- ES and IT landing QA passed.
- ES and IT checkout-to-shipping QA passed with `EUR`, no verification wall, no payment, and no order.

## Reviewer Instructions

For each row in `ES_IT_GOLDEN_DAISY_NATIVE_REVIEW_SIGNOFF_FORM.csv`:

1. Set `reviewer_verdict` to one of the allowed verdicts.
2. If verdict is `APPROVED_WITH_EDITS`, fill `replacement_text`.
3. If verdict is `REJECTED_REWRITE_REQUIRED`, explain why in `reviewer_notes`.
4. Keep replacement text within Google Ads limits.
5. Preserve country-qualified URLs unless a replacement URL is separately QA-read back.

## Validation

Run:

```bash
python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/validate_es_it_native_signoff_form.py
```

Current expected result before reviewer work:

- `status`: `PENDING_NATIVE_REVIEW`
- `platform_use_ready`: `false`

## Next Gate

After native signoff:

1. Run the signoff-form validator.
2. If any row has edits, create a new review-only replacement file and rerun the microtest verifier.
3. Rerun country-qualified landing and no-payment checkout QA if any final URL changes.
4. Request exact owner action-time approval before any Google Ads preview/import/upload/use.

## Guardrails

No Google Ads upload, preview, import, campaign/ad group/ad/keyword/status/budget/bid edit, live spend, Merchant/Pinterest/Shopify product/feed/conversion write, checkout payment/order/refund/cancel, billing/account/credential edit, or destructive action occurred.
