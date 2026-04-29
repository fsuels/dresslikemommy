# Merchant Age Group + Stale Offer Fix

Use `upload_matched_age_group_with_paid_status.txt` for Merchant Center source `10626787326` / `supplemental_feed_pilot.txt`.

This file intentionally:
- keeps only the `5,933` offers that matched in the latest Merchant Center processing report;
- excludes the `1,391` rows reported as `Offer does not exist`;
- preserves `custom_label_4` paid-status values for matched offers;
- adds valid Google `age_group` values.

Rollback file: `rollback_paid_status_only_custom_label_4.csv`.

Do not upload older full-row age-group drafts from this folder if present; they include stale offer IDs.
