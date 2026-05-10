# Market Activation Priority Scorecard

Generated: 2026-05-09

Worker: Worker C / market activation priority lane

Decision: `LOCAL_APPROVAL_GATED_SCORECARD_ONLY__LIVE_SPEND_READY_MARKETS_0`

## Scope

This lane ranks the 17 non-US markets for the smallest future approved paid-growth tests using existing evidence only. No external systems were opened or changed.

No Google Ads preview/import/upload, campaign creation, campaign enablement, budget, bid, status, product-scope, feed-label, product-group, conversion-goal, Merchant, Shopify, Pinterest, theme, checkout payment, or order action occurred.

## Evidence Used

- All 17 non-US markets have paused-infrastructure checkout/rate evidence by 2026-05-09.
- The safer held Google Search CSV excludes all `Vacation Family` rows tied to the stale beach metadata URL.
- Held CSV validation: `1496` rows, `17` paused non-US Search campaigns, `170` paused ad groups, `510` paused positive keywords, `629` negatives, `170` paused RSAs, `680` country-qualified final URL rows, max CPC `US$0.15`, and `0` forbidden-surface hits.
- Live-spend-ready non-US markets remain `0`.
- Standard Shopping post-May-6 readback is tiny: `1` click, `58` impressions, `US$0.02` cost, `0.00` conversions/value.
- Economics guardrail: `US$70` AOV at `650%` ROAS gives max CPA about `US$10.77`; stricter international band is about `US$9.49-US$9.73`; `US$16` with zero purchases remains a hard-pause decision context.
- Shared gates remain active: exact owner approval for paused non-US Google Search `TEST BUILD`, separate approval before any spend, Merchant US/es age_group repair, Pinterest Event Quality / paused drafts, and Shopify beach metadata repair if Vacation Family is restored.

## Scoring Model

The score is a priority score for an approval-gated test sequence, not a live-spend authorization.

| Component | Points | Read |
|---|---:|---|
| Checkout and currency evidence | 30 | No-payment checkout/rates/currency evidence exists for the market. |
| Fit with current English-first CSV | 20 | Stronger where English is natural or localized URL evidence is already strong. |
| Held Search CSV cleanliness | 15 | All markets use the clean held CSV with Vacation Family removed. |
| Smallest-unit practicality | 15 | Higher where a one-country, one-ad-group exact test is easiest to interpret. |
| Shared measurement/catalog risk | 10 | Discounted by unresolved shared gates and zero live-spend readiness. |
| Economics priority | 10 | Higher for first-sequence markets with better odds of useful signal under tight CPC caps. |

## Executive Result

Live-spend-ready markets: `0`.

Paused-infrastructure-ready, approval-gated markets: `17`.

Fastest controlled path is still:

1. Get the exact owner approval for the paused non-US Google Search `TEST BUILD`.
2. Preview only with the held `1496`-row CSV.
3. Read back all entities paused, no US campaign `23827590655`, no PMax, no Standard Shopping, no product/feed/conversion surfaces, no enabled entities, CPC at or below `US$0.20`, country-qualified final URLs, and presence-only location targeting.
4. Treat any later spend as a separate approval. The smallest spend unit should be one country, one exact ad group, not the full 17-country bundle.

## Smallest First Approved Test Units

These are candidate units only after the paused test build exists cleanly and after a separate action-time spend approval.

| Sequence | Candidate unit | Why it is smallest and cleanest | Required readback before spend |
|---:|---|---|---|
| 1 | `GB` / `Mommy & Me Dresses - Exact` only | English market, GBP checkout evidence, strongest fit with current English ad copy, and Standard Shopping historical query evidence includes mommy-and-me intent. | Campaign/ad group/keywords/ad paused before activation; UK only; presence-only; final URLs include `country=GB`; checkout still GBP; purchase tracking and value readback ready. |
| 2 | `CA` / `Mommy & Me Dresses - Exact` only | English market, CAD checkout evidence, clean one-country read. | Same as GB with `country=CA`, Canada only, CAD checkout, and no US targeting. |
| 3 | `AU` / `Mommy & Me Dresses - Exact` only | English market, AUD checkout evidence, prior 429 blocker solved through isolated retry. | Same as GB with `country=AU`, Australia only, AUD checkout, and no verification wall. |
| 4 | `ES` / `Mommy & Me Dresses - Exact` only | Localized ES route and EUR evidence make it the strongest non-English-market candidate, but the current CSV is English-first. | Owner must accept English-first ad copy or approve native copy; final URL must keep localized path plus `country=ES`; checkout/currency/policy readback must still pass. |
| 5 | `IT` / `Mommy & Me Dresses - Exact` only | Localized IT route and EUR evidence; similar caveat to ES. | Owner must accept English-first ad copy or approve native copy; final URL must keep localized path plus `country=IT`; checkout/currency/policy readback must still pass. |
| 6 | `PT` or `RO` / `Mommy & Me Dresses - Exact` only | Both have localized checkout/currency evidence; PT has EUR and pt-BR route behavior, RO has RON evidence. | Owner decision on which market to test first; native-copy or English-first risk must be explicit; country/currency readback required. |

Do not start with Pinterest spend. Pinterest remains a paused-draft or Event Quality repair lane while Event Quality is `Fair`. Do not restore Vacation Family until the Shopify metadata issue is approved, fixed, and publicly read back.

