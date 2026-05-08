# Pinterest Catalog / Tag / Event-Quality Gate

Generated: 2026-05-07 14:12 EDT

Subagent scope: read-only/local Pinterest gate synthesis and paused draft readiness. No Pinterest Ads, Shopify Admin, campaign, budget, product group, pixel, tag, CAPI, catalog, product, feed, or spend writes were made. Pinterest Ads was not opened in this subagent pass to avoid browser/tab collision risk; this packet synthesizes stored readbacks and local repo checks.

## Current Known Gate Status

Decision: `PINTEREST_US_CATALOG_RETARGETING_NOT_READY_FOR_DRAFT_CREATION_WITHOUT_FRESH_READBACK_AND_EXPLICIT_APPROVAL`.

Status summary:

| Gate | Current status | Evidence |
|---|---|---|
| Advertiser/account access | Last known pass on 2026-05-06 | Pinterest Ads was logged in for `Dress Like Mommy | Matching Family Outfits`, domain `dresslikemommy.com`, advertiser ID `549756244483`. |
| Campaign/spend state | Pass for no-spend baseline | 2026-05-06 readback showed `0 campaigns`, `0 currently being served`, `$0.00` spend. |
| Catalog merchant status | Pass with monitoring | Catalog `Catalog_Retail`, Shopify source `3041760849210539103`, Merchant status `Approved`, ingestion completed, `5.66k` successful uploads (`99.86%`), `8` failed (`0.14%`), `152` warnings (`2.68%`), `32` product groups visible. |
| Shopping eligibility | Pass with caveat | 2026-05-06 UI text said approved merchant able to run shopping ad campaigns; visible note still said `VMP under review`. |
| Item-level paid candidate proof | Historical pass, must refresh before build | 2026-04-29 item readback found `346/346` candidate rows as `FOUND_EN_US_IN_STOCK` across Mommy & Me (`214`), Family Matching (`103`), Pajamas (`29`). This is useful structure, but stale for a 2026-05-07 draft/build decision. |
| Official tag/API event path | Pass | 2026-05-06 events overview showed main events from `Api · Tag`: PageVisit, ViewCategory, AddToCart, InitiateCheckout, Search, Checkout, AddPaymentInfo. |
| Shopify official Pinterest app pixel | Pass after fix | Approved 2026-05-06 fix changed only the official Pinterest app pixel from `Optimized` to `Always on`. Post-fix readback: `Pinterest / Connected / Always on`. |
| Checkout web-pixel block | Pass after fix | Post-fix no-purchase checkout diagnostic showed Pinterest pixel `22577249`, app `3009811`, tag `2620007050621`, `checkout_started` emitted `SUCCESS`, `dataSharingControls=["share_all_events"]`, and `0` Pinterest blocked events. |
| Theme duplicate tag risk | Pass from local scan | Local scan found Pinterest only in social links/icons/schema; no theme-level `pintrk`, `ct.pinterest`, or custom Pinterest tag code. |
| Pinterest Event Quality score | Pending / stale | Last stored Pinterest readback still showed `Fair`, health score updated `5/4/2026`, after the Shopify fix had not yet refreshed. |
| Click ID proof | Pending / limited by no live Pinterest traffic | Synthetic `epik` test after the fix produced `_epik` / `_derived_epik`, but real ad-click `_epik` coverage cannot be proven while no Pinterest campaigns are serving. |
| AddPaymentInfo product/value gaps | Pending | 2026-05-06 Event Quality action items still included `Product ID` / `Order Value` in AddPaymentInfo; Checkout/AddPaymentInfo event overview rows still lagged at pre-fix timestamps. |

## What Passed

- Pinterest catalog/shop status is promising: approved merchant, Shopify data source, completed ingestion, and shopping-ads eligibility text were captured on 2026-05-06.
- The earlier item-level catalog gate found a usable US-only candidate structure: `DLM_PIN_US_SHOPPING_MOMMY_AND_ME`, `DLM_PIN_US_SHOPPING_FAMILY_MATCHING`, and `DLM_PIN_US_SHOPPING_PAJAMAS`, limited to exact paid-ready/in-stock rows.
- The official Pinterest app path is the intended tracking path. The repo should not add a custom tag or CAPI token.
- The controllable Shopify pixel blocker was fixed on 2026-05-06: official Pinterest app pixel is now `Always on`, checkout emits successfully, and the web-pixel manager no longer blocks the Pinterest checkout-start event.
- Local theme scan confirms no duplicate Pinterest tag implementation in theme code.
- No Pinterest spend exists in the stored readbacks, so there is no hidden paid performance or live campaign cleanup to preserve.

## Still Pending

- Fresh Pinterest Ads login/readback in the assigned `DLM-PINTEREST-EventCatalog` tab/session:
  - advertiser ID and domain
  - campaign count/spend still zero
  - catalog source, ingestion timestamp, failed/warning counts, and merchant status
  - item-level status for the exact candidate rows if a draft build is requested
  - Event Quality score update timestamp and current action items
  - event overview last-received timestamps for Checkout and AddPaymentInfo after the 2026-05-06 Shopify fix
- Real click-ID coverage cannot be fully proven until real Pinterest ad traffic exists. A tiny controlled spend test may be needed later, but only after draft/readback approval and explicit launch approval.
- `AddPaymentInfo` product ID/order value and `AddToCart` email coverage remain a platform-health risk until Pinterest refreshes or a fresh readback proves improvement.
- Catalog warnings/failures from 2026-05-06 were low but not zero; they must be rechecked before creating product groups or drafts.
- `VMP under review` was visible on 2026-05-06 despite merchant approval text; confirm whether it remains informational or launch-blocking.

