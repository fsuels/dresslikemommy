# Shopify international inventory — Merchant 513542500

Confidence: H for the readbacks below. Snapshot: **before root corrections**, collected 2026-09-09 16:43–16:50 UTC. Read-only; zero external mutations. Root owns live Merchant/Shopify corrections and canonical continuity.

Raw evidence, validated queries, timestamps and pagination receipts: [market_inventory.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/market_inventory.json).

## Verified coverage and correction candidate

- Shopify identity: Dress Like Mommy, Shop15571635, primary domain `https://www.dresslikemommy.com`.
- Complete ACTIVE-product traversal: **240 unique products, 4,945 variants**; five pages `50/50/50/50/40`, final `hasNextPage=false`, every variant count `EXACT`.
- **240/240** published to Google & YouTube `Publication21969633377 / App1780363` and Online Store `Publication55169925 / App580111`. Live labels were independently bound through schema-discovered deprecated `Publication.name/app`; all channel `catalog` fields returned null.
- **238/240** included and published in each explicit United States, Eurozone and International market catalog. The same two products below are absent in all three. Exact-ID `includedProducts` and `products` queries independently returned empty in every catalog.
- All 48 variants of these two products returned `availableForSale=true`; both products are ACTIVE, `requiresSellingPlan=false`, and have ordinary apparel/audience/color tags without an observed hold marker. Exact-ID searches found no worklog/problem/listing explanation. **The exclusion reason is UNKNOWN.**
- Root's separate Google-feedback scan identifies the same two IDs as lacking feedback. This is correlation; ingestion cause has not been proven.

| Product ID | Variants | Google + Online Store | All 3 explicit market catalogs |
|---|---:|---|---|
| 7109517770849 | 27 | Yes | No |
| 7227374534753 | 21 | Yes | No |

Exact excluded product identities:

- `7109517770849`: Mother & Daughter Vibrant Two-Piece Swimsuit Set with Flowing Skirt Matching Family Swimwear Collection; available variant prices USD16.99/19.99.
- `7227374534753`: Matching Mommy & Me Tiered Smocked Dresses – Elegant Puff Sleeve Dress Set; available variant prices USD22.99/27.99.

Exact market catalog/publication targets, all ACTIVE and `autoPublish=true`:

| Market | Catalog ID | Publication ID | Price list |
|---|---|---|---|
| United States | 6881083489 | 77106053217 | null |
| Eurozone | 6880723041 | 77105660001 | null |
| International | 910622817 | 77105823841 | 14023753825; USD; 0 fixed prices; parent decrease 0% |

All six markets are type `REGION`. No B2B market was returned. `priceInclusions` is null on all six; this does not establish tax/duty treatment. These reads do not prove why exclusions exist. Root and the independent reviewer own the correction decision and fresh before/after verification.

**Independent review update — publication correction HOLD:** the standards reviewer reports 43/48 failing GTIN checksums across these two products, with the other five checksum-passing values still lacking manufacturer proof, plus six supplier-hosted image references in the swimsuit body. Root owns that separate product-data evidence and remediation. ACTIVE/available/published flags do not establish Merchant readiness. Contain those defects before widening catalog inclusion.

## Markets, languages and shipping

**6 ACTIVE markets; 68 memberships; 65 unique country codes.** AU/CA overlap International with their standalone markets; GB overlaps Eurozone with its standalone market.

| Market | Handle | Countries | Base currency | Local currencies | Explicit catalog coverage |
|---|---|---:|---|---|---|
| Australia | australia | 1 | AUD | Off | No explicit catalog |
| Canada | canada | 1 | CAD | Off | No explicit catalog |
| Eurozone | eu | 43 | EUR | On | 238/240 |
| International | international | 21 | USD | On | 238/240 |
| United Kingdom | united-kingdom | 1 | GBP | Off | No explicit catalog |
| United States | us | 1 | USD | Off | 238/240 |

The primary domain's `MarketWebPresence259915873` has English plus **20 alternate published locales**, with 21 root URLs. Every market-specific web-presence connection is empty. The shared primary presence is verified through `shop.primaryDomain.marketWebPresence`; empty per-market connections do not mean that localized routes are absent. Published locales: ar, cs, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, nl, no, pl, pt-BR, ro, ru, sv. Portuguese locale `pt-BR` uses public root `/pt/`. Rendered locale/country checkout was NOT RUN.

Enabled presentment currencies (**20**): AUD, BSD, CAD, CHF, CZK, DKK, EUR, FJD, GBP, ISK, KYD, NZD, PLN, RON, RSD, SEK, USD, WST, XCD, XPF. Country currency values in the matrix are actual Shopify region readbacks; NO/RU returned EUR and MX returned USD. Submitted-offer, landing and checkout currency parity remains unverified.

Shipping is one **General profile10664050785**, with one location group and two complete zones:

| Zone | Countries | Standard | Priority |
|---|---|---|---|
| Countries Epacket | AU, CA, FR, GB, IL, NO, RU, SA, UA, US | Free; active; no conditions | USD12.99; active; weight 0–5 lb inclusive |
| Rest of world | Rest-of-world flag | Free; active; no conditions | USD12.99; active; weight 0–5 lb inclusive |

All 65 active-region countries are covered by configured General rates. `shop.shipsToCountries` enumerates 237 shipping destinations; it is **not** the active market count or proof that those 237 countries are checkout-ready. No additional profile was returned.

