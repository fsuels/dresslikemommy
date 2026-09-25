# Independent Polish campaign closeout review

**Verdict: PARTIAL_BLOCKED is accurate. Campaign 506256099 is reported saved Paused with the requested Polish content and Poland settings; obsolete group negatives and image localization remain unfinished. No activation is authorized or reported.**

Confidence: high for the local consistency, scope and manifest checks below; live facts are parent-provided native observations. This verifier did not use a browser, replay any native check, alter the payload, or perform external/canonical writes. Only this review file was written.

## Evidence reviewed

- `final_native_verification.json`, including the subsequently supplied explicit native sitelink, callout and snippet rows.
- `negative_reconciliation_and_cleanup.json`.
- `payload/campaign_payload.json` and `payload/image_caption_translations.json`.
- Parent clarification that the rejected image attempt preceded the remaining-caption translation file; three successfully saved pairs match their prepared entries.

The final native receipt identifies account477439/customer770182, source506254907 and target506256099 with the exact PL/PL name. It reports Paused, Poland presence targeting, Polish campaign/eight-group language, USD10/day, Maximize Clicks and checked USD0.20cap. These are internally consistent with the authorized paused build.

## Independent local checks

The original comparison performed447 checks:446 passed, while one detected a real wording difference for the rejected image attempt, explained below. After explicit asset rows were supplied, another51 field/mapping checks passed (43 sitelink/callout and8 snippet comparisons). These are checks of saved evidence, not independent native replay.

- **Keywords:** group Polish counts17/20/18/17/15/16/18/23 sum to144. Paused English counts21/20/18/17/15/21/18/23 sum to153; all153 recorded English keyword IDs are unique. **144+153=297**. The receipt reports no missing Polish or unexpected enabled rows. The campaign remains paused even though144 Polish keyword rows are enabled under it.
- **Eight RSAs:** eight unique IDs, each reports15 exact headline and4 exact description comparisons after reopening its native editor:120+32=152 text comparisons. Actual URL, path and suffix values saved in the receipt match the corresponding payload fields. The receipt does not store the full152 native headline/description strings, so their exact text comparison is the parent's reported result, not reproducible from this JSON alone.
- **Text assets:** eight explicit native sitelink rows match payload titles, both descriptions and URLs. Every group's four recorded IDs resolves to exactly its intended title set:32 associations total. Six explicit callout rows and their IDs match the payload. Eight snippet ID/text/group mappings match their headers and values. The earlier missing ID-to-title evidence gap is resolved.
- **Campaign negatives:** expected247=229Phrase+18Exact matches the payload and receipt's actual247, missing0, extra0. This is an internally consistent parent reconciliation; the JSON contains summary counts rather than all247 native tuples.
- **Group negatives:** expected64 rows are reported all present, but actual group rows total240 because176 obsolete rows remain. Group expected counts10/10/6/0/9/21/0/8 match the payload. All31 conditional routing rows remain in that64-row plan; conditional downstream eligibility is still a separate consideration before any later activation.
- **Cleanup manifest:** all176 obsolete IDs and all176 scoped keyword/match tuples are unique, with162Phrase+14Exact. Each is assigned to one of the exact eight target group IDs; none matches an intended negative tuple in that same group. Every group total equals expected+extras. Cleanup IDs are disjoint from the153 paused English positive IDs. No deletion has been performed.

| Target group | ID | Expected | Obsolete extras | Native total |
|---|---|---:|---:|---:|
| Sukienki dla mamy i córki | 1273236272902732 | 10 | 23 | 33 |
| Ubrania dla całej rodziny | 1261141645145937 | 10 | 39 | 49 |
| Koszule i koszulki rodzinne | 1274335784975901 | 6 | 31 | 37 |
| Piżamy dla mamy i córki | 1272136760775851 | 0 | 17 | 17 |
| Koszule dla taty i syna | 1276534808106671 | 9 | 25 | 34 |
| Stylizacje dla mamy i córki | 1275435295874062 | 21 | 25 | 46 |
| Stroje kąpielowe mama i córka | 1260042133390080 | 0 | 16 | 16 |
| Swetry i bluzy dla rodziny | 1275435295842174 | 8 | 0 | 8 |

