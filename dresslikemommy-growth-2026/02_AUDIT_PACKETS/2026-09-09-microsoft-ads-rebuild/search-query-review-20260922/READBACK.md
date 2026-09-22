# September 21 clicked-query review

Action `TA15-SEARCH-QUERY-REVIEW-20260922` — account **477439**, customer **770182**. Native evidence captured September 22, 12:25–12:33 UTC. Local diagnostic complete; live optimization and tracking repair remain **PARTIAL/BLOCKED**.

## Finding that changes the decision

The U.K. campaign **506255081** currently has **Maximize Clicks**, its maximum-CPC checkbox checked, and **USD0.20** in the native Max. CPC field. This exceeds the retained owner ceiling of **USD0.15**. The campaign was Enabled, English, with an individual configured USD20/day budget. No setting was entered or saved. The current setting is not a change-history proof of the setting during yesterday's clicks, and the configured budget is not spending authority.

September 21's Search report contains **20 clicked queries, USD2.97 spend and 20 clicks**. Every captured query has one click. **12 reported clicks cost more than USD0.15**, accounting for **USD2.21** of reported spend. The unrounded mean is USD0.1485, which shows why the rounded USD0.15 average cannot demonstrate compliance on each click. Amounts are the native report's displayed USD values.

| Campaign label | Search clicks | Search spend | Clicks above USD0.15 |
| --- | ---: | ---: | ---: |
| US | 13 | USD2.08 | 9 |
| GB | 4 | USD0.58 | 2 |
| CA | 1 | USD0.19 | 1 |
| AU | 1 | USD0.09 | 0 |
| EUR | 1 | USD0.03 | 0 |

The 20 rows reconcile to all reported Search clicks and spend. Their 23 impressions do **not** represent all 617 Search impressions. The native report showed 92 terms before the report-only `Clicks > 0` filter. Audience placements are outside this query report. Campaign labels and English query text do not prove user country or language demand.

## Narrow exclusion review

Nineteen clicks were reported as Phrase close variants and one as an Exact close variant. All 20 rows have a disposition in [analysis.json](analysis.json). Relevant shopping queries remain protected; generic or product-specific queries require actual offer and destination checks.

Two literal **Exact ad-group** candidates are prepared as **conditional local review options**, not approved exclusions or an upload file:

| Query | Bound campaign / ad group | Evidence and limit |
| --- | --- | --- |
| `celebrity family event outfits` | GB 506255081 / Family Matching Outfits 1275435292356142 | One click, USD0.09. Could be editorial inspiration or shopping; offer mismatch is unverified. |
| `top 10 family costumes` | US 506254907 / Family Matching Outfits 1275435291895118 | One click, USD0.20. List/research wording is a hypothesis, not demonstrated waste. |

The selected live behavior is to retain these terms until actual ad/destination fit, inherited negative associations, conflicts, and exact write authority are resolved. The two historical clicks cost USD0.29; that is **not forecast savings**. No broad exclusions for mother, baby, costume, Disney, photographs, or seasonal terms were proposed. Core mother/daughter dress queries must not be removed merely because they appeared in the broader family group.

Microsoft documents Exact/Phrase negatives and campaign/ad-group inheritance; that supports the proposed narrow method but does not establish the commercial merit of either exclusion. [Microsoft negative-keyword documentation](https://learn.microsoft.com/en-us/advertising/guides/negative-keywords?view=bingads-13), retrieved September 22.

## Authority and verification

Current owning controls remain `READ_ONLY_MARKETING_RECONCILIATION`, `FRESH_ACTION_TIME_APPROVAL_REQUIRED`, `approved_external_scope: NONE`. The existing six-campaign pause and numeric daily-budget/maximum-30-day-loss questions remain pending and were not repeated. No new budget, status, bid, tracking, campaign, support, billing, or order action was performed. No shared writer interval exists; shared canonical records were not edited.

On the U.K. settings page, clicking Cancel after a read-only inspection produced an unexpected unsaved-changes warning. The operator clicked **No**. Settled AX confirmed the warning closed; no field was edited, no Save or discard confirmation was accepted. The cause is unknown. Task-owned tab6 is retained at this page; resolve this warning and obtain a fresh before-state before any future write. The temporary U.S. identity-lookup tab was closed; UET and query-report tabs were retained.

Root arithmetic and consistency checks passed **25/25**. [Independent review](independent-review.json) returned **PASS_WITH_LIMITS** across 24 focused checks (18 machine checks and six manual reviews), with no corrections required. Neither candidate is presently justified for live application. The review covers saved evidence; independent native replay was NOT RUN. Strict continuity passed all 10 checks before handoff; final delivery state belongs in the execution checkpoint.

Zero reported conversions/revenue do not establish zero orders while measurement remains unresolved. No verified CPA, ROAS, contribution profit, savings or sales increase is claimed. The previous receiver/completed-day packet was accepted by the parent at 09:06 UTC; it was not repeated. No newly verified support response was found in the retrieved state, and no unchanged support-routing retry was made.

## One next action

Resolve the **existing paid-control decision** before more active delivery or expansion: the fresh GB cap mismatch adds evidence to the pending decision. A possible GB correction is exactly USD0.20 to USD0.15, but it remains **not entered/not saved**, with no bundled budget, strategy, status or tracking changes. Do not repeat the pending question.

Independent queue: inspect the actual ad/destination for the two literal query candidates; use the existing support case 7108824779 only when its authenticated channel premise changes; preserve the parent's next full sales clock, no earlier than September 22 at 20:33:21 UTC absent material lifecycle/cost changes. Do not repeat this completed query extraction or reopen completed country/product audits.

Continuation: use [the canonical prompt](../../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md), resume `TA15-SEARCH-QUERY-REVIEW-20260922` with a changed authority/support premise or the bounded candidate destination check. Latest retrieved relevant parent anchor: `2026-09-22-ceo-google-organic-order-verified`.
