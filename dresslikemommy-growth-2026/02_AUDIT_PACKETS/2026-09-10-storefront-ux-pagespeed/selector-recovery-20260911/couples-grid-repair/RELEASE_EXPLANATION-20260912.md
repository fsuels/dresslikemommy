# Latest theme, fixes and publication status

Verified September 12, 2026 at **08:29:57 UTC / 4:29 a.m. New York**.

The latest uploaded theme, and the version I recommend, is **DLM UX Performance QA 2026-09-10 (137888792673)**. Its name retains September 10; its final upload was **September 11 at 23:12:13 UTC / 7:12 p.m. New York**. It is still **UNPUBLISHED**. The live theme remains **dresslikemommy/main (133290917985)**.

**The draft repairs and scoped buyer checks are verified. The requested live release is BLOCKED by the Shopify connector's restriction on theme publication.** Shopify access is connected: the connector successfully saved the draft and independently read back its complete source. No additional general authorization is needed; the user has already requested publication.

## Why this draft is better

| Area | What changed and why it matters |
| --- | --- |
| Size and variant selection | Correct variant links initialize buying controls. Products the custom selector cannot classify safely keep their native size choices, so child sizes do not disappear. Explicit Girl/Boy options remain distinct. Adult normal/extended labels and original size-guide labels are preserved. |
| Mobile buying | Valid preselected variants work with the mobile Add button. Missing initial guide data no longer stops matching-piece controls. The cart footer no longer covers item controls, and quantity changes update the cart heading. |
| Couples collection | The three existing approved products now display. The page uses both saved translated description paragraphs, including how to order each person's option. The obsolete generated text below the grid is suppressed only for this exact collection ID. |
| Search and filtering | Filters no longer click through to products underneath, and outdated search responses cannot replace newer results. |
| Images, accessibility and languages | Responsive image sizing, deferred hidden hero slides, hero controls, headings, contrast, language-preserving links, Arabic child recognition and Japanese descriptions were repaired in the combined release. These changes are not a measured PageSpeed-score claim. |
| Reviews and existing integrations | Genuine review widgets and Shopify app hooks remain. Unsupported automatic review/promotional fallback wording was removed. Earlier consent, Merchant landing and localization work is retained. |

## What was preserved

The latest additions change **seven files** from the frozen V7 candidate and preserve **520** exactly. The final combined draft contains **527 files**, all matching the expected source. Compared with the live theme, it has **64 modified files, two added consent assets, 461 identical files and zero deleted files**. This complete comparison includes earlier inherited work as well as the latest repairs.

Both configuration files and **all 20 templates** remain byte-identical to MAIN. The latest changes do not alter product records, prices, variant availability, tags, source measurements, saved reviews or payment settings. Existing navigation, native buying forms, genuine review widgets and app hooks remain present. These are specific preservation checks, not certification of every third-party app.

All **525 live theme files remain unchanged**. The former live theme must be kept for rollback after publication. The immutable frozen candidate and exact three-file inverse are also retained.

The seven latest files are:

- `assets/product-desktop-ux-20260513-ruler-sync.js`
- `assets/component-product-desktop-ux-ruler-sync.css`
- `assets/size-conversion.js`
- `sections/main-product.liquid`
- `snippets/collection-grid-product-visible.liquid`
- `sections/main-collection-banner.liquid`
- `sections/main-collection-seo.liquid`

## Checks completed

- **Nine product/cart cases passed** for the size-selection repair on September 11. Those four product-related files are unchanged in the final combined source.
- **Three additional collection-to-cart paths passed on September 12**: Together Heart Adult 4XL/Green, Tropical Dress/Mother M, and Minimalist Adult M/Black. Each added the observed exact variant, quantity one, at the displayed USD price. Every test item was removed.
- The Couples page shows all three cards and complete stored copy in **English desktop/mobile, French, Spanish and Arabic**. Localized product links remain localized. The non-target Family collection still renders 36 cards and its existing lower text.
- Desktop/mobile screenshots were visually inspected; the mobile cart's product, quantity, remove control and standard Checkout button are clear.
- The selector and label suites passed **20 tests**. The independent Couples suite passed **10 tests**, including 432 non-target category/tag combinations and exact rendering of all 21 saved descriptions. Full **527-file Shopify Theme Check: zero diagnostics**. The Liquid skill validator passed all three collection files.
- Final source/inventory readback confirms this is the latest uploaded draft, with no source drift. Browser cleanup restored **MAIN, US/USD, English, cart zero**, reset the viewport and closed the task-owned tab; all four original user tabs remain.
- `git diff --check` passed. Strict continuity returned **CONTINUITY_OK**; see [continuity result](continuity-20260912.txt).

Evidence: [final source and buyer binding](verified-release-20260912.json), [September 12 buyer receipt](BUYER_READBACK-20260912.json), [independent review](independent-review.json), [earlier nine product/cart cases](../final-release/BUYER_READBACK.json), [three-file rollback](inverse.json).

The earlier empty-Couples finding is fixed and verified **in the draft**. It remains a live-site issue until publication. No order/payment was submitted, and no PageSpeed or conversion lift has been established. Amazon Pay was unavailable in earlier MAIN and preview checks and remains unresolved. Some broader localized presentation issues remain; the website is not certified perfect.

## Exact remaining owner action

Open [Shopify Admin → Online Store → Themes](https://admin.shopify.com/store/dresslikemommy-com/themes). Under the unpublished themes, publish **DLM UX Performance QA 2026-09-10 (137888792673)**. Keep **dresslikemommy/main (133290917985)** as the rollback theme.

The Shopify connector explicitly lists **theme publishing** among mutations “blocked for safety” and directs the owner to perform blocked operations in Shopify Admin. It also prohibits writing theme files to MAIN. Publication was not attempted through a browser, CLI or alternate API. This is a platform dependency, not a new request for permission or an automatic approval-review rejection.

After publication, verify that **137888792673 is MAIN**, compare its complete source with this final binding, then rerun the affected buyer checks and a properly bound desktop/mobile PageSpeed test.

Continuation: “I published DLM UX Performance QA 2026-09-10. Verify MAIN 137888792673 against the September 12 final source binding, then check the live buyer paths and PageSpeed.”
