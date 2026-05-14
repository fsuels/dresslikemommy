# Expert Growth Playbook 2026

Last updated: 2026-05-14

Purpose: give Dress Like Mommy paid-growth agents one source-backed operating standard for expert-level Google Ads, Pinterest, CRO, measurement, and agent coordination. This is a local command-layer standard, not approval to make live writes.

## North Star

Get customers to buy. Grow as many profitable Dress Like Mommy paid-growth sales as possible across Google Ads and Pinterest while targeting about `650% ROAS`.

Starting 2026-05-14, treat today as Day 1 of the growth operating system. Each day that passes without more sales, usable learning, or a sales-moving improvement is a failure signal that requires action, not a reason to wait.

Current planning math:

- Repo-known AOV: about `$70`.
- Target ROAS: about `650%`.
- Implied target CPA: about `$10.77`.
- Diagnostics such as impressions, clicks, CTR, CPC, Quality Score, ad strength, search terms, and product-feed warnings matter only because they explain how to reach profitable purchases.

## Day 1 Growth Cadence

The operating question every morning is: how many paid-growth sales did we get by tomorrow, at what CPA and ROAS, and what did we change to get closer to `650% ROAS`?

- Proactive action is mandatory. If a mistake, broken state, underperforming path, or clear improvement is visible, fix it immediately when local/read-only or currently approved. If a live external write is needed but not approved, write the exact smallest approval packet and keep another safe lane moving.
- Monitoring is not the deliverable. Every monitor/readback loop must end in a concrete result: `fix now`, `execute approved bounded action`, `prepare exact approval packet`, `reroute to another safe sales-moving lane`, or `hold with evidence because no action is currently valid`.
- By tomorrow, every active paid lane must report sales, revenue/conversion value, CPA, ROAS, and the next action. If sales are zero, the lane still owes a diagnosis and improvement path.
- Zero impressions after 24 hours is not acceptable drift. It triggers same-day serving diagnosis and a high-intent long-tail expansion or auction-entry decision, inside current approval boundaries.
- Zero clicks after qualified impressions triggers ad/creative/photo/title/price/query-fit diagnosis.
- Clicks without purchases trigger search-term, landing trust, price, shipping clarity, product/photo fit, mobile path, and measurement diagnosis.
- Purchases with weak ROAS trigger bid, keyword, negative, product, landing, and scale-control work; do not celebrate sales that cannot approach `650% ROAS`.
- AI speed means faster evidence loops, candidate generation, guardrail checks, and bounded execution. It does not mean unsafe broadening, stale evidence, or skipping approval boundaries.

## Source-Backed Principles

Use these official and high-reputation sources as the strategy floor:

