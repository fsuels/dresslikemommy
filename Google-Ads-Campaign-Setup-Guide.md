# DressLikeMommy.com - Google Ads Current Setup Guide

Updated: April 29, 2026
Google Ads account: `399-097-6848`
Merchant Center account: `124884876`

## Current Answer For The Shopping Draft

Use this exact answer for the browser AI prompt:

```text
Maximize clicks, budget $25/day
```

Then keep the campaign `PAUSED`. If Google Ads exposes a max CPC bid limit for Maximize clicks, set the first cap to `$0.25`. Raise to `$0.35` only if the campaign has too little eligible traffic after 72 hours. Do not enable spend until the operator explicitly says to enable.

## Do Not Use The Old All-Products Plan

The current clean Shopping cohort is not all products.

- Verified paid cohort: `780` offer rows across `81` Shopify product listings.
- Required product filters: `custom_label_4 = us_test_ready` and `custom_label_0 = paid_eligible`.
- Exclude all international rows, all unknown-margin rows, all fix-before-paid rows, and anything Limited, Not approved, out of stock, or not in the exact clean cohort.
- Root files `supplemental-feed-pilot.csv` and `supplemental-feed.tsv` are legacy apparel-attribute files only. Do not upload them for paid labels.
- Actual clean-label upload proof: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-merchant-clean-label-upload/upload_matched_full_clean_labels_with_age_group.txt`.

Live Merchant Center readback on April 29, 2026 confirmed the sampled US/en paid offer has:

```text
custom_label_0 = paid_eligible
custom_label_1 = margin_medium
custom_label_2 = mommy_me
custom_label_3 = aov_medium
custom_label_4 = us_test_ready
```

## Launch Rules

- Build new campaigns paused first.
- Do not enable, restart, or change live spend without explicit operator approval.
- Use Google Search only for Search campaigns. Uncheck Search Partners and Display.
- Use United States and English only for the first paid test.
- Use the Shopify Google & YouTube app purchase action only: `Google Shopping App Purchase`.
- Do not paste Google Ads manual conversion snippets into the theme.
- Do not claim free shipping or free returns in ad copy unless a current policy/checkout proof packet explicitly supports that claim.

## Campaign 1: Search - Brand

Purpose: defend brand demand and capture the highest-intent traffic at the lowest risk.

### Settings

| Setting | Value |
| --- | --- |
| Campaign name | `Search - Brand` |
| Objective | Sales |
| Campaign type | Search |
| Networks | Google Search only; no Search Partners; no Display |
| Location | United States |
| Language | English |
| Budget | `$10/day` |
| Bidding | Maximize conversion value, no target ROAS |
| Fallback bidding | Maximize clicks with `$0.50` max CPC if Google blocks value bidding for low data |
| Status | Paused |

### Ad Group 1: Brand - Exact

```text
[dress like mommy]
[dresslikemommy]
[dresslikemommy.com]
[dress like mommy store]
[dress like mommy shop]
[dlm dresses]
[dress like mommy outfits]
[dress like mommy matching]
```

### Ad Group 2: Brand - Phrase

```text
"dress like mommy"
"dresslikemommy"
"dress like mommy store"
"dress like mommy shop"
```

### Responsive Search Ad

Final URL: `https://www.dresslikemommy.com`
Display path: `matching/outfits`

Pin headline position 1:

```text
Dress Like Mommy Official
```

Other headlines:

```text
Mommy and Me Outfits
Mother Daughter Dresses
Family Matching Outfits
Matching Dresses and Sets
Shop New Matching Styles
Matching Family Clothes
Cute Mommy and Me Looks
Shop Dress Like Mommy
Matching Outfits for Kids
30-Day Return Window
Secure Checkout
Mom and Daughter Dresses
Matching Swimwear
New Styles Added Weekly
```

Descriptions:

