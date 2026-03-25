# Discontinued Redirect Audit

- Generated at: 2026-03-24 23:29:22 EDT
- Source export: `GPT/products_export_1_backfill.csv`
- Unique product handles audited: `660`

## Live Status Counts

- `200`: `15`
- `301`: `22`
- `404`: `47`
- `429`: `576`

## Decision Buckets

- `already_redirected`: `22`
- `gone`: `37`
- `live`: `15`
- `redirect`: `10`
- `review`: `576`

## Redirect Targets

- `/collections/family-pajamas`: `2`
- `/collections/sweaters`: `8`

## Generated Files

- `shopify_url_redirects.csv`: import-ready redirect rows for Shopify admin.
- `redirect_candidates_detailed.csv`: redirect rows with reasons and product metadata.
- `gone_candidates.csv`: dead URLs that should stay removed rather than be redirected.
- `manual_review.csv`: dead URLs without a safe automatic rule.
- `already_resolved.csv`: live or already redirected URLs.

## Notes

- Holiday and dragon-pattern products are conservatively treated as `gone` candidates.
- Only high- or medium-confidence matches become automatic redirect rows.
- Anything ambiguous is routed to manual review rather than forcing a weak redirect.
