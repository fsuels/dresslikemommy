# Pinterest US Spanish Parent Collections Test Packet

Generated: 2026-05-20 05:55 EDT
Updated: 2026-05-20 06:42 EDT

AGENT_CONTINUITY_ANCHOR: 2026-05-20-pinterest-us-spanish-source-submitted-processing

## Owner Direction

- Owner asked whether a Spanish-market campaign in the United States makes sense.
- Owner then directed: `Do the spanish !`
- Owner then directed `do that` after being told the exact next step was completing the local Spanish feed-copy gate for all `210` rows.
- Owner then approved only the Pinterest US Spanish source/product-group prep phrase, with no campaign launch, spend, budget, bid, status, tracking, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM change.

## Verdict

`SOURCE_SUBMITTED__INGESTION_PROCESSING__PRODUCT_GROUPS_GATED`

The Spanish lane makes strategic sense, and the local parent feed now has Spanish title and description copy for all `210` parent rows. With the owner-approved source/product-group prep phrase, the repaired feed was uploaded to the dedicated Worker-backed URL and submitted to Pinterest as a separate U.S. Spanish URL source. Pinterest accepted the file validation and created source `3041760893334979315`, but the source is still processing. Product groups were not created because the approved `99/77/34` group gate requires completed ingestion and visible label counts from that source.

## Public Spanish Storefront Readback

Collection URLs:

| Lane | URL | HTTP | Readback |
|---|---|---:|---|
| Mommy & Me | `https://www.dresslikemommy.com/es/collections/mommy-and-me` | `200` | `lang="es"`, canonical `/es/collections/mommy-and-me`, Spanish collection title, `/es/cart/add`, `Agregar al carrito` |
| Family Matching | `https://www.dresslikemommy.com/es/collections/new-women-outfits` | `200` | `lang="es"`, canonical `/es/collections/new-women-outfits`, Spanish collection title, `/es/cart/add`, `Agregar al carrito` |
| Daddy & Me | `https://www.dresslikemommy.com/es/collections/daddy-me` | `200` | `lang="es"`, canonical `/es/collections/daddy-me`, Spanish collection title, `/es/cart/add`, `Agregar al carrito` |

Sample product URLs:

| Lane | URL | HTTP | Readback |
|---|---|---:|---|
| Mommy & Me | `https://www.dresslikemommy.com/es/products/red-resort-mommy-and-me-set` | `200` | Spanish canonical/product context, USD price, `Agregar al carrito` |
| Family Matching | `https://www.dresslikemommy.com/es/products/blue-stripe-family-matching-shirts` | `200` | Spanish canonical/product context, USD price, `Agregar al carrito` |
| Daddy & Me | `https://www.dresslikemommy.com/es/products/daddy-and-me-matching-floral-shirts-black-rose-print-short-sleeve-button-up-set` | `200` | Spanish canonical/product context, USD price, `Agregar al carrito` |

Supplier/source-host spot check:

- `1688`, `alicdn`, `detail.1688`, and `vendor_url` returned no hits on the three sample Spanish PDPs.
- The only `source_url` hit on collection pages was Shopify's own `trekkie.storefront` script, not a supplier/source URL.

Blocker:

- `https://www.dresslikemommy.com/es` and `https://www.dresslikemommy.com/es/` returned `500` / `Something went wrong` during public fetch. This does not block direct collection/PDP paid traffic, but it is a Spanish storefront health issue to fix or monitor before scaling Spanish traffic.

## Draft Feed Built

Local draft only:

