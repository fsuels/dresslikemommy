# Pinterest Event Quality Draft Gate

Generated: 2026-05-08 03:01 EDT

Mode: local/read-only evidence refresh only. No Pinterest campaign, draft, product group, catalog, audience, tag, CAPI, budget, bid, account, or spend write was made.

## Verdict

`PAUSED_US_DRAFT_GATE_READY_FOR_EXACT_OWNER_APPROVAL__LIVE_SPEND_STILL_BLOCKED_BY_EVENT_QUALITY_FAIR`

The Pinterest catalog scope blocker is no longer the old `337/346` unresolved state. The current clean local scope is ready for a future owner-approved paused US-only catalog/retargeting draft build:

- Clean scope path: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`
- Clean scope rows: `342` EN-US `IN_STOCK` rows. The CSV has `343` lines including its header.
- Product split: `210` Mommy & Me, `103` Family Matching, `29` Pajamas.
- Exclusions path: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`
- Excluded variants: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`.

`Fair` Event Quality is not a reason to block an owner-approved paused draft build with no spend. It remains a live-spend/enablement blocker until the owner separately approves the risk or approves a narrow Event Quality repair.

## Evidence Used

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/LANE_BOARD.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_scope_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/unresolved_variant_reresolve_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/event_quality_api_probe.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/campaign_spend_baseline.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-orchestrated-safe-advance/lanes/pinterest/PINTEREST_342_SCOPE_DRAFT_GATE.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/pinterest/PINTEREST_PT_URL_READBACK_MONITOR.md`

## Account / Campaign Baseline

Latest stored read-only campaign baseline:

- Advertiser: `549756244483`.
- Visible account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`.
- Date range in baseline URL: `2026-04-08` through `2026-05-07`.
- Campaigns: `0`.
- Currently serving: `0`.
- Spend: `$0.00`.
- Results: `0`.
- Impressions: `0`.
- Pin clicks: `0`.

## Event Quality Status

Freshest local Event Quality API probe:

- Generated: `2026-05-08T05:55:17.164Z`.
- Overall WEB status: `Fair`.
- Pinterest Tag status: `Fair`.
- Conversions API status: `Fair`.
- Event Quality updated date: `2026-05-06`.
- Pinterest Tag latest: `2026-05-08T05:50:56.502Z`.
- Conversions API latest: `2026-05-08T05:51:13.760Z`.
- Verified Merchant Program: `PASS`.
- Automatic Enhanced Match: `PASS`.
- Enhanced Match: `ERROR`.
- Top action items: `product_id__ADD_PAYMENT_INFO`, `hashed_email__ADD_TO_CART`, `click_id_epik__CHECKOUT`.

Interpretation: the official Pinterest app path is alive because Tag and CAPI both have fresh activity. Event Quality has not cleared. The `click_id_epik` gap is partly expected while Pinterest has no serving traffic, but it still blocks a clean live-spend decision.

## Catalog Source Gate

Use only the EN-US Shopify source for any future US paused draft:

- EN Shopify source/feed profile: `3041760867124595727`.
- Catalog: `Catalog_Retail`.
- Catalog ID: `3041764155561548387`.
- Merchant ID used by helper: `3041760832963738705`.
- EN source status in prior readback: `Completed`, `5,663/5,663` uploaded, `0` failed, `152` warnings.
- Latest visible EN issue: `Warning 1039`, `description_html` too long; Pinterest indicates affected items publish without `description_html`.

Do not use the failed sitemap source `3041760916127467912`, localized sources, or international Pinterest expansion for this paused US draft gate.

## Failed / Ruled-Out Paths

- Creating any paused Pinterest object now: ruled out because this subagent has no owner action-time approval and the lane guardrail prohibits account writes.
- Live Pinterest spend or enablement: ruled out because Event Quality remains `Fair`, economics/readbacks still need approval, and there is no live-spend approval.
- Reusing the older `337` resolved / `9` unresolved plan: superseded by the later `342` clean scope and `4` explicit exclusions.
- Including the 4 unresolved variants: ruled out until they re-resolve in a fresh just-in-time proof.
- Using sitemap or localized catalog sources: ruled out because sitemap remains failed and localized sources are not launch-clean.
- Forcing Event Quality to `Good` locally: ruled out. The safe official app path is alive, and clearing `Fair` likely requires platform/app behavior, qualified Pinterest traffic/click IDs, or separately approved tracking work.
- Adding a duplicate theme-level Pinterest tag or custom CAPI path: ruled out without exact owner approval because it risks duplicate events, customer-data handling mistakes, and account tracking drift.

## Approval Wording

Paused US-only draft build:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

Narrow Event Quality repair, if the owner chooses repair before drafts:

`APPROVE NARROW PINTEREST EVENT QUALITY REPAIR ONLY: INVESTIGATE OFFICIAL SHOPIFY/PINTEREST APP AND CUSTOMER EVENTS CONFIGURATION FOR PRODUCT ID, EMAIL, AND CLICK ID GAPS; NO CAMPAIGN, DRAFT, PRODUCT GROUP, CATALOG SOURCE, AUDIENCE, BUDGET, BID, STATUS, OR SPEND CHANGES; NO DUPLICATE THEME TAG; NO CUSTOM CAPI DEPLOYMENT OR CUSTOMER-DATA CHANGE WITHOUT A SEPARATE READBACK AND APPROVAL; READ BACK BEFORE AND AFTER.`

## Next Action

Parent should choose one gate:

1. Ask the owner for the exact paused US Pinterest draft approval above, then run just-in-time read-only Event Quality/catalog/scope readbacks before any paused account write.
2. Or ask for the narrow Event Quality repair approval above, keeping all campaign/draft/product/catalog objects untouched until the repair path is read back.

Until then, Pinterest remains parked for live spend and no objects should be created.
