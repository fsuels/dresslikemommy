# Pinterest Exact-Label Index Diagnosis - 2026-05-21

## Scope

Owner direction: keep campaign `626758581530` paused; diagnose why Pinterest indexes broad full-source groups but returns zero for exact `custom_label_2` + `custom_label_4`; if needed, move to a truly separate catalog/source structure where parent rows do not collide with existing variant records.

This packet is read-only/local-only. No Pinterest catalog, source, product group, campaign, ad group, budget, bid, tracking, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM write occurred.

## Current Safety State

- Campaign `626758581530` remains paused from the prior approved safety pause.
- No replacement product group is spend-safe yet.
- Do not restart, attach product groups, or use the broad groups.

## Evidence

### Full grouped source is clean but exact live preview fails

Live source readback for `3041760873378113572`:

- Source name: `DLM Cloudflare Grouped Feed 2026-05-18`
- Current ingestion: `Completed`
- Product count: `28,122`
- Current ingestion row: `28,122 of 28,122`
- Latest ingestion: `May 21 at 3:03 AM EDT`
- Failed uploads: `0`
- Warnings: `0`
- Images: `Completed`

Local Worker feed readback:

- Worker SHA: `b76539eb641fede467bd6a572f90689c5b1bbff12edd8707fc202c87b4f1b1c0`
- Data rows: `28,122`
- `custom_label_0=us`, lane `custom_label_2`, and `custom_label_4=collection_intent_v20260520` local counts:

| Lane | Variant rows | Unique `item_group_id` parents | In-stock rows | Parents with at least 1 in-stock row |
|---|---:|---:|---:|---:|
| `mommy_and_me` | `1,419` | `99` | `1,418` | `99` |
| `family_matching` | `2,590` | `77` | `2,571` | `77` |
| `daddy_and_me` | `522` | `34` | `522` | `34` |

Pinterest live product-group builder readback:

- Exact Mommy & Me filter `custom_label_0=us` + `custom_label_2=mommy_and_me` + `custom_label_4=collection_intent_v20260520` returned `0 products selected`, `0 products in stock`, no preview rows, and disabled `Create product group`.
- This same exact-filter gate had returned `1,419` variant rows on May 20 after the first collection-intent ingestion, so the current failure is not explained by missing local rows.

### Broad groups still work, but are not approved

Full-source broad groups remain nonzero:

| Existing broad group | Count | Why not approved |
|---|---:|---|
| `DLM_PIN_US_LABEL_MOMMY_ME_20260520` / `4673019642205` | `1,523` | Uses broad `custom_label_1` categories, not collection-intent lanes |
| `DLM_PIN_US_LABEL_FAMILY_MATCHING_20260520` / `4673019642201` | `2,892` | Uses broad `custom_label_1` categories, not collection-intent lanes |
| `DLM_PIN_US_LABEL_PAJAMAS_20260520` / `4673019642195` | `252` | Not part of the approved three-lane parent structure |

### Parent-only source collision evidence

The parent-only source `3041760889836768751` also ingested cleanly, but later product groups showed zero. Local collision analysis explains why a same-catalog parent-only source is unsafe:

| Check against full variant source | Parent-only source result |
|---|---:|
| Parent-only rows | `210` |
| `id` lower-case collisions | `0` |
| `item_group_id` collisions | `210 / 210` |
| Exact `link` collisions | `210 / 210` |

Interpretation: the parent-only source had new item IDs, but it reused the same Shopify parent `item_group_id` and the same canonical PDP URLs as the variant source inside the same Pinterest catalog. Pinterest appears to merge or cross-index products at catalog level, so a clean ingestion can still fail the catalog Products/Product Groups materialization gate.

## Diagnosis

The local feed math is correct. The live Pinterest catalog index is the broken layer.

Most likely cause:

- Multiple data sources in the same Pinterest catalog describe the same Dress Like Mommy products with overlapping Shopify parent identity and PDP URLs.
- Pinterest canonicalizes or merges catalog records across those feeds.
- The full source still has products, and broad `custom_label_1` groups still work, but the newer exact collection-intent labels in `custom_label_2` / `custom_label_4` are not reliably attached to the materialized product records used by the product-group builder.
- The parent-only source failed for the same reason at a higher severity: its parent rows collided with variant records by `item_group_id` and `link`, so the source could show clean ingestion while product groups evaluated to zero.

## Local Isolated Candidate

Created a local-only candidate parent feed that removes all direct collisions against the current full variant source:

