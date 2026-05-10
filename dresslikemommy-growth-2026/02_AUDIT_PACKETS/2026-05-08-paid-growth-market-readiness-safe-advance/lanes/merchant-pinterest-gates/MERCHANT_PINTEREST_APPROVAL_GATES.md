# Merchant / Pinterest Approval Gates

Generated: 2026-05-09

Mode: local/read-only synthesis only. No Merchant upload/source refresh/source edit, Shopify product-data edit, Pinterest draft/campaign/tag/CAPI/catalog write, Google Ads edit, budget/bid/status change, product-scope/feed-label/product-group change, or live-spend action was made.

## Executive Status

Merchant and Pinterest are not cleared for live spend. They are clear enough to move into exact-owner-approved narrow next actions:

- Merchant: original paid-cohort `US` / `en` / `United States` `Missing age group` is solved and must not be redone. Remaining Merchant gate is only `US` / `es` / `United States` on source `10627981690`.
- Pinterest: catalog scope is clean for a future paused US draft using `342` EN-US in-stock rows with `4` explicit exclusions. Event Quality remains `Fair`, so live spend remains gated.

## Merchant Gate

Status: `OWNER_APPROVAL_REQUIRED_FOR_NARROW_US_ES_REPAIR`

Problem ID: `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`

What is solved and must not be repeated:

- Shopify-side ProductVariant `mm-google-shopping.age_group` was already repaired for the current paid cohort.
- Exact Merchant all-issues export showed paid-cohort `US` / `en` / `United States` `Missing age group` count is `0`, down from prior exact `623`.
- The old `US/en` blocker is closed as `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT`.
- Do not rerun broad Shopify age_group edits, broad Merchant source refreshes, Merchant uploads, product-scope/feed-label/product-group changes, Standard Shopping edits, or local-inventory fixes to solve this.

Remaining blocker:

- Merchant account: `124884876`
- Source: `10627981690` / `Shopify App API`
- Feed label: `US`
- Language: `es`
- Country: `United States`
- Issue: `Missing age group`
- Exact affected paid-cohort scope: `625` item IDs / `1,250` issue rows
- Traffic split: `625` Shopping ads rows and `625` Free listings rows
- Read-only product-detail proof: two affected samples still lack effective `n:age_group`; one control sample on the same source has `n:age_group`

Narrow approval path:

Preferred Path A is an age_group-only supplemental source joined to source `10627981690` after exact preview. It must use only exact previewed affected paid-cohort item IDs and only `id` plus `age_group` columns.

Fallback Path B is a source-specific official refresh only if the UI proves it applies narrowly to source `10627981690` / `US` / `es`. If the control is broad or ambiguous, do not click it.

Exact approval wording for Path A:

```text
APPROVE MERCHANT US/ES AGE_GROUP PATH A ONLY: CREATE OR UPDATE ONE AGE_GROUP-ONLY MERCHANT SUPPLEMENTAL SOURCE JOINED TO SOURCE 10627981690 / SHOPIFY APP API FOR FEED LABEL US, LANGUAGE ES, COUNTRY UNITED STATES, USING ONLY EXACT PREVIEWED PAID-COHORT ITEM IDS CURRENTLY FAILING MISSING AGE_GROUP AND ONLY COLUMNS ID AND AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO PRIMARY SOURCE EDIT, BROAD SOURCE REFRESH, OR NON-AGE_GROUP PRODUCT-DATA CHANGE; PREVIEW ROW SCOPE FIRST, APPLY ONLY IF PREVIEW MATCHES, AND READ BACK SOURCE PROCESSING, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.
```

Required pre-readbacks before any approved Merchant repair:

1. Confirm the active writer claim is clear or owned by the parent for Merchant US/es age_group only.
2. Fresh exact Merchant all-issues export or equivalent readback showing `US/en` remains `0` and recording current `US/es` count.
3. Product detail readback for affected US/es samples:
   - `shopify_US_7227630649441_41872775020641`, expected age_group `kids`
   - `shopify_US_7227379023969_41871522431073`, expected age_group `adult`
4. Product detail readback for control sample:
   - `shopify_US_7227254276193_41871113158753`, expected age_group `toddler`
5. Source/path readback confirming source `10627981690`, source name `Shopify App API`, feed label `US`, language `es`.
6. For Path A, preview row count and schema: exact affected row scope, only `id` and `age_group`, valid age_group values only, no labels/source URLs/prices/shipping/inventory/descriptions/titles/campaign columns.

Required post-readbacks after any approved Merchant repair:

1. Source/action processing timestamp advanced; no parse errors; `age_group` recognized; matched/unmatched counts recorded.
2. Affected US/es sample details show no `Missing age group` and effective `n:age_group` present.
3. Control sample remains clean.
4. Fresh exact export shows paid-cohort `US/es/United States` `Missing age group` count is `0`, or any residual rows are itemized into a narrower problem.
5. Paid-cohort `US/en/United States` remains `0`.
6. Labels and paid-scope integrity remain unchanged: no Standard Shopping, product group, feed label, product scope, budget, bid, status, conversion-goal, Google Ads, Pinterest, or Shopify product-data change.

## Pinterest Gate

Status: `PAUSED_US_DRAFT_READY_FOR_EXACT_OWNER_APPROVAL__LIVE_SPEND_BLOCKED_BY_EVENT_QUALITY_FAIR`

Problem ID: `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`

Clean catalog scope:

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

What is superseded:

- The older `337/346` Pinterest catalog blocker is superseded by the clean `342` row scope with `4` explicit exclusions.
- Do not reuse older `337` resolved / `9` excluded plans unless fresh just-in-time proof changes the row state again.

Event Quality:

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
- `Fair` Event Quality is not a blocker to creating paused US draft objects after exact owner approval and just-in-time readbacks.
- `Fair` Event Quality remains a live-spend gate unless the owner explicitly accepts the risk or approves a narrow tracking repair.
- Do not add duplicate theme tags, custom CAPI, customer-data changes, catalog-source changes, or tracking code by inference.

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

## Current Decision

Do not request broad approval. The next clean actions are separate, exact approvals:

1. Merchant US/es age_group Path A repair for source `10627981690`, with preflight preview and post-readbacks.
2. Paused US Pinterest catalog/retargeting draft build using only the 342-row clean scope and 4 exclusions.
3. Separate narrow Pinterest Event Quality repair only if the owner wants measurement cleanup before paused drafts.

Live spend remains blocked until the owner gives separate live-spend approval after current Merchant/Pinterest/tracking/economics readbacks.

## Evidence Used

- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/PROBLEM_TRACKER.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/MERCHANT_AGE_GROUP_EXACT_EXPORT_READBACK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/merchant-us-es-readonly/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/merchant-us-es-repair/MERCHANT_US_ES_AGE_GROUP_REPAIR_APPROVAL_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-safe-followup/lanes/pinterest-gate/PINTEREST_EVENT_QUALITY_DRAFT_GATE.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/pinterest-gate/PINTEREST_PAUSED_US_DRAFT_EVENT_QUALITY_GATE_REFRESH.md`
