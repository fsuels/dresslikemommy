# Phase 5 Country Checkout/Admin Validation

Generated: 2026-05-07T14:12:25-04:00

## Decision

- Paid traffic remains US-only.
- No non-US country was added to the paid allowlist.
- Non-US paid expansion remains blocked until localization, shipping, returns, country conversion, and margin pass country by country.

## Admin Readback

- Markets read: 6 (Australia, Canada, Eurozone, International, United Kingdom, United States)
- Delivery profiles read: 1 (General profile)
- Published locales read: ar, cs, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, nl, no, pl, pt-BR, ro, ru, sv
- Policies read through Admin REST: 5 (Contact, Privacy policy, Refund policy, Shipping, Terms of service)

## Paid Gate Evidence

- Paid cohort rows: 780
- Paid cohort markets: {'US': 780}
- Non-US paid rows found: 0
- Country-exclusion upload rows: 7063
- Excluded country count: 42
- US exclusion rows found: 0
- Paid gate status: PASS_US_ONLY

## Live Checkout Probe

- Method: anonymous storefront cart shipping-rate lookup; no payment step and no order creation.
- Probe status: COMPLETE
- Probe blocker: none
- Countries with live rates in this packet: 3 non-US
- Countries blocked in this packet: 0 non-US

## Country Matrix

- Countries/regions in matrix: 118
- Non-US rows in matrix: 117
- Non-US active market rows: 116
- Full details: `country_validation_matrix.csv`

## Files

- `markets_admin_readback.json`
- `shipping_admin_readback.json`
- `locales_admin_readback.json`
- `policies_admin_readback.json`
- `paid_us_only_evidence.json`
- `checkout_shipping_rate_validation.json`
- `country_validation_matrix.csv`
- `summary.json`