- Candidate file: `pinterest_us_paid_parent_isolated_candidate.tsv`
- Candidate summary: `pinterest_us_paid_parent_isolated_candidate.summary.json`
- Candidate rows: `210`
- SHA: `db2fcddaa95609ccade30b5af11d3edd9d90e35c10f2d011b24fc4b57dce8113`
- Label version: `collection_intent_parent_isolated_v20260521`

Candidate lane counts:

| Lane | Rows | Unique isolated `item_group_id` |
|---|---:|---:|
| `mommy_and_me` | `99` | `99` |
| `family_matching` | `77` | `77` |
| `daddy_and_me` | `34` | `34` |

Candidate collision checks against full source:

| Collision type | Count |
|---|---:|
| Lower-case `id` collisions | `0` |
| `item_group_id` collisions | `0` |
| Exact `link` collisions | `0` |
| Duplicate candidate IDs | `0` |
| Missing `item_group_id` | `0` |
| Missing `image_link` | `0` |

How it avoids collisions:

- `id` is namespaced as `dlm_paid_us_parent_<lane>_<parent_id>`.
- `item_group_id` is namespaced the same way.
- `link` stays on the same public PDP but includes paid-parent tracking parameters so it does not exactly equal the variant-source PDP URL.
- `custom_label_4` is a new isolated version: `collection_intent_parent_isolated_v20260521`.

## Recommendation

Expert setup now is not another same-catalog group rebuild. The cleanest next move is a separate Pinterest paid-parent catalog, or if Pinterest account limits block a separate catalog, a separate isolated source that uses collision-free IDs, `item_group_id`, and links.

Preferred next approved path:

1. Create a separate Pinterest paid-parent catalog for Dress Like Mommy US parent collections.
2. Add one URL source using the isolated candidate feed.
3. Wait for clean ingestion: `210` successful, `0` failed, `0` warnings, images completed.
4. Create three product groups from `custom_label_0=us`, `custom_label_2=mommy_and_me/family_matching/daddy_and_me`, and `custom_label_4=collection_intent_parent_isolated_v20260521`.
5. Verify product-group selector counts `99/77/34`, preview rows, image rendering, and PDP URLs.
6. Stop. Do not attach to campaign/ad group or restart until separate approval.

Fallback if a separate catalog is not available:

1. Use the isolated candidate feed as a new source, not the old parent-only source.
2. Keep all IDs, `item_group_id`, links, and label version collision-free.
3. Apply the same count/preview/readback gate before any campaign attachment.

## Approved No-Spend Test Preparation - 2026-05-21

Owner gave fresh approval to test a separate no-spend Pinterest paid-parent catalog/source from the isolated 210-row feed, verify clean ingestion plus selector counts `99/77/34`, and stop before any campaign/ad-group attachment or restart.

Completed feed-hosting preparation:

- Uploaded isolated candidate feed to R2 object `dlm-pinterest-feeds/pinterest/pinterest_us_paid_parent_isolated_candidate.tsv`.
- Deployed Worker version `0e9a95d4-32e6-4ecd-a453-09bd86c8870d` with a new isolated URL route.
- Public feed URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-paid-parent-isolated-feed.tsv`

Public route readback:

| Check | Result |
|---|---:|
| HTTP status | `200` |
| `X-DLM-Feed-Object-Key` | `pinterest/pinterest_us_paid_parent_isolated_candidate.tsv` |
| `X-DLM-Feed-Rows` | `210` |
| `X-DLM-Feed-Sha256` | `db2fcddaa95609ccade30b5af11d3edd9d90e35c10f2d011b24fc4b57dce8113` |
| Downloaded line count | `211` |
| Downloaded SHA | `db2fcddaa95609ccade30b5af11d3edd9d90e35c10f2d011b24fc4b57dce8113` |

Downloaded route lane readback:

| Lane | Rows |
|---|---:|
| `mommy_and_me` | `99` |
| `family_matching` | `77` |
| `daddy_and_me` | `34` |

Worker verification:

- `npm test` under `ops/cloudflare/pinterest-feed-worker` passed `14/14`, including the new isolated route, app-proxy-style isolated route, and non-GET fail-closed checks.

Account-side blocker:

- Chrome/Pinterest UI automation could not continue because the Codex Chrome extension bridge returned `Browser is not available: extension`.
- Retry after two seconds returned the same failure.
- Recovery checks showed Chrome is installed/running, the Codex Chrome Extension is installed and enabled, and the native host manifest is correct.
- Because the extension/native-host checks passed but communication still failed, the Chrome skill required owner permission before opening a Chrome window for the selected profile and retrying the connection.
- Owner approved that recovery step. Opening a Chrome window for selected profile `Profile 1` succeeded, but the retry still returned `Browser is not available: extension`.
- Per the Chrome recovery workflow, the next fix is to reinstall or repair the Codex Chrome Extension/plugin from the Codex plugin UI before another Pinterest UI attempt.

No Pinterest catalog/source/product-group was created yet from the isolated route. No campaign/ad-group attachment, restart, campaign status, budget, bid, tracking, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM change occurred.

### Owner-Completed Pinterest Source Creation

Owner manually completed the no-spend URL source creation after the Chrome bridge blocker:

- Source name: `DLM US Paid Parent Isolated 2026-05-21`
- Data source ID: `3041760890485574219`
- Feed URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-paid-parent-isolated-feed.tsv`
- Format: `TSV`
- Country: `United States`
- Language: `English (US)`
- Currency: `USD`
- Reported status: `Processing`
- Reported ingestion start: `May 21, 2026 at 6:12 AM EDT`

