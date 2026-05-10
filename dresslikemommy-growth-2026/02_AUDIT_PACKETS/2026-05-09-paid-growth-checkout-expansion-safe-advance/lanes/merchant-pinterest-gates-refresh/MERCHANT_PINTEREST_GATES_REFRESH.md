# Merchant / Pinterest Gates Refresh

Generated: 2026-05-09

Mode: local/read-only evidence synthesis only. This lane did not open Merchant Center or Pinterest accounts, did not upload/sync/edit sources, did not edit Shopify product data, did not create Pinterest campaigns/drafts/product groups, and did not change tags/CAPI/pixel, budgets, bids, statuses, feed labels, product scope, product groups, conversion goals, or live spend.

## Verdict

Merchant US/es and Pinterest are still approval-gated, not live-spend-ready. The next safe actions are narrow and separate:

1. Merchant US/es `Missing age group`: request exact approval for preferred Path A, an age_group-only supplemental source joined to source `10627981690` after exact preview and before/after readbacks.
2. Pinterest: request exact approval for paused US-only catalog/retargeting draft objects using the clean `342`-row EN-US scope and excluding the `4` unresolved variants. Event Quality `Fair` remains a live-spend gate.

## Tracker Reconciliation

Problem tracker drift found:

- `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`
  - Active Summary status: `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`
  - Detailed record status: `PARTIALLY_MITIGATED_LOCAL_ADS_HOLD__OWNER_APPROVAL_REQUIRED_FOR_SHOPIFY_FIX`
  - Reconciled lane interpretation: Active Summary is the cleaner current status. The detailed status appears stale/misaligned because this problem is not a Shopify SEO/title fix and is not primarily an Ads-hold mitigation problem. The current Merchant blocker is the source `10627981690` / `US` / `es` / `United States` age_group repair gate.

No tracker drift found for:

- `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`
  - Active Summary status: `OWNER_APPROVAL_REQUIRED`
  - Detailed record status: `OWNER_APPROVAL_REQUIRED`
  - Reconciled lane interpretation: consistent. Event Quality `Fair` gates live spend; paused US draft creation still requires exact owner approval and just-in-time readbacks.

This subagent did not edit `ops/PROBLEM_TRACKER.md` because the lane scope says write only under this packet directory.

## Merchant US/es Gate

Problem ID: `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`

Current status: `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`

Remaining blocker:

- Merchant account: `124884876`
- Source: `10627981690` / `Shopify App API`
- Feed label: `US`
- Language: `es`
- Country: `United States`
- Issue: `Missing age group`
- Exact affected paid-cohort scope: `625` unique item IDs / `1,250` issue rows
- Traffic split: `625` Shopping ads rows and `625` Free listings rows
- Product-detail proof: two affected US/es samples lacked effective `n:age_group`; one control sample on the same source had effective `n:age_group`

What is already solved and must not be redone:

- Shopify-side ProductVariant `mm-google-shopping.age_group` is already fixed for the current paid cohort.
- The original paid-cohort `US` / `en` / `United States` `Missing age group` gate is solved: fresh exact export showed current count `0`, down from prior exact `623`.
- The US/en dedicated age_group supplemental source path exists separately from US/es and must not be treated as the current blocker.
- Merchant local inventory was solved the correct dropshipping way by removing the physical-store `Local inventory ads` add-on; do not create local inventory feeds, pickup, warehouse, local-stock, or on-hand inventory claims.

Preferred Path A:

Create or update one age_group-only Merchant supplemental source joined to source `10627981690` / `Shopify App API`, only after exact owner approval and exact row preview. The payload must include only exact affected paid-cohort item IDs and only columns `id` and `age_group`.

Fallback Path B:

Use one source-specific official refresh only if the UI proves it applies narrowly to source `10627981690` / feed label `US` / language `es`. If the control is broad or ambiguous, do not click it.

Exact approval wording for preferred Path A:

```text
APPROVE MERCHANT US/ES AGE_GROUP PATH A ONLY: CREATE OR UPDATE ONE AGE_GROUP-ONLY MERCHANT SUPPLEMENTAL SOURCE JOINED TO SOURCE 10627981690 / SHOPIFY APP API FOR FEED LABEL US, LANGUAGE ES, COUNTRY UNITED STATES, USING ONLY EXACT PREVIEWED PAID-COHORT ITEM IDS CURRENTLY FAILING MISSING AGE_GROUP AND ONLY COLUMNS ID AND AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO PRIMARY SOURCE EDIT, BROAD SOURCE REFRESH, OR NON-AGE_GROUP PRODUCT-DATA CHANGE; PREVIEW ROW SCOPE FIRST, APPLY ONLY IF PREVIEW MATCHES, AND READ BACK SOURCE PROCESSING, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.
```

Required pre-readbacks before any approved Merchant repair:

1. Confirm a narrow Merchant US/es writer claim is clear or parent-owned.
2. Fresh exact Merchant all-issues export or equivalent readback showing paid-cohort `US/en/United States` remains `0` and recording current paid-cohort `US/es/United States` count.
3. Product detail readback for affected US/es samples:
   - `shopify_US_7227630649441_41872775020641`, expected age_group `kids`
   - `shopify_US_7227379023969_41871522431073`, expected age_group `adult`
4. Product detail readback for control sample:
   - `shopify_US_7227254276193_41871113158753`, expected age_group `toddler`
5. Source/path readback confirming source `10627981690`, source name `Shopify App API`, feed label `US`, language `es`.
6. Path A preview: exact affected row count, only `id` and `age_group`, valid values only, and no labels/source URLs/prices/shipping/inventory/descriptions/titles/campaign columns.

Required post-readbacks after any approved Merchant repair:

