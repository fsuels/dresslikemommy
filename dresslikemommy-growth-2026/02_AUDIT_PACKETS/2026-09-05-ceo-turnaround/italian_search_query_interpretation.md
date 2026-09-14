# Italian Search query interpretation

Confidence: H for arithmetic; M for retention hypotheses. Reviewed 2026-09-06. **Campaign scaling remains HOLD.** Local review of [keywords](italian_search_keywords_current.tsv), [queries](italian_search_queries_current.tsv), [campaign cost](italian_ga4_campaign_cost_readback.json) and [historical scope](italian_search_original_scope.json). Campaign 23866684201/June 7–September 4 scope, UI totals and unsampled daily-data status are operator-supplied; the TSVs contain no filter metadata.

| Dimension | Recomputed rows/clicks | Displayed row-cost sum | Operator UI total | Campaign gap using UI total |
| --- | --- | --- | --- | --- |
| Keyword | 7 / 851 | $126.75 | $126.74 | $0.60 / 4 clicks |
| Query | 134 / 663 | $98.78 | $98.76 | $28.58 / 192 clicks |

Query cost coverage is 98.76/127.34 = **77.56%**. Row sums exceed UI totals by $0.01/$0.02. Rounding is plausible, not verified; neither the larger coverage gaps nor their causes are explained by an unsampled flag.

`vestiti uguali mamma e figlia`: 24 clicks/$3.59/one purchase key event/$151.46 revenue → 42.1894× ROAS. Separately, `abiti mamma figlia`: 435 clicks/$64.84/one purchase key event → 2.3359×. The query-to-keyword/ad-group join is **NOT VERIFIED here**. Neither selected row supersedes campaign-wide 1.1894× ROAS.

One purchase among 134 inspected queries creates substantial selection uncertainty; the selected query’s result does not establish repeatable profitability. Zero reported purchase events do not prove no orders. Missing-purchase capture and attribution remain unresolved. This query already generated paid traffic; adding it as a keyword would not itself establish incremental traffic or avoid overlapping targeting.

Retain the converting query as a hypothesis. Verify its current association before any narrowing proposal; avoid duplicate targeting. Investigate high-spend, zero-reported-purchase cohorts, starting with `costumi famiglia` (237 clicks/$35.25), without classifying relevant categories as irrelevant. No plainly irrelevant hard-negative candidate is supported by these 134 query strings. Current destination fit is another agent’s scope.

The historical nine EXACT keywords and 66 negatives establish launch scope only; seven report rows do not establish current inventory, match types, exclusions or serving status. Prepare any later narrowing decision from verified association, fit and economics; preserve control/approval gates and make no live mutation.

SHA256: keywords `b95660a32eb18a0db4fe2e9f456de6c0eba91d5269007ee2cc74c1b56bbfa7dc`; queries `ac755f774e28b455194ae6bac315166a790711b747ddebc84355fe9642b8e35e`.
