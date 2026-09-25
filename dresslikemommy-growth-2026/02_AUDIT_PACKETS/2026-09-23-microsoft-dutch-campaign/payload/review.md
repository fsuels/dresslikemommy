# Dutch payload review — local extraction only

Confidence: H for supplied-text extraction and mechanical checks; no account or storefront readback.

`campaign_payload.json` preserves the supplied Dutch copy, Exact/Phrase distinctions, eight destinations, two paths per ad, source suffixes, extension content and mapping. `source.txt` is a verbatim copy; SHA-256 is recorded. `parse_payload.py` reproduces extraction and `validation.json`.

Verified counts: 8 groups, 144 positive rows (62 Exact/82 Phrase), 120 headlines, 32 descriptions; 202 campaign negatives (111 Dutch Phrase + 82 English Phrase + 9 temporary Exact); 45 group negatives (20 Phrase/25 Exact); 8 sitelinks, 32 group associations, 6 callouts and 8 structured snippets.

| Group | Positive rows | Own negatives |
|---|---:|---:|
| Jurken voor moeder en dochter | 17 | 6 Phrase |
| Matching familiekleding | 20 | 8 Exact |
| Overhemden en T-shirts voor families | 18 | 6 Exact |
| Pyjama’s voor moeder en dochter | 17 | 0 |
| Overhemden voor vader en zoon | 15 | 6 Phrase |
| Matching outfits voor moeder en dochter | 16 | 11 Exact |
| Badkleding voor moeder en dochter | 18 | 0 |
| Matching familietruien en hoodies | 23 | 8 Phrase |

All supplied ad, path, callout and sitelink text passes its stated character limit. Snippet values also pass a 25-character candidate check. No duplicate keyword/match tuples within their applicable scopes and no literal positive conflict with campaign or own-group negatives were found. Literal testing uses case-folded word tokens and does not certify Microsoft's semantic matching or current native negative lists. No Dutch text correction was required for these checks.

The market is unresolved: the request says `NL | NL`, whereas the attachment explicitly says United States, `US | NL`, and `dlm_ms_us_nl_search_202609`. Both are preserved; resolved campaign name, market and suffix fields are null pending root's owner clarification. The source settings table has a truncated campaign-name cell (`DLM`), but the full attachment name appears elsewhere.

Retain all 45 group-negative rows in the reconciliation plan. The attachment explicitly conditions 19 rows (family clothing's 8 and mother/daughter outfits' 11) on the corresponding specific groups being active and suitable. Another 6 Exact rows route families' shirts to father/son shirts or sweaters. Do not silently omit these rows or promote them to campaign scope. Nine campaign Exact restrictions reflect an unaudited historic assortment assumption. Root must resolve applicability against current target/destination evidence while preserving paused state.

Image captions are missing: the attachment references 160 pairs in download files, but includes neither those pairs nor usable download links. The claimed 320-field image validation cannot be reproduced. Source artwork should remain unchanged; any captions require actual source-asset evidence.

The attachment's prior public-page, 40-query, spreadsheet and ZIP checks are assertions only. Three source URLs are explicitly provisional (`family-tops`, `swimsuits`, `family-sweaters`); all eight live-readback flags remain false in this extraction. Claims about garment offerings, shared adult/child sizing and destination suitability require root verification. No new budget, bids, purchase goal or activation authority is supplied by this packet.

Next: root resolves geography and uses the full payload for native target-only completion/reconciliation. Canonical state and all external actions remain root-owned; no such files or accounts were changed here.
