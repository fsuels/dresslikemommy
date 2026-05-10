# Paid-Growth AI-Army Safe Advance 2

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-ai-army-safe-advance-2`

Mode: parent/orchestrator with five parallel subagents on disjoint local/read-only lanes. No external account writes, live spend, campaign enablement, budget/bid/status changes, PMax enable, Standard Shopping changes, product-scope/feed-label/product-group changes, conversion-goal changes, Merchant uploads, Shopify live product-data edits, Pinterest writes, checkout payment/order, theme publish, or credential changes were made.

## Executive Result

The sprint moved safe growth infrastructure forward without crossing approval boundaries:

- Google Ads non-US paused Search packet remains structurally valid: `17` campaigns, `204` ad groups, `612` exact/phrase keywords, `629` negatives, `204` paused RSAs, `1666` web-bulk rows, max CPC `$0.15`, no US campaign `23827590655` rows, no PMax/Standard Shopping/product-scope/feed-label/product-group/conversion-goal rows. Future approval must use the canonical `TEST BUILD` wording.
- Localization/product landing checks passed for all `17` international target markets with one low-volume product-page GET per market, but live spend readiness remains `0` markets. GB/CA still need visual no-payment checkout UI; CH/DK/DE/NL/SE/FR/BE/PL/CZ/GR need checkout/shipping QA.
- Merchant US/es age_group repair is now a concrete approval packet, not a vague blocker. Preferred Path A is a narrow US/es age_group-only supplemental source for source `10627981690`; Path B is a source-specific official refresh only if the UI proves it is narrow.
- Pinterest remains ready for exact-owner-approved paused US drafts only: `342` clean EN-US rows, `4` excluded unresolved variants, Event Quality still `Fair`, live spend blocked.
- Economics/reporting controls are tightened around `$70` AOV, `650%` ROAS, max CPA `$10.77`, `$0.15` CPC requiring about `1.39%` CVR, and a `$16` no-purchase hard-pause rule.

## New Problem Found

`PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`

The paid-candidate beach/vacation product URL:

`https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601&country=GB`

returned HTTP `200`, retained `country=GB`, and showed a beach/vacation H1, but its `<title>`, `og:title`, and `twitter:title` were all `Family Matching Sets - Christmas Print | Dress Like Mommy`.

This should block live paid traffic to that URL until one of two safe paths happens:

- exact owner approval for a narrow Shopify product SEO/social-title repair on product `7227378892897`, with public readback after; or
- local-only Ads packet swap/exclusion for the `Vacation Family` final URL before any future approved paused import.

No Shopify product-data edit was made in this session.

## Lane Results

### Google Ads Intl Search

Report: `lanes/google-ads-intl/GOOGLE_ADS_INTL_PAUSED_BUILD_VALIDATION.md`

Status: `PASS_WITH_APPROVAL_GATE_SHARPENING`.

The importable packet is paused-only and non-US-only. The subagent found only documentation/template references to existing US campaign `23827590655`, not importable rows. The exact approval phrase in the canonical prompt should be used before any Google Ads preview/import.

### Localization / Checkout

Report: `lanes/localization-checkout/LOCALIZATION_CHECKOUT_READINESS_REPORT.md`

Status: product landing checks passed, spend blocked.

Strong paused-infra candidates with checkout or rate evidence: `GB`, `CA`, `AU`, `ES`, `IT`, `RO`, `PT`.

Product-landing-only paused shell candidates: `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `PL`, `CZ`, `GR`.

Live-spend-ready markets: `0`.

### Merchant US/es

Report: `lanes/merchant-us-es-repair/MERCHANT_US_ES_AGE_GROUP_REPAIR_APPROVAL_PACKET.md`

Status: `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`.

US/en remains solved with exact count `0`. US/es is separate: source `10627981690`, `625` paid item IDs / `1,250` rows. The packet defines two repair candidates, ruled-out paths, preflight readbacks, post-readbacks, fixed criteria, and exact approval language.

### Pinterest

