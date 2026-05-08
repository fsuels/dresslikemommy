# Merchant Source Refresh Approved Action

Date: 2026-05-08
Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-08-merchant-source-refresh-approved-action`

## Decision

`MERCHANT_AGE_GROUP_SOURCE_PROPAGATION_MOVED_VISIBLE_SAMPLE_CLEARED`

The owner approved the exact Merchant source-refresh action gate by reference to
`MERCHANT_SOURCE_REFRESH_SOLUTION_LADDER.md`.

Just-in-time readback found that the Merchant source had already moved, so no
additional refresh/sync/update click was made. Re-clicking would have been a
duplicate source action while another Merchant workstream was active.

## What Changed In Merchant

Fresh live Merchant readback showed a new/existing dedicated supplemental source:

- Source page: `upload_paid_cohort_age_group_only.txt details`
- Merchant source ID: `10651516446`
- Type: `File (manual)`
- Feed label: `US`
- Last updated: `May 8, 2026 1:55 AM`
- Total updated products: `780`
- Matched products: `771`
- Attribute names: `All recognized`
- File issue: `Offer does not exist`
- Affected products: `9`

The US/en `Shopify App API` product-list sample also advanced:

- Sample item: `shopify_US_7227254276193_41871113158753`
- Source: `10627623003` / `Shopify App API`
- Prior stale timestamp: `2026-05-07T14:14:02+00:00`
- Fresh timestamp: `2026-05-08T05:55:06+00:00`
- Labels intact: `custom_label_0=paid_eligible`, `custom_label_4=us_test_ready`

## Diagnostics Readback

Fresh diagnostics page/network readbacks showed:

- Visible diagnostics updated at `1:58 AM May 8, 2026` and later `2:04 AM May 8, 2026`.
- The visible prioritized diagnostics table no longer showed `Missing age group`.
- The sample item row no longer listed `Missing age group`; it listed only `Missing local inventory data`.
- `Missing local inventory data` remains a separate local-inventory-program issue, not a product-data fix for this dropshipping business.
- Account-level `TopItemIssueService` still returned a `Missing age group` bucket, but with no visible prioritized-row exposure in the captured page and no sample-row age_group issue. Exact CSV download remained unreliable.

## Action Taken

No additional Merchant source button was clicked in this pass.

Reason:

- The source update had already landed before the approved action could safely click.
- The source/detail readback showed the age_group-only file processed `780` rows and matched `771`.
- The target sample timestamp advanced beyond the Shopify repair timestamp.
- The target sample's visible diagnostics no longer contained `Missing age group`.
- Another Merchant write lane for local-inventory add-on removal was active in coordination, so adding a duplicate source update click was not the smallest effective action.

## Evidence

- `pre-action-merchant-browser-rpc-sample/merchant_exact_label_readback_refresh_check.json`
- `pre-action-live-tabs/`
- `source-detail-processing-readback/source_detail.txt`
- `source-detail-processing-readback/source_detail.png`
- `diagnostics-network-capture/diagnostics_text.txt`
- `diagnostics-network-capture/body_010.txt`
- `diagnostics-age-group-table-filter-capture/diagnostics_age_group_table_filter_text.txt`
- `readback-after-timestamp-advance/browser-source-readback/merchant_exact_label_readback_refresh_check.json`
- `readback-after-timestamp-advance/product-issues-browser-export/download_attempt_summary.json`

## Guardrails Preserved

- No additional Merchant upload.
- No source refresh/sync/update click.
- No Google & YouTube publication toggle.
- No Shopify product edits.
- No local inventory feeds or physical-store inventory claims.
- No Google Ads, Pinterest, GA4, campaign, budget, bid, status, product-scope, product-group, feed-label, or conversion-goal changes.

## Remaining Risk

The exact paid-cohort product-issues CSV did not download in this run. The
strongest current evidence is source-processing readback plus sample/product-list
and visible diagnostics readback. A later exact export should confirm whether
the former `623` paid-cohort US/en count is now `0`.

## Next Best Action

Do not repeat age_group product edits or source-update clicks immediately. Let
Merchant processing settle, then run a read-only exact product-issues export/API
readback. If the exact paid-cohort count is still non-zero, use the `9` unmatched
source rows as the next narrow investigation surface instead of editing the full
cohort again.
