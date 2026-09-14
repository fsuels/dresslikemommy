# Pinterest Post-Pause Tracking And Landing Diagnostics - 2026-05-29

## Scope

- Read-only continuation from `AGENT_CONTINUITY_ANCHOR: 2026-05-29-pinterest-parent-spend-safety-pause-executed`.
- Campaign kept paused: `626758581530` / `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520`.
- Advertiser: `549756244483`.
- No Pinterest campaign, ad group, budget, bid, product group, source/feed, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or other campaign change occurred.
- Checks completed in the requested order: Events Manager Checkout/tag readback, then catalog ad/PDP deep-link sample, then Shopify/Pinterest UTM propagation.

## Campaign Pause Readback

- Pinterest reporting filter: campaign ID `626758581530`, objective `Catalog sales`, date range `2026-05-18` through `2026-05-29`, time zone `UTC`.
- UI row readback after the prior pause: `Paused`.
- Campaign name readback: `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520`.
- Spend readback in the refreshed UI row: `$105.30`.
- Impressions: `75,021`.
- Pin clicks: `1,005`.
- Screenshot: `pinterest-campaign-paused-diagnostic-readback-20260529.png`.
- Note: the pause-execution packet read `$105.00` immediately after pausing; this later reporting row refreshed to `$105.30` while status still read `Paused`.

## Pinterest Events Manager Readback

Events Overview, `Last 30 days`, showed the tag/CAPI pipeline is receiving web events from both sources:

| Event | Source | Total events | Last received |
|---|---:|---:|---:|
| `PageVisit` | `Api + Tag` | `27,900` | `2026-05-29 16:36 UTC` |
| `ViewCategory` | `Api + Tag` | `4,219` | `2026-05-29 16:36 UTC` |
| `AddToCart` | `Api + Tag` | `775` | `2026-05-29 15:29 UTC` |
| `InitiateCheckout` | `Api + Tag` | `172` | `2026-05-29 15:29 UTC` |
| `Search` | `Api + Tag` | `61` | `2026-05-29 15:38 UTC` |
| `AddPaymentInfo` | `Api + Tag` | `35` | `2026-05-28 17:12 UTC` |
| `Checkout` | `Api + Tag` | `34` | `2026-05-27 23:38 UTC` |

Tag Manager readback:

- Tag name: `conversion_tracker`.
- Tag ID: `2620007050621`.
- Latest event: `2026-05-29 16:36 UTC`.
- Automatic enhanced match: `Enabled`.

Event Quality readback:

- Conversions API source: `Fair`, Web events `Needs attention`, updated `2026-05-28`.
- Pinterest Tag source: `Fair`, Web events `Needs attention`, updated `2026-05-28`.
- Highest-priority gaps shown by Pinterest include `Click ID` quality on `Checkout`, `Add to Cart`, `Initiate Checkout`, and `Add Payment Info`; Tag quality also flags `Email` on `Add to Cart` and Checkout-related events.

Interpretation: the Pinterest tag/CAPI stack is not completely dead. Checkout is being received, but event-match quality is weak enough that paid-click attribution can still fail or undercount.

Screenshots:

- `pinterest-events-overview-20260529.png`
- `pinterest-event-quality-capi-20260529.png`
- `pinterest-event-quality-tag-20260529.png`
- `pinterest-tag-manager-20260529.png`

## Catalog Ad/PDP Deep-Link Sample

Method: sampled 10 catalog rows from the current parent source feed used for the parent collection intent lane. The live campaign remained paused; no paid ads were clicked. Because this is a catalog sales campaign, these source rows are the ad-to-PDP routing surface.

