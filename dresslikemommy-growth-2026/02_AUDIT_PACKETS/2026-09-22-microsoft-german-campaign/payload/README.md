# German campaign payload

Local review/input artifact. This directory is not a live account readback or a second command layer. Root owns all Microsoft actions and canonical continuity.

Target: `DLM | MS | DE | DE | Search | 202609`, Germany, German. The current user target overrides the attachment's US/German target. Every group suffix uses `utm_campaign=dlm_ms_de_de_search_202609`; source/medium and Microsoft macros are preserved. Budget and bidding remain null because the attachment supplies no numbers.

## Inputs and outputs

- `campaign_payload.json`: complete extracted campaign, all eight groups, extensions, source provenance, limitations and optional copy edits.
- `group_01.json` through `group_08.json`: individually consumable group records.
- `group_NN_positive_keywords.txt`, `group_NN_negative_keywords.txt`: quote/bracket syntax ready for the correct positive or negative UI. Groups 04 and 07 intentionally have empty negative files.
- `group_NN_rsa.txt`: URL, paths, 15 headlines, four descriptions and suffix.
- `campaign_negative_keywords.txt`: 230 rows, comprising 218 phrase and 12 provisional exact exclusions. Separate phrase/exact files are also supplied.
- `sitelinks.json`, `callouts.txt`: text extension payloads. Each group's JSON contains its four sitelink associations and structured snippet.
- `optional_copy_edits_not_applied.json`: six minor phrasing/hyphenation improvements. These have been length-checked, but source copy remains unchanged in campaign/group/RSA outputs.
- `validation.json`: full counts, individual length checks, exact duplicates, intentional sharp-s/ss equivalences, and literal exclusion checks.
- `source_crosscheck.json`: 403/403 separate source membership, target override and structure checks passed.
- `build_payload.py`: deterministic extraction/validation, with no network or account access. Run with `python3 build_payload.py`.

## Validation

| Group | English mapping | Positives | Group negatives |
|---|---|---:|---:|
| Kleider für Mutter und Tochter | Mommy & Me Dresses | 17 | 6 |
| Familienoutfits im Partnerlook | Family Matching Outfits | 20 | 9 |
| Familienhemden und T-Shirts | Family Matching Shirts | 18 | 7 |
| Schlafanzüge für Mutter und Tochter | Mommy & Me Pajamas | 17 | 0 |
| Hemden für Vater und Sohn | Father & Son Shirts | 15 | 6 |
| Outfits für Mutter und Tochter | Mommy & Me Outfits | 16 | 15 |
| Bademode für Mutter und Tochter | Mommy & Me Swimsuits | 18 | 0 |
| Familienpullover und Hoodies | Family Matching Sweaters | 23 | 6 |
| Total | | 144 | 49 |

PASS: eight groups, 144 positives, 120 headlines, 32 descriptions, 136 German phrase plus 82 supplemental English phrase plus 12 provisional exact campaign negatives, 49 group negatives, eight sitelinks, six callouts, eight snippets. All supplied titles/descriptions/paths/extension fields meet the attachment's stated limits. No literal conflicts with campaign or own-group negatives; no exact duplicate keyword-and-match-type rows within a scope or across positive groups.

The German negative spellings `großhandelslieferant`/`grosshandelslieferant` and their plurals are intentionally preserved. Python casefold considers them equivalent, which is not evidence of Microsoft accepting/rejecting them as duplicate rows. Native readback should reconcile their saved form.

Sitelink titles are printed twice in the paste (a heading followed by the actual title). Extraction verifies the repeats agree and retains one title plus the two real descriptions, avoiding a shifted description field.

## Limits and native review dependencies

The attachment refers to downloadable ZIP/Excel/160 image-caption-and-alt-text pairs/40 query tests but supplies none of their content or actual download links. Image text is null, never invented. Root can retain source pictures and translate observed live captions/alt text separately if authorized. No image asset mapping was inspected by this worker.

The 31 Exact group negatives (groups 02, 03 and 06) separate category intent and depend on the intended destination groups being active and eligible. A negative exclusion does not force another group to serve. The remaining 18 group negatives are phrase exclusions for swim dresses in ordinary dresses, tees in the button-shirt group, and sweater dresses in ordinary sweaters. Do not move group exclusions to campaign level.

The 12 campaign Exact negatives are explicitly provisional assortment exclusions in the source. They are not fresh catalog findings. The 82 English phrase negatives intentionally remain to filter mixed-language unwanted searches; they are not untranslated positive keywords.

The source flags the family-sweaters destination as unverified and calls for all localized landing/checkout paths to be checked. Root's later live observations are separate evidence and may resolve that source limitation; this worker made no external reads. Stock, sizes, prints, shipping, returns and conversion readiness are not proven by this local text validation.

Source German is comprehensible. Optional edits improve compound hyphenation and two awkward phrases; English loanwords such as Outfits, Hoodies, Prints, Sets and Partnerlook are established fashion usage. No free-delivery, deadline, UV-protection, review, promotion, stock or local-store claim has been added.

Microsoft semantic matching, inherited exclusions, account language, tracking precedence, editorial review and serving are outside these checks. Root must verify exact live campaign identity, copied child inventories, monetary configuration and all saved fields.
