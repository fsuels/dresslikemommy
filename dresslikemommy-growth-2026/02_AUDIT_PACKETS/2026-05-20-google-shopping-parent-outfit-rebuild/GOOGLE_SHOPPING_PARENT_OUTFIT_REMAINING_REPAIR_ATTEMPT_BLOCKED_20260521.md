# Google Shopping Parent-Outfit Remaining Repair Attempt Blocked

Generated: `2026-05-21T10:46:27Z`

## Scope

Owner approved only the narrow remaining eligibility repair/exclusion:

- Hold out `20` current `OUT_OF_STOCK` expected offer IDs from strict paid-ready eligibility without changing Shopify inventory.
- Repair the current Ads-visible blank-label rows with the smallest supplemental label/image overlay.
- Repair only the narrow Ads-absent presence lane for the remaining expected offer IDs.
- Keep all Shopping campaigns paused.

## Current Readback

Fresh read-only gate after the attempted Merchant step:

- Gate JSON: `google_shopping_parent_outfit_merchant_feed_gate_20260521T104627Z.json`
- Gate passed: `false`
- Expected rows: `4,531`
- Ready rows: `4,392`
- Missing expected rows: `139`
- Bad catchall units: `0`
- Campaign status ok: `true`
- Old test campaign paused: `true`
- Merchant Content API available: `false`

Fresh eligibility diagnostic used for the repair split:

- Diagnostic JSON: `google_shopping_parent_outfit_eligibility_diagnostic_20260521T103741Z.json`
- Expected rows: `4,531`
- Ads-present expected rows: `4,460`
- Ads-absent expected rows: `71`
- Ads-ready-label rows: `4,392`
- Ads-present non-ready-label rows: `68`
- Availability counts: `IN_STOCK=4,440`, `OUT_OF_STOCK=20`

The current `68` Ads-visible non-ready rows are blank-label Spanish-language Shopping rows. The current Merchant supplemental source list shows only four supplemental sources, all used in `Shopify App API (US, English)`. No existing Spanish-targeted supplemental source was visible.

## Artifacts Built

Local exact-row artifacts were generated with no external write:

- `GOOGLE_SHOPPING_PARENT_OUTFIT_REMAINING_ELIGIBILITY_REPAIR_ARTIFACTS_20260521T104255Z.md`
- `google_shopping_parent_outfit_remaining_eligibility_repair_artifacts_20260521T104255Z.json`
- `google_shopping_parent_outfit_blank_label_overlay_20260521T104255Z.tsv`
- `google_shopping_parent_outfit_blank_label_repair_scope_20260521T104255Z.csv`
- `google_shopping_parent_outfit_ads_absent_presence_repair_scope_20260521T104255Z.csv`
- `google_shopping_parent_outfit_out_of_stock_holdout_scope_20260521T104255Z.csv`
- `merchant_label_update_spec_excluding_oos_holdout_20260521T104255Z.csv`

## Attempted Merchant Action

I opened the authenticated Merchant Center supplemental-source creation flow and selected `Upload a file from your computer` for a new minimal file source. This was the only visible narrow route to target the Spanish blank-label rows, because existing supplemental sources were US/en only.

The browser file upload failed before transmission:

- Error: `Not allowed`
- Wrapper message: `fileChooser.setFiles failed`
- Result: no Merchant source was created, no file was uploaded, and no Continue/Create/Upload action was submitted.

## Guardrails Preserved

- All parent-outfit V2 Shopping campaigns stayed paused.
- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` stayed paused.
- No Google Ads campaign, budget, bid, status, product group, conversion, billing, or activation change occurred.
- No Shopify title, price, handle, body, SEO, inventory, publication, product, or variant write occurred.
- No broad Google & YouTube sync, source reset, product recreation, or Merchant primary-source overwrite occurred.
- No activation discussion is authorized from this packet.

## Blocker

The approved blank-label repair cannot be completed from this Chrome profile until local Chrome extension file upload is allowed for the Codex extension. Merchant API / Content API scope is also unavailable from the local token, so there is no current API fallback for a supplemental upload.

The next exact action is to enable Chrome extension file upload access for this profile, then retry only the generated `68`-row TSV overlay against a Spanish-targeted supplemental source path, followed by processing wait and the read-only counts/images/no-catchall gate. The `71` Ads-absent presence lane remains blocked unless a narrow Merchant/Google & YouTube per-product presence control is exposed; broad sync/source reset/product recreation is still forbidden.
