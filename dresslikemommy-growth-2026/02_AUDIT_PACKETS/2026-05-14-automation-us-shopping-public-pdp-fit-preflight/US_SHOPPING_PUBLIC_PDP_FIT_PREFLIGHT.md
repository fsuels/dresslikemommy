# US Shopping Public PDP Fit Preflight

Generated: `2026-05-14T17:04:09Z`

## Scope

- Public storefront readback for the 24 rows in `us_shopping_query_title_candidates.csv`.
- Unique PDP handles checked: `10`.
- This reduces landing/source/title ambiguity before the required authenticated Google Ads / Merchant item-level export.
- It is not a product/feed/title change and not a live Ads action.

## Result

- PDP handles returning `200` for both public header variants: `10/10`.
- Source-clean handles: `8/10`.
- Public candidate rows ready to carry into the authenticated item export: `18/24`.
- Query-fit counts: `{'STRONG': 22, 'WEAK': 2}`.

## Decisions

- Continue with the authenticated read-only Standard Shopping item-level export; this packet does not prove which products actually received impressions.
- Do not add negatives, edit product groups, change bids/budgets/status, or edit Shopify/Merchant titles from this public preflight alone.
- If the authenticated export shows one of these clean PDPs received impressions but the feed title lacks the matching buyer intent, prepare a narrow owner approval packet for title/feed repair.

## Files

- Rows: `us_shopping_public_pdp_fit_preflight_rows.csv`
- Auth-export clean scope: `us_shopping_auth_export_public_clean_scope.csv`
- Summary: `us_shopping_public_pdp_fit_preflight_summary.json`

## Holds

- Supplier/source hit handles: `['chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit']`
- URL-like brand hit handles: `[]`
- Stale/invalid copy hit handles: `['dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set']`
