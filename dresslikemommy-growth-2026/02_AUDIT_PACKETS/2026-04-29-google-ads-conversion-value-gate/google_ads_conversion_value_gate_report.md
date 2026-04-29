# Google Ads Purchase Conversion-Value Gate

Generated: 2026-04-29T06:08:41

## Decision

`PASS_PURCHASE_CONVERSION_VALUE_TRACKING_VERIFIED__NO_CURRENT_AD_ATTRIBUTION`

No Google Ads settings were changed. This packet is read-only evidence for whether Ads work can become actionable.

## Current Evidence

- Source page: `Conversion actions - dresslikemommy.com - Google Ads`
- Source URL: `https://ads.google.com/aw/conversions?ocid=220823493`
- Date range: `{'label': 'Last 7 days', 'start': 'Apr 22, 2026', 'end': 'Apr 28, 2026'}`
- Purchase goal active: `True`
- Purchase results in visible date range: `0.0`
- Primary account-level purchase actions: `1`
- Target action primary/account-level: `True`
- Target value setting proves dynamic values: `True`
- Target value evidence present: `True`
- Target raw historical conversions/value present: `True`
- Target raw last conversion date: `20260128`
- Target last received request: `2026-04-25T23:55:54.592430+00:00`
- Target recent request present: `True`
- Campaign enable allowed by this packet: `False`

## Target Action Settings

- Conversion name: `Google Shopping App Purchase`
- Action optimization: `Purchases, Primary action`
- Value: `Use different values. If there's no value, use 0.`
- Source: `Website`
- Count: `Every conversion`
- Click-through window: `90 days`

## Tracking Implementation Evidence

- Google Ads tag IDs: `["AW-853411529"]`
- Conversion send_to IDs: `["AW-853411529/14hzCOifhogBEMmN-JYD", "AW-853411529/25RNCJnowY8YEMmN-JYD", "AW-853411529/7Bv_COKfhogBEMmN-JYD", "AW-853411529/BcjoCNyfhogBEMmN-JYD", "AW-853411529/FDPVCJvnwY8YEMmN-JYD", "AW-853411529/F_APCJ_owY8YEMmN-JYD", "AW-853411529/LeL6CMiLmYcBEMmN-JYD", "AW-853411529/UbkpCN-fhogBEMmN-JYD", "AW-853411529/ditQCJzowY8YEMmN-JYD", "AW-853411529/el1ECO6fhogBEMmN-JYD", "AW-853411529/gGYoCJ7nwY8YEMmN-JYD", "AW-853411529/xayVCOWfhogBEMmN-JYD", "AW-853411529/zDt5COufhogBEMmN-JYD"]`
- GA4 measurement IDs: `["G-N4EQNK0MMB"]`
- Manual snippet default value zero: `True`

## Purchase Conversion Actions

| Conversion action | Source | Optimization | Included in account goals | Raw last conversion | Raw all conv. | Raw all conv. value |
| --- | --- | --- | --- | --- | ---: | ---: |
| Google Shopping App Purchase | Website | Primary | True | 20260128 | 5.0 | 193.9 |
| Purchases from google Adwords | Website | Secondary | False | 20260128 | 1284.0 | 100091.33 |
| Purchases from google analytics data | Website (Google Analytics (UA)) | Secondary | False | -- | 494.0 | 26863.31 |
| dresslikemommy.com - GA4 (web) purchase | Website (Google Analytics (GA4)) | Secondary | False | 20260128 | 16.541798 | 1300.122373636 |

## Blockers


## Advisories

- Visible Purchase results are 0 for the captured Google Ads date range. That is attributed Ads activity, not tag-fire proof, and can be expected while campaigns are paused.
- Google Ads default manual snippets show value 0.0 and blank transaction_id placeholders; do not paste those snippets into the theme. Runtime purchase tracking should stay with Shopify Google & YouTube.

## Gate Rule

The tracking gate passes when the Purchase goal is active, exactly one primary account-level purchase action is present, the target action has value evidence, and the target action has a recent received request. Visible Purchase results are treated as attributed Ads results, not the sole tracking-health signal. This packet never enables campaigns.
