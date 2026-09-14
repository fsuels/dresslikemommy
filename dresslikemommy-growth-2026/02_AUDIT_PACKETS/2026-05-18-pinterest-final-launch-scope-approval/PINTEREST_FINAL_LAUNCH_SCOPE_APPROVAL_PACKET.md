# Pinterest Final Launch / Scope Approval Packet

Date prepared: 2026-05-18 06:32 EDT

Status: `REVIEW_REACHED__EXACT_GROUPS_SELECTED__PUBLISH_STOPPED_FINAL_REVIEW_INCOMPLETE`

This packet is the separate final approval surface for moving from a clean Pinterest catalog source to an exact launch scope. It does not approve or execute a launch by itself.

## Execution Update

On 2026-05-18 at 06:55 EDT, owner approved proceeding under this packet. The exact product groups were created under source `3041760873378113572`:

| Product group | Product group ID | Product readback |
|---|---:|---:|
| `DLM_PIN_US_SHOPPING_MOMMY_ME_333` | `4673019468477` | 201 |
| `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333` | `4673019468479` | 103 |
| `DLM_PIN_US_SHOPPING_PAJAMAS_333` | `4673019468480` | 29 |

Launch has not started. Browser recovery completed, Pajamas detail readback passed, and the campaign flow reached Review with exact groups selected. Publish was stopped because the final Review screen did not explicitly display every approval-phrase field: it did not show `Pin clicks`, did not show `Custom`, did not show the selected data-source name directly, and still displayed Pinterest Performance+ targeting / expanded targeting language. See `PINTEREST_CAMPAIGN_REVIEW_STOP_READBACK.md`.

## Current Clean Source Readback

The repaired Cloudflare-hosted Pinterest source is clean and usable as a feed source:

