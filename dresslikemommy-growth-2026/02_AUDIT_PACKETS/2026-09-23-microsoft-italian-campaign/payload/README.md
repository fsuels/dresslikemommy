# Italian campaign payload — local extraction

Status: **PASS_LOCAL_EXTRACTION**. This folder contains source extraction and UI paste files only; no native account writes or activation.

| Group | Positive rows | Group negatives |
|---|---:|---:|
| 1. Abiti mamma e figlia | 17 | 6 |
| 2. Outfit coordinati famiglia | 20 | 8 |
| 3. Camicie e magliette famiglia | 18 | 8 |
| 4. Pigiami mamma e figlia | 17 | 0 |
| 5. Camicie papà e figlio | 15 | 8 |
| 6. Outfit mamma e figlia | 16 | 11 |
| 7. Costumi da bagno mamma e figlia | 18 | 0 |
| 8. Maglioni e felpe famiglia | 23 | 8 |

Counts: 144 positives; 120 headlines; 32 descriptions; 196 campaign Phrase negatives (112 Italian + 84 complementary English); 13 provisional campaign Exact negatives; 49 group negatives (22 Phrase + 27 conditional Exact); 8 sitelinks, 32 group associations, 6 callouts, 8 snippets.

Local validation: 51/51 checks pass, 0 length violations, 0 literal conflicts. Match/text duplicates are checked per scope. Native editorial eligibility and negative conflict report remain separate.

## Unresolved gates

- All 27 Exact group routing negatives are preserved. The attachment explicitly gates 19 rows in groups 2 and 6 on destination groups being active and eligible; the same operational gate for 8 group-3 routing rows is an inference and is labeled per row.
- 13 Exact campaign assortment restrictions are provisional: retain unless product/size evidence supports removal.
- Family-sweaters URL and its sitelink require explicit destination verification.
- Mommy & Me Outfits is absent from the 7-group native source inventory supplied by parent; eighth group needs separately determined copy/creation method.
- The 160 image-caption pairs advertised by the pasted document are absent; no inferred values included.
- Supplied complementary English negatives are literal source content, not automatically an all-Italian final-language policy.
- Local literal checks do not substitute for native negative keyword conflict report or editorial approval.

## Resolved settings

Parent reports explicit user selection of Italy/Italian: `DLM | MS | IT | IT | Search | 202609`. Preserve USD10/day, Maximize Clicks, USD0.20 max CPC in the paused copy. All eight selected suffixes use `utm_campaign=dlm_ms_it_it_search_202609`; supplied US originals remain provenance. No activation authority is inferred.

## Files

- `payload.json`: full extracted payload, source hash/line ranges, source names, conditional row metadata, extensions and supplied/candidate/selected tracking.
- `ui_ready.json`: compact UI-ready groups with multiline keyword and negative strings, ad field arrays, selected Italy suffixes, campaign settings and extensions.
- `validation.json`: counts, checks, full character lengths and limitations.
- `ui/01..08_keywords.txt`: source Exact/Phrase syntax, one row per line.
- `ui/01..08_negatives_complete_plan.txt`: all group negatives; conditional rows are not omitted.
- `ui/01..08_negatives_exact_conditional.txt`: isolated routing rows for gate-aware handling.
- `ui/campaign_negatives_*.txt`: complete and split campaign lists.
- `ui/01..08_headlines.txt`, `descriptions.txt`, `ad.json`: ad-entry fields.
- `build_payload.py`: deterministic extractor; rerunning regenerates only this owned folder.

The attachment advertises downloadable ZIP/Excel/image-caption files but provides no downloadable URLs or actual caption pairs. The claimed 40 sample-query tests and spreadsheet/ZIP validations cannot be reproduced from the pasted content; they are not adopted as performed checks.

Parent owns native source inventory, external writes/readbacks, authoritative coordination/worklog updates and independent review.
