# Italian Search: retain the purchase intent, contain the test

Confidence: H in the scoped report; M in the test hypothesis. September 6, 2026. **LOCAL PROPOSAL ONLY. Not approved, uploaded or executable from historical settings.** Campaign scaling remains on hold.

The question was whether cheap Italian clicks contained a useful purchase signal. The report identifies one: **“vestiti uguali mamma e figlia”** (matching mother-and-daughter clothes), 24 clicks, USD3.59 cost and one purchase key event/USD151.46 revenue. A fresh exact-query filter joins that purchase to **“abiti mamma figlia”**, ad group **196333557323**, in customer **3990976848**, campaign **23866684201**. The original group name is Mommy & Me Dresses. Its historical destination was `/it/collections/mommy-and-me?country=IT`.

The keyword join displays empty cost/click cells; those are unknown in that view. The query and ad-group views separately display the same USD3.59/24 clicks. This is a report association, not a direct Ads billing or conversion-credit readback.

| June 7–September 4 scope | Clicks | Ads cost | Recorded purchases | Reported ROAS |
|---|---:|---:|---:|---:|
| Entire Italian campaign | 855 | USD127.34 | 1 | 1.19x |
| Keyword `abiti mamma figlia` | 435 | USD64.84 | 1 | 2.34x |
| Selected query `vestiti uguali mamma e figlia` | 24 | USD3.59 | 1 | 42.19x |
| Keyword `costumi famiglia` | 237 | USD35.25 | 0 | 0.00x |
| Keyword `abiti coordinati famiglia` | 91 | USD13.50 | 0 | 0.00x |

The last two keywords account for USD48.75, or 38.28% of campaign cost. Their zero recorded purchases make them lower-priority uses of a small test budget; incomplete purchase capture prevents calling that money a verified loss. All134 returned queries were reviewed, but their USD98.76 UI total covers only77.56% of campaign cost: **USD28.58/192 clicks are not represented**. Keyword and query displayed sums also exceed their UI totals by USD0.01/USD0.02. The causes are unknown; unsampled reporting does not resolve them.

## Proposed change after the prerequisites clear

Use the existing Italian campaign and Mommy & Me Dresses ad group for one isolated intent test. Do not clone the campaign. First read current criteria, current match types, negatives, URLs, statuses, bidding, geo/language, purchase actions and account-wide exposure from the operating Ads account. Bind the proposed changes to that before-state; abort or revise if it differs from the historical inventory.

For the proposed test window, retain or add **one EXACT keyword `[vestiti uguali mamma e figlia]`** in group196333557323 only after checking whether it already exists. Temporarily hold the two historical dress seeds (`abiti mamma figlia`, `abiti mamma e figlia`) and the other three historical ad groups (Family Matching196333557283, Pajamas196333557483, Swimwear196333557523) within this campaign, if current readback confirms them. Preserve all unrelated campaigns. This isolates the hypothesis; it does not establish incremental demand or prevent close-variant traffic. No negative keyword is proposed because the observed terms do not establish plainly irrelevant intent.

Keep maximum CPC at or below USD0.15 and use the stricter of the6.5x ROAS planning floor and actual return-adjusted30% net economics. A **proposed USD10 cumulative first-stage allocation**, within the existing USD50 planning envelope, is a risk checkpoint for review—not a new budget approval or guaranteed platform spending cap. The envelope has no verified unused balance; historical USD127.34 cost belongs to its own reporting window, not an inferred future authorization window. Before any launch, specify the exact new window, account-wide exposure, enforceable spend monitoring and authorized stop action; a daily-budget entry alone does not prove a hard cumulative limit. If reliable enforcement is unavailable, do not launch. USD500+ scaling is not supported by this one selected sale.

## Required proof and stop conditions

- Restore original Ads management access. The already-approved Google support submission remains blocked on Contact email validation; no case exists. No unchanged failed submission retry or replacement account.
- Verify actual fulfilled costs/returns, attribution and purchase capture for this cohort. Derive a numerical allowable acquisition cost using the existing economics calculator and a consistent revenue/return basis before execution; USD10 is not an established allowable CPA. Shopify's recorded organic journey remains a conflict. No revenue forecast or30% profit claim follows from this report.
- Verify the current Italian destination and buyer path. Two Shopify source attempts returned upstream500; Italian collection membership, translations and publication were not returned. Keep that read blocked until changed service evidence or a materially different, permitted read path preserves the same account/scope; no unchanged retry or public-access workaround after429. Skyfade7536992976993 is one identified purchased-basket component and has an unresolved size-source conflict. Do not promote that product or substitute a collection from DA/NL evidence.
- Obtain the exact reviewed current-state action authority. After execution, read back every changed criterion/group, settings and unchanged unrelated scope. Preserve original source/status for reversal; rollback is a separate authorized, conflict-checked action, not a reason to resume unproven spend automatically.
- Stop at the authorized cumulative limit or earlier on CPC/control/measurement/landing failure. Zero impressions after24hours triggers same-day serving and auction diagnosis, without increasing bids beyond the ceiling. After the observed conversion lag, compare retained order contribution and report results; extend only through a reviewed next stage. One purchase cannot certify a winner.

The credible alternative is keeping the whole dress group unchanged. Its two observed keyword rows total USD68.88 for one recorded purchase, below the planning return floor. Isolating the observed phrase is the more bounded hypothesis, but it can fail from low volume, selected-sample luck or imperfect attribution. The phrase produced only24 clicks across90 days, so it cannot currently be treated as the main traffic engine. Add a proposed seven-day maximum test window as well as the cumulative cost checkpoint; insufficient volume means inconclusive, not permission to raise bids, extend automatically or declare a winner. The separate prepared US candidate and organic release work remain necessary. **No sales lift is yet measured.**

One owner action goes first: correct Contact email on the original Google support form so its existing submission approval can be used after consistent readback. This restores a path toward controlling reported recent ad spend. The prepared four-file Shopify organic/CRO release remains available under its existing separate owner-release process.

Evidence: [current readback](italian_search_current_readback.json), [all134 query rows](italian_search_queries_current.tsv), [seven keyword rows](italian_search_keywords_current.tsv), [historical scope](italian_search_original_scope.json), [source limitation](italian_search_landing_source.json), and [independent interpretation](italian_search_query_interpretation.md). Field semantics: [Google's report definitions](https://support.google.com/analytics/answer/14617038?hl=en).
