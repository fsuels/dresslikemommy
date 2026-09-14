# Pinterest Parent Paid Source Execution Readback

Date: 2026-05-20

## Objective

Build the expert-level Pinterest catalog structure around Shopify collection intent, not brittle item-ID lists or variant-row selector counts.

The approved paid lanes are parent/outfit-level:

| Paid lane | Expected parent products | Feed label |
|---|---:|---|
| Mommy & Me | 99 | `custom_label_2=mommy_and_me` |
| Family Matching | 77 | `custom_label_2=family_matching` |
| Daddy & Me | 34 | `custom_label_2=daddy_and_me` |

All rows use `custom_label_0=us` and `custom_label_4=collection_intent_parent_v20260520`.

## Local Parent Feed Build

Generated parent-only paid source:

- Input: `feeds/pinterest_us_collection_intent.tsv`
- Output: `feeds/pinterest_us_paid_parent_collection_intent.tsv`
- Readback CSV: `pinterest_us_paid_parent_feed_readback.csv`
- Row count: `210`
- Unique parent count: `210`
- SHA-256: `e990b912ecc80d1c73e72b19f421f10d8a0d21aea13628506ea9230df1c114b6`
- Required field misses: `0`
- Duplicate IDs: `0`
- Supplier/source host hits: `0`
- Count gate: `PASS`

Subgroup counts:

| Paid lane | Subgroups |
|---|---|
| `mommy_and_me` | `swimwear=35`, `dresses=30`, `pajamas=22`, `tops_shirts=5`, `sweaters_outerwear=4`, `outfit_sets=3` |
| `family_matching` | `dresses=34`, `tops_shirts=33`, `sweaters_outerwear=6`, `outfit_sets=4` |
| `daddy_and_me` | `daddy_shirts_tshirts=34` |

## Cloudflare Worker And R2 Execution

External writes completed under the owner's current-session approval for the recommended parent-only source path:

- Uploaded R2 object: `dlm-pinterest-feeds/pinterest/pinterest_us_paid_parent_collection_intent.tsv`
- Deployed Worker route support for:
  - `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`
  - `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-paid-parent-feed.tsv`
- Worker version ID read back after deploy: `e1895fb5-1870-44de-8067-e73357f4d064`

Public parent-feed readback with Pinterestbot user agent:

- URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-paid-parent-feed.tsv`
- HTTP status: `200`
- Content type: `text/tab-separated-values; charset=utf-8`
- Content length: `857334`
- `X-DLM-Feed-Object-Key`: `pinterest/pinterest_us_paid_parent_collection_intent.tsv`
- `X-DLM-Feed-Rows`: `210`
- `X-DLM-Feed-SHA256`: `e990b912ecc80d1c73e72b19f421f10d8a0d21aea13628506ea9230df1c114b6`
- Parsed line count: `211` including header
- Parsed lane counts: `mommy_and_me=99`, `family_matching=77`, `daddy_and_me=34`
- Duplicate IDs: `0`
- Missing `item_group_id`: `0`
- Missing `image_link`: `0`
- Supplier/source host hits: `0`

Existing full-feed route remains live:

- URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`
- HTTP status: `200`
- `X-DLM-Feed-Object-Key`: `pinterest/pinterest_unified_all_markets.tsv`
- `X-DLM-Feed-Rows`: `28122`
- `X-DLM-Feed-SHA256`: `b76539eb641fede467bd6a572f90689c5b1bbff12edd8707fc202c87b4f1b1c0`

Residual technical note: a generic Python `urllib` fetch without a browser/Pinterestbot-style user agent returned `403 Forbidden`, while `curl` with a Pinterestbot user agent returned the expected `200` and body. Pinterest validation succeeded in the UI, so this is recorded as a monitoring risk, not a current blocker.

## Pinterest Source Creation

Created a new separate primary data source in Pinterest Catalogs:

