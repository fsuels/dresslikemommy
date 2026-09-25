# Product body structure and placeholder handoff

Local source-bound candidates only. Root owns live release, GitHub main reconciliation and public verification.

## Independently reviewed first cohort

The final structural cohort is 375 unique product/locale body fields. Author versions v1–v4 remain frozen. Use the independent final copy at `../article-title-independent/body_structure375_reviewed.json` (SHA256 `f8ae9d61b29a01f6628edf21cbf84421efd9c893f7d40f1e86c13538818ac501`). It includes the reviewer’s seven final image-alt quote encodings. All 375 parsed structures and 441 parsed image attribute records passed independent checks. The final header v2 baseline also carries these seven encodings.

## Placeholder cohort awaiting independent qualification

`placeholder_candidates_v2.json`: 88 unique current fields, SHA256 `935093c964c983e916af8a336fe517b2b610b9dd455b16eee1f46c2fe1af9d44`.

- 87 fields restore corrupt placeholder fragments; one Romanian P134 field restores an incorrect opening `strong` to the source-backed closing `li`.
- Exact old/new patches and full English source quotes are embedded per row. Original before/source/digest/raw bindings remain intact. Root must compose with the reviewed header/size-label values and rebind the fresh before object before release.
- Seven source-backed prose items require independent meaning review: P153 CS/EL/FI, P154 CS/EL/FI, P182 DE. The Greek P145 missing Key Features heading is also localized explicitly. All other changes restore tag boundaries or remove corrupt token characters while retaining actual prose.
- `placeholder_checks_v2.json`: all 88 source/before/digest bindings checked against 20 frozen raw files; exact explicit-patch reconstruction; table, URL and image bytes unchanged; no remaining corrupt token fragments in candidates; no nonoptional structure failures under the bounded optional-tag checker. Three deliberate corruptions were rejected.
- `placeholder_held_v1.json`: six outdated P215 fields are held for full content review. All six already belong to the original source-disposition body holds. None of the current 88 fields overlaps the original 595 unresolved source-disposition tuples.

## Scope and classification

The inventory covers 4,760 fields (238 products × 20 published non-English locales), after the 327 verified released body overlays. The full scan found 93 genuine QZ/XTOKEN/QX artifact bodies with 127 corrupt fragments. Twenty additional QZ matches were unchanged source image filenames and are false positives.

Of the 193 strict-stack warnings outside the original structural cohort, 112 reflect optional end-tag omissions, 70 reflect ignored stray closing list tags with implicit paragraph closure, and 11 reflect actual nonoptional structure errors. These categories describe parser behavior; visible placeholder corruption is a separate dimension. The final 88 repairs resolve all 11 nonoptional structure errors in that set. The optional-tag checker implements explicit bounded HTML5 rules, not a complete browser or HTML5 parser. Browser verification is NOT RUN in this lane.

## Separate unresolved evidence

- `existing_prose_scope_differences.json`: 11 current fields have a later five-item feature list in English that is absent from the stored translation. These are P166 CS/DA/EL/NO, P171 EL, P176 EL/FI/RO, P178 EL, P191 EL and P196 EL. Minimal placeholder repairs do not establish full-body completeness.
- `legacy_image_count_differences.json`: seven existing source/target image-count differences are preserved; no images were deleted or invented to force sequence equality.
- The initial source-unique size-label inventory and P51 queue were handed to the independent size-label owner. This lane does not duplicate that work.

No Shopify/API/provider calls, Git/index writes, browser actions or canonical state mutations were performed in this lane.

## Subsequent eleven-description completion

Root expanded this lane to the 11 evidenced omissions and stale prose clauses. `prose_completion11_candidates_v1.json` is frozen at SHA256 `1f02da30ede31cd4c0bbcaf94e1413796c201eeaf3befb2c3da37e9a68b0bc2a` and is pending independent full meaning review by agent A. It uses the independently reviewed `placeholder88_reviewed.json` as its planned before.

The candidates translate 154 missing source-tail text nodes, correct 56 evidenced stale or mistranslated first-list clauses, and retain 10 correct first-list clauses. All 22 reviewed table elements remain byte-exact. Full source/target prose was read for the six products and 11 locale variants. Source prose numbers and element sequences match, standard HTML parser balance passes, raw/source/planned-before bindings pass, and two negative corruption tests are rejected. See `prose_completion11_checks.json` and `prose_completion11_delta_ledger.json`. English source was not changed. Root still owns fresh guards, release receipts and public verification.
