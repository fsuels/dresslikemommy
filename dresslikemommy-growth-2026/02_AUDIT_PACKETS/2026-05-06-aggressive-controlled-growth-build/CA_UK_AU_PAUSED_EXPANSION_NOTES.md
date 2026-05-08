# CA / UK / AU Paused Expansion Notes

Date: 2026-05-06

Scope: notes only. No international campaign was launched, enabled, uploaded, budgeted, or targeted.

## Recommendation

Prepare Canada, United Kingdom, and Australia as the first non-US English expansion markets, but keep them paused until the activation gates below are read back cleanly at action time.

## Why These Markets

- They are English-language markets, reducing immediate translation risk.
- They were already identified in prior storefront/shipping review as the clearest non-US shipping-supported markets.
- The owner has recent non-US demand signals, but Denmark and Switzerland should remain learning signals, not live paid targets, until shipping, duties, returns, currency, and localized checkout proof are stronger.

## Paused Campaign Shell Concept

Do not create live spend yet. If approved later, use separate paused shells by market rather than one mixed campaign:

- `DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED`
- `DLM_UK_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED`
- `DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED`

Recommended starting controls if later approved:

- Status: Paused at creation.
- Network: Google Search only.
- Language: English.
- Match types: Exact and phrase only.
- CPC ceiling: no higher than the US nonbrand rebuild cap unless market readback proves better economics.
- Conversion goals: read back first, then keep account-default purchase goals unless separately approved.
- Landing pages: English collection pages only.
- Product scope/feed/Merchant: unchanged unless separately approved.

## Activation Gates

Before enabling any CA / UK / AU spend, read back:

- Checkout can accept the destination country and local currency cleanly.
- Shipping rate, delivery estimate, duties/taxes, return policy, and swimwear return restrictions are clear.
- Top landing pages return `200` and do not show stale mixed-language product content.
- Google Ads location option is presence-only: people in or regularly in the included location.
- Campaign is not using Display Network, Search Partners, AI Max, or broad match unless separately approved.
- Purchase conversion remains primary and dynamic.
- Standard Shopping product scope, feed labels, product groups, budget, status, and conversion goals remain untouched.

## Country Priority

1. Canada: closest operationally, English first; French Canada only after French storefront QA.
2. United Kingdom: good English fit; delivery-time expectation and returns clarity are critical.
3. Australia: good English fit; longer delivery expectations may hurt conversion rate, so cap tightly.

## Blocked For Now

- No Denmark or Switzerland live paid traffic from this pass.
- No translated-language paid traffic from this pass.
- No Pinterest international spend from this pass.
- No PMax expansion from this pass.
