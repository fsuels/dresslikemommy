# Pinterest Exact Product Groups Execution Readback

Date: 2026-05-18 06:55 EDT

Status: `REVIEW_REACHED__EXACT_GROUPS_SELECTED__PUBLISH_STOPPED_FINAL_REVIEW_INCOMPLETE`

## Approved Action Boundary

Owner approved proceeding under the final launch/scope packet constraints. This execution used only the exact item-ID product-group creation path under clean source `3041760873378113572`.

No broad `All Products` launch, old feed profile `3041760867124595727`, legacy source pause/remove, campaign save/publish, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4/GTM, Worker metadata, or product-data change occurred.

## Source Readback

- Pinterest advertiser: `549756244483`
- Pinterest catalog: `3041764155561548387`
- Selected feed profile: `DLM Cloudflare Grouped Feed 2026-05-18`
- Selected source/feed profile ID: `3041760873378113572`
- Product group page URL: `https://www.pinterest.com/business/catalogs/3041764155561548387/product-groups/?subjectBusinessId=343118202768859516&feedProfileId=3041760873378113572`

## Exact Groups Created

| Product group | Product group ID | Expected item-ID count | Pinterest readback | Status |
|---|---:|---:|---:|---|
| `DLM_PIN_US_SHOPPING_MOMMY_ME_333` | `4673019468477` | 201 | 201 products | `PASS_CREATED_PREVIEW_LOADS` |
| `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333` | `4673019468479` | 103 | 103 products | `PASS_CREATED_PREVIEW_LOADS` |
| `DLM_PIN_US_SHOPPING_PAJAMAS_333` | `4673019468480` | 29 | 29 products | `PASS_CREATED_LIST_READBACK` |

The three exact groups total the refreshed approved whitelist of `333` item IDs.

## Detail / Preview Evidence

- Mommy & Me pre-create preview showed `201 products selected`, `201 products in stock`, and `0 products out of stock`.
- Mommy & Me detail page showed source `DLM Cloudflare Grouped Feed 2026-05-18`, `201` products, and live product preview rows with item IDs.
- Family Matching pre-create preview showed `103 products selected`, `103 products in stock`, and `0 products out of stock`.
- Family Matching detail page showed source `DLM Cloudflare Grouped Feed 2026-05-18`, `103` products, and live product preview rows with item IDs.
- Pajamas pre-create preview showed `29 products selected`, `29 products in stock`, and `0 products out of stock`.
- Pajamas post-create list readback showed `29` products.
- After browser recovery, Pajamas detail page showed source `DLM Cloudflare Grouped Feed 2026-05-18`, product group `DLM_PIN_US_SHOPPING_PAJAMAS_333`, ID `4673019468480`, `29` products, and live preview rows.

## Evidence Files

- `raw/mommy-me-precreate-201-preview.snapshot.txt`
- `raw/mommy-me-precreate-201-preview.png`
- `raw/mommy-me-after-create.snapshot.txt`
- `raw/mommy-me-after-create.png`
- `raw/dlm-pin-us-shopping-mommy-me-333-detail-readback.snapshot.txt`
- `raw/dlm-pin-us-shopping-mommy-me-333-detail-readback.png`
- `raw/dlm-pin-us-shopping-family-matching-333-precreate-103-preview.snapshot.txt`
- `raw/dlm-pin-us-shopping-family-matching-333-precreate-103-preview.png`
- `raw/dlm-pin-us-shopping-family-matching-333-after-create.snapshot.txt`
- `raw/dlm-pin-us-shopping-family-matching-333-after-create.png`
- `raw/dlm-pin-us-shopping-family-matching-333-detail-readback.snapshot.txt`
- `raw/dlm-pin-us-shopping-family-matching-333-detail-readback.png`
- `raw/dlm-pin-us-shopping-pajamas-333-precreate-29-preview.snapshot.txt`
- `raw/dlm-pin-us-shopping-pajamas-333-precreate-29-preview.png`
- `raw/dlm-pin-us-shopping-pajamas-333-after-create.snapshot.txt`
- `raw/dlm-pin-us-shopping-pajamas-333-after-create.png`
- `raw/dlm-pin-us-shopping-pajamas-333-detail-readback.snapshot.txt`
- `raw/dlm-pin-us-shopping-pajamas-333-detail-readback.png`
- `PINTEREST_CAMPAIGN_REVIEW_STOP_READBACK.md`

## Campaign Review Stop

After browser recovery, the campaign flow proved that the three exact groups are selectable under clean source `3041760873378113572`.

Publish was stopped. The Review screen showed Catalog sales, exact groups `29/103/201`, daily budget `USD 5.00`, and max CPC `0.15`, but it did not explicitly display `Pin clicks`, did not explicitly display `Custom`, did not show the selected data-source name directly, and still showed Pinterest Performance+ targeting / expanded targeting language.

## Next Safe Action

Do not click Publish from the current Review screen unless the owner gives a fresh explicit override that names the visible review-screen caveats recorded in `PINTEREST_CAMPAIGN_REVIEW_STOP_READBACK.md`.
