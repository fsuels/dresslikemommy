# Local Gates And Validation Report

Generated: 2026-05-09

Worker: Local-Gates / local-only validation lane.

Lane path: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/lanes/local-gates-and-validation/`

Decision: `PASS_LOCAL_ONLY_APPROVAL_GATED`

No external accounts, public checkout, Shopify Admin, Merchant Center, Google Ads, Pinterest, theme, feed, product, budget, bid, status, conversion-goal, product-scope, feed-label, product-group, or live-spend action was opened or changed by this worker.

## Inputs

- Canonical prompt: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- Problem tracker: `ops/PROBLEM_TRACKER.md`
- Coordination registry: `ops/AGENT_COORDINATION.md`
- Google Ads continuity: `ops/GOOGLE_ADS_CONTINUITY.md`
- Current packet README: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/README.md`
- Held CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`
- Prior Ads hold evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/GOOGLE_ADS_INTL_URL_HOLD_VALIDATION.md`
- Prior held CSV revalidation: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/ads-held-csv/HELD_ADS_CSV_VALIDATION.md`
- Merchant US/es evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/merchant-us-es-readonly/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md`
- Pinterest clean scope evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`
- Merchant/Pinterest gate synthesis: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/merchant-pinterest-gates/MERCHANT_PINTEREST_APPROVAL_GATES.md`
- Beach metadata evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/landing-url-quality/LANDING_METADATA_QUALITY_REPORT.md`

## Held CSV Validation

Script: `validate_held_non_us_search_csv.py`

Result JSON: `held_non_us_search_csv_validation.json`

Overall result: `PASS`

| Check | Result |
|---|---:|
| Data rows | `1496` |
| Header columns | `95` |
| Actions | `1496 Add` |
| Campaigns | `17` |
| Non-US locations | `17` |
| Campaign rows | `17` |
| Ad group rows | `170` |
| Positive keyword rows | `510` |
| Campaign negative keyword rows | `629` |
| Responsive search ad rows | `170` |
| Final URL rows | `680` |
| Final URL country params | `40` rows each for `AU`, `BE`, `CA`, `CH`, `CZ`, `DE`, `DK`, `ES`, `FR`, `GB`, `GR`, `IT`, `NL`, `PL`, `PT`, `RO`, `SE` |
| Campaign budgets observed | `$1.00`, `$2.00` |
| CPC values observed | `$0.10`, `$0.12`, `$0.15` |
| Max CPC | `$0.15` |
| Existing entity ID columns populated | `0` |
| Importable non-paused entity rows | `0` |

Status readback:

| Entity | Status |
|---|---|
| Campaigns | `17 Paused` |
| Ad groups | `170 Paused` |
| Keywords | `510 Paused` |
| Ads | `170 Paused` |
| Negative keywords | `629` rows, counted separately because this export has no negative-keyword status field |

Forbidden scan:

| Forbidden item | Hits |
|---|---:|
| US campaign `23827590655` | `0` |
| US campaign names / United States location | `0` |
| Bad beach handle | `0` |
| Product `7227378892897` | `0` |
| `Vacation Family` rows | `0` |
| `PMax` / `Performance Max` | `0` |
| `Standard Shopping` / `Shopping ads` | `0` |
| Product-scope rows | `0` |
| Feed/feed-label rows | `0` |
| Product-group rows | `0` |
| Conversion-goal rows | `0` |
| Merchant rows | `0` |
| Final URLs missing `country` | `0` |
| CPC over `$0.20` | `0` |

Finding: the held CSV remains a local-only, paused, non-US Search build candidate. It still excludes the beach/Vacation Family URL risk and still contains no import/create/edit rows for the existing US nonbrand campaign, PMax, Standard Shopping, product/feed/conversion surfaces, or live enablement.

## Approval Gates

### Merchant US/es Age Group

Problem: `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`

Current status: `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`

Known state:

- Original paid-cohort `US` / `en` / `United States` age_group issue is solved and must not be redone.
- Remaining issue is isolated to Merchant account `124884876`, source `10627981690` / `Shopify App API`, feed label `US`, language `es`, country `United States`.
- Exact scope from prior evidence: `625` paid item IDs / `1,250` issue rows.
- Product-detail RPC proof showed affected US/es samples missing effective `n:age_group`; one control sample on the same source was clean.

Exact approval gate from the canonical prompt:

```text
APPROVE MERCHANT US/ES AGE_GROUP REPAIR REVIEW FOR SOURCE 10627981690: READ BACK THE US/ES PRODUCT DETAIL AND SOURCE STATE FIRST; THEN USE ONLY THE NARROWEST SAFE OFFICIAL REPAIR PATH FOR US FEED LABEL / ES LANGUAGE / UNITED STATES MISSING AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO BROAD SOURCE REFRESH, MERCHANT UPLOAD, SOURCE EDIT, OR SHOPIFY DATA EDIT WITHOUT A PREVIEW, EXACT ROW SCOPE, AND POST-READBACK.
```

Preferred narrow Path A approval from existing gate evidence:

```text
APPROVE MERCHANT US/ES AGE_GROUP PATH A ONLY: CREATE OR UPDATE ONE AGE_GROUP-ONLY MERCHANT SUPPLEMENTAL SOURCE JOINED TO SOURCE 10627981690 / SHOPIFY APP API FOR FEED LABEL US, LANGUAGE ES, COUNTRY UNITED STATES, USING ONLY EXACT PREVIEWED PAID-COHORT ITEM IDS CURRENTLY FAILING MISSING AGE_GROUP AND ONLY COLUMNS ID AND AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO PRIMARY SOURCE EDIT, BROAD SOURCE REFRESH, OR NON-AGE_GROUP PRODUCT-DATA CHANGE; PREVIEW ROW SCOPE FIRST, APPLY ONLY IF PREVIEW MATCHES, AND READ BACK SOURCE PROCESSING, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.
```

### Pinterest Event Quality And Paused Drafts

Problem: `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`

Current status: `OWNER_APPROVAL_REQUIRED`

Known state:

- Old `337/346` Pinterest catalog blocker is superseded.
- Clean US Pinterest scope is `342` EN-US in-stock rows, with `4` explicit unresolved variant exclusions.
- Excluded variants: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`.
- Event Quality remains `Fair`; official Tag and CAPI are alive, but live spend remains gated.
- `Fair` is not a blocker to exact-owner-approved paused draft creation, but it is a spend gate unless the owner accepts the risk or approves a narrow Event Quality repair.