Report: `lanes/pinterest-gate/PINTEREST_PAUSED_US_DRAFT_EVENT_QUALITY_GATE_REFRESH.md`

Status: paused draft possible only after exact owner approval; live spend blocked.

Clean scope remains `342` EN-US rows with `4` explicit exclusions. Event Quality is still `Fair`; Tag/CAPI are alive in stored evidence, but top gaps remain Product ID in AddPaymentInfo, Email in AddToCart, and Click ID in Checkout.

### Economics / Reporting

Report: `lanes/economics-reporting/ECONOMICS_REPORTING_OPERATOR_PACK.md`

Status: local-ready controls.

The operator pack adds CPA/CPC/CVR guardrails, first-72-hour kill/scale rules, weekly reporting columns, claim-safe creative themes, and an unsupported-claims blacklist.

## Approval Gates

Google Ads paused non-US Search:

`APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT CREATE OR EDIT US CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, PRESENCE-ONLY LOCATION TARGETING, CPC CAPS AT OR BELOW $0.20, AND KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY PRODUCT-DATA, PINTEREST, THEME, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT CHANGES; PREVIEW AND READ BACK BEFORE AND AFTER.`

Pinterest paused US drafts:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

Merchant US/es preferred Path A:

`APPROVE MERCHANT US/ES AGE_GROUP PATH A ONLY: CREATE OR UPDATE ONE AGE_GROUP-ONLY MERCHANT SUPPLEMENTAL SOURCE JOINED TO SOURCE 10627981690 / SHOPIFY APP API FOR FEED LABEL US, LANGUAGE ES, COUNTRY UNITED STATES, USING ONLY EXACT PREVIEWED PAID-COHORT ITEM IDS CURRENTLY FAILING MISSING AGE_GROUP AND ONLY COLUMNS ID AND AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO PRIMARY SOURCE EDIT, BROAD SOURCE REFRESH, OR NON-AGE_GROUP PRODUCT-DATA CHANGE; PREVIEW ROW SCOPE FIRST, APPLY ONLY IF PREVIEW MATCHES, AND READ BACK SOURCE PROCESSING, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.`

Shopify beach outfit SEO title repair:

`APPROVE NARROW SHOPIFY PRODUCT SEO TITLE REPAIR ONLY FOR PRODUCT 7227378892897 / HANDLE matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set: READ BACK CURRENT TITLE, SEO TITLE, META DESCRIPTION, OG/TWITTER TITLE SOURCE, AND TRANSLATIONS FIRST; THEN CHANGE ONLY THE STALE CHRISTMAS SEO/SOCIAL TITLE METADATA TO BEACH/VACATION FAMILY OUTFIT WORDING; DO NOT CHANGE PRODUCT STATUS, HANDLE, PRICE, VARIANTS, INVENTORY, TAGS, VENDOR/SOURCE URL FIELDS, PUBLICATIONS, MERCHANT, GOOGLE ADS, PINTEREST, FEED LABELS, PRODUCT SCOPE, PRODUCT GROUPS, CONVERSION GOALS, BUDGETS, BIDS, CAMPAIGN STATUS, THEME, OR LIVE SPEND; READ BACK PUBLIC TITLE/OG/TWITTER TITLE AFTER.`

## Next Best Action

The closest path to the North Star is to clear the highest-leverage approval-gated blockers in this order:

1. Fix or swap the beach/vacation URL before it is used in any paid build.
2. Clear Merchant US/es age_group only if Spanish US serving/future tests matter now; otherwise keep it parked with the exact gate and avoid redoing US/en.
3. Use the corrected Google Ads paused non-US Search approval gate if the owner wants infrastructure creation next.
4. Use the separate Pinterest paused US draft gate only after just-in-time readbacks; keep live Pinterest spend blocked while Event Quality is `Fair`.
5. Run GB/CA visual no-payment checkout UI QA, then one-country-at-a-time checkout/shipping QA for CH/DK/DE/NL/SE/FR/BE/PL/CZ/GR.

