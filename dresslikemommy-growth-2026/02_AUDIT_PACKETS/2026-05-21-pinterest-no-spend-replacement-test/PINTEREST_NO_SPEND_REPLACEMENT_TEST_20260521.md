# Pinterest No-Spend Replacement Test - 2026-05-21

## Scope

Owner instruction: do not restart. Use a no-spend replacement test, and require fresh approval before any rebuild or restart.

This packet is local/read-only. No Pinterest campaign, ad group, product group, feed, budget, bid, tracking, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM write occurred.

## Current Safety State

- Campaign: `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520`
- Campaign ID: `626758581530`
- Current status: `Paused`
- Serving readback from prior approved pause: `0 currently being served`
- Restart status: blocked until product-group replacement is clean and owner gives fresh approval.

## Failed Path: Parent-Only Source

Parent-only source:

- Source ID: `3041760889836768751`
- Source name: `DLM US Paid Parent Collection Intent 2026-05-20`
- Feed route: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-paid-parent-feed.tsv`
- Feed rows: `210`
- Local lane counts: Mommy `99`, Family `77`, Daddy `34`
- May 21 scheduled ingestion: `Completed`, `210 of 210`, `210` successful uploads, `0` failed, `0` warnings, images `Completed`

Why it is not restart-safe:

- Auto-created `All Products` product group `4673019642691` shows `0`.
- Saved product groups `4673019642885`, `4673019642929`, and `4673019642938` still evaluate correct filters as `0 products selected`.
- Catalog Products search for a served parent item ID such as `shopify_us_parent_7230180884577` returns `0`.
- Working diagnosis: Pinterest accepted synthetic parent-only rows at ingestion level but did not materialize them into the catalog Products/Product Groups index, likely because they collide or merge with existing variant-source products by Shopify parent `item_group_id` and/or duplicate product URL.

## Replacement Test Result: Full Grouped Source

Full grouped source:

- Source ID: `3041760873378113572`
- Source name: `DLM Cloudflare Grouped Feed 2026-05-18`
- Feed route: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`
- Worker body SHA used for local no-spend test: `b76539eb641fede467bd6a572f90689c5b1bbff12edd8707fc202c87b4f1b1c0`
- Worker rows used for local no-spend test: `28,122`

Pinterest catalog materialization readback:

- Auto-created `All Products` group `4673019439386`: `28,002` products, nonzero preview, `Promote` visible.
- Existing full-source label groups are nonzero:
  - `DLM_PIN_US_LABEL_MOMMY_ME_20260520` / `4673019642205`: `1,523` products
  - `DLM_PIN_US_LABEL_FAMILY_MATCHING_20260520` / `4673019642201`: `2,892` products
  - `DLM_PIN_US_LABEL_PAJAMAS_20260520` / `4673019642195`: `252` products
- These existing label groups are not the recommended final replacement because their filters use broad `custom_label_1` values, not the exact collection-intent lane filters.

Local exact lane validation from the full grouped feed:

| Intended paid lane | Exact filter | Variant rows | Unique parents | In-stock rows | Parents with at least 1 in-stock row |
|---|---:|---:|---:|---:|---:|
| Mommy & Me | `custom_label_0=us`, `custom_label_2=mommy_and_me`, `custom_label_4=collection_intent_v20260520` | `1,419` | `99` | `1,418` | `99` |
| Family Matching | `custom_label_0=us`, `custom_label_2=family_matching`, `custom_label_4=collection_intent_v20260520` | `2,590` | `77` | `2,571` | `77` |
| Daddy & Me | `custom_label_0=us`, `custom_label_2=daddy_and_me`, `custom_label_4=collection_intent_v20260520` | `522` | `34` | `522` | `34` |

Interpretation:

- Pinterest will show variant-row selector counts for the full grouped source, not parent counts.
- The business validation count must therefore be unique `item_group_id` parents: `99 / 77 / 34`.
- This path avoids the parent-only materialization failure because Pinterest already sees variant products from source `3041760873378113572`.

## Approved No-Spend Live Preview Attempt - 2026-05-21 05:18 EDT

Owner gave fresh approval to create or preview the three exact full-source groups, verify nonzero Pinterest counts, independently validate `99/77/34` parent counts, confirm previews/URLs render, and stop before any restart.

Live Pinterest readback:

- Full grouped source `3041760873378113572` source detail is clean: current ingestion `Completed`, `28,122` product count, `28,122 of 28,122`, `0` failed uploads, `0` warnings, images `Completed`, latest ingestion `May 21 at 3:03 AM EDT`.
- Exact Mommy & Me preview using `custom_label_0=us`, `custom_label_2=mommy_and_me`, and `custom_label_4=collection_intent_v20260520` returned `0 products selected`, `0 products in stock`, and no rendered product preview rows.
- The `Create product group` button was disabled for the exact Mommy & Me preview, so no exact full-source product group was created.
- Because the first exact full-source lane failed the required nonzero Pinterest selector-count gate, the test stopped before creating any product group and before touching any campaign/ad group.

Local feed revalidation during the same attempt still passed:

- Worker body SHA: `b76539eb641fede467bd6a572f90689c5b1bbff12edd8707fc202c87b4f1b1c0`
- Worker rows: `28,122`
- Exact local lane counts remain Mommy & Me `1,419` variant rows / `99` unique parents, Family Matching `2,590` / `77`, Daddy & Me `522` / `34`.

Conclusion:

- The full-source path is not restart-safe yet. Local feed labels are correct, but Pinterest's live product-group filter index does not currently return nonzero products for the exact `custom_label_2` + `custom_label_4` lane filter.
- Do not create replacement groups, attach product groups, restart, or spend from this structure until Pinterest exact filters return nonzero preview/product-group counts and rendered product URLs.

## Recommended No-Spend Replacement Gate - Superseded By Failed Live Preview

Use the full grouped source, but only with exact collection-intent filters:

- `custom_label_0=us`
- `custom_label_2=mommy_and_me` / `family_matching` / `daddy_and_me`
- `custom_label_4=collection_intent_v20260520`

Before any restart, a future approved recovery step should:

1. Re-diagnose why Pinterest's live product-group filter index returns zero for the exact labels even though the current Worker feed contains the rows.
2. Create or preview only those three exact full-source product groups after the exact preview is nonzero.
3. Independently validate exported/item-readback IDs collapse to unique parent counts `99 / 77 / 34` by `item_group_id`.
4. Confirm preview rows and product URLs render.
5. Stop. Do not restart until separate owner approval.

## Approval Boundary

No rebuild or restart is approved by this packet.

Fresh approval is required for any external write, including:

- creating replacement product groups,
- creating/replacing an ad group,
- reattaching product groups,
- changing campaign/ad group status,
- changing budget, bid, tracking, feed, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM.

Suggested exact next approval packet, if the owner wants the next write later:

`APPROVE PINTEREST NO-SPEND FULL-SOURCE PRODUCT-GROUP TEST ONLY: under catalog 3041764155561548387 and full grouped source 3041760873378113572, create or preview only three replacement product groups using filters custom_label_0=us, custom_label_2=mommy_and_me/family_matching/daddy_and_me, and custom_label_4=collection_intent_v20260520; verify nonzero Pinterest selector counts and independently validate unique item_group_id parent counts 99/77/34; do not attach to a campaign/ad group, do not restart, do not change budget, bid, tracking, feed, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM; stop after readback.`
