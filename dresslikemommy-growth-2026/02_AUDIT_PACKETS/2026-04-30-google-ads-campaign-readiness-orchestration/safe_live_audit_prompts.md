# Safe Live Audit Prompts

Use these prompts with any browser/GUI agent that can access Google Ads. Audit only unless a later controller prompt explicitly authorizes a paused-draft safety patch.

## Universal Prompt

```text
STOP. Audit only. Do not enable anything.

Owner says these campaigns have never started or must be paused. Verify, do not assume.

Open Google Ads and report for each campaign:
- Status
- Campaign ID
- Campaign type
- Budget
- Bid strategy
- Networks
- Location targeting
- Location options
- Language
- Conversion goal
- URL options / final URL suffix
- Final URL expansion where applicable
- Cost today
- Cost since creation
- Clicks
- Impressions
- Conversions
- Conversion value
- ROAS
- CPA/CAC
- Whether it can spend right now

Open Change history from Apr 29, 2026 through Apr 30, 2026 and report:
- campaign created
- budget changed
- bid strategy changed
- status changed
- conversion goal changed
- product/listing/audience changes
- policy/ad changes
- who changed it
- old value
- new value
- timestamp

Do not change anything.
Do not enable anything.
Do not apply recommendations.
Output exact screenshots/exports.
```

## Campaigns

```text
DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429
DLM_US_STANDARD_SHOPPING_TEST_PAID_READY
PMax: Shopping ads (United States)
PMax: USA Google Shopping T-Shirts
Remarketing - Cart Abandoners & Checkout Starters
```

## Extra Fields By Campaign

Brand Search:
- ad groups, keywords, match types, negatives, RSAs, assets, final URLs, Search Partners, Display Network, brand-only controls.

Standard Shopping:
- Merchant Center ID, feed label, campaign priority, inventory filter, product groups, Everything else status, product count, item IDs/export, Search Partners setting if exposed.

PMax campaigns:
- linked Merchant Center, product eligibility, asset groups, listing groups, product filters, included item IDs, search themes, audience signals, brand exclusions, final URL expansion, URL exclusions.

Remarketing:
- policy diagnostics, ad copy, audience source/size/duration/definition, purchaser exclusions, optimized targeting, frequency controls, content exclusions, final URLs, consent/CMP implications.
