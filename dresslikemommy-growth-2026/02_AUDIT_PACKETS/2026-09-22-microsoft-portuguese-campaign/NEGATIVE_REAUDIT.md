# Negative keyword audit — September 22, 2026

Target: **DLM | MS | BR & PT | PT | Search | 202609**, campaign **506255983**, account **477439**. Campaign remains paused.

**Corrected:** 48 missing exact-match Portuguese negatives were added to three ad groups. Fresh native Microsoft exports confirm all244 suppliedcampaign negatives and all76 suppliedgroup negatives, with0missing and0duplicates. Earlier completion wording was too broad: it counted only28unconditional group terms and omitted48routing terms. The current explicit request completes those entries in the paused draft; recipient eligibility remains a check before any separatelyauthorizedlaunch.

| Ad group | Planned and present | Obsolete copied extras | Current total |
|---|---:|---:|---:|
| Vestidos mãe e filha | 10 | 23 | 33 |
| Roupas combinando em família | 16 | 39 | 55 |
| Camisas e camisetas em família | 10 | 31 | 41 |
| Pijamas mãe e filha | 0 | 17 | 17 |
| Camisas pai e filho | 8 | 25 | 33 |
| Looks mãe e filha | 22 | 25 | 47 |
| Moda praia mãe e filha | 0 | 16 | 16 |
| Suéteres e moletons em família | 10 | 0 | 10 |

Pajamas and swimwear correctly have **zero additional ad-group negatives in the supplied plan**. The244campaign negatives apply to them. Their current17/16English group exclusions are obsolete copies requiring cleanup.

Campaign:244planned present,11obsolete extras,255current total. Group:76planned present,176obsolete extras,252current total. Permanent removal of **187 obsolete negatives** will produce exact244/76lists. No negatives have been permanently deleted. The earlier152pausedEnglishpositivecleanup remains separate.

Local comparison against all144supplied positivekeyword rows found0literal exact/phrase conflicts after case, punctuation and accent normalization. This doesnotclaim a Microsoft platform conflict report or serving eligibility.

The remaining action-time confirmation is required by the Computer Use tool policy: permanent deletion has no normal Microsoft undo. Exact11campaign and176group IDs were captured in `review/final_paused_readback.json`; the current comparison includes everyobsolete text/match/group tuple. All76planned grouprecords must be retained, including the48newExactrows. Do not apply the stale28-target cleanup rule.


## September 23 continuation — partial cleanup, browser input blocked

The user replied **continue** to the exact 187-negative deletion proposal. This is recorded authorization for that scoped cleanup; no new deletion approval is pending.

- **Implemented:** native Delete submitted for exactly the eleven obsolete campaign IDs, after each ID/text/match was reread and the toolbar confirmed eleven selected. The table refreshed with selection cleared and persisted through reload. Pagination indicates 244 remaining (thirteen pages at twenty rows, four on the last page).
- **Verification limitation:** the virtualized DOM capture recovered 164 unique remaining rows, not all 244. New Export attempts produced no downloaded file. Full text/match reconciliation is therefore BLOCKED, not complete.
- **Not implemented:** no ad-group Delete was invoked. Twelve obsolete Dresses rows were selected before an input failure; reload discarded that selection. The 176 obsolete group entries remain pending. All 76 intended entries were verified in the preceding complete native export; that evidence remains dated September 22.
- **Blocker:** side-panel controls stopped accepting input reliably. Native and Playwright checkbox/navigation controls, a fresh same-IAB tab and a runtime reconnect did not resolve it. No authentication or permission failure was observed; no macOS grants or helpers were changed.
- **Current safety state:** exact target campaign still Paused. No positive-keyword, activation, budget, source, peer or shared-asset changes.

Resume in IAB2/tab3; original tab1 and previous working tab2 are preserved. Reconcile the campaign list first, then remove only still-present IDs in the 176-group manifest, retaining all 76 desired entries. Do not repeat additions or infer the earlier 28-row target. Full checkpoint: `review/negative_cleanup_checkpoint_20260923.json`.


## Later September 23 restart checkpoint — supersedes the previous browser hold

Fresh native export now verifies **244/244 campaign negatives, zero missing/extra/duplicates**. Group before-export confirmed252rows=76desired+176approvedextras. Removed25obsolete Looks rows and39obsolete FamilyOutfits rows with post-action native readbacks. The31-row FamilyShirts Delete action then timed out; **its outcome is UNKNOWN** and must be reconciled before any repeat. Another81approvedobsolete entries have not been attempted.

Browser control is waiting on a possible native confirmation; its presence is not confirmed. Native Codex/ChatGPT app inspection was refused by the computer-use safety layer. User dialog-check question is pending. Current task browser is IAB1/tab1 and is preserved. Existing cleanup authorization persists. Campaign remainsPaused; positive keywords and other assets unchanged.

Evidence: `negative_campaign_final_20260923.csv`, `negative_group_before_cleanup_20260923.csv`, `review/negative_cleanup_progress_after_restart_20260923.json`. Local strict continuity all10PASS and scoped diff checkPASS; these do not resolve the pending external write.
