# Polish Microsoft Search payload — local preparation

Target: `DLM | MS | PL | PL | Search | 202609`, Poland, Polish. Current user scope supersedes the attachment's US/Polish market. This folder is a prepared payload, not evidence that Microsoft has saved or activated anything.

`campaign_payload.json` is the complete structured payload. `group_01.json` through `group_08.json` provide individual groups. Matching `_positive_keywords.txt`, `_negative_keywords.txt`, and `_rsa.txt` files provide paste blocks. Campaign negative blocks are available combined and separately by Phrase/Exact and Polish/English. `sitelinks.json`, `callouts.txt` and `structured_snippets.json` contain extensions; each group JSON names its four sitelink associations.

The 84 English supplementary Phrase negatives are intentionally preserved from the attachment. Empty negative files for groups 4 and 7 mean zero additional group negatives, not a missing extraction.

| Group | Polish name | Positives | Group negatives | Match type |
|---|---|---:|---:|---|
| 1 | Sukienki dla mamy i córki | 17 | 10 | Phrase |
| 2 | Ubrania dla całej rodziny | 20 | 10 | Exact, conditional routing |
| 3 | Koszule i koszulki rodzinne | 18 | 6 | Exact |
| 4 | Piżamy dla mamy i córki | 17 | 0 | — |
| 5 | Koszule dla taty i syna | 15 | 9 | Phrase |
| 6 | Stylizacje dla mamy i córki | 16 | 21 | Exact, conditional routing |
| 7 | Stroje kąpielowe mama i córka | 18 | 0 | — |
| 8 | Swetry i bluzy dla rodziny | 23 | 8 | Phrase |

Local verification passed: 8 groups; 144 positive keywords; 120 headlines and 32 descriptions; 145 Polish + 84 English Phrase campaign negatives, plus 18 Exact campaign negatives; all 64 group negatives; 8 sitelinks with 32 group associations; 6 callouts; 8 snippets. Unicode length checks against attachment limits passed. No within-scope duplicate keyword/match tuples or literal conflicts with campaign/own-group negatives were found. Full results are in `validation.json`. Whole-attachment keyword multiset and verbatim text checks are in `source_crosscheck.json`.

Preserve the conditional routing information in groups 2 and 6. Their 31 Exact negatives belong to the full expected payload; the attachment says to use them when the receiving specific groups are active and eligible. Routing does not itself prove another ad will serve.

`proposed_final_url_suffix` is conditional on parent native tracking readback. Only its campaign identifier changes from `dlm_ms_us_pl_search_202609` to `dlm_ms_pl_pl_search_202609`. Source suffixes are retained separately. No automatic clearing of existing templates/custom parameters or duplicate UTM tagging is authorized by this file.

Material discrepancies and limits:

- The attachment claims 160 image caption/alt pairs but actually supplies **zero**. No caption or image content has been fabricated. Parent must reconcile existing native assets or obtain the missing actual material.
- The attachment campaign settings table contains a truncated campaign-name cell, `` `DLM ``; the exact current user target name controls.
- Attachment URL checks are historical; parent is responsible for current destination verification. The payload marks all eight destinations as requiring that independent live check.
- Budget, bid strategy, native target ID and live status remain `null`; this delegated lane did not inspect Microsoft. Attachment source names/match sequences do not establish native source parity.
- Literal tests do not reproduce Microsoft semantic matching or inspect inherited/shared exclusions. Product availability, checkout, tracking and editorial approval are not established here.

To rebuild from the user attachment, run `python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-23-microsoft-polish-campaign/payload/build_payload.py` from the repository root. It reads only the supplied attachment and writes only this folder. Parent owns native actions, final reconciliation and canonical continuity updates.
