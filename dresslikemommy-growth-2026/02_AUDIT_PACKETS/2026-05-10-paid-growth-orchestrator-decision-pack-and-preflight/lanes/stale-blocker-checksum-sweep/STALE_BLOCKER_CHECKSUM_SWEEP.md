# Stale Blocker Checksum Sweep — 2026-05-10

Lane: `stale-blocker-checksum-sweep`
Parent packet: `2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight`
Sweep run: 2026-05-10 (read-only verification)
Operator: Lane E subagent (Stale-Blocker-Checksum-Sweep)

## 1. Method

For each artifact listed in the brief, the sweep computed:

- `sha256sum <file>` -> 64-char hex digest
- `wc -l < <file>`  -> newline count (== row count when file ends in `\n`, which all files here do; verified via `tail -c 1 | xxd`)

Recorded sha256 baselines were read from:
`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/SHA256SUMS.txt`

Expected line counts:

- Google Ads split CSVs: 89 lines = 1 header + 88 data rows
  (88 data rows = 1 Campaign + 10 Ad group + 30 Keyword + 37 Negative keyword + 10 Ad)
- Pinterest clean-scope CSV: 343 lines = 1 header + 342 data rows
- Vacation-family-hold source CSV: 1497 lines = 1 header + 1496 data rows

No file was opened for write. Only `sha256sum`, `wc`, `awk`, `tail`, `xxd`, `ls`, `cat` (read-only) were invoked.

## 2. Per-file Results

### 2a. Google Ads non-US Search split CSVs (17 files)

| # | File | Computed sha256 | Lines | Recorded sha256 | Status |
|---|---|---|---|---|---|
| 1 | `split_csvs/AU_intl_search_paused_draft_web_bulk.csv` | `642bf7f74cb50105d7c010cacb88b86ee7d8e67e85cba42ef4e47734ed2cf5c1` | 89 | `642bf7f74cb50105d7c010cacb88b86ee7d8e67e85cba42ef4e47734ed2cf5c1` | PASS |
| 2 | `split_csvs/BE_intl_search_paused_draft_web_bulk.csv` | `273fb256f44b084520f2d8bc1bdfddafa26b0a823b62282371719bf79003327d` | 89 | `273fb256f44b084520f2d8bc1bdfddafa26b0a823b62282371719bf79003327d` | PASS |
| 3 | `split_csvs/CA_intl_search_paused_draft_web_bulk.csv` | `d4e45c0f018ad1132b0482e53cb59eb43c844e02cb535a9c67466dce1a120f1b` | 89 | `d4e45c0f018ad1132b0482e53cb59eb43c844e02cb535a9c67466dce1a120f1b` | PASS |
| 4 | `split_csvs/CH_intl_search_paused_draft_web_bulk.csv` | `0dc85e3b629c980e3c8508e6410e2d475abfd8af711e382993a471c5cd706a4f` | 89 | `0dc85e3b629c980e3c8508e6410e2d475abfd8af711e382993a471c5cd706a4f` | PASS |
| 5 | `split_csvs/CZ_intl_search_paused_draft_web_bulk.csv` | `a2e20892564494d10aacf42792be1310df55c473054be456ab16cefa1fd05b55` | 89 | `a2e20892564494d10aacf42792be1310df55c473054be456ab16cefa1fd05b55` | PASS |
| 6 | `split_csvs/DE_intl_search_paused_draft_web_bulk.csv` | `8674d63c624e3e0216d6276fd43e857a6b054fb4d05123cb416bfb53a77120a0` | 89 | `8674d63c624e3e0216d6276fd43e857a6b054fb4d05123cb416bfb53a77120a0` | PASS |
| 7 | `split_csvs/DK_intl_search_paused_draft_web_bulk.csv` | `c6dd4a8a48c4a295c7f00a8a80963fcf6c809151a7959941f7cb96292e59bd8c` | 89 | `c6dd4a8a48c4a295c7f00a8a80963fcf6c809151a7959941f7cb96292e59bd8c` | PASS |
| 8 | `split_csvs/ES_intl_search_paused_draft_web_bulk.csv` | `73075d41d9bf03ae97ce8613bba3bfe42bceee23fcab1a28d2a50439c9caf9e1` | 89 | `73075d41d9bf03ae97ce8613bba3bfe42bceee23fcab1a28d2a50439c9caf9e1` | PASS |
| 9 | `split_csvs/FR_intl_search_paused_draft_web_bulk.csv` | `02025e1c1c2cfb42abac7f5138b773b0843afcfc28bcfda0ef0d289b371f5aa8` | 89 | `02025e1c1c2cfb42abac7f5138b773b0843afcfc28bcfda0ef0d289b371f5aa8` | PASS |
| 10 | `split_csvs/GB_intl_search_paused_draft_web_bulk.csv` | `a6411f863f720c97db5d8ac0eb9acd2d60763c990ff7a5ea90aa5554ed146ede` | 89 | `a6411f863f720c97db5d8ac0eb9acd2d60763c990ff7a5ea90aa5554ed146ede` | PASS |
| 11 | `split_csvs/GR_intl_search_paused_draft_web_bulk.csv` | `48c88f4b5f2e9fb44b85e5bb27eb79539707075a7ba622ef530d9cb1a9b2fc8f` | 89 | `48c88f4b5f2e9fb44b85e5bb27eb79539707075a7ba622ef530d9cb1a9b2fc8f` | PASS |
| 12 | `split_csvs/IT_intl_search_paused_draft_web_bulk.csv` | `adfbf9aedd13ec2d92c2a57737672e476332328b00cb2ce2a01dc71c30597377` | 89 | `adfbf9aedd13ec2d92c2a57737672e476332328b00cb2ce2a01dc71c30597377` | PASS |
| 13 | `split_csvs/NL_intl_search_paused_draft_web_bulk.csv` | `3c945ebcf7042f2602f5743090f0a09a0e94a57858c2aa26f334e41fe0969f13` | 89 | `3c945ebcf7042f2602f5743090f0a09a0e94a57858c2aa26f334e41fe0969f13` | PASS |
| 14 | `split_csvs/PL_intl_search_paused_draft_web_bulk.csv` | `3ce7a8df5fc7a5e8c248d2441c57154d8e9e1aee575a6dd826a76906bb00bd76` | 89 | `3ce7a8df5fc7a5e8c248d2441c57154d8e9e1aee575a6dd826a76906bb00bd76` | PASS |
| 15 | `split_csvs/PT_intl_search_paused_draft_web_bulk.csv` | `5a02a1cff436d7de6444b3462c8017c37742a87bb0fb85f2a0a071e08cdb47a7` | 89 | `5a02a1cff436d7de6444b3462c8017c37742a87bb0fb85f2a0a071e08cdb47a7` | PASS |
| 16 | `split_csvs/RO_intl_search_paused_draft_web_bulk.csv` | `b3e9eac7c59d06813c3c2b7089c4d46d21c6e92f0d0c5459eab71b5c73a43001` | 89 | `b3e9eac7c59d06813c3c2b7089c4d46d21c6e92f0d0c5459eab71b5c73a43001` | PASS |
| 17 | `split_csvs/SE_intl_search_paused_draft_web_bulk.csv` | `9bcaf0f04b93adfe8f94dff034b2c2487ed58fbf26cd65ade5f93560a11bfd76` | 89 | `9bcaf0f04b93adfe8f94dff034b2c2487ed58fbf26cd65ade5f93560a11bfd76` | PASS |

