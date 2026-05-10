# Economics And Creative Safe Growth Pack

Date: 2026-05-08
Lane: economics + creative subagent
Decision: `LOCAL_READY_NO_EXTERNAL_WRITES`

## Scope

This pack combines the paid-growth economics guardrails with claim-safe creative guidance for the next controlled growth step.

No Google Ads, Pinterest, Merchant Center, Shopify Admin, feed, catalog, product data, campaign, import, enable, pause, budget, bid, product-scope, product-group, feed-label, conversion-goal, tag, CAPI, or live-spend action was taken.

Write scope stayed inside:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-safe-followup/lanes/economics-creative/`

## Inputs Used

- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/GROWTH_NORTH_STAR.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/roas/ROAS_CONTROLLED_GUARDRAILS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/roas/cpc_cvr_guardrails.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/ADS_INTL_COUNTRY_URL_PACKET_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/country_tier_plan.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/localization/country_readiness.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/creative/CREATIVE_CONTROLLED_COPY_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`

## Core Economics

Planning formula:

`max CPA = AOV / target ROAS`

With a `$70.00` AOV and `650%` target ROAS:

| Item | Value |
|---|---:|
| AOV scenario | `$70.00` |
| Target ROAS | `650%` |
| Max CPA | `$10.77` |
| 50% margin/non-marketing cost scenario | `$35.00` |
| Contribution after target CPA, before returns/chargebacks/reships | `$24.23` |

Practical read:

- `$10.77` is the normal target-CPA ceiling only when tracking, landing page, product scope, and query quality are clean.
- `$9.49-$9.73` remains the conservative stop/decision band for weaker international, mixed-language, stale-catalog, or uncertain tracking cases.
- Owner preference for CPC near or below `$0.20` is economically sound: at `$0.20`, traffic needs about `1.86%` CVR to hold `650%` ROAS on `$70` AOV.
- The current international Search packet cap of `$0.15` requires about `1.39%` CVR. That is feasible only for high-intent exact/phrase traffic with clean landing pages.

## CPC And CVR Guardrail

| CPC | Required CVR For `$10.77` CPA | Clicks Per Target CPA | Operating Read |
|---:|---:|---:|---|
| `$0.04` | `0.37%` | `269` | Current low-bid Shopping math can work, but only if product/query quality is clean. |
| `$0.08` | `0.74%` | `135` | Good discovery cap for lower-CPC countries if pages and checkout pass. |
| `$0.10` | `0.93%` | `108` | Strong cold-test target for high-intent exact/phrase. |
| `$0.12` | `1.11%` | `90` | Good cap for high-value watchlist and broader EU paused tests. |
| `$0.15` | `1.39%` | `72` | Current Search cap. Do not use for broad or weak traffic. |
| `$0.20` | `1.86%` | `54` | Upper edge. Use only after proof of CVR and clean purchase value. |

## Starting Budget Recommendations

These are recommendations for future owner-approved paused builds or later owner-approved activation. They are not authorization to import, enable, edit, or spend.

| Surface | Countries | Starting Budget If Later Spend-Approved | CPC / Effective CPC Guardrail | Notes |
|---|---|---:|---:|---|
| Existing US nonbrand Search | `US` | `$2/day` | `$0.15` | Campaign `23827590655` already exists paused. Do not duplicate. |
| Priority English Search | `GB`, `CA`, `AU` | `$2/day` each | `$0.15` | Best first non-US candidates after country presentment, shipping, Ads, tracking, and catalog readbacks. |
| High-value watchlist Search | `CH`, `DK` | `$1/day` each | `$0.12-$0.15` | Use English shells only until local route/language/checkout QA passes. |
| Broader EU Search | `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT` | `$1/day` each | `$0.10-$0.12` | ES/IT have localized URL evidence, but live spend still needs catalog/tracking/economics gates. |
| Lower-CPC discovery Search | `PL`, `CZ`, `RO`, `GR`, `PT` | `$1/day` each | `$0.08-$0.10` | PT and RO localized route evidence exists; RO presents in RON, so normalize currency before ROAS decisions. |
| Pinterest US catalog/retargeting draft | `US` only | `$1/day` only after separate spend approval | Plan to keep effective CPC near `$0.10-$0.15` | Use the clean `342` EN-US scope and exclude the `4` unresolved variants. Event Quality `Fair` remains a spend gate. |

