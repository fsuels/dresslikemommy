# Multimarket Native Search Expansion Decision Packet

Generated UTC: `2026-05-19T11:44:22Z`

Guardrail: `LOCAL_READ_ONLY_PACKET__NO_GOOGLE_ADS_MUTATION`

## Decision

- Do not duplicate the existing English non-US campaigns. The live account already has country-level Search campaigns for AU, CA, GB, CH, CZ, DE, DK, ES, IT, NL, PL, and SE, but the readback shows they are English-language campaigns (`languageConstants/1000`).
- Native-language expansion should be separated by country and language. Do not put Spanish/Italian/Polish/Romanian/Czech keywords into those English campaign shells without a separate approved rebuild.
- Use exact-first native Search packets, then add phrase only after clean search-term proof. The only phrase-first candidate is Spanish `ropa familiar a juego`, because the exact row did not survive the click forecast gate at `$0.15`.
- No live Google Ads campaign, keyword, bid, budget, status, negative, conversion, Merchant, Shopify, Pinterest, GA4, GTM, or billing write occurred while creating this packet.

## Priority Order

| Rank | Market | Recommended action | Why |
|---:|---|---|---|
| 1 | `IT_IT` | `9` exact phase-1 rows; `0` phrase microtest rows; `9` phrase hold rows | Strongest balanced set: 18 forecastable rows, multiple themes, low forecast average CPC rows, and clean Italian localized collection URLs. |
| 2 | `PL_PL` | `4` exact phase-1 rows; `0` phrase microtest rows; `4` phrase hold rows | Highest upside but phrase risk is real, especially `sukienki dla mamy i córki`; launch exact first and hold matching phrase rows unless budget/search terms justify them. |
| 3 | `ES_ES` | `3` exact phase-1 rows; `1` phrase microtest rows; `3` phrase hold rows | Healthy Spanish Spain native set across family matching, pajamas, swimwear, and mommy-and-me dresses; include one phrase-only microtest if negatives are ready. |
| 4 | `RO_RO` | `1` exact phase-1 rows; `0` phrase microtest rows; `1` phrase hold rows | Very small but clear Romanian mommy-and-me dress signal; exact-first microtest only. |
| 5 | `CZ_CS` | `1` exact phase-1 rows; `0` phrase microtest rows; `1` phrase hold rows | Very small Czech mommy-and-me dress signal; exact-first microtest only. |

## Candidate Summary

| Market | Forecastable rows | Exact | Phrase | Phase 1 exact | Phase 1 phrase | Phase 2 phrase hold | 30d forecast clicks at $0.15 | 30d forecast cost at $0.15 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `IT_IT` | 18 | 9 | 9 | 9 | 0 | 9 | 40.849 | $2.89 |
| `PL_PL` | 8 | 4 | 4 | 4 | 0 | 4 | 213.823 | $23.32 |
| `ES_ES` | 7 | 3 | 4 | 3 | 1 | 3 | 34.616 | $3.51 |
| `RO_RO` | 2 | 1 | 1 | 1 | 0 | 1 | 65.070 | $7.53 |
| `CZ_CS` | 2 | 1 | 1 | 1 | 0 | 1 | 0.160 | $0.01 |

## All-Market Historical Gate

These are Google Ads API historical rows from the same candidate matrix. They are not fabricated CPC/search-volume/competition values. Rows with `0` or missing low top-of-page bid are not counted as cheap.

| Market | Candidate rows | Positive low-bid rows | Low top bid <= $0.15 | Low top bid <= $0.20 | Forecastable launch rows after $0.15 forecast | Hold rows from priority forecast |
|---|---:|---:|---:|---:|---:|---:|
| `AU_EN` | 12 | 2 | 0 | 0 | 0 | 0 |
| `BE_FR` | 50 | 6 | 0 | 0 | 0 | 0 |
| `BE_NL` | 50 | 12 | 0 | 0 | 0 | 0 |
| `CA_EN` | 12 | 3 | 0 | 0 | 0 | 0 |
| `CA_FR` | 50 | 10 | 4 | 6 | 0 | 4 |
| `CH_DE` | 50 | 10 | 0 | 0 | 0 | 0 |
| `CH_FR` | 50 | 6 | 2 | 2 | 0 | 2 |
| `CH_IT` | 50 | 2 | 0 | 0 | 0 | 0 |
| `CZ_CS` | 50 | 10 | 2 | 6 | 2 | 0 |
| `DE_DE` | 50 | 28 | 0 | 2 | 0 | 0 |
| `DK_DA` | 50 | 12 | 0 | 0 | 0 | 0 |
| `ES_ES` | 50 | 22 | 10 | 18 | 7 | 3 |
| `FR_FR` | 50 | 14 | 0 | 4 | 0 | 0 |
| `GB_EN` | 12 | 4 | 0 | 0 | 0 | 0 |
| `GR_EL` | 50 | 4 | 0 | 0 | 0 | 0 |
| `IT_IT` | 50 | 30 | 24 | 26 | 18 | 6 |
| `NL_NL` | 50 | 22 | 2 | 2 | 0 | 2 |
| `PL_PL` | 50 | 20 | 20 | 20 | 8 | 12 |
| `PT_PT` | 50 | 20 | 12 | 18 | 0 | 12 |
| `RO_RO` | 50 | 4 | 2 | 2 | 2 | 0 |
| `SE_SV` | 50 | 18 | 0 | 4 | 0 | 0 |
| `US_ES` | 50 | 8 | 0 | 4 | 0 | 0 |

## Existing Account Scope