- Script: `ops/scripts/build_pinterest_us_es_parent_paid_feed.py`
- Output: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-pinterest-us-spanish-parent-test/feeds/pinterest_us_es_paid_parent_collection_intent.tsv`
- Summary: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-pinterest-us-spanish-parent-test/feeds/pinterest_us_es_paid_parent_collection_intent.summary.json`
- Public readback CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-pinterest-us-spanish-parent-test/pinterest_us_es_parent_feed_public_readback.csv`

Draft feed structure:

| Field | Value |
|---|---|
| Rows | `210` |
| Unique parents | `210` |
| Mommy & Me | `99` |
| Family Matching | `77` |
| Daddy & Me | `34` |
| `custom_label_0` | `us_es` |
| `custom_label_4` | `collection_intent_parent_es_v20260520` |
| Duplicate IDs | `0` |
| Missing required fields | `0` |

Spanish copy status after the local repair:

| Check | Result |
|---|---:|
| Spanish title translations resolved | `210 / 210` |
| Spanish description translations resolved | `210 / 210` |
| Missing Spanish title translations | `0 / 210` |
| Missing Spanish description translations | `0 / 210` |
| Machine translation failures | `0` |
| Feed SHA-256 | `f4679594f0112105f814be617ff62919019cd711be147d7d0dcae4eb73ef4a69` |

Translation-source breakdown:

| Field | Method | Rows |
|---|---|---:|
| Title | Local cache exact | `201` |
| Title | Local cache strict contains/prefix match | `9` |
| Description | Local cache exact | `153` |
| Description | Existing normalized exact cache | `45` |
| Description | Local cache strict contains/prefix match | `12` |

The repair pass used local machine-translation fallback to populate true gaps, then a final no-network/default rerun passed from the local cache with `machine_translation_enabled=false`.

Quality guardrails:

- `guardrail_spanish_copy_complete=true`
- `guardrail_counts_match_expected=true`
- `guardrail_required_fields_present=true`
- `guardrail_unique_ids=true`
- Supplier/source-host scan of the generated TSV returned `0` hits for `1688`, `alicdn`, `alibaba`, `aliexpress`, `taobao`, `tmall`, `vendor_url`, `source_url`, or `detail.1688`.
- Sample inspection caught and corrected an initial overly-broad cache matcher that had pulled generic option labels into copy; the final builder requires stronger title/description match direction and machine-translates true gaps instead.

## Source/Product-Group Prep Execution

Owner approval used:

`APPROVE PINTEREST US SPANISH SOURCE AND PRODUCT GROUP PREP ONLY: upload or connect the repaired local US Spanish parent feed as a separate Pinterest catalog source, verify ingestion before-state/after-state, create only product groups for custom_label_0=us_es plus custom_label_2=mommy_and_me/family_matching/daddy_and_me plus custom_label_4=collection_intent_parent_es_v20260520, keep counts 99/77/34, do not create or launch a campaign, do not enable spend, do not change budget/bid/status/tracking/tag/CAPI/billing/Shopify/Merchant/Google Ads/GA4/GTM, then report the source and product-group readbacks.`

Cloudflare/Worker execution:

| Check | Result |
|---|---|
| R2 object uploaded | `dlm-pinterest-feeds/pinterest/pinterest_us_es_paid_parent_collection_intent.tsv` |
| Worker route deployed | `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-paid-parent-es-feed.tsv` |
| Worker version ID | `4ae0663a-9b31-43cd-a229-a6b1058b7ab4` |
| HTTP readback | `200` |
| `X-DLM-Feed-Rows` | `210` |
| `X-DLM-Feed-SHA256` | `f4679594f0112105f814be617ff62919019cd711be147d7d0dcae4eb73ef4a69` |
| Body SHA-256 | `f4679594f0112105f814be617ff62919019cd711be147d7d0dcae4eb73ef4a69` |
| Parsed labels | `custom_label_0=us_es`, `custom_label_4=collection_intent_parent_es_v20260520` |
| Parsed lane counts | Daddy `34`, Family `77`, Mommy `99` |
| Supplier/source-host hits | `0` |
| Non-GET guard | `POST` returned `405` / `method_not_allowed` |

Pinterest before-state:

- No separate URL source existed for `pinterest-paid-parent-es-feed.tsv`.
- Existing Shopify Spanish-language source `3041760870381325333` remained a Shopify feed with `4,639` products and was not used for this parent test.
- Existing English parent URL source `3041760889836768751` remained unchanged.

Pinterest after-state:

| Field | Readback |
|---|---|
| Source name | `DLM US ES Paid Parent Collection Intent 2026-05-20` |
| Source ID | `3041760893334979315` |
| Catalog | `3041764155561548387` / `Catalog_Retail` |
| Country | `United States` |
| Language | `Español (Américas)` |
| Source type | `URL` |
| Source URL | `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-paid-parent-es-feed.tsv` |
| File format | `TSV` |
| Currency | `USD` |
| Schedule | Daily, next update `May 21 at 3:45 AM EDT` |
| Submitted ingestion | `May 20 at 6:36 AM EDT` |
| Current product count | `Processing` |
| Current images | `Processing` |
| Past ingestion successful uploads | `0` while processing |
| Past ingestion failed uploads | `0` while processing |
| Past ingestion warnings | `0` while processing |

Product-group status:

- Not created yet.
- Reason: Pinterest source `3041760893334979315` still reads `Processing`, so the source does not yet expose confirmed `99/77/34` product counts for `custom_label_0=us_es` plus lane `custom_label_2` plus `custom_label_4=collection_intent_parent_es_v20260520`.
- Creating groups before the source completes would fail the approved count/readback gate.

## Strategic Recommendation

Do not launch from the earlier partial-copy draft. The current local feed copy gate is now passed, but live Pinterest work still needs a separate approval chain.

Best path:

1. Keep the repaired local Spanish parent structure and lane counts: `99/77/34`.
2. With a separate approval, upload/reingest as a separate US Spanish Pinterest catalog source.
3. With a separate approval, create Spanish product groups from `custom_label_0=us_es`, `custom_label_2=mommy_and_me/family_matching/daddy_and_me`, and `custom_label_4=collection_intent_parent_es_v20260520`.
4. With a final separate approval, launch as a small separate Spanish test campaign, not mixed into the current English campaign.

Recommended first test:

- Campaign name: `DLM_PIN_US_ES_PARENT_COLLECTIONS_99_77_34_20260520`
- Objective/format: Catalog sales / Shopping
- Audience: United States, Spanish-language audience/targeting where Pinterest allows it
- Product groups: Mommy `99`, Family `77`, Daddy `34`
- Budget: maximum `$5/day` for the new test campaign
- Bid: start max CPC `$0.15`; if delivery is too low after readback, prepare a controlled approval to test `$0.20-$0.25`
- Tracking: keep separate naming/UTM discipline so Spanish results are not mixed with English campaign learning

## Guardrails

Live external write performed under the exact owner-approved source/product-group prep phrase:

- Created/submitted only the separate Pinterest U.S. Spanish URL source `3041760893334979315`.
- Uploaded the repaired local Spanish parent feed to the dedicated Cloudflare R2 object and deployed the Worker route needed to serve it.

No out-of-scope live external write occurred:

- No Pinterest product group was created while ingestion is processing.
- No Pinterest campaign/ad group/ad was created or launched.
- No spend was enabled.
- No budget, bid, status, tracking, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM change occurred.

## Approval Packet Needed Before Live Pinterest Source/Product-Group Work

Exact next approval phrase:

`APPROVE PINTEREST US SPANISH SOURCE AND PRODUCT GROUP PREP ONLY: upload or connect the repaired local US Spanish parent feed as a separate Pinterest catalog source, verify ingestion before-state/after-state, create only product groups for custom_label_0=us_es plus custom_label_2=mommy_and_me/family_matching/daddy_and_me plus custom_label_4=collection_intent_parent_es_v20260520, keep counts 99/77/34, do not create or launch a campaign, do not enable spend, do not change budget/bid/status/tracking/tag/CAPI/billing/Shopify/Merchant/Google Ads/GA4/GTM, then report the source and product-group readbacks.`

Campaign launch should remain a final separate approval after source ingestion and product-group readbacks pass. The immediate next safe action is to poll source `3041760893334979315` until ingestion is completed; if it reads `210` successful uploads, `0` failed uploads, and `0` warnings, create only the three Spanish product groups with filters `custom_label_0=us_es`, `custom_label_2=mommy_and_me/family_matching/daddy_and_me`, and `custom_label_4=collection_intent_parent_es_v20260520`, expected counts `99/77/34`.