## Safe Paused US Draft Prerequisites

Before any paused Pinterest US catalog/retargeting draft is created:

1. Use a separate Pinterest tab/session assigned to this lane; confirm advertiser `549756244483`, site `dresslikemommy.com`, and no unsaved UI state.
2. Read back catalog health and save evidence: merchant status, ingestion timestamp, source ID, successful/failed/warning counts, product group count, and whether `VMP under review` remains.
3. Refresh exact item-level proof for any included rows. Use only rows that are current `IN_STOCK` / approved / US English / clean landing page, and exclude all rows without exact proof.
4. Recheck Event Quality after the 2026-05-06 pixel fix. Ideal pass: score updated after `2026-05-06 11:13 UTC`, official Tag + API still present, Checkout/AddPaymentInfo timestamps refreshed, no Shopify web-pixel blocking.
5. Keep official Pinterest app Tag + CAPI only. Do not add a theme `pintrk`, custom customer pixel, custom CAPI token, third-party tracking app, or duplicate event path.
6. Draft structure only after approval:
   - campaign name: `DLM_PIN_US_SHOPPING_TEST_PAID_READY`
   - objective: Shopping/catalog sales
   - geography: United States only
   - status: paused/draft only
   - product groups: Mommy & Me, Family Matching, Pajamas only
   - exclude: All Products, unknown-cost rows, out-of-stock rows, unverified landing pages, international targeting, stale catalog rows, and anything without exact item-level proof
7. Retargeting drafts, if approved, should stay US-only, paused, exclude purchasers/converters where available, use only official Pinterest events/audiences, and avoid broad prospecting until catalog and event gates are fresher.
8. No live spend, campaign enablement, budgets, product groups, catalogs, pixels, tags, CAPI, Shopify product/feed changes, or Merchant/Google Ads changes without separate explicit owner approval.

## Exact Approval Gate Required

For a fresh read-only account recheck, no write approval should be required if the parent can assign a separate read-only Pinterest tab/session. Stop on login, account switcher, billing prompt, modal, policy warning, or any save/apply/create flow.

For paused Pinterest draft creation, request this exact approval before any UI/API draft, campaign, ad group, budget, product group, or audience object is created:

`APPROVE PAUSED PINTEREST US CATALOG RETARGETING DRAFT BUILD: READ BACK PINTEREST ADVERTISER 549756244483, DOMAIN DRESSLIKEMOMMY.COM, CATALOG SOURCE, MERCHANT STATUS, EVENT QUALITY, AND EXACT US ITEM-LEVEL CATALOG ROWS FIRST; CREATE ONLY PAUSED/DRAFT US-ONLY PINTEREST CATALOG/RETARGETING STRUCTURE IF GATES PASS; NO LIVE SPEND, NO CAMPAIGN ENABLEMENT, NO PRODUCT GROUP LAUNCH, NO PIXEL/TAG/CAPI CHANGES, NO SHOPIFY PRODUCT OR FEED CHANGES, NO MERCHANT UPLOADS, NO GOOGLE ADS CHANGES, NO STANDARD SHOPPING/PMAX/CONVERSION-GOAL CHANGES.`

For live launch/spend later, require a separate approval after paused draft readbacks. Do not infer launch permission from draft permission.

## Sources Read

- `ops/AGENT_COORDINATION.md`
- `ops/BROWSER_SUBAGENT_COORDINATION.md`
- `ops/MEMORY_CONTINUITY_PROTOCOL.md`
- `ops/GROWTH_NORTH_STAR.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/AGENT_WORKLOG.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-remarketing-policy-cleanup-pinterest-gate/REMARKETING_POLICY_CLEANUP_PINTEREST_GATE.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-pinterest-event-quality-fix/PINTEREST_EVENT_QUALITY_FIX_RECHECK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/pinterest_shopping_ads_gate_report.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-item-readback/pinterest_item_level_readback_summary.json`
- Local theme scan paths: `layout`, `sections`, `snippets`, `templates`, `assets`, `config`

## Commands Used

- `find dresslikemommy-growth-2026/02_AUDIT_PACKETS -maxdepth 2 -type d | sort | rg '2026-05-0(6|7).*pinterest|pinterest|paid-growth-parallel'`
- `sed -n '1,260p' ops/AGENT_COORDINATION.md`
- `sed -n '1,240p' ops/BROWSER_SUBAGENT_COORDINATION.md`
- `sed -n '1,180p' ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `sed -n '1,220p' ops/GROWTH_NORTH_STAR.md`
- `sed -n '1,260p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-pinterest-event-quality-fix/PINTEREST_EVENT_QUALITY_FIX_RECHECK.md`
- `sed -n '260,520p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-pinterest-event-quality-fix/PINTEREST_EVENT_QUALITY_FIX_RECHECK.md`
- `sed -n '1,260p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-remarketing-policy-cleanup-pinterest-gate/REMARKETING_POLICY_CLEANUP_PINTEREST_GATE.md`
- `jq . dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/summary.json`
- `jq . dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-item-readback/pinterest_item_level_readback_summary.json`
- `rg -n "pintrk|pinterest|ct.pinterest|trkn\\.pinterest|Pinterest" layout sections snippets templates assets config`
- `git status --short`

## Handoff

Lane status: `DONE_LOCAL_SYNTHESIS__FRESH_PINTEREST_READBACK_AND_APPROVAL_REQUIRED_FOR_DRAFTS`.

Next safe parallel action: parent can continue other lanes while Pinterest waits for either a fresh read-only account/tab recheck or the exact paused-draft approval gate above. The next Pinterest agent should not repeat the 2026-05-06 Shopify pixel fix; it should verify whether Pinterest Event Quality has refreshed after that completed fix.
