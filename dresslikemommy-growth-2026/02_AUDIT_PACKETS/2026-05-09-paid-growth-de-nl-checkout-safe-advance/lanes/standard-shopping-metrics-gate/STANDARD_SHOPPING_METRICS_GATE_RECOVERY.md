# Standard Shopping Metrics Gate Recovery

Worker: Worker D
Timestamp: 2026-05-09 01:23 EDT
Scope: local/read-only only

## Target

- Problem: `PROB-2026-05-08-STANDARD-SHOPPING-LIVE-METRICS-READBACK`
- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Campaign ID: `23802638621`
- Goal: recover a fresh read-only metrics path for post-2026-05-06 Standard Shopping spend/CPC/conversion readback without changing Google Ads, Merchant, feed, product scope, product groups, feed labels, conversion goals, credentials, or live product data.

## Result

Status: `CREDENTIALS_REQUIRED`

No fresh post-2026-05-06 Google Ads metrics were recovered locally. The newest usable Standard Shopping metrics evidence remains:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-standard-shopping-cost-control-review/STANDARD_SHOPPING_COST_CONTROL_REVIEW.md`
- Date range: Apr 29-May 5, 2026
- Campaign totals: `81` clicks, `3,906` impressions, `$0.23` avg CPC, `$18.58` cost, `0.00` conversions, `0.00` conversion value
- Post-review live change already documented there: included child product-group base bids lowered from `$0.05` to `$0.04`; budget, status, product scope, feed labels, product groups, and conversion goals unchanged.

## Recovery Attempts

### 1. Local Evidence And Export Search

Commands used:

- `find . -type f \( -iname '*standard*shopping*' -o -iname '*shopping*metrics*' -o -iname '*live*readback*' -o -iname '*campaign*metrics*' -o -iname '*google*ads*metrics*' \) -not -path './.git/*' | sort`
- `rg -n "Apr 29-May 5|May 6|May 7|May 8|May 9|81 clicks|3,906|\$18\.58|\$0\.23 avg CPC|product-group bids|STANDARD_SHOPPING_COST_CONTROL|STANDARD_SHOPPING_LIVE_READBACK_GATE" dresslikemommy-growth-2026/02_AUDIT_PACKETS ops -g '*.md' -g '*.txt' -g '*.csv' -g '*.json' -S`
- `rg -n "23802638621|DLM_US_STANDARD_SHOPPING_TEST_PAID_READY|\$18\.58|81 clicks|0\.00 conversions|cost|clicks|avg|CPC|conversion value" dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-0[7-9]* ops/AGENT_WORKLOG.md ops/PROBLEM_TRACKER.md -S`

Result:

- Found many older Standard Shopping settings/status artifacts and guardrail references.
- Found no newer Standard Shopping performance export/readback than the 2026-05-06 cost-control review.
- Found the 2026-05-08 gate note confirming a Google Ads browser redirect to sign-in, with no metrics captured:
  - `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/raw/STANDARD_SHOPPING_LIVE_READBACK_GATE.md`

### 2. Non-Mutating CLI/API Credential Availability Check

Commands used:

- `env | cut -d= -f1 | rg -i 'GOOGLE|ADS|ADWORDS|GAQL|GADS' || true`
- `command -v gcloud`
- checked for local Google Ads config files at:
  - `$HOME/google-ads.yaml`
  - `$HOME/.google-ads.yaml`
  - `$HOME/.config/google-ads.yaml`
  - `$HOME/.config/google_ads/google-ads.yaml`
  - `$HOME/.config/gcloud/application_default_credentials.json`
- `gcloud auth list --filter='status:ACTIVE' --format='value(status)'`
- `gcloud config get-value account` with the account value redacted
- `python3` import probe for `google.ads.googleads`

Result:

- `gcloud` is installed and has an active configured account, but that does not provide a Google Ads metrics path by itself.
- No Google Ads environment variable names were present.
- No checked `google-ads.yaml` or Application Default Credentials file was present.
- `google.ads.googleads` Python package is not installed.
- No safe local Google Ads API/CLI path was available for a read-only GAQL metrics query.

## Guardrails Preserved

No browser sign-in was attempted. No Google Ads UI writes, campaign/budget/bid/status edits, Standard Shopping edits, Merchant/feed/product-scope/product-group/feed-label/conversion changes, credential changes, or destructive filesystem actions were made.

## Next Unblock Action

Provide one of:

1. A logged-in Google Ads browser/account session that can access campaign `23802638621`, for no-edit readback only.
2. An approved read-only Google Ads export for campaign `23802638621` covering post-2026-05-06 spend, clicks, avg CPC, conversions, conversion value, search terms, product performance, and product-group metrics.
3. A read-only Google Ads API credential/config with sufficient scope for GAQL metrics queries, without granting write access.

Problem tracker recommendation: keep `PROB-2026-05-08-STANDARD-SHOPPING-LIVE-METRICS-READBACK` at `CREDENTIALS_REQUIRED` and add this recovery attempt as evidence. Any live Standard Shopping edit after metrics readback remains `OWNER_APPROVAL_REQUIRED`.
