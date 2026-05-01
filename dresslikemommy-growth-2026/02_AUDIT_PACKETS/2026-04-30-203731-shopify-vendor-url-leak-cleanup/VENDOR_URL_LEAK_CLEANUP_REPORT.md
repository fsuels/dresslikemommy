# Shopify Vendor URL Leak Cleanup Report

Status: `LIVE_SHOPIFY_VENDOR_URL_TAGS_REMOVED`

Why:
- Owner found an unacceptable supplier/source URL exposure risk while the Standard Shopping test was active and paused the campaign.
- Dress Like Mommy customer/feed-visible product data must only use `dresslikemommy.com` / Dress Like Mommy, never `1688.com`, Alibaba, AliExpress, or other supplier/source URLs.

Root cause:
- The canonical listing prompt previously instructed agents to put `VENDOR_URL` in Shopify tags.
- Shopify tags are product data and may be visible to downstream channels, feeds, exports, or apps. They are not a safe place for supplier/source evidence.

Actions:
- Updated `ops/prompts/shopify-listing-master-prompt.md` so vendor/source URLs are allowed only in local operator evidence files, not Shopify product data.
- Added `ops/scripts/audit_and_remove_vendor_url_leaks.py`.
- Added `ops/tests/test_vendor_url_leak_guard.py`.
- Ran a live Shopify audit across `803` products.
- Removed exact leaking vendor/source URL tags from `263` products.
- Re-ran live Shopify scans after cleanup.

Live Shopify result:
- Products scanned: `803`
- Products with vendor URL leaks after cleanup: `0`
- Products with bad vendor URL tags after cleanup: `0`
- Products with title/body/SEO/metafield vendor URL leaks after cleanup: `0`

Paid/feed artifact checks:
- `paid_cohort_exact_780_rows.csv`: `0` vendor URL rows
- `google_shopping_us_clean_subset_master.csv`: `0` vendor URL rows
- `upload_matched_full_clean_labels_with_age_group.csv`: `0` vendor URL rows

Evidence files:
- `vendor_url_leak_scan.csv`
- `post_cleanup_vendor_url_leak_scan.csv`
- `execution_summary.json`
- `final-rescan/vendor_url_leak_scan.csv`
- `final-rescan/dry_run_summary.json`

Campaign safety:
- The owner reported pausing `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`.
- Do not re-enable Standard Shopping until Merchant Center / Google Ads live readback confirms no supplier/source URL exposure and the owner gives fresh explicit approval.
