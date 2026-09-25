# Public French landing QA — 2026-09-22

**PASS for URL reachability and basic assortment fit. PARTIAL for French localization. Rendered browser QA was BLOCKED by subagent IAB availability.** No ad-copy change is required by the observed assortment evidence. Retain the paused campaign build.

Root reports user confirmation of **France and Canada**. Live source metadata is now correctly separated from the attachment campaign name. The independent payload check was rerun after that correction: **225/225 pass**. The payload's geography-status string still describes its earlier parse time and should not supersede the fresh user answer.

## Method and evidence

The initial browser inventory exposed no IAB. Creating a new background IAB tab returned `Browser is not available: iab`; no existing tabs were selected or touched. Public web fetch returned the swimsuits page; the other seven URLs failed within that tool on an initial attempt and one retry. A public, unauthenticated HTTP GET pass succeeded for all eight routes at **2026-09-22 18:06 UTC**. No browser cookies, locale/country controls, cart, checkout, or storefront data were changed.

Every URL returned **HTTP 200**, retained its requested `/fr/` URL, declared `lang="fr"`, and contained a French collection H1. These are source-HTML observations, not rendered desktop/mobile or country-specific shopping tests. `landing_readback.json` records timestamps, URL/status, source hashes, headings, product links, and extracted-text paths. `landing_sources/` retains complete extracted public text and separate main-content text; scripts/styles are excluded. Product counts below are the collection's displayed source count, not stock or purchase availability.

| Collection | Count | Assortment evidence | Locale result |
| --- | ---: | --- | --- |
| [Dresses](https://www.dresslikemommy.com/fr/collections/dresses) | 37 | Floral, ruffled, smocked, white/beach and long dresses appear | French heading; some mixed brand/style names and filters |
| [Family outfits](https://www.dresslikemommy.com/fr/collections/new-women-outfits) | 86 | Coordinated dress/shirt/short families and photo/travel collections | French heading; several mixed English product titles |
| [Family tops](https://www.dresslikemommy.com/fr/collections/family-tops) | 36 | Button-down shirts, striped tops, floral/graphic t-shirts | French H1; English introductory and ending collection prose |
| [Pajamas](https://www.dresslikemommy.com/fr/collections/pajamas) | 22 | Mother-child short- and long-sleeve pajama styles | French H1/products; English introductory and ending prose |
| [Father-son shirts](https://www.dresslikemommy.com/fr/collections/daddy-me-shirts) | 23 | Tropical/Hawaiian collared, button-down, short-sleeve examples | French H1/main copy; document title and size/type filters retain English |
| [Mommy-and-me outfits](https://www.dresslikemommy.com/fr/collections/mommy-and-me) | 116 | Dresses, coordinated tops/skirts and separate-piece examples | French H1; some mixed English product names |
| [Swimwear](https://www.dresslikemommy.com/fr/collections/swimsuits) | 35 | One-piece, skirted, bikini, tankini, long-sleeve and floral examples | French H1/products; mixed filters and a wrong color label |
| [Family sweaters](https://www.dresslikemommy.com/fr/collections/family-sweaters) | 7 | Heart/cable-knit sweaters, cardigans and a striped fleece hoodie | French H1; English introductory and ending prose |

## Residual defects and limits

- **Shared shipping policy remains English** in all eight HTTP responses. Native navigation and some filter values also remain English. French ad text therefore does not yet imply an entirely French purchase journey.
- **Swimwear has a wrong color-filter translation:** an iPhone-model label is attached to five products. Evidence: `landing_sources/swimsuits.txt`, lines 497–499. This is a storefront data/localization issue, not an unsupported swimwear ad claim.
- **Father-son document title is English:** `landing_sources/daddy-me-shirts.txt`, line 1. The current main heading, product examples, and collection description are French, so the older attachment's broad mixed-English warning should be narrowed to what is currently observed.
- English collection prose is directly evidenced in `family-tops.txt` lines 440 and 1511, `pajamas.txt` lines 440 and 1189, and `family-sweaters.txt` lines 440 and 988.
- **Source/timing conflict:** the earlier web-tool swimsuits snapshot showed English tax text. The newer direct HTTP responses show French tax text. Do not report English tax text as a confirmed current defect.
- The unauthenticated fetch defaulted to United States/USD. France/Canada presence in the public country menu does not verify market shipping, prices, currency, taxes, variant selection, or checkout. Those were intentionally not changed or tested.
- Collection examples support the stated garment categories. They do not prove every matched adult/child variant is simultaneously purchasable, every price is per piece, or the 14 temporary catalogue negative restrictions are still necessary. No unsupported fabric, delivery, promotion, inventory, or returns claim should be added.

**Next action:** root can finish the authorized paused French build, using these eight reachable destinations. Keep native France/Canada settings, inherited assets, and final campaign readback in the root lane. The existing storefront owner can address locale defects without this reviewer taking over its browser or cookie state.
