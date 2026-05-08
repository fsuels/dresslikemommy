# Pinterest Gate Recheck

Generated: 2026-05-07 23:04 EDT

Lane: Pinterest catalog, tag, and event-quality gate.

Scope: local/read-only synthesis from stored Pinterest readbacks plus a local theme duplicate-tag scan. No Pinterest campaign, draft, product group, catalog, pixel, tag, CAPI, budget, bid, audience, spend, Shopify, Merchant, Google Ads, or product-data write was made.

## Decision

`PINTEREST_US_CATALOG_RETARGETING_DRAFTS_STILL_BLOCKED_PENDING_FRESH_ACCOUNT_READBACK_ITEM_PROOF_AND_EXPLICIT_APPROVAL`

Pinterest is closer than the older gate implied: the official Shopify Pinterest app pixel was repaired on 2026-05-06, and the 2026-05-07 Events Overview shows Checkout and AddPaymentInfo events arriving from both API and Tag. The draft gate is still not clear because Event Quality still reads `Fair`, exact current item-level paid candidate proof has not been refreshed since 2026-04-29, the failed sitemap source/localized feed warnings need interpretation, and any Pinterest draft creation still needs action-time approval.

## Latest Evidence Used

| Evidence | Timestamp / freshness | What it proves |
|---|---|---|
| `2026-05-07-paid-growth-continuation-readbacks/lanes/pinterest/PINTEREST_READBACK.md` | Generated 2026-05-07 14:45 EDT | Latest stored account readback for Event Quality, Events Overview, catalog data sources, EN ingestion, and product groups. |
| `event_quality_readback.txt` | Event Quality updated 2026-05-06 | Score still `Fair`; action items remain Product ID in AddPaymentInfo, Email in AddToCart, and Click ID in Checkout. |
| `events_overview_fresh_readback.txt` | Captured 2026-05-07 18:40 UTC | Standard events show `Api + Tag`; Checkout and AddPaymentInfo last received 2026-05-07 13:22 UTC. |
| `catalog_en_data_source_detail_fresh_readback.txt` | EN ingestion May 7 at 1:14 PM EDT | EN Shopify source `3041760867124595727` completed `5,663 of 5,663`, `0` failed, `152` warnings. |
| `catalog_en_ingestion_fresh_readback.txt` | Captured 2026-05-07 18:40 UTC | Visible EN ingestion issue rows were blank, so no concrete issue text was captured for the latest ingestion. |
| `2026-05-06-pinterest-event-quality-fix/PINTEREST_EVENT_QUALITY_FIX_RECHECK.md` | Post-fix diagnostic 2026-05-06 07:13 EDT | Official Pinterest app pixel changed to `Always on`; checkout pixel no longer blocked in Shopify Web Pixels Manager. |
| `2026-04-29-pinterest-item-readback/pinterest_item_level_readback_summary.json` | Generated 2026-04-29 05:01 | Historical item-level proof: `346/346` candidate rows found EN-US in stock, but stale for draft creation. |

## Trusted For Planning

- Advertiser/domain: latest stored Pinterest surfaces show `Dress Like Mommy | Matching Family Outfits`, `dresslikemommy.com`, advertiser `549756244483`.
- Official integration path: use the official Pinterest Shopify app Tag + CAPI path only. The repaired app pixel has pixel `22577249`, app `3009811`, tag `2620007050621`, and `dataSharingControls=["share_all_events"]` in the 2026-05-06 checkout diagnostic.
- Checkout pixel blocker: fixed as of 2026-05-06. The post-fix no-payment diagnostic showed `checkout_started` emitted with `SUCCESS` and `0` Pinterest `web_pixels_manager_subscriber_event_blocked` events.
- Event receipt: the 2026-05-07 Events Overview shows `Api + Tag` for PageVisit, ViewCategory, AddToCart, InitiateCheckout, Search, Checkout, and AddPaymentInfo. Checkout and AddPaymentInfo were last received 2026-05-07 01:22 PM UTC.
- EN catalog source: the latest stored readback identifies the active English source as `3041760867124595727`, United States / `en`, latest ingestion May 7 at 1:14 PM EDT, `Completed`, `5,663 of 5,663`, `0` failed, `152` warnings.
- Local duplicate-tag risk: a fresh local scan found no theme-level `pintrk`, `ct.pinterest`, Pinterest v3 event endpoint, hardcoded Pinterest tag ID, or hardcoded Pinterest pixel ID. Only social/icon/schema Pinterest references are present.
- Historical candidate structure is useful but not launch-current: the 2026-04-29 gate defined review-only groups for Mommy & Me (`214` rows), Family Matching (`103` rows), and Pajamas (`29` rows), all with known cost, paid-ready labels, and EN-US in-stock item proof at that time.

