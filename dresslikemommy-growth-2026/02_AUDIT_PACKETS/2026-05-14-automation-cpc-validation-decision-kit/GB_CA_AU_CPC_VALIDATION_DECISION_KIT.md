# GB/CA/AU CPC Validation Decision Kit

Timestamp: 2026-05-14 15:25 EDT

Scope: repo-local Keyword Planner input and future forecast-export parser prep for the existing canonical 36-row GB/CA/AU CPC validation packet. No Google Ads upload/apply/add keyword/bid/budget/status/negative action occurred.

## Result

- Source rows: `36`
- Markets: `{'AU': 12, 'CA': 12, 'GB': 12}`
- Keyword Planner validation rows: `72` (`exact` plus `phrase` for each source row)
- Hard max CPC gate: `$0.15`
- Decision state: `AUTHENTICATED_FORECAST_EXPORT_REQUIRED`

## Generated Inputs

- `keyword_planner_input_au_exact.txt` and `keyword_planner_input_au_phrase.txt`
- `keyword_planner_input_ca_exact.txt` and `keyword_planner_input_ca_phrase.txt`
- `keyword_planner_input_gb_exact.txt` and `keyword_planner_input_gb_phrase.txt`
- `gb_ca_au_36_keyword_planner_validation_matrix.csv`
- `keyword_planner_forecast_export_template.csv`
- `validate_keyword_planner_forecast_export.py`

## Route Scope

- `/collections/family-swimsuits`: `5` source rows
- `/collections/matching-outfits`: `11` source rows
- `/collections/mommy-and-me`: `15` source rows
- `/collections/pajamas`: `5` source rows

## Exact Next Gate

In an authenticated Google Ads / Keyword Planner session, validate these keywords at max CPC `$0.15`. Export the forecast/readback columns into a CSV shaped like `keyword_planner_forecast_export_template.csv`, then run:

```bash
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/validate_keyword_planner_forecast_export.py --forecast-csv /path/to/authenticated-forecast-export.csv
```

Only rows classified `PASS_015_CPC_GATE` may become a fresh `GREEN` action-queue row, and only after fresh Ads before-state readback, reviewer pass, anti-cannibalization check, and after-state readback plan. Rows classified `FAIL_015_CPC_GATE`, `LOW_VOLUME_OR_NO_AUCTION`, `POLICY_OR_DESTINATION_BLOCK`, or `MISSING_REQUIRED_FORECAST_DATA` must stay local and must not be uploaded.

## Guardrails

- This kit is not an upload file.
- Do not raise bids above `$0.15`.
- Do not upload head or close-head variants that already failed the hard CPC economics.
- Do not add negatives, change budgets, change statuses, alter conversion settings, or mutate feeds/products from this packet.
