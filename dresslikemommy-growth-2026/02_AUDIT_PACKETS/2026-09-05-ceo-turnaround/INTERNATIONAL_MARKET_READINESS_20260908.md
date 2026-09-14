# International market and locale readiness — September 8

Status: `LIVE_VERIFIED_CONFIGURATION__BUYER_ROUTE_AND_ECONOMICS_GATED`. Shopify structured read-only metadata; artifact captured at 18:31:44 UTC. Parent confirmed store `15571635` before this lane. No private shop, customer, order, product, supplier, billing, or shipping records were queried. Parent retains the primary Google integration task and canonical writes.

## Current configuration

Three schema-validated queries returned **21 published locales**, English primary; **6 markets, all ACTIVE**; **68 country-membership rows / 65 distinct country codes**; and **1 global web presence with 21 language-root URLs**. All outer and nested pagination is complete. Market names describe configuration, not geographic guarantees: “Eurozone” includes countries using DKK, CZK, RON, GBP and other currencies.

| Country candidate | Published locale | Configured country currency | ACTIVE market membership | Configured language root |
|---|---|---|---|---|
| Denmark | da | DKK | Eurozone | `/da/` |
| Germany | de | EUR | Eurozone | `/de/` |
| Czechia | cs | CZK | Eurozone | `/cs/` |
| Romania | ro | RON | Eurozone | `/ro/` |
| Italy | it | EUR | Eurozone | `/it/` |
| Netherlands | nl | EUR | Eurozone | `/nl/` |
| Belgium | nl, fr | EUR | Eurozone | `/nl/`, `/fr/` |
| France | fr | EUR | Eurozone | `/fr/` |
| Spain | es | EUR | Eurozone | `/es/` |
| Greece | el | EUR | Eurozone | `/el/` |
| Canada | fr, en | CAD | Canada and International conditions | `/fr/`, `/` |
| United States | es, en | USD | United States | `/es/`, `/` |

Every listed currency is enabled in the returned country configuration. Roots are under `https://www.dresslikemommy.com`. They identify language, not selected country, verified product availability or checkout currency. The full current locale list is `ar, cs, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, nl, no, pl, pt-BR, ro, ru, sv`. The API maps locale `pt-BR` to **`/pt/`**, not `/pt-BR/`; do not derive URLs by blindly copying locale codes.

Other configured native-language pairs available for later qualification include Finland/fi/EUR, Poland/pl/PLN and Sweden/sv/SEK. Norway/no returns **EUR**, not NOK; report the configuration as read and verify the intended shopper experience before recommending Norway. The published Hindi, Japanese, Korean, Hebrew, Arabic and Brazilian-Portuguese locales do not establish corresponding country memberships or sales readiness; Brazil, India, Japan, South Korea and Israel are absent from these returned country conditions. No new country or language is recommended merely because a locale exists.

## Routes and evidence limitations

All six `Market.webPresences` connections returned empty; the one global web presence also returned no explicit associated markets. Shopify documents that a market without its own web presence is accessible on the primary domain through country selectors. This is consistent with shared language roots but does not prove the current selector, redirect, effective market priority or buyer journey. [Market web presence documentation](https://shopify.dev/docs/api/admin-graphql/2026-07/objects/MarketWebPresence)

Canada, Australia and United Kingdom occur in both dedicated-market and broader-market conditions. Effective market precedence/inheritance was not queried; these overlaps are not evidence of duplicate product feeds or a defect and authorize no pruning.

Required before paid launch: exact country selection; active/public/purchasable product and photo/title fit; supplier-clean native copy; presentment price and purchase currency; actual shipping/delivery terms and delivered costs; retained-order profitability; verified conversion deduplication; and current account, Merchant destination and spend gates. None is certified by this metadata read. Free SEO work can use actual language routes as source material, but indexing, rendered copy, product fit and demand still need their existing evidence. This lane does not release live feed or product changes.

## Existing product-route references for the other agents

These are saved source references, not a new product or rendered readback:

- Sunshine `7545279512673`: `https://www.dresslikemommy.com/products/sunshine-stripe-family-matching-tops`; saved `sunshine_product_detail_current.json` and `sunshine_stripe_current_offer.json`.
- Rainbow `7229023846497`: handle `vibrant-rainbow-maxi-dress-set-for-mom-and-daughter-colorful-summer-matching-outfits`; saved `current_sales_checkpoint_20260908.json` and `rainbow_title_plan.json`.
- Mermaid `7109117280353`: handle `chic-pink-mermaid-scales-tankini-set-for-mother-and-daughter`; saved `current_sales_checkpoint_20260908.json`.

Appending these handles to a language root is only a candidate destination until the exact localized product route is read back. The paid agent can qualify DK/DE/CZ/RO/IT/NL using this configuration; the SEO agent can evaluate DA/DK, NL/NL+BE, EL/GR, ES/US, and IT/IT without treating country-language pairs as measured demand.

## Evidence and validation

- `international_market_locale_readback_20260908.json` preserves the returned allowed fields, pagination, counts and limits.
- `international_market_locale_readback_20260908.graphql` contains the three read-only operations, with no mutation or denied `appInstallations` field.
- Current schema discovery and Shopify structured documentation search passed. Connector validation passed for all 3 operations; live queries returned no errors or denied fields. Bundled skill validation of the complete 3-operation artifact passed at revision 2.
- The initial Homebrew Node attempt failed on missing `libsimdjson.29.dylib`; the bundled Node documentation-search script then failed to fetch. The permitted Shopify structured documentation connector succeeded; no account/authentication retry or runtime modification was performed.
- Local validation checks counts, uniqueness, pagination, target pairs, file whitespace and absence of stored private addresses. No browser, CUA, checkout, shipping, market, source, translation, or external write occurred.

Single next action for this lane: qualify the six selected European product/country combinations against existing product, route and delivered-cost evidence. Continue in the existing paid/SEO agents while root resolves the Google integration. No new market or translation expansion is needed to begin that work.