## Stale Or Not Trusted For Draft Creation

- Event Quality status is not clean. It still reads `Fair`, updated `5/6/2026`, with unresolved Product ID, Email, Click ID, and AddPaymentInfo Order Value gaps.
- Real Pinterest Click ID coverage remains unproven. The synthetic `epik` test showed cookie/data-sharing permission after the fix, but real `_epik` coverage requires actual Pinterest ad traffic.
- The 2026-04-29 item-level proof is stale. It predates later catalog ingestions, Shopify listing/product changes, shipping/policy fixes, and any paid-cohort evolution. It cannot be the final proof for draft product groups.
- The 2026-05-06 catalog-source ID in the prior synthesis should not be reused blindly. The 2026-05-07 data-source list shows `3041760867124595727` as English; older `3041760849210539103` appears as `ar` in the latest list.
- Campaign/spend baseline is stale for action time. Prior Pinterest readbacks showed `0 campaigns`, `0 currently being served`, and `$0.00` spend, but this must be rechecked immediately before any draft/build workflow.
- The separate sitemap source `3041760916127467912` still showed `Failed` on May 7 at 3:31 AM EDT. It may be unrelated to the EN Shopify catalog used for drafts, but it is not understood enough to ignore without a readback note.
- Localized Shopify feeds still showed warning/fail counts in the 2026-05-07 data-source list. They should not be used for Pinterest international testing yet.
- The old `VMP under review` note was visible on 2026-05-06 and was not clearly refreshed in the latest stored EN source detail. Confirm whether it is gone, informational, or launch-blocking.

## Exact Readbacks Needed Before Paused US Drafts

1. Pinterest account/session readback:
   - Use a dedicated `DLM-PINTEREST-EventCatalog` tab/session.
   - Confirm advertiser `549756244483`, account `Dress Like Mommy | Matching Family Outfits`, and domain `dresslikemommy.com`.
   - Confirm no unsaved changes, billing prompt, account switcher, modal, or permission prompt.

2. Campaign and spend baseline:
   - Read back campaign count, currently serving count, last 30 day spend, and any existing drafts.
   - Required gate: no active/serving Pinterest campaigns or unexpected spend before any new paused draft work.

3. Event Quality:
   - Capture score, update timestamp, source path, and date range.
   - Confirm whether the score refreshed after `2026-05-06`.
   - Open details for Product ID in AddPaymentInfo, Order Value in AddPaymentInfo, Email in AddToCart, Click ID in Checkout, and Event ID duplicate-event health.
   - Required gate for drafts: Event Quality does not need to be perfect, but unresolved gaps must be explicit and consciously accepted before any draft approval.

4. Events Overview:
   - Capture PageVisit, ViewCategory, AddToCart, InitiateCheckout, Search, Checkout, and AddPaymentInfo totals, sources, and last-received timestamps.
   - Required gate: standard ecommerce events still arrive from API + Tag; Checkout and AddPaymentInfo have recent post-fix receipt.

5. Shopify official pixel confirmation:
   - Read back Customer Events if access is available: `Pinterest / Connected / Always on`.
   - If not available, run a no-payment storefront-to-checkout diagnostic only if safe and slow; confirm no Pinterest app-pixel blocked events and no order/payment.
   - Do not add theme tag, custom pixel, or custom CAPI token.

6. Catalog source and ingestion:
   - Confirm catalog `Catalog_Retail` and catalog ID `3041764155561548387`.
   - Confirm English source `3041760867124595727`, country United States, language `en`, source Shopify, latest ingestion timestamp, product count, `Completed` state, failed count, warning count, and issue text.
   - Resolve the failed sitemap source enough to know whether it is irrelevant to the draft catalog or a real launch blocker.

