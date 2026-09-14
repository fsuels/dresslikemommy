# Google Shopping Remaining Missing Offers Attribute Repair Execution

UTC execution window: `2026-05-21T09:12:16Z` to `2026-05-21T09:18:55Z`

## Scope

Owner-approved remaining missing-offer repair stayed limited to:

- `8` diagnosed Mommy & Me parent products.
- `141` missing expected offer IDs.
- Shopify Google & YouTube / Merchant source attributes only.

No campaign activation, budget, bid, status, product-group, conversion, billing, title, price, handle, body, SEO, inventory, broad source reset, account sync, or product recreation was performed.

## What Was Found

The earlier Google & YouTube publication resync was not enough because Shopify Admin product feedback still showed Google & YouTube demotion messages on the affected products. The concrete blocker was missing Google Shopping apparel attributes, mainly `age_group`, plus `size` on the scoped variants.

Dry-run plan:

- Scoped variant rows: `141`
- Planned variant rows: `141`
- Planned metafield updates: `278`
- Fields:
  - `mm-google-shopping.age_group`: `137`
  - `mm-google-shopping.size`: `141`
- Desired age groups:
  - `adult`: `61`
  - `kids`: `57`
  - `toddler`: `23`

## Repair Executed

Script:

- `run_google_shopping_remaining_missing_offer_attribute_repair.py`

Mutation:

- Shopify Admin GraphQL `metafieldsSet`
- Owner objects: only the `141` scoped `ProductVariant` IDs from the missing-offer CSV.
- Namespace: `mm-google-shopping`
- Keys: `age_group`, `size`

Execution readback:

- Attempted metafield updates: `278`
- Applied batches: `12`
- Shopify user errors: `0`
- After-plan rows already correct: `141 / 141`

After the attribute repair, the narrow Google & YouTube `publishablePublish` resync was rerun for the same `8` products:

- Repair attempted: `true`
- Shopify user errors: `0`
- Blocking reasons: `[]`

## Gate Rerun

After a bounded processing wait, the parent-outfit Merchant/feed gate was rerun read-only:

- Gate file: `google_shopping_parent_outfit_merchant_feed_gate_20260521T091855Z.json`
- Gate passed: `false`
- Expected rows: `4,531`
- Ready rows: `4,390`
- Missing expected rows: `141`
- Label mismatches: `0`
- Image mismatches: `0`
- Missing live images: `0`
- Bad catchall units: `0`
- V2 campaign status ok: `true`
- Old test campaign paused: `true`

## Conclusion

The scoped Shopify/Google & YouTube source-side repair is complete and verified locally: all `141` missing variants now have the intended Google age/size source attributes. The live Google Ads Shopping-product surface has not propagated those offers yet, so activation remains blocked.

The existing heartbeat `rerun-google-shopping-parent-outfit-gate` was updated to poll the gate every `30` minutes read-only. If the gate still reads `4,390 / 4,531`, do not repeat this repair. Continue read-only polling, or request a fresh explicit approval only if a broader Google & YouTube/Merchant control surface or eligible-scope exclusion is required.

## Evidence

- `google_shopping_remaining_missing_offer_attribute_plan_20260521T091216Z.csv`
- `google_shopping_remaining_missing_offer_attribute_repair_summary_20260521T091216Z.json`
- `google_shopping_remaining_missing_offer_attribute_plan_20260521T091231Z.csv`
- `google_shopping_remaining_missing_offer_attribute_after_20260521T091231Z.csv`
- `google_shopping_remaining_missing_offer_attribute_feedback_20260521T091231Z.json`
- `google_shopping_remaining_missing_offer_attribute_repair_summary_20260521T091231Z.json`
- `google_shopping_remaining_missing_offer_repair_execution_20260521T091343Z.json`
- `google_shopping_remaining_missing_offer_shopify_after_20260521T091343Z.json`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_GATE_READBACK_20260521T091855Z.md`
- `google_shopping_parent_outfit_merchant_feed_gate_20260521T091855Z.json`
