# Google Ads API Basic Access Status

Date: 2026-05-18

## API Center Readback

- Manager account selected: `Dress Like Mommy Manager`
- MCC ID: `700-107-9966`
- Current developer-token access level: `Explorer Access`
- API contact email: `info@dresslikemommy.com`
- Company name: `Dress Like Mommy`
- Company URL: `https://dresslikemommy.com`
- Company type: `Advertiser`
- Principal place of business: `United States`

## Basic Access Form State

The Basic Access application form was opened at:

`https://support.google.com/adspolicy/contact/new_token_application`

2026-05-19 update:

- Owner received Google Ads API Basic Access Approval for manager account `700-107-9966`.
- The API rerun is no longer blocked by `DEVELOPER_TOKEN_NOT_APPROVED`.
- A local account-capable runtime was created at `/tmp/dlm-google-ads-api-runtime-20260519` with the official `google-ads` Python client because the older `/tmp/dlm-google-ads-api-venv` path was not a complete virtualenv.
- The forecast harness now sleeps between single-keyword forecast calls to respect Google's short `Requests per service per method` throttle.
- The API export completed successfully.

2026-05-18 update:

- Owner approved completing and submitting the Basic Access form.
- The prepared RTF design document was attached under question 7: `google_ads_api_tool_design_document.rtf`.
- The form was submitted successfully.
- Submission readback: Google displayed `Your email has been sent` and `The Google Ads API Compliance team has received your ticket.`
- Google's confirmation page said applications are typically reviewed within three business days, though complex reviews may take longer.

Fields submitted:

- API contact email confirmed checkbox: checked
- MCC ID: `700-107-9966`
- Contact email: `info@dresslikemommy.com`
- Ongoing relationship with a Google representative: `No`
- Company URL: `https://dresslikemommy.com`
- Business model / Google Ads use: filled from the prepared answer packet
- Tool access: `Internal users - employees only (outsourcing, contractor included)`
- Token used with tool developed by someone else: `No`
- App Conversion Tracking and Remarketing API: `No`
- Campaign types: `Search`
- Tool capabilities: `Reporting`, `Keyword Planning Services`
- Accuracy acknowledgment: checked
- Terms and Conditions acceptance: checked

## Upload Blocker

Upload-ready design document:

`google_ads_api_tool_design_document.rtf`

Resolved on 2026-05-18. The file was attached through the form's native `Choose file` control and the page displayed `google_ads_api_tool_design_document.rtf(file attached)`.

Earlier 2026-05-18 Chrome-specific attempts:

- The direct Chrome extension settings route was blocked by browser security policy for `chrome://extensions`.
- A normal form upload click was attempted, but the native upload did not become controllable from the active app surface.
- A direct in-page file injection attempt was attempted, but the support form sandbox did not expose `File`, `Blob`, `DataTransfer`, `atob`, or `Uint8Array`, so the attachment could not be synthesized safely.
- Fallback to the Playwright-controlled browser allowed the required form attachment and submission.

## API Rerun Status

The exact requested rerun harness is ready:

```bash
/tmp/dlm-google-ads-api-runtime-20260519/bin/python dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-18-search-keyword-planner-us-020/run_google_ads_api_us_search_keyword_forecast.py --customer-id 3990976848
```

Current API result:

- Status: complete
- Historical rows: `29`
- Forecast rows: `29`
- Joined decision rows: `29`
- Historical CSV: `google_ads_api_us_search_historical_rows.csv`
- Forecast CSV: `google_ads_api_us_search_forecast_rows.csv`
- Joined decision CSV: `google_ads_api_us_search_joined_decision_rows.csv`
- Summary JSON: `google_ads_api_us_search_keyword_summary.json`

API proof:

- Source rows: `29`
- Match types: `26` exact, `3` phrase
- Geo target ID: `2840` United States
- Language ID: `1000` English
- Network: `GOOGLE_SEARCH`
- Max CPC: `200000` micros (`$0.20`)
- Forecast period: `2026-05-20` through `2026-06-18`

## Next Owner Action

1. Use `google_ads_api_us_search_joined_decision_rows.csv` to build the launch keyword set.
2. Launch only the forecastable exact-match priority terms first unless fresh data or owner approval expands scope.
3. Keep the `$0.20` CPC cap as a hard launch guardrail; the historical low top-of-page bids are still above `$0.20`, so expect constrained/lower-position delivery.