- Pinterest advertiser: `549756244483`
- Pinterest catalog: `3041764155561548387`
- Current data source: `DLM Cloudflare Grouped Feed 2026-05-18`
- Current data source ID / feed profile ID: `3041760873378113572`
- Feed URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`
- Repaired TSV body SHA-256: `809d48e96832ffc4db8a30de685250273412c2988678b5364d48c627699e8863`
- Latest ingestion readback: `41,814 of 41,814`
- Past ingestion readback: `41,814` successful uploads, `0` failed, `0` warnings, `0` videos
- Images readback: completed
- Diagnostics readback: `There are no ingestion issues for this data source`
- Product groups readback: auto-created `All Products` group `4673019439386`, `41,694` products, previews load, and `Promote` is visible

Important: `All Products` visibility is only proof that the source can support product-group previews. It is not an approved launch scope.

## Approved Candidate Launch Scope

The first launch candidate remains the refreshed US active-clean whitelist from the 2026-05-15 Pinterest scope refresh:

| Scope | Expected item IDs / variants | Expected unique products within scope | Launch role |
|---|---:|---:|---|
| Mommy & Me | 201 | 26 | Exact high-intent catalog group |
| Family Matching | 103 | 7 | Exact high-intent catalog group |
| Pajamas | 29 | 1 | Exact small test group only if selectable cleanly |
| Total whitelist | 333 | 30 total unique products after overlap | Maximum approved launch inventory |

The prior `342` scope is not approved. The `9` held variants remain excluded.

## Critical Scope Constraint

The previous exact-group attempt was tied to old feed profile `3041760867124595727` and stopped because the product-group preview read back `0 products selected` / `0 products in stock`.

The clean source now available is feed profile `3041760873378113572`. Any next Pinterest launch step must create, select, or validate exact product groups under this new source only.

Do not reuse the old exact-group filter assumptions blindly. The repaired Path B feed uses grouping/repair labels, not the older `paid_eligible`, `us_test_ready`, `mommy_me`, `family_matching`, and `pajamas` custom-label launch taxonomy. Therefore the safest launch scope is:

1. Use the refreshed 333-row item-ID whitelist from `pinterest_paused_draft_refreshed_clean_scope.csv`.
2. Create or expose exact Pinterest product groups under source `3041760873378113572`.
3. Stop if Pinterest cannot prove the exact rows or exact grouped inventory before save/publish.

A later feed-label enrichment path is possible, but it would be a separate local repair/upload approval. It is not included in this launch packet.

## Required Preflight Before Any Save Or Publish

Before any future external write, the operator must read back and record:

1. Selected Pinterest advertiser is `Dress Like Mommy | Matching Family Outfits` / advertiser `549756244483`.
2. Selected catalog is `3041764155561548387`.
3. Selected source is `DLM Cloudflare Grouped Feed 2026-05-18` / source `3041760873378113572`.
4. The launch scope is exact item-ID whitelist only: Mommy & Me `201`, Family Matching `103`, Pajamas `29`, total `333`.
5. No broad `All Products`, broad Shopify collection, broad category bucket, old feed profile, or legacy source is selected as launch scope.
6. Exact group previews load with real product thumbnails and no `0 products selected` / `0 products in stock` readback.
7. Any count delta is explained before proceeding. If the exact group counts do not map to the `333` whitelist or a documented Pinterest eligibility display delta, stop.
8. Campaign objective is Catalog sales.
9. Optimization is Pin clicks.
10. Bidding is Custom, not Performance+ or automated ROAS bidding.
11. Max CPC is no more than `$0.15`.
12. Daily budget is no more than `$5/day`.
13. No campaign, ad group, ad, audience, budget, bid, status, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4/GTM, Worker metadata, or legacy-source cleanup change is made outside the exact approval.

## Recommended Approval Phrase

Use this exact phrase only if the owner wants to approve the next live-gated step:

```text
I approve creating or selecting exact Pinterest product groups under source 3041760873378113572 only, using the refreshed 333-row US active-clean item-ID whitelist split into Mommy & Me 201 variants, Family Matching 103 variants, and Pajamas 29 variants, excluding the 9 held variants and not using broad All Products, broad collection groups, old feed profile 3041760867124595727, or legacy sources. After readback confirms the exact groups are usable, I approve launching one Pinterest Catalog sales test for advertiser 549756244483 only if final review shows the selected data source is DLM Cloudflare Grouped Feed 2026-05-18, catalog 3041764155561548387, objective Catalog sales, optimization Pin clicks, Custom bidding, max CPC $0.15, daily budget max $5/day, no Performance+ bidding, no catalog/source/feed/tag/CAPI/billing/Shopify/Merchant/Google Ads/GA4/GTM changes, and no legacy source pause/remove. Stop before saving or publishing if any selector, prompt, count, budget, bid, billing, policy, permission, CAPTCHA, account switch, broad-scope, or out-of-scope condition appears.
```

## Stop Conditions

Stop immediately before saving, publishing, or launching if Pinterest shows:

- Login, CAPTCHA, account switcher, billing, permissions, policy, or legal prompt.
- A selected data source other than `3041760873378113572`.
- A scope that includes broad `All Products`, broad collection/category groups, or old feed profile `3041760867124595727`.
- Exact product groups with `0 products selected`, `0 products in stock`, missing previews, or unexplained count drift.
- Performance+ bidding, automated ROAS bidding, CPC above `$0.15`, daily budget above `$5/day`, or any spend setting not named in the approval phrase.
- Any prompt to pause, remove, replace, or clean up legacy feeds.
- Any request to change Shopify products/theme/app-proxy, Merchant, Google Ads, GA4/GTM, Pinterest tag/CAPI, billing, or Worker metadata.

## After-State Readback Plan

If and only if the owner gives the approval phrase, capture after-state evidence:

1. Exact product-group readback under source `3041760873378113572`.
2. Campaign/ad group readback showing exact scope, objective, optimization, bid, budget, and status.
3. Screenshot and DOM/text snapshot before publish.
4. Screenshot and DOM/text snapshot after publish if launch is approved and completed.
5. First serving readback after Pinterest accepts the object.
6. Worklog, action queue, current marketing state, review log, coordination, and problem tracker update.

## Sources

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-18-pinterest-gate-b3-cloudflare-source/GATE_B3_PINTEREST_CLOUDFLARE_SOURCE_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-18-pinterest-gate-b3-cloudflare-source/GATE_B3_LOCAL_FEED_REPAIR_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-paused-draft-scope-refresh/pinterest_paused_draft_refreshed_clean_scope.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-exact-product-group-unblock/PINTEREST_EXACT_PRODUCT_GROUP_ATTEMPT_STOP.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-live-launch-cpc-scope-blocker/PINTEREST_LIVE_LAUNCH_CPC_SCOPE_BLOCKER.md`
- `ops/scripts/generate_pinterest_feed_grouped.py`
