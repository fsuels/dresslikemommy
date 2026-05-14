# Keyword Scoring Rubric

Last updated: 2026-05-14

Purpose: score local keyword candidates consistently before any live Search, Shopping, Pinterest, or creative action. This is a local decision tool, not upload approval.

## Hard Disqualifiers

A keyword cannot be promoted live if any are true:

- It routes to a landing page that is not active, public, purchasable, country/currency-correct, or supplier-clean.
- It is a close-head variant with first-page estimates above the hard `$0.15` CPC ceiling.
- It implies DIY, free, sewing pattern, used, rental, marketplace-only, local pickup, same-day local inventory, adult, doll/game, supplier/source, or inspiration-only traffic.
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
| Economic fit | 10 | Can the term plausibly work at `$0.15` CPC and about `650% ROAS`, using the planning target CPA of about `$10.77` at `$70` AOV? |
| Volume/serveability | 10 | Is it likely to get impressions, or is it so narrow it may be low-search-volume dead weight? |
| Waste risk | 5 | Does it avoid DIY, free, ideas-only, marketplace, same-day, local-stock, supplier, and wrong-intent traffic? |

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
- first-page estimate is `<= $0.15`, or max CPC `$0.15` has no below-first-page warning
- no broad/generic expansion is used as the first repair
- daily budget and expected clicks fit the learning plan
- after-state readback plan is written
- Marketing Safety Reviewer outcome is `PASS` or `PASS_WITH_GATES`

## Stop-Loss Logic

Use the rough planning target CPA of `$10.77`.

- About `$5.38` spend with no add-to-cart, checkout, qualified search term, or other useful signal: hold, narrow, or prepare pause.
- About `$10.77` spend with no purchase: pause, narrow, or reroute if authority and evidence allow it.
- Obvious bad search term: exact negative if authorized; otherwise exact approval packet.

## Session Rule

Every live Search session must end with a serving repair, negative action, keyword expansion, hold/kill/scale decision, or exact blocker/unblock action. A monitor-only session is not progress unless there was genuinely no data, no blocker, and the next decision is recorded in `daily_scorecard.md`.
