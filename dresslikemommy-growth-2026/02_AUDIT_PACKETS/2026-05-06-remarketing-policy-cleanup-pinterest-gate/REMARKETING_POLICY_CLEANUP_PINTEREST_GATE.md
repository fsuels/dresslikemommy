# Remarketing Policy Cleanup and Pinterest Gate

Date: 2026-05-06

Owner direction:

`Clean the remarketing policy issue first, then rerun the Pinterest login gate. After the nonbrand RSAs clear review, we can decide whether to enable that paused nonbrand rebuild with very tight spend controls.`

## Scope

Allowed:

- Read back Remarketing before editing.
- Remove or neutralize old paused policy-limited Remarketing ads if the UI allowed it.
- Keep Remarketing paused at `$1/day`.
- Rerun Pinterest Ads gate read-only.

Blocked:

- No Remarketing enablement.
- No budget increase.
- No audience changes.
- No conversion-goal changes.
- No Merchant Center, Shopify, feed, Standard Shopping, PMax, Brand Search, or nonbrand Search edits.
- No Pinterest campaign creation, spend, or credential entry.

## Google Ads Remarketing Cleanup

Campaign: `Remarketing - Cart Abandoners & Checkout Starters`

Campaign ID: `23609373008`

Pre-cleanup readback:

- Campaign status: Paused.
- Type: Display.
- Budget: `$1.00/day`.
- Date range: Apr 29-May 5, 2026.
- Spend: `$0.00`.
- Impressions: `0`.
- Conversions: `0.00`.
- Ads table showed `6` RDAs:
  - `5` old paused RDAs with `Policy (Clickbait), Campaign is paused`.
  - `1` generic warm RDA: `Dress Like Mommy Styles` / `Matching Family Styles From Dress Like Mommy` / `Shop matching looks for moms, dads, kids, and families.`

Cleanup action:

- Selected only the five old RDAs with:
  - `Complete Your Purchase Today`
  - `You Left Something Behind! Complete Your Dress Like Mommy Order Today`
  - `Policy (Clickbait), Campaign is paused`
- Confirmed Google's removal dialog: `Permanently remove 5 ads? Once an ad is removed, it can't be re-enabled.`
- Google confirmation readback: `5 ads removed`.

Post-cleanup readback:

- The five old clickbait-policy RDAs now read `Removed`.
- The clean generic warm RDA was not removed.
- Clean generic warm RDA still reads `Not eligible, Campaign is paused`, with no clickbait policy text visible on its row.
- Campaign remains paused.
- Budget remains `$1.00/day`.
- Spend remains `$0.00`.
- Impressions remain `0`.
- Conversions remain `0.00`.

Residual:

- Campaign row still showed `Most ads limited by policy` immediately after removal and after a short refresh/wait.
- Treat this as not clean enough to enable yet. It may be policy-status propagation lag, or Google may still be surfacing removed ad policy history in the campaign row.
- Future enablement requires another fresh readback where the active/non-removed ad path is clean and the campaign-level policy status has cleared.

## Pinterest Ads Gate

Account readback:

- Account: `Dress Like Mommy | Matching Family Outfits`.
- Domain: `dresslikemommy.com`.
- Advertiser ID visible in URL: `549756244483`.
- Browser was logged in successfully.

Campaign readback:

- Reporting page: Last 30 days.
- Conversion settings: `7/7`.
- Campaigns: `0 campaigns`.
- Currently serving: `0 currently being served`.
- Table spend: `$0.00`.
- No Pinterest campaign creation, edits, budgets, or spend were made.

Catalog readback:

- Catalog section: `Catalog_Retail`.
- Data source: Shopify / `3041760849210539103`.
- Merchant status: `Approved`.
- Visible note: `VMP under review`.
- Shopping ads eligibility text: `You're now an approved merchant... able to run shopping ad campaigns.`
- Product groups visible: `32` rows total.
- Visible product groups:
  - `Fall & Winter`: `223` products, last updated `4/28/2026`.
  - `Daddy & Me Shirts`: `276` products, last updated `4/26/2026`.
  - `Best Deals`: `1,002` products, last updated `5/5/2026`.
  - `Sundresses`: `302` products, last updated `4/28/2026`.
- Catalog health:
  - Successful uploads: `5.66k`, `99.86%` of total data source.
  - Failed to upload: `8`, `0.14%`.
  - Warnings: `152`, `2.68%`.
  - Ingestion status: completed.

Pinterest conversion events readback:

- Events overview source: `Api · Tag` for the main ecommerce events.
- PageVisit: `19,656`, last received `5/6/2026 06:53am (UTC)`.
- ViewCategory: `4,131`, last received `5/6/2026 05:06am (UTC)`.
- AddToCart: `679`, last received `5/6/2026 05:28am (UTC)`.
- InitiateCheckout: `118`, last received `5/6/2026 05:29am (UTC)`.
- Search: `40`, last received `5/2/2026 07:07am (UTC)`.
- Checkout: `23`, last received `5/6/2026 05:29am (UTC)`.
- AddPaymentInfo: `21`, last received `5/6/2026 05:29am (UTC)`.

Pinterest event-quality readback:

- Event quality page: `Event quality for dresslikemommy.com`.
- Updated: `5/4/2026`.
- Event source: Conversions API and Pinterest Tag.
- Date range checked: Last 14 days / Last 1 day.
- Event quality score: `Fair`.
- Top action items:
  - Improve `Product ID` in `Add Payment Info`.
  - Improve `Click ID` in `Checkout`.
  - Improve `Email` in `Add to Cart`.
- Event insights parameters to improve:
  - `Product ID` in `Add Payment Info`.
  - `Order Value` in `Add Payment Info`.
- Duplicate-event section showed `Event ID` in good health for at least `Page Visit` and `View Category` in the visible table.

## Decision

`REMARKETING_POLICY_ROWS_REMOVED_BUT_CAMPAIGN_POLICY_STATUS_NOT_CLEARED__PINTEREST_GATE_LOGGED_IN_CATALOG_APPROVED_TAG_AND_API_RECEIVING_EVENTS_EVENT_QUALITY_FAIR_NO_PINTEREST_SPEND`

## Next Gate

Do not enable Remarketing until the campaign-level policy status clears or a fresh readback proves only removed historical rows are causing the warning.

Do not launch Pinterest spend until event-quality issues for Checkout click ID and purchase/product/value parameters are improved or consciously accepted with a very small test budget.