Owner confirmed it is not attached to any campaign or ad group, and nothing was restarted.

Next gate:

- Poll source `3041760890485574219`.
- Proceed only if ingestion completes cleanly with `210` successful uploads, `0` failed uploads, `0` warnings, and images completed.
- Then create or preview only the three isolated product groups:
  - `custom_label_0=us` + `custom_label_2=mommy_and_me` + `custom_label_4=collection_intent_parent_isolated_v20260521`, expected `99`
  - `custom_label_0=us` + `custom_label_2=family_matching` + `custom_label_4=collection_intent_parent_isolated_v20260521`, expected `77`
  - `custom_label_0=us` + `custom_label_2=daddy_and_me` + `custom_label_4=collection_intent_parent_isolated_v20260521`, expected `34`
- Stop before any campaign/ad-group attachment or restart.

### Isolated Source And Product-Group Readback

Chrome bridge recovered in the `test` profile. Completed the approved no-spend source/product-group gate only.

Source readback for `3041760890485574219`:

| Check | Readback |
|---|---:|
| Source name | `DLM US Paid Parent Isolated 2026-05-21` |
| Current ingestion | `Completed` |
| Product count | `210` |
| Successful uploads | `210 of 210` |
| Failed uploads | `0` |
| Warnings | `0` |
| Images | `Completed` |
| Ingestion time | `May 21 at 6:12 AM EDT` |

Created and verified isolated product groups:

| Product group | ID | Filter | Preview count before save | Detail/list count after save |
|---|---:|---|---:|---:|
| `DLM_PIN_US_ISOLATED_PARENT_MOMMY_AND_ME_99_20260521` | `4673019914864` | `custom_label_0=us`, `custom_label_2=mommy_and_me`, `custom_label_4=collection_intent_parent_isolated_v20260521` | `99` | `99` |
| `DLM_PIN_US_ISOLATED_PARENT_FAMILY_MATCHING_77_20260521` | `4673019915037` | `custom_label_0=us`, `custom_label_2=family_matching`, `custom_label_4=collection_intent_parent_isolated_v20260521` | `77` | `77` |
| `DLM_PIN_US_ISOLATED_PARENT_DADDY_AND_ME_34_20260521` | `4673019915140` | `custom_label_0=us`, `custom_label_2=daddy_and_me`, `custom_label_4=collection_intent_parent_isolated_v20260521` | `34` | `34` |

Preview/readback notes:

- Each group detail page shows data source `DLM US Paid Parent Isolated 2026-05-21`.
- Each group detail page rendered in-stock product rows with isolated `dlm_paid_us_parent_*` item IDs.
- The auto-created `All Products` group remains source-level only at `210`.
- Heartbeat automation `pinterest-isolated-source-poll` was deleted after the gate completed.

Stop state:

- No campaign/ad-group attachment occurred.
- Campaign `626758581530` was not restarted.
- No campaign status, budget, bid, tracking, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM change occurred.

## Approval Boundary

No move, source upload, catalog creation, product-group creation, campaign attachment, or restart is approved by this diagnosis.

Suggested exact next approval phrase:

`APPROVE PINTEREST ISOLATED PAID-PARENT CATALOG TEST ONLY: create a separate no-spend Pinterest paid-parent catalog/source test using the local isolated 210-row parent feed with collision-free id, item_group_id, link, and custom_label_4=collection_intent_parent_isolated_v20260521; wait for clean ingestion; create or preview only three product groups for custom_label_0=us and custom_label_2=mommy_and_me/family_matching/daddy_and_me; verify selector counts 99/77/34 plus rendered previews and PDP URLs; do not attach to campaign/ad group, do not restart, do not change campaign status, budget, bid, tracking, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM; stop after readback.`
