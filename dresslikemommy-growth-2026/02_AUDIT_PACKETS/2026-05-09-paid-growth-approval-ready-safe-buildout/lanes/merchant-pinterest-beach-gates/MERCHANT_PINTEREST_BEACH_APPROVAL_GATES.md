# Merchant, Pinterest, And Beach Metadata Approval Gates

Generated: 2026-05-09

Worker: Worker B, local/read-only gate synthesis.

Mode: evidence synthesis only. No Merchant Center, Pinterest, Shopify Admin, Google Ads, feed, catalog, campaign, budget, bid, status, product-data, product-scope, feed-label, product-group, conversion-goal, upload, preview/import, or live-spend write was made.

Assigned write scope honored: only `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-approval-ready-safe-buildout/lanes/merchant-pinterest-beach-gates/`.

## Executive Gate Board

| Gate | Current status | Closest safe next action | Live-spend ready |
|---|---|---|---|
| Merchant US/es age_group | `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX` | Get exact approval for Path A: one age_group-only supplemental source joined to Merchant source `10627981690`, after exact preview and readbacks | No |
| Pinterest Event Quality / paused drafts | `OWNER_APPROVAL_REQUIRED` | Get exact approval either for paused US draft objects from the clean `342` rows, or for a separate narrow Event Quality repair | No |
| Beach / Vacation Family metadata | `PARTIALLY_MITIGATED_LOCAL_ADS_HOLD__OWNER_APPROVAL_REQUIRED_FOR_SHOPIFY_FIX` | Keep using the held `1496`-row Ads CSV, or get exact approval for narrow Shopify SEO/social metadata repair for product `7227378892897` | No |

Operator rule: keep these as separate approval gates. Do not bundle Merchant, Pinterest, Shopify metadata, and Google Ads actions into one approval or one browser session.

## Gate 1: Merchant US/es Age_Group

Problem ID: `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`

Current status: `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`

Surface:
- Merchant Center account: `124884876`
- Source: `10627981690` / `Shopify App API`
- Feed label: `US`
- Language: `es`
- Country: `United States`
- Issue: `Missing age group`
- Exact affected paid-cohort scope: `625` item IDs / `1,250` issue rows
- Split: `625` Shopping ads rows and `625` Free listings rows

Current evidence:
- The original paid-cohort `US/en/United States` Missing age group gate is solved: exact export count is `0`, down from prior `623`.
- Shopify-side ProductVariant `mm-google-shopping.age_group` is already fixed for the current paid cohort and should not be redone.
- Live read-only Merchant product-detail RPC confirmed two affected US/es samples on source `10627981690` still lack effective `n:age_group`; one control sample on the same source has effective `n:age_group`.
- Product detail samples from prior readback:
  - Affected: `shopify_US_7227630649441_41872775020641`, expected age_group `kids`
  - Affected: `shopify_US_7227379023969_41871522431073`, expected age_group `adult`
  - Control: `shopify_US_7227254276193_41871113158753`, expected age_group `toddler`

Tried, ruled, or routed paths:
- Tried: exact product-issues export reconciliation. Result: US/en is solved, US/es remains isolated to `625` IDs / `1,250` rows.
- Tried: live read-only source/product detail readback. Result: source `10627981690` is the authoritative US/es blocker.
- Ruled out: repeating Shopify age_group edits, unless a fresh Shopify readback proves regression.
- Ruled out: blind Merchant source refresh, broad all-source sync, source edit, Merchant upload, Shopify product-data edit, product-scope/feed-label/product-group/conversion-goal change, or Standard Shopping change without exact approval.
- Ruled out: local inventory feed, pickup, warehouse, local-stock, or on-hand inventory claims. DLM is dropshipping and the physical-store local inventory diagnostic was already solved by removing the local inventory ads add-on.

Exact next unblock action:
- Ask the owner for one narrow Merchant approval. Preferred Path A is deterministic: preview and create/update one age_group-only supplemental source joined to source `10627981690`, using only affected US/es paid-cohort item IDs and only `id` plus `age_group`.

