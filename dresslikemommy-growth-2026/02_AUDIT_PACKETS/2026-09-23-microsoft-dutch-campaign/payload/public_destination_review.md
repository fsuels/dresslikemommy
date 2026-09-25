# Dutch collection readback — 2026-09-23

Confidence: H for HTTP reachability and returned HTML; M for broad category fit; Netherlands shopping readiness remains unverified.

All eight exact supplied URLs returned **HTTP 200**, retained their `/nl/` paths without redirect, and declare `lang="nl"`. Collection headings, sampled product titles and navigation contain Dutch. No collection was empty in the returned HTML.

| Destination | Reported total | Cards on returned page | Category assessment |
|---|---:|---:|---|
| [Dresses](https://www.dresslikemommy.com/nl/collections/dresses) | 37 | 36 | Mother/daughter dress titles match |
| [Family outfits](https://www.dresslikemommy.com/nl/collections/new-women-outfits) | 86 | 36 | Broad family assortment; dresses, shirts and sweaters observed |
| [Family tops](https://www.dresslikemommy.com/nl/collections/family-tops) | 36 | 36 | Tops/shirts fit broadly; also includes a sweater card |
| [Pajamas](https://www.dresslikemommy.com/nl/collections/pajamas) | 22 | 22 | Mother/child pajama titles match; collection heading is broader family category |
| [Father/son shirts](https://www.dresslikemommy.com/nl/collections/daddy-me-shirts) | 23 | 23 | Father/son, tropical and buttoned shirt titles match; joint sizes untested |
| [Mother/daughter outfits](https://www.dresslikemommy.com/nl/collections/mommy-and-me) | 116 | 36 | Broad matching outfits, including dresses, tops and swimwear |
| [Swimwear](https://www.dresslikemommy.com/nl/collections/swimsuits) | 35 | 35 | Mother/daughter swimsuit, bikini and swimdress titles match |
| [Sweaters](https://www.dresslikemommy.com/nl/collections/family-sweaters) | 7 | 7 | Sweater, cardigan and hoodie titles match broadly |

Every response initializes `Shopify.country="US"` and active currency `USD`. This establishes the unauthenticated server response context, not what a Netherlands shopper will ultimately see after browser localization. `/nl/` proves language routing, not Netherlands/EUR market, delivery or checkout suitability. A Netherlands browser buyer-path check remains necessary before activation.

No exact missing product is established. Counts are collection labels and first-page card links, not inventory, availability or complete-assortment certification. Matching adult/child variants, all advertised styles, product details, shipping, cart, checkout and mobile rendering were not tested. Do not remove assortment exclusions based on this check. Category overlap remains relevant to the routing negatives.

The web tool could not access any URL; one representative retry failed identically. Normal unauthenticated HTTP GETs provided the evidence instead. `public_destination_readback.json` preserves timestamps, URLs, status, extraction and SHA-256; `public_html_evidence/` preserves compressed response bodies. Script: `fetch_public_destinations.py`. No account, storefront or browser state changed.
