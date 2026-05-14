# US Shopping Auth Export Join Prep

Generated: `2026-05-14T18:04:07+00:00`

## Purpose

- Package the next authenticated read-only Standard Shopping export step for campaign `23802638621`.
- Force the future item-level export to join against the `18` public-clean US Shopping candidate rows first.
- Keep held PDP rows out of title/feed/product decisions unless their exact repair gate is cleared or item-level proof warrants the one documented weak-fit exception.
- Avoid product/feed/title/product-group/bid/budget/status writes from local hypotheses.

## Current Local Result

- Public-clean candidate rows loaded: `18`.
- Public-clean unique handles: `7`.
- Held/review rows loaded for exclusion gates: `6`.
- Export template: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/us_shopping_authenticated_item_export_template.csv`.
- Handle-level scope: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/us_shopping_public_clean_scope_by_handle.csv`.

## Required Authenticated Export Columns

- Required if available: `item_id`, `product_title`, `product_group`, `custom_label_0`, `custom_label_4`, `search_term` or `query`, `impressions`, `clicks`, `cost`, `conversion_value`, and `landing_url` or another product URL column.
- The join key is the Shopify product handle parsed from a product URL. If the export cannot include URLs, add the handle manually from the visible destination URL before using it for decisions.

## Decision Rules

- `PUBLIC_CLEAN_MATCH_NO_IMPRESSION_PROOF`: no title/feed action; no item-level demand proof.
- `ITEM_LEVEL_PROOF_PUBLIC_CLEAN_NO_TITLE_ACTION_YET`: item received impressions and is public-clean, but the title does not obviously miss the observed buyer intent.
- `REVIEW_FOR_NARROW_TITLE_FEED_APPROVAL_PACKET`: item received impressions and the exported title appears to miss one or more buyer-intent signal groups. This is a review candidate only, not approval to edit.
- `HOLD_FROM_TITLE_FEED_DECISIONS_UNTIL_REPAIRED_OR_PROVEN_EXCEPTION`: the row matched a held PDP gate and must stay out of decisions unless the repair/readback condition is met.
- `UNMATCHED_TO_PUBLIC_CLEAN_SCOPE_REVIEW_BEFORE_USE`: the export row did not match the public-clean scope; review before using it.

## Optional Export Join Result

- No authenticated export was supplied in this automation run.
- This is expected in the unattended runtime because authenticated Google Ads/account surfaces are already gated as `AUTOMATION_CAPABILITY_MISMATCH`.

## Guardrails

- No Google Ads upload/apply/import/add keyword/bid/budget/status/negative/product-group write occurred.
- No Merchant feed/source/product/title edit occurred.
- No Shopify Admin product/title/feed-visible edit and no live Shopify theme push occurred.
- No Pinterest, GA4/GTM, billing, conversion, credential, or destructive filesystem write occurred.

## Next Action

Run the authenticated read-only product-item export in a Google Ads/Merchant-capable session, save it outside secrets-bearing paths, then run:

```bash
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/run_us_shopping_auth_export_join_prep.py --export-csv /path/to/authenticated-export.csv
```

Only if the joined decision CSV identifies proven mismatches should the next operator prepare a narrow owner approval packet for Shopify/Merchant title/feed repair.