Exact paused draft approval gate:

```text
APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.
```

Optional separate Event Quality repair gate:

```text
APPROVE NARROW PINTEREST EVENT QUALITY REPAIR ONLY: INVESTIGATE OFFICIAL SHOPIFY/PINTEREST APP AND CUSTOMER EVENTS CONFIGURATION FOR PRODUCT ID, EMAIL, AND CLICK ID GAPS; NO CAMPAIGN, DRAFT, PRODUCT GROUP, CATALOG SOURCE, AUDIENCE, BUDGET, BID, STATUS, OR SPEND CHANGES; NO DUPLICATE THEME TAG; NO CUSTOM CAPI DEPLOYMENT OR CUSTOMER-DATA CHANGE WITHOUT A SEPARATE READBACK AND APPROVAL; READ BACK BEFORE AND AFTER.
```

### Beach / Vacation Family Metadata

Problem: `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`

Current status: `PARTIALLY_MITIGATED_LOCAL_ADS_HOLD__OWNER_APPROVAL_REQUIRED_FOR_SHOPIFY_FIX`

Known state:

- Product `7227378892897` / handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` has stale Christmas title/OG/Twitter metadata on a beach/vacation paid-candidate URL.
- Stale metadata was observed in English and sampled ES/IT/RO/PT localized routes.
- Local Ads risk is mitigated by the held `1496`-row CSV, which removes all `Vacation Family` ad groups, keywords, and ads tied to this handle.
- Do not send live paid traffic to this URL unless repaired and publicly read back, or keep using the held/excluded URL packet.

Exact Shopify metadata repair approval gate:

```text
APPROVE NARROW SHOPIFY PRODUCT SEO TITLE REPAIR ONLY FOR PRODUCT 7227378892897 / HANDLE matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set: READ BACK CURRENT TITLE, SEO TITLE, META DESCRIPTION, OG/TWITTER TITLE SOURCE, AND TRANSLATIONS FIRST; THEN CHANGE ONLY THE STALE CHRISTMAS SEO/SOCIAL TITLE METADATA TO BEACH/VACATION FAMILY OUTFIT WORDING; DO NOT CHANGE PRODUCT STATUS, HANDLE, PRICE, VARIANTS, INVENTORY, TAGS, VENDOR/SOURCE URL FIELDS, PUBLICATIONS, MERCHANT, GOOGLE ADS, PINTEREST, FEED LABELS, PRODUCT SCOPE, PRODUCT GROUPS, CONVERSION GOALS, BUDGETS, BIDS, CAMPAIGN STATUS, THEME, OR LIVE SPEND; READ BACK PUBLIC TITLE/OG/TWITTER TITLE AFTER.
```

### Non-US Paused Google Search Import

Current status: `LOCAL_PACKET_PASS__OWNER_APPROVAL_REQUIRED_BEFORE_PREVIEW_OR_IMPORT`

The current safer candidate is the held `1496`-row CSV validated above. Any Google Ads preview/import/create step still requires exact owner approval and parent-owned readbacks.

Exact approval gate from the canonical prompt:

```text
APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT CREATE OR EDIT US CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, PRESENCE-ONLY LOCATION TARGETING, CPC CAPS AT OR BELOW $0.20, AND KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY PRODUCT-DATA, PINTEREST, THEME, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT CHANGES; PREVIEW AND READ BACK BEFORE AND AFTER.
```

## Files Changed

- `validate_held_non_us_search_csv.py`
- `held_non_us_search_csv_validation.json`
- `LOCAL_GATES_AND_VALIDATION_REPORT.md`

All files are under this lane path only.

## Verification Commands Run

```bash
python3 -m py_compile dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/lanes/local-gates-and-validation/validate_held_non_us_search_csv.py
python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/lanes/local-gates-and-validation/validate_held_non_us_search_csv.py
```

## Problem Tracker / Worklog

Per worker lane restrictions, this worker did not update:

- `ops/PROBLEM_TRACKER.md`
- `ops/AGENT_WORKLOG.md`
- `ops/AGENT_COORDINATION.md`
- `AGENTS.md`
- Canonical prompt

Parent integration should record this lane as a local-only validation pass and attach this report plus `held_non_us_search_csv_validation.json`.

## Recommended Next Safe Action

Parent should integrate this lane, then choose one exact approval gate rather than bundling surfaces. If the goal is fastest paused growth infrastructure, the cleanest next owner request is the paused non-US Google Search `TEST BUILD` gate using the held `1496`-row CSV, followed by preview/readback before and after. Merchant US/es, Pinterest, and beach metadata should remain separate exact approval gates.

No non-US market is live-spend-ready from this lane alone.