1. Source/action processing timestamp advanced; no parse errors; `age_group` recognized; matched/unmatched counts recorded.
2. Affected US/es sample details show no `Missing age group` and effective `n:age_group` present.
3. Control sample remains clean.
4. Fresh exact export shows paid-cohort `US/es/United States` `Missing age group` count is `0`, or any residual rows are itemized into a narrower problem.
5. Paid-cohort `US/en/United States` remains `0`.
6. Labels and paid-scope integrity remain unchanged; no Standard Shopping, product group, feed label, product scope, budget, bid, status, conversion-goal, Google Ads, Pinterest, or Shopify product-data change occurred.

## Pinterest Gate

Problem ID: `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`

Current status: `OWNER_APPROVAL_REQUIRED`

Clean paused-draft scope:

- Advertiser: `549756244483`
- Account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
- Clean scope CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`
- Clean rows: `342`
- Locale: `en-US`
- Availability: `IN_STOCK`
- Paid labels: `custom_label_0=paid_eligible`, `custom_label_4=us_test_ready`
- Product split: `210` Mommy & Me, `103` Family Matching, `29` Pajamas
- Exclusions CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`
- Excluded Shopify variant IDs: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`
- Clean/exclusion overlap: `0`

What is already solved and must not be redone:

- The old `337/346` Pinterest catalog blocker is superseded. Five stale rows re-resolved by Shopify variant ID, leaving `342` clean rows and `4` explicit exclusions.
- Do not reuse older `337` resolved / `9` excluded plans unless fresh just-in-time proof changes the row state.
- Do not add duplicate Pinterest tags, custom CAPI, customer-data changes, catalog-source changes, or tracking code by inference.

Event Quality state:

- Latest stored Event Quality status: `Fair`
- Event Quality updated date: `2026-05-06`
- Pinterest Tag status: `Fair`
- Conversions API status: `Fair`
- Pinterest Tag latest stored activity: `2026-05-08T05:50:56.502Z`
- Conversions API latest stored activity: `2026-05-08T05:51:13.760Z`
- Verified Merchant Program: `PASS`
- Automatic Enhanced Match: `PASS`
- Enhanced Match: `ERROR`
- Top gaps: `product_id__ADD_PAYMENT_INFO`, `hashed_email__ADD_TO_CART`, `click_id_epik__CHECKOUT`

Interpretation:

- The official Pinterest app path is alive.
- `Fair` Event Quality is not a blocker to exact-owner-approved paused draft creation.
- `Fair` Event Quality remains a live-spend gate unless the owner explicitly accepts the risk or approves a narrow tracking repair.

Exact approval wording for paused US Pinterest draft:

```text
APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.
```

Optional separate approval wording for narrow Event Quality repair:

```text
APPROVE NARROW PINTEREST EVENT QUALITY REPAIR ONLY: INVESTIGATE OFFICIAL SHOPIFY/PINTEREST APP AND CUSTOMER EVENTS CONFIGURATION FOR PRODUCT ID, EMAIL, AND CLICK ID GAPS; NO CAMPAIGN, DRAFT, PRODUCT GROUP, CATALOG SOURCE, AUDIENCE, BUDGET, BID, STATUS, OR SPEND CHANGES; NO DUPLICATE THEME TAG; NO CUSTOM CAPI DEPLOYMENT OR CUSTOMER-DATA CHANGE WITHOUT A SEPARATE READBACK AND APPROVAL; READ BACK BEFORE AND AFTER.
```

Required pre-readbacks before any approved paused Pinterest draft:

1. Confirm one Pinterest writer owns the account surface.
2. Read back advertiser `549756244483`: campaign count, currently serving count, spend, active/promoted objects, login/CAPTCHA/billing/unsaved prompts.
3. Read back Event Quality: overall WEB, Tag, CAPI, updated date, latest Tag/CAPI timestamps, Verified Merchant Program, Automatic Enhanced Match, Enhanced Match, top action items.
4. Revalidate clean scope CSV and exclusions: `342` clean rows, `4` exclusions, no overlap, all clean rows `en-US` / `IN_STOCK`.
5. Verify draft source is EN-US Shopify source `3041760867124595727`, not failed sitemap source `3041760916127467912` or localized sources.

Required post-readbacks after any approved paused Pinterest draft:

1. Created objects are paused/draft only.
2. Currently serving remains `0`.
3. Spend remains `$0.00`.
4. Product scope uses the 342-row clean set and excludes the four unresolved variants.
5. No tag/CAPI/catalog/feed/audience/budget/bid/source/Merchant/Google Ads/Shopify product-data changes occurred outside approval.
6. Event Quality is recorded again; live spend remains blocked if still `Fair`.

## Evidence Used

- `ops/PROBLEM_TRACKER.md`
- `ops/AGENT_COORDINATION.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/MERCHANT_AGE_GROUP_EXACT_EXPORT_READBACK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/reconciliation/merchant-product-issues-paid-age-group-context-breakdown.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/merchant-us-es-readonly/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/merchant-us-es-repair/MERCHANT_US_ES_AGE_GROUP_REPAIR_APPROVAL_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_scope_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/pinterest-gate/PINTEREST_PAUSED_US_DRAFT_EVENT_QUALITY_GATE_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/merchant-pinterest-gates/MERCHANT_PINTEREST_APPROVAL_GATES.md`

## Guardrails Confirmed

- No Merchant Center account was opened.
- No Pinterest account was opened.
- No source upload, sync, refresh, source edit, or Shopify product-data edit was made.
- No Pinterest campaign, draft, product group, tag, CAPI, pixel, catalog source, audience, budget, bid, status, or spend change was made.
- No Google Ads campaign, budget, bid, status, product scope, feed label, product group, conversion goal, PMax, Standard Shopping, or live-spend change was made.
- No external account writes occurred.
