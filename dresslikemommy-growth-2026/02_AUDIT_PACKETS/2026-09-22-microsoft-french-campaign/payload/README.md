# French campaign source payload

LOCAL CANDIDATE — not uploaded or independently verified in Microsoft Ads.

Target supplied by root: `506255077` / `DLM | MS | FR & CA | FR | Search | 202609`.

`campaign_fr_payload.json` contains every supplied ad/keyword/extension string plus group-level paste blocks. `group_01.json` through `group_08.json` provide compact group reads. `campaign_negatives.txt` contains all 251 campaign exclusions. `parse_attachment.py` reproducibly parses the user attachment and writes these artifacts. `validation.json` records validation and facts needing current landing-page evidence.

## Verified local counts

| Content | Count |
|---|---:|
| Groups | 8 |
| Positive keywords | 144 |
| Headlines | 120 |
| Descriptions | 32 |
| Group negatives | 58 |
| Campaign French phrase negatives | 151 |
| Campaign English phrase negatives | 86 |
| Campaign temporary exact negatives | 14 |
| Callouts | 6 |
| Sitelinks | 8 |
| Structured snippets | 8 |
| Image text pairs actually supplied | 0 |

All 120 headlines meet 30 characters; all 32 descriptions meet 90; all display paths meet 15. Callouts meet 25, sitelinks meet 25/35/35, and snippet values meet 25. No duplicate keyword/match pairs or lexical positive/negative conflicts detected. This does not simulate Microsoft matching or inspect inherited account negatives.

## Decisions and evidence still owned by root

- The attachment is explicitly US/French and carries `dlm_ms_us_fr_search_202609` UTM campaign values. The current user target overrides its campaign name. `candidate_final_url_suffix_for_fr_ca` changes only that UTM campaign value; apply only after current geography and inherited/manual tracking are reconciled. The original suffix is retained separately.
- Exact routing negatives in groups 2 and 6 are explicitly conditional on the specific destination groups being eligible to serve. Apply the same dependency check to group 3 routing negatives. The payload preserves all strings and identifies this condition rather than silently dropping them.
- The 14 catalog-specific exact negatives are acknowledged as stale by the source and need a current availability decision.
- Product assortment, adult/child purchasability, per-piece pricing, size guides, delivery estimates/options and return conditions are factual claims needing landing evidence. The copy avoids unsupported guaranteed arrival, free returns, UV/UPF, physical stock and promotional claims.
- Source says family tops and family sweaters French URLs were not verified, and father-son/cart/shipping had English. This is historical source commentary, not current evidence.
- The source references 160 image-caption/alt pairs and downloadable files but provides neither pair strings nor usable download links. Images may be reused under the user's request; existing text still needs a live readback before translation.

No ad, keyword, negative or extension text was rewritten. The parser only supplies the current target campaign identity and a clearly marked candidate geography-specific tracking suffix. Root owns live writes, independent validation, canonical records and the final campaign result.