| Sample | Lane | PDP path | Status | Add-to-cart surface | Feed URL has UTM | UTM probe preserved |
|---:|---|---|---:|---:|---:|---:|
| 1 | `daddy_and_me` | `/products/daddy-baby-bestie-heart-matching-t-shirt-onesie-set-adorable-father-and-child-outfit` | `200` | yes | no | yes |
| 2 | `daddy_and_me` | `/products/matching-dad-son-tropical-cotton-button-up-shirts-set-navy-leaf-print-short-sleeve` | `200` | yes | no | yes |
| 3 | `daddy_and_me` | `/products/top-dad-and-top-son-matching-t-shirt-onesie-set-inspired-family-outfit` | `200` | yes | no | yes |
| 4 | `family_matching` | `/products/blue-striped-family-matching-set` | `200` | yes | no | yes |
| 5 | `family_matching` | `/products/cable-horse-family-matching-tops` | `200` | yes | no | yes |
| 6 | `family_matching` | `/products/vibrant-rainbow-family-matching-outfits-striped-t-shirts-and-yellow-overalls-set-for-family-outings` | `200` | yes | no | yes |
| 7 | `mommy_and_me` | `/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits` | `200` | yes | no | yes |
| 8 | `mommy_and_me` | `/products/autumn-peter-rabbit-mommy-and-me-pajamas` | `200` | yes | no | yes |
| 9 | `mommy_and_me` | `/products/chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection` | `200` | yes | no | yes |
| 10 | `mommy_and_me` | `/products/scarlet-ruffle-mommy-and-me-set` | `200` | yes | no | yes |

Sample summary:

- PDPs loaded: `10/10`.
- Add-to-cart surface detected: `10/10`.
- Current feed URLs with Pinterest UTM parameters: `0/10` sampled, `0/210` full feed.
- Manual UTM probes preserved by Shopify storefront redirects: `10/10`.
- Source/vendor-host hits detected in sampled storefront HTML: `0`.

## UTM Attribution Propagation

Current parent source file:

- Path: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-pinterest-shopify-collection-mapping/feeds/pinterest_us_paid_parent_collection_intent.tsv`.
- Rows: `210`.
- Rows with `utm_source`, `utm_medium`, and `utm_campaign`: `0`.
- Rows with `dlm_pg`: `0`.

Later isolated candidate feed, not applied to the paused campaign:

- Path: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-21-pinterest-isolated-catalog-diagnosis/pinterest_us_paid_parent_isolated_candidate.tsv`.
- Rows: `210`.
- Rows with `utm_source`, `utm_medium`, and `utm_campaign`: `210`.
- Rows with `dlm_pg`: `210`.

Interpretation: Shopify is preserving attribution parameters when they are present, but the current parent feed/source is not passing them. That makes Shopify/GA/Pinterest reconciliation weaker and makes `0` Shopify Pinterest-attributed orders less diagnostic than it should be.

## Result

- Spend-safety state is still correct: campaign `626758581530` reads `Paused`.
- Tracking is alive but not healthy: Checkout is received by both API and Tag, yet Pinterest Event Quality is `Fair` and flags click-ID quality on Checkout/AddToCart.
- PDP routing did not fail in the 10-row sample: all sampled catalog PDPs loaded and exposed add-to-cart.
- Attribution propagation is the concrete gap: the current source lacks UTM and `dlm_pg` coverage, while Shopify preserves those params if present.

Do not relaunch this campaign from the current source as-is. The next valid sales-moving step is an approval-gated relaunch plan that first fixes attribution/source tracking and event-match quality, or creates a new paused review-only catalog test with UTM-bearing links. Any source/feed, tag/CAPI, campaign, budget, bid, product-group, or status change still requires fresh exact approval.

## Evidence Files

- `pinterest_events_tag_campaign_readback.json`
- `pinterest_parent_feed_deeplink_utm_summary.json`
- `pinterest_parent_feed_deeplink_utm_readback.json`
- `pinterest_parent_feed_deeplink_utm_readback.csv`
- `pinterest-events-overview-20260529.png`
- `pinterest-event-quality-capi-20260529.png`
- `pinterest-event-quality-tag-20260529.png`
- `pinterest-tag-manager-20260529.png`
- `pinterest-campaign-paused-diagnostic-readback-20260529.png`
