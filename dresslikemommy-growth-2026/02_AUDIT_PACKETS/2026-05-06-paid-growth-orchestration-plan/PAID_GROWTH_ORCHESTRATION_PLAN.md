# Dress Like Mommy Paid Growth Orchestration Plan

Verified: 2026-05-06, America/New_York

## Executive Decision

Do not scale broadly or launch multilingual paid traffic yet. The profitable path is:

1. Keep paid traffic focused on purchase-tracked, shipping-supported, English-first markets.
2. Fix low-CPC Google governance before feeding more budget into automation.
3. Treat Pinterest as a capped visual discovery channel until its tag/catalog/CAPI gates are proven.
4. Use international orders from Denmark, the UK, and Switzerland as demand signals, not as permission to launch paid traffic in those countries before shipping, localization, returns, duties, and checkout proof are clean.

Ad strength matters, but it is not the business target. Purchase value, cost per order, product-level ROAS, and refund-adjusted contribution are the targets.

## Live Google Ads Readback

Date range visible in Google Ads: Apr 29-May 5, 2026.

Account total:
- Clicks: 90
- Impressions: 3,916
- Avg CPC: $0.22
- Cost: $19.88
- Primary conversions: 0.00
- Primary conversion value: $0.00

Campaigns:

| Campaign | Status | Budget | Bid strategy | Clicks | Cost | Avg CPC | Primary purchases | Finding |
|---|---:|---:|---|---:|---:|---:|---:|---|
| `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` | Eligible | $20/day | Manual CPC | 81 | $18.58 | $0.23 | 0 | Active spend is above the owner target CPC and has no attributed purchase yet. It is overdue for a cost-control review. |
| `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` | Bid strategy learning | $2/day | Maximize conversions | 9 | $1.30 | $0.14 | 0 | Posture drifted from the older continuity memory of $5/day Maximize clicks. Ads are Average/Poor, not Excellent. |
| `Search-105DLM_US_SEARCH_NONBRAND_20260503` | Paused | $2/day | Maximize conversions | 0 | $0.00 | n/a | 0 | Two paused RSAs are Poor and generic. Keep paused; rebuild before any launch. |
| `PMax: Shopping ads (United States)` | Paused | $1/day | PMax | 0 | $0.00 | n/a | 0 | Still has no-products/wrong-campaign risk. Do not repair in place. |
| `PMax: USA Google Shopping T-Shirts` | Paused | $1/day | PMax | 0 | $0.00 | n/a | 0 | Local readiness packet exists; live enable remains blocked. |
| `Remarketing - Cart Abandoners & Checkout Starters` | Paused | $1/day | Display | 0 | $0.00 | n/a | 0 | Warm remarketing packet exists, but live row still shows policy limitations. Recheck before enable. |

Conversion cleanup was completed separately on 2026-05-06. Purchase stayed Primary/dynamic/enhanced; non-purchase micro values were set to no value in Google Ads only.

## CPC Economics

Owner target: about $70 order value, 50% gross margin, target ROAS 650%.

Target CPA at 650% ROAS:

`$70 / 6.5 = $10.77`

Maximum CPC depends on conversion rate:

| Conversion rate | Max CPC before return friction |
|---:|---:|
| 1.0% | $0.11 |
| 1.5% | $0.16 |
| 2.0% | $0.22 |
| 3.0% | $0.32 |
| 4.0% | $0.43 |

Conclusion: $0.25 CPC is not mathematically impossible, but it requires stronger conversion rate/AOV proof. With 81 Shopping clicks, $18.58 spend, and 0 purchases in the readback window, the professional move is to reduce waste and isolate winners before scaling.

## Website And International Readiness

Public storefront readback found mixed-language issues on Spanish, French, German, and Danish homepages. A local theme patch was made for the homepage category/occasion strip and spotlight card labels/buttons in EN/ES/FR/DE/DA, but this does not make all localized pages paid-ready.

The shipping page still creates targeting risk:
- It says the store ships matching family outfits worldwide.
- The explicit supported-country list only names United States, Canada, United Kingdom, and Australia.
- Countries like Denmark and Switzerland have purchase signals, but paid traffic should wait for country-level shipping/returns/duties/checkout proof and localized landing-page QA.

The Spanish PDP for a recently corrected product also appeared stale in translation cache, still describing the old set/pants framing after English was corrected. That blocks localized paid PDP launches until translation sync/readback is done.

## Final Channel Strategy

### Google Ads

Immediate priority is not PMax scale. Immediate priority is clean purchase data, low-CPC governance, and product-level Shopping control.

1. Standard Shopping: run a just-in-time product/query/CPC review, then lower the max CPC cap to $0.18-$0.20 or pause/reduce if waste continues. Keep product scope unchanged unless separately approved.
2. Brand Search: repair the campaign posture and assets so the brand campaign is tight, low CPC, and deterministic. Do not let it drift into broad automation.
3. Nonbrand Search: keep the current paused Poor campaign paused. Rebuild into tightly themed ad groups with strong RSAs, exact/phrase keywords, negative keywords, and CPC control.
4. Remarketing: likely the best next cheap-intent lever, but only after policy readback confirms the active RDA is clean and the old limited/clickbait ads are not blocking the campaign.
5. PMax: hold until purchase volume and feed/product labels are stronger. PMax is powerful, but it is not the first tool for a strict low-CPC learning environment.

### Pinterest

Pinterest can produce cheaper visual discovery traffic, but it should not be treated as guaranteed conversion traffic.

