# Google Ads Purchase Conversion-Value Gate

Generated: 2026-04-29T04:30:15

## Decision

`BLOCKED_PURCHASE_CONVERSION_VALUE_NOT_RECORDING_RECENTLY`

No Google Ads settings were changed. This packet is read-only evidence for whether Ads work can become actionable.

## Current Evidence

- Source page: `Conversion actions - dresslikemommy.com - Google Ads`
- Source URL: `https://ads.google.com/aw/conversions?ocid=220823493`
- Date range: `{'end': '', 'label': '', 'start': ''}`
- Purchase goal active: `True`
- Purchase results in visible date range: `0.0`
- Primary account-level purchase actions: `1`
- Target action primary/account-level: `True`
- Target value setting proves dynamic values: `False`
- Target value evidence present: `True`
- Target raw historical conversions/value present: `True`
- Target raw last conversion date: `20260128`

## Target Action Settings

- Conversion name: ``
- Action optimization: ``
- Value: ``
- Source: ``
- Count: ``
- Click-through window: ``

## Purchase Conversion Actions

| Conversion action | Source | Optimization | Included in account goals | Raw last conversion | Raw all conv. | Raw all conv. value |
| --- | --- | --- | --- | --- | ---: | ---: |
| Google Shopping App Purchase | Website | Primary | True | 20260128 | 5.0 | 193.9 |
| Purchases from google Adwords | Website | Secondary | False | 20260128 | 1284.0 | 100091.33 |
| Purchases from google analytics data | Website (Google Analytics (UA)) | Secondary | False | -- | 494.0 | 26863.31 |
| dresslikemommy.com - GA4 (web) purchase | Website (Google Analytics (GA4)) | Secondary | False | 20260128 | 16.541798 | 1300.122373636 |

## Blockers

- Visible Purchase results are 0 for the current Google Ads date range.

## Gate Rule

The gate passes only when the Purchase goal is active, exactly one primary account-level purchase action is present, the target purchase action uses transaction-specific values, and current Google Ads evidence shows non-zero purchase results/value. Historical raw value is useful context but is not enough to restart or build actionable Ads work.
