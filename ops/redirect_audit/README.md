# Redirect Audit Outputs

Use these files in this order:

- `verified_missing_shopify_redirects.csv`
  - Safe import-ready rows built from live-verified `404` URLs checked directly against the storefront.
- `verified_missing_details.csv`
  - The same verified rows with reasoning and current live status.

The broader first-pass audit files in this folder are partial:

- `shopify_url_redirects.csv`
- `redirect_candidates_detailed.csv`
- `gone_candidates.csv`
- `manual_review.csv`
- `already_resolved.csv`
- `summary.md`
- `status_cache.json`

Those files came from a wide historical-export sweep and hit Shopify `429` rate limiting on many URLs. Treat them as operator working files, not final import files, until the audit script is rerun in smaller batches.

Recommended rerun pattern:

```bash
python3 ops/scripts/build_discontinued_redirect_audit.py \
  --export GPT/products_export_1_backfill.csv \
  --output-dir ops/redirect_audit_batch \
  --workers 2 \
  --include-regex 'swim|swimsuit|bikini|bathing|t-?shirt|tee|sweater|jacket|coat|christmas|reindeer|santa|daddy and me|daddy-me'
```
