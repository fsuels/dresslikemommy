# Google Shopping Campaign Gate Report

Generated: 2026-04-29T05:32:48

## Decision

`DRY_RUN_STRUCTURE_ONLY_NOT_ACTIONABLE__PURCHASE_VALUE_BLOCKED`

The local paid cohort is real and verified. Do not enable or restart Google Ads from this packet.
Ads dry-run actionable allowed: `False`

## Verified Local Cohort

- Paid offer rows: `780`
- Shopify product listings: `81`
- Proposed role/item groups: `131`
- Reviewed offer rows: `7324`
- Excluded/fix-before-paid offer rows: `6544`
- Paid listings with mixed eligible/excluded variants: `80`
- Product feed structure counts: `{'A_TRUE_VARIANT_GROUP': 39, 'B_FAMILY_STYLE_DIFFERENT_PHYSICAL_PRODUCTS': 42}`
- Role counts: `{'father': 89, 'child': 227, 'unclear': 35, 'mother': 429}`
- Product family counts: `{'daddy_me': 89, 'family_matching': 103, 'mommy_me': 214, 'pajamas': 29, 'swimsuits': 345}`

## Live Merchant Label Gate

- Gate: `PASS_CAMPAIGN_FILTER_LABELS_VISIBLE`
- Campaign filter gate: `PASS_CAMPAIGN_FILTER_LABELS_VISIBLE`
- Full label gate: `PASS_ALL_EXPECTED_LABELS_VISIBLE`
- Campaign filter creation allowed: `True`
- Label 1-3 subdivision allowed: `True`
- Supplemental label join allowed: `True`
- Observed US/en sample rows: `[{"custom_label_0": "paid_eligible", "custom_label_1": "margin_medium", "custom_label_2": "mommy_me", "custom_label_3": "aov_medium", "custom_label_4": "us_test_ready", "feed_label": "US", "language_code": "en", "last_updated_utc": "2026-04-29T08:25:05+00:00", "source_id": "10627623003", "source_name": "Shopify App API"}]`
- Sample label mismatches: `[]`
- Evidence artifact: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-merchant-clean-label-emergency-recheck/merchant_exact_label_readback_refresh_check.json`

## Purchase Conversion-Value Gate

- Gate: `BLOCKED_PURCHASE_CONVERSION_VALUE_NOT_RECORDING_RECENTLY`
- Gate passed: `False`
- Purchase goal active: `True`
- Purchase results in captured range: `0.0`
- Target action: `Google Shopping App Purchase`
- Target primary/account-level: `True`
- Target raw last conversion date: `20260128`
- Evidence artifact: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-ads-conversion-value-gate/google_ads_conversion_value_gate_summary.json`

## Ads Dry-Run Actionability

- Actionable allowed: `False`
- Blockers: `["Visible Purchase results are 0 for the current Google Ads date range."]`

## Post-Gate Google Ads Structure

Do not restart Google Ads yet. This is a dry-run structure for use only after the named gates pass. It is not actionable while `ads_dry_run_actionable_allowed` is false.

| Campaign | Use only after | Required exclusions |
| --- | --- | --- |
| Brand Search — USA | Purchase conversion tracking records value correctly. | Exclude if tracking is not recording. |
| Standard Shopping — USA eligible products | Merchant Center and product-margin gates pass. | Exclude UNKNOWN_MARGIN, FIX_BEFORE_PAID, limited, and not-approved products. |
| PMax — USA eligible products | Only after feed, conversion, landing-page, and product-label gates pass. | URL expansion off unless an approved landing-page map exists. |
| Non-brand Search | Search Console query/page exports prove commercial opportunity. | Exclude pages not READY_FOR_PAID. |
| Remarketing | Policy-limited ads are fixed and tracking is deduped. | Do not use current limited ads. |

## Standard Shopping Build Details

- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Type: Standard Shopping only, USA only, paused on creation if later approved.
- Do not use All Products, international inventory, unknown-margin products, fix-before-paid products, Limited products, or Not approved products.
- Include only `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible` after Ads picker/readback proves those labels exist.
- Product groups: use `custom_label_4 > custom_label_0` first. Add `custom_label_1..3` subdivisions only after the full-label gate passes and Ads dry-run actionability is true; until then use item IDs, product type, or the local item-group plan for reporting/exclusions.
- Keep variant rows in Merchant Center for price, size, availability, and eligibility accuracy.

## Important Feed Note

Do not solve this by writing one Shopify product-level paid label onto every product listing. In this cohort, most paid listings mix eligible and excluded variants. Product-level writes would include variants the local clean-subset intentionally excluded.

## Next Action

Do not build or restart Ads from this packet. Produce current purchase conversion-value proof with non-zero purchase results/value before the dry-run structure becomes actionable.
