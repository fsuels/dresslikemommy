# GSC 404 Audit Outputs

Use these files in this order:

- `shopify_url_redirects.csv`
  - Import-ready Shopify URL redirects built from the March 24, 2026 GSC `Not found (404)` export.
  - This file has already been filtered with `non_product_live_status.csv` so it does not overwrite the collection/page/misc redirects that are already live on the storefront.
- `already_resolved.csv`
  - Exact non-product source paths that were live-verified as existing `301` redirects and therefore removed from the import CSV.
- `gone_candidates.csv`
  - Seasonal holiday, dragon novelty, and accessory URLs that should stay removed instead of being redirected.
- `redirect_candidates_detailed.csv`
  - The same import rows with GSC counts, source examples, reasons, and targets.
- `manual_review.csv`
  - Currently empty in this pass.

Supporting files:

- `live_path_sets.json`
  - Cached sitemap snapshot used to validate canonical product, collection, and page targets.
- `non_product_live_status.csv`
  - Targeted live verification of non-product source paths to avoid overwriting working admin redirects.
- `summary.md`
  - High-level counts for redirects, gone rows, and already resolved rows.

Regenerate the audit:

```bash
python3 ops/scripts/build_gsc_404_audit.py \
  --status-overrides-csv ops/redirect_audit_gsc/non_product_live_status.csv
```

Optional deeper verification:

```bash
python3 ops/scripts/build_gsc_404_audit.py \
  --verify-live-status \
  --workers 1 \
  --status-overrides-csv ops/redirect_audit_gsc/non_product_live_status.csv
```
