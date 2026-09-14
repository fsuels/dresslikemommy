# Google Shopping Parent-Outfit Merchant TSV Refresh Execution

Date: 2026-05-21

## Scope

Fresh owner approval in the current session was limited to:

- Restore Chrome/Codex file-upload capability.
- Upload only `google_shopping_parent_outfit_merchant_supplemental_update_20260520.tsv` to existing Merchant source `10663204023`.
- Wait for processing and rerun the parent-outfit counts/images/no-catchall gate.

No activation, scope broadening, source reset, broad sync, campaign/product/budget/bid/status/conversion/billing change, or product mutation was approved.

## File Upload Recovery

- Confirmed Chrome was running and the Codex Chrome extension plus native host were installed.
- Enabled the Codex Chrome extension setting `Allow access to file URLs`.
- Cleared the stale Playwright MCP process that owned the temporary browser profile.
- Verified the browser automation file chooser could attach the approved TSV in Merchant Center.

## Merchant Upload

- Merchant account: `Dresslikemommy` / `124884876`.
- Existing supplemental source: `10663204023`.
- Uploaded file: `google_shopping_parent_outfit_merchant_supplemental_update_20260520.tsv`.
- Source type: `File (manual)`.

Before this session's refresh, Merchant source `10663204023` read:

- Last updated: `May 20, 2026 7:11 AM`.
- Total updated products: `4,531`.
- Matched products: `4,390`.
- Attribute names: all recognized.
- Source issue: `Offer does not exist`, affected products `141`.

After this session's approved refresh, Merchant source `10663204023` read:

- Last updated: `May 21, 2026 5:35 AM`.
- Total updated products: `4,531`.
- Matched products: `4,392`.
- Attribute names: all recognized.
- Source issue: `Offer does not exist`, affected products `139`.

Evidence: `merchant_source_10663204023_after_approved_tsv_refresh_20260521T093710Z.json`.

## Gate Reruns

Immediate gate rerun `20260521T093641Z` failed closed:

- Expected included variant rows: `4,531`.
- Live rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `4,390`.
- Missing expected rows: `141`.
- Unexpected ready-label rows: `0`.
- Label mismatches: `0`.
- Image mismatches: `0`.
- Missing live images: `0`.
- Bad catchall units: `0`.
- V2 Shopping campaigns remained paused.
- Old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` remained paused.

Delayed gate rerun `20260521T093856Z` also failed closed with the same Ads-side count:

- Expected included variant rows: `4,531`.
- Live rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `4,390`.
- Missing expected rows: `141`.
- Unexpected ready-label rows: `0`.
- Label mismatches: `0`.
- Image mismatches: `0`.
- Missing live images: `0`.
- Bad catchall units: `0`.
- V2 Shopping campaigns remained paused.
- Old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` remained paused.

Additional bounded propagation gate rerun `20260521T094158Z` still failed closed with the same Ads-side count:

- Expected included variant rows: `4,531`.
- Live rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `4,390`.
- Missing expected rows: `141`.
- Unexpected ready-label rows: `0`.
- Label mismatches: `0`.
- Image mismatches: `0`.
- Missing live images: `0`.
- Bad catchall units: `0`.
- V2 Shopping campaigns remained paused.
- Old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` remained paused.

Current-session rerun `20260521T095240Z` still failed closed with the same Ads-side count:

- Expected included variant rows: `4,531`.
- Live rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `4,390`.
- Missing expected rows: `141`.
- Unexpected ready-label rows: `0`.
- Label mismatches: `0`.
- Image mismatches: `0`.
- Missing live images: `0`.
- Bad catchall units: `0`.
- V2 Shopping campaigns remained paused.
- Old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` remained paused.

## Decision

The approved upload succeeded and Merchant source matching improved from `4,390` to `4,392`, but the bounded Google Ads Shopping-product propagation reruns still did not reflect that movement and remain fail-closed at `4,390 / 4,531`.

Activation is still blocked. Because the bounded propagation rerun still holds at `4,390 / 4,531`, stop repeating uploads/resyncs and use the read-only eligibility diagnostic approval packet before any next repair or exclusion packet. The next valid lane is to isolate why the `4,390` live labeled rows read `NOT_ELIGIBLE` and why the remaining expected rows still do not surface in the Ads Shopping-product readback.

## Guardrails Preserved

- No Shopping activation or unpause occurred.
- No budget, bid, status, product-group, conversion, billing, campaign, broad sync, source reset, Shopify product, title, price, handle, inventory, or feed-scope change occurred.
- No scope-down launch is allowed from this evidence.

## Evidence

- `merchant_source_10663204023_after_approved_tsv_refresh_20260521T093710Z.json`
- `google_shopping_parent_outfit_merchant_feed_gate_20260521T093641Z.json`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_GATE_READBACK_20260521T093641Z.md`
- `google_shopping_parent_outfit_merchant_feed_gate_20260521T093856Z.json`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_GATE_READBACK_20260521T093856Z.md`
- `google_shopping_parent_outfit_merchant_feed_gate_20260521T094158Z.json`
- `google_shopping_parent_outfit_merchant_feed_gate_20260521T095240Z.json`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_GATE_READBACK_20260521T095240Z.md`
