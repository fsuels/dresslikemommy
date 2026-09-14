# Google Shopping Parent-Outfit Missing Offers Repair Execution

UTC execution window: `2026-05-20T07:29Z` to `2026-05-20T07:38Z`

## Scope

Owner approval phrase received:

> Approve the Google Shopping missing-offer primary-source repair only: keep all Shopping V2 campaigns paused, keep DLM_US_STANDARD_SHOPPING_TEST_PAID_READY paused, read back and repair only the Google & YouTube / Merchant publication or sync state for the 8 diagnosed Mommy & Me parent products, do not change titles/prices/handles/body/SEO/inventory/campaigns/budgets/bids/statuses/product groups/conversions/billing, wait for processing, and rerun the counts/images/no-catchall gate before any activation discussion.

No Shopping activation, unpause, budget, bid, status, product-group, conversion, billing, title, price, handle, body, SEO, or inventory change was made.

## Before-State Gate

Gate timestamp: `20260520T072949Z`

- Gate passed: `false`
- Reason: `FAIL_CLOSED__MERCHANT_FEED_LABEL_IMAGE_READBACK_NOT_LIVE`
- Expected rows: `4531`
- Live ready-label rows: `47`
- V2 campaign status ok: `true`
- Old test campaign paused: `true`
- Bad catchall units: `0`

## Before-State Shopify Publication Readback

Google & YouTube publication: `gid://shopify/Publication/21969633377`

Before repair:

| Parent product ID | Title | Missing rows | Google & YouTube published |
|---|---|---:|---|
| `6718948147297` | Matching Mom & Child One Shoulder Swimsuit | `40` | `false` |
| `7562834215009` | Crochet Mommy and Me Set - Beach Coverup | `35` | `true` |
| `6718945034337` | Mom & Child Matching Two Piece Swimsuit | `20` | `false` |
| `6719764463713` | Matching Mommy And Me Hollow Out Bikini | `10` | `false` |
| `6719774720097` | Matching Mommy & Me Orange Print Swimsuit | `10` | `false` |
| `6719792873569` | Matching Mommy & Me Sunflower Print Swimsuit | `10` | `false` |
| `7535944368225` | Powder Blue Mommy and Me Set — Flutter Top & Eyelet Pants | `8` | `true` |
| `7227254276193` | Matching Yellow Sleeveless Maxi Dress Vibrant Summe... \| DLM | `6` | `true` |

## Repair Executed

Mutation used: Shopify Admin GraphQL `publishablePublish`

Target publication:

- `gid://shopify/Publication/21969633377` / Google & YouTube

Target products:

- `gid://shopify/Product/6718948147297`
- `gid://shopify/Product/7562834215009`
- `gid://shopify/Product/6718945034337`
- `gid://shopify/Product/6719764463713`
- `gid://shopify/Product/6719774720097`
- `gid://shopify/Product/6719792873569`
- `gid://shopify/Product/7535944368225`
- `gid://shopify/Product/7227254276193`

Result:

- Mutation calls: `8`
- Shopify `userErrors`: `0`
- Products remained `ACTIVE`: `8`

Execution JSON:

- `google_shopping_missing_offer_shopify_publish_execution_20260520T0730Z.json`

## After-State Shopify Publication Readback

After repair, all 8 products read back as published to Google & YouTube.

Fresh publish timestamps were created for the five products that were previously missing publication:

- `6718948147297`: `2026-05-20T07:31:59Z`
- `6718945034337`: `2026-05-20T07:32:00Z`
- `6719764463713`: `2026-05-20T07:32:01Z`
- `6719774720097`: `2026-05-20T07:32:02Z`
- `6719792873569`: `2026-05-20T07:32:03Z`

After readback JSON:

- `google_shopping_missing_offer_shopify_publication_after_20260520T0730Z.json`

## Processing Poll

Google Ads Shopping-product polling showed the supplemental ready-label propagation is moving, but not complete:

- `2026-05-20T07:32:53Z`: ready rows `54`
- `2026-05-20T07:33:55Z`: ready rows `54`
- `2026-05-20T07:34:57Z`: ready rows `54`
- `2026-05-20T07:35:59Z`: ready rows `54`
- `2026-05-20T07:37:01Z`: ready rows `72`
- `2026-05-20T07:38:03Z`: ready rows `73`

The newly published whole-missing parent products had not appeared in the Google Ads Shopping-product surface during the bounded poll window.

Poll JSON:

- `google_shopping_missing_offer_processing_poll_20260520T0732Z.json`

## After-State Gate

Gate timestamp: `20260520T073815Z`

- Gate passed: `false`
- Reason: `FAIL_CLOSED__MERCHANT_FEED_LABEL_IMAGE_READBACK_NOT_LIVE`
- Expected rows: `4531`
- Live ready-label rows: `72`
- V2 campaign status ok: `true`
- Old test campaign paused: `true`
- Bad catchall units: `0`
- Merchant Content API scope available: `false`

## Conclusion

The approved primary-source publication repair was completed successfully in Shopify Admin for the 8 diagnosed parent products. The account is now waiting on Google & YouTube / Merchant / Google Ads product propagation and supplemental-label matching.

Activation remains blocked. All V2 Shopping campaigns must stay paused until the gate proves live counts, hero images, exclusions, and no catchall leakage.
