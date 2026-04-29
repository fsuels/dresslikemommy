# Google Shopping Campaign Gate Report

Generated: 2026-04-29T01:14:44

## Decision

`DO NOT CREATE OR ENABLE THE GOOGLE ADS SHOPPING CAMPAIGN YET.`

The local paid cohort is real and verified, but the live Merchant Center/Ads label gate is not passed.

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

- Gate: `BLOCKED_CLEAN_LABELS_NOT_VISIBLE`
- Evidence: `{"campaign_creation_allowed": false, "expected_custom_label_0": "paid_eligible", "expected_custom_label_4": "us_test_ready", "gate_status": "BLOCKED_CLEAN_LABELS_NOT_VISIBLE", "generated_at": "2026-04-29T01:13:48", "merchant_center_account": "124884876", "mode": "READ_ONLY_LIVE_MERCHANT_CENTER_CLEAN_LABEL_GATE", "notes": ["Read-only browser RPC check; no Merchant Center or Google Ads changes were made.", "Cookies and request headers were used only in memory and are not written to disk.", "Campaign creation stays blocked unless the sampled US/en offer shows paid_eligible and us_test_ready."], "observed_us_en_rows": [{"custom_label_0": "high", "custom_label_1": "set", "custom_label_2": "true", "custom_label_3": "summer", "custom_label_4": "0-25", "feed_label": "US", "language_code": "en", "last_updated_utc": "2026-04-28T18:06:19+00:00", "source_id": "10627623003", "source_name": "Shopify App API"}], "query_results": [{"body_excerpt": "{\"1\":[{\"1\":\"shopify_US_7107978395745_41493652963425\",\"2\":\"Mommy and Me Maxi Dresses - Blue | Dress Like Mommy Child 3-4 Years / Blue\",\"7\":\"1777438296\",\"8\":false,\"9\":\"https://encrypted-tbn0.gstatic.com/images?q\\u003dtbn:ANd9GcRT3oOvkr1K8XwCSdfDvlDiqSkcVbFymbQ8wep1V6VQsYwUWVzO\",\"10\":\"SAR_544866401\",\"11\":\"en\",\"12\":\"0\",\"15\":{\"2\":{\"1\":\"96000000\",\"2\":\"SAR\",\"3\":\"SAR\\u00a096.00\"}},\"16\":1,\"17\":3,\"25\":5,\"26\":4,\"27\":\"\",\"28\":\"\",\"29\":\"\",\"30\":\"\",\"31\":\"\",\"33\":1,\"37\":false,\"39\":[\"5158375858400780112\"],\"41\":2,\"43\":{\"1\":\"10627981726\",\"3\":\"Shopify App API\",\"5\":{\"2\":6},\"6\":14,\"7\":[0,1]},\"44\":{\"1\":[39]},\"46\":{\"2\":6},\"47\":\"0\",\"50\":{\"2\":2},\"54\":[0],\"85\":\"SAR_544866401|en|shopify_US_7107978395745_41493652963425|10627981726\",\"88\":[1,5,38],\"95\":{\"1\":\"0\",\"2\":\"SAR\",\"3\":\"SAR\\u00a00.00\"}},{\"1\":\"shopify_US_7107978395745_41493652963425\",\"2\":\"Mommy and Me Maxi Dresses - Blue | Dress Like Mommy Child 3-4 Years / Blue\",\"7\":\"1777438112\",\"8\":false,\"9\":\"https://encrypted-tbn0.gstatic.com/images?q\\u003dtbn:ANd9GcRT3oOvkr1K8XwCSdfDvlDiqSkcVbFymbQ8wep1V6VQsYwUWVzO\",\"10\":\"VND_544866401\",\"11\":\"en\",\"12\":\"0\",\"15\":{\"2\":{\"1\":\"669000000000\",\"2\":\"VND\",\"3\":\"\\u20ab669,000\"}},\"16\":1,\"17\":4,\"25\":6,\"26\":5,\"27\":\"\",\"28\":\"\",\"29\":\"\",\"30\":\"\",\"31\":\"\",\"33\":1,\"37\":false,\"39\":[\"418332734200255023\"],\"41\":2,\"43\":{\"1\":\"10627981744\",\"3\":\"Shopify App API\",\"5\":{\"2\":6},\"6\":14,\"7\":[0,1]},\"44\":{\"1\":[38]},\"46\":{\"2\":6},\"47\":\"0\",\"50\":{\"2\":2},\"54\":[0],\"85\":\"VND_544866401|en|shopify_US_7107978395745_41493652963425|10627981744\",\"88\":[1,5,38],\"95\":{\"1\":", "body_length": 40542, "contains_old_custom_label_0_high": true, "contains_old_custom_label_4_0_25": true, "contains_paid_eligible": false, "contains_us_test_ready": false, "parse_error": "", "query": "shopify_US_7107978395745_41493652963425", "row_count": 50, "rows": [{"cu`

## Correct Campaign Structure After Gate Passes

- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Type: Standard Shopping only, USA only, paused on creation.
- Do not use Performance Max, Search Partners, Display, international, or All Products.
- Include only `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible` after Ads picker/readback proves those labels exist.
- Product groups: `custom_label_4 > custom_label_0 > custom_label_2/product_type > proposed item group/listing/style`; use item IDs for reporting or exact exclusions, not tiny initial bids.
- Keep variant rows in Merchant Center for price, size, availability, and eligibility accuracy.

## Important Feed Note

Do not solve this by writing one Shopify product-level paid label onto every product listing. In this cohort, most paid listings mix eligible and excluded variants. Product-level writes would include variants the local clean-subset intentionally excluded.

## Next Action

Verify that the supplemental clean-label source is joined to the live `en/US` Shopping source used by target offers, then recheck an exact paid offer until Merchant Center or the Ads picker shows `paid_eligible` and `us_test_ready`. Only then create the paused Standard Shopping campaign.
