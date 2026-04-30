# Google Ads Brand Search Paused Editor Import

Campaign: `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`
Mode: `PAUSED_ONLY`; do not enable live spend.

This packet is the safe Brand Search path when Google Ads web draft creation only exposes `Publish campaign`.
Import through Google Ads Editor, review the proposed changes, and post only if every campaign, ad group, keyword, and ad row remains paused.

The packet intentionally uses a unique campaign name so it cannot restore or mutate the removed legacy `Search - Brand` campaign.

Import order:

Google Ads Editor files:
1. `auto_import_safe_paused_core/01_campaign_settings.csv`
2. `auto_import_safe_paused_core/02_campaign_locations.csv`
3. `auto_import_safe_paused_core/03_ad_groups.csv`
4. `auto_import_safe_paused_core/04_keywords.csv`
5. Select the new campaign in Editor, open `Keywords & targeting > Keywords, Negative`, click `Make multiple changes`, choose `Use selected destinations` and `Add as campaign-level negative keywords`, then paste `auto_import_safe_paused_core/05_campaign_negative_keywords_editor_bulk_paste.tsv`.
6. `auto_import_safe_paused_core/06_responsive_search_ads.csv`

`auto_import_safe_paused_core/05_campaign_negative_keywords_reference.csv` is audit evidence only; use the TSV with Editor's campaign-negative bulk flow.

Google Ads web bulk-preview files:
- Preferred single-file preview: `web_bulk_preview_templates/00_brand_search_paused_combined_web_bulk.csv`
- Split-file fallback:
  1. `web_bulk_preview_templates/01_campaign_web_bulk.csv`
  2. `web_bulk_preview_templates/02_ad_groups_web_bulk.csv`
  3. `web_bulk_preview_templates/03_keywords_web_bulk.csv`
  4. `web_bulk_preview_templates/04_campaign_negative_keywords_web_bulk.csv`
  5. `web_bulk_preview_templates/05_responsive_search_ads_web_bulk.csv`

Required readback before posting/applying:
- Campaign status is `Paused`.
- Both ad groups are `Paused`.
- All keywords are `Paused`.
- Both responsive search ads are `Paused`.
- Networks show Google Search only; Search partners and Display are off.
- Location is United States only.
- Campaign-level negatives imported from `Master Negatives - DLM`.
- EU political ads is set to `No, does not have EU political ads`.

Do not enable the campaign until the final launch gate passes and the operator explicitly approves live spend.
