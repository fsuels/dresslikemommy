# ROAS Reporting Decision Control Pack

Generated: 2026-05-09

Lane: `roas-reporting-controls`

Decision: `LOCAL_READY_NO_EXTERNAL_WRITES`

## Scope

This is a local/read-only operator control pack for the paid-growth sprint. It consolidates the latest Standard Shopping metrics readback, prior economics guardrails, and reporting controls for future owner-approved tests.

No external account writes, campaign imports, campaign enablement, budget edits, bid edits, status edits, product-scope changes, product-group changes, feed-label changes, conversion-goal changes, Merchant uploads, Shopify changes, Pinterest changes, or theme changes were made.

## Evidence Used

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/PAID_GROWTH_NL_UI_STANDARD_POST_MAY6_SAFE_ADVANCE_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/lanes/standard-shopping-post-may6-readback/STANDARD_SHOPPING_POST_MAY6_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/lanes/standard-shopping-post-may6-readback/summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-checkout-standard-metrics-safe-advance/lanes/standard-shopping-metrics-readback/STANDARD_SHOPPING_METRICS_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/roas/ROAS_CONTROLLED_GUARDRAILS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/roas/cpc_cvr_guardrails.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-safe-followup/lanes/economics-creative/ECONOMICS_AND_CREATIVE_SAFE_GROWTH_PACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/economics-reporting/ECONOMICS_REPORTING_OPERATOR_PACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance/lanes/local-gates-and-validation/held_non_us_search_csv_validation.json`

## Standard Shopping Current Read

Campaign: `23802638621` / `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`

Current readback posture:

| Window | Clicks | Impressions | Cost | Avg CPC | Conversions | Conversion value |
|---|---:|---:|---:|---:|---:|---:|
| All time through 2026-05-09 | `82` | `3,962` | `US$18.60` | `US$0.23` | `0.00` | `0.00` |
| Custom 2026-05-06 through 2026-05-09, Google Ads Pacific time | `1` | `58` | `US$0.02` | `US$0.02` | `0.00` | `0.00` |

Product-group custom-range readback:

| Product group | Max CPC/status | Impressions | Clicks | Cost |
|---|---:|---:|---:|---:|
| `us_test_ready / daddy_me` | `US$0.04` | `14` | `0` | `US$0.00` |
| `us_test_ready / family_matching` | `US$0.04` | `7` | `0` | `US$0.00` |
| `us_test_ready / mommy_me` | `US$0.04` | `19` | `1` | `US$0.02` |
| `us_test_ready / pajamas` | `US$0.04` | `0` | `0` | `US$0.00` |
| `us_test_ready / swimsuits` | `US$0.04` | `18` | `0` | `US$0.00` |
| Everything else in All products | `Excluded` | `0` | `0` | `US$0.00` |

## What The Metrics Imply

- The `$0.04` included product-group bid posture appears to have throttled spend sharply after 2026-05-06.
- Current post-May-6 spend is far below one target-CPA learning window, so the custom-range data is not large enough to judge conversion rate, product-market fit, or profitability.
- The all-time zero-conversion result remains a warning, but it mixes older higher-CPC learning with the newer low-bid posture. Do not blend it into a scale case.
- Product scope stayed tight in readback: the included child groups were still at `US$0.04`, and `Everything else in All products` remained excluded.

## What The Metrics Do Not Justify

- They do not justify raising Standard Shopping bids, raising budget, changing status, changing product groups, changing product scope, changing feed labels, changing conversion goals, or enabling any other campaign.
- They do not justify scaling from CTR, low CPC, impressions, product eligibility, add-to-cart signals, or checkout starts.
- They do not prove that Standard Shopping should be paused immediately, because post-May-6 cost is only `US$0.02`.
- They do not prove that Standard Shopping is profitable, because there are still `0.00` purchases and `0.00` conversion value.

## Core Economics

Planning formula: `max CPA = AOV / target ROAS`.

At current planning AOV `US$70.00` and target ROAS `650%`:

| Item | Value |
|---|---:|
| AOV | `US$70.00` |
| Target ROAS | `650%` |
| Max CPA | `US$10.77` |
| Planning non-marketing cost model | `50%` of revenue |
| Estimated non-marketing cost | `US$35.00` |
| Contribution after target CPA, before returns/chargebacks/reships/duties/support drag | `US$24.23` |

Use `US$9.49-US$9.73` as the stricter decision band for weaker evidence: international, mixed-language, stale catalog, duties/returns uncertainty, or tracking uncertainty.

## CPC / CVR Break-Even

| CPC | Required CVR at `US$70` AOV / `650%` ROAS | Clicks per target CPA | Operating read |
|---:|---:|---:|---|
| `US$0.04` | `0.37%` | `269` | Current low-bid Shopping math can work, but only if query and product quality are clean. |
| `US$0.08` | `0.74%` | `135` | Good discovery ceiling for lower-CPC countries after readiness gates. |
| `US$0.10` | `0.93%` | `108` | Strong cold-test cap for high-intent exact/phrase traffic. |
| `US$0.12` | `1.11%` | `90` | Good cap for watchlist and broader EU tests. |
| `US$0.15` | `1.39%` | `72` | Current Search packet cap; needs real buyer intent. |
| `US$0.20` | `1.86%` | `54` | Upper edge; use only after CVR proof. |
| `US$0.25` | `2.32%` | `43` | Expensive for this model; not for unproven cold traffic. |

## Standard Shopping Decision Gates

All Standard Shopping actions remain approval-gated. This lane recommends only how to interpret future readbacks.

| Gate | Condition | Operator decision |
|---|---|---|
| Continue monitoring | Post-May-6 spend remains below about `US$5`, query/product-group quality is not obviously poor, and no Merchant/source regression appears. | Keep read-only monitoring. No scale or edit. |
| Narrowing decision | A product group or query cluster spends about `US$5` with weak intent, irrelevant terms, or no qualified product engagement. | Parent should request exact owner approval for the smallest safe narrowing action. |
| Target-CPA decision | Post-May-6 spend reaches `US$9.49-US$10.77` with `0` purchases. | Force owner decision: hold briefly with evidence, reduce/narrow, or pause. |
| Hard rollback decision | Post-May-6 spend reaches `US$16-US$20` with `0` purchases and no strong checkout/purchase-value evidence. | Parent should recommend rollback or pause, still requiring exact owner approval before any status/bid/budget/product-group change. |
| Scale consideration | At least `3` primary-purchase conversions from the paid cohort, ROAS at or above `650%`, clean query terms, no catalog/source regression, and no return/chargeback warning. | Only then consider a small owner-approved scale step, normally `10%-20%`. |

## Paused Non-US Search TEST BUILD Controls

The current safer held CSV is a paused infrastructure candidate only:

- `1496` rows.
- `17` non-US Search campaigns.
- All actions are `Add`.
- Campaigns, ad groups, keywords, and ads are paused.
- Max CPC is `US$0.15`.
- Final URL rows are country-qualified, `40` per country.
- No US campaign `23827590655`, PMax, Standard Shopping, Merchant, product group, product scope, feed label, conversion-goal, enablement, bad beach handle, product `7227378892897`, or `Vacation Family` hits were found.

How ROAS controls govern this after exact TEST BUILD approval:

- Approval to preview/import paused infrastructure is not spend approval.
- Keep every imported entity paused and segmented by country so losers cannot hide inside blended averages.
- Before any future activation, refresh final URL country, checkout/currency, purchase tracking, Merchant/Pinterest catalog health if relevant, and campaign settings.
- First activation should be one existing or newly approved smallest unit, not the full international bundle.
- Use the same `US$10.77` max CPA and stricter `US$9.49-US$9.73` international decision band.
- At `US$16` spend with `0` purchases in a country/ad group, hard pause the smallest unit after owner approval.
- Do not scale a non-US Search unit before at least `3` clean primary-purchase conversions, correct currency value, and ROAS at or above `650%`.

## Weekly Reporting Schema

Use `weekly_reporting_schema.csv` as the working schema. Minimum reporting must preserve:

- Platform, country, currency, language, campaign, ad group/product group/product set, and status.
- Spend, impressions, clicks, CTR, average CPC.
- Primary purchases, conversion value, CPA, ROAS, AOV, purchase CVR.
- Search term or product/theme cluster.
- Final URL country parameter and landing-page/readback status.
- Merchant/Pinterest/catalog/tracking health notes.
- Owner approval reference, action taken, action reason, next review date, and residual risk.

Use primary purchase value for ROAS decisions. Do not use historical all-conversion value from before micro-conversion cleanup as the primary ROAS source.

## Guardrails Preserved

- No live spend action.
- No campaign import, preview, create, enable, pause, or edit.
- No campaign budget, bid, status, product-scope, product-group, feed-label, or conversion-goal change.
- No PMax, Remarketing, Standard Shopping, Merchant, Shopify, Pinterest, or theme write.
- No Shopify product-data edit and no Merchant upload.
- No claim of physical inventory, local stock, warehouse inventory, or store pickup.

## Files In This Lane

- `ROAS_REPORTING_DECISION_CONTROL_PACK.md`
- `cpc_cvr_break_even_table.csv`
- `weekly_reporting_schema.csv`
- `summary.json`

## Residual Risks

- This pack is local control guidance only, not a live platform readback and not spend authorization.
- Standard Shopping search-term readback was visible-table capture, not a full downloaded export.
- Post-May-6 spend is too small to decide profitability.
- Future non-US Search spend still requires exact owner approval and just-in-time readbacks after any approved paused TEST BUILD.
