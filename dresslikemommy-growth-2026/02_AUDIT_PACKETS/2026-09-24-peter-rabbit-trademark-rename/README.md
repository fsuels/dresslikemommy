# Peter Rabbit trademark rename (2026-09-24/25)

Owner request: several pajama listings used "Peter Rabbit", a trademarked character name that Merchant Center could disapprove. The owner approved in chat: rename them, change the URLs and add 301 redirects, and correct the Autumn set's title to long-sleeve.

The print artwork was inspected. It shows generic watercolor rabbits with no Beatrix Potter–style clothed rabbit, so renaming is enough to remove the name risk.

## Products (all still ACTIVE)

| Product | Old handle | New title | New handle | Color value |
|---|---|---|---|---|
| 7533379059809 | peter-rabbit-mommy-and-me-pajamas | Watercolor Bunny Garden Mommy and Me Pajamas — Short-Sleeve Set | watercolor-bunny-garden-mommy-and-me-pajamas | Bunny Garden |
| 7533454098529 | autumn-peter-rabbit-mommy-and-me-pajamas | Autumn Woodland Bunny Mommy and Me Pajamas — Long-Sleeve Set | autumn-woodland-bunny-mommy-and-me-pajamas | Autumn Woodland Bunny |
| 7533454655585 | peter-rabbit-gauze-mommy-and-me-pajamas | Eucalyptus Bunny Gauze Mommy and Me Pajamas — Long-Sleeve Set | eucalyptus-bunny-gauze-mommy-and-me-pajamas | Eucalyptus Bunny Meadow |

## Changes

- **English fields:** title, handle (`redirectNewHandle`), SEO title and description, body copy, Color option value, `custom.pattern`, and the "Peter Rabbit" tag removed.
- **Autumn set:** the "Short Sleeve Pajamas" tag was replaced with "Long Sleeve Pajamas".
- **Image alt text:** updated on the 4 images of 7533379059809.
- **SEO description for 7533379059809:** it listed wrong sizes (3Y/5Y/8Y). It now says Kids 1–6Y & Mom One Size.
- **Translations:** the owned poller (`poll_shopify_product_translations.py --force-refresh --execute`) refreshed most fields. Google Translate's free endpoint then returned HTTP 429. The remaining 68 fields in cs/da/el/fi/he/ja/ko/sv were hand-written and registered with `translationsRegister`. They are recorded in `MANUAL_TRANSLATION_PAYLOADS.json`.

## Readback (LIVE_VERIFIED)

- **English fields:** 0 trademark hits on all 3 products (`AFTER_STATE_ENGLISH.json`).
- **Translations:** 1,704 checked (20 locales × product, options, option values and metafields). 0 contain the name in any script, and 0 are outdated.
- **Old URLs:** each returns a 301 to the new handle, checked at `/`, `/de/` and `/en-au/`.
- **Storefront:** H1s checked in en/de/ja/he/da/fr. The only remaining matches are CDN image filenames (`peter-rabbit-mommy-and-me-pajamas-0X.png` on 7533379059809) and the "St. Pierre & Miquelon" country entry.

## Not changed (outside the approved scope)

- **Image filenames:** renaming them changes each image's CDN URL, which Merchant and Pinterest use as `image_link`.
- **Merchant feeds:** the US hosted feed and the manual AU `au-en.tsv` are generated files that still carry the old titles and links. At 03:53Z the US Worker returned 503 `feed_manifest_invalid_or_stale` during another owner's active restore run `20260925T025242Z-us-restore-r3`. That run's candidate was built before this rename. See PROB-2026-09-25-PETER-RABBIT-FEED-PROPAGATION.
- **Pinterest URL feeds:** these still carry the old rows (`pinterest-feed.tsv` has 156 rows; each paid-parent feed has 3). Pinterest's Shopify-app sources update automatically.

## Rollback

`BEFORE_STATE.json` holds the full prior English fields, tags, options, media alt text and all 20 locales' translations. To roll back, re-run `productUpdate` with those values and delete the three redirects.
