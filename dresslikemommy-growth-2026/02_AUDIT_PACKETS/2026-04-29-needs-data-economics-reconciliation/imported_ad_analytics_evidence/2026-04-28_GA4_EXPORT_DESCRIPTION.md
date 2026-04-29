# 2026-04-28_GA4_EXPORT_DESCRIPTION

## Platform

GA4

## Store / property

dresslikemommy.com - GA4

## Scope

GA4 only. Read/export only. Do not visit Google Ads, Merchant Center, Search Console, Pinterest, or Shopify. Do not change anything.

## Current attached GA4 context

The active-tab GA4 Home page context provides only partial Home-card data:

- Last 7 days, 2026-04-20 to 2026-04-26:
  - Active users: 350
  - Event count: 3.2K
  - Key events: 398
  - Purchases: 4
- Last 7 days session default channel group:
  - Organic Search: 140 sessions
  - Direct: 123 sessions
  - Unassigned: 79 sessions
  - Organic Shopping: 26 sessions
  - Referral: 15 sessions
  - Organic Social: 0 sessions
- Last 7 days event card:
  - page_view: 1.1K
  - user_engagement: 741
  - session_start: 386
  - view_item: 335
  - first_visit: 346
  - scroll: 110
  - form_start: 84
- Last 90 days Pages and screens card, 2026-01-27 to 2026-04-26:
  - Mother Daughter Matching Dresses & Family Outfits | Dresslikemommy – Dress Like Mommy: 742 views
  - Mommy and Me Dresses | Family Matching Outfits: 508 views
  - 404 Not Found – Dress Like Mommy: 501 views

This is not enough to complete the required 30/90/365 ecommerce packet.

## Required GA4 exports to complete GA4_PACKET_v1

Export each report for:

- Last 30 days
- Last 90 days
- Last 365 days

Use exact GA4 date picker ranges shown by GA4. Avoid partial current-day data.

### 1. Ecommerce overview

Metrics:

- Total revenue
- Purchases
- Sessions
- Users
- Ecommerce conversion rate

Computed fields:

- AOV = Total revenue / Purchases
- Max CAC = AOV × 0.15

### 2. Revenue by source / medium

Dimension:

- Session source / medium

Metrics:

- Sessions
- Users
- Purchases
- Total revenue
- Ecommerce conversion rate

### 3. Revenue by campaign

Dimension:

- Session campaign

Metrics:

- Sessions
- Users
- Purchases
- Total revenue
- Ecommerce conversion rate

### 4. Revenue by country

Dimension:

- Country

Metrics:

- Sessions
- Users
- Purchases
- Total revenue
- Ecommerce conversion rate

### 5. Revenue by device

Dimension:

- Device category

Metrics:

- Sessions
- Users
- Purchases
- Total revenue
- Ecommerce conversion rate

### 6. Landing page performance

Dimension:

- Landing page + query string

Metrics:

- Sessions
- Purchases
- Total revenue
- Ecommerce conversion rate

### 7. Item performance

Dimensions:

- Item name
- Item ID

Metrics:

- Items viewed
- Items added to cart
- Items purchased
- Item revenue

### 8. Funnel event counts

Dimension:

- Event name

Filter:

- view_item
- add_to_cart
- begin_checkout
- purchase

Metric:

- Event count

### 9. Purchase tracking QA

Use Explore or Events inside GA4.

Filter:

- event_name = purchase

Dimensions / parameters:

- transaction_id
- currency

Metrics:

- Event count
- Total revenue
- Purchase revenue
- Event value if available

QA rules:

- Missing transaction_id on purchase = tracking concern.
- Missing value on purchase = tracking concern.
- Missing currency on purchase = tracking concern.
- Same transaction_id with event count greater than 1 = possible duplicate purchase tracking.
- Revenue attached to blank, direct, unassigned, or unknown campaign rows requires attribution review.

### 10. Google Ads link status

Stay inside GA4 only:

- Admin
- Product Links
- Google Ads Links

Capture whether a Google Ads link exists. Do not enter Google Ads.

## Suggested file names for exports

- `2026-04-28_GA4_overview_last30.csv`
- `2026-04-28_GA4_overview_last90.csv`
- `2026-04-28_GA4_overview_last365.csv`
- `2026-04-28_GA4_source_medium_last30.csv`
- `2026-04-28_GA4_source_medium_last90.csv`
- `2026-04-28_GA4_source_medium_last365.csv`
- `2026-04-28_GA4_campaign_last30.csv`
- `2026-04-28_GA4_campaign_last90.csv`
- `2026-04-28_GA4_campaign_last365.csv`
- `2026-04-28_GA4_country_last30.csv`
- `2026-04-28_GA4_country_last90.csv`
- `2026-04-28_GA4_country_last365.csv`
- `2026-04-28_GA4_device_last30.csv`
- `2026-04-28_GA4_device_last90.csv`
- `2026-04-28_GA4_device_last365.csv`
- `2026-04-28_GA4_landing_pages_last30.csv`
- `2026-04-28_GA4_landing_pages_last90.csv`
- `2026-04-28_GA4_landing_pages_last365.csv`
- `2026-04-28_GA4_items_last30.csv`
- `2026-04-28_GA4_items_last90.csv`
- `2026-04-28_GA4_items_last365.csv`
- `2026-04-28_GA4_events_last30.csv`
- `2026-04-28_GA4_events_last90.csv`
- `2026-04-28_GA4_events_last365.csv`
- `2026-04-28_GA4_purchase_params_QA.csv`
- `2026-04-28_GA4_google_ads_link_status.png`

## Completion standard

A complete packet must include exact numbers for all requested GA4 ecommerce metrics across Last 30, Last 90, and Last 365 days. It must not infer profitability without Shopify margin and cost data.
