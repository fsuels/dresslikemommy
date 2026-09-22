# Danish shirt-filter repair — phase 3

Confidence: H for the reproduced source defect and actual-script regression. Browser preview of these candidate bytes is NOT RUN by this worker.

Status: PASS_LOCAL_SOURCE_AND_ACTUAL_SCRIPT_REGRESSIONS. Candidate frozen for independent parent review. No external writes, inventory changes, collection-membership changes, routing-target changes, ad-negative changes, Git writes or shared-canonical edits. Earlier packets unchanged.

The parent captured 23 cards in the Danish/Denmark draft preview of `daddy-me-shirts`, all hidden. The exact title fixture is `../danish_shirt_browser_titles.json`. Fresh script `assets/daddy-me-collection-filter.js` accepted English shirt/shirts only and overwrote count text in English. The actual original script executed in the VM reproduces zero visible cards and `0 products` from those 23 titles.

Two candidate upload files:

- `assets/daddy-me-collection-filter.js`: detects Danish using the page language root; Danish title matching additionally recognizes `skjorte`, `skjorter`, `skjortesæt` and compounds such as `bomuldsskjorter`/`hawaiiskjorter`. Existing English shirt matching and all tee exclusions are preserved. For Danish only, the script writes `0 produkter`, `1 produkt` or plural `produkter`; all other locales retain their previous count output.
- `locales/da.json`: exact restoration of Phase 1 bytes, removing the two speculative zero keys that rendered testing disproved as a fix. All 38 successful Phase 1 Danish corrections remain. Final MD5 is `90962b170b6ae87a2bf69a1ac0a0060f`.

| File | Current before MD5 | Candidate MD5 |
| --- | --- | --- |
| assets/daddy-me-collection-filter.js | 45a6e48cda28fc815c3d1b54a0a82a4a | 9b6784bb391206159520b196c4ef4788 |
| locales/da.json | 3ad0181cb1165661d4841d350b9dbf30 | 90962b170b6ae87a2bf69a1ac0a0060f |

Source bindings: fresh `theme_daddy_filter_before.json` for JavaScript; successful `theme_followup_execution.json` and exact Phase 2 candidate bytes for current da locale. Full SHA256 hashes: `MANIFEST.json`, manifest SHA256 `3fee424a43bf82c9ea1560b785d398d3ba14a35d29268108e15c01597f3a35ae`. Composite final 13-file source list: `COMBINED_13_FILE_MANIFEST.json`; this is a local composite, not a fresh full-theme remote binding.

Checks actually run:

- Bundled Node `--check` on candidate JavaScript: PASS.
- Bundled Node `--test --test-reporter=tap regression.test.mjs`: **10 passed, 0 failed**. Stored output: `regression.tap`.
- Tests execute the complete actual IIFE through `node:vm` with a bounded DOM stub; no rewritten classifier stand-in. Exact observed cohort: baseline 0 visible/0 products; candidate 23 visible/23 produkter. Six tee-negative cases remain excluded, including mixed Danish-shirt/English-tee text. Counts 0/1/2/23 pass on both desktop/mobile count elements. Danish language/case variants pass.
- English/non-Danish output snapshots match baseline across seven language values, four collection handles and three filter states (84 small comparisons), including the Danish title fixture under non-Danish language. Existing parent navigation/query values, tee inverse behavior and no-op cases pass.
- Original observer implementation/options are byte-identical. Repeated observer/popstate callbacks are idempotent in the stub. This does not certify every live DOM mutation-loop scenario; no observer redesign was introduced.
- Hashes, exact Phase 1 locale restoration, all unrelated JavaScript source bytes and all 13 composite candidate hashes verified. Whitespace check produced zero diagnostics.

Limitations and next action:

The fix makes a title-based UI filter understand the observed Danish terms. It does not certify inventory, market availability, product facts or target qualification. The 23 fixture titles are evidence inputs only. Parent must obtain independent review, stage only the two exact files to the authorized unpublished theme, read back MD5s and verify Danish desktop/narrow shirt, tee and parent-filter views with stable counts. Only rendered destination evidence can supersede the earlier empty-view observation; preserve narrower routing negatives and all other unresolved eligibility limits.

Continuation prompt: Independently review the frozen two-file Danish filter repair and passing actual-script regressions, stage the exact manifest when authorized, verify MD5s and desktop/mobile preview, then renew the cumulative 13-file source binding and record what the destination readback establishes without inventory or qualification inference.
