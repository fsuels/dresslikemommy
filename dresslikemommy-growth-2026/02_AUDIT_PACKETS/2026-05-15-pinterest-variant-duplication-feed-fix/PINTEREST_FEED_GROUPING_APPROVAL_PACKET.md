# Pinterest Feed Variant-Grouping — Approval Packet

Generated: 2026-05-15
Mode: repo-local approval/action packet only. No live writes yet.

## Decision Required

Toggle the Shopify -> Pinterest feed so it submits **one parent product per item** (variants grouped via `item_group_id`) instead of **one row per variant**. This is the smallest change that fixes the duplicate listings and wrong-hero-image symptom the owner observed in the Pinterest "Dresses" catalog group.

Diagnosis: `PINTEREST_VARIANT_DUPLICATION_DIAGNOSIS.md` in this same folder.

## Exact Approval Phrase

`I approve toggling the Shopify Pinterest sales-channel feed to group variants under a single parent product via item_group_id for advertiser 549756244483, with no Shopify product/title/price/inventory/vendor/type/policy edits, no Pinterest campaign/budget/bid/status/audience/tag/CAPI/billing changes, and no edits to other sales channels. After the 24-hour Pinterest re-sync, capture the after-state readback and only then consider promoting/launching.`

Until that exact phrase is given in the current session, no live Shopify or Pinterest write happens.

## Before-State Readback (do this before the toggle)

Capture from Pinterest Ads Manager -> Catalogs -> advertiser `549756244483`:

1. Total catalog item count.
2. "Dresses" product group entry count (owner-reported value: `157`).
3. Sample item-ID format (expected pattern: `shopify_US_<parent>_<variant>`).
4. Up to 3 example duplicate sets (same parent ID, different variant IDs) with their current `image_link` and price.

Capture from Shopify Admin -> Sales channels -> Pinterest -> Settings:

5. Screenshot or HTML readback of the product-feed / variant-submission section as it stands today.
6. Confirm the connected advertiser ID matches `549756244483`.
7. Confirm no pending re-authentication or scope-change prompts.

## Exact UI Steps (after approval phrase received)

1. In Shopify Admin, open `Sales channels` -> `Pinterest`.
2. Open `Settings` (sometimes labelled `Preferences` depending on channel version).
3. Locate the section named one of: `Product feed`, `Variant submission`, `Catalog feed options`, `How variants are sent`.
4. Look for whichever of these labels is present and change to the grouped option:
   - "Submit one product per variant" -> change to **"Submit one product per parent product (group variants by item_group_id)"**
   - "Send each variant separately" -> change to **"Group variants under their parent product"**
   - "Variant submission: Each variant" -> change to **"Variant submission: Primary variant only with item_group_id"**
5. If a separate `Default image` / `Image source` field exists, set it to **"Product featured image"** (not "Variant image").
6. If a separate `Additional images` field exists, leave it set to **"Variant images"** so color swatches still appear as additional_image_link.
7. Do **not** change any other field on the page (region, currency, conversion, tag, audience, billing, account, market).
8. Click `Save`.
9. Confirm the save banner reads success and no follow-up modal asks for re-authentication, scope changes, billing, or destructive confirmation.

If any of the labels above are not present, **STOP** and escalate to Path B (custom feed via Shopify Admin GraphQL).

## During-Save Stop Conditions

Stop immediately and read back if you see:

- Re-authentication / OAuth scope prompt.
- A confirmation modal that mentions deleting catalog history.
- A warning that other sales channels (Google & YouTube, Facebook & Instagram, TikTok) will be affected.
- A currency / market / region mapping change request.
- A billing / payment prompt.
- A CAPTCHA, policy review, or destructive-action confirm.
- Any unexpected "Pause campaigns" prompt — campaigns are already at `0 active` per current state, but a prompt would mean Pinterest is about to do more than expected.

## After-State Readback (24 hours after toggle)

Pinterest catalog typically re-ingests within 24 hours. Capture:

1. New total catalog item count for advertiser `549756244483`.
2. New "Dresses" group entry count. Expected: materially smaller (estimate: ~14 to 25 entries for the Dresses group; the 333-variant active-clean US scope collapses to **30 parent products** based on repo analysis).
3. New item-ID sample — confirm rows now share `item_group_id` or there is one row per parent.
4. The 3 example dresses captured pre-toggle — confirm each now appears once, with the correct hero image and a single price (the lowest variant price by default).
5. Pinterest catalog warnings / disapprovals panel — confirm no new severity-1 issues introduced.
6. Pinterest Event Quality dashboard — confirm no regression in event coverage (this toggle should be neutral for events).

## Rollback

If the after-state readback shows fewer working products than expected, missing hero images, or new disapprovals:

1. Return to the same Shopify Pinterest settings page.
2. Re-select the original variant-submission option captured in the before-state screenshot.
3. Save.
4. Wait one re-sync cycle and confirm catalog returns to its prior shape.

No campaign, ad group, ad, audience, tag, CAPI, conversion goal, billing, or account-level object should be touched at any point during rollback.

## Expected Impact

| Surface | Before | After (24h re-sync) |
|---|---|---|
| Pinterest catalog total items | ~thousands of variant rows | ~hundreds of parent products |
| "Dresses" group entry count | 157 | ~14 to 25 |
| Active-clean US scope | 333 variant rows | 30 parent products |
| Hero image per ad | mixed swatches / partial shots | primary product image |
| Per-product reporting | split across variants | clean per-parent |
| Wasted impressions on duplicates | high | eliminated |

## Why This Is The Right Fix

The owner's diagnosis is correct: Pinterest is not misbehaving — the Shopify feed is shipping every variant as a standalone item. This packet implements the smallest, lowest-risk, reversible feed-level change that:

- Solves the duplication symptom at its root.
- Restores correct hero images.
- Preserves all existing Shopify product data, prices, and inventory.
- Preserves all existing Pinterest campaign/account/billing state (currently `0 campaigns active`).
- Does not require any Pinterest live-write, so it bypasses the current `PINTEREST-CATALOG-EVENT-QUALITY` and `PINTEREST_LIVE_LAUNCH_CPC_SCOPE_BLOCKER` gates.
- Unblocks the active-clean exact-product-group launch path by collapsing variant rows into the parent dimension Pinterest's product-group selector actually uses.
