# Microsoft market and language inventory — September 14, 2026

Confidence: M. Fresh configuration is verified; shipping, country-selected buyer journeys and most native target eligibility remain unproved. This inventory makes no campaign or storefront change.

The validated Shopify read at 2026-09-14 20:44:40 UTC returned **21 published languages, six ACTIVE markets and 65 distinct countries (68 memberships)**. The fresh English dress-page selector matches all65 countries; its hreflang links match all21 Admin roots. The [machine inventory](market-language-inventory.json) contains every **1,365 country × locale component pair**, exact dress URL, evidence status and existing campaign join. These are possible selector combinations, not 1,365 campaign recommendations.

| Published language | Microsoft evidence | Dress route | Page source | Existing design countries |
|---|---|---|---|---|
| Arabic (`ar`) | Help listed; API conflict | [/ar/collections/dresses](https://www.dresslikemommy.com/ar/collections/dresses) | 200 / matching lang | None |
| Czech (`cs`) | Listed; account caveat | [/cs/collections/dresses](https://www.dresslikemommy.com/cs/collections/dresses) | 200 / matching lang | CZ |
| Danish (`da`) | Listed | [/da/collections/dresses](https://www.dresslikemommy.com/da/collections/dresses) | 200 / matching lang | DK |
| German (`de`) | Listed | [/de/collections/dresses](https://www.dresslikemommy.com/de/collections/dresses) | 200 / matching lang | DE |
| Greek (`el`) | Listed; account caveat | [/el/collections/dresses](https://www.dresslikemommy.com/el/collections/dresses) | 200 / matching lang | None |
| English (`en`) | Listed | [/collections/dresses](https://www.dresslikemommy.com/collections/dresses) | 200 / matching lang | US, AU |
| Spanish (`es`) | Listed | [/es/collections/dresses](https://www.dresslikemommy.com/es/collections/dresses) | 200 / matching lang | US, ES |
| Finnish (`fi`) | Listed | [/fi/collections/dresses](https://www.dresslikemommy.com/fi/collections/dresses) | 200 / matching lang | None |
| French (`fr`) | Listed | [/fr/collections/dresses](https://www.dresslikemommy.com/fr/collections/dresses) | 200 / matching lang | FR |
| Hebrew (`he`) | Help listed; API conflict | [/he/collections/dresses](https://www.dresslikemommy.com/he/collections/dresses) | 429; candidate only | None |
| Hindi (`hi`) | Help listed; API conflict | [/hi/collections/dresses](https://www.dresslikemommy.com/hi/collections/dresses) | 429; candidate only | None |
| Italian (`it`) | Listed | [/it/collections/dresses](https://www.dresslikemommy.com/it/collections/dresses) | 429; candidate only | IT |
| Japanese (`ja`) | Listed; account caveat | [/ja/collections/dresses](https://www.dresslikemommy.com/ja/collections/dresses) | 429; candidate only | None |
| Korean (`ko`) | Not listed as ad language | [/ko/collections/dresses](https://www.dresslikemommy.com/ko/collections/dresses) | 429; candidate only | None |
| Dutch (`nl`) | Listed | [/nl/collections/dresses](https://www.dresslikemommy.com/nl/collections/dresses) | 429; candidate only | NL |
| Norwegian (`no`) | Listed | [/no/collections/dresses](https://www.dresslikemommy.com/no/collections/dresses) | 429; candidate only | None |
| Polish (`pl`) | Listed; account caveat | [/pl/collections/dresses](https://www.dresslikemommy.com/pl/collections/dresses) | 429; candidate only | None |
| Portuguese (Brazil) (`pt-BR`) | Listed | [/pt/collections/dresses](https://www.dresslikemommy.com/pt/collections/dresses) | 429; candidate only | None |
| Romanian (`ro`) | Listed; account caveat | [/ro/collections/dresses](https://www.dresslikemommy.com/ro/collections/dresses) | 429; candidate only | RO |
| Russian (`ru`) | Help listed; API conflict | [/ru/collections/dresses](https://www.dresslikemommy.com/ru/collections/dresses) | 429; candidate only | None |
| Swedish (`sv`) | Listed | [/sv/collections/dresses](https://www.dresslikemommy.com/sv/collections/dresses) | 429; candidate only | None |

Microsoft’s [June19,2026 help source](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_aboutlanguageoptions) lists **20 of the21** site languages, including Hindi. Korean appears only in display/interface lists. The [API ad-language guide](https://learn.microsoft.com/en-us/advertising/guides/ad-languages?view=bingads-13) omits Hindi, while the [Search campaign schema](https://learn.microsoft.com/en-us/advertising/campaign-management-service/campaign?view=bingads-13) also omits Arabic, Hebrew and Russian and flags Czech, Greek, Japanese, Polish and Romanian account availability. Preserve these explicit account checks. Shopify `no` maps to Microsoft Norwegian/NB; `pt-BR` uses `/pt/` and Portuguese/PT. No Hindi API code is invented.

The existing library has **11 designs across ten countries and nine languages**, 21groups,147keywords,21RSAs and180negative proposals. Preserve US/en506254907 and DE/de506254908 (dated root saved-target receipt); this lane did not reopen them. Reuse US/es, ES/es, FR/fr, DK/da, NL/nl, IT/it, CZ/cs, RO/ro and AU/en local designs. Their nine dress groups still point to `/collections/mommy-and-me`; the inventory supplies the matching `/collections/dresses` candidate for root review. Tee URLs and all source CSVs remain unchanged. No uncreated campaign is called saved.

| ACTIVE Shopify market | Exact country conditions |
|---|---|
| Australia | AU |
| Canada | CA |
| Eurozone | AX, AD, CY, FI, GF, TF, GP, IT, XK, LV, LT, LU, MT, MQ, YT, MC, ME, NL, PT, RE, SM, SK, SI, ES, AT, BE, HR, BG, CZ, DK, FR, DE, GR, IS, IE, NO, PL, RO, RU, RS, SE, CH, GB |
| International | AI, BM, BS, CK, FJ, GL, KY, MX, NZ, SV, TC, TV, UM, VG, WF, WS, CA, AU, MF, BL, PM |
| United Kingdom | GB |
| United States | US |

AU,CA,GB occur in both dedicated and broader conditions; precedence was not queried. All language roots are global. Norway’s country metadata returns EUR; checkout currency is not inferred. BR,IN,JP,KR,IL are absent despite corresponding languages.

Published/selected countries are not shippable destinations: Shopify requires an active market **and applicable shipping rates**. No profile/rate or checkout was inspected here. [Shipping requirements](https://help.shopify.com/en/manual/international/shipping/shipping-zones)

Current exact Microsoft country eligibility remains unresolved beyond the dated US/DE saved targets. The linked current market-availability page failed, and the official repository Countries.md returned404; its Learn path also failed without retry. The [January2023 list](https://about.ads.microsoft.com/en/blog/post/january-2023/access-a-world-of-opportunity-scaling-campaigns-to-164-markets) is historical, not current authorization; it does not list these storefront codes: AX, BL, CK, GP, MF, PM, RU, TF, TV, UM, WF, WS, XK, YT. Russia also has a [historical Microsoft sales-suspension notice](https://blogs.microsoft.com/on-the-issues/2022/03/04/microsoft-suspends-russia-sales-ukraine-conflict/); Russian ad language does not establish Russia targeting eligibility. Root can verify the [latest authenticated location data](https://learn.microsoft.com/en-us/advertising/guides/geographical-location-codes?view=bingads-13) or native selectable locations without inventing IDs.

Nine GETs verified HTML language, canonical URL, dress heading and product links. Twelve returned429 in the same bounded batch; no retries followed. All21 candidate links remain supported by Admin roots and the successful English hreflang extraction. These source checks do not certify native copy, rendering, stock, shipping, checkout, purchases or low CPC/CPA. Auxiliary English policy headings occur in several translated sources.

Validation: **13 local checks passed**, including complete pagination,65-country selector equality,21root equality,1365unique pair coverage, exact library counts and source-file hash preservation. No shared or external writes.

Next action: use the inventory to qualify the exact country/language choices and dress destinations during root’s paused-campaign preparation; shipping, consent, purchase and economics gates remain separate.

Continuation: “Use market-language-inventory.json to fill existing campaign gaps, resolve marked language/country eligibility, and preserve all dated evidence and paused boundaries.”
