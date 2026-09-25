# German campaign saved-content review

Verdict: **PASS_WITH_GATES**. Checks: **50/50**. Overall status remains **PARTIAL_KEYWORD_CLEANUP_APPROVAL_PENDING**.

Reviewed campaign506256066 against supplied payload and root-authored native receipts; no browser/external access or independent live replay.

| Area | Reconciled evidence |
|---|---|
| Positive keywords | 297=144intended Enabled+153obsolete Paused; no reported missing/duplicate/status issue |
| Campaign negatives | 241=230intended+11obsolete |
| Group negatives | 225=49intended+176obsolete |
| Cleanup manifest | Exact match to all340extra tuples; zero intersection with intended payload tuples |
| Ads | 8RSAs,120headlines,32descriptions; root reports216checked fields and zero differences |
| Text extensions | 8campaign sitelinks,32exact mapped group associations,6callouts,8snippets; unique native IDs |
| Images | 95associations=90German+5uncaptioned;76unique new IDs disjoint from original IDs; root reports95picture/crop matches and zero caption differences |
| Campaign | Paused, German, Germany presence-only; fresh expanded settings recorded; copied10USD/day MaxClicks0.20USD; no monetary edits |

One obsolete English positive has a `Disapproved` delivery label; all153remain operationally Paused and included in the exact cleanup manifest. This does not establish a German ad issue.

## Remaining gates

- Await existing exact340record permanent-cleanup confirmation. No deletion attempted. This review grants no deletion or activation authority.
- After authorized cleanup, independently reconcile final144/230/49inventories using fresh native rows.
- Retain campaign pause. Editorial processing,31conditional routing-negative recipient eligibility, tracking/checkout readiness and activation remain separate.

## Evidence limits

The review recomputes payload totals, all exact cleanup tuples, mapping/count arithmetic, uniqueness, image ID disjointness and dictionary lengths. Intended native row inclusion,216actual ad fields, extension text, captions and95crop matches rely on root’s supplied reconciliation/receipt results; their raw per-field native values are not embedded in the specified files. Separate new image IDs support copy isolation but do not independently prove source/shared immutability. The truncated dictionary key remains an explicitly qualified translation; a source-wording confirmation is not separately documented here.

Full check results and input hashes are in `content_completion_review_20260923.json`.