- Existing non-US country campaigns are mostly English language (`1000`), even when their campaign name contains country codes like ES, IT, PL, or CZ.
- The native rows in this packet are `NEW_TO_SCOPE`; they did not match existing same country/language positive keywords in the live account inventory.
- GB/CA/AU English are not included here because they already have existing English Search structures and the current candidate set did not produce a new positive low-top `$0.15` opportunity. Repair/validate those existing structures instead of cloning campaigns.

## Landing Readback

| Market | Theme | Status | Supplier/source hits | Collection-grid signal | Localized URL | Title |
|---|---|---:|---:|---|---|---|
| `CZ_CS` | Mommy & Me Dresses | 200 | 0 | True | https://www.dresslikemommy.com/cs/collections/mommy-and-me?country=CZ | Oblečení pro mámu a já / Šaty, plavky a odpovídající soupravy |
| `ES_ES` | Family Matching | 200 | 0 | True | https://www.dresslikemommy.com/es/collections/matching-outfits?country=ES | Trajes a juego para la familia / Mamá y yo |
| `ES_ES` | Matching Pajamas | 200 | 0 | True | https://www.dresslikemommy.com/es/collections/pajamas?country=ES | Pijamas para Mamá y Bebé - Ropa de Dormir Familiar a Juego / Viste Como Mamá – Dress Like Mommy |
| `ES_ES` | Matching Swimwear | 200 | 0 | True | https://www.dresslikemommy.com/es/collections/family-swimsuits?country=ES | Trajes de baño familiares a juego / Traje de baño familiar |
| `ES_ES` | Mommy & Me Dresses | 200 | 0 | True | https://www.dresslikemommy.com/es/collections/mommy-and-me?country=ES | Mamá y yo Trajes / Vestidos, Trajes de baño y Conjuntos a juego |
| `IT_IT` | Family Matching | 200 | 0 | True | https://www.dresslikemommy.com/it/collections/matching-outfits?country=IT | Abiti coordinati per la famiglia / Mamma e Me |
| `IT_IT` | Matching Pajamas | 200 | 0 | True | https://www.dresslikemommy.com/it/collections/pajamas?country=IT | Pigiami Mamma e Me - Pigiami Coordinati per Famiglia / Vestiti Come Mamma – Dress Like Mommy |
| `IT_IT` | Matching Swimwear | 200 | 0 | True | https://www.dresslikemommy.com/it/collections/family-swimsuits?country=IT | Costumi da bagno coordinati per la famiglia / Costumi da bagno per famiglie |
| `IT_IT` | Mommy & Me Dresses | 200 | 0 | True | https://www.dresslikemommy.com/it/collections/mommy-and-me?country=IT | Mamma e Me Abiti / Abiti, Costumi da bagno e Set abbinati |
| `PL_PL` | Family Matching | 200 | 0 | True | https://www.dresslikemommy.com/pl/collections/matching-outfits?country=PL | Rodzinne stroje pasujące / Mama i ja |
| `PL_PL` | Matching Pajamas | 200 | 0 | True | https://www.dresslikemommy.com/pl/collections/pajamas?country=PL | Piżamy dla Mamy i Dziecka - Pasujące Rodzinne Piżamy / Ubierz się jak Mama – Dress Like Mommy |
| `PL_PL` | Mommy & Me Dresses | 200 | 0 | True | https://www.dresslikemommy.com/pl/collections/mommy-and-me?country=PL | Mama i ja Stroje / Sukienki, Stroje kąpielowe i pasujące Zestawy |
| `RO_RO` | Mommy & Me Dresses | 200 | 0 | True | https://www.dresslikemommy.com/ro/collections/mommy-and-me?country=RO | Ținute pentru mine și mami / Rochii, costume de baie și seturi asortate |

## Per-Market Files

- `IT_IT`: `it_it_launch_candidates.csv`
- `PL_PL`: `pl_pl_launch_candidates.csv`
- `ES_ES`: `es_es_launch_candidates.csv`
- `RO_RO`: `ro_ro_launch_candidates.csv`
- `CZ_CS`: `cz_cs_launch_candidates.csv`
- All forecastable rows: `native_language_launch_candidates_all_markets.csv`
- Existing campaign language readback: `live_search_campaign_language_summary.csv`
- Corrected localized landing readback: `winning_market_localized_landing_readback_corrected.csv`

## Launch Guardrails For Future Approval

- Use Manual CPC only, Google Search only, Search Partners off, Display/content off, AI Max off, broad match off, PMax off, purchase-only conversion, and subtotal/product-revenue ROAS reporting unchanged.
- Max CPC for these native non-US packets: `$0.15` (`150000` micros). Do not raise bids to chase first-page estimates.
- Start one native market at a time or at most two. Keep each new/test campaign at or below `$5/day` unless the owner gives fresh exact approval.
- Exact phase-1 rows are the cleanest launch candidates. Phrase rows with same-text exact candidates are phase-2 holds to prevent cannibalization and query waste.
- Add native negatives before launch: free/used/DIY/pattern/sewing/template/costume/wholesale/retailer/platform terms translated where needed, plus English account negatives already used in the existing Search campaigns.
- A live build still needs a fresh approval packet, before-state readback, validate-only mutate pass, after-state readback, and reviewer signoff.

## Recommended Next Exact Packet

Prepare `IT_IT` first as a paused or enabled owner-approved microtest, exact-only phase 1, using the rows marked `PHASE_1_EXACT_LAUNCH_CANDIDATE` in `it_it_launch_candidates.csv`. PL can follow, but keep Polish phrase rows held until exact terms prove query quality.
