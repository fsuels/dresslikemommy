# Google Shopping Parent-Outfit Reduced Activation-Review Gate

Generated: `20260521T103852Z`

Mode: read-only local evidence build. No Merchant, Shopify, Google & YouTube, Google Ads, campaign, product group, budget, bid, status, conversion, billing, feed, product-data, inventory, source reset, broad sync, activation, or unpause write occurred.

## Decision

Reduced read-only activation-review gate: `PASS`

Reason: `REDUCED_READ_ONLY_ACTIVATION_REVIEW_SCOPE_CLEAN`

## Source Inputs

- Latest local ready-products CSV: `google_shopping_parent_outfit_ready_products_20260521T103730Z.csv`
- Matching gate JSON: `google_shopping_parent_outfit_merchant_feed_gate_20260521T103730Z.json`
- Exact unresolved-offer exclusion CSV: `google_shopping_parent_outfit_unresolved_offer_exclusion_scope_20260521T095911Z.csv`
- Exact out-of-stock hold CSV: `google_shopping_parent_outfit_eligibility_out_of_stock_rows_20260521T095911Z.csv`
- Included Merchant spec rows: `4531`
- Latest ready-label rows: `4392`
- Exact unresolved-offer exclusion rows held out: `141`
- Exact out-of-stock hold rows held out: `20`
- Unresolved rows that are now ready but still held out by exact scope: `2`

## Reduced Candidate Scope

- Candidate rows: `4370`
- Candidate parent products: `203`
- Candidate rows by lane: `{'daddy_and_me': 522, 'family_matching': 2571, 'mommy_and_me': 1277}`
- Candidate parent products by lane: `{'daddy_and_me': 34, 'family_matching': 77, 'mommy_and_me': 92}`
- Candidate rows by subgroup: `{'dresses': 503, 'pajamas': 252, 'sets': 167, 'sweaters_outerwear': 236, 'swimwear': 484, 'tops_shirts': 2728}`

## Safety Checks

- Candidate rows all in included spec: `True`
- Candidate rows all in latest ready-label CSV: `True`
- Candidate excludes all exact unresolved-offer rows: `True`
- Candidate excludes all exact out-of-stock hold rows: `True`
- Candidate labels match spec: `True`
- Candidate product images match proposed parent hero images: `True`
- Candidate availability all `IN_STOCK`: `True`
- Latest gate label mismatches: `0`
- Latest gate image mismatches: `0`
- Latest gate missing live images: `0`
- V2 campaigns paused / status safe: `True`
- Old test campaign paused: `True`
- Bad catchall listing units: `0`

## Approval Boundary

This gate does not authorize activation. It only proves a reduced review surface after holding out the exact `141` unresolved-offer rows and exact `20` out-of-stock rows.

Separate activation approval packet:

- `GOOGLE_SHOPPING_PARENT_OUTFIT_REDUCED_SCOPE_ACTIVATION_APPROVAL_PACKET_20260521.md`

## Recommended Next Action

Review the separate reduced-scope activation approval packet first. This is better than another upload/resync because the clean candidate rows already pass the local label/image/catchall/paused-safety checks while the held-out rows are isolated for a later repair lane.

## Evidence Outputs

- `google_shopping_parent_outfit_reduced_activation_review_gate_20260521T103852Z.json`
- `google_shopping_parent_outfit_reduced_activation_review_candidates_20260521T103852Z.csv`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_REDUCED_ACTIVATION_REVIEW_GATE_20260521T103852Z.md`
