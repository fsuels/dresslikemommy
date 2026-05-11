# CSV Guardrail Revalidation

Status: `PASS_LOCAL_READ_ONLY`

Scope: local/read-only validation of unresolved Google Ads split CSV artifacts for `RO`, `PT`, `GR`, `FR`, and `BE`. No browser/account access, no external writes, and no files edited outside this lane report.

## Evidence Inputs

- Prior split manifest: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/manifest.json`
- Prior row-count manifest: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/campaign_row_counts.csv`
- Prior checksum manifest: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/SHA256SUMS.txt`
- Current handoff context: `ops/PROBLEM_TRACKER.md` and `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-cz-ro-pt-gr-paused-search-build/PAID_GROWTH_CZ_RO_PT_GR_PAUSED_SEARCH_BUILD_REPORT.md`

## Result

All five target source split CSVs still match the prior manifest checksums and pass the current local guardrails:

| Country | Campaign | Rows | Row Shape | Final URL Rows | Max CPC | SHA Match | Guardrail Result |
|---|---|---:|---|---:|---:|---|---|
| `RO` | `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 campaign, 10 ad groups, 30 keywords, 37 negatives, 10 ads | 40 country-qualified | `$0.10` | yes | pass |
| `PT` | `DLM_PT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 campaign, 10 ad groups, 30 keywords, 37 negatives, 10 ads | 40 country-qualified | `$0.10` | yes | pass |
| `GR` | `DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 campaign, 10 ad groups, 30 keywords, 37 negatives, 10 ads | 40 country-qualified | `$0.10` | yes | pass |
| `FR` | `DLM_FR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 campaign, 10 ad groups, 30 keywords, 37 negatives, 10 ads | 40 country-qualified | `$0.12` | yes | pass |
| `BE` | `DLM_BE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 campaign, 10 ad groups, 30 keywords, 37 negatives, 10 ads | 40 country-qualified | `$0.12` | yes | pass |

Checks performed:

- `Action=Add` only.
- Campaign/ad group/keyword/ad ID fields are blank.
- Campaign, ad group, keyword, negative keyword, and ad statuses are `Paused` where importable.
- Default max CPC values are at or below `$0.20`.
- Each file contains exactly one campaign and that campaign matches its country code.
- No completed-country campaign names were found for `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, or `CZ`.
- No duplicate campaign names appeared across the validated set.
- No forbidden hits found for US campaign references, `23827590655`, `23802638621`, `DLM_US_`, PMax/Performance Max, Standard Shopping, Merchant/feed/product-group/product-scope/conversion terms, the stale beach handle, product `7227378892897`, `Vacation Family`, `Christmas`, or `Xmas`.

## Blockers And Limits

- This lane did not use browser/account access, so it did not recheck the live Google Ads upload page or live campaign state.
- Per local handoff artifacts, the next Ads operator still needs to recheck the existing `RO` preview before any new upload. If clean, validate/download/apply/read back `RO`; if stale/in-progress/errors/throttle, park it and do not stack `PT`/`GR`.
- `PT` and `GR` remain source-CSV-ready locally, but should wait until `RO` is resolved or parked.
- `FR` source CSV is clean locally, but live work remains blocked by the prior stale/no-change preview/apply history; it needs a fresh non-stale `88/88 # OK` preview and no-duplicate readback.
- `BE` source CSV is clean locally, but live work remains blocked by the prior Google Ads upload-throttle cooldown.
- No non-US campaign enablement is cleared by this report; the purchase-event currency measurement gate remains separate.

## Commands Run

- `sed -n '1,220p' AGENTS.md`
- `sed -n '1,220p' ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `sed -n '1,260p' ops/PROBLEM_TRACKER.md`
- `rg --files dresslikemommy-growth-2026/02_AUDIT_PACKETS ...`
- `sed -n '1,220p' .../GOOGLE_ADS_SPLIT_IMPORT_CONTROL_REPORT.md`
- `sed -n '1,220p' .../manifest.json`
- `sed -n '1,80p' .../campaign_row_counts.csv`
- `sed -n '1,120p' .../SHA256SUMS.txt`
- `sed -n '1,220p' .../working/local_preflight_validation.json`
- `sed -n '1,8p' .../split_csvs/RO_intl_search_paused_draft_web_bulk.csv`
- `sed -n '1,220p' .../PAID_GROWTH_CZ_RO_PT_GR_PAUSED_SEARCH_BUILD_REPORT.md`
- `sed -n '1,180p' .../raw/ro-preview-timeout/ro_preview_extended_poll.json`
- `sed -n '1,220p' .../GOOGLE_ADS_NON_US_SEARCH_PAUSED_TEST_BUILD_APPROVED_PARTIAL_REPORT.md`
- `python3 - <<'PY' ...` using `csv`, `hashlib`, `json`, and regex checks
- `mkdir -p dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/lanes/csv-guardrail-revalidation`
