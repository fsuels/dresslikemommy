# Rollbacks

This pass did not modify theme runtime code. It created inventory artifacts and a local backup only.

## Rollback assets

- Backup zip:
  - `dlm-google-remediation-2026-03-27/dresslikemommy-theme-backup-2026-03-27.zip`

## Rollback approach for later remediation work

1. Preserve this inventory folder as the pre-edit baseline.
2. If a later repo-based remediation needs reversal, restore files from the backup zip and compare against git history before deploy.
3. If a later remediation happens in Shopify Admin or GTM, export or screenshot those external settings separately because they are not restorable from this repo backup alone.

## Phase 1 local rollback

- Repo files changed in the Phase 1 local pass:
  - `layout/theme.liquid`
  - `ops/customer-events/ga4-checkout-ecommerce-pixel.js`
- To roll back only the repo-side Phase 1 changes, restore those files from git history or from the pre-edit backup zip after validating against any unrelated newer edits.
