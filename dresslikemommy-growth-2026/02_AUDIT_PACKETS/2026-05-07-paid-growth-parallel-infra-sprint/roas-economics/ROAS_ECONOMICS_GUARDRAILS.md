# ROAS Economics Guardrails

Date: 2026-05-07
Lane: ROAS/economics guardrail subagent
Mode: local-only model and rules. No external systems opened or changed.

## Inputs Used

- North Star target: about `650% ROAS`.
- Current sprint AOV assumption: about `$70`.
- Gross margin assumption: about `50%`.
- Owner CPC preference: near or below `$0.20`.
- Existing master economics rule: all-in non-marketing cost is `50%` of selling price, and older benchmark AOV was `$63.25` with a `15%` CAC cap / `6.67x` ROAS.

## Core Math

| Metric | Value | Formula |
| --- | ---: | --- |
| AOV planning assumption | `$70.00` | Sprint/North Star working assumption |
| Target ROAS | `6.50x` / `650%` | Revenue / ad spend |
| Target max CPA/CAC | `$10.77` | `$70 / 6.5` |
| Conservative old-rule CPA at `$70` AOV | `$10.50` | `$70 x 15%` |
| Gross profit before ad spend | `$35.00` | `$70 x 50%` |
| Contribution after target CPA, before returns/chargebacks | `$24.23` | `$35 - $10.77` |
| Marketing spend as percent of revenue at 650% ROAS | `15.38%` | `$10.77 / $70` |
| Break-even CPA at 50% margin | `$35.00` | `$70 x 50%` |

Operating interpretation:

- Use `$10.77` CPA as the planning ceiling for `650%` ROAS.
- Use `$10.50` as the conservative kill/approval threshold when returns, chargebacks, duties friction, or weak tracking are present.
- A `$0.20` click only fits the target if purchase conversion rate is about `1.86%` or better.
- A `$0.15` click needs about `1.39%` CVR.
- A `$0.10` click needs about `0.93%` CVR.
- A `$0.04` Shopping click needs only about `0.37%` CVR, which explains why very low Shopping bids can be economically attractive if product/query quality is clean.

Full CPC/CVR math lives in `cpc_cvr_cpa_model.csv`.

## Launch Budgets If Approved

These are local guardrails for future paused-build activation decisions, not approval to spend.

| Lane | Starting Budget | CPC Cap | Notes |
| --- | ---: | ---: | --- |
| US nonbrand Search rebuild | `$2/day` | `$0.15` | Existing paused rebuild already uses this posture. Keep exact/phrase only and strict negatives. |
| Priority English markets: UK, Canada, Australia | `$2/day` each | `$0.15-$0.20` | Use `$0.20` only if landing/shipping/readback quality is clean and early CVR is strong. |
| Priority QA-sensitive markets: Switzerland, Denmark | `$1-$2/day` each | `$0.12-$0.18` | Prior/order or value signal justifies testing, but duties/language friction can suppress CVR. |
| Broader EU: Germany, Netherlands, Sweden, France, Belgium, Spain, Italy | `$1/day` first | `$0.08-$0.15` | Require localization/shipping QA before any spend; do not launch all at once if portfolio budget is tight. |
| Lower-CPC discovery: Poland, Czechia, Romania, Greece, Portugal | `$1/day` each | `$0.05-$0.12` | Useful only if traffic stays high-intent and pages can convert. Cheap CPC is not a quality substitute. |
| Pinterest US retargeting/catalog test | `$1/day` first | Platform bid guardrail must map back to CPA <= `$10.77` | Only after tag/catalog/event gates pass and with explicit approval. |

Recommended portfolio cap for new tests:

- First wave: no more than `$10-$15/day` incremental spend across new Search tests until first clean purchase-value readbacks.
- Full international discovery portfolio: no more than `$20/day` incremental spend until at least one country proves purchase CPA near or below `$10.77`.
- Keep live Standard Shopping, Brand Search, PMax, Remarketing, product scope, feed labels, and conversion goals outside this economics lane unless separately approved.

## Kill Rules

Pre-launch hard stops:

- Do not spend if purchase conversion value, currency, or transaction IDs are not trusted.
- Do not spend if the landing page has mixed-language trust problems, unclear shipping/returns/duties, broken product grids, or unclear "choose one size per person" purchase flow.
- Do not spend if Merchant/Pinterest catalog eligibility is not clean enough for the products used.
- Do not spend on campaigns with broad match, weak negatives, unsupported claims, or PMax automation until the parent gate says those are ready.

Early traffic controls:

