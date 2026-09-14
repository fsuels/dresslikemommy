# Google Shopping Parent-Outfit Eligibility Cleanup Approval Packet

Generated: 2026-05-21

Mode: approval packet only. No Merchant, Shopify, Google & YouTube, Google Ads, campaign, product group, budget, bid, status, conversion, billing, feed, product-data, inventory, source reset, broad sync, or activation write is authorized by this document.

## Why This Packet Exists

The read-only eligibility diagnostic narrowed the parent-outfit blocker:

- `not_eligible_in_any_campaign` appears on the found expected items because no active campaign is advertising them. That is expected while all V2 Shopping campaigns remain paused.
- The hard product-scope blockers are now:
  - `71` expected offer IDs absent from the Google Ads Shopping-product surface.
  - `20` expected offer IDs with `not_eligible_out_of_stock`.
- Labels/images/catchalls are not the current failure: latest gate still shows `0` label mismatches, `0` image mismatches, `0` missing live images, and `0` bad catchalls.

Evidence: `GOOGLE_SHOPPING_PARENT_OUTFIT_ELIGIBILITY_DIAGNOSTIC_READBACK_20260521.md`.

## Recommended Next Step

Do one narrow cleanup pass before any activation discussion:

1. Read back the exact `71` absent offer IDs in Shopify Admin and Google & YouTube/Merchant surfaces where available.
2. If the absent rows still exist in Shopify and are Google & YouTube published, repair only their narrow Merchant/Google & YouTube presence using the smallest exposed control surface. Stop if the only available path is broad account sync, source reset, product recreation, or campaign change.
3. Read back the exact `20` out-of-stock offer IDs. If they are still out of stock, exclude only those offer IDs from the parent-outfit ready scope until inventory/availability is corrected.
4. Rerun the counts/images/no-catchall gate.

This packet does not authorize activation, unpausing, or spend.

## Approval Phrase

If approved, paste this exact phrase:

```text
Approve Google Shopping parent-outfit eligibility cleanup only: keep all Shopping V2 campaigns paused and keep DLM_US_STANDARD_SHOPPING_TEST_PAID_READY paused; inspect and repair only the Merchant/Google & YouTube presence for the 71 diagnosed absent parent-outfit offer IDs if a narrow product-level control surface is available, exclude only the 20 diagnosed out-of-stock offer IDs from parent-outfit ready scope if they still read out of stock, do not change titles/prices/handles/body/SEO/images/inventory except for that exact out-of-stock exclusion scope, do not upload or resync the full TSV again, do not trigger broad account sync/source reset/product recreation, do not change campaigns/product groups/budgets/bids/statuses/conversions/billing, stop if a narrow path is unavailable, and rerun the counts/images/no-catchall gate before any activation discussion.
```

## Included Absent Offer Scope

| Parent product ID | Handle | Lane | Subgroup | Absent offer IDs |
|---|---|---|---|---:|
| `7562834215009` | `white-crochet-mommy-and-me-set` | `mommy_and_me` | `sets` | `35` |
| `6718945034337` | `mom-child-matching-two-piece-swimsuit` | `mommy_and_me` | `swimwear` | `20` |
| `6719774720097` | `matching-mommy-me-orange-print-swimsuit` | `mommy_and_me` | `swimwear` | `10` |
| `7227254276193` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | `mommy_and_me` | `dresses` | `6` |

## Included Out-Of-Stock Scope

| Parent product ID | Handle | Lane | Subgroup | Out-of-stock offer IDs |
|---|---|---|---|---:|
| `7230645239905` | `eternal-love-family-matching-t-shirts-colorful-heart-design` | `family_matching` | `tops_shirts` | `15` |
| `7537367679073` | `playful-graphic-family-matching-tops` | `family_matching` | `tops_shirts` | `3` |
| `7537367384161` | `red-plaid-family-matching-tops` | `family_matching` | `tops_shirts` | `1` |
| `7546613530721` | `golden-daisy-mommy-and-me-set` | `mommy_and_me` | `tops_shirts` | `1` |

## Still Blocked Without Separate Approval

- No Shopping activation or unpause.
- No spend, budget, bid, status, product-group, campaign, conversion, or billing change.
- No full TSV upload/resync loop.
- No broad Merchant source reset, fetch trigger, account sync, or product recreation.
- No Shopify title, price, body, handle, SEO, image, inventory, product, publication, or variant edit outside the exact approved cleanup scope.

## Expected After-State Readback

After any approved cleanup:

- All V2 Shopping campaigns still paused.
- Old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` still paused.
- Counts/images/no-catchall gate rerun.
- Evidence must show:
  - remaining expected rows;
  - ready-label rows;
  - missing expected rows;
  - label mismatches;
  - image mismatches;
  - missing live images;
  - bad catchall units;
  - any intentionally excluded offer IDs and reason.

