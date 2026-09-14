# Action-Biased Keyword Strategy

Last updated: 2026-09-11

Purpose: build the largest useful Dress Like Mommy keyword universe locally, score it aggressively, and promote only small validated batches into live paid tests. This file is local strategy only; it is not approval to upload keywords or change live campaigns.

## Operating Rule

The expert strategy is:

1. Build the keyword universe as large as possible locally.
2. Score every row by buyer intent, product fit, occasion/deadline intent, landing-page match, economics, serveability, and waste risk.
3. Promote only `GREEN` rows into exact, bounded live packets after fresh readback and reviewer pass.
4. Use phrase match only as a controlled discovery repair when exact rows are too narrow or low-search-volume.
5. Never upload the full universe live.

This is action, not bureaucracy: the local universe should grow fast, but live spend should stay concentrated on terms that can plausibly create profitable sales at about `650% ROAS` and the owner's hard `$0.15` CPC ceiling.

## Store Category Map

Use these Dress Like Mommy category/moment families as the seed map:

- Mommy & Me
- Family Matching
- Pajamas
- Matching Dresses
- Swimsuits
- Daddy & Me
- Couples
- Vacation
- Photo Days
- Birthdays
- Beach Days

Each keyword must map to one clear category, landing route, and campaign owner before it can become a live action.

## Four Keyword Layers

| Layer | Use | Live posture |
|---|---|---|
| Layer 1 - Core obvious terms | Anchor demand like `mommy and me dresses`, `mother daughter dresses`, `matching family outfits`, `matching family pajamas`, `matching family swimsuits`, and `daddy and me outfits`. | Keep small and exact. Do not bid up expensive head terms above `$0.15`; close-head variants are usually not real long tail. |
| Layer 2 - High-intent long-tail terms | Buyer moments like `family outfits for beach photos`, `matching family vacation outfits`, `mommy and me dresses for pictures`, `mother daughter wedding guest dresses`, and `family cruise outfits`. | Primary Search expansion source. Promote in small exact batches first; add tightly themed phrase variants only when serving is too narrow. |
| Layer 3 - Product/category combinations | Product-fit terms like `mommy and me maxi dresses`, `matching family tropical outfits`, `mommy and me swimsuits`, `mother daughter bathing suits`, `dad and son vacation shirts`, and `matching couple beach outfits`. | Use only when a truthful category/PDP exists and the query is routed to that exact promise. |
| Layer 4 - Research/watchlist terms | Higher-funnel terms like `family outfit ideas`, `what to wear for family photos`, and `beach family photo outfit ideas`. | Keep local for SEO/Pinterest/content/search-term monitoring. Do not launch in paid Search unless query evidence proves purchase intent. |

## Market Language

| Market | Required language adaptation |
|---|---|
| US | Primary market. Use `mom`, `mommy`, `mommy and me`, `mother daughter`, `mom daughter`, `family photos`, `family pictures`, `vacation`, `birthday`, `wedding guest`, `beach photos`, and `matching family`. |
| GB | Use `mum`, `mummy`, `holiday`, `family photos`, `family pictures`, `pyjamas`, and UK spelling where natural. |
| CA English | Use `mom`, `mommy`, `family pictures`, `vacation`, `Canada`, and Canadian buyer moments. Do not mix French-Canada into English campaigns. |
| AU | Use `mum`, `mummy`, `holiday`, `beach`, `swimwear`, `pyjamas`, and Australia wording where natural. |
| French Canada | Separate native-review lane only. Do not upload French rows from machine translation without native signoff. |

## Forced Action Rules

### 24-Hour No-Impression Rule

If an enabled Search campaign or ad group has `0` impressions after 24 hours, do not close the task as "monitoring."

Run the same-day checklist:

- campaign status
- ad group status
- keyword status, including eligible, low-search-volume, disapproved, paused, and below-first-page warnings
- ad/RSA status and policy
- location targeting and presence setting
- language targeting
- final URL availability and landing sanitizer
- bid, budget, and auction entry against the `$0.15` cap
- search volume and match type

If no technical blocker exists and the existing terms are eligible but too narrow, prepare or execute a green-gated repair using `5-20` closely related exact/phrase long-tail rows from `keyword_universe.csv`. Do not jump to broad expensive head terms.

### Low-Search-Volume Rule

Low-search-volume exact keywords stay useful as local evidence, but they cannot be the only learning engine.

If exact rows are inactive or dead weight:

- add phrase variants with the same buyer intent when green-gated
- add adjacent occasion terms, not generic head terms
- keep one theme per ad group
- review search terms the next day
- do not use broad generic terms unless there is conversion history and negative coverage

### Spend And Stop-Loss Rule

Use the reviewed common retained-revenue convention: R is retained merchandise revenue after discounts/refunds plus retained shipping income, excluding tax; V is disjoint actual variable costs net of evidenced recoveries; H is allocated overhead and other costs excluded from V; CM = R − V. For positive R, permitted advertising A must satisfy `A ≤ min(R/6.5, CM − H − 0.30R, approved cash/loss allowance)`. This requires 6.5x business ROAS and 30% all-in profit on the same R basis. Unknown required inputs or a nonpositive result mean no economically qualified spending amount. Do not substitute platform purchase value without reconciling its revenue basis. Preserve the USD 0.15 CPC ceiling. The former USD 70 AOV/USD 10.77 CPA example is historical modeling, not a current target.

Compare spend only after observed conversion lag, while reserving unresolved refund/fulfillment exposure. The approved cumulative loss limit protects downside independently of ordinary sample uncertainty. Do not pause from a fixed modeled CPA or optimize purchase campaigns toward cart events. Prepare narrow negatives only from relevant query evidence and current authority.

### Search Session Output Rule

Every live Search session must produce one of:

- serving repair
- negative keyword action
- keyword expansion from qualified evidence
- hold, kill, or scale decision
- exact blocker with the next unblock action

No session may claim "monitoring progress" unless `daily_scorecard.md` has been updated with spend, impressions, clicks, purchases, revenue, ROAS, and the next decision.

## Current Promotion State

The May 14 descriptions of US Standard Shopping and GB/CA/AU Search as live are historical observations, not current account facts. Retrieve current campaign/account identity, country/language scope, effective CPC control, purchase acceptance, actual costs and authority from the canonical command layer before promotion. Do not clone a historical campaign or treat historical first-page estimates as current.

No live external write is authorized by this strategy file alone.

Evidence rule: current command-layer readbacks govern account status and authority. A local score is a research priority, not live readiness. Economic-fit and serveability points require dated evidence for the exact market, keyword and offer; assign zero evidence credit when unknown. Zero credit does not mean zero demand. Recompute the total/threshold without changing keyword identity or promotion status.

Negative intent is not a blanket one-word exclusion: adult sizes are valid apparel; “free shipping” can express buying intent; “pattern” can describe a garment; and “costume/costumi” changes meaning by language. Use original-language, query-specific evidence and check existing negatives before proposing a narrow exclusion.