The retrieved shipping policy states processing in 1–3 business days, with an additional 1–2 days possible at high volume; it points buyers to checkout for delivery estimates. No fixed numeric transit estimate is given. Returns allow requests within 30 days of delivery, customer-paid return shipping except damaged/defective items, and exceptions including swimwear/intimates, Final Sale and gift cards. Policy bodies/contact details were not persisted. Merchant import parity and actual delivery promises remain root verification items.

## Country matrix

Exact ISO-code join to [Google's current Shopify-app sync table](https://support.google.com/merchants/answer/13693394?hl=en): **36 listed countries, 29 unlisted**. This is app-table availability, not proof of Merchant free-listing eligibility. English is globally published for every listed country; there are **63 exact supported published country/language pairs**. Missing optional local languages are opportunities, not universal blockers. `pt-BR` is not silently normalized to Google's listed `pt`; app normalization requires native readback.

All rows have a configured General shipping rate. Actual Google country selection, received offers and free-listing eligibility are UNKNOWN for every row in this subtask.

| Code | Active market handles | Shopify region currency | App table | Exact published languages in table |
|---|---|---|---|---|
| AD | eu | EUR | Unlisted | — |
| AI | international | XCD | Unlisted | — |
| AT | eu | EUR | Yes | de, en |
| AU | australia, international | AUD | Yes | en |
| AX | eu | EUR | Unlisted | — |
| BE | eu | EUR | Yes | en, fr, nl |
| BG | eu | EUR | Yes | en |
| BL | international | EUR | Unlisted | — |
| BM | international | USD | Unlisted | — |
| BS | international | BSD | Unlisted | — |
| CA | canada, international | CAD | Yes | en, fr |
| CH | eu | CHF | Yes | de, en, fr, it |
| CK | international | NZD | Unlisted | — |
| CY | eu | EUR | Yes | el, en |
| CZ | eu | CZK | Yes | cs, en |
| DE | eu | EUR | Yes | de, en |
| DK | eu | DKK | Yes | da, en |
| ES | eu | EUR | Yes | en, es |
| FI | eu | EUR | Yes | en, fi |
| FJ | international | FJD | Unlisted | — |
| FR | eu | EUR | Yes | en, fr |
| GB | eu, united-kingdom | GBP | Yes | en |
| GF | eu | EUR | Unlisted | — |
| GL | international | DKK | Unlisted | — |
| GP | eu | EUR | Unlisted | — |
| GR | eu | EUR | Yes | el, en |
| HR | eu | EUR | Yes | en |
| IE | eu | EUR | Yes | en |
| IS | eu | ISK | Unlisted | — |
| IT | eu | EUR | Yes | en, it |
| KY | international | KYD | Unlisted | — |
| LT | eu | EUR | Yes | en |
| LU | eu | EUR | Yes | de, en, fr |
| LV | eu | EUR | Yes | en |
| MC | eu | EUR | Unlisted | — |
| ME | eu | EUR | Unlisted | — |
| MF | international | EUR | Unlisted | — |
| MQ | eu | EUR | Unlisted | — |
| MT | eu | EUR | Yes | en |
| MX | international | USD | Yes | en, es |
| NL | eu | EUR | Yes | en, nl |
| NO | eu | EUR | Yes | en, no |
| NZ | international | NZD | Yes | en |
| PL | eu | PLN | Yes | en, pl |
| PM | international | EUR | Unlisted | — |
| PT | eu | EUR | Yes | en |
| RE | eu | EUR | Unlisted | — |
| RO | eu | RON | Yes | en, ro |
| RS | eu | RSD | Yes | en |
| RU | eu | EUR | Yes | en, ru |
| SE | eu | SEK | Yes | en, sv |
| SI | eu | EUR | Yes | en |
| SK | eu | EUR | Yes | en |
| SM | eu | EUR | Unlisted | — |
| SV | international | USD | Yes | en, es |
| TC | international | USD | Unlisted | — |
| TF | eu | EUR | Unlisted | — |
| TV | international | AUD | Unlisted | — |
| UM | international | USD | Unlisted | — |
| US | us | USD | Yes | en, es |
| VG | international | USD | Unlisted | — |
| WF | international | XPF | Unlisted | — |
| WS | international | WST | Unlisted | — |
| XK | eu | EUR | Unlisted | — |
| YT | eu | EUR | Unlisted | — |

## Verification and remaining work

- VERIFIED: Shopify schema discovery; every executed operation validated; coverage also validated using the installed skill script and bundled Node. Complete products, markets/regions/catalogs/web presences, channels, shipping zones/rates and excluded-product variants.
- Query-size recovery: initial market query cost1017 exceeded the per-query limit1000; reduced pagination sizes, revalidated, and obtained all rows. This was not an exhausted account quota.
- System Node failed with the known missing `libsimdjson.29.dylib`; bundled Node worked. Skill documentation fetch failed; structured Shopify documentation search succeeded. No auth or policy bypass.
- NOT RUN: Merchant source-country/offer eligibility, actual country/variant checkout, real delivery capability, revenue or profit proof. The independent [standards review](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/standards_review.md) distinguishes app support from free-listing eligibility.
- No canonical files edited by this agent. Only `market_inventory.json` and `market_inventory.md` are owned here.

**Next action:** root and independent reviewer contain the identifier and source-image defects on the exact two excluded products, then assess the six catalog joins. This goes first because broader catalog inclusion would carry those defects into more destinations. Follow with Merchant ingestion and country/checkout readback; do not claim eligibility from Shopify publication alone.

Continuation: use the existing [owner-standard continuation prompt](/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md) and root's current anchor; this packet is evidence, not another command layer.
