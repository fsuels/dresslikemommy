# Pinterest Campaign Review Stop Readback

Date: 2026-05-18 07:11 EDT

Status: `REVIEW_REACHED__EXACT_GROUPS_SELECTED__PUBLISH_STOPPED_FINAL_REVIEW_INCOMPLETE`

## Approved Boundary

Owner approved opening a fresh same-profile Chrome window, capturing the Pajamas detail readback, and continuing only if the exact groups were selectable inside the campaign flow.

No Publish click, Promote click, legacy-feed pause/remove, Shopify, Merchant, Google Ads, GA4/GTM, tag/CAPI, billing, Worker metadata, or product-data write occurred.

## Completed Readbacks

- Fresh Chrome connection succeeded after opening a same-profile Chrome window.
- Pajamas detail page read back `DLM_PIN_US_SHOPPING_PAJAMAS_333`, source `DLM Cloudflare Grouped Feed 2026-05-18`, group ID `4673019468480`, and `29` products with live preview rows.
- Campaign builder initially defaulted to `Consideration`, Performance+ campaign mode, daily budget `10.00`, and no exact product group selector in view. This was not publishable.
- Performance+ campaign mode was switched to manual after Pinterest displayed the confirmation dialog.
- Objective was switched to `Catalog sales`.
- Campaign name was set to `DLM_PIN_US_CATALOG_333_EXACT_20260518`.
- Daily budget was set to `USD 5.00 per day`.

## Product Group Selector Readback

The first ad-group product selector defaulted to an unapproved legacy/broad source:

- `All Products`
- ID `4673008376478`
- `5,594 Products in stock`
- source display `../ication%2Fjsonl`

The broad/legacy source was not used for final scope. The selector source dropdown exposed the clean source:

- `DLM Cloudflare Grouped Feed 2026-05-18`
- source/feed profile ID `3041760873378113572`

Switching to the clean source cleared the broad selection and exposed exactly four groups:

| Product group | ID | Products in stock | Selected |
|---|---:|---:|---|
| `All Products` | `4673019439386` | 41,694 | No |
| `DLM_PIN_US_SHOPPING_PAJAMAS_333` | `4673019468480` | 29 | Yes |
| `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333` | `4673019468479` | 103 | Yes |
| `DLM_PIN_US_SHOPPING_MOMMY_ME_333` | `4673019468477` | 201 | Yes |

After applying the selection, the ad group showed only the three exact groups from `DLM Cloudflare Grouped Feed 2026-05-18`. It did not show broad `All Products`.

## Delivery Settings Before Review

The create-flow form read back:

- Ad group name: `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518`
- Promotions: `Do not apply any promotions`
- Optimization: `Pin clicks`
- Bidding: `Custom`
- Maximum CPC bid: `0.15`

## Review Screen Readback

The Review screen read back:

- Advertiser/account: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
- Objective: `Catalog sales`
- Campaign name: `DLM_PIN_US_CATALOG_333_EXACT_20260518`
- Campaign status: `Active`
- Daily budget: `USD 5.00 per day`
- URL parameters: `None`
- Product groups:
  - `DLM_PIN_US_SHOPPING_PAJAMAS_333`, ID `4673019468480`, `29 items`
  - `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333`, ID `4673019468479`, `103 items`
  - `DLM_PIN_US_SHOPPING_MOMMY_ME_333`, ID `4673019468477`, `201 items`
- Broad `All Products`: not present on the review screen
- Bidding: `Maximum CPC bid (in USD): 0.15`

## Stop Reason

Publish was stopped because the final Review screen did not explicitly display all approval-phrase fields:

- It did not show the selected data-source name `DLM Cloudflare Grouped Feed 2026-05-18`; the exact group IDs imply that source, but the final screen itself only showed `Catalog_Retail` / `Product feed`.
- It did not display the words `Pin clicks`.
- It did not display the word `Custom`.
- It still displayed `You've selected Pinterest Performance+ targeting` and `Expanded targeting: On`. This is targeting language, not the disallowed Performance+ bidding path, but it is visible enough that it should be treated as a fresh owner decision before launch.

The create-flow snapshots prove `Pin clicks` and `Custom` were selected before Review, and the Review screen proves max CPC `0.15`; however, the final approval packet required the final review itself to show the key launch fields. Therefore the safe decision is `NO_PUBLISH`.

## Evidence Files

- `raw/dlm-pin-us-shopping-pajamas-333-detail-readback.snapshot.txt`
- `raw/dlm-pin-us-shopping-pajamas-333-detail-readback.png`
- `raw/campaign-builder-after-switch-to-manual.snapshot.txt`
- `raw/campaign-builder-after-catalog-sales-selected.snapshot.txt`
- `raw/campaign-builder-campaign-settings-5-dollar.snapshot.txt`
- `raw/campaign-product-groups-edit-open.snapshot.txt`
- `raw/campaign-product-groups-source-dropdown.snapshot.txt`
- `raw/campaign-product-groups-clean-source-switch-confirmed.snapshot.txt`
- `raw/campaign-product-groups-exact-selected-before-add.snapshot.txt`
- `raw/campaign-adgroup-after-exact-groups-added.snapshot.txt`
- `raw/campaign-adgroup-after-targeting-manual-confirmed.snapshot.txt`
- `raw/campaign-optimization-pin-clicks-selected.snapshot.txt`
- `raw/campaign-bidding-custom-selected.snapshot.txt`
- `raw/campaign-adgroup-settings-cpc-015.snapshot.txt`
- `raw/campaign-review-screen.snapshot.txt`
- `raw/campaign-review-screen.png`

## Next Safe Action

Do not click Publish from the current Review screen unless the owner gives a fresh explicit override that names the visible review-screen caveats: final review lacks visible `Pin clicks` / `Custom` labels and still shows Performance+ targeting / expanded targeting language, while exact groups, Catalog sales, `USD 5/day`, and max CPC `0.15` are visible or evidenced.

## Publish Approval Follow-up

Timestamp: 2026-05-18 15:05 EDT.

Owner provided the requested override phrase authorizing publication of the current Pinterest Catalog sales Review screen for advertiser `549756244483` despite the final Review screen caveats.

Before clicking Publish, the selected Pinterest tab was re-read. The approved Review screen was no longer current/recoverable. The selected tab was on a create-campaign page at:

`ads.pinterest.com/advertiser/549756244483/ads/create/?actingBusinessId=343118202768859516&enter_from=Ad_reporting_create_campaign`

The visible page no longer matched the approved launch scope. It showed:

- Objective selected: `Consideration`
- Campaign name: `Consideration Campaign | 2026-05-18 19:03 UTC`
- Ad group name: `Consideration Ad group | 2026-05-18 19:03 UTC`
- Budget amount: `10.00`
- Bottom actions: `Draft actions`, `Review`, `Publish`

It did not show the approved campaign `DLM_PIN_US_CATALOG_333_EXACT_20260518`, `Catalog sales`, exact groups `29/103/201`, daily budget `USD 5.00`, or max CPC `0.15`.

Decision: `NO_PUBLISH`. Publishing from the current page would risk launching a different Pinterest campaign. No Publish click occurred and no campaign/ad group/ad/budget/bid/status/source/tag/CAPI/billing/feed/product/Shopify/Merchant/Google Ads/GA4/GTM change was made.

Follow-up evidence:

- `raw/publish-approval-followup-current-page-readback.txt`
- `raw/publish-approval-followup-unsafe-create-page.png`
