# Google Shopping Parent-Outfit Label-Precedence Repair Approval Packet

Mode: approval packet only. No additional Merchant source replacement, Shopify write, Google Ads campaign change, activation, spend, budget, bid, status, product-group, conversion, or billing write is authorized by this document.

## Why Another Repair Is Needed

The parent-outfit supplemental source `10663204023` now processes the approved TSV again:

- Total updated products: `4,531`
- Matched products: `4,390`
- Attribute names: all recognized
- Remaining missing offers: `141`

But the gate still fails because an older label source stack is still winning two fields:

- `custom_label_0` still shows `exclude_feed_issue` on many parent-outfit rows that should be `paid_eligible`.
- `custom_label_4` still shows old values like `us_test_ready` or `us_fix_before_paid` on most older rows that should be `us_parent_outfit_ready_v20260520`.

This explains why:

- `custom_label_3=parent_outfit` is live on `4,390` rows.
- The strict ready label is live on only `145` rows.
- Images and labels are clean where the strict ready label is live.
- Catchalls are still clean; this is not an Ads structure problem.

## Proposed Smallest Repair

1. Read back the current source/settings state for the older active label source(s), especially the source that last set `custom_label_0` and `custom_label_4` for `us_test_ready` / `us_fix_before_paid`.
2. Build a deterministic replacement overlay that:
   - preserves existing non-parent-outfit rows and their current label values;
   - changes only the approved parent-outfit offer IDs from `merchant_label_update_spec.csv`;
   - sets `custom_label_0=paid_eligible`;
   - sets `custom_label_1` to the parent lane (`mommy_and_me`, `family_matching`, `daddy_and_me`);
   - sets `custom_label_2` to the subgroup;
   - sets `custom_label_3=parent_outfit`;
   - sets `custom_label_4=us_parent_outfit_ready_v20260520`;
   - preserves known non-label attributes in that older source where present, such as `age_group`.
3. Upload/update only that label source or the smallest equivalent Merchant supplemental source needed to make `custom_label_0` and `custom_label_4` stop losing precedence.
4. Wait for processing.
5. Rerun the counts/images/no-catchall gate.

## Hard Boundaries

- Keep all Shopping V2 campaigns paused.
- Keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused.
- Do not enable spend.
- Do not change Google Ads budgets, bids, statuses, product groups, conversion goals, or billing.
- Do not change Shopify titles, prices, handles, body copy, SEO, inventory, or publications.
- Do not include 404, archived, unavailable, or excluded products.
- Stop on login, CAPTCHA, permission, policy, source schema, destructive, or broad-overwrite prompt.

## Exact Approval Phrase

Approve the Google Shopping parent-outfit label-precedence repair only: keep all Shopping V2 campaigns paused, keep DLM_US_STANDARD_SHOPPING_TEST_PAID_READY paused, read back the older Merchant label source state, update only the smallest Merchant supplemental label source needed so the approved parent-outfit rows win custom_label_0=paid_eligible and custom_label_4=us_parent_outfit_ready_v20260520 while preserving non-parent rows and known non-label attributes, do not change Shopify titles/prices/handles/body/SEO/inventory/publications/campaigns/budgets/bids/statuses/product groups/conversions/billing, wait for processing, and rerun the counts/images/no-catchall gate before any activation discussion.