| Source | Principle for Dress Like Mommy |
|---|---|
| [Google Ads Help: keyword match types](https://support.google.com/google-ads/answer/7478529?hl=en) | Start controlled with exact or phrase where intent is known; broad expansion belongs behind conversion-value, landing, and search-term quality gates. |
| [Google Ads Help: search terms report](https://support.google.com/google-ads/answer/7102466?hl=en-EN) | Actual search terms drive expansion and negatives. Do not guess from a watchlist when live search-term evidence is missing. |
| [Google Ads Help: negative keywords](https://support.google.com/google-ads/answer/2453972?hl=en) | Negatives help focus spend, but overblocking can reduce qualified reach. Add negatives carefully and from evidence. |
| [Google Ads Help: Target ROAS bidding](https://support.google.com/google-ads/answer/6268637?hl=en-EN) | Target ROAS and value bidding require conversion values and enough learning signal. Do not switch young zero-data tests into ROAS automation by hope. |
| [Google Ads Help: Quality Score](https://support.google.com/google-ads/answer/13738235?hl=en) | Use expected CTR, ad relevance, and landing page experience as diagnostics for cheaper, higher-quality traffic. |
| [Google Ads Help: ad quality](https://support.google.com/google-ads/answer/156066?hl=en) | Better ad quality can improve position and cost. Check ad quality before solving every issue with higher bids. |
| [Google Ads Help: keyword prioritization](https://support.google.com/google-ads/answer/2756257?hl=en) | Manage overlapping keywords, ad groups, and formats intentionally so the account does not confuse routing or self-compete by structure. |
| [Pinterest Business: lower-funnel creative best practices](https://business.pinterest.com/en-ca/blog/lower-funnel-creative-best-practices/) | Use clear product imagery, direct CTA, clear copy, multiple lower-funnel formats where relevant, and a seamless clickthrough experience. |
| [OpenAI: Practical guide to building AI agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | Give agents clear instructions, tools, guardrails, evals, and escalation paths. Tool risk matters, especially financial and external writes. |
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Keep agent systems simple, transparent, composable, and evaluated. Use specialized workflows only when they improve reliability. |

## Keyword Standard

Every Search keyword must pass this rubric before it is recommended, added, expanded, paused, or used as a negative:

| Criterion | Required standard |
|---|---|
| Intent | Shopper is likely trying to buy matching family, mommy-and-me, mother-daughter, or event-appropriate dresses, not just browse inspiration. |
| Economics | CPC and expected CPA can plausibly support `$10.77` target CPA and `650% ROAS`. Cheap traffic is not good if buying intent is weak. |
| Competition | Prefer lower-waste, less-contested long-tail and product/event terms before expensive generic or retailer/marketplace terms. |
| Landing fit | Keyword promise matches the PDP or collection: product, role, photo, price, shipping, country, currency, and season. |
| Measurement | The campaign can report spend, clicks, purchases, conversion value, currency, CPA, and ROAS before scale. |
| Cannibalization | One active owner per query intent, market, language, and landing path. Avoid duplicate exact keywords or unclear overlap across ad groups/campaigns. |
| Evidence | Starter hypotheses are allowed only in tight tests; scale, negatives, broadening, and bid changes require fresh data. |

Starter keyword hypotheses are not "smart" until the daily data proves them. A keyword is proving smart only when it produces qualified impressions/search terms, acceptable CPC, relevant clicks, purchase or value signal, and a path to the `650% ROAS` target.

Use `ops/marketing/keyword_factory_015_cpc_criteria.md` as the operating criteria and `ops/marketing/us_primary_keyword_lane.md` for the US-first lane. US is the biggest market and must be the first keyword-intelligence universe, even when the immediate active Search repair is GB/CA/AU. The rule is to build a large local universe quickly, but only promote validated batches into live packets. At the current `$0.15` hard CPC cap, head terms or close-head variants with first-page estimates above `$0.15` are rejected action rows, not bid-up opportunities.

Long-tail candidate themes to investigate quickly, not blindly upload:

- Role plus product: mother daughter floral dresses, mommy daughter matching dresses, mom and baby girl dresses.
- Occasion plus buyer intent: mommy and me birthday dresses, mother daughter wedding guest dresses, matching family photoshoot dresses, family beach vacation outfits.
- Product style plus role: mommy and me tulle dress, mother daughter ruffle dress, matching family holiday dress.
- Market language/country modifiers where natural: UK, Canada, Australia, near-country spelling differences, and local event vocabulary.
- Pain-point or gift intent only when the landing page truly satisfies it: family photo outfits, birthday outfit, vacation matching dress.

Reject long-tail terms that are cheap because they are informational, DIY, sewing, used, rental, marketplace-only, local pickup, unsupported fast shipping, adult, doll/game, supplier/source, or unrelated apparel intent.

## Negative Keyword Standard

Negatives are a steering tool, not a bulk guess list.

- Watchlists are `watch_only_not_uploaded` until search-term evidence proves the waste.
- Add negatives when actual search terms show free, DIY, sewing-pattern, used, rental, adult, doll/game, supplier/source, unsupported marketplace, local pickup, same-day, or wrong-product intent.
- Do not block competitor, retailer, marketplace, or generic words just because they seem risky; prove waste or protect a specific routing rule.
- Keep negative scope narrow enough that it does not block high-intent matching dress shoppers.

## Anti-Cannibalization Standard

Avoid competing against ourselves or confusing the account:

- Assign one active query-intent owner by market/language: exact Search, phrase/broad discovery, Shopping, Pinterest, or remarketing.
- Do not run duplicate exact keywords in multiple live ad groups for the same market and landing path.
- If phrase or broad tests are later approved, isolate them from exact winners and use evidence-backed negatives or campaign structure to route traffic.
- Shopping and Search can both be useful, but their roles must be explicit: Search captures named query intent; Shopping validates product/feed/title/image demand.
- Pinterest does not own Google Search keywords. It owns product, creative, catalog, audience, and visual intent.

## Daily Optimization Rhythm

Every active or approved-ready paid lane needs an owner, a clock, and an action rule.

Daily:

- Read today and yesterday spend, impressions, clicks, CTR, CPC, conversions, conversion value, CPA, ROAS, search terms, ad/RSA status, Quality Score components when available, landing route, product/photo fit, and blocker state.
- Decide `scale`, `hold`, `pause/reduce`, `fix blocker`, `build paused`, or `needs owner approval`.
- Update `campaign_explorer.json`, `daily_scorecard.md`, `decision_log.md`, `action_queue.md`, and `operator_cockpit.md` after material decisions.

Checkpoints:

- T+24: confirm the campaign is eligible, serving or explain why not, and has no obvious landing/measurement/approval blocker.
- T+24 zero-impression rule: if an active campaign has zero impressions after one day, run serving diagnosis the same day and prepare high-intent long-tail or auction-entry action options. Do not wait until T+72 to start thinking.
- T+72: if zero impressions or zero learning persists, escalate from diagnosis to a bounded action or exact approval packet: long-tail exact/phrase expansion, CPC cap review, ad/RSA fix, landing fix, or pause/rebuild decision.
- T+7d: keep only tests with purchase/value signal, meaningful qualified learning, or a clear evidence-backed next test.

## Channel Strategy Guardrails

Google Search:

- Start with high-intent exact or phrase groups when conversion value is not yet mature.
- Manual CPC can be right for tiny exploratory tests because it limits downside and avoids optimizing for empty clicks.
- Maximize Clicks is not a goal; it is only a controlled discovery tool when capped, justified, and approved.
- Target ROAS or value bidding is the goal-state bidding family only after purchase value tracking and enough conversion learning are proven.

Google Shopping:

- Shopping does not use manual Search keywords. It depends on product titles, images, feed labels, product groups, price, availability, landing page, and conversion value.
- Use search terms, product-level metrics, and feed diagnostics to decide whether to exclude, improve product data, or scale.
- Do not change product groups, feed labels, sources, product scope, or conversion goals without current approval.

Pinterest:

- Success depends on product/photo fit, catalog health, audience/product group fit, clear creative, direct CTA, and clickthrough consistency.
- Prefer clean catalog scope and product imagery that quickly communicates matching family dresses.
- Do not create or alter catalog/source/product groups, tag/CAPI, budgets, bids, or statuses unless approval and access are clean.

Landing/CRO:

- Paid traffic must land on active, public, purchasable, country/currency-correct, supplier-clean pages.
- Page promise must match the ad and product photo.
- Trust, shipping clarity, sizing clarity, role selection, price truthfulness, mobile speed, and checkout path are part of paid performance, not separate design polish.

## Agent Personas

Agents must operate like specialists, not note takers:

- Head of Growth: senior performance marketing director. Owns priorities, approvals, green-gated action, daily accountability, and profit logic.
- Google Ads Operator: senior Search/Shopping performance marketer. Owns keyword economics, bidding, query quality, Quality Score diagnostics, Shopping structure, and no-cannibalization routing.
- Pinterest Operator: senior paid social shopping operator. Owns catalog readiness, product-group fit, creative/product-photo quality, lower-funnel testing, and access gates.
- Analytics ROAS Operator: measurement economist. Owns metric freshness, purchase/value truth, CPA/ROAS math, and what data is enough to act.
- Landing CRO Operator: shopper empathy and conversion lead. Owns paid-landing trust, product/photo promise match, country/currency/shipping clarity, and mobile buying friction.
- Marketing Safety Reviewer: approval and risk auditor. Owns boundary checks, stale-evidence checks, supplier/source leak risk, active-product scope, spend authority, and blocker classification.

## Rookie Mistakes To Block

- Letting an active campaign sit for days with zero impressions, zero clicks, or zero purchase signal without a diagnosis deadline.
- Treating obvious broad category keywords as the whole strategy when CPC is too high for the ROAS target.
- Moving too slowly when safe work exists: long-tail research, live readbacks, diagnosis packets, paused-ready builds, and green-gated bounded actions should move daily.
- Optimizing for clicks when the business goal is profitable purchases at about `650% ROAS`.
- Raising bids before checking ad quality, keyword eligibility, search volume, Quality Score components, policy/destination status, and landing fit.
- Treating a negative keyword watchlist as an upload list.
- Broadening match types or enabling AI expansion before conversion value, landing, and search-term controls are proven.
- Mixing languages, currencies, countries, seasons, or product categories without native/local or shopper-intent proof.
- Advertising inactive, draft, unavailable, stale, supplier-leaking, or not-currently-read-back products.
- Letting Search, Shopping, Pinterest, and remarketing target the same intent without a clear role and evidence-backed routing.
- Calling an audit complete when it does not create a sales-moving next action, controlled build, approval packet, blocker removal, or exact unblock step.
