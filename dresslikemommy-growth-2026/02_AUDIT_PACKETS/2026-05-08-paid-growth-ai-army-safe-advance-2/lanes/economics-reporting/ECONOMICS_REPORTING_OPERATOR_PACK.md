# Economics, Creative, And Reporting Operator Pack

Date: 2026-05-08
Lane: economics-reporting subagent
Decision: `LOCAL_READY_NO_EXTERNAL_WRITES`

## Scope

This pack tightens the local operating controls for 650% ROAS growth decisions. It does not authorize or perform Google Ads, Merchant Center, Shopify Admin, Pinterest, feed, catalog, campaign, budget, bid, status, conversion-goal, product-scope, product-group, tag, CAPI, theme, checkout, or live-spend changes.

Write scope stayed inside:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/economics-reporting/`

## Inputs Used

- `AGENTS.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/GROWTH_NORTH_STAR.md`
- `ops/GOOGLE_ADS_CONTINUITY.md`
- `ops/AGENT_COORDINATION.md`
- `ops/PROBLEM_TRACKER.md`
- Prior May 8 ROAS, creative, and measurement packets under `2026-05-08-paid-growth-controlled-infra-refresh/`, `2026-05-08-paid-growth-safe-followup/`, and `2026-05-08-paid-growth-orchestrated-safe-advance/`.

## Core Guardrail Math

Formula: `max CPA = AOV / target ROAS`.

At the current planning AOV of `$70.00` and target ROAS `650%`, max CPA is `$10.77`. With the planning `50%` non-marketing cost model, gross profit before ads is `$35.00`, leaving about `$24.23` contribution after target ad spend before refunds, chargebacks, reships, duties friction, or support drag.

Operating thresholds at `$70.00` AOV:

| CPC | Required CVR | Clicks Per Target CPA | Read |
|---:|---:|---:|---|
| `$0.04` | `0.37%` | `269` | Current low-bid Shopping math can work only with clean product/query quality. |
| `$0.08` | `0.74%` | `135` | Good discovery ceiling for lower-CPC countries after readiness gates. |
| `$0.10` | `0.93%` | `108` | Strong cold-test cap for high-intent exact/phrase traffic. |
| `$0.12` | `1.11%` | `90` | Good cap for watchlist and broader EU tests. |
| `$0.15` | `1.39%` | `72` | Current Search packet cap; needs real buyer intent. |
| `$0.20` | `1.86%` | `54` | Upper edge; use only after CVR proof. |
| `$0.25` | `2.32%` | `43` | Expensive for this model; not for unproven cold traffic. |

Use `$9.49-$9.73` as the conservative decision band when tracking, localization, duties, catalog, language, or product mix is weaker. Use `$10.77` only when primary purchase value, final URLs, query quality, and catalog health are clean.

## First 72-Hour Rules

These rules apply after a future owner-approved activation. They are not authorization to activate anything.

| Time Window | Kill Or Narrow | Hold | Scale |
|---|---|---|---|
| Preflight | Do not launch if purchase value, final URL country, Merchant/Pinterest proof, or no-payment checkout readback is stale. | Keep paused and refresh readbacks. | No scale. |
| 0-24 hours | At about `$5` spend with weak terms, broad intent, irrelevant products, or no qualified engagement, narrow or pause the smallest unit. | If spend is below `$5` and terms are clean, keep collecting. | No scale before `3` purchases. |
| 24-48 hours | At `$9.49-$10.77` spend with `0` purchases, force pause, narrow, or owner decision. Use the lower band for weaker international lanes. | If 1 purchase appears, evaluate CPA, AOV, search terms, and checkout evidence before changing anything. | Still no scale unless `3+` clean purchases and primary value pass. |
| 48-72 hours | At `$16` spend with `0` purchases, hard pause the unit. For Standard Shopping monitoring, `$16-$20` post-bid-change with `0` purchases should trigger rollback decision. | Hold only with clean evidence and explicit owner decision. | Scale only `10%-20%` for borderline winners or `20%-30%` for clean winners, no more often than every `3-7` days. |

Smallest unit means ad group, country, campaign, product group, Pinterest ad group, product set, or theme, whichever exposes the loss most clearly.

Do not scale from CTR, add-to-cart, checkout starts, saves, impressions, outbound clicks, or cheap CPC alone.

## Weekly Reporting Columns

Use `weekly_reporting_columns.csv` as the operator schema. The weekly review must separate Google Search, Standard Shopping, Pinterest, country, product/theme, and campaign status so blended averages cannot hide losers.

Minimum decision fields:

- Spend, clicks, impressions, CTR, average CPC.
- Primary purchase conversions, conversion value, ROAS, CPA, AOV, purchase CVR.
- Country, currency, language, final URL country parameter, and FX normalization status.
- Search terms or product/theme cluster.
- Merchant/Pinterest catalog status and issue count.
- Tracking freshness, event quality, and conversion-action notes.
- Action taken, action reason, owner approval reference, and next review date.

Use primary purchase value for ROAS decisions. Do not use historical all-conversion value from periods before micro-conversion value cleanup as the main ROAS source.

## Claim-Safe Creative Themes

Google Search safe territory:

- Coordinated family looks for photos, vacations, birthdays, holidays, beach trips, pool days, and family moments.
- Mommy and me dresses, daddy and me outfits, family pajamas, family swimwear, and family matching outfits.
- Choose separate sizes for each person.
- Browse by theme, person, or occasion.
- `Dress Like Mommy` and `Official Site` language when pointing to owned pages.

Pinterest safe territory:

- Visual planning ideas for family photos, vacations, birthdays, holidays, beach, pool, pajamas, and father-child or mother-child matching.
- Warm product-viewer reminders that say "revisit" or "browse" without cart urgency.
- USA-only catalog/retargeting draft posture using the clean `342` EN-US scope and excluding the `4` unresolved variants unless fresh proof re-resolves them.

Localized posture:

- ES, IT, RO, and PT can have local-language draft concepts only with country-qualified product URLs and just-in-time readbacks.
- RO presents in RON; ROAS needs native RON reporting or documented FX normalization before comparison to USD planning thresholds.
- Other markets should use English-first paused shells or stay in QA hold until language and checkout quality pass.

## Unsupported Claims Blacklist

Do not use these claims in ads, draft ads, listing copy, reports intended for upload, or channel-visible feed language unless fresh evidence exists and the owner approves the specific claim:

- Fast shipping, rush shipping, same-day shipping, guaranteed delivery date.
- Warehouse, store pickup, local stock, stocked inventory, nearby inventory, guaranteed on-hand stock.
- Bestseller, most popular, top-rated, viral, trending, customer favorite.
- Review counts, star ratings, customer-volume claims.
- Sale, discount, coupon, limited-time offer, free gift, promo claim.
- Guaranteed fit, guaranteed availability, no-risk returns.
- Catalog-size claims such as "200+ styles" unless the live destination and data prove the exact scope.
- Free outbound shipping as an ad claim unless the target country, checkout rate, and policy/source text are current. Do not confuse outbound shipping rates with return shipping.

## Files In This Lane

- `ECONOMICS_REPORTING_OPERATOR_PACK.md`
- `cpa_cpc_cvr_guardrails.csv`
- `first_72_hour_rules.csv`
- `weekly_reporting_columns.csv`
- `claim_safe_creative_themes.csv`
- `unsupported_claims_blacklist.csv`
- `summary.json`

## Residual Risks

- This pack is local strategy and reporting control only. It does not prove live platform policy approval, current spend, purchase volume, Merchant/Pinterest health, native-language quality, or profitability.
- Live spend remains blocked until exact owner approval and just-in-time readbacks.
- Merchant US/es age_group and Pinterest Event Quality remain separate active approval-gated lanes.
