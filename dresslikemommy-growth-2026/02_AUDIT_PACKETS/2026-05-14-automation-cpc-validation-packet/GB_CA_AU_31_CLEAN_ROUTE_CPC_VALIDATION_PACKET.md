# GB/CA/AU 31 Clean-Route CPC Validation Packet

Generated: 2026-05-14 automation run

## Purpose

Prepare the exact authenticated Google Ads / Keyword Planner validation scope for the next sales-moving GB/CA/AU Search repair step. This packet is local/read-only. It is not a Google Ads upload file and gives no authority to add keywords, change bids, budgets, statuses, negatives, or campaign settings.

## Capability Result

- `AUTOMATION_CAPABILITY_MISMATCH`: this unattended runtime cannot complete the authenticated Keyword Planner/UI CPC validation.
- Shell check found no Google Ads environment keys and the `google.ads.googleads` Python package is not installed.
- Existing automation memory already records authenticated account surfaces as mismatched; no Computer Use permission repair or startup probing was attempted.
- No external writes occurred.

## Exact Scope

- Rows selected: `31` from `ops/marketing/keyword_universe.csv`.
- `AU`: `10` rows, campaign `23834424182`, ad group `198852670520` / `Mommy & Me Dresses - Exact`.
- `CA`: `10` rows, campaign `23834423669`, ad group `196679079575` / `Mommy & Me Dresses - Exact`.
- `GB`: `11` rows, campaign `23838895360`, ad group `194138528537` / `Mommy & Me Dresses - Exact`.
- Included routes only: `/collections/mommy-and-me`, `/collections/family-matching`, `/collections/pajamas`.
- Excluded: all swimwear rows, because `/collections/swimsuits` still leaks supplier vendors through Shopify automatic product JSON.

## Validation Rule

For each row, validate in authenticated Google Ads Keyword Planner or keyword UI with the relevant country/language context. Pass only if the row can plausibly enter the auction at max CPC `$0.15` without a below-first-page warning, first-page/top-of-page estimate above `$0.15`, policy/destination issue, duplicate/cannibalized intent, or landing mismatch.

If a row passes, it can become a candidate for a small exact/phrase batch after fresh Ads readback, marketing safety reviewer pass, exact action-queue row, and after-state readback plan. If it fails, keep it local and record the failure reason. Do not raise bids above `$0.15`.

## Focused Public Route Readback

| Market | Route | Status | Supplier/url-brand hits | Ships-to signal | priceCurrency |
|---|---|---:|---:|---|---|
| AU | `/collections/family-matching` | `200` | `0` | `True` | `False` |
| AU | `/collections/mommy-and-me` | `200` | `0` | `True` | `False` |
| AU | `/collections/pajamas` | `200` | `0` | `True` | `False` |
| CA | `/collections/family-matching` | `200` | `0` | `True` | `False` |
| CA | `/collections/mommy-and-me` | `200` | `0` | `True` | `False` |
| CA | `/collections/pajamas` | `200` | `0` | `True` | `False` |
| GB | `/collections/family-matching` | `200` | `0` | `True` | `False` |
| GB | `/collections/mommy-and-me` | `200` | `0` | `True` | `False` |
| GB | `/collections/pajamas` | `200` | `0` | `True` | `False` |

## Rows

| Market | Score | Keyword | Match | Route | Action gate |
|---|---:|---|---|---|---|
| AU | 90 | `mum and daughter dresses for photos australia` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| AU | 90 | `mummy and me dresses for family photos` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| AU | 89 | `mother daughter wedding guest dresses australia` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| AU | 89 | `mum daughter beach dresses` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| AU | 89 | `mummy and me beach dresses australia` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| AU | 88 | `dad and son holiday shirts australia` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| AU | 88 | `family beach photo outfits australia` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| AU | 87 | `family matching pyjamas australia` | `exact` | `/collections/pajamas` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| AU | 87 | `matching family holiday outfits australia` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| AU | 87 | `mother daughter holiday dresses australia` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 90 | `mom daughter family picture dresses canada` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 90 | `mommy and me dresses canada pictures` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 90 | `mother daughter outfits for family pictures` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 89 | `mother daughter wedding guest dresses canada` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 88 | `family beach photo outfits canada` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 88 | `family cruise outfits canada` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 88 | `matching family outfits canada photos` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 88 | `matching family vacation outfits canada` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 87 | `matching family pajamas canada` | `exact` | `/collections/pajamas` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| CA | 87 | `mommy and me pajamas canada` | `exact` | `/collections/pajamas` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 90 | `mum and daughter dresses for photos` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 90 | `mummy and me dresses for family photos` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 89 | `mum daughter wedding guest dresses` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 89 | `mummy and me beach dresses` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 88 | `dad and son holiday shirts` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 88 | `family beach photo outfits uk` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 88 | `matching family outfits for holiday photos` | `phrase` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 87 | `family matching pyjamas` | `exact` | `/collections/pajamas` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 87 | `matching family holiday outfits` | `exact` | `/collections/family-matching` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 87 | `mother daughter holiday dresses uk` | `exact` | `/collections/mommy-and-me` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |
| GB | 87 | `mummy and me pyjamas` | `exact` | `/collections/pajamas` | `keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload` |

## Files

- Row CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-packet/gb_ca_au_31_clean_route_cpc_validation_rows.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-packet/gb_ca_au_31_clean_route_cpc_validation_summary.json`

## Guardrails Preserved

- No Google Ads upload/apply/import/add keyword/bid/budget/status/negative/campaign write.
- No Shopify Admin product/vendor/source metadata edit and no live theme push/sync/publish.
- No Merchant, Pinterest, GA4/GTM, billing, feed, product-scope, product-group, conversion, credential, or destructive filesystem write.
- No Computer Use startup probing or permission repair.
