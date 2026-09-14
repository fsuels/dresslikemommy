# Keyword Scoring Rubric

Last updated: 2026-09-11

Purpose: score local keyword candidates consistently before any live Search, Shopping, Pinterest, or creative action. This is a local decision tool, not upload approval.

## Hard Disqualifiers

A keyword cannot be promoted live if any are true:

- It routes to a landing page that is not active, public, purchasable, country/currency-correct, or supplier-clean.
- Current effective CPC controls or economically evaluated exposure cannot satisfy the USD 0.15 ceiling; historical first-page estimates alone do not establish present serving or CPC.
- It implies DIY, free-product-only intent, sewing-pattern requests, used, rental, marketplace-only, local pickup, same-day local inventory, sexually explicit content, doll/game, supplier/source, or inspiration-only traffic.
- It belongs to another language or market lane, such as French-Canada inside English-Canada.
- It duplicates a live exact keyword without a clear anti-cannibalization owner.
- It requires native language ad/keyword use without native signoff.

## Scorecard

Score every row from `0-100`.

| Criterion | Weight | What to check |
|---|---:|---|
| Buyer intent | 25 | Does the phrase imply someone is shopping now, not browsing ideas? Strong signals include product type, role, event, trip, photo, birthday, wedding guest, swim, pajamas, or matching need. |
| Product match | 20 | Does Dress Like Mommy actually sell the item/category/role implied by the query? |
| Occasion/deadline | 15 | Does the query include a buyer moment such as photoshoot, vacation, birthday, wedding, cruise, beach day, holiday, or family pictures? |
| Landing-page match | 15 | Is there a clean page, collection, or PDP that truthfully satisfies the query with country/currency fit and no supplier/source leak? |
| Economic fit | 10 | Dated evidence supports USD 0.15 CPC/control and the stricter of 6.5x return-adjusted ROAS and 30% all-in profit using actual costs; unknown earns zero evidence credit. |
| Volume/serveability | 10 | Dated exact-market demand/auction evidence supports serving; unknown earns zero evidence credit, not a zero-demand claim. |
| Waste risk | 5 | Does it avoid DIY, free-product-only intent, ideas-only, marketplace, same-day, local-stock, supplier, and wrong-intent traffic? |

## Thresholds

| Score | Label | Action |
|---:|---|---|
| `85-100` | `GREEN` | Candidate for exact/phrase validation and small bounded live packet after fresh readback, reviewer pass, landing proof, and CPC proof. |
| `70-84` | `YELLOW` | Keep local. Use for controlled phrase discovery or adjacent repair only if stronger rows cannot serve and gates pass. |
| `<70` | `RED` | Do not launch. Keep for SEO/Pinterest/content/watchlist or reject. |

## Promotion Checklist

Before a `GREEN` keyword can move live:

- exact market, language, campaign, ad group, match type, final URL, and negative watchlist are named in `action_queue.md`
- fresh Ads readback is saved
- landing sanitizer readback passes
- current effective CPC controls meet the USD 0.15 ceiling and dated market-specific auction evidence supports a bounded test; an absent warning or historical bid range is not proof
- no broad/generic expansion is used as the first repair
- daily budget and expected clicks fit the learning plan
- after-state readback plan is written
- Marketing Safety Reviewer outcome is `PASS` or `PASS_WITH_GATES`

## Stop-Loss Logic

Calculate the exact basket allowable CPA from current actual costs, retained revenue/shipping and returns. Do not use the historical USD 70/USD 10.77 example as a current pause threshold. Evaluate ordinary uncertainty after conversion lag; enforce the separately approved cumulative loss ceiling with unresolved exposure reserved. A negative or pause still requires exact current scope, evidence and authority.

## Session Rule

Every live Search session must end with a serving repair, negative action, keyword expansion, hold/kill/scale decision, or exact blocker/unblock action. A monitor-only session is not progress unless there was genuinely no data, no blocker, and the next decision is recorded in `daily_scorecard.md`.

Evidence rule: current command-layer readbacks govern account status and authority. A local score is a research priority, not live readiness. Economic-fit and serveability points require dated evidence for the exact market, keyword and offer; assign zero evidence credit when unknown. Zero credit does not mean zero demand. Recompute the total/threshold without changing keyword identity or promotion status.

Negative intent is not a blanket one-word exclusion: adult sizes are valid apparel; “free shipping” can express buying intent; “pattern” can describe a garment; and “costume/costumi” changes meaning by language. Use original-language, query-specific evidence and check existing negatives before proposing a narrow exclusion.

Economics definitions follow `keyword_strategy.md`: R is retained merchandise plus retained shipping, excluding tax; V is actual variable costs; H is allocated overhead/other costs excluded from V; CM = R − V. Require `A ≤ min(R/6.5, CM − H − 0.30R, approved cash/loss allowance)`. Unknown required inputs remain unqualified; platform value must be reconciled to this basis.
