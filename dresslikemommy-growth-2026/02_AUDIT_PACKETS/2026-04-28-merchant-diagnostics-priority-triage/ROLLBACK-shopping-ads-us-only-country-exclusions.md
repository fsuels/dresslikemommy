# Rollback: Shopping Ads US-Only Country Exclusions

Date: 2026-04-28 23:12:02 EDT

Scope:
- Intended live change is a new, separate Merchant Center supplemental source using `shopping_ads_us_only_country_exclusions_UPLOAD_APPROVED.txt`.
- The source should only set `shopping_ads_excluded_country` for Shopify-style item IDs.
- It must not replace `supplemental_feed_pilot.txt`.
- It must not include or alter `custom_label_4` or `age_group`.

Preferred rollback:
1. In Merchant Center, open Product sources / Data sources.
2. Remove or disable the newly created supplemental source for Shopping ads US-only country exclusions.
3. Confirm `supplemental_feed_pilot.txt` still exists and still reports clean processing.
4. Recheck Needs attention after the next Merchant Center refresh.

Do not rely on this packet to clear `shopping_ads_excluded_country` by blank upload unless Merchant Center confirms blank supplemental values clear the attribute. Removing the separate source is the safer rollback.
