# Landing Metadata Quality Scan

Date: 2026-05-08

Scope: low-volume public GET/HTML readback for the existing international Search final URL mapping. No carts, checkouts, account surfaces, Shopify Admin, product edits, or live paid-platform writes were used.

## Inputs Read

- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/PROBLEM_TRACKER.md` entry `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/final_url_mapping.csv`

## Sample Strategy

- Source mapping contains 102 final URL rows: 17 countries x 6 product themes.
- Checked 31 public URLs:
  - 6 base English-route GB product/theme URLs.
  - 6 ES localized product/theme URLs.
  - 6 IT localized product/theme URLs.
  - 6 RO localized product/theme URLs.
  - 6 PT localized product/theme URLs.
  - 1 targeted bad GB variant URL from the tracker.
- This samples each unique `product_handle + locale_path` combination once, plus the known bad variant URL, while keeping request volume low.

## Readback Summary

- HTTP status: 31/31 returned `200`.
- No `404` responses found.
- No `429` responses found.
- No verification/CAPTCHA page was detected; product metadata and product H1 rendered in the public HTML.
- Safe sampled rows: 25/31.
- Needs owner-approved Shopify metadata repair: 6/31.

## Confirmed Blocker

`PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH` is still present.

The known GB beach/vacation URL still returns stale Christmas SEO/social metadata:

- URL: `https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?country=GB`
- HTTP: `200`
- `<title>`: `Family Matching Sets - Christmas Print | Dress Like Mommy`
- `og:title`: `Family Matching Sets - Christmas Print | Dress Like Mommy`
- `twitter:title`: `Family Matching Sets - Christmas Print | Dress Like Mommy`
- H1: `Beach Outfits Holiday Palm Tree Print Summer Dresse...`

The targeted variant recheck also still returns stale Christmas metadata:

- URL: `https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601&country=GB`
- HTTP: `200`
- Same stale Christmas title, OG title, and Twitter title.

## Expanded Finding

The issue is not limited to the English/base route. The same `Vacation Family` beach/palm/summer handle has stale Christmas-themed SEO/social title metadata in sampled localized routes:

| Locale | Metadata title | Product H1 |
|---|---|---|
| ES | `Conjuntos a Juego para la Familia - Estampado Navideño | Viste Como Mamá – Dress Like Mommy` | `Conjuntos de playa con estampado de palmeras para vacaciones, vestidos de verano...` |
| IT | `Set Coordinati per Famiglia - Stampa Natalizia | Vestiti come Mamma – Dress Like Mommy` | `Abiti da spiaggia Abito estivo con stampa di palme per le vacanze...` |
| RO | `Seturi asortate pentru familie - Imprimeu de Crăciun | Îmbracă-te ca Mami – Dress Like Mommy` | `Ținute de plajă cu imprimeu de palmieri pentru vacanță, rochii de vară` |
| PT | `Conjuntos Família Combinando - Estampa de Natal | Vista-se Como Mamãe – Dress Like Mommy` | `Roupas para Praia com Estampa de Palmeira para Férias Vestidos de Verão` |

Because the base English route metadata is product-level and the `country` query parameter is not expected to change SEO/social title content, all base-route `Vacation Family` rows should remain on hold too. Net recommendation: hold all 17 mapping rows for handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` until repaired or swapped.

## Other Themes

No obvious stale/irrelevant title metadata was detected in the sampled rows for these themes:

- `Mommy & Me Dresses`
- `Family Matching`
- `Matching Pajamas`
- `Matching Swimwear`
- `Daddy & Me`

These sampled rows returned HTTP `200`, rendered product H1s, and did not show stale Christmas terms in title, OG title, or Twitter title.

## Recommendations

- `needs owner-approved Shopify metadata repair`: all `Vacation Family` final URLs using handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`.
- `hold`: do not use this beach/vacation handle in any approved paid Search import or live traffic until public readback shows beach/vacation-specific title, OG title, and Twitter title in English and localized routes, or until the product is swapped out locally for a clean URL.
- `safe-to-use`: sampled non-Vacation themes are safe for metadata/title quality based on this low-volume scan, subject to the existing broader spend gates for shipping, tracking, Merchant/Pinterest, economics, and owner approval.

## Artifacts

- `landing_metadata_quality_scan.csv`: checked URL readbacks with HTTP status, final URL, title, OG title, Twitter title, H1, flags, and recommendation.
- `landing_metadata_quality_scan.json`: JSON copy of checked URL readbacks.
- `landing_metadata_quality_summary.json`: aggregate counts and hold rows.
- `final_url_mapping_quality_recommendations.csv`: recommendation mapped back to all 102 rows in the source final URL mapping.

## Residual Risk

This was intentionally low-volume. It sampled by product handle and locale path, not every `country` query parameter for every product. Country-specific metadata drift is unlikely for Shopify product SEO/social titles, but a full 102-row scan would be the only way to prove every final URL independently.
