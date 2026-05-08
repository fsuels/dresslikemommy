# Localization, Shipping, And Landing Page QA

Generated: 2026-05-07

Scope: read-only local/public QA for international paid-growth landing readiness. No Shopify Admin edits, theme publishes, ad/feed changes, translation edits, or checkout payment steps were performed.

## Decision

- `US` remains the only live-safe paid market from this lane.
- `GB`, `CA`, and `AU` are safe for paused English-first campaign infrastructure, but live spend still needs action-time checkout, tracking, and feed/readback gates.
- Broader international markets should stay draft/research only until the visible shipping/policy copy is repaired and country-specific checkout/currency/duties QA passes.
- The biggest blocker is not route availability. The biggest blocker is that public shipping pages still say the store ships only to `United States`, `Canada`, `United Kingdom`, and `Australia`, while Admin/country selectors expose many more markets.

## Safe English-First Pages

Public checks returned `200` for these English paid landing/policy URLs:

| URL | Status | Use |
|---|---:|---|
| `/collections/mother-daughter-matching-dresses` | 200 | Primary Mommy & Me / mother-daughter Search landing page |
| `/collections/matching-outfits` | 200 | Broad family matching / matching outfits |
| `/collections/matching-family-vacation-outfits` | 200 | Vacation / resort / trip intent |
| `/collections/family-pajamas` | 200 | Pajamas / seasonal family matching |
| `/collections/family-swimsuits` | 200 | Swim / beach / resort intent |
| `/collections/daddy-and-me` | 200 | Daddy & Me intent |
| `/policies/shipping-policy` | 200 | Shipping policy |
| `/policies/refund-policy` | 200 | Refund policy |

Footer/support URL spot-checks also returned `200` for the actual live menu targets:

- `/pages/shipping-info`
- `/pages/return-policy`
- `/pages/faqs`
- `/pages/track-your-order`
- `/pages/contact-us`

## Localized Landing Checks

Targeted public route checks for `/collections/mother-daughter-matching-dresses`:

| Locale route | Status | HTML lang | Title signal | Notes |
|---|---:|---|---|---|
| `/fr/...` | 200 | `fr` | `Maman et moi Robes | Mère fille` | Route works; needs full human/local QA before local-language ads |
| `/de/...` | 200 | `de` | `Mama und ich Kleider | Mutter Tochter` | Route works; saw localized shipping-options term, no `$100+`/free-shipping threshold hit in this sample |
| `/da/...` | 200 | `da` | `Mommy and Me Kjoler | Moder Datter` | Route works but title is mixed English/Danish |
| `/es/...` | 200 | `es` | `Mamá y yo Vestidos | Madre e hija` | Route works; saw localized shipping-options term |
| `/nl/...` | 200 | `nl` | `Mama en ik Jurken | Moeder Dochter` | Route works |
| `/sv/...` | 200 | `sv` | `Mamma och jag Klänningar | Mamma Dotter` | Route works |
| `/it/...` | 200 | `it` | `Mamma e Me Abiti | Madre Figlia` | Route works |
| `/pl/...` | 200 | `pl` | `Mama i ja Sukienki | Mama Córka` | Route works |
| `/cs/...` | 200 | `cs` | `Šaty pro mámu a já | matka dcera` | Route works; copy quality should be reviewed |
| `/el/...` | 200 | `el` | `Φορέματα Mommy and Me | Μητέρα Κόρη` | Route works but title is mixed Greek/English |
| `/ro/...` | 200 | `ro` | `Rochii Mami și Eu | Mama Fiica` | Route works |
| `/pt-br/...` | 404 | n/a | n/a | Portuguese route did not resolve |
| `/pt` | 500 | n/a | n/a | Portuguese generic route errored |
| `/pt-BR`, `/pt-PT`, `/pt-pt` | 404 | n/a | n/a | No usable Portugal/Brazil route found in this public check |

Previous local claim cleanup is present in target locale files: `free_shipping_label`, `faster_shipping_prefix`, and `free_shipping_all_orders` now use checkout-availability wording for the checked target locales. It still has not been published, and policy/page content remains Admin-managed/live.