Preferred approval phrase:

```text
APPROVE MERCHANT US/ES AGE_GROUP PATH A ONLY: CREATE OR UPDATE ONE AGE_GROUP-ONLY MERCHANT SUPPLEMENTAL SOURCE JOINED TO SOURCE 10627981690 / SHOPIFY APP API FOR FEED LABEL US, LANGUAGE ES, COUNTRY UNITED STATES, USING ONLY EXACT PREVIEWED PAID-COHORT ITEM IDS CURRENTLY FAILING MISSING AGE_GROUP AND ONLY COLUMNS ID AND AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO PRIMARY SOURCE EDIT, BROAD SOURCE REFRESH, OR NON-AGE_GROUP PRODUCT-DATA CHANGE; PREVIEW ROW SCOPE FIRST, APPLY ONLY IF PREVIEW MATCHES, AND READ BACK SOURCE PROCESSING, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.
```

Fallback approval phrase, only if the UI proves the control is source-specific:

```text
APPROVE MERCHANT US/ES AGE_GROUP PATH B ONLY: READ BACK SOURCE 10627981690 AND TWO AFFECTED US/ES PRODUCT DETAILS FIRST; THEN CLICK ONE CLEARLY LABELED SOURCE-SPECIFIC OFFICIAL SHOPIFY APP API / GOOGLE & YOUTUBE REFRESH, SYNC, OR UPDATE-PRODUCTS CONTROL ONLY IF THE UI CONTEXT PROVES IT APPLIES TO SOURCE 10627981690 / FEED LABEL US / LANGUAGE ES; NO MERCHANT UPLOAD, SOURCE CREATION, PRIMARY SOURCE EDIT, SHOPIFY PRODUCT-DATA EDIT, GOOGLE ADS, PINTEREST, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; DO NOT USE A BROAD ALL-SOURCES REFRESH; READ BACK SOURCE TIMESTAMP, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.
```

Pre-readbacks before any approved Merchant repair:
- Confirm a narrow Merchant US/es writer claim is parent-owned in coordination.
- Fresh exact all-issues export or equivalent: US/en remains `0`; US/es current count is recorded.
- Product detail readback for the two affected samples and the one control sample above.
- Source/path readback confirms source `10627981690`, source name `Shopify App API`, feed label `US`, language `es`.
- Path A preview proves exact row count, only `id` and `age_group`, valid values only: `newborn`, `infant`, `toddler`, `kids`, `adult`.
- Path B UI proof shows the refresh is source-specific to `10627981690` / `US` / `es`; if broad or ambiguous, stop.

Post-readbacks after any approved Merchant repair:
- Source/action timestamp advanced; no parse errors; `age_group` recognized; matched/unmatched counts recorded.
- Both affected US/es samples show no Missing age group and effective `n:age_group`.
- Control sample remains clean.
- Fresh exact export shows paid-cohort `US/es/United States` Missing age group count is `0`, or residuals are itemized into a narrower problem.
- Paid-cohort `US/en/United States` remains `0`.
- Standard Shopping product scope, feed labels, product groups, budget, bids, status, and conversion goals remain unchanged.

Stop conditions:
- Owner approval is missing or does not name source `10627981690`.
- Preview row scope does not match the current affected US/es scope.
- Payload contains anything except `id` and `age_group`.
- UI control appears account-wide, all-source, all-product, or ambiguous.
- Any prompt asks for product scope, feed label, product group, campaign, budget, bid, conversion, Shopify product-data, or Standard Shopping change.

Expressly forbidden:
- Broad Merchant refresh, unspecific sync, upload without preview, primary source edit, Shopify product-data edit, local inventory feed, product-scope/feed-label/product-group change, Google Ads or Pinterest write, campaign enablement, budget/bid/status change, PMax, Standard Shopping change, conversion-goal change, or live spend.

## Gate 2: Pinterest Event Quality And Paused US Drafts

Problem ID: `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`

Current status: `OWNER_APPROVAL_REQUIRED`

