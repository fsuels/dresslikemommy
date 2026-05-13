# ES/IT Native Review Request

Date: 2026-05-12

Status: `READY_TO_SEND_TO_NATIVE_REVIEWER__NOT_UPLOADED`

## Files For Review

- `es_it_native_keyword_replacements_review_only.csv`
- `es_it_native_rsa_replacements_review_only.csv`
- `es_it_native_negative_replacements_review_only.csv`
- `es_it_native_locale_status_review_only.csv`

## Reviewer Instructions

Please review the Spanish (`es-ES`) and Italian (`it-IT`) Google Ads Search copy for native clarity, buyer intent, and policy-safe accuracy. These rows are not uploaded and must remain review-only until approved.

For each market, confirm or correct:

- High-intent keyword wording for mother-daughter, mommy-and-me, matching family dresses, outfits, and beach/vacation matching sets.
- Whether exact and phrase variants sound natural and are commercially useful.
- RSA headline and description fluency, grammar, and claim safety.
- Negative keyword appropriateness by market, especially terms that would waste spend or attract non-buyer traffic.
- Any words that are technically translated but locally awkward, misleading, or too broad.

## Hard Review Rules

- Do not add claims about a physical store, local inventory, warehouse stock, guaranteed on-hand stock, or pickup.
- Do not add discount, review-count, shipping-time, delivery-date, or price claims unless separately verified in the evidence packet.
- Do not use supplier/source terms or marketplace terms.
- Do not approve any row for platform upload until country-qualified landing QA has also passed.

## Landing URL Rule

Paid URLs for these locales must be country-qualified:

- ES: `/es/products/<handle>?country=ES`
- IT: `/it/products/<handle>?country=IT`

Do not use bare `/es` or `/it` product URLs for ads without a fresh readback.

## Requested Output

Return one of these verdicts per file and market:

- `APPROVED_NATIVE`
- `APPROVED_WITH_EDITS`
- `REJECTED_REWRITE_REQUIRED`

For edited rows, return the row identifier plus the replacement text. Keep each replacement inside Google Ads limits.

## Guardrail

This is a review package only. No Google Ads upload, preview, import, campaign edit, budget/bid/status change, Merchant/Pinterest/Shopify product/feed/conversion write, payment, or order action is authorized by this request.
