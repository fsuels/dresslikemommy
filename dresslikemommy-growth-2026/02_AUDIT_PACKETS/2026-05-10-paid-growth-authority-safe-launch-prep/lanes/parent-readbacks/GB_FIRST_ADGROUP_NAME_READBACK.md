# GB First Ad Group Name Readback

Date: 2026-05-10

Source evidence:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/raw/after-readbacks/gb_direct_campaign_readback/ads.json`

Result:

- Actual ad group string found: `Mommy & Me Dresses - Exact` -> `True`
- Stale local runbook string found in source readback: `Mommy & Me Dresses - Exact only` -> `False`

Interpretation:

The first-enable target ad group must be named exactly `Mommy & Me Dresses - Exact`. The older phrase `Mommy & Me Dresses - Exact only` was a local documentation error and is now a stop condition if seen in an action-time checklist instead of the live ad group name.

No Google Ads account write occurred in this readback.
