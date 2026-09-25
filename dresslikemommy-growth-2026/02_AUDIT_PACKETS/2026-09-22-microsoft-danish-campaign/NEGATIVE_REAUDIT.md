# Negative keyword re-audit — verified

Campaign: DLM | MS | DK | DA | Search | 202609, ID 506254908; Microsoft account477439/customer770182. Current user explicitly requested correction of campaign and missing ad-group negatives.

On September22 at16:35–16:39 America/New_York, direct navigation to the previously visited native negative-keywords page restored usable controls. Before-state confirmed20 direct group negatives. Added25 supplied Exact exclusions:8 to Matchende familietøj,6 to Familieskjorter og T-shirts,11 to Matchende tøj til mor og datter. Each group and multiline value was read before Save; text fields were blurred. No deletion, campaign-status, budget, bid, shared-list, image or other-campaign edit occurred.

## Saved result

Native rendered-table readback captured201campaign rows and45group rows. Separate full native Export files were then compared by text, match type, campaign and group against all246expected rows:

- Campaign201/201 matched:192Phrase+9Exact;0missing,0unexpected.
- Ad group45/45 matched:20Phrase+25Exact;0missing,0unexpected.
- Group counts in source order:6/8/6/0/8/11/0/6.
- Nattøj til mor og datter and Badetøj til mor og datter intentionally have0direct negatives; campaign exclusions apply.

Evidence: negative_campaign_native_export.csv and negative_group_native_export.csv are original UTF16 TSV native downloads, dated16:38:39 and16:39:11ET. negative_comparison.json records the exact comparisons. The prior20/held25 state and browser blocker are superseded by these saved readbacks. All25routingExact terms have matchingExactpositive terms in intended recipients, and payload review found0literal own-positive conflicts across144positives. This is not a simulation of all Microsoft matching or a fresh inventory audit of the9temporary assortment exclusions.

Campaign header is currentlyEnabled; root didnotactivate or change status. EarlierPaused evidence remains historical. Microsoft's full editorial eligibility was not independently recertified by this negative-only correction. No serving, sales or performance outcome is inferred.

Rollback: these25new rows can be located by exact group/text in the native group export. Permanent deletion would require the applicable action-time confirmation; do not delete existing20category rows. No rollback is currently needed.

Independent final export review PASS in payload/negative_final_verification.md: all246rows match both payload and expected CSV,0duplicates,0literal own-positive conflicts. The verifier did not execute the live changes.

Local closeout checks: bundled Python ops/scripts/check_continuity_integrity.py --strict returned CONTINUITY_OK (exit0); scoped git diff --check returned exit0. Independent review is separate from root execution. The browser remains on the native Ad group negative-keyword view.
