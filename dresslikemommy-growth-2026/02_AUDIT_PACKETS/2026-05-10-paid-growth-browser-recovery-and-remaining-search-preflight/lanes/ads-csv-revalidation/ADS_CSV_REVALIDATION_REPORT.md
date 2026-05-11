# Ads CSV Revalidation Report

Generated: 2026-05-10
Lane: `ads-csv-revalidation`
Scope: local/read-only revalidation of unresolved Google Ads split CSVs for `PL`, `CZ`, `RO`, `PT`, `GR`, `IT`, `FR`, `BE`.
External actions: none. No browser, Google Ads, Merchant, Shopify, Pinterest, or theme actions were performed.

## Sources Read

- Canonical prompt: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- Coordination row: `ops/AGENT_COORDINATION.md` row for `Paid-growth browser recovery + remaining non-US Search preflight`
- Prior playbook/report context:
  - `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/ads-apply-playbook/ADS_APPLY_PLAYBOOK_REPORT.md`
  - `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/ads-resume-order/ADS_RESUME_ORDER_REPORT.md`
  - `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/stale-blocker-checksum-sweep/STALE_BLOCKER_CHECKSUM_SWEEP.md`
- Source CSV manifest:
  - `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/SHA256SUMS.txt`
  - `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/`

## Commands Run

```sh
pwd && rg --files | rg '(^ops/|2026-05-10|SHA256SUMS|split|csv|GOOGLE_ADS|paid-growth)'
rg -n "TEST BUILD|PL|CZ|RO|PT|GR|IT|FR|BE|non-US|split|SHA256|Vacation Family|beach" ops/prompts/paid-growth-ai-army-continuation-prompt.md ops/AGENT_COORDINATION.md ops/AGENT_WORKLOG.md dresslikemommy-growth-2026/02_AUDIT_PACKETS -g '*.md'
find dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight -type f | sort
find dresslikemommy-growth-2026/02_AUDIT_PACKETS -type f \( -iname '*split*.csv' -o -iname '*bulk*.csv' -o -name 'SHA256SUMS*' \) | rg '2026-05-(08|09|10)|non-us|ads|intl|held'
sed -n '1,220p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/ads-apply-playbook/ADS_APPLY_PLAYBOOK_REPORT.md
sed -n '1,180p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/SHA256SUMS.txt
sed -n '1,8p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/PL_intl_search_paused_draft_web_bulk.csv
find dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest -maxdepth 2 -type f | sort
sed -n '1,220p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/ads-resume-order/ADS_RESUME_ORDER_REPORT.md
sed -n '1,180p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/stale-blocker-checksum-sweep/STALE_BLOCKER_CHECKSUM_SWEEP.md
python3 - <<'PY'
# Parsed the 8 CSVs with csv.DictReader, computed SHA-256, checked row types,
# paused statuses, budgets, max CPCs, campaign language/location/network,
# RO/PT final URL prefixes, and forbidden text/handle hits.
PY
rg -n "ads-csv-revalidation|browser-recovery|remaining-search|NON-US-SEARCH|PL|CZ|RO|PT|GR|IT|FR|BE" ops/AGENT_COORDINATION.md ops/prompts/paid-growth-ai-army-continuation-prompt.md | sed -n '1,160p'
```

## Pass/Fail Table

Expected per file:

- `88` data rows: `1 Campaign + 10 Ad group + 30 Keyword + 37 Negative keyword + 10 Ad`
- All mutable entity statuses paused: `51/51` (`Campaign`, `Ad group`, `Keyword`, `Ad` rows)
- Campaign `Action = Add`, `Budget = 1.00`, `Language = en`, `Networks = Google search`, `Bid strategy type = Manual CPC`
- Max CPC: `0.10` for `PL`, `CZ`, `RO`, `PT`, `GR`; `0.12` for `IT`, `FR`, `BE`
- SHA-256 must match `SHA256SUMS.txt`
- No `Vacation Family` or bad beach handle rows

| Country | Rows | Row Types | Paused Statuses | Budget | Max CPC | Location | RO/PT URL Prefix | SHA Match | Bad Beach/Vacation Rows | Verdict |
|---|---:|---|---|---:|---:|---|---|---|---|---|
| PL | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.10 | Poland | n/a | yes | 0 | PASS |
| CZ | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.10 | Czechia | n/a | yes | 0 | PASS |
| RO | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.10 | Romania | yes, `/ro/products/` plus `country=RO` | yes | 0 | PASS |
| PT | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.10 | Portugal | yes, `/pt/products/` plus `country=PT` | yes | 0 | PASS |
| GR | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.10 | Greece | n/a | yes | 0 | PASS |
| IT | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.12 | Italy | n/a | yes | 0 | PASS |
| FR | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.12 | France | n/a | yes | 0 | PASS |
| BE | 88 | 1/10/30/37/10 | 51/51 | 1.00 | 0.12 | Belgium | n/a | yes | 0 | PASS |

## Hash Readback

| Country | SHA-256 |
|---|---|
| PL | `3ce7a8df5fc7a5e8c248d2441c57154d8e9e1aee575a6dd826a76906bb00bd76` |
| CZ | `a2e20892564494d10aacf42792be1310df55c473054be456ab16cefa1fd05b55` |
| RO | `b3e9eac7c59d06813c3c2b7089c4d46d21c6e92f0d0c5459eab71b5c73a43001` |
| PT | `5a02a1cff436d7de6444b3462c8017c37742a87bb0fb85f2a0a071e08cdb47a7` |
| GR | `48c88f4b5f2e9fb44b85e5bb27eb79539707075a7ba622ef530d9cb1a9b2fc8f` |
| IT | `adfbf9aedd13ec2d92c2a57737672e476332328b00cb2ce2a01dc71c30597377` |
| FR | `02025e1c1c2cfb42abac7f5138b773b0843afcfc28bcfda0ef0d289b371f5aa8` |
| BE | `273fb256f44b084520f2d8bc1bdfddafa26b0a823b62282371719bf79003327d` |

All 8 computed hashes match the recorded values in `SHA256SUMS.txt`.

## Drift

No local CSV drift detected.

- File presence: all 8 unresolved split CSVs present.
- File contents: byte-identical to `SHA256SUMS.txt`.
- Row structure: identical expected `88` data rows per country.
- Statuses: all mutable entity rows remain `Paused`; negative keyword rows have blank status as expected.
- Budgets/CPCs: all remain within playbook values and below the `0.20` approval cap.
- URL guard: `RO` and `PT` use localized, country-qualified product URLs.
- Bad landing guard: no `Vacation Family` or `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` rows found.
- External-surface guard: no checked rows contained protected bad-surface strings such as `PMax`, `Performance Max`, `Standard Shopping`, `Merchant feed`, `product scope`, `feed label`, `product group`, or `conversion goal`.

## Next Action

Local CSV preflight is clear. The next browser-enabled parent/operator can resume the approved paused-build lane one country at a time in the playbook order:

`PL -> CZ -> RO -> PT -> GR -> IT -> FR -> BE`

Do not start any upload while the prior `IT` preview is still in progress. For every country, require a fresh Google Ads preview of `88 changes / 88 success / 0 errors`, then apply only if clean, then perform campaign/network/location readbacks before moving to the next country.