Portfolio cap:

- First spend wave should add no more than `$5/day` incremental spend unless the parent explicitly approves a wider test.
- Until the first clean purchase-value readback, keep all new approved tests at or below `$10-$15/day` total incremental spend.
- Full international discovery should remain at or below `$20/day` incremental spend until at least one country proves purchase CPA near or below target.

## Country Tier Guidance

| Tier | Countries | Recommended Next Safe Action | Spend Posture |
|---|---|---|---|
| Existing governed US | `US` | Use existing paused nonbrand Search as the template; do not duplicate. Keep Standard Shopping unchanged. | No new spend without explicit activation approval. |
| Priority English | `GB`, `CA`, `AU` | Best candidates for paused Search shells because English copy can be used while route/currency/shipping is read back. | `$2/day` each only after approval and just-in-time readbacks. |
| High-value watchlist | `CH`, `DK` | Keep paused English shells; defer local-language copy until route, checkout, duties/returns clarity, and native QA pass. | `$1/day` first, then owner decision. |
| Broader ecommerce | `DE`, `NL`, `SE`, `FR`, `BE` | English-only shells are safer than local-language launches until language QA clears. | `$1/day`, lower CPC caps, strict query review. |
| Localized candidates | `ES`, `IT`, `RO`, `PT` | Use country-qualified localized product URLs only. Do not use bare language URLs. | `$1/day` only after catalog, tracking, economics, and approval gates pass. |
| Lower-CPC discovery | `PL`, `CZ`, `GR` | Paused English discovery shells only until language/checkout/currency QA exists. | `$1/day`, `$0.08-$0.10` CPC target. |
| Hold/extra QA | Arabic, Hebrew, Japanese, Korean, mixed-language markets | Do not prepare spend-facing copy until landing language and checkout QA pass. | Hold. |

Important Merchant gate: US Spanish `Missing age group` rows are still an active problem in the current memory. Do not use US/es Spanish-language paid traffic until the US/es source path is diagnosed.

## Kill Rules

Use the smallest relevant unit available: ad group, country, campaign, product group, or Pinterest ad set. Do not let blended account averages hide a losing country or theme.

Search kill rules:

- At about `$5` spend with weak search terms, irrelevant intent, or no qualified product engagement: pause, narrow, or add negatives after approval.
- At `$9.49-$10.77` spend with `0` purchases: force a pause, narrowing pass, or owner decision. Use `$9.49-$9.73` for international or weaker evidence.
- At `$16` spend with `0` purchases: hard pause the unit.
- After `2` purchases, hold or reduce if CPA is above `$10.77` or ROAS is below `650%`.
- Do not scale from CTR, add-to-cart, checkout starts, saves, or cheap CPC alone.

Pinterest kill rules:

- Do not spend if Event Quality remains stale/Fair without a parent owner-decision, item proof is missing, USA-only scope is not verified, or the 342/4 scope is not preserved.
- At `$5` spend with no qualified outbound clicks, saves, product engagement, add-to-cart, or checkout evidence: pause or rebuild targeting/creative.
- At `$9.49-$10.77` spend with `0` purchases: pause unless the parent explicitly approves one tightly capped retargeting window based on strong checkout evidence.
- At `$16` spend with `0` purchases: hard pause.
- Do not scale from saves, impressions, outbound clicks, or checkout starts alone.

Scale rules:

- Require at least `3` purchases in the unit being scaled.
- Require primary purchase value, correct currency, and clean transaction IDs.
- Require CPA at or below `$10.77` or ROAS at or above `650%`.
- Prefer CPA below `$8.75` or ROAS at or above `800%` before a larger increase.
- Future budget increases should be `10%-20%` for borderline winners and `20%-30%` for clean winners, no more often than every `3-7` days.

## Claim-Safe Google RSA Themes

Safe message territory:

- Coordinated family looks for photos, vacations, birthdays, holidays, beach trips, pool days, and family moments.
- Mommy & me dresses, daddy & me outfits, family pajamas, family swimwear, and full-family matching outfits.
- Choose separate sizes for each person.
- Browse styles by theme or occasion.
- Dress Like Mommy brand/store language is acceptable when pointing to owned brand pages, but avoid implying local inventory or physical retail.

Reusable English headline ideas, all kept short for RSA limits:

