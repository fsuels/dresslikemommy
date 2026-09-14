# All-market Google Ads build — September 14, 2026

**Status: prepared locally; live campaign creation and ad submission remain blocked by the unresolved Google identity/Save step and launch requirements. No new campaigns, ads, keywords, negative keywords, budgets or spend were submitted in this pass.**

The country and language build now accounts for **65 countries/territories**, **75 proposed country-language groups** and **21 published-language ad sets**. The language library contains **126 headlines, 63 descriptions, 42 exact research seeds and 95 narrow phrase-negative candidates**. Research seeds are not measured or launch-qualified keywords. The previous four US/AU/CA/GB product-specific drafts and completed18European candidate results remain preserved; this is their all-market coverage extension, not a replacement of their evidence.

Open [ADS_BY_LANGUAGE.md](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/current_campaign_repair/research/all_market_build_20260914/ADS_BY_LANGUAGE.md) to review the actual copy and negatives, or [MARKET_COVERAGE_REVIEW.csv](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/current_campaign_repair/research/all_market_build_20260914/MARKET_COVERAGE_REVIEW.csv) for the complete country list. The structured assembly is [ALL_MARKET_CAMPAIGN_BUILD.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/current_campaign_repair/research/all_market_build_20260914/ALL_MARKET_CAMPAIGN_BUILD.json). These are review files, not Ads Editor import files.

## Current account gap

| Item | Fresh account readback | Prepared correction |
|---|---|---|
| Campaign | One visible Performance Max campaign, Paused | Preserve it while repairing the existing copy; use qualified Search tests for retained CPC control |
| Geography | United States only; Presence or Interest | Presence within each selected country |
| Language | English selected | Matched language ads and verified localized destinations |
| Negatives | Empty campaign view; account summary None | Reviewed campaign-specific sewing-intent phrases |
| Automated text/URLs | Text customization and final URL expansion on | Existing exact repair plan turns both off pending saved readback |
| Merchant in this campaign | Not set up | Separate existing Merchant owner and exact product-link qualification; no blind connection |

The completed September7–13 report shows356impressions,5clicks,USD0.80cost and0conversions. These are the same totals already recorded for September11, not new spend since that earlier readback. The calculated average CPC isUSD0.16; PMax cannot enforce the retainedUSD0.15per-click control. Earlier channel evidence attributes the spend toYouTube, so Search negatives cannot be presented as savings against that cost.

The pending18copy changes/27values remain unsaved. The original editor was preserved; no repeat Save or authentication attempt was made. [ADS_TARGETING_LIVE_READBACK.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/current_campaign_repair/research/all_market_build_20260914/ADS_TARGETING_LIVE_READBACK.json) records what was and was not checked.

## Campaign strategy

Use one campaign per qualified country with separate language ad groups, a matching localized landing page and country-specific economics. The first paid test should select one qualifying product/keyword cohort; it should not spread the existing small budget across65countries or75groups. Country plans currently have null budgets, null native location IDs and no qualified initial keywords. They are not scheduled for automatic launch.