7. Current item-level candidate proof:
   - Refresh exact item-level readback for the intended included rows before creating any product group/draft.
   - Include only current EN-US approved/salable rows with exact item IDs or variant IDs, known cost/margin, clean US landing pages, and paid-ready labels.
   - Preserve the current review-only structure unless refreshed proof changes it:
     - `DLM_PIN_US_SHOPPING_MOMMY_AND_ME`
     - `DLM_PIN_US_SHOPPING_FAMILY_MATCHING`
     - `DLM_PIN_US_SHOPPING_PAJAMAS`
   - Exclude All Products, out-of-stock rows, unknown-cost rows, stale catalog rows, unverified landing pages, non-US/non-English rows, and anything without exact current proof.

8. Retargeting-specific proof:
   - Read back available event/audience sources for site visitors, product viewers, add-to-cart, checkout starters, and purchasers/converters.
   - Confirm purchaser/converter exclusion is available or document the fallback.
   - No customer-list upload, PII upload, or custom audience write without separate approval.

9. Draft UI safety:
   - Before saving anything, confirm the draft workflow supports United States only targeting, paused/draft status, no live delivery, and no automatic product-group promotion.
   - Stop before Save/Create/Promote if the UI cannot guarantee paused-only output.

## Approval Gate

Paused draft creation still requires this exact approval before any Pinterest UI/API draft, campaign, ad group, budget, product group, or audience object is created:

`APPROVE PAUSED PINTEREST US CATALOG RETARGETING DRAFT BUILD: READ BACK PINTEREST ADVERTISER 549756244483, DOMAIN DRESSLIKEMOMMY.COM, CATALOG SOURCE, MERCHANT STATUS, EVENT QUALITY, AND EXACT US ITEM-LEVEL CATALOG ROWS FIRST; CREATE ONLY PAUSED/DRAFT US-ONLY PINTEREST CATALOG/RETARGETING STRUCTURE IF GATES PASS; NO LIVE SPEND, NO CAMPAIGN ENABLEMENT, NO PRODUCT GROUP LAUNCH, NO PIXEL/TAG/CAPI CHANGES, NO SHOPIFY PRODUCT OR FEED CHANGES, NO MERCHANT UPLOADS, NO GOOGLE ADS CHANGES, NO STANDARD SHOPPING/PMAX/CONVERSION-GOAL CHANGES.`

Live launch or spend requires a separate later approval after paused draft readbacks. Draft approval must not be treated as launch approval.

## Guardrails Preserved

- No Pinterest writes.
- No Shopify Admin, theme, product, or feed writes.
- No Merchant Center, Google Ads, GA4/GTM, campaign, budget, bid, status, product-scope, product-group, feed-label, pixel/tag/CAPI, audience, payment, or order changes.
- No duplicate Pinterest tag or custom CAPI path was added.
- No physical-store, warehouse, owned-inventory, or guaranteed-stock claims were introduced.

## Commands Run

- `sed -n` reads of AGENTS, paid-growth prompt, coordination files, lane board, worklog, and source packets.
- `rg -n "Pinterest|pinterest|Event Quality|catalog|PINTEREST" ...`
- `find dresslikemommy-growth-2026/02_AUDIT_PACKETS -path '*pinterest*' -o -path '*Pinterest*'`
- `jq .` on current Pinterest summaries and historical item/catalog gate summaries.
- `rg -n "pintrk|ct\\.pinterest|trkn\\.pinterest|pinterest\\.com/v3|Pinterest Tag|2620007050621|22577249" layout sections snippets templates assets config || true`
- `rg -n "pinterest|Pinterest" layout sections snippets templates assets config || true`
- `date '+%Y-%m-%d %H:%M:%S %Z (%z)'`

## Handoff

Lane status: `DONE_LOCAL_SYNTHESIS_NO_LIVE_READBACK_NO_WRITES`.

Next safest Pinterest action: run a fresh read-only account readback in the assigned Pinterest tab, then refresh exact item-level proof for the intended US rows. If those gates pass, ask for the exact paused-draft approval phrase above. Keep Pinterest draft creation and all spend parked until then.
