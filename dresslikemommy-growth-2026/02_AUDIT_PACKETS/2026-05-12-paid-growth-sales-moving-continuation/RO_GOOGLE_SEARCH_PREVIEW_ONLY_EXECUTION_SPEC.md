# RO Google Search Preview-Only Execution Spec

Date: `2026-05-12`
Status: `LOCAL_SPEC_ONLY__NO_GOOGLE_ADS_ACTION`

## Purpose

Narrow the remaining Google Search build lane to the next single-country action: `RO` preview only.

This file does not authorize Google Ads upload, preview, import, apply, campaign creation, budget/bid/status edit, or live spend. It exists so the next authenticated and approved Ads session can move quickly without re-uploading completed countries or stacking `PT`/`GR` behind unresolved `RO`.

## Source CSV

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/RO_intl_search_paused_draft_web_bulk.csv`

SHA256:

`b3e9eac7c59d06813c3c2b7089c4d46d21c6e92f0d0c5459eab71b5c73a43001`

## Row Shape

| Field | Value |
|---|---|
| Rows | `88` |
| Campaign | `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` |
| Action | `Add` only |
| Campaign status | `Paused` |
| Campaign type | `Search` |
| Network | `Google search` |
| Language | `en` |
| Location | `Romania` |
| Budget | `1.00` |
| Ad groups | `10`, all paused |
| Keyword rows | `30`, all paused |
| Negative rows | `37` |
| RSA/ad rows | `10`, all paused |
| Default max CPC | `0.10` |
| Unique final URLs | `5`, all `/ro/...?...country=RO` |

## Unique Final URLs

- `https://www.dresslikemommy.com/ro/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=RO`
- `https://www.dresslikemommy.com/ro/products/elegant-matching-family-outfits-light-blue-halter-dresses-casual-t-shirt-set-for-summer?country=RO`
- `https://www.dresslikemommy.com/ro/products/cute-matching-mom-and-daughter-cartoon-pajama-set-fun-and-cozy-sleepwear?country=RO`
- `https://www.dresslikemommy.com/ro/products/chic-pink-mermaid-scales-tankini-set-for-mother-and-daughter?country=RO`
- `https://www.dresslikemommy.com/ro/products/daddy-and-me-matching-floral-shirts-black-rose-print-short-sleeve-button-up-set?country=RO`

## Before Preview Readbacks Required

Run these immediately before any Google Ads upload/preview action:

1. Confirm current session has fresh exact owner approval naming `RO` and the preview/apply boundary.
2. Confirm `ops/AGENT_COORDINATION.md` has no active Google Ads international Search write lock owned by another agent.
3. Confirm no campaign named `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` exists.
4. Confirm no `RO_intl_search_paused_draft_web_bulk.csv` upload, preview, or apply job is in progress or stale-visible.
5. Confirm the source CSV still has exactly `88` rows, SHA256 `b3e9eac7c59d06813c3c2b7089c4d46d21c6e92f0d0c5459eab71b5c73a43001`, no IDs, and only `Action=Add`.
6. Confirm the preview/import surface is empty for `RO`; do not reuse any old preview.

## Preview Rule

Preview `RO` only.

Do not upload, preview, apply, or touch `PT`, `GR`, `FR`, `BE`, completed countries, US campaign `23827590655`, Standard Shopping, PMax, Merchant, Shopify product data, Pinterest, product scope, feed labels, product groups, conversion goals, budget increases, bid increases, or enablement.

## Clean Preview Criteria

Do not apply unless the fresh preview result is downloaded and validates:

- `88/88` rows accepted or `# OK`.
- `0` errors.
- `0` unexpected warnings that alter status, budget, bid, URL, network, product/feed/conversion scope, or campaign type.
- The preview belongs to the current `RO` upload, not a stale prior preview.

## Apply Criteria

Apply only after a clean `RO` preview and only if the current approval explicitly permits applying after clean preview.

After apply, read back:

- Campaign exists and is `Paused`.
- All ad groups, keywords, and ads are `Paused`.
- Campaign is Search only / Google Search network only.
- Location is Romania with presence-only behavior.
- Budget is unchanged from source.
- CPC is `0.10` and at or below `$0.20`.
- No campaign conversion-goal override.
- No product/feed/Merchant/Pinterest/Shopify/Standard Shopping/PMax changes.

## Stop Conditions

Stop and report instead of proceeding if:

- Fresh owner approval is missing or does not name `RO`.
- Any `RO` campaign already exists.
- Any `RO` upload/preview/apply is in progress or stale-visible.
- File picker or upload path is not controllable.
- Preview is not downloadable.
- Preview is not clean `88/88`.
- UI asks to enable, launch, change budget, change bids, alter conversion goals, or touch non-RO surfaces.
- Presence-only readback is not clean and no separate exact approval exists for a narrow repair.

## Current Decision

`RO` is preview-ready as a local file only. It is not live-ready, not native-language-ready, and not approved for platform action in this session.

Exact next unblock: authenticated Google Ads file-picker/session access plus fresh exact action-time owner approval for `RO` preview/apply boundary.