Surface:
- Advertiser: `549756244483`
- Account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
- Catalog: `Catalog_Retail`
- Catalog ID: `3041764155561548387`
- EN Shopify source/feed profile: `3041760867124595727`

Current evidence:
- Event Quality remains `Fair`, updated `2026-05-06`.
- Pinterest Tag status: `Fair`; Conversions API status: `Fair`.
- Latest stored official app activity: Tag `2026-05-08T05:50:56.502Z`; CAPI `2026-05-08T05:51:13.760Z`.
- Verified Merchant Program: `PASS`; Automatic Enhanced Match: `PASS`; Enhanced Match: `ERROR`.
- Top gaps: `product_id__ADD_PAYMENT_INFO`, `hashed_email__ADD_TO_CART`, `click_id_epik__CHECKOUT`.
- Clean US launch scope: `342` EN-US in-stock rows with `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready`.
- Product split: `210` Mommy & Me, `103` Family Matching, `29` Pajamas.
- Exact exclusions: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`.
- Prior campaign baseline: `0` campaigns, `0` currently serving, `$0.00` spend.

Tried, ruled, or routed paths:
- Tried: official Shopify Pinterest pixel set to Always on / share all events. Result: official path alive, but Event Quality still Fair.
- Tried: catalog proof repair. Result: old `337/346` blocker superseded by clean `342` rows and `4` explicit exclusions.
- Ruled out: including the four unresolved variants until they re-resolve in a fresh just-in-time proof.
- Ruled out: failed sitemap source `3041760916127467912`, localized Pinterest sources, and international Pinterest expansion before US measurement is cleaner.
- Ruled out: duplicate theme-level Pinterest tag, duplicate CAPI, or custom CAPI/customer-data change without separate approval.
- Ruled out: waiting passively as the only solution. If waiting is chosen, schedule a readback and keep parallel draft/repair work moving.

Exact next unblock action:
- Choose one of two separate approvals:
  - Paused US draft approval using only the clean `342` rows and four exclusions.
  - Narrow Event Quality repair approval focused only on official app/customer-events gaps.
- Live spend remains blocked while Event Quality is Fair unless the owner explicitly accepts that risk in a separate spend approval.

Paused draft approval phrase:

```text
APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.
```

Optional Event Quality repair approval phrase:

```text
APPROVE NARROW PINTEREST EVENT QUALITY REPAIR ONLY: INVESTIGATE OFFICIAL SHOPIFY/PINTEREST APP AND CUSTOMER EVENTS CONFIGURATION FOR PRODUCT ID, EMAIL, AND CLICK ID GAPS; NO CAMPAIGN, DRAFT, PRODUCT GROUP, CATALOG SOURCE, AUDIENCE, BUDGET, BID, STATUS, OR SPEND CHANGES; NO DUPLICATE THEME TAG; NO CUSTOM CAPI DEPLOYMENT OR CUSTOMER-DATA CHANGE WITHOUT A SEPARATE READBACK AND APPROVAL; READ BACK BEFORE AND AFTER.
```

Pre-readbacks before any approved paused Pinterest draft:
- Confirm one Pinterest writer owns the account surface.
- Read back advertiser `549756244483`: campaign count, currently serving count, spend, active/promoted objects, login/CAPTCHA/billing/unsaved prompts.
- Read back Event Quality: overall WEB, Tag, CAPI, updated date, latest Tag/CAPI timestamps, Verified Merchant Program, Automatic Enhanced Match, Enhanced Match, top action items.
- Revalidate clean scope and exclusions: `342` clean rows, `4` exclusions, no overlap, all clean rows `en-US` / `IN_STOCK`.
- Verify the EN Shopify source `3041760867124595727` is selected, not the failed sitemap source or localized feeds.

Post-readbacks after any approved paused Pinterest draft:
- All created objects are paused/draft only.
- Currently serving remains `0`.
- Spend remains `$0.00`.
- Product scope uses the `342` clean rows and excludes the four unresolved variants.
- No tag/CAPI/catalog/feed/audience/budget/bid/source/Merchant/Google Ads/Shopify product-data changes occurred outside approval.
- Event Quality is recorded again; live spend stays blocked if still Fair.

Stop conditions:
- Owner approval is missing or bundles live spend with draft creation.
- Fresh scope no longer reads `342` clean rows and four explicit exclusions.
- Pinterest prompts to enable, publish, launch, promote, set live budgets, or change bid activation.
- The selected source is sitemap/localized or otherwise not the EN Shopify source `3041760867124595727`.
- Draft setup requires tag/CAPI/customer-data/catalog-source changes not named in approval.

Expressly forbidden:
- Live Pinterest spend, serving enablement, budget or bid activation, campaign/ad/ad-group/product-group launch, catalog source edit, tag/CAPI/pixel changes, custom CAPI/token work, duplicate theme tag, audience change, Shopify product edit, Merchant write, Google Ads write, feed change, or including the four unresolved variants without fresh proof.

## Gate 3: Beach / Vacation Family Metadata Hold

Problem ID: `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`

Current status: `PARTIALLY_MITIGATED_LOCAL_ADS_HOLD__OWNER_APPROVAL_REQUIRED_FOR_SHOPIFY_FIX`

Surface:
- Shopify product: `7227378892897`
- Handle: `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`
- Theme in Ads packets: `Vacation Family`
- Known affected public metadata: HTML `<title>`, `og:title`, and `twitter:title`

Current evidence:
- Public product URL with `?variant=41871520661601&country=GB` returned HTTP `200`, retained `country=GB`, and showed a beach/vacation H1.
- The same page's `<title>`, `og:title`, and `twitter:title` were stale Christmas wording: `Family Matching Sets - Christmas Print | Dress Like Mommy`.
- A later low-volume scan found the same stale metadata in sampled ES, IT, RO, and PT localized routes.
- Local Ads risk is mitigated by the held CSV:
  - Source non-US Search CSV: `1666` rows.
  - Held CSV: `1496` rows.
  - Removed: all `Vacation Family - Exact` and `Vacation Family - Phrase` ad groups, keywords, and ads across all `17` non-US country campaigns.
  - Latest local validation: `0` hits for bad handle, product `7227378892897`, `Vacation Family`, US campaign `23827590655`, PMax, Standard Shopping, product/feed/conversion surfaces, enablement, or missing country params.

Tried, ruled, or routed paths:
- Tried: public metadata readback and expanded landing scan. Result: problem confirmed in English and sampled localized routes.
- Tried: local Google Ads URL hold. Result: safer `1496`-row held CSV excludes every Vacation Family row tied to the bad handle.
- Ruled out: sending live paid traffic to the stale URL.
- Ruled out: using the original `1666`-row non-US Search CSV as the preferred future import candidate while the metadata is stale.
- Ruled out: live Shopify SEO/social metadata edit without fresh action-time approval.
- Ruled out: broad product-data cleanup; this is a narrow SEO/social title repair unless later evidence proves a wider pattern.

Exact next unblock action:
- If the owner wants fastest paused non-US Search infrastructure, keep using the held `1496`-row CSV and leave Vacation Family excluded.
- If the owner wants Vacation Family restored, ask for the narrow Shopify SEO/social metadata approval below, then public-readback English plus localized title/OG/Twitter output before putting Vacation Family back into any Ads packet.

Shopify metadata repair approval phrase:

```text
APPROVE NARROW SHOPIFY PRODUCT SEO TITLE REPAIR ONLY FOR PRODUCT 7227378892897 / HANDLE matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set: READ BACK CURRENT TITLE, SEO TITLE, META DESCRIPTION, OG/TWITTER TITLE SOURCE, AND TRANSLATIONS FIRST; THEN CHANGE ONLY THE STALE CHRISTMAS SEO/SOCIAL TITLE METADATA TO BEACH/VACATION FAMILY OUTFIT WORDING; DO NOT CHANGE PRODUCT STATUS, HANDLE, PRICE, VARIANTS, INVENTORY, TAGS, VENDOR/SOURCE URL FIELDS, PUBLICATIONS, MERCHANT, GOOGLE ADS, PINTEREST, FEED LABELS, PRODUCT SCOPE, PRODUCT GROUPS, CONVERSION GOALS, BUDGETS, BIDS, CAMPAIGN STATUS, THEME, OR LIVE SPEND; READ BACK PUBLIC TITLE/OG/TWITTER TITLE AFTER.
```

Pre-readbacks before any approved Shopify metadata repair:
- Confirm one Shopify product-data writer owns the product surface.
- Admin/API readback for product title, SEO title, meta description, OG/Twitter title source, product ID, handle, status, publications, variants, price, tags, and translations.
- Public readback for English product URL title/OG/Twitter/H1.
- Public readback for localized sampled routes: ES, IT, RO, PT title/OG/Twitter/H1.
- Confirm no vendor/source URLs are present or introduced in title/body/SEO/metafields.
- Confirm held Ads CSV remains the active safe candidate until public metadata passes.

Post-readbacks after any approved Shopify metadata repair:
- English public product URL shows beach/vacation-specific title, `og:title`, and `twitter:title`; no stale Christmas wording.
- ES, IT, RO, and PT sampled public routes show localized or at least non-Christmas title/OG/Twitter behavior.
- Product status, handle, price, variants, tags, vendor/source fields, publications, Merchant, feed labels, product scope, product groups, conversion goals, budgets, bids, campaign statuses, theme, and live spend remain unchanged.
- A refreshed local Ads packet either keeps using the held CSV or explicitly validates re-adding Vacation Family after the public metadata pass.

Stop conditions:
- Owner approval is missing or does not name product `7227378892897`.
- The repair path requires product status, handle, price, variant, inventory, publication, tag, vendor/source URL, feed, Merchant, Ads, Pinterest, theme, budget, bid, conversion, or campaign-status changes.
- Public readback still shows stale Christmas title/OG/Twitter metadata after cooldown.
- Localized metadata readback regresses or introduces wrong-language/wrong-theme titles.

Expressly forbidden:
- Live Shopify product-data change without exact approval, handle change, price/variant/inventory/status/publication/tag/vendor/source URL change, Merchant upload/source edit, Google Ads preview/import/enablement, Pinterest write, feed-label/product-scope/product-group/conversion-goal change, budget/bid/status change, PMax, Standard Shopping change, theme edit, or live spend.

## Evidence Sources

- `ops/PROBLEM_TRACKER.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/MERCHANT_AGE_GROUP_EXACT_EXPORT_READBACK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/reconciliation/merchant-product-issues-paid-age-group-context-breakdown.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/merchant-us-es-readonly/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/merchant-us-es-repair/MERCHANT_US_ES_AGE_GROUP_REPAIR_APPROVAL_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_scope_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/pinterest-gate/PINTEREST_PAUSED_US_DRAFT_EVENT_QUALITY_GATE_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/PAID_GROWTH_URL_HOLD_CHECKOUT_SAFE_ADVANCE_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/landing-url-quality/LANDING_METADATA_QUALITY_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/GOOGLE_ADS_INTL_URL_HOLD_VALIDATION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/lanes/local-gates-and-validation/LOCAL_GATES_AND_VALIDATION_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/lanes/local-gates-and-validation/held_non_us_search_csv_validation.json`

## Parent Integration Notes

- Tracker drift was observed in existing evidence: the Merchant detailed problem status was stale/misaligned in one section as a Shopify/Ads-hold status, while the active summary correctly says `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`. Parent should reconcile this in `ops/PROBLEM_TRACKER.md`.
- Beach detailed tracker status in one section was older than the active summary; parent should keep the partially mitigated Ads-hold status plus the Shopify metadata approval gate.
- This worker did not edit `ops/PROBLEM_TRACKER.md`, `ops/AGENT_WORKLOG.md`, `ops/AGENT_COORDINATION.md`, `AGENTS.md`, or the canonical prompt.
