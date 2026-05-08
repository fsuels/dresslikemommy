# Merchant Paid-Cohort Age Group Upload Recheck

Date: 2026-05-06  
Merchant Center account: `124884876`  
Supplemental source: `supplemental_feed_pilot.txt` / source URL `joinFeedId=10626787326`

## Scope

Owner approved the Merchant age-group supplemental upload for the current paid cohort only.

Important implementation guardrail: the existing supplemental source carries `custom_label_0..4`, including the active paid targeting labels `paid_eligible` and `us_test_ready`. Replacing it with the local 780-row `id,age_group` file would strip those labels. The safer upload preserved the full existing source shape and changed only current paid-cohort `age_group` values where the refreshed paid-cohort parser differed.

## Upload File

Uploaded file:

`upload_preserve_labels_paid_cohort_age_group_refresh.txt`

Rows:

- Upload rows: `5,933`
- Columns: `id`, `custom_label_0`, `custom_label_1`, `custom_label_2`, `custom_label_3`, `custom_label_4`, `age_group`
- Current paid cohort rows present: `780 / 780`
- Current paid cohort missing from current source: `0`
- Existing paid cohort rows with same age group before upload: `775`
- Effective paid-cohort age group changes: `5`
- Effective changes: all `kids -> adult` for `13-14 years` size rows

Guardrails verified locally:

- `custom_label_0..4` preserved byte-for-byte from the current full source.
- Only `age_group` differed, and only for current paid-cohort IDs.
- No Shopify product edits, feed-label edits, product-scope edits, campaign edits, budget edits, bid edits, or conversion-goal edits were made.

## Source Processing Readback

Merchant source detail readback after upload:

- Last updated: `May 6, 2026 3:26 PM`
- Total updated products: `5,933`
- Matched products: `5,771`
- Attribute names: `All recognized`
- Supplemental product data file: `1 issue found`
- Source issue: `Offer does not exist`
- Affected products: `162`

Downloaded source report:

`merchant-source-offer-does-not-exist-report.csv`

Source issue overlap check:

- Source issue rows downloaded: `162`
- Current paid cohort overlap: `0`
- All 162 stale rows are labeled `custom_label_0=exclude_feed_issue` and `custom_label_4=us_fix_before_paid`

Prepared but did not upload a stale-row cleanup file:

`upload_preserve_labels_age_group_minus_162_stale_nonpaid_PROPOSED_DO_NOT_UPLOAD.txt`

That proposed file removes the 162 non-paid stale offer rows, keeps `780 / 780` paid rows, and preserves the same columns. It was not uploaded because the owner approval was scoped to current paid-cohort age-group repair, not non-paid stale-row cleanup.

## Product Diagnostics Recheck

Merchant product diagnostics export after source processing:

`merchant-product-issues-filtered-download-product_issues_2026-05-06_15-37-13.csv`

Readback:

- Product issues export rows: `37,947`
- Total `Missing age group` issue rows in the filtered export: `16,758`
- Unique item IDs with `Missing age group`: `4,695`
- Current paid cohort size: `780`
- Current paid cohort item IDs still showing `Missing age group` anywhere in the export: `777`
- Current paid cohort US/en/United States item IDs still showing `Missing age group`: `758`
- Current paid cohort US/en `Missing age group` rows:
  - `758` Shopping ads rows
  - `758` Free listings rows

Sample paid product detail readback:

- Product ID: `shopify_US_7227254276193_41871113158753`
- Labels visible: `paid_eligible`, `margin_medium`, `swimsuits`, `aov_medium`, `us_test_ready`
- Product detail still showed `Needs attention (2)`
- Needs-attention tab still showed:
  - `Missing local inventory data`
  - `Missing age group`

## Interpretation

The upload was accepted by the supplemental source and the attribute names were recognized, but the paid-cohort product diagnostic has not cleared. At this point, the correct read is:

- Source upload: accepted/processed.
- Paid-label preservation: protected.
- Source issue: 162 stale non-paid excluded rows now visible; no paid overlap.
- Paid-cohort age-group diagnostic: not fixed yet in current Merchant product diagnostics.

This may still be a propagation delay, but it cannot be called fixed from the current live readback.

## Next Best Action

1. Recheck Merchant product diagnostics later after the next issue-refresh window.
2. If the same paid-cohort `Missing age group` rows remain, stop relying on this supplemental source for age-group repair and use a separately approved primary-feed path:
   - Shopify Google/YouTube app product attribute repair for the current paid cohort, or
   - a new dedicated Merchant supplemental source explicitly validated against product detail diagnostics.
3. Separately, if approved, upload the prepared stale-row cleanup file to clear the 162 non-paid `Offer does not exist` source issue.

