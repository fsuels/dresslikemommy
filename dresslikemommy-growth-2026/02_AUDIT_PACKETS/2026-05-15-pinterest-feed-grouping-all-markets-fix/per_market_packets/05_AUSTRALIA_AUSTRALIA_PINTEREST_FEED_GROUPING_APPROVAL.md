# Pinterest Feed Grouping Approval Packet — Australia

Shopify Market handle: `australia`
Owner priority rank: 5
Languages: en
Primary currency: AUD

Generated: 2026-05-15
Mode: repo-local approval/action packet only. No live writes yet.

## Decision Required

Toggle the Shopify -> Pinterest feed for the `australia` Shopify Market so every variant carries `item_group_id = <parent_product_id>` and `image_link = product.featuredImage.url`. This fix is identical in structure to every other market's packet in this folder; the only differences are the market handle, languages, and currency above.

## Exact Approval Phrase (this market only)

```
I approve fixing the Shopify -> Pinterest catalog feed for the `australia` Shopify Market (Australia, languages en) by enabling parent-product grouping via item_group_id and pinning image_link to the product featured image, with no Shopify product/title/price/inventory/vendor/type/policy edits, no Pinterest campaign/budget/bid/status/audience/tag/CAPI/billing changes, no Merchant Center source/feed mutations beyond what the Shopify channel emits automatically, and no edits to other sales channels. After the 24-hour Pinterest re-sync, capture before/after readback for this market and only then consider promoting/launching. The automated guardrail in ops/scripts/check_pinterest_feed_grouping.py must continue to pass.
```

To approve all markets in a single phrase instead, use `MASTER_ALL_MARKETS_APPROVAL_PHRASE.md`.

## Before-State Readback (capture before the toggle)

Capture for `australia` only:

1. Pinterest Ads Manager -> Catalogs -> advertiser `549756244483` -> catalog item count for the `australia` source (or the merged catalog if Pinterest does not split by Shopify Market).
2. Pinterest "Dresses" group entry count where source/market = `australia` (if Pinterest exposes per-source filters; otherwise capture overall).
3. Sample item-ID format — expected pattern: `shopify_AUSTRALIA_<parent>_<variant>`.
4. Up to 3 example duplicate sets (same parent product ID, different variant IDs) with their current `image_link` and price.
5. Screenshot or HTML of `Shopify Admin -> Sales channels -> Pinterest -> Settings` showing the current variant-submission setting.
6. Confirm the connected advertiser ID matches `549756244483` and the Shopify Market mapping is `australia`.
7. Confirm no pending re-auth or scope prompts.

## Exact UI Steps (after approval phrase received)

1. In Shopify Admin, open `Sales channels -> Pinterest`.
2. If the channel supports per-market overrides, select the `australia` Shopify Market context. Otherwise the global channel setting applies to every market and a single toggle covers all of them — record which behavior the UI exposes.
3. Open `Settings` (some versions label it `Preferences`).
4. Locate the section named one of: `Product feed`, `Variant submission`, `Catalog feed options`, `How variants are sent`.
5. Set the variant-submission option to the grouped option (label varies):
   - "Submit one product per variant" -> change to **"Submit one product per parent product (group variants by item_group_id)"**, OR
   - "Send each variant separately" -> change to **"Group variants under their parent product"**, OR
   - "Variant submission: Each variant" -> change to **"Variant submission: Primary variant only with item_group_id"**.
6. If a `Default image` / `Image source` field exists, set it to **"Product featured image"**.
7. If an `Additional images` field exists, leave it set to **"Variant images"** so color swatches still appear as `additional_image_link`.
8. Do not change any other field (region, currency, conversion, tag, audience, billing, account, market mapping).
9. Click `Save`.
10. Confirm success banner and no follow-up modal asks for re-authentication, scope change, billing, or destructive confirm.

If the toggle does not exist for this market, STOP. Fall back to Path B (custom GraphQL feed generator) for `australia` only — see `../scripts/generate_pinterest_feed_grouped.py` and upload its `australia` output as a separate Pinterest catalog source.

## During-Save Stop Conditions

Stop and read back if you see:

- Re-authentication / OAuth scope prompt.
- A modal mentioning catalog history deletion.
- A warning that other sales channels will be affected.
- A currency / market / region mapping change request.
- A billing / payment prompt.
- A CAPTCHA, policy review, or destructive-action confirm.
- A "Pause campaigns" prompt — campaigns should be at `0 active`, but a prompt means Pinterest is about to do more than expected.

## After-State Readback (24 hours after toggle)

For `australia` only:

1. New Pinterest catalog item count for the `australia` source.
2. New "Dresses" group entry count and any other product group counts.
3. New item-ID sample. Confirm rows now share `item_group_id` or one row per parent.
4. The 3 example sets captured pre-toggle — confirm each now appears once with the correct hero image and a single price.
5. Pinterest catalog warnings / disapprovals panel — confirm no new severity-1 issues.
6. Pinterest Event Quality dashboard — confirm no regression (this toggle should be neutral for events).
7. Run `python3.13 ops/scripts/check_pinterest_feed_grouping.py --market australia` -> expect `PASS`.

## Rollback

If after-state readback shows fewer working products than expected, missing hero images, or new disapprovals:

1. Return to the same Shopify Pinterest channel settings page (in the `australia` context if per-market).
2. Re-select the original variant-submission option captured in the before-state screenshot.
3. Save.
4. Wait one re-sync and confirm catalog returns to its prior shape.

No campaign, ad group, ad, audience, tag, CAPI, conversion goal, billing, or account-level object should be touched at any point during rollback.

## Why This Matters for `Australia`

- Currency is `AUD`, so wasted impressions on duplicate variant items burn `AUD` budget directly.
- Languages in scope are `en` — every language route emits the same duplicated shape today; the fix applies uniformly.
- Markets currently showing zero in Merchant exports (CA, GB) still need this fix locked in **before** propagation completes, so they never publish with the wrong shape in the first place.

## Acceptance Criteria for `australia`

- Catalog rows for `australia` collapse from ~20x variant inflation to one row per parent OR rows sharing `item_group_id`.
- `image_link` on every row is the parent product's featured image.
- `additional_image_link` carries variant images.
- Guardrail `check_pinterest_feed_grouping.py --market australia` returns PASS.
- Pinterest catalog shows no new severity-1 disapprovals for `australia`.