- `Matching Family Outfits`
- `Mommy & Me Dresses`
- `Family Photo Outfits`
- `Vacation Family Looks`
- `Pick Sizes Separately`
- `Daddy & Me Outfits`
- `Family Pajama Ideas`
- `Matching Swimwear`
- `Coordinated Looks`
- `Dress Like Mommy`

Reusable English descriptions:

- `Browse coordinated family styles for photos, vacations and special days.`
- `Choose separate sizes for each person and build a matching look.`
- `Find mommy and me, daddy and me, pajamas, swimwear and family outfits.`
- `Keep new country tests paused until tracking, catalog and checkout gates pass.`

Localized creative posture:

- `ES`, `IT`, `RO`, and `PT` may use local-language draft concepts only with country-qualified product URLs and fresh readbacks.
- `RO` must be evaluated in RON or with documented FX normalization.
- Other markets should use English-only paused shells or remain held until language QA exists.

## Claim-Safe Pinterest Themes

Use visual planning angles, not urgency or unverified performance claims:

- Mommy & me dress ideas for photos, birthdays, vacations, and family moments.
- Matching family outfit ideas for parents planning portraits, trips, or special days.
- Family vacation outfit ideas for beach, resort, and sunny plans.
- Matching family pajama ideas for cozy mornings, holidays, and snapshots.
- Coordinated swimwear ideas for beach days, pool trips, and vacations.
- Daddy & me outfit ideas for father-child photos and family plans.
- Warm retargeting: revisit coordinated family looks. Do not imply cart urgency, discount, or availability.

Pinterest US scope:

- Future paused US drafts should use only the clean `342` EN-US rows.
- Keep the `4` unresolved Pinterest-specific variants excluded unless a fresh just-in-time proof re-resolves them.
- Event Quality `Fair` remains a live-spend gate. A paused draft build may still be useful after exact approval, but spend should remain separately gated.

## Do Not Use These Claims Yet

- Fast shipping, rush shipping, quick delivery, same-day delivery, or guaranteed delivery dates.
- Warehouse, local stock, stocked inventory, store pickup, nearby inventory, or guaranteed on-hand stock.
- Bestseller, most popular, top-rated, viral, trending, or customer-favorite claims.
- Review counts, star ratings, or customer-volume claims.
- Sale, discount, limited-time offer, coupon, free gift, or promotion claims.
- Guaranteed fit, guaranteed availability, or no-risk returns.

## Evidence Needed Before Stronger Claims

| Stronger Claim Type | Evidence Required Before Use |
|---|---|
| Fast shipping or delivery timing | Market-specific checkout delivery estimates, shipping-policy source text, fulfillment/provider proof, and recent order delivery evidence. |
| Free shipping | Country-specific checkout rate readback and current policy/source confirmation. Do not call outbound shipping "returns." |
| Discounts or promotions | Live storefront promo evidence, approved offer terms, start/end dates, coupon rules, and destination-page consistency. |
| Reviews or ratings | Live review system evidence, count/rating source, product or brand scope, and screenshot/API readback. |
| Bestseller or popular | Recent sales/order evidence by SKU/category, date range, and clear definition of the comparison set. |
| Price claims | Live PDP price and currency readback for the target country, including variant-level price if relevant. |
| Availability | Feed/PDP eligibility proof only. Do not translate channel availability into warehouse, stocked, local inventory, or guaranteed-on-hand claims. |
| Local-language quality | Native or high-confidence QA of landing page, policy, cart, checkout, sizing, and customer-support wording. |

## Next Safe Growth Step

Best next parent action, without live spend:

1. Request the existing exact approval gate for paused non-US Google Search infrastructure only, separated from Pinterest.
2. If approved, create/import only paused Search test campaigns from the already validated packet, with no enablement and no Standard Shopping/PMax/conversion/feed/product-scope edits.
3. For Pinterest, request a separate paused US-only catalog/retargeting draft approval using the clean `342` scope and `4` exclusions; keep live spend gated while Event Quality is `Fair`.
4. Before any spend, run just-in-time readbacks for purchase tracking, country final URLs, checkout/currency, Merchant/Pinterest catalog health, and campaign settings.

Closest spend test after approvals and readbacks:

- Start with either existing US nonbrand Search at `$2/day`, or one priority English market at `$2/day`.
- Do not activate a wide international bundle at once.
- Keep Pinterest at paused draft only until Event Quality and item proof are accepted by the parent/owner.