```text
Shop mommy and me dresses, family outfits, pajamas and swimwear for matching moments.
Find matching looks for moms, daughters, dads and kids. New styles added weekly.
Dress Like Mommy helps families match for photos, vacations, birthdays and everyday memories.
Browse curated matching outfits with secure checkout and a 30-day return window.
```

## Campaign 2: Standard Shopping Clean Subset

Purpose: test only the feed rows that passed margin, inventory, PDP, Merchant Center, and custom-label gates.

### Settings

| Setting | Value |
| --- | --- |
| Campaign name | `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` |
| Campaign type | Shopping |
| Subtype | Standard Shopping |
| Merchant Center | `124884876` |
| Country | United States |
| Budget | `$25/day` |
| Bidding | Maximize clicks |
| Max CPC cap | `$0.25` if available |
| Campaign priority | Medium |
| Status | Paused |

### Inventory Filter

Use both filters together:

```text
custom_label_4 = us_test_ready
custom_label_0 = paid_eligible
```

### Product Group Order

1. `custom_label_4 = us_test_ready`
2. `custom_label_0 = paid_eligible`
3. `custom_label_2` product family
4. `custom_label_1` margin tier
5. `custom_label_3` AOV tier

Exclude everything outside the included subdivision.

Current expected family counts:

| Family | Offer rows |
| --- | ---: |
| `swimsuits` | 345 |
| `mommy_me` | 214 |
| `family_matching` | 103 |
| `daddy_me` | 89 |
| `pajamas` | 29 |

## Campaigns To Hold

Do not launch these yet:

- Non-brand Search: hold until Search Console query/page exports prove commercial opportunity.
- Performance Max: hold until Standard Shopping has stable conversion volume and feed/landing-page proof.
- Remarketing: hold until policy-limited products and dedupe evidence are fully clean.
- Display, Dynamic Search Ads, broad Search, or international campaigns: excluded from this first test.

## Shared Assets

### Sitelinks

| Sitelink | URL |
| --- | --- |
| Mommy & Me | `https://www.dresslikemommy.com/collections/mommy-and-me` |
| Family Matching | `https://www.dresslikemommy.com/collections/family-sets` |
| Swimsuits | `https://www.dresslikemommy.com/collections/swimsuits` |
| Pajamas | `https://www.dresslikemommy.com/collections/pajamas` |
| New Arrivals | `https://www.dresslikemommy.com/collections/new-matching-outfits` |

### Callouts

```text
Matching Family Styles
New Styles Weekly
30-Day Return Window
Secure Checkout
Mommy and Me Looks
Family Photo Ready
```

### Structured Snippet

Header: `Types`

```text
Dresses, Swimsuits, Pajamas, Shirts, Sets, Family Outfits
```

### Negative Keyword List

Create or verify shared list: `Master Negatives - DLM`

Import: `negative-keywords-import.txt`

Apply to:

- `Search - Brand`
- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Any future Search campaign before it is enabled

## Pre-Enable Checklist

Before enabling spend, every item must be true:

- Brand Search and Shopping campaigns are paused and reviewed.
- Search networks are Google Search only.
- Location is United States only.
- Language is English.
- Shopping campaign includes only `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible`.
- `Master Negatives - DLM` is applied.
- Brand RSA has no unsupported shipping/free-return claims.
- `Google Shopping App Purchase` is the single primary purchase conversion action.
- Purchase value setting is `Use different values. If there's no value, use 0.`
- Merchant Center live readback still shows `paid_eligible` and `us_test_ready`.
- No old paused/removed campaigns are restarted.
- Operator has explicitly approved the final live budget and enable action.

## First 7 Days After Enable

- Review search terms every day for the first 3 days, then twice weekly.
- Add irrelevant terms to `Master Negatives - DLM`.
- If Shopping spends with no add-to-cart signal after 100 clicks, lower CPC cap or pause weak product groups.
- If ROAS is below `6.67` after meaningful spend, pause the weak family/product group.
- If spend is capped and ROAS is above `6.67`, raise Shopping budget by 20 percent increments only.
- Do not switch to Target ROAS until Shopping has stable conversion volume.