## Ranked Market Scorecard

| Rank | ISO | Market | Currency evidence | Current language posture | Score | Tier | Read |
|---:|---|---|---|---|---:|---|---|
| 1 | GB | United Kingdom | GBP / `en-GB` checkout evidence | English-first fit | 91 | First approved test queue | Best first single-country exact test candidate. |
| 2 | CA | Canada | CAD / `en-CA` checkout evidence | English-first fit | 90 | First approved test queue | Strong second single-country exact test candidate. |
| 3 | AU | Australia | AUD / `en-AU` checkout evidence | English-first fit | 89 | First approved test queue | Strong third candidate; prior 429 blocker was solved. |
| 4 | ES | Spain | EUR / localized ES evidence | Localized URL, English ads | 83 | Localized-url queue | Good non-English candidate if English-first copy risk is accepted or native copy is approved. |
| 5 | IT | Italy | EUR / localized IT evidence | Localized URL, English ads | 82 | Localized-url queue | Similar to ES; needs copy-language decision before spend. |
| 6 | RO | Romania | RON / localized RO evidence | Localized URL, English ads | 80 | Localized-url queue | Useful currency-diverse test, but copy-language risk remains. |
| 7 | PT | Portugal | EUR / pt-BR route evidence | Localized URL, English ads | 79 | Localized-url queue | Stronger after PT checkout passed; copy-language risk remains. |
| 8 | CH | Switzerland | CHF / `en-CH` checkout evidence | English-first shell | 72 | Watchlist queue | Checkout evidence is clean, but language and market complexity are higher. |
| 9 | DK | Denmark | DKK / `en-DK` checkout evidence | English-first shell | 71 | Watchlist queue | Clean checkout evidence; native-language or English-first decision needed. |
| 10 | DE | Germany | EUR / `en-DE` checkout evidence | English-first shell | 70 | Watchlist queue | Larger market, but English-first ad/checkout posture makes it less clean than ES/IT for immediate spend. |
| 11 | NL | Netherlands | EUR / `en-NL` checkout evidence | English-first shell | 69 | Watchlist queue | NL 429 blocker was later cleared; still not a top first-spend unit. |
| 12 | SE | Sweden | SEK / `en-SE` checkout evidence | English-first shell | 68 | Watchlist queue | Checkout passed; keep behind native-copy decision. |
| 13 | FR | France | EUR / `en-FR` checkout evidence | English-first shell | 67 | Watchlist queue | Checkout passed; stronger with native French copy. |
| 14 | BE | Belgium | EUR / `en-BE` checkout evidence | English-first shell | 66 | Watchlist queue | Multilingual market; needs clearer language targeting before spend. |
| 15 | PL | Poland | PLN / `en-PL` checkout evidence | English-first shell | 64 | Later queue | Checkout passed; lower priority until copy and economics proof improve. |
| 16 | CZ | Czechia | CZK / `en-CZ` checkout evidence | English-first shell | 63 | Later queue | Checkout passed; lower priority until copy and economics proof improve. |
| 17 | GR | Greece | EUR / `en-GR` checkout evidence | English-first shell | 62 | Later queue | Checkout passed; lower priority until copy and economics proof improve. |

## Required Readback Before Any Spend

Before any future approved spend, read back and store evidence for the exact unit being activated:

- Owner approval text names the exact country, campaign, ad group, budget/spend cap, CPC cap, status action, and stop rule.
- Campaign, ad group, keywords, and ad exist and are paused immediately before activation.
- Only the approved country is targeted; United States is absent.
- Location targeting is presence-only: people in or regularly in the included location.
- Search Network only; no Display expansion, PMax, Shopping, Merchant, product group, product scope, feed label, or conversion-goal changes.
- CPC is at or below the approved cap and never above `US$0.20` for this packet; local CSV max is `US$0.15`.
- Final URLs keep the expected `country=<ISO>` parameter and do not contain the held beach/Vacation Family product.
- Product landing, cart, shipping rates, and checkout currency still match the target market.
- Purchase conversion and value reporting are ready for primary-purchase ROAS decisions.
- Reporting packet is ready to monitor spend, clicks, CPC, conversions, value, CPA, ROAS, final URL, search terms, and country/currency.
- Stop rule is pre-accepted: at roughly `US$9.49-US$10.77` spend with zero purchases, force an owner decision; at `US$16` with zero purchases, recommend hard pause of the smallest unit, still requiring exact approval for the edit.

## Residual Gates

- Non-US Google Search TEST BUILD is still owner-approval-gated. No preview/import/build has occurred in this lane.
- Spend activation is a separate approval from paused infrastructure creation.
- Merchant US/es age_group source `10627981690` remains a separate exact-approval repair gate.
- Pinterest Event Quality remains `Fair`; paused Pinterest drafts or Event Quality repair require separate exact approval.
- Beach/Vacation Family metadata remains excluded from the held Search CSV until approved Shopify metadata repair and public readback.
- Current Google Search CSV is English-first. Native-language launch quality requires a separate copy decision or native copy packet before spend in non-English markets.

## Files In This Lane

- `MARKET_ACTIVATION_PRIORITY_SCORECARD.md`
- `market_activation_priority_scorecard.csv`
- `market_activation_priority_scorecard.json`
