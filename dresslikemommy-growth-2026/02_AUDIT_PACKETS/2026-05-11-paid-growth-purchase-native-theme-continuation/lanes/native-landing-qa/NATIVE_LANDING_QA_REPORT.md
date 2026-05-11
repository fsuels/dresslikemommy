# Native Rewrite + Landing-language QA

Generated: 2026-05-11
Lane: Sidecar 2 native rewrite + landing-language QA
Mode: local/repo/public-read-only; no account writes; no Shopify Admin writes; no Ads/Pinterest writes; no checkout/payment entry.

## Source Files Reviewed

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation/google_ads_native_keyword_replacements_local_only.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation/google_ads_native_rsa_replacements_local_only.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation/google_ads_native_negative_replacements_local_only.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation/native_rewrite_locale_status.csv`
- Prior final URL map checked for route posture: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/final_url_mapping.csv`

## Counts

- Replacement keyword rows reviewed: `450`
- Replacement RSA rows reviewed: `45`
- Replacement negative-review rows reviewed: `133`
- Corrected locales reviewed: `9`
- Corrected markets reviewed: `ES`, `IT`, `RO`, `DE`, `NL`, `FR`, `SE`, `PL`, `CZ`
- All Google Ads replacement rows remain `REVIEW_ONLY_NOT_UPLOAD`.
- All nine corrected locales have `50` keyword rows, `5` RSA rows, and `25` unique replacement keywords.
- Negative-review rows vary by market: ES `14`, IT `16`, RO `16`, DE `14`, NL `13`, FR `15`, SE `14`, PL `16`, CZ `15`.
- Length validation remains mechanically clean from the source packet: max keyword `41`, max headline `30`, max description `77`, and `0` RSA forbidden-pattern hits.

## Public Spot Check

I ran one low-volume product landing GET for a clean representative product in each corrected locale using country-qualified localized routes:

- `/es/...?...country=ES`
- `/it/...?...country=IT`
- `/ro/...?...country=RO`
- `/de/...?...country=DE`
- `/nl/...?...country=NL`
- `/fr/...?...country=FR`
- `/sv/...?...country=SE`
- `/pl/...?...country=PL`
- `/cs/...?...country=CZ`

No cart, checkout, payment, order, CAPTCHA bypass, account login, or platform write occurred.

Spot-check result:

- `9/9` returned HTTP `200`.
- `9/9` retained the country-qualified final URL.
- `9/9` exposed expected `html lang` prefixes.
- `9/9` exposed expected currency markers.
- The raw pages include Shopify's standard `captcha-bootstrap` script text; this is not the same as a visible verification wall. The check did not enter or bypass verification.
- Raw evidence files: `landing_language_public_spotcheck.csv` and `landing_language_public_spotcheck.json`.

Important landing compliance blocker: the same representative product page exposed a hidden supplier/source URL in public HTML on several localized renders. The confirmed context is a related product card attribute:

`data-analytics-vendor="https://detail.1688.com/offer/602107180663.html"`

The scanner saw the supplier-domain token on the RO, DE, SE, and CZ spot-check pages. Because this is public page source, those markets are landing-compliance blocked until the vendor/source URL is removed from public analytics/card data and read back clean. This lane did not fix it because the scope allowed only local/repo/public read-only checks and files under this lane.

## Language-quality Risks Requiring Native Review

- ES: copy is much better than the old noun-chain packet, but `looks` / `outfits` are anglicisms and should be accepted or replaced by a Spain-native reviewer before use.
- IT: `look` / `outfit` are common but still need native review; negative terms around `costume` / carnival/theater intent should stay review-only to avoid blocking swimwear.
- RO: `lookuri` and father/child phrasing are plausible but need native review; RO also has a landing compliance blocker from the public supplier-domain token.
- DE: ad copy is mechanically stronger, but the spot-checked H1 still mixes English product wording (`Mother & Daughter Matching`) into German; DE is not landing-language clean.
- NL: ad copy is plausible, but the spot-checked title `Familie Matchende Sets` reads Dunglish and needs native landing-copy review.
- FR: ad copy is plausible, but title-style wording such as `Ensembles assortis Famille` should be checked by a French reviewer.
- SE: ad copy still uses `looks` / `outfits`, and the spot-checked title/H1 were English fallback text. SE fails landing-language QA until the page title/H1/meta/body are Swedish.
- PL: ad copy is plausible, but landing wording around `pasujące do mamy i córki` should get native Polish review before paid traffic.
- CZ: ad copy is plausible, but `Rodinné sady` and `looky` are obvious native-review items; CZ also has a public supplier-domain token blocker.

