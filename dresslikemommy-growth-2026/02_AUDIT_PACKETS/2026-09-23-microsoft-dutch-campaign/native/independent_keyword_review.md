# Independent saved-keyword review

Confidence: H. **PASS_WITH_GATES** for desired keyword coverage in these saved exports; campaign completion remains unverified.

| Scope | Desired present | Extras | Missing | Duplicate tuples |
|---|---:|---:|---:|---:|
| Positive keywords | 144/144 | 132 | 0 | 0 |
| Campaign negatives | 202/202 | 0 | 0 | 0 |
| Ad-group negatives | 45/45 | 151 | 0 | 0 |

All 144 desired positives are Enabled; all 132 English extras are Paused. **All 16 desired mother/daughter-outfit keywords show Delivery=Draft ad group.** One paused English extra, `mom and son matching shirts` (Phrase, family-shirts group), shows Disapproved. The remaining 259 rows show Campaign paused. These are saved-export states, not a fresh live observation.

Campaign negatives exactly match 193 Phrase and 9 Exact entries. All 45 desired group negatives match their proper groups, including intentional zero-additional-negative groups.

The complete cleanup dictionaries exactly equal the independently calculated extras: 132 positives, zero campaign negatives, 151 group negatives. No desired tuple is included. Root reconciliation counts, statuses, hashes and exclusions agree. Four named aggregate positive-report footer rows were excluded; no keyword row was dropped. Comparison used exact campaign/group/text/match tuples without normalization.

Every row names `DLM | MS | NL | NL | Search | 202609`; all group names match the payload. IDs are absent from these exports, so campaign506255078 binding relies on root context.

The 151 extra group negatives and 132 paused English positives remain. The Draft group is incomplete. This review authorizes no cleanup, retry or activation; root's reported write stop pending user remains.

RSAs, text assets, images/crops, targeting, bids, subsequent live changes, semantic matching and performance were not independently verified. No browser/account action occurred. Full hashes, parsing method, per-group counts and checks are in `independent_keyword_review.json`.