1. First gate: confirm Pinterest account login, tag, checkout value, event dedupe, catalog approval, and product groups.
2. Start with a paused/draft US-only catalog-shopping structure or a very small live test after approval.
3. Do not use broad Performance+ Catalog Sales as the first test if exact product-cohort control is required. Official Pinterest docs say Performance+ Catalog Sales uses the All Products product group.
4. Prospecting cap should stay low until add-to-cart, checkout, and purchase quality proves out.

### International

Launch order:

1. US English: active optimization now.
2. UK/Canada/Australia English: only after country shipping/returns/currency/checkout proof and landing-page QA.
3. Denmark/Switzerland/other EU: hold as research opportunities. Add explicit shipping policy, duties/tax expectations, and localized or English-country landing pages before paid spend.
4. Non-English language campaigns: blocked until homepage, collection, PDP, cart, policies, checkout path, translation cache, and product-feed language quality pass QA.

## Implementation Queue

### Completed Today

- Live Google Ads readback for campaign posture and performance.
- Website readback for homepage, translations, shipping, swim collection, and product-page clarity.
- Parallel subagent audit of site/localization, paid-media packets, and official platform guidance.
- Local theme patch for homepage category/occasion/trust/spotlight label localization in EN/ES/FR/DE/DA.
- Local orchestration packet created.

### Next Live Work Requiring Explicit Approval

Use only one approval phrase at a time.

**Approval 1: Standard Shopping Cost Control**

`APPROVE STANDARD SHOPPING COST CONTROL REVIEW: READ BACK SEARCH TERMS, PRODUCTS, CPC, AND SPEND FIRST; LOWER MAX CPC CAP TO $0.20 OR LESS ONLY IF READBACK CONFIRMS NO PURCHASE VALUE; KEEP BUDGET, PRODUCT SCOPE, FEED LABELS, PRODUCT GROUPS, CONVERSION GOALS, AND CAMPAIGN STATUS UNCHANGED.`

Preferred implementation if approved: reduce CPC cap to $0.20 first, then reassess. If no purchase signal continues, consider $0.18 or pause only with a separate approval.

**Approval 2: Brand Search Governance Repair**

`APPROVE BRAND SEARCH GOVERNANCE REPAIR: READ BACK SETTINGS FIRST; RESTORE LOW-CPC BRAND PROTECTION POSTURE; IMPROVE OR PAUSE POOR BRAND RSA ASSETS; KEEP BUDGET AT OR BELOW $2/DAY; KEEP CPC CAP AT OR BELOW $0.15-$0.20 IF AVAILABLE; NO STANDARD SHOPPING, PMAX, REMARKETING, PRODUCT SCOPE, OR CONVERSION GOAL CHANGES.`

Blocked note: a stale Brand Search asset-upload claim from 2026-05-01 remains in `ops/AGENT_COORDINATION.md`; reconcile before live asset work.

**Approval 3: Paused Nonbrand Search Rebuild**

`APPROVE CREATE PAUSED NONBRAND SEARCH REBUILD ONLY: BUILD NEW TIGHT US-ENGLISH EXACT/PHRASE AD GROUPS WITH EXCELLENT-QUALITY RSAS, NEGATIVES, AND LOW-CPC CONTROLS; KEEP CAMPAIGN PAUSED; NO BUDGETED LAUNCH, PMAX, SHOPPING, PRODUCT SCOPE, OR CONVERSION GOAL CHANGES.`

**Approval 4: Pinterest Read-Only Gate**

`APPROVE PINTEREST READ-ONLY GATE: LOGIN AND READ BACK TAG, CATALOG, PRODUCT GROUPS, CHECKOUT VALUE, EVENT DEDUPE, AND EXISTING CAMPAIGNS ONLY; NO CAMPAIGN CREATION, ENABLE, BUDGET, TARGETING, OR CATALOG CHANGES.`

**Approval 5: Pinterest Paused Draft Build**

`APPROVE PINTEREST PAUSED US CATALOG TEST DRAFT ONLY: CREATE OR PREPARE PAUSED US-ONLY PRODUCT-GROUP CAMPAIGN STRUCTURE FOR MOMMY & ME, FAMILY MATCHING, AND PAJAMAS; KEEP ALL ADS PAUSED; NO LIVE SPEND, NO BROAD INTERNATIONAL TARGETING, NO PERFORMANCE+ ALL-PRODUCTS LAUNCH.`

## Official Platform Notes Used

- Google Performance Max overview and controls: https://support.google.com/google-ads/answer/10724817
- Google PMax listing groups: https://support.google.com/google-ads/answer/11596074
- Google final URL expansion exclusions: https://support.google.com/google-ads/answer/14337539
- Google PMax negative keywords: https://support.google.com/google-ads/answer/15726455
- Google AI Max for Search: https://support.google.com/google-ads/answer/15910187
- Google tROAS guidance: https://support.google.com/google-ads/answer/6268637
- Pinterest catalogs before launch: https://help.pinterest.com/en/business/article/before-you-get-started-with-catalogs
- Pinterest product-group promotion: https://help.pinterest.com/en/business/article/promote-your-product-groups
- Pinterest Performance+: https://help.pinterest.com/en/business/article/pinterest-performance-plus
- Pinterest API for Conversions: https://help.pinterest.com/en/business/article/the-pinterest-api-for-conversions

## Decision

`DO_NOT_SCALE_BROADLY_YET__FIX_LOW_CPC_GOVERNANCE_AND_LANGUAGE_COUNTRY_GATES_FIRST__STANDARD_SHOPPING_AND_BRAND_SEARCH_ARE_THE_NEXT_APPROVAL_CONTROL_POINTS`
