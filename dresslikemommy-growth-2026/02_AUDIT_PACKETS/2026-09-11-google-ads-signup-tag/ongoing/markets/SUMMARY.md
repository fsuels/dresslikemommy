Confidence: H for Shopify configuration and report completeness; M for diagnostic prioritization.

Fresh read-only Shopify captures on September 11, 2026 at **18:41:24–18:42:33 UTC** verify Dress Like Mommy, shop15571635, `dresslikemommy-com.myshopify.com`, USD accounting currency and America/New_York reporting time. There are **6 ACTIVE markets, 68 country memberships, 65 unique countries, 21 published locales and 20 enabled presentment currencies**. Every market, region and web-presence connection finished pagination.

| Market | ID | Memberships | Base currency |
|---|---:|---:|---|
| United States | 544735329 | 1 | USD |
| Canada | 22986326113 | 1 | CAD |
| United Kingdom | 22986260577 | 1 | GBP |
| Australia | 22986424417 | 1 | AUD |
| Eurozone | 544800865 | 43 | EUR |
| International | 544866401 | 21 | USD |

AU and CA also occur in International; GB also occurs in Eurozone. These are observed condition overlaps, not proven errors. The normalized inventory preserves them without counting countries twice. Country-specific currency settings are authoritative for QA: for example Norway is EUR, Mexico USD and Denmark DKK.

One shared web presence contains all 21 locale roots. **`pt-BR` uses `/pt/`**, not `/pt-br/`. Individual markets return no separate web presence; Shopify documents primary-domain country-selector fallback in that configuration. Published language settings do not prove translation quality or complete product coverage. [Shopify MarketWebPresence documentation](https://shopify.dev/docs/api/admin-graphql/2026-07/objects/MarketWebPresence).

The one additional aggregate query uses **June 13–September 10: 90 complete shop-local dates**. All 129 country rows reconcile to provider totals: 22,362 sessions, 439 sessions with cart additions, 142 reaching checkout and 35 completing checkout (**0.1565%**). The existing same-period sales report is reused with its source hash: 43 reported orders, USD3,190.41 net sales. Session checkouts and sales-report orders have different scopes; their difference does not prove a tracking failure.

US contributes 15,079 sessions and 20 completed-checkout sessions. Romania has 140 sessions/12 reaching checkout/0 completed; Netherlands128/10/0. These justify country-specific buyer-path diagnosis. Small samples do not establish paid winners. The 4,317 sessions without an exact current-active-country name match produced no completed checkout; source, device, automated-traffic and historical-market explanations remain unresolved.

**Next decision:** compare the exact live Google campaign locations and languages with this inventory, then qualify a narrow cohort. All Google country targeting—including US—Merchant approval, product sellability, real payment/purchase acceptance, paid CPA, ROAS and retained profit remain UNKNOWN. No external setting changed.

Use [market_readback.json](market_readback.json), [65-country inventory](active_country_inventory.csv), [68 memberships](market_country_assignments.csv), [locale roots](locale_routes.csv), [country funnel](country_funnel.csv) and the [1,365 derived QA candidates](country_locale_qa_matrix.csv). The latter is a test scope, not 1,365 passed tests. [Validation](VALIDATION.json) records531 local source/schema/pagination/arithmetic checks; it is not runtime or independent business verification. Continue through the existing [canonical prompt](../../../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md) and parent ongoing goal.
