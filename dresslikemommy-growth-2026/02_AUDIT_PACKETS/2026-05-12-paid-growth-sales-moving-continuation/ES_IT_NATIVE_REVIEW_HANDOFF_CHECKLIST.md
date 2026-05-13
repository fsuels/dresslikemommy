# ES/IT Native Review Handoff Checklist

Date: 2026-05-12
Owner lane: Worker C local-only ES/IT launch-quality prep
Status: `READY_FOR_NATIVE_REVIEW__REVIEW_ONLY_NOT_UPLOAD`

## Source Packet

Use the existing ES/IT no-upload slice:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/`

Primary reviewer request:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/ES_IT_NATIVE_REVIEW_REQUEST.md`

Landing QA:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/ES_IT_COUNTRY_QUALIFIED_LANDING_QA.md`

## Files Native Reviewer Must Approve

| File | Rows | ES rows | IT rows | Current gate |
|---|---:|---:|---:|---|
| `es_it_native_keyword_replacements_review_only.csv` | `100` | `50` | `50` | `REVIEW_ONLY_NOT_UPLOAD` |
| `es_it_native_rsa_replacements_review_only.csv` | `10` | `5` | `5` | `REVIEW_ONLY_NOT_UPLOAD` |
| `es_it_native_negative_replacements_review_only.csv` | `30` | `14` | `16` | `REVIEW_ONLY_NOT_UPLOAD` |
| `es_it_native_locale_status_review_only.csv` | `2` | `1` | `1` | `REVIEW_ONLY_NOT_UPLOAD` |

Row keys to use when returning edits:

- Keywords: `market`, `locale`, `theme`, `match_type`, `corrected_keyword`.
- RSAs: `market`, `locale`, `theme`.
- Negatives: `market`, `locale`, `negative_keyword`, `recommended_match_type`, `category`.
- Locale status: `market`, `locale`.

## Market Watchpoints

### ES

- Confirm Spanish buyer intent is natural for mother-daughter, mommy-and-me, family matching, beach/vacation, and photo-oriented searches.
- Check that exact and phrase keyword rows are not too broad for a low-budget launch.
- Review negative rows carefully before approving broad use; some terms should remain exact-only until live search-term waste proves need.
- Do not approve wording that implies a physical store, local stock, warehouse stock, pickup, guaranteed inventory, guaranteed delivery date, unverified discounts, or review-count/social-proof claims.

### IT

- Confirm Italian keyword wording sounds like real shopper language, not literal translation.
- Check family matching and parent-child phrases for local clarity, especially where the product could be confused with costumes, DIY patterns, or generic family clothing.
- Review negative rows for ambiguity before approval; keep marketplace/supplier/DIY terms conservative unless the reviewer is confident they do not block qualified apparel intent.
- Do not approve wording that implies physical store operations, stocked inventory, pickup, guaranteed delivery, unverified promotions, or unsupported best-seller/review claims.

## Landing QA Already Passed

Slow country-qualified Golden Daisy landing QA passed locally for:

- ES: `https://www.dresslikemommy.com/es/products/golden-daisy-mommy-and-me-set?country=ES`
- IT: `https://www.dresslikemommy.com/it/products/golden-daisy-mommy-and-me-set?country=IT`

Validated results:

- HTTP `200`.
- Expected ES/IT language signals.
- EUR presentment.
- No verification wall or Shopify `429`.
- No supplier/source-domain hits.
- No stale paid blocker copy.

Required URL rule remains: paid URLs must be country-qualified (`?country=ES` or `?country=IT`). Do not use bare `/es` or `/it` product routes for ads without a fresh readback.

## Post-Signoff QA And Approval Path

1. Native reviewer returns one verdict per file and market: `APPROVED_NATIVE`, `APPROVED_WITH_EDITS`, or `REJECTED_REWRITE_REQUIRED`.
2. If edits are returned, update a new local replacement layer only; keep all rows `REVIEW_ONLY_NOT_UPLOAD`.
3. Re-run local count/status validation:
   - ES keywords `50`, IT keywords `50`.
   - ES RSAs `5`, IT RSAs `5`.
   - ES negatives `14`, IT negatives `16`.
   - ES/IT locale status `1` row each.
   - All upload statuses exactly `REVIEW_ONLY_NOT_UPLOAD`.
4. Build the exact final URL map using only country-qualified ES/IT URLs.
5. Run slow no-payment browser QA for each exact paid final URL through PDP, cart, and checkout shipping step:
   - correct language behavior;
   - EUR presentment;
   - correct selected country;
   - shipping/pricing copy safe for a dropshipping business;
   - no supplier/source-token exposure;
   - no stale blocked URL or old metadata;
   - no payment submitted and no order created.
6. After native review and final URL QA pass, prepare the exact owner approval phrase for the next action. Until then, do not upload, preview, import, enable, edit, or associate any ES/IT Google Ads rows.

## Worker C Local Validation

Validated on 2026-05-12 from disk:

- `es_it_native_keyword_replacements_review_only.csv`: `100` rows, ES `50`, IT `50`, upload status only `REVIEW_ONLY_NOT_UPLOAD`.
- `es_it_native_rsa_replacements_review_only.csv`: `10` rows, ES `5`, IT `5`, upload status only `REVIEW_ONLY_NOT_UPLOAD`.
- `es_it_native_negative_replacements_review_only.csv`: `30` rows, ES `14`, IT `16`, upload status only `REVIEW_ONLY_NOT_UPLOAD`.
- `es_it_native_locale_status_review_only.csv`: `2` rows, ES `1`, IT `1`, upload status only `REVIEW_ONLY_NOT_UPLOAD`.
- `es_it_country_landing_qa_summary.csv`: `2` rows, decisions `ES_COUNTRY_QUALIFIED_LANDING_QA_PASSED` and `IT_COUNTRY_QUALIFIED_LANDING_QA_PASSED`.

## Guardrail

This handoff is local-only. It does not authorize Google Ads upload/preview/import, campaign/ad group/ad/keyword/status/budget/bid edits, Merchant/Pinterest/Shopify product/feed/conversion writes, live spend, checkout payment/order actions, credential/account/billing changes, or destructive actions.
