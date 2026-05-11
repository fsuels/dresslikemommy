# Remaining Split CSV Guardrail Validation

Generated: 2026-05-10
Lane: `remaining-split-csv-guardrail-validation`
Scope: local/read-only validation of unresolved Google Ads split CSVs for `CZ`, `RO`, `PT`, `GR`, `FR`, and `BE`.

No external systems, browser tabs, Google Ads, Shopify Admin, Merchant Center, Pinterest, credentials, live theme files, or live product/feed/campaign surfaces were touched.

## Verdict

`PASS` for all six unresolved split CSVs.

Each target file matches the current split manifest, contains exactly `88` data rows, uses only the expected row types, keeps all mutable entities paused, has max CPC at or below `$0.20`, excludes completed countries, excludes US campaign `23827590655`, excludes PMax/Standard Shopping/Merchant/feed/conversion/product-scope/product-group references, and has zero `Vacation Family` / bad beach-handle rows.

## Files Read

- `ops/MEMORY_CONTINUITY_PROTOCOL.md`
- `ops/AGENT_WORKLOG.md`
- `ops/AGENT_COORDINATION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/ads-csv-revalidation/ADS_CSV_REVALIDATION_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/GOOGLE_ADS_SPLIT_IMPORT_CONTROL_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/manifest.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/campaign_row_counts.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/SHA256SUMS.txt`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/CZ_intl_search_paused_draft_web_bulk.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/RO_intl_search_paused_draft_web_bulk.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/PT_intl_search_paused_draft_web_bulk.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/GR_intl_search_paused_draft_web_bulk.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/FR_intl_search_paused_draft_web_bulk.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/BE_intl_search_paused_draft_web_bulk.csv`

## Commands Run

```sh
pwd && rg --files -g 'AGENTS.md' -g 'ops/MEMORY_CONTINUITY_PROTOCOL.md' -g 'ops/AGENT_WORKLOG.md' -g 'ops/AGENT_COORDINATION.md' -g 'ops/GOOGLE_ADS_CONTINUITY.md' -g 'ops/GROWTH_NORTH_STAR.md' -g 'ops/prompts/paid-growth-ai-army-continuation-prompt.md'
find dresslikemommy-growth-2026/02_AUDIT_PACKETS -maxdepth 2 -type d | sort | tail -60
sed -n '1,220p' ops/MEMORY_CONTINUITY_PROTOCOL.md
tail -220 ops/AGENT_WORKLOG.md
sed -n '1,220p' ops/AGENT_COORDINATION.md
find dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight -type f \( -name '*.csv' -o -name '*manifest*' -o -name '*.json' -o -name '*.md' \) | sort
find dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest -maxdepth 2 -type f | sort
sed -n '1,220p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/ads-csv-revalidation/ADS_CSV_REVALIDATION_REPORT.md
find dresslikemommy-growth-2026/02_AUDIT_PACKETS -path '*google-ads-split-manifest*' -type f \( -name '*.csv' -o -name '*.json' -o -name '*.txt' -o -name '*.md' \) | sort
sed -n '1,220p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/GOOGLE_ADS_SPLIT_IMPORT_CONTROL_REPORT.md
sed -n '1,80p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/campaign_row_counts.csv
sed -n '1,120p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/SHA256SUMS.txt
python3 -m json.tool dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/manifest.json | sed -n '1,260p'
python3 - <<'PY'
# Read CZ header/sample rows with csv.reader.
PY
python3 - <<'PY'
# Parsed CZ/RO/PT/GR/FR/BE with csv.DictReader, computed SHA-256,
# compared each file against manifest.json, and checked guardrails.
PY
mkdir -p dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/remaining-split-csv-guardrail-validation
```

Note: one initial broad `rg` search across historical paid-media files was stopped/truncated after producing noisy unrelated output; it did not write files or touch external systems.

## Validation Table

Expected per target file: `88` data rows = `1 Campaign + 10 Ad group + 30 Keyword + 37 Negative keyword + 10 Ad`; `51/51` mutable entity rows paused; `40` final URL rows; `Action=Add`; blank Campaign/Ad group/Keyword/Ad IDs; Search-only campaign row; Google Search network only; Manual CPC; `Language=en`; daily budget `1.00`.

| Country | Rows | Row Types | Paused | Budget | Max CPC | Location | Final URL Rows | SHA Match | Forbidden Hits | Verdict |
|---|---:|---|---:|---:|---:|---|---:|---|---:|---|
| CZ | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.10 | Czechia | 40 | yes | 0 | PASS |
| RO | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.10 | Romania | 40 | yes | 0 | PASS |
| PT | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.10 | Portugal | 40 | yes | 0 | PASS |
| GR | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.10 | Greece | 40 | yes | 0 | PASS |
| FR | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.12 | France | 40 | yes | 0 | PASS |
| BE | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.12 | Belgium | 40 | yes | 0 | PASS |

## Hashes

| Country | SHA-256 |
|---|---|
| CZ | `a2e20892564494d10aacf42792be1310df55c473054be456ab16cefa1fd05b55` |
| RO | `b3e9eac7c59d06813c3c2b7089c4d46d21c6e92f0d0c5459eab71b5c73a43001` |
| PT | `5a02a1cff436d7de6444b3462c8017c37742a87bb0fb85f2a0a071e08cdb47a7` |
| GR | `48c88f4b5f2e9fb44b85e5bb27eb79539707075a7ba622ef530d9cb1a9b2fc8f` |
| FR | `02025e1c1c2cfb42abac7f5138b773b0843afcfc28bcfda0ef0d289b371f5aa8` |
| BE | `273fb256f44b084520f2d8bc1bdfddafa26b0a823b62282371719bf79003327d` |

All six computed hashes match `manifest.json`, `campaign_row_counts.csv`, and `SHA256SUMS.txt`.

## Guardrail Checks

- Completed countries absent: no `DLM_GB_`, `DLM_CA_`, `DLM_AU_`, `DLM_CH_`, `DLM_DK_`, `DLM_DE_`, `DLM_NL_`, `DLM_SE_`, `DLM_ES_`, `DLM_IT_`, `DLM_PL_`, or completed-country `country=` URL parameters appeared in the six target CSVs.
- US campaign absent: no `23827590655` or `DLM_US_` references.
- Campaign surface clean: no `PMax`, `Performance Max`, `Standard Shopping`, `Shopping ads`, Merchant, feed-label, product-scope, product-group, or conversion-goal references.
- Bad landing guard clean: no `Vacation Family`, `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`, or product ID `7227378892897` hits.
- URL country qualification clean: every populated `Final URL` contains the target file's own `country=<code>` parameter.
- Import safety structure clean: all rows are `Action=Add`; entity ID columns are blank; row types are only `Campaign`, `Ad group`, `Keyword`, `Negative keyword`, and `Ad`.

## Residual Notes

This is local CSV evidence only. It does not prove Google Ads preview/apply state, location presence settings, or account-side absence/readback. Parent should still continue one country at a time in the current order: `CZ` -> `RO` -> `PT` -> `GR`, then `FR` only after fresh non-stale preview/no-duplicate readback, and `BE` last after upload-throttle cooldown.