**The manifest is locally coherent and target-scoped; “all group negatives complete” would be false while these176 extras remain.** The153 paused English positives are a separate retained set, not part of this negative-deletion manifest.

## Images and the wording difference

The translation file contains76 unique source IDs and152 translated text fields. All recorded lengths equal independently computed lengths; all fit the parent-observed35 display/90 alt limits (actual maxima35/55). This verifies text preparation, not native acceptance or visual truth.

Parent receipt reports76 original unique records/90 associations, three saved Polish copies,73 unique caption records unfinished and87 associations retaining English captions. Arithmetic is coherent:76−3=73 and90−3=87. Saved source IDs8864942534762,8864942551975,8864942551976 all exist in the translation file, with new IDs8864942648365/8366/8367. Parent says saved texts match their prepared translations; exact saved field strings and all90 association/media rows are not reproduced in the final JSON, so that observation cannot be independently replayed here.

Rejected image source**8864942551977**, media**1261139890752049**, returned native **“Adult content”** on Save. Receipt records the actual attempted display “Pasująca dzianina dla rodziny” and alt “Pasujące ubrania z dzianiny dla dorosłych i dzieci”; these differ from the later prepared “Pasujące dzianiny dla rodziny” / “Pasujące dzianiny dla dorosłego i dziecka.” Parent clarified the attempt preceded that file. This is an explained rejected-attempt difference, not a saved-copy mismatch. Preserve its actual wording and rejection; do not rewrite history to claim an exact payload attempt.

The blocked record was canceled, its original association retained, and further image submissions stopped. No rewording, appeal or alternate-write bypass is claimed. Native rejection does not establish that the underlying image actually contains prohibited content; it establishes that this Save was rejected.

Original media sets are reported retained for the affected groups, but **crop equality is not established**. For source8864942551975, the receipt explicitly records source crop roit0.2857/roib0.8483 versus Polish0.219/0.7816. It would be inaccurate to claim all images/crops were unchanged or image localization complete. Shared originals are reported unmodified.

## Remaining gates and claim limits

1. **Permanent deletion:** Computer Use requires action-time user confirmation for the exact176 obsolete target group-negative rows. Immediately before any authorized deletion, reread target/group/ID/text/match to detect drift. Retain all64 intended rows, including31 conditional rows, preserve source/peers/shared lists, and keep153 paused English positives outside that manifest unless separately authorized.
2. **Image policy and completion:** resolve the native rejection through the normal user/platform review path before resuming affected submissions. No bypass/rewording retry. Finish73 unique caption records only after the gate is resolved, preserving suitable original images; reconcile the reported sweater crop mismatch before claiming image parity.
3. **After-state proof:** after any approved cleanup or resumed image work, capture fresh settled native rows and compare exact tuples/asset associations. The parent used complete table pages with overlapping reads and reopened editors; browser download export was unavailable. **No native export artifact or independent live replay is claimed.** Expected native rows are partly summarized, so this verifier can certify manifest arithmetic and supplied asset fields, not every native expected row independently.
4. **Scope:** remain Paused. No activation, spend increase, measurement infrastructure change, sales, conversion attribution, or profitability claim follows from these configuration receipts. Applied suffix strings match the payload, but the final JSON alone is not a full effective tracking-hierarchy audit or checkout/purchase proof.

The next concrete approval is the176-row negative cleanup; the image-policy gate is independently unresolved. Neither permits activation.

## Reviewed file hashes

- `final_native_verification.json` SHA256: `fbf78b907391b5180323d2c3cbeac4d2253320e35a55cb33d69195e744925645`
- `negative_reconciliation_and_cleanup.json` SHA256: `29b2197b801c33fe82f07c083a00c27210d1b8af29dccc625543c2e6cc820f97`
- `payload/campaign_payload.json` SHA256: `f410411a0415c968d688bd1ffe78e258afeaa9ae169f5bbcc0d7062517393500`
- `payload/image_caption_translations.json` SHA256: `d444a6e9f84fac68ce8a56f55b8af9dcc3347bbb644a216ffd102d73b93106b6`
