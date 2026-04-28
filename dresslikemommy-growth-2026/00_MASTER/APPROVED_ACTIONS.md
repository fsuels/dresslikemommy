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
