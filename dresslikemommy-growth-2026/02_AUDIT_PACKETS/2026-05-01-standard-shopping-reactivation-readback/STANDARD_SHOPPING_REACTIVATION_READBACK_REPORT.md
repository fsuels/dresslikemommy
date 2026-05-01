# Standard Shopping Reactivation Readback Report

Decision: `DO_NOT_REACTIVATE_MERCHANT_CENTER_STILL_SHOWS_SUPPLIER_URL_MATCHES`

Campaign:
- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Campaign ID: `23802638621`

Owner directive:
- Keep the campaign paused until both Merchant Center and Google Ads live readbacks confirm no supplier/source URL exposure after refresh.
- Require fresh explicit owner approval before any re-enable.

## Readbacks

### Shopify live product data

Result: `PASS`

- Live Shopify products scanned: `803`
- Products with vendor URL tags: `0`
- Products with title/body/SEO/scanned-metafield vendor URL leaks: `0`
- Evidence: `shopify-live-rescan/dry_run_summary.json`

### Merchant Center clean paid-label readback

Result: `PASS_LABELS`

- `custom_label_0=paid_eligible` visible for the sample paid offer.
- `custom_label_4=us_test_ready` visible for the sample paid offer.
- Full expected labels matched for the sample paid offer.
- Evidence: `merchant-label-readback/merchant_exact_label_readback_refresh_check.json`

### Merchant Center supplier/source URL exposure readback

Result: `BLOCKED`

Live Merchant Center browser RPC still returned supplier-domain search matches:

- Query `1688.com`: `50` rows
- Query `detail.1688.com`: `50` rows
- Query `alibaba.com`: `0` rows
- Query `aliexpress.com`: `0` rows

The exact paid-cohort sample offers from products that previously had supplier URL tags returned no supplier-domain hits, but the broader Merchant Center product index is still not clean. Several returned rows show older non-paid/non-US feed labels and old custom labels such as `custom_label_4=0-25`, indicating stale Merchant Center product data remains after Shopify cleanup.

Evidence: `merchant-vendor-url-readback/merchant_vendor_url_exposure_readback.json`

### Google Ads campaign table readback

Result: `PAUSED`

- Campaign table contains `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`.
- Campaign table contains `Paused`.
- Campaign table does not contain visible supplier domains.
- Evidence: `google-ads-status-readback/google_ads_campaigns_table_readback.json`

## Decision

Do not reactivate yet.

The required reactivation condition is not satisfied because Merchant Center still returns supplier/source URL matches. Wait for Merchant Center / Google product data refresh, then re-run the live supplier-domain readback. Only after Merchant Center and Google Ads readbacks are clean should the operator be asked for fresh explicit approval to re-enable.