- Catalog: `3041764155561548387`
- Source name: `DLM US Paid Parent Collection Intent 2026-05-20`
- Source ID: `3041760889836768751`
- Source type: `URL`
- URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-paid-parent-feed.tsv`
- File format: `TSV`
- Country: `United States`
- Language: `English (US)`
- Currency: `USD`
- Schedule: every `24` hours at `03:30 America/New_York`
- Pinterest validation: `File validation complete`
- Submission readback: `Your data source has been submitted and changes will be reflected soon. For large feeds, this may take up to 24 hours.`

Current Pinterest ingestion readback:

- Latest ingestion: `May 20 at 1:58 AM EDT`
- Status: `Completed`
- Product count: `210`
- Images: `Completed`
- Successful uploads: `210`
- Failed to upload: `0`
- Warnings: `0`
- Videos: `0`
- Next scheduled update: `May 20 at 3:30 AM EDT`

## Gate Status

The parent-only source completed cleanly and the count-verified parent product groups were created under source `3041760889836768751`.

Created product groups:

| Group name | Required filters | Expected selector count |
|---|---|---:|
| `DLM_PIN_US_PARENT_MOMMY_AND_ME_99_20260520` / `4673019642885` | `custom_label_0=us`, `custom_label_2=mommy_and_me`, `custom_label_4=collection_intent_parent_v20260520` | 99 |
| `DLM_PIN_US_PARENT_FAMILY_MATCHING_77_20260520` / `4673019642929` | `custom_label_0=us`, `custom_label_2=family_matching`, `custom_label_4=collection_intent_parent_v20260520` | 77 |
| `DLM_PIN_US_PARENT_DADDY_AND_ME_34_20260520` / `4673019642938` | `custom_label_0=us`, `custom_label_2=daddy_and_me`, `custom_label_4=collection_intent_parent_v20260520` | 34 |

List readback after creation:

- `All Products` / `4673019642691`: `210`
- `DLM_PIN_US_PARENT_MOMMY_AND_ME_99_20260520` / `4673019642885`: `99`
- `DLM_PIN_US_PARENT_FAMILY_MATCHING_77_20260520` / `4673019642929`: `77`
- `DLM_PIN_US_PARENT_DADDY_AND_ME_34_20260520` / `4673019642938`: `34`

## Guardrails

- No Pinterest campaign restart occurred.
- No campaign/ad group/ad/product-group attachment occurred.
- No budget, bid, status, tag/CAPI, billing, Shopify product/theme/app-proxy, Merchant, Google Ads, GA4, or GTM mutation occurred.
- Do not attach the old item-ID groups or the variant-row source groups.
- Do not restart campaign `626758581530` until budget/CPC/optimization/status are reviewed and the owner gives fresh restart approval.

## Paused Campaign Replacement Attempt

Date: 2026-05-20 03:05 EDT

Owner approval phrase received:

`APPROVE PINTEREST PAUSED CAMPAIGN GROUP REPLACEMENT ONLY: open campaign 626758581530, replace the old product groups with the verified parent groups 4673019642885 / 4673019642929 / 4673019642938, review budget/CPC/optimization/status, do not restart, publish, enable, or change budget/bid/status/tag/CAPI/billing/Shopify/Merchant/Google Ads/GA4/GTM, and stop before restart.`

Readback before attempted replacement:

- Campaign: `DLM_PIN_US_CATALOG_333_EXACT_20260518`
- Campaign ID: `626758581530`
- Campaign status: `Paused`
- Reporting state: `0 currently being served`
- Ad group: `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518`
- Ad group ID: `2680090307739`
- Ad group status: `Active`
- Bid: `$0.15`
- Optimization: `Pin clicks`
- Bidding: `Custom`
- Existing selected groups:
  - `DLM_PIN_US_SHOPPING_PAJAMAS_333` / `4673019468480` / `29` products / `DLM Cloudflare Grouped Feed 2026-05-18`
  - `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333` / `4673019468479` / `103` products / `DLM Cloudflare Grouped Feed 2026-05-18`
  - `DLM_PIN_US_SHOPPING_MOMMY_ME_333` / `4673019468477` / `166` products / `DLM Cloudflare Grouped Feed 2026-05-18`

Result:

- Attempted to switch the product-group selector data source to `DLM US Paid Parent Collection Intent 2026-05-20` / `3041760889836768751`.
- Pinterest blocked the action with: `Action not allowed` and `Switching data sources is not allowed in edit mode. You can duplicate an ad group or create a new ad group to use a different data source.`
- The modal was closed without saving.
- Reporting after the attempt still shows the same three old groups selected: Mommy `166`, Pajamas `29`, Family Matching `103`.

Guardrails honored:

- No `Save edits` click occurred.
- No duplicate/new ad group was created.
- No old ad group pause/remove action occurred.
- No campaign/ad group/ad/product-group attachment change, restart, publish, enable, budget, bid, status, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM write occurred.

Next valid approval path:

- Create a replacement ad group inside paused campaign `626758581530` using parent source `3041760889836768751` and the three verified parent groups, copy/review the same `Pin clicks`, `Custom`, `$0.15` CPC, format, targeting, tracking, and status settings, then pause or otherwise neutralize the old ad group before any future restart. This requires a fresh approval because it creates/duplicates account objects and changes ad-group structure.

## Replacement Ad Group Save Attempt Blocked

Date: 2026-05-20 03:26 EDT

Owner approval phrase received:

`fresh approval for a replacement ad group under the paused campaign, using parent source 3041760889836768751, attaching the three verified parent groups, copying/reviewing Pin clicks, Custom, $0.15 CPC, targeting/format/tracking/status, and neutralizing the old ad group before any restart.`

Approved work attempted:

- Created/staged replacement ad group under paused campaign `626758581530`.
- Selected parent source `3041760889836768751`.
- Attached the three verified parent product groups:
  - `4673019642938` / Daddy & Me / `34`
  - `4673019642929` / Family Matching / `77`
  - `4673019642885` / Mommy & Me / `99`
- Reviewed/copied settings: `Pin clicks`, `Custom`, max CPC `0.15`, Shopping-only format, Performance+ creative optimization `Off`, URL tracking `None`, CTA `Shop now`, U.S. targeting, and Browse/search placement.
- Staged old ad group `2680090307739` as `Paused` before save.

Blocked save readback:

- Original Chrome edit tab accepted the staged settings but repeated `Save edits` clicks did not persist or exit the editor.
- Separate authenticated Chrome DevTools tab confirmed the saved account state still had only one ad group before retrying the same approved replacement path.
- DevTools retry reached the same staged replacement structure, but Pinterest blocked final save with `1 error found` / `Bid is required` for the new ad group and disabled `Save edits`.
- The visible new-ad-group controls showed `Bidding=Custom` and bid field value `0.15`, but Pinterest validation still treated the bid as missing.

Guardrails honored:

- No successful external save was read back.
- No campaign restart, publish, enable, budget increase, billing, tag/CAPI, Shopify, Merchant, Google Ads, GA4, or GTM change occurred.
- The saved reporting surface still showed `1 ad group`, `0 currently being served` at the time of blocked save readback.
- The old ad group was not confirmed saved as paused because final save was blocked.

Next valid path:

- Continue only from a clean editor state or alternate supported Pinterest route. Recreate the replacement ad group, but verify the bid value clears validation before pausing the old ad group and saving. If Pinterest repeats the `Bid is required` validation loop while the field visibly contains `0.15`, stop and escalate to manual UI/API support instead of forcing or discarding unsaved edits.

## Replacement Ad Group Clean Retry Saved

Date: 2026-05-20 03:47 EDT

Owner approval phrase received:

`Reopen from a clean Pinterest editor state or use a supported alternate route. Recreate the replacement ad group, confirm the $0.15 bid clears validation before pausing the old group, then save and read back. If Pinterest repeats the same bid validation loop, escalate to manual UI/API support rather than forcing it.`

Saved action:

- Opened a clean authenticated Pinterest reporting tab for campaign `626758581530`.
- Created replacement ad group `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520`.
- New ad group ID after save/readback: `2680090331049`.
- Switched the new ad group to parent source `DLM US Paid Parent Collection Intent 2026-05-20` / `3041760889836768751`.
- Attached only the three verified parent groups:
  - `DLM_PIN_US_PARENT_DADDY_AND_ME_34_20260520` / `4673019642938` / `34`
  - `DLM_PIN_US_PARENT_FAMILY_MATCHING_77_20260520` / `4673019642929` / `77`
  - `DLM_PIN_US_PARENT_MOMMY_AND_ME_99_20260520` / `4673019642885` / `99`
- Set/reviewed optimization and delivery before neutralizing the old group:
  - Optimization: `Pin clicks`
  - Bidding: `Custom`
  - Max CPC bid: `0.15`
  - Bid validation: no `Bid is required` message, no `error found`, `Save edits` enabled before pausing the old group
- Set/reviewed format/tracking:
  - Pinterest Performance+ creative optimization: `Off`
  - Format: `Shopping ad`
  - Ad destination: `Website`
  - URL tracking: `None`
  - CTA: `Shop now`
  - Tracking URL: blank
- Targeting/placement remained the copied broad setup:
  - All genders, all ages, all languages, all devices
  - Location inclusions: all U.S.
  - Placement: Browse and search
- After bid validation cleared, old ad group `2680090307739` was set to `Paused`.

Save/readback:

- Save initially appeared blocked because Pinterest's feedback overlay covered the sticky save button area. Collapsing the feedback overlay exposed the active `Save edits` button.
- Final save exited the editor back to reporting.
- Campaign reporting readback:
  - Campaign `DLM_PIN_US_CATALOG_333_EXACT_20260518` / `626758581530` still reads `Paused`.
  - `0 currently being served`.
  - `2 ad groups`.
  - New ad group `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520` / `2680090331049` reads `Active`, spend `$0.00`, clicks `0`, bid `$0.15`.
  - Old ad group `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518` / `2680090307739` reads `Paused`, bid `$0.15`.
- Product-group reporting readback for new ad group `2680090331049`:
  - `3 product groups`.
  - Mommy & Me `99 products`, `Active`, ad format `Shopping`.
  - Family Matching `77 products`, `Active`, ad format `Shopping`.
  - Daddy & Me `34 products`, `Active`, ad format `Shopping`.
- New ad group edit readback confirmed:
  - `adGroupName=DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520`
  - `AdGroupShoppingOptimizationPicker=Pin clicks`
  - `adGroupBidStrategySelector=Custom`
  - `bid=0.15`
  - status tab `Active (recommended)` selected
  - selected product groups are the parent source groups at `34/77/99`
  - Performance+ creative optimization `Off`, format `Shopping ad`, URL tracking `None`, CTA `Shop now`

Guardrails honored:

- No campaign restart, publish, enable, or campaign budget change occurred.
- No billing, tag/CAPI, Shopify, Merchant, Google Ads, GA4, or GTM change occurred.
- No broad `All Products` group is attached to the replacement ad group.

Next valid path:

- Before any restart, do a final read-only review of campaign status, budget, ad group statuses, product-group counts, bid, optimization, and tracking. Restart/enable still requires fresh explicit owner approval.

## Final Pre-Restart Read-Only Review

Date: 2026-05-20 04:08 EDT

Scope:

- Read-only review only.
- No `Save edits`, restart, publish, enable, campaign budget, bid, tracking, status, billing, tag/CAPI, Shopify, Merchant, Google Ads, GA4, or GTM change.

Campaign reporting readback:

- Campaign `DLM_PIN_US_CATALOG_333_EXACT_20260518` / `626758581530` reads `Paused`.
- Reporting shows `0 currently being served`.
- Campaign row objective: `Catalog sales`.
- Campaign reporting window shows historical metrics only: `$5.29` spend, `2,741` impressions, `37` Pin clicks, `$0.14` CPC.

Campaign editor readback:

- Campaign status tab: `Paused` selected; `Active` not selected.
- Budget type: `Daily`.
- Budget amount: `10.00` USD.
- Campaign schedule: `Run continuously`.
- Campaign-level URL tracking / automatic URL parameters: not enabled; preview text shown but the apply checkbox is unchecked.

Ad group reporting readback:

- Campaign has `2 ad groups`.
- New replacement ad group `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520` / `2680090331049` reads `Active`, bid `$0.15`, spend `$0.00`, impressions `0`, clicks `0`.
- Old ad group `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518` / `2680090307739` reads `Paused`, bid `$0.15`.

New ad group editor readback:

- Ad group name: `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520`.
- Status tab: `Active (recommended)` selected.
- Optimization: `Pin clicks`.
- Bidding: `Custom`.
- Maximum CPC bid: `0.15` USD.
- Promotions: `Do not apply any promotions`.
- Product groups selected from `DLM US Paid Parent Collection Intent 2026-05-20` / source `3041760889836768751`:
  - `DLM_PIN_US_PARENT_DADDY_AND_ME_34_20260520` / `4673019642938` / `34 Products in stock`
  - `DLM_PIN_US_PARENT_FAMILY_MATCHING_77_20260520` / `4673019642929` / `77 Products in stock`
  - `DLM_PIN_US_PARENT_MOMMY_AND_ME_99_20260520` / `4673019642885` / `99 Products in stock`
- Format details:
  - Pinterest Performance+ creative optimization: `Off`
  - Format: `Shopping ad`
  - Ad destination: `Website`
  - URL tracking: `None`
  - CTA: `Shop now`
- Pinterest Performance+ creative:
  - Generate backgrounds: `Off`
  - Image resizing: `Off`
- Targeting:
  - Gender: `All genders`
  - Ages: `All ages`
  - Language: `All languages`
  - Device: `All devices`
  - Location inclusions: `All U.S.`
  - Location exclusions: `None`
  - Placement: `Browse and search`

Product-group reporting readback:

- New ad group `2680090331049` has `3 product groups`.
- Mommy & Me group reads `99 products`, `Active`, ad format `Shopping`, metrics all `0`.
- Family Matching group reads `77 products`, `Active`, ad format `Shopping`, metrics all `0`.
- Daddy & Me group reads `34 products`, `Active`, ad format `Shopping`, metrics all `0`.

Reviewer verdict:

- `PRE_RESTART_READBACK_PASSED__OWNER_APPROVAL_REQUIRED`
- Structure is ready for a bounded restart if the owner explicitly approves.
- The campaign is still paused and cannot serve until restarted.

## Restart Execution Readback

Date: 2026-05-20 04:22 EDT

Owner approval phrase received:

`APPROVE PINTEREST RESTART ONLY: change only campaign 626758581530 from Paused to Active, save, then read back campaign/ad group/product-group status and serving state. Do not change budget, bid, tracking, product groups, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM.`

Approved action executed:

- Opened the campaign editor for campaign `626758581530`.
- Before-state readback immediately before action showed:
  - Campaign status: `Paused`
  - Budget type: `Daily`
  - Budget amount: `10.00` USD
  - Schedule: `Run continuously`
  - Campaign automatic URL parameters: unchecked / not enabled
- Changed only campaign status from `Paused` to `Active`.
- Pre-save validation showed:
  - Campaign status tab `Active` selected
  - Campaign status tab `Paused` not selected
  - Budget still `10.00` USD
  - Schedule still `Run continuously`
  - Campaign automatic URL parameters still unchecked
  - No validation error text
  - `Save edits` enabled
- Clicked `Save edits`.
- Save exited the editor to reporting with no visible error.

After-state campaign reporting readback:

- Campaign `DLM_PIN_US_CATALOG_333_EXACT_20260518` / `626758581530` reads `Active`.
- Reporting shows `1 currently being served`.
- Objective: `Catalog sales`.
- Historical reporting window still shows `$5.29` spend, `2,741` impressions, `37` Pin clicks, `$0.14` CPC, `0` actions.

After-state campaign editor readback:

- Campaign status tab `Active` selected.
- Campaign status tab `Paused` not selected.
- Budget still `Daily` / `10.00` USD.
- Schedule still `Run continuously`.
- Campaign automatic URL parameters still unchecked / not enabled.

After-state ad group reporting readback:

- Campaign `DLM_PIN_US_CATALOG_333_EXACT_20260518` / `626758581530` shows `2 ad groups` in the campaign-filtered reporting table.
- Reporting shows `1 currently being served`.
- New replacement ad group `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520` / `2680090331049` reads `Active`, bid `$0.15`, spend `$0.00`, impressions `0`, clicks `0`.
- Old ad group `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518` / `2680090307739` reads `Paused`, bid `$0.15`.

After-state product-group reporting readback:

- New ad group `2680090331049` has `3 product groups`.
- `DLM_PIN_US_PARENT_MOMMY_AND_ME_99_20260520` reads `Active`, `99 products`, ad format `Shopping`, metrics all `0`.
- `DLM_PIN_US_PARENT_FAMILY_MATCHING_77_20260520` reads `Active`, `77 products`, ad format `Shopping`, metrics all `0`.
- `DLM_PIN_US_PARENT_DADDY_AND_ME_34_20260520` reads `Active`, `34 products`, ad format `Shopping`, metrics all `0`.

Guardrails honored:

- No budget change.
- No bid change.
- No tracking or URL-parameter change.
- No product-group change.
- No ad group status change during this restart step.
- No tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM change.

Reviewer verdict:

- `RESTART_EXECUTED__SERVING_STATE_ACTIVE__READBACK_PASSED`

Next action:

- Monitor read-only after Pinterest has time to deliver, watching spend, impressions, Pin clicks, outbound clicks, CPC, product-group distribution, checkout/purchase events, and any policy or delivery issue. Do not optimize, pause, change budget, bid, tracking, product groups, or tags without fresh approval unless a spend-safety stop is explicitly approved.

## Old Ad Group Archive Cleanup Readback

Date: 2026-05-20 05:15 EDT

Owner approval phrase received:

`APPROVE PINTEREST OLD AD GROUP ARCHIVE ONLY: archive/remove old paused ad group 2680090307739 from campaign 626758581530, leave new ad group 2680090331049 active, do not change budget, bid, tracking, product groups, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM, then read back that only the new 99/77/34 product groups remain visible/serving.`

Why this was needed:

- The campaign-level product-groups view showed `6` product-group rows because Pinterest displayed product groups from both the new active ad group and the old paused ad group.
- The old product groups themselves showed `Active` status, which was visually confusing even though the old ad group was paused.

Approved action executed:

- Opened campaign `626758581530` ad group reporting.
- Selected only old paused ad group `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518` / `2680090307739`.
- Confirmed new ad group `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520` / `2680090331049` was not selected.
- Opened `More Options`.
- Chose `Archive`.
- Pinterest showed irreversible archive confirmation: archiving campaigns, ad groups and/or ads cannot be undone, and reporting data remains available.
- Confirmed `Archive` for the selected old ad group.

Immediate archive readback:

- Old ad group `2680090307739` changed from `Paused` to `Archived` in the selected/archived reporting context.
- New ad group `2680090331049` remained `Active`.
- Campaign still showed `1 currently being served`.

Clean after-state campaign readback:

- Clean campaign reporting view, excluding archived ad groups, shows `1 campaign`.
- Campaign `DLM_PIN_US_CATALOG_333_EXACT_20260518` / `626758581530` reads `Active`.
- Reporting shows `1 currently being served`.

Clean after-state ad group readback:

- Campaign `626758581530` now shows `1 ad group` in the normal campaign-filtered view.
- The only visible ad group is `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520` / `2680090331049`.
- It reads `Active`.
- The old ad group `2680090307739` is not visible in the clean view.

Clean after-state product-group readback:

- Campaign `626758581530` now shows exactly `3 product groups`.
- Visible product groups are only:
  - `DLM_PIN_US_PARENT_MOMMY_AND_ME_99_20260520` / `99 products` / `Active` / `Shopping`
  - `DLM_PIN_US_PARENT_FAMILY_MATCHING_77_20260520` / `77 products` / `Active` / `Shopping`
  - `DLM_PIN_US_PARENT_DADDY_AND_ME_34_20260520` / `34 products` / `Active` / `Shopping`
- The old confusing `166 / 29 / 103` product-group rows are no longer visible in the normal campaign product-groups view.

Guardrails honored:

- No budget change.
- No bid change.
- No tracking or URL-parameter change.
- No product-group change.
- No new ad group change.
- No campaign status change.
- No tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM change.

Reviewer verdict:

- `OLD_AD_GROUP_ARCHIVED__CLEAN_VIEW_SHOWS_ONLY_PARENT_99_77_34__READBACK_PASSED`

Next action:

- Continue read-only delivery/spend-quality monitoring for the active parent campaign and product groups.

## Campaign Rename Cleanup Readback

Date: 2026-05-20 05:26 EDT

Owner approval phrase received:

`APPROVE PINTEREST CAMPAIGN RENAME ONLY: rename campaign 626758581530 to DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520, do not change status, budget, bid, tracking, ad groups, product groups, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM, then read back the new name.`

Approved action executed:

- Opened campaign editor for campaign `626758581530`.
- Before-state readback:
  - Campaign name: `DLM_PIN_US_CATALOG_333_EXACT_20260518`
  - Campaign status: `Active`
  - Budget amount: `10.00` USD
  - Schedule: `Run continuously`
  - Campaign automatic URL parameters: unchecked / not enabled
- Changed only the campaign name to `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520`.
- Pre-save readback showed:
  - Campaign name field set to `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520`
  - Status still `Active`
  - Budget still `10.00` USD
  - Schedule still `Run continuously`
  - No validation error
- Clicked `Save edits`.
- Save exited to reporting with no visible error.

After-state readback:

- Campaign reporting shows `1 campaign`, `1 currently being served`.
- Campaign name now reads `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520`.
- Campaign ID remains `626758581530`.
- Objective remains `Catalog sales`.
- Clean ad group reporting shows `1 ad group`: `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520` / `2680090331049`, `Active`, bid `$0.15`.
- Clean product-group reporting shows exactly `3 product groups`: Mommy `99`, Family `77`, Daddy `34`, all Active Shopping.

Guardrails honored:

- No status change.
- No budget change.
- No bid change.
- No tracking or URL-parameter change.
- No ad group change.
- No product-group change.
- No tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM change.

Reviewer verdict:

- `CAMPAIGN_RENAMED_PARENT_COLLECTIONS__READBACK_PASSED`

Next action:

- Continue read-only delivery/spend-quality monitoring.