- Pause a keyword/ad group if average CPC exceeds the approved cap after a meaningful click sample and cannot be corrected with tighter match types or negatives.
- Add negatives or pause immediately for irrelevant search terms, supplier/wholesale intent, free/cheap-only intent, costume/Halloween mismatch, adult/NSFW terms, unrelated brand/IP terms, or generic fashion traffic without family-matching intent.
- If spend reaches `$5` in a new ad group with no qualified product views, cart intent, or clean search terms, pause and rewrite/narrow.

Purchase economics controls:

- At spend >= `$10.77` with `0` purchases, pause or narrow unless there is strong checkout evidence and the parent explicitly chooses to continue learning.
- At spend >= `$16` with `0` purchases, hard pause the ad group/country.
- At spend >= `2` purchases, hold or reduce if CPA is above `$10.77` or ROAS is below `650%`.
- If ROAS is `500%-650%`, hold budget and improve terms/landing/CPC before scaling.
- If ROAS is below `500%` after at least two purchases or one target-CPA learning window, pause or cut budget.
- If returns, chargebacks, cancellation, or shipping/duties complaints surface for a country, move that country to the conservative `$10.50` CPA threshold or pause until fixed.

## Scale Rules

- Do not scale on clicks, CTR, add-to-cart, checkout starts, or micro-conversions alone.
- Scale only from purchase value, clean search terms, acceptable CPC, and no obvious return/chargeback warnings.
- Require at least `3` purchases in a country/campaign before meaningful scaling; for very low-volume countries, use a parent-approved exception only when search terms and checkout quality are unusually clean.
- If CPA is <= `$8.75` or ROAS >= `800%`, increase budget by `20%-30%` every `3-7` days.
- If CPA is `$8.75-$10.77` or ROAS is `650%-800%`, increase budget by `10%-20%` every `3-7` days.
- If CPA is `$10.77-$14.00`, do not scale; tighten CPC, negatives, query intent, product/category, or landing page.
- If CPA is > `$14.00`, reduce or pause unless there is a documented high-AOV cohort that makes the math work.

## Country Prioritization Implications

- Priority/proven markets can start first, but only with segmented campaigns so losers do not hide inside blended performance.
- UK, Canada, and Australia can use English-first tests if shipping/returns and checkout clarity pass.
- Switzerland and Denmark are attractive but QA-sensitive; use lower starting CPC caps until language, duties, and checkout friction are proven.
- Germany, Netherlands, Sweden, France, Belgium, Spain, and Italy need localization QA before spend. Their economics should be judged by country, not blended EU average.
- Poland, Czechia, Romania, Greece, and Portugal are good low-CPC discovery candidates. Their advantage is that `$0.05-$0.12` clicks can hit target ROAS at much lower CVR, but only if traffic is still high-intent.
- Arabic/Hebrew/Japanese/Korean or mixed-language markets should stay on hold until localization, checkout, currency, shipping, and returns clarity are clean enough for shoppers.

See `country_budget_implications.csv` for the country-level budget/CPC matrix.

## Residual Risks

- The `$70` AOV is a working sprint assumption; older master docs used `$63.25`. If current AOV differs materially, recompute CPA with `target_cpa = AOV / 6.5`.
- Gross margin is assumed at `50%`; return, chargeback, duty, reshipment, and customer-service drag are not fully modeled.
- International conversion rates may be lower than US rates because of shipping time, duties, currency, translation quality, or checkout trust friction.
- Google Ads and Pinterest attribution can lag; do not overreact to same-day ROAS, but do not let low-quality spend run past the hard caps.
- Small `$1-$2/day` tests will learn slowly. That is intentional for cash control, but the parent should aggregate by wave and make disciplined go/kill decisions.

## Commands Run

- `sed -n '1,260p' ops/GROWTH_NORTH_STAR.md`
- `sed -n '1,260p' ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `sed -n '1,260p' ops/AGENT_COORDINATION.md`
- `tail -n 220 ops/AGENT_WORKLOG.md`
- `rg -n "650% ROAS|ROAS|gross margin|AOV|kill rule|CPA|CPC" dresslikemommy-growth-2026 ops -g '*.md' -g '*.csv' -g '*.json'`
- `node - <<'NODE' ...` for CPA/CPC/CVR calculation verification
- `ruby -rcsv -e 'ARGV.each { ... }' cpc_cvr_cpa_model.csv country_budget_implications.csv`
- `git diff --check -- dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/roas-economics`

## Guardrails Preserved

- No external systems touched.
- No campaign creation, enablement, pausing, budget edits, bid edits, feed uploads, product-data edits, product-scope changes, product-group changes, feed-label changes, pixel edits, or conversion-goal changes.
- Edits were limited to `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/roas-economics/`.
