# ES/IT Country-Qualified Landing QA

Generated: 2026-05-12T16:08:45-04:00

Mode: slow public landing-page GETs only. No checkout, payment, order, Ads, Merchant, Pinterest, Shopify product, feed, conversion-goal, budget, bid, or status write occurred.

| Market | Decision | HTTP | Lang | Currency | Supplier tokens | Stale blockers |
| --- | --- | ---: | --- | --- | --- | --- |
| `ES` | `ES_COUNTRY_QUALIFIED_LANDING_QA_PASSED` | `200` | `es` | `EUR, €` | `none` | `none` |
| `IT` | `IT_COUNTRY_QUALIFIED_LANDING_QA_PASSED` | `200` | `it` | `EUR, €` | `none` | `none` |

## Details

### ES

- Requested URL: `https://www.dresslikemommy.com/es/products/golden-daisy-mommy-and-me-set?country=ES`
- Final URL: `https://www.dresslikemommy.com/es/products/golden-daisy-mommy-and-me-set?country=ES`
- Title: `Golden Daisy Mamá e hija | Dress Like Mommy`
- H1: `Golden Daisy Mamá e hija - top o pantalón`
- Expected-language word hits: `mamá, hija, conjunto, añadir, carrito`
- Checks: `{"country_qualified_url_used": true, "currency_signal_present": true, "http_ok": true, "language_signal_present": true, "no_stale_paid_blocker_copy": true, "no_supplier_or_source_tokens": true, "not_verification_or_429": true}`

### IT

- Requested URL: `https://www.dresslikemommy.com/it/products/golden-daisy-mommy-and-me-set?country=IT`
- Final URL: `https://www.dresslikemommy.com/it/products/golden-daisy-mommy-and-me-set?country=IT`
- Title: `Golden Daisy mamma e figlia | Dress Like Mommy`
- H1: `Golden Daisy mamma e figlia - top o pantaloni`
- Expected-language word hits: `mamma, figlia, coordinato, aggiungi, carrello`
- Checks: `{"country_qualified_url_used": true, "currency_signal_present": true, "http_ok": true, "language_signal_present": true, "no_stale_paid_blocker_copy": true, "no_supplier_or_source_tokens": true, "not_verification_or_429": true}`

## Evidence

- Summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/es_it_country_landing_qa_summary.json`
- Summary CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/es_it_country_landing_qa_summary.csv`
- Raw HTML directory: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/landing_qa_raw`
