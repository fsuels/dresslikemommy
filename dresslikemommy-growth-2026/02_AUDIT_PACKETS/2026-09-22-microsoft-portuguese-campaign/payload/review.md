# Portuguese campaign payload validation

Confidence: H for faithful text extraction and local checks; live state is unverified.

Target: `DLM | MS | BR & PT | PT | Search | 202609`, Brazil and Portugal, Portuguese. Current user geography supersedes the attachment's US market. Copy remains the supplied Brazilian Portuguese. Root owns exact native identity, permissions, browser work, current settings and all external writes. This payload grants no activation authority.

| Group | Portuguese name | Positives | Group negatives | Conditional routing subset |
|---|---|---:|---:|---:|
| 1 | Vestidos mãe e filha | 17 | 10 | 0 |
| 2 | Roupas combinando em família | 20 | 16 | 16 |
| 3 | Camisas e camisetas em família | 18 | 10 | 10 |
| 4 | Pijamas mãe e filha | 17 | 0 | 0 |
| 5 | Camisas pai e filho | 15 | 8 | 0 |
| 6 | Looks mãe e filha | 16 | 22 | 22 |
| 7 | Moda praia mãe e filha | 18 | 0 | 0 |
| 8 | Suéteres e moletons em família | 23 | 10 | 0 |

Verified: 8 groups, 144 positive Exact/Phrase entries, 120 headlines (15 per group), 32 descriptions (4 per group), 244 campaign negatives (141 Portuguese Phrase + 86 supplemental English Phrase + 17 temporary Exact), 76 group negatives, 8 sitelinks with 32 group associations, 6 callouts and 8 snippets. All 702 extracted text values are present unchanged in the supplied source. There are no same-text/same-match duplicate positive rows within or across groups, no duplicate negatives within their applied scope, and no literal positive-versus-campaign/own-group-negative conflicts. An accent-folded sensitivity check also finds zero conflicts.

Character maxima: headlines 30/30; descriptions 89/90; paths 11/15; callouts 25/25; sitelink titles 21/25; sitelink descriptions 34/35; snippet values 22/25. Limits follow the attachment. Brand, public URL slugs, tracking tokens and intentionally supplemental English negative keywords remain as supplied.

## Conditional items and exact gaps

- **All eight URLs need current verification.** Source `/pt/collections/…` paths are proposed only; the published locale may be `/pt-br`. Root must verify through the language menu and update ads, sitelinks and related destination associations consistently. The attachment specifically could not recover family-tops, swimsuits or family-sweaters. That historical limitation does not prove those pages broken or empty.
- **48 routing negatives are separated from 28 category exclusions.** Group 2 routes to 3/8; group 3 to 5/8; group 6 to 1/4/7/8. Source explicitly conditions groups 2/6 on recipient active/readiness. Group 3 is conservatively marked with the equivalent gate for root resolution. Keep Exact match, preserve the setup pause and do not transform these into broad category negatives. Category Phrase exclusions in 1/5/8 stay at their own group level.
- **Candidate tracking uses `dlm_ms_br_pt_pt_search_202609`.** Apply only after checking the real inherited/manual/automatic tagging method and copied ad-level suffixes. Null template/custom-parameter fields mean no proposed change, not clearing. Preserve `bing`, `cpc`, `{AdId}`, `{Keyword}`, and no initial `?` or `{lpurl}` in suffixes.
- **160 referenced image-caption/alt pairs are absent.** Zero image fields were available or validated. Preserve original images; obtain actual source pairs or inspect each existing image/caption before a faithful translation. Do not invent pictured people, clothing, colors or angles.
- The 17 temporary catalog Exact exclusions are source-preserved, not freshly stock-qualified. Brazilian and European Portuguese demand, native eligibility, shipping, stock, paired sizes, purchase measurement and profitability remain unverified. Never mutate lists/assets shared with another campaign while localizing the target.

Source SHA256: `76a9f8acb85169642e4f63cb88ae626195c115720af42848c8fe30ecd96eb724`.

Files: `payload.json` contains the structured candidate and provenance; `validation.json` contains check results; `paste_blocks.txt` provides source-faithful UI text with conditional routing separately labeled; `extract_validate.py` reproduces all artifacts. No shared canonical files or external accounts changed by this worker. Root integrates verified findings into its own claim/worklog.

Reproduce: `python3 /Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-22-microsoft-portuguese-campaign/payload/extract_validate.py`.

Next action: root reconcile native copied objects and published Portuguese destinations before applying the candidate.
