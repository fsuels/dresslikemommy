# Google Shopping Parent-Outfit Eligibility Control-Surface Approval Packet

Generated: `2026-05-21T09:17:43Z`

Mode: approval packet only. No Merchant, Shopify, Google & YouTube, Google Ads, campaign, product group, budget, bid, status, conversion, billing, feed, product-data, or activation write is authorized by this document.

## Why This Packet Exists

The exact-approved narrow Google & YouTube publication resync ran cleanly, but it did not move the parent-outfit Shopping gate. A delayed read-only rerun at `20260521T091743Z` still failed closed.

The result changed the diagnosis:

- The blocker is no longer label precedence.
- The narrow `publishablePublish` resync is disproven as the fix.
- A simple scope-down activation is not clean, because the `4,390` live labeled rows all read `shopping_product.status=NOT_ELIGIBLE`.
- Strict live `item_group_id` proof is still unavailable because the current Google token does not have Merchant Content API scope.

## Latest Read-Only Gate Result

Evidence:

- `google_shopping_parent_outfit_merchant_feed_gate_20260521T091743Z.json`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_GATE_READBACK_20260521T091743Z.md`
- `google_shopping_parent_outfit_ready_products_20260521T091743Z.csv`
- `google_shopping_parent_outfit_old_us_test_ready_products_20260521T091743Z.csv`

Readback summary:

- Gate passed: `false`
- Reason: `FAIL_CLOSED__MERCHANT_FEED_LABEL_IMAGE_READBACK_NOT_LIVE`
- Expected included variant rows: `4,531`
- Live rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `4,390`
- Missing expected rows: `141`
- Unexpected ready rows: `0`
- Label mismatches: `0`
- Image mismatches: `0`
- Missing live images: `0`
- Bad catchall units: `0`
- V2 campaigns paused: `true`
- Old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused: `true`
- Merchant Content API scope available: `false`
- Ready-row status distribution: `4,390 / 4,390` are `NOT_ELIGIBLE`
- Ready-row availability distribution: `4,370` `IN_STOCK`, `20` `OUT_OF_STOCK`

Live parent counts from the spec join:

| Lane | Expected parents | Live ready parents |
|---|---:|---:|
| `mommy_and_me` | `99` | `92` |
| `family_matching` | `77` | `77` |
| `daddy_and_me` | `34` | `34` |

## Recommended Next Step

Recommended next step: run a Merchant / Google & YouTube eligibility control-surface diagnostic for the exact parent-outfit scope before any activation, scope-down launch, feed write, source reset, or broad sync.

Why this should happen first:

- It answers the current blocker instead of repeating the disproven narrow resync.
- It explains why all `4,390` live labeled rows are `NOT_ELIGIBLE`.
- It can identify whether the `141` missing rows are a source/indexing issue, a Google & YouTube publication/sync issue, a Merchant approval issue, or a product-level policy/attribute issue.
- It preserves the paid-growth guardrail: no activation or spend until the actual Merchant/Shopping eligibility issue is known.

Do not recommend activating only the `4,390` ready-label rows yet. The labels/images are clean, but `NOT_ELIGIBLE` status plus missing strict `item_group_id` proof makes that premature.

## Approval Phrase

If approved, paste this exact phrase:

```text
Approve Google Shopping parent-outfit eligibility diagnostic only: use existing authenticated Merchant Center, Google & YouTube, Shopify Admin, and Google Ads read-only surfaces to inspect/export issue, approval, status, source, item_group_id, and eligibility diagnostics for the exact 4,531 parent-outfit expected offer IDs, including the 4,390 labeled NOT_ELIGIBLE rows and the 141 missing expected rows. Do not change Merchant feeds/sources, Shopify products/publications, Google & YouTube settings, Google Ads campaigns/product groups/budgets/bids/statuses/conversions, billing, product data, labels, inventory, prices, handles, SEO, or trigger broad account sync. Stop with an evidence packet and the smallest exact repair or exclusion approval packet.
```

## Allowed If Approved

- Use existing authenticated Merchant Center, Google & YouTube, Shopify Admin, and Google Ads surfaces for read-only diagnostics.
- Export or save local evidence for the exact parent-outfit scope.
- Check issue/status/approval/source/readiness for:
  - the `4,390` currently labeled rows;
  - the `141` missing expected rows;
  - strict `item_group_id` proof if the surface exposes it;
  - product approval and Shopping eligibility reasons.
- Prepare one exact follow-up packet:
  - either a minimal repair packet naming the exact control surface and mutation;
  - or a scope-exclusion packet with updated parent counts and a clear reason each excluded item stays out.

## Still Blocked Without Separate Approval

- No Shopping campaign activation or unpause.
- No budget, bid, status, product group, campaign, conversion, or billing changes.
- No Merchant feed/source upload, source reset, fetch trigger, broad sync, or product recreation.
- No Shopify product title, price, body, handle, SEO, inventory, publication, variant, image, or Google & YouTube setting changes.
- No activation discussion until diagnostics prove the exact eligible serving scope.

## Next Best Prompt

```text
Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical operating prompt. Start from `AGENT_CONTINUITY_ANCHOR: 2026-05-21-google-shopping-parent-outfit-eligibility-diagnostic-packet`.

Recommended next action: if the owner approved the exact phrase in `GOOGLE_SHOPPING_PARENT_OUTFIT_ELIGIBILITY_CONTROL_SURFACE_APPROVAL_PACKET_20260521.md`, run only the approved read-only Merchant / Google & YouTube / Shopify Admin / Google Ads eligibility diagnostic for the exact 4,531 parent-outfit expected offer IDs, then stop with evidence and one exact repair or exclusion packet. Do not activate spend or change feeds/products/campaigns.
```