## Shipping And Checkout Evidence

Existing previous packet evidence:

- `country-admin-checkout/checkout_shipping_rate_validation.json` live-probed `US`, `GB`, `CA`, and `AU`.
- All four returned:
  - `Standard Delivery (10 - 14 Days) 0.00 USD`
  - `Express Delivery (7 - 11 Days) 12.99 USD`
- `country-admin-checkout/shipping_admin_readback.json` shows a `Rest of world` shipping zone with the same Standard/Express methods.
- `country-admin-checkout/locales_admin_readback.json` shows published locales: `ar, cs, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, nl, no, pl, pt-BR, ro, ru, sv`.

Fresh no-payment anonymous cart shipping-rate probe:

| Country | Result |
|---|---|
| `CH` | Rates returned: Standard `0.00 USD`; Express `12.99 USD` |
| `DK` | Rates returned: Standard `0.00 USD`; Express `12.99 USD` |
| `DE` | Rates returned: Standard `0.00 USD`; Express `12.99 USD` |
| `SE` | Rates returned: Standard `0.00 USD`; Express `12.99 USD` |
| `FR` | Rates returned: Standard `0.00 USD`; Express `12.99 USD` |
| `BE` | Rates returned: Standard `0.00 USD`; Express `12.99 USD` |
| `PL` | Rates returned: Standard `0.00 USD`; Express `12.99 USD` |
| `CZ` | Rates returned: Standard `0.00 USD`; Express `12.99 USD` |
| `GR` | Rates returned: Standard `0.00 USD`; Express `12.99 USD` |
| `NL` | First probe returned `422` because the test postal code was invalid for Netherlands |
| `ES` | First probe returned `422` because Shopify requested a province |
| `IT` | First probe returned `422` because Shopify requested a province |
| `RO` | First probe returned `422` because Shopify requested a county |
| `PT` | First probe returned `422` because Shopify requested a region |

I attempted one corrected-address retry for `NL`, `ES`, `IT`, `RO`, and `PT`, but Shopify storefront bot protection returned `429` at cart add. I stopped probing at that point. Treat those five countries as checkout-not-yet-proven, not as failed shipping countries.

## Public Policy And Claim Gaps

Live `Shipping Policy` page:

- Says shipping is currently to `United States`, `Canada`, `United Kingdom`, and `Australia`.
- Says shoppers should contact support if their country is not listed.
- Says free standard shipping on all orders.
- Includes customs/duties disclosure for international orders.

Live `/pages/shipping-info`:

- Says "we ship matching family outfits to families worldwide" near the top.
- But its "Where We Ship" list again only names `United States`, `Canada`, `United Kingdom`, and `Australia`.
- Says free standard shipping on every order.
- Gives delivery estimates only for `US`, `CA`, `GB`, and `AU`.
- Includes customs/duties disclosure.

Live `Terms of Service`:

- Says shipping is to `United States`, `Canada`, `United Kingdom`, and `Australia`.
- Says all prices are in `USD` unless otherwise noted.
- Says shipping/taxes are calculated at checkout.

Live `Refund Policy`:

- Gives 30-day return/exchange window.
- Says return shipping is the customer's responsibility unless damaged/defective.
- Says swimwear and intimates are non-returnable.

Paid-readiness interpretation:

- `GB`, `CA`, and `AU` are aligned with visible shipping policy.
- `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `GR`, and `PT` are not aligned with visible shipping policy despite country selectors/Admin shipping signals.
- Free standard shipping appears true for probed countries, but country-specific delivery windows, duties expectations, and local currency display still need final QA before spend.

## Country Readiness Tiers

### Tier 0: Live-Safe Now

- `US`

Reason: existing paid-market gate is US-only, English pages are live, and the active paid feed/campaign scope is US.

### Tier 1: Paused English-First Infrastructure Safe

- `GB`
- `CA`
- `AU`

Reason: English-first pages work, policy pages explicitly list these countries, and prior no-payment checkout probes returned Standard/Express rates. Do not enable spend until final action-time readbacks confirm tracking, feed/catalog, currency/checkout, and economics.

### Tier 2: Draft-Only, Promising After Policy Cleanup

- `CH`
- `DK`
- `DE`
- `SE`
- `FR`
- `BE`
- `PL`
- `CZ`
- `GR`

Reason: fresh no-payment checkout rates returned for these countries, and localized routes exist for the relevant languages checked. Blocker: visible policy and Shipping Info copy still imply these countries are not standard ship-to destinations. Use paused/draft planning only until policy/landing copy is repaired and rechecked.

### Tier 3: Checkout Address QA Still Needed

- `NL`
- `ES`
- `IT`
- `RO`

Reason: localized routes returned `200`, but the first shipping probe needed country-specific postal/province/county details, and the corrected retry hit `429` before readback. These are not rejected; they need slower browser/manual checkout-rate QA.

### Tier 4: Hold

- `PT` / Portugal and Portuguese routes
- Arabic/Hebrew/Japanese/Korean markets
- Any market using `ar`, `he`, `ja`, or `ko` paid traffic

Reason: Portuguese public route checks returned `404` or `500`; Admin shows `pt-BR` published but the usable public route was not found. Arabic/Hebrew/Japanese/Korean are already designated extra-QA markets and should wait for full language/layout/RTL or script QA, policy QA, and checkout proof.

## Next Safe Actions

1. Repair visible shipping/policy copy before EU/CH/DK paid spend:
   - either narrow the public market promise to the actually launched markets, or update policy/Shipping Info/Terms with a country-specific "available at checkout" posture that matches Admin shipping and country selectors.
   - include delivery-window caveats for broader international destinations.
   - keep customs/duties disclosure prominent.

2. Run slow browser checkout QA for `NL`, `ES`, `IT`, `RO`, and `PT` with valid local address/province fields after bot protection cools down.

3. Recheck Portuguese route configuration before any Portugal/Brazil copy or campaign work.

4. For Google Ads international Search, use:
   - English-only paused build for `GB`, `CA`, `AU`.
   - Draft-only local-language packs for Tier 2 countries until policy and checkout gates pass.
   - No local-language ad text where the destination title/body is mixed-language or unreviewed.

## Commands And Files Used

Read files:

- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/GROWTH_NORTH_STAR.md`
- `ops/MEMORY_CONTINUITY_PROTOCOL.md`
- `ops/AGENT_COORDINATION.md`
- `ops/BROWSER_SUBAGENT_COORDINATION.md`
- `ops/GOOGLE_ADS_CONTINUITY.md`
- `ops/AGENT_WORKLOG.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-continuation/PAID_GROWTH_AI_ARMY_CONTINUATION_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-continuation/country-admin-checkout/*.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-continuation/country-admin-checkout/country_validation_matrix.csv`
- `locales/*.json` target-locale shipping-copy snippets
- `snippets/product-page-copy-map.liquid`
- `ops/scripts/validate_phase5_country_checkout_admin.py`

Commands/tools run:

- `sed` reads of sprint, continuity, coordination, and script files.
- `tail -n 260 ops/AGENT_WORKLOG.md`.
- `find dresslikemommy-growth-2026/02_AUDIT_PACKETS ...`.
- `jq` reads of prior country/admin/checkout artifacts.
- `rg` scans for shipping/free-shipping/duties policy and locale terms.
- `curl` public HTTP checks for core English collection and policy pages.
- Python `urllib` public checks for localized collection routes and no-payment anonymous cart shipping-rate lookup.

Guardrails preserved:

- No Shopify Admin writes.
- No translation edits.
- No theme publish.
- No Google Ads, Merchant Center, Pinterest, GA4/GTM, campaign, bid, budget, feed, product-scope, product-group, feed-label, conversion-goal, or live product-data changes.
- No payment, order submission, credential entry, login, CAPTCHA, or account-tab action.
