# Google Ads API CPC Forecast Retry Harness

Timestamp: 2026-05-14 16:39 EDT

Scope: repo-local read-only harness for the active P0 GB/CA/AU `$0.15` CPC validation gate. No Google Ads upload, apply, add keyword, bid, budget, status, campaign, negative, feed, product, conversion, billing, or credential write occurred.

## Result

- Added `run_google_ads_api_cpc_forecast.py` beside the existing CPC decision kit.
- The harness reads `gb_ca_au_36_keyword_planner_validation_matrix.csv`.
- It forecasts each canonical row one keyword at a time so the output is row-level, not the invalid US/Broad aggregate export from the prior UI attempt.
- It uses Google Search only, English language `1000`, max CPC `150000` micros (`$0.15`), and market geo targets:
  - `GB`: `2826`
  - `CA`: `2124`
  - `AU`: `2036`
- It writes parser-compatible rows to `google_ads_api_cpc_forecast_rows.csv`, then the existing parser can classify rows as `PASS_015_CPC_GATE`, `FAIL_015_CPC_GATE`, `LOW_VOLUME_OR_NO_AUCTION`, `POLICY_OR_DESTINATION_BLOCK`, or `MISSING_REQUIRED_FORECAST_DATA`.

## Verification

```bash
python3.13 -m py_compile dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/run_google_ads_api_cpc_forecast.py
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/run_google_ads_api_cpc_forecast.py --dry-run
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/run_google_ads_api_cpc_forecast.py
```

Outcomes:

- Compile passed.
- Dry run passed with `72` source rows: `24` AU, `24` CA, `24` GB; `36` exact and `36` phrase; max CPC `150000` micros.
- First live API attempt stopped before any API call because `GOOGLE_ADS_CUSTOMER_ID` was unset and `--customer-id` was not supplied. This is recorded as `AUTOMATION_CAPABILITY_MISMATCH`, not as evidence that the Google Ads account is inaccessible.
- Follow-up live API retry installed the official `google-ads` Python client into temporary venv `/tmp/dlm-google-ads-api-venv` and ran with `--customer-id 3990976848`; it still failed closed before any API request because no Google Ads API config file exists at `/Users/fsuels/google-ads.yaml`, and no alternate `google-ads.yaml` / `googleads.yaml` / `adwords.yaml` file was found under the checked user paths.
- Follow-up UI retry in authenticated Keyword Planner returned `No results found` for `Canada`, `Australia`, `United Kingdom`, `Great Britain`, `England`, and `UK` in the location selector, so no valid GB/CA/AU scoped export was produced.
- The temporary Keyword Planner plan created during the validation attempt was removed; after-state readback showed `1 plan removed from your account`.

Additional follow-up evidence:

- `google_ads_api_cpc_forecast_live_attempt_summary.json`
- `GOOGLE_ADS_API_CONFIG_SETUP.md`
- `../2026-05-14-authenticated-gb-ca-au-cpc-validation/ui_retry_and_plan_cleanup_summary.json`

## Account-Capable Command

In an account-capable shell with the official `google-ads` Python client installed and a valid Google Ads config loaded:

```bash
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/run_google_ads_api_cpc_forecast.py --customer-id 3990976848
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/validate_keyword_planner_forecast_export.py --forecast-csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/google_ads_api_cpc_forecast_rows.csv
```

Only real `PASS_015_CPC_GATE` rows may become a new `GREEN` action-queue row, and only after fresh Ads before-state readback, reviewer pass, anti-cannibalization check, and after-state readback plan.

## Guardrails

- This is forecast/readback only.
- Do not raise bids above `$0.15`.
- Do not use the prior invalid US/Broad/Maximize-conversions export for promotion.
- Do not upload or apply any keyword, negative, bid, budget, status, or campaign action from this harness alone.
