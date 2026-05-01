# Brand Search Quality Cleanup Report

Date: 2026-04-30

Campaign: `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`

Campaign ID: `23805046526`

## Decision

`BRAND_SEARCH_QUALITY_CLEANUP_COMPLETE_STILL_PAUSED_AWAITING_EXPLICIT_ENABLE_APPROVAL`

No campaign was enabled. No budget was increased. No PMax or Remarketing work was performed.

Exact approval phrase still required before enabling Brand Search:

`APPROVE ENABLE BRAND SEARCH AT $1.00/DAY NOW`

## Owner-Approved Paused Edits Applied

1. Added one new responsive search ad to `Brand - Exact`.
2. Added one new responsive search ad to `Brand - Phrase`.
3. Added campaign URL suffix:
   `utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}&utm_matchtype={matchtype}`
4. Added four campaign-level callout assets:
   - `Official Store`
   - `Family Matching`
   - `Mommy And Me`
   - `Daddy And Me`
5. Accepted / attached the campaign-level assets that Google created through the RSA asset flow. The asset readback now shows `18` assets in scope, including eligible account-level sitelinks, callouts, and a structured snippet plus campaign-level assets.

## RSA Readback

Before cleanup, the campaign had `2` responsive search ads.

After cleanup, the campaign has `4` responsive search ads:

- Existing `Brand - Exact` RSA: paused because the campaign/ad is paused.
- Existing `Brand - Phrase` RSA: paused because the campaign/ad is paused.
- New `Brand - Exact` RSA:
  - Headline preview: `Dress Like Mommy Official | Official DressLikeMommy | Dress Like Mommy Store +12 more`
  - Status readback: `Not eligible - Campaign is paused`
  - Ad strength readback: `Pending`
- New `Brand - Phrase` RSA:
  - Headline preview: `Dress Like Mommy Official | Shop Dress Like Mommy | Mommy And Me Dresses +12 more`
  - Status readback: `Not eligible - Campaign is paused`
  - Ad strength readback: `Pending`

The two new ads are unavailable only because the parent campaign is paused. This is expected.

## Assets Readback

The final assets page readback shows:

- `18` assets in current view scope.
- Account-level callouts already present:
  - `Quality Fabrics`
  - `200+ Styles`
- New campaign-level callouts created at 2026-04-30 5:19:22 PM Google Ads account time:
  - `Official Store`
  - `Family Matching`
  - `Mommy And Me`
  - `Daddy And Me`
- Existing eligible account-level sitelinks with descriptions:
  - `New Arrivals`
  - `Best Sellers`
  - `Matching Swimsuits`
  - `Matching Dresses`
  - `Family Sets`
- Existing eligible structured snippet:
  - `Types: Dresses, Swimsuits, T-Shirts, Pajamas, Sweaters, Sets`

An additional structured snippet was attempted, but the Google Ads header selector would not commit a valid header in this session. I cancelled that form without saving a broken asset.

## URL Suffix Readback

Campaign URL options now read:

- Summary: `Using URL tracking options`
- Final URL suffix:
  `utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}&utm_matchtype={matchtype}`

## Brand List Enforcement

Not applied.

Reason:

- The live Google Ads Brand settings panel says: `Turn on AI Max in your campaign to use brand inclusions and exclusions`.
- AI Max remains intentionally off for this Brand Search campaign.
- Turning on AI Max would expand matching/asset behavior and would conflict with the controlled brand-protection posture.

Decision:

`BRAND_LIST_ENFORCEMENT_BLOCKED_BY_AI_MAX_REQUIREMENT`

Use exact/phrase brand keywords, negatives, low CPC cap, presence-only location, and search-term monitoring as the current brand-protection controls.

## Negative Keyword Audit

No negative keywords were removed.

The source negative set has:

- `253` total campaign negatives
- `190` phrase negatives
- `63` exact negatives
- `0` broad negatives
- `0` evidence-supported prune candidates

Important correction:

- Exact negatives such as `[free]`, `[amazon]`, `[review]`, and `[reviews]` do not block queries like `dress like mommy free shipping`, `dress like mommy amazon`, or `dress like mommy reviews`.
- The phrase negatives containing `free` are specific freebie/non-buyer patterns, such as `free pattern`, `free matching`, `free outfits`, `free clothes`, `free shipping only`, and `free sample`.

Decision:

`NEGATIVE_PRUNING_NOT_APPLIED_NO_SAFE_PRUNE_CANDIDATES`

Removing protections without search-term evidence would reduce safety, not improve ROI.

## Final Gate Status

Brand Search remains:

- Status: `Paused`
- Budget: `$1.00/day`
- Bid strategy: `Maximize clicks`
- Max CPC cap: `0.20`
- Location option: `Presence`
- Network: Google Search Network only
- AI Max: off
- Automatically created assets: off
- Broad match keywords: off
- Ads: `4` RSAs
- Assets: `18` visible assets in scope
- Cost: `$0.00`
- Clicks: `0`
- Impressions: `0`

## Evidence

Key files:

- Final ads readback: `raw/brand_final_ads_readback.txt`
- Final assets readback: `raw/brand_final_assets_readback.txt`
- Final change history readback: `raw/brand_final_change_history_readback.txt`
- URL suffix readback: `raw/brand_url_suffix_confirm_opened.json`
- Brand list blocker: `raw/brand_list_panel_open_attempt.txt`
- Negative audit: `raw/brand_negative_pruning_audit.json`
- Screenshots: `screenshots/`

