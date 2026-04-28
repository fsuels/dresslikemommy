# Approved Actions

This file tracks actions approved for execution. Local analysis and file organization are allowed by default; live external-system changes should be recorded here or requested explicitly in the active task.

## Standing Local Actions

| Scope | Approval | Notes |
| --- | --- | --- |
| Local workspace organization | Approved | Create folders, add notes, generate local analysis artifacts, and keep evidence organized inside `dresslikemommy-growth-2026/`. |

## Live Or External Actions

| Date | System | Action | Approval Source | Status | Rollback |
| --- | --- | --- | --- | --- | --- |
| 2026-04-28 | None | No live growth-channel actions approved from this workspace yet. | N/A | N/A | N/A |
| 2026-04-28 | Merchant Center | Destination approved for future paid-status custom-label writeback: paid-status-only supplemental feed keyed by `shopify_US_<product_id>_<variant_id>`. No upload/write performed. | Operator active request on 2026-04-28: "Regenerate from a fresh Shopify export before any real feed/custom-label writeback, then approve the upload destination." | Destination approved, pending separate upload execution. | Remove/delete the supplemental feed or upload a rollback file restoring prior label values if a future upload is executed. |
| 2026-04-28 | Merchant Center | Uploaded paid-status-only supplemental feed to existing source `10626787326` / `supplemental_feed_pilot.txt`, updating only `custom_label_4`. | Operator active request on 2026-04-28: "Execute the paid-status-only Merchant Center supplemental feed upload with a pre-upload snapshot and rollback file." | Executed at April 28, 2026 5:32 PM EDT; 7,324 submitted, 5,933 matched, 1,391 `Offer does not exist`, attributes all recognized. | Upload `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-merchant-paid-status-upload/rollback_restore_pre_upload_custom_label_4.csv` to the same source to restore pre-upload `custom_label_4` values. |
