# Google Shopping Parent-Outfit Reduced-Scope Activation Approval Packet

Generated: `20260521T132011Z`

Mode: approval packet only. No Shopping activation, unpause, budget, bid, status, product group, conversion, billing, Merchant feed/source, Google & YouTube sync, Shopify product/publication/inventory/title/price/handle/SEO, broad sync, source reset, or product-data write is authorized by this document.

## Reduced Scope Proven Read-Only

The reduced activation-review gate passed using:

- Exact `141` unresolved-offer exclusion scope: `google_shopping_parent_outfit_unresolved_offer_exclusion_scope_20260521T095911Z.csv`.
- Exact `20` out-of-stock hold: `google_shopping_parent_outfit_eligibility_out_of_stock_rows_20260521T095911Z.csv`.
- Latest local ready-label readback: `google_shopping_parent_outfit_ready_products_20260521T131716Z.csv`.

Reduced candidate counts:

- Candidate rows: `4370`.
- Candidate parent products: `203`.
- Rows by lane: `{'daddy_and_me': 522, 'family_matching': 2571, 'mommy_and_me': 1277}`.
- Parent products by lane: `{'daddy_and_me': 34, 'family_matching': 77, 'mommy_and_me': 92}`.
- Rows by subgroup: `{'dresses': 503, 'pajamas': 252, 'sets': 167, 'sweaters_outerwear': 236, 'swimwear': 484, 'tops_shirts': 2728}`.

The gate also confirmed:

- Candidate rows are included spec rows and latest ready-label rows.
- Candidate rows exclude all exact unresolved-offer rows and all exact out-of-stock hold rows.
- Candidate labels/images match the spec.
- Candidate rows are `IN_STOCK`.
- V2 Shopping campaigns and the old test campaign remain paused in the source gate.
- Bad catchall listing units remain `0`.

## Approval Phrase

If approved later, paste a fresh exact action-time approval phrase that names the allowed activation action and keeps every non-activation surface blocked. Do not infer approval from this packet.

Suggested phrase:

```text
Approve Google Shopping parent-outfit reduced-scope activation only: using the passed reduced activation-review gate GOOGLE_SHOPPING_PARENT_OUTFIT_REDUCED_ACTIVATION_REVIEW_GATE_20260521T132011Z.md, activate only the already-built paused parent-outfit V2 Shopping campaign/ad-group/product-ad structures for the 4370 candidate ready-label in-stock rows, keeping the exact 141 unresolved-offer rows and exact 20 out-of-stock rows held out. Do not change Merchant feeds/sources, trigger Google & YouTube sync, change Shopify products/publications/inventory/prices/titles/handles/SEO, change budgets, change bids, change conversion goals, change billing, broaden product scope, reset sources, or alter held-out rows. Capture before-state and after-state readbacks and stop immediately after activation readback.
```

## Still Not Approved

- Do not activate or unpause without fresh owner approval.
- Do not change budget, bid, product group, campaign structure, conversion, billing, Merchant source/feed, Shopify product data, Shopify inventory, publication, Google & YouTube sync, source reset, broad sync, or held-out scope.
- Do not include the `141` unresolved-offer rows or the `20` out-of-stock rows in an activation surface until a separate repair/readback proves them clean.

## Evidence

- `google_shopping_parent_outfit_reduced_activation_review_gate_20260521T132011Z.json`
- `google_shopping_parent_outfit_reduced_activation_review_candidates_20260521T132011Z.csv`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_REDUCED_ACTIVATION_REVIEW_GATE_20260521T132011Z.md`
- `google_shopping_parent_outfit_ready_products_20260521T131716Z.csv`
- `google_shopping_parent_outfit_merchant_feed_gate_20260521T131716Z.json`
