# Authenticated GB/CA/AU CPC Validation Attempt

Run time: 2026-05-14 16:24 EDT

## Scope

- Source packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-canonical-url-packet/gb_ca_au_36_clean_route_cpc_validation_rows_canonical_urls.csv`
- Validation matrix: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/gb_ca_au_36_keyword_planner_validation_matrix.csv`
- Intended gate: canonical `36` GB/CA/AU rows, `72` exact/phrase validations, max CPC `$0.15`, no upload/apply/add keyword/bid/status/negative action.

## Authenticated Surface

- Existing authenticated Google Ads account surface was found through Chrome remote debugging.
- Account text readback: `399-097-6848 dresslikemommy.com` and `testhqfinds@gmail.com`.
- Keyword Planner accepted the `72` exact/phrase validation inputs and created plan `1421560327`.
- No campaign, ad group, live keyword, bid, budget, status, negative, billing, conversion, feed, Shopify, Merchant, Pinterest, GA4/GTM, or product write occurred.

## Exported Evidence

Downloaded authenticated exports into `downloads/`:

- `All Keywords Forecast 2026-05-14 at 16_22_40.csv`
- `Saved Keywords Stats 2026-05-14 at 16_23_13.csv`

Readback problem:

- Forecast context stayed `United States`, `All languages`, `Google`, `Broad`, `Maximize conversions`, with date `Jun 1 - 30, 2026`.
- Forecast aggregate showed `Avg. CPC $4.18`, not the required max-CPC `$0.15` market/match row proof.
- Forecast export is aggregate by campaign/device/location, not canonical keyword rows.
- Saved-keyword export is historical stats, not forecast CPC proof, and it collapsed exact/phrase inputs into `35` keyword rows without canonical `market` and `match_type` fields.

## Parser Result

The parser was patched to read real Google export encoding/TSV shape and to require canonical matrix matching before any PASS decision.

Outputs:

- `all_keywords_forecast_parser_decisions.csv`
- `all_keywords_forecast_parser_summary.json`
- `saved_keywords_stats_parser_decisions.csv`
- `saved_keywords_stats_parser_summary.json`

Summary:

- Forecast export: `8` decision rows, `0` `PASS_015_CPC_GATE`, all `MISSING_REQUIRED_FORECAST_DATA`.
- Saved-keyword stats export: `37` decision rows, `0` `PASS_015_CPC_GATE`, all `MISSING_REQUIRED_FORECAST_DATA`.

## Decision

No fresh `GREEN` action row was created because there are `0` real `PASS_015_CPC_GATE` rows.

The active gate remains: obtain an authenticated export/readback that proves GB/CA/AU market targeting, exact/phrase match validation, and max CPC `$0.15` row-level feasibility. The next attempt should use either:

- Google Ads API / KeywordPlan forecast with explicit `geo_target_constants`, language, exact/phrase ad group criteria, and max CPC micros `150000`; or
- UI workflow that can be read back as GB/CA/AU, exact/phrase, manual CPC/max CPC `$0.15`, then export keyword-level forecast rows.

Do not upload/apply/add keywords, raise bids, change statuses/budgets, or add negatives from the invalid US/Broad/Maximize-conversions export.

## 2026-05-14 16:44 EDT Retry And Cleanup

Follow-up scope: execute the next-best action without adding any live keyword/bid/budget/status/negative/campaign write.

What was attempted:

- Re-opened the authenticated Keyword Planner plan in the existing Chrome/Google Ads session.
- Retried the UI location picker with typed country searches for `Canada`, `Australia`, `United Kingdom`, `Great Britain`, `England`, and `UK`.
- The UI location picker returned `No results found` for those country searches, so it still could not produce a valid GB/CA/AU market-scoped row-level export.
- Ran the Google Ads API forecast harness dry-run over the canonical matrix: `72` rows, `24` AU, `24` CA, `24` GB, `36` exact, `36` phrase, max CPC `150000` micros.
- Installed the official `google-ads` Python client into a temporary venv at `/tmp/dlm-google-ads-api-venv` after the system Python rejected direct package installation as externally managed.
- Retried the live API command with `--customer-id 3990976848`; it failed closed before any API request because no Google Ads API config file exists at the expected path `/Users/fsuels/google-ads.yaml`, and no alternate `google-ads.yaml` / `googleads.yaml` / `adwords.yaml` file was found under the checked user paths.
- Removed the temporary Keyword Planner plan created by this validation attempt. The after-state readback is the Keyword Planner home page showing `1 plan removed from your account`; older historical draft plans remain visible and were not touched.

Evidence added:

- `ui_location_search_no_results.png`
- `keyword_planner_plan_removed_readback.png`
- `../2026-05-14-automation-cpc-validation-decision-kit/google_ads_api_cpc_forecast_summary.json`

Decision after retry:

- `0` valid GB/CA/AU exact/phrase max `$0.15` keyword-level pass rows exist.
- No `GREEN` action row was created.
- P0 remains active, but the blocker is now precise: `API_CLIENT_READY_CONFIG_MISSING__UI_LOCATION_NO_RESULTS__PLAN_CLEANED_UP`.
