# Google Shopping Campaign Gate Report

Generated: 2026-04-29T03:58:51

## Decision

`READY_FOR_PAUSED_CAMPAIGN_FILTER_BUILD__DO_NOT_SUBDIVIDE_BY_LABEL_1_2_3`

The local paid cohort is real and verified. Do not enable or restart Google Ads from this packet.

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
- Full label gate: `BLOCKED_FULL_LABEL_MISMATCH`
- Campaign filter creation allowed: `True`
- Label 1-3 subdivision allowed: `False`
- Observed US/en sample rows: `[{"custom_label_0": "paid_eligible", "custom_label_1": "set", "custom_label_2": "true", "custom_label_3": "summer", "custom_label_4": "us_test_ready", "feed_label": "US", "language_code": "en", "last_updated_utc": "2026-04-29T04:04:27+00:00", "source_id": "10627623003", "source_name": "Shopify App API"}]`
- Sample label mismatches: `[{"expected": "margin_medium", "label": "custom_label_1", "observed": "set"}, {"expected": "mommy_me", "label": "custom_label_2", "observed": "true"}, {"expected": "aov_medium", "label": "custom_label_3", "observed": "summer"}]`
- Evidence artifact: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-product-feed-plan-recheck/merchant_exact_label_readback_refresh_check.json`

## Post-Gate Google Ads Structure

Do not restart Google Ads yet. This is a dry-run structure for use only after the named gates pass.

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
- Product groups: use `custom_label_4 > custom_label_0` first. Add `custom_label_1..3` subdivisions only after the full-label gate passes; until then use item IDs, product type, or the local item-group plan for reporting/exclusions.
- Keep variant rows in Merchant Center for price, size, availability, and eligibility accuracy.

## Important Feed Note

Do not solve this by writing one Shopify product-level paid label onto every product listing. In this cohort, most paid listings mix eligible and excluded variants. Product-level writes would include variants the local clean-subset intentionally excluded.

## Next Action

If building the paused campaign now, restrict it to the two verified filters and avoid `custom_label_1..3` product-group subdivisions. The clean-label source or upstream Shopify label mapping still needs follow-up before those secondary labels are trusted.