The retained control is ManualCPC at or belowUSD0.15, no upward bid adjustments, Search partners off, Display off, automated keyword/bid recommendations off, and AI Max/search expansion off for the initial candidate test. Google confirms AI Max search-term matching does not work with ManualCPC; this is an account-fit decision, not a claim that advanced automation is generally ineffective. [Google AI Max FAQ](https://support.google.com/google-ads/answer/15913066?hl=en).

Starting September2026, Search campaign language selection is being removed and language matching depends on the creative and landing page. PMax non-Search channels still use language settings, while Shopping is separate. Verify the actual account rollout and buyer experience instead of promising language isolation from a selector. [Google language targeting](https://support.google.com/google-ads/answer/1722078?hl=en).

Presence targeting reduces interest-only cross-border reach but cannot guarantee perfect geographic accuracy. Review actual country performance after launch. [Google location options](https://support.google.com/google-ads/answer/1722038?hl=en).

Keep Purchase as the business outcome; do not promote page views or carts merely to fill an empty conversion report. Before spending, verify the selected valued purchase, transaction deduplication, relevant consent, actual basket/fulfillment/fee/refund economics and exact authority. Retained-revenue ad capacity remains the lower ofR/6.5, R−actual variable costs−allocated overhead−30% ofR, and the exact authorized loss allowance. Unknown costs mean profit is unqualified.

## Negative keyword discipline

The current English repair candidate includes phrase negatives “sewing pattern”, “sewing patterns”, “how to sew”, and “sewing tutorial”. Localized equivalents are prepared for each language. The scope is finished-clothing purchase intent: do not block broad terms such as free, shipping, adult, cheap, pattern, floral, wedding or pajamas.

Negatives require explicit relevant language/grammar variants; they do not automatically translate or cover every synonym or singular/plural. Current Google documentation says case changes and misspellings are already handled. Accent variants can differ. Verify inherited shared lists and exact matched queries before applying changes. [Google negative keywords](https://support.google.com/google-ads/answer/2453972?hl=en).

The local conflict check protects candidate positive terms and realistic finished-apparel examples. It does not simulate Google matching or prove every native-language false positive is excluded. These are preventive candidates, with no claimed savings. [TARGETING_REPAIR_ADDENDUM.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/current_campaign_repair/research/all_market_build_20260914/TARGETING_REPAIR_ADDENDUM.json) extends the existing exact repair plan; no new live scope is granted by the file.

## Country and language coverage

The65country membership codes are unchanged from the prior source; the detailed language-group queue expands from23to75candidate groups. Market names are configuration labels, not shipping or consumer-demand proof. Country-language assignments below are strategy candidates: all markets returned empty individual web-presence connections, and the global21language roots do not establish effective country selection or checkout acceptance. [Shopify market web presence](https://shopify.dev/docs/api/admin-graphql/2026-07/objects/MarketWebPresence).

Arabic, Hebrew, Hindi, Japanese, Korean and Russian copy is prepared but not assigned to a launchable country cohort. Those speakers may later qualify within an existing allowed country; published languages do not justify inventing new country markets. Russia is accounted for as held because Google currently pauses ads to users there. [Google current regional notice](https://support.google.com/google-ads/answer/6149970?hl=en).

Portugal currently uses publishedpt-BR at/pt/and requires Portugal-specific adaptation. Norway is configuredEURand MexicoUSD; no NOK/MXN price promises are included. English alternatives in countries lacking a published native locale address English-comprehending shoppers only. Exact local copy, country currency, shipping, available variants and product routes remain launch checks.

| Country | Configured currency | Proposed language groups | Specific gap |
|---|---|---|---|
| Andorra (AD) | EUR | es, fr | Catalan is not a published locale; Spanish/French are research alternatives, not complete local-language coverage. |
| Anguilla (AI) | XCD | en | Country/product/route/cost qualification pending |
| Austria (AT) | EUR | de | Country/product/route/cost qualification pending |
| Australia (AU) | AUD | en | Country/product/route/cost qualification pending |
| Åland Islands (AX) | EUR | sv | Country/product/route/cost qualification pending |
| Belgium (BE) | EUR | fr, nl, de | Country/product/route/cost qualification pending |
| Bulgaria (BG) | EUR | en | Bulgarian is not published; English candidate is limited to comprehending shoppers. |
| St. Barthélemy (BL) | EUR | fr | Country/product/route/cost qualification pending |
| Bermuda (BM) | USD | en | Country/product/route/cost qualification pending |
| Bahamas (BS) | BSD | en | Country/product/route/cost qualification pending |
| Canada (CA) | CAD | en, fr | Country/product/route/cost qualification pending |
| Switzerland (CH) | CHF | de, fr, it | Country/product/route/cost qualification pending |
| Cook Islands (CK) | NZD | en | Country/product/route/cost qualification pending |
| Cyprus (CY) | EUR | el, en | Turkish is not published; no all-language Cyprus claim. |
| Czechia (CZ) | CZK | cs | Country/product/route/cost qualification pending |
| Germany (DE) | EUR | de | Country/product/route/cost qualification pending |
| Denmark (DK) | DKK | da | Country/product/route/cost qualification pending |
| Spain (ES) | EUR | es | Country/product/route/cost qualification pending |
| Finland (FI) | EUR | fi, sv | Country/product/route/cost qualification pending |
| Fiji (FJ) | FJD | en | Country/product/route/cost qualification pending |
| France (FR) | EUR | fr | Country/product/route/cost qualification pending |
| United Kingdom (GB) | GBP | en | Country/product/route/cost qualification pending |
| French Guiana (GF) | EUR | fr | Country/product/route/cost qualification pending |
| Greenland (GL) | DKK | da | Kalaallisut is not published; Danish candidate requires demand and buyer-route validation. |
| Guadeloupe (GP) | EUR | fr | Country/product/route/cost qualification pending |
| Greece (GR) | EUR | el | Country/product/route/cost qualification pending |
| Croatia (HR) | EUR | en | Croatian is not published; English candidate is limited to comprehending shoppers. |
| Ireland (IE) | EUR | en | Country/product/route/cost qualification pending |
| Iceland (IS) | ISK | en | Icelandic is not published; English candidate is limited to comprehending shoppers. |
| Italy (IT) | EUR | it | Country/product/route/cost qualification pending |
| Cayman Islands (KY) | KYD | en | Country/product/route/cost qualification pending |
| Lithuania (LT) | EUR | en | Lithuanian is not published; English candidate is limited to comprehending shoppers. |
| Luxembourg (LU) | EUR | fr, de | Luxembourgish is not published; French/German candidates do not cover every local language. |
| Latvia (LV) | EUR | en | Latvian is not published; English candidate is limited to comprehending shoppers. |
| Monaco (MC) | EUR | fr | Country/product/route/cost qualification pending |
| Montenegro (ME) | EUR | en | Montenegrin/Serbian localization is not established; English candidate is limited to comprehending shoppers. |
| St. Martin (MF) | EUR | fr | Country/product/route/cost qualification pending |
| Martinique (MQ) | EUR | fr | Country/product/route/cost qualification pending |
| Malta (MT) | EUR | en | Country/product/route/cost qualification pending |
| Mexico (MX) | USD | es | Configured currency is USD; do not advertise MXN pricing or assume checkout currency. |
| Netherlands (NL) | EUR | nl | Country/product/route/cost qualification pending |
| Norway (NO) | EUR | no | Configured currency is EUR; do not advertise NOK pricing or assume checkout currency. |
| New Zealand (NZ) | NZD | en | Country/product/route/cost qualification pending |
| Poland (PL) | PLN | pl | Country/product/route/cost qualification pending |
| St. Pierre & Miquelon (PM) | EUR | fr | Country/product/route/cost qualification pending |
| Portugal (PT) | EUR | pt-BR | Published pt-BR at /pt/ needs European-Portuguese adaptation and current route review. |
| Réunion (RE) | EUR | fr | Country/product/route/cost qualification pending |
| Romania (RO) | RON | ro | Country/product/route/cost qualification pending |
| Serbia (RS) | RSD | en | Serbian is not published; English candidate is limited to comprehending shoppers. |
| Russia (RU) | EUR | ru | Google currently pauses ads to users located in Russia; no launch or bypass. Russian-language templates may later qualify for a different allowed country. |
| Sweden (SE) | SEK | sv | Country/product/route/cost qualification pending |
| Slovenia (SI) | EUR | en | Slovenian is not published; English candidate is limited to comprehending shoppers. |
| Slovakia (SK) | EUR | en | Slovak is not published; English candidate is limited to comprehending shoppers. |
| San Marino (SM) | EUR | it | Country/product/route/cost qualification pending |
| El Salvador (SV) | USD | es | Country/product/route/cost qualification pending |
| Turks & Caicos Islands (TC) | USD | en | Country/product/route/cost qualification pending |
| French Southern Territories (TF) | EUR | fr | Google country targeting availability and practical consumer delivery are unverified; do not create an account target from ISO code alone. |
| Tuvalu (TV) | AUD | en | Country/product/route/cost qualification pending |
| U.S. Outlying Islands (UM) | USD | en | Google country targeting availability and practical consumer delivery are unverified; do not create an account target from ISO code alone. |
| United States (US) | USD | en, es | Country/product/route/cost qualification pending |
| British Virgin Islands (VG) | USD | en | Country/product/route/cost qualification pending |
| Wallis & Futuna (WF) | XPF | fr | Country/product/route/cost qualification pending |
| Samoa (WS) | WST | en | Country/product/route/cost qualification pending |
| Kosovo (XK) | EUR | en | Albanian/Serbian are not published; English candidate is limited to comprehending shoppers. |
| Mayotte (YT) | EUR | fr | Country/product/route/cost qualification pending |

## Verification and next action

138/138 integration checks passed for complete source pagination, exact country/locale coverage, text counts and weighted lengths, duplicate text, literal negative conflicts, held status and unassigned budgets. Independent review is recorded separately; local validation is not Google acceptance or native-human certification. See [BUILD_VALIDATION.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/current_campaign_repair/research/all_market_build_20260914/BUILD_VALIDATION.json) and [INDEPENDENT_REVIEW.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/current_campaign_repair/research/all_market_build_20260914/INDEPENDENT_REVIEW.json).

**Next Google Ads action:** complete the existing normal Google verification/Save step so the already-authorized repair can be submitted and read back. No further launch should follow until its country/product/cost/purchase and exact spend gates pass. The existing four-hour workflow remains in place; this pass creates no new automation or goal.

Continuation: “Continue the existing Google Ads task from this all-market packet, reconcile any new normal identity/Save result, complete the reviewed repair when possible, and qualify the next existing country/product cohort without repeating completed keyword research.”

Sources were checkedSeptember14,2026. See [SOURCE_DECISIONS.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/current_campaign_repair/research/all_market_build_20260914/SOURCE_DECISIONS.json) for the exact recommendation basis and availability limits.