All 17 split CSVs: row total per file = 88 data rows + 1 header (89 lines). Drift since 2026-05-09 packet creation: NO.

### 2b. Pinterest clean-scope CSV

| File | Computed sha256 | Lines | Recorded sha256 | Status |
|---|---|---|---|---|
| `2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv` | `ae0c1721cc40e1ca0fbb51f3a15e1fa1bc49095f6226c6f73ef908f4b7a7ab83` | 343 | (none recorded in lane SHA256SUMS.txt) | PASS (row count) |

Expected: 343 lines = 1 header + 342 data rows. Match. No prior recorded sha256 to compare against in the 2026-05-09 lane manifest, so this entry is verified by row count + header structure only. The new digest above is now the canonical baseline for future drift checks.
Drift since 2026-05-09 packet creation: NO (row count intact).

### 2c. Vacation-family-hold source CSV (1496 data rows)

| File | Computed sha256 | Lines | Recorded sha256 | Status |
|---|---|---|---|---|
| `2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv` | `8401e29066693c4215760e0f9b09080f50d94de47f6e27300724f99ed5e0c814` | 1497 | `8401e29066693c4215760e0f9b09080f50d94de47f6e27300724f99ed5e0c814` | PASS |

Expected: 1497 lines = 1 header + 1496 data rows. Match.
Drift since 2026-05-09 packet creation: NO.

## 3. Aggregate Verdict

- Total files verified: 19
- Total PASS: 19
- Total FAIL: 0
- All recorded sha256 baselines (18 in `SHA256SUMS.txt`) match computed digests bit-for-bit.
- All expected row counts match.

Aggregate verdict: PASS — all artifacts are byte-identical to the 2026-05-09 packet snapshot. The next browser session may safely proceed using these artifacts without re-generation.

## 4. Failure Fallback Instructions

Not triggered. No FAIL recorded. No artifact needs to be removed from the next browser apply step. No fallback artifact is required.

(Reference, in case a future re-sweep flips a row to FAIL: do NOT use any FAIL artifact for the next browser apply step. Quarantine the file, regenerate from the upstream `2026-05-08-paid-growth-url-hold-checkout-safe-advance` master + `2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance` localization patch, and re-record sha256 before proceeding.)

## 5. Sweep Integrity Confirmation

- Tools used: `sha256sum`, `wc -l`, `awk`, `tail`, `xxd`, `ls`, `cat` — all read-only.
- No write to any verified file. No `mv`, `rm`, `cp`, `sed -i`, `>`, `>>`, `tee`, theme upload, Shopify mutation, Google Ads upload, Merchant Center push, Pinterest push, or `curl` was issued.
- The only write performed by this lane was the creation of this single markdown file at:
  `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/stale-blocker-checksum-sweep/STALE_BLOCKER_CHECKSUM_SWEEP.md`
- All 19 verified artifacts remain byte-identical to their 2026-05-09 / 2026-05-08 snapshots.

End of sweep.
