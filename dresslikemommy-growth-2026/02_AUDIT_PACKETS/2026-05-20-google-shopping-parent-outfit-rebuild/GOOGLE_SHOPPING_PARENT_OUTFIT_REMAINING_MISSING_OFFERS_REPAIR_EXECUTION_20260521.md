# Google Shopping Parent-Outfit Remaining Missing Offers Repair Execution

UTC execution window: `2026-05-21T08:58Z` to `2026-05-21T09:12Z`

## Approval

Owner pasted the exact remaining missing-offer primary-source repair approval phrase.

No Shopping activation, unpause, budget, bid, status, product-group, conversion, billing, title, price, handle, body, SEO, inventory, variant, Merchant source, or broad Google & YouTube sync change was made.

## Before-State Gate

Latest pre-repair gate:

- File: `google_shopping_parent_outfit_merchant_feed_gate_20260521T085123Z.json`
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

## Shopify Readback

Evidence files:

- `google_shopping_remaining_missing_offer_shopify_before_20260521T085853Z.json`
- `google_shopping_remaining_missing_offer_shopify_before_20260521T085903Z.json`
- `google_shopping_remaining_missing_offer_shopify_after_20260521T085903Z.json`
- `google_shopping_remaining_missing_offer_repair_execution_20260521T085903Z.json`

Readback summary:

- Approved parent products: `8`
- Missing expected offer IDs in scope: `141`
- Products active: `8`
- Products already published to Google & YouTube: `8`
- Missing expected variants present in Shopify: `141`
- Missing expected variants absent from Shopify: `0`
- Blocking precheck reasons: `0`

## Repair Executed

The only narrow product-level Shopify Admin action available through the API was an idempotent Google & YouTube publication resync:

- Mutation: Shopify Admin GraphQL `publishablePublish`
- Publication: `gid://shopify/Publication/21969633377` / Google & YouTube
- Target products: the same 8 approved Mommy & Me parent products only
- Mutation calls: `8`
- Shopify `userErrors`: `0`

Because all 8 products were already published to Google & YouTube, the publish dates did not advance. No wider account sync, source reset, product recreation, product-field mutation, variant mutation, inventory mutation, or Merchant source update was attempted.

## After-State Gate Polls

The gate was rerun after the narrow repair and during a bounded processing wait:

| Gate timestamp | Expected | Ready | Missing | Label mismatches | Image mismatches | Bad catchalls | V2/old paused |
|---|---:|---:|---:|---:|---:|---:|---|
| `20260521T085925Z` | `4,531` | `4,390` | `141` | `0` | `0` | `0` | `true` |
| `20260521T090029Z` | `4,531` | `4,390` | `141` | `0` | `0` | `0` | `true` |
| `20260521T090133Z` | `4,531` | `4,390` | `141` | `0` | `0` | `0` | `true` |
| `20260521T090237Z` | `4,531` | `4,390` | `141` | `0` | `0` | `0` | `true` |
| `20260521T090341Z` | `4,531` | `4,390` | `141` | `0` | `0` | `0` | `true` |
| `20260521T090808Z` | `4,531` | `4,390` | `141` | `0` | `0` | `0` | `true` |
| `20260521T091012Z` | `4,531` | `4,390` | `141` | `0` | `0` | `0` | `true` |
| `20260521T091217Z` | `4,531` | `4,390` | `141` | `0` | `0` | `0` | `true` |

## Result

The narrow approved repair executed cleanly, but the live gate did not move during the bounded wait.

Current result:

- Gate passed: `false`
- Ready rows: `4,390 / 4,531`
- Remaining missing expected rows: `141`
- Label/image/catchall checks: clean on ready rows
- All V2 Shopping campaigns remain paused
- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` remains paused
- Activation discussion remains blocked

## Follow-Up Attribute Repair And Upload Attempt

After the owner approved the updated exact remaining-missing-offer phrase, the narrow Shopify Google & YouTube attribute repair was executed for the same approved `141` missing expected offer IDs:

- Script: `run_google_shopping_remaining_missing_offer_attribute_repair.py --apply`
- Changed namespace: `mm-google-shopping`
- Changed keys: `age_group`, `size`
- Scoped variant rows: `141`
- Planned/applied metafield updates: `278`
- Applied batches: `12`
- Shopify mutation user errors: `0`
- After-plan file: `google_shopping_remaining_missing_offer_attribute_after_20260521T091231Z.csv`
- Summary file: `google_shopping_remaining_missing_offer_attribute_repair_summary_20260521T091231Z.json`

The latest post-attribute-repair read-only gate remained closed:

- File: `google_shopping_parent_outfit_merchant_feed_gate_20260521T092023Z.json`
- Gate passed: `false`
- Expected rows: `4,531`
- Ready rows: `4,390`
- Missing expected rows: `141`
- Label mismatches: `0`
- Image mismatches: `0`
- Bad catchall units: `0`
- V2 campaigns paused: `true`
- Old test campaign paused: `true`

The approved Merchant source refresh for source `10663204023` was prepared in the authenticated Merchant Center page, and the upload dialog opened for the approved file `google_shopping_parent_outfit_merchant_supplemental_update_20260520.tsv`. The Chrome extension file-chooser path failed before transmission with `fileChooser.setFiles failed` / `Not allowed`, so the TSV was not uploaded in this follow-up attempt. No Merchant source reset, broad sync, product recreation, campaign edit, activation, budget, bid, product-group, conversion, or billing change occurred.

## Next Step

Do not broaden into an account-level Google & YouTube sync, Merchant source reset, product deletion/recreation, product-field edit, campaign/product-group change, or activation without a separate explicit approval.

The only remaining approved-but-not-executed action is the existing-source Merchant supplemental refresh from the approved TSV. The current blocker is local Chrome file-upload permission, not a feed-scope decision. After file upload capability is restored, upload only the approved TSV to source `10663204023`, wait for processing, and rerun the counts/images/no-catchall gate. If it still remains `4,390 / 4,531`, do not repeat Shopify resync; diagnose the Merchant/Google & YouTube eligibility surface or prepare the next exact repair/exclusion packet before any activation discussion.