Negative keywords across all markets must stay `Exact review` / `Phrase review` as written. Do not widen free/used/pattern/costume/marketplace/supplier negatives without native and search-query review.

## Landing-language QA Requirements Before Any Platform Use

1. Use country-qualified localized product URLs for every corrected market. The older final URL map is already localized for ES, IT, and RO, but still uses base English routes for DE, NL, FR, SE, PL, and CZ. The spot check proves localized routes resolve, so any future local import packet should rebuild those final URLs to `/de`, `/nl`, `/fr`, `/sv`, `/pl`, and `/cs` paths before preview/import.
2. Run full final-URL QA for every ad group/theme in the actual upload candidate, not just one representative product. Include title, H1, meta title, OG/Twitter title, product body, size chart, country checker entry point, and shipping/support links.
3. Do not use the known beach/vacation handle for paid traffic until the stale Christmas metadata blocker is repaired and publicly read back clean, or continue using the held packet that excludes it.
4. Confirm only brand text remains English where appropriate. Product/category titles, H1s, body copy, CTAs, shipping clarity, and size-chart surfaces should be in the target language.
5. Confirm public source/HTML has `0` supplier/source-domain leaks, including `data-analytics-*`, product-card JSON, structured data, Shopify product JSON, and related-product cards.
6. Confirm country and currency presentment hold on landing pages: ES/IT/DE/NL/FR in EUR, RO in RON, SE in SEK, PL in PLN, CZ in CZK.
7. Confirm no physical-store, warehouse, local-stock, guaranteed-inventory, or pickup claims appear.
8. Get native-speaker review for keywords, RSAs, negatives, and the landing page language before any Google Ads preview/import/use.

## Market Verdicts

| Market | Locale | Verdict |
|---|---:|---|
| ES | es-ES | Local copy packet is review-ready; one landing spot check passed language/currency, but native review and full URL QA remain required. |
| IT | it-IT | Local copy packet is review-ready; one landing spot check passed language/currency, but native review and full URL QA remain required. |
| RO | ro-RO | Copy is review-ready, but landing is blocked by public supplier-domain token until fixed/read back clean. |
| DE | de-DE | Copy is review-ready, but landing is blocked by mixed English H1, older base-route mapping, and public supplier-domain token. |
| NL | nl-NL | Copy is review-ready, but landing needs native title review and older base-route mapping must be rebuilt to localized URLs. |
| FR | fr-FR | Copy is review-ready, but landing needs native title review and older base-route mapping must be rebuilt to localized URLs. |
| SE | sv-SE | Copy is review-ready only; landing-language QA fails because title/H1 are English fallback and a supplier-domain token was present. |
| PL | pl-PL | Copy is review-ready, but landing needs native Polish review and older base-route mapping must be rebuilt to localized URLs. |
| CZ | cs-CZ | Copy is review-ready, but landing needs native Czech review, older base-route mapping rebuild, and supplier-domain cleanup. |

Live-spend-ready corrected markets from this lane: `0`.

## Gated Locales Kept Gated

- `pt-PT`: keep gated until Portugal `pt-PT` vs storefront `pt-BR` dialect/route decision is made and read back.
- `da-DK`: keep gated; no Danish-native replacement rows exist in the May 11 rewrite packet.
- `fr-BE`: keep gated until Belgium FR/NL split, route proof, native review, and landing QA are complete.
- `nl-BE`: keep gated until Belgium FR/NL split, route proof, native review, and landing QA are complete.
- `el-GR`: keep gated; Greek-native review and Greek landing-language QA are still required.
- `CH`: keep gated; no CH native rows exist and the market needs a de-CH/fr-CH/it-CH/English split decision plus CHF landing proof.

## Next Best Action

Fix or route around the supplier-domain exposure before any non-US localized paid traffic work: remove source/vendor URLs from public product/card analytics data or the underlying product vendor fields, then run a low-volume public source readback proving `0` supplier-domain hits. In parallel, send ES/IT/RO/DE/NL/FR/SE/PL/CZ slices to native reviewers and rebuild the local final URL map so DE/NL/FR/SE/PL/CZ use localized country-qualified URLs.
