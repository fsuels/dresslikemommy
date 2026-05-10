# Standard Shopping Post-May-6 Readback

Generated: 2026-05-09.

Lane: `standard-shopping-post-may6-readback`.

Scope: read-only Google Ads metrics recovery for campaign `23802638621` / `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`.

Decision: `CUSTOM_RANGE_READBACK_PASSED_NO_ADS_WRITES`.

## Paths Attempted

1. Default Chrome DevTools MCP browser route:
   - Opened the campaign URL in the tool-managed browser.
   - Result: redirected to Google sign-in.
   - Stopped without signing in, switching accounts, accepting permissions, or changing credentials.
   - Evidence: `raw/google_ads_signin_snapshot.txt`, `raw/google_ads_signin_gate.png`.

2. Desktop Computer Use route:
   - Tried to inspect `Google Chrome`.
   - Result: Apple event error `-1743`; no GUI interaction was possible through that route.

3. Existing logged-in CDP route:
   - Found existing Chrome remote-debugging session at `127.0.0.1:9222` with Google Ads pages already open for campaign `23802638621`.
   - Opened disposable read-only Google Ads tabs through that existing profile.
   - Used the Google Ads date range selector only, then clicked the date-picker dialog Apply control scoped to the date picker.
   - Result: custom range readback passed.

4. Local export/API/config search:
   - Searched repo evidence plus `~/Downloads`, `~/Desktop`, and `~/Documents` for likely Google Ads exports.
   - Checked local Google Ads API/config availability.
   - Result: no existing post-May-6 export found; `gcloud` exists, but no usable `google-ads.yaml`, Google Ads CLI, or Python `google.ads.googleads` package was available.

## Date Range

Google Ads UI timezone: `(GMT-07:00) North American Pacific Time`.

Exact UI range used: custom `2026-05-06` through `2026-05-09`. The UI displayed the range as `2026 May 6-9` and stated that the data viewed was from `2026-05-06` to `2026-05-09`.

## Campaign Metrics

Campaign status and controls remained visible as:

- Status: `Enabled / Eligible`
- Type: `Shopping`
- Budget: `US$20.00/day`
- Campaign settings link visible, not opened

Custom-range metrics:

| Metric | Readback |
|---|---:|
| Clicks | `1` |
| Impressions | `58` |
| CTR | `1.72%` |
| Average CPC | `US$0.02` |
| Cost | `US$0.02` |
| Conversions | `0.00` |
| Cost / conversion | `US$0.00` |
| Conversion value | `0.00` |

## Product Groups

| Product group | Max CPC/status | Impressions | Clicks | Cost | Avg CPC |
|---|---:|---:|---:|---:|---:|
| All products | `-` | `58` | `1` | `US$0.02` | `US$0.02` |
| `us_test_ready / daddy_me` | `US$0.04` | `14` | `0` | `US$0.00` | `-` |
| `us_test_ready / family_matching` | `US$0.04` | `7` | `0` | `US$0.00` | `-` |
| `us_test_ready / mommy_me` | `US$0.04` | `19` | `1` | `US$0.02` | `US$0.02` |
| `us_test_ready / pajamas` | `US$0.04` | `0` | `0` | `US$0.00` | `-` |
| `us_test_ready / swimsuits` | `US$0.04` | `18` | `0` | `US$0.00` | `-` |
| Everything else in All products | `Excluded` | `0` | `0` | `US$0.00` | `-` |

Product group scope still matched the guardrail posture: included child product groups at `US$0.04`, and Everything else in All products excluded.

## Search Terms

Search terms custom range loaded `19` visible rows. The visible rows all showed `0` clicks, `US$0.00` cost, and `0.00` conversions. Examples:

| Search term | Impressions | Clicks | Cost |
|---|---:|---:|---:|
| `baby and me dresses` | `1` | `0` | `US$0.00` |
| `clothes to wear for family photo shoot` | `3` | `0` | `US$0.00` |
| `family matching outfits for photoshoot` | `5` | `0` | `US$0.00` |
| `matching family beach outfits` | `1` | `0` | `US$0.00` |
| `matching family vacation outfits` | `1` | `0` | `US$0.00` |

Residual: the campaign-level `1` click did not appear in the visible search-term rows captured. A full export was not downloaded.

## No-Write Proof

- No campaign/account Save or Apply control was clicked.
- The only `Apply` clicked in Google Ads was scoped in script to the date range dialog (`aria-label` date range selector), which is a read-only reporting control.
- No Enable, Pause, Upload, Edit, budget, bid, product-group, feed-label, product-scope, conversion-goal, Merchant, Shopify, Pinterest, sign-in, account-switch, permission, CAPTCHA, or credential action was taken.
- Disposable CDP tabs were closed after capture; final CDP page check showed only the pre-existing Ads pages remained.
- No export download was triggered after the custom readback passed, avoiding an unnecessary browser download outside this lane path.

## Evidence

- Summary JSON: `summary.json`
- Read-only CDP helper: `cdp_ads_readonly.py`
- Campaign custom range: `raw/05_after_readonly_date_apply.json`, `raw/05_after_readonly_date_apply.txt`, `raw/05_after_readonly_date_apply.png`
- Product groups custom range: `raw/05_productgroups_after_readonly_date_apply.json`, `raw/05_productgroups_after_readonly_date_apply.txt`, `raw/05_productgroups_after_readonly_date_apply.png`
- Search terms custom range: `raw/05_searchterms_after_readonly_date_apply.json`, `raw/05_searchterms_after_readonly_date_apply.txt`, `raw/05_searchterms_after_readonly_date_apply.png`
- Attempt log: `raw/custom_date_attempt.log`

## Residual Risks

- Search-term capture was visible-table readback, not a full downloaded export.
- Product-level custom-date capture was not completed; a route attempt landed on the product custom-label breakdown and remained all-time, so it is not used as custom-date evidence.
- Google Ads still showed the ad-blocker warning, but the relevant campaign, product-group, and search-term tables rendered and were captured.

## Next Unblock Action

Parent should update `PROB-2026-05-08-STANDARD-SHOPPING-LIVE-METRICS-READBACK` to reflect `CUSTOM_RANGE_READBACK_PASSED_NO_ADS_WRITES`. Before any live Standard Shopping decision, use this custom-range readback plus the existing all-time readback; any pause, budget, bid, status, product-group, product-scope, feed-label, or conversion-goal action still needs fresh exact owner approval.
