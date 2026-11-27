# PDP gallery gap on colour change (2026-11-27) — diagnosed, NOT changed

## Reproduced (built-in browser, 1 page load + 1 variant change, no 429/403)
- Product: /products/nordic-yoke-family-matching-sweaters, colour **Gray** (variant 48855064182881).
- The Gray photo is square (1:1, 375x375 / 505x505), not landscape. The other photos are 9:16 lifestyle shots (0.5625).
- Mobile 375: on Gray the active slide is 375x665 (list 677), but the photo draws 373 px tall (object-fit contain, top). That leaves a **~292 px white gap** under it. Cream/lifestyle: gap about 2 px.
- Desktop 1024: Gray box 325x325, photo fills it, **no gap**. Mobile only.
- No horizontal overflow (375/375).

## Where it comes from
`sections/main-product.liquid` inline style ("Reserve PDP gallery height before deferred product CSS finishes loading"): on <=749 px every `.product__media-item`, `.product-media-container`, modal opener and `.media` gets `aspect-ratio: var(--dlm-mobile-gallery-ratio)`. That value is `{{ mobile_gallery_ratio }}` = the first photo's ratio (0.5625 here) for all slides. It is a deliberate anti-layout-shift lock, so the square slide gets a 9:16 box. On colour change Dawn moves the variant photo to the first slide (scrollLeft 0), but the box keeps the locked ratio.

## Why no change
Giving each slide its own ratio does not remove the gap by itself. The horizontal slider list is as tall as its tallest slide, so the square slide still sits in a 665 px row. Removing it would need the slider height to follow the active slide in JS. Every swipe between 9:16 and 1:1 photos would then move the page content below by about 290 px. That changes gallery behaviour and the anti-shift lock, which is the "rehacer la galería" case. No theme change made; no lock taken.

## Options (for the CEO)
1. Content (recommended, no code): give Gray a 9:16 (or same-ratio) photo like the other colours, following the "photo for every colour" listing rule. Also check the Cream catalog shot (same 1:1 ratio, slide 5).
2. Code (bigger, needs a decision): ratio follows the active slide on mobile, with a short height transition. Cost: the page jumps on swipe, and the first-paint lock needs rework.

## Note
The built-in browser pane is shared: before my load, tab-36 showed another session's /pl/cart; my navigation replaced it.

# Fix released (2026-11-27 ~08:25Z, coordinator decision after the ratio audit: 50 products affected)

Commit `ab38ad5`; theme listed (2 differ) then applied in a separate call (applied 2, re-check 0 differ). THEME_LOCK held 08:23Z until after the export check; Shopify export `32e5cec` keeps both files unchanged.

## Change (38 lines, no structure change)
- `assets/media-gallery.js`: `slideRatio()` reads the slide's existing inline `--ratio` (already rendered by Liquid). `hasMixedRatios()` returns false when all photos share one ratio, and then nothing is bound or set. `fitActiveRatio(slide)` sets `--dlm-mobile-gallery-ratio` on the gallery viewer to the active photo's ratio, mobile only (`(min-width: 750px)` returns). It is called on `slideChanged` (swipe) and in `setActiveMedia` (colour choice).
- `sections/main-product.liquid` inline style: on <=749 px without reduced motion, `transition: aspect-ratio 0.2s ease` on the 4 gallery boxes that already use the variable.
- First paint unchanged: the reserve (tallest photo ratio) stays. Desktop unchanged.

## Verification (built-in browser, own background tab, 7 store loads 10 s or more apart, no 429/403)
Background tabs do not advance animations, so after each change I called `finish()` on the aspect-ratio transitions; I sampled the transition itself once on a pre-release trial: 677 -> 385 px in about 200 ms. Swipes were triggered by `scrollTo` plus a `scroll` event, because the background tab does not dispatch scroll.
- nordic-yoke, mobile: load list 677, 0 layout shifts, var not set. Gray: 373x373 photo, list 385 (was 665 box, ~292 px gap). Swipe to a 9:16 lifestyle slide: list 677, gap 2 px (as before). Swipe to the Cream catalog slide: 385. Cream colour: 373x373, list 385.
- nordic-yoke, desktop 1024: var never set; Gray 325x325 and lifestyle 326x579, same as before.
- little-lamb (affected): Cream then Light Blue: each 373x373, list 385.
- cream-heart cardigans (not affected, all 0.5625): var not set after a swipe, list 677, no new code path.
- bamboo-garden-panda (case b, 0.5626/0.80): swipe sets var 0.80, as intended.
- /de nordic-yoke: lang de, no overflow, no layout shift.
- Everywhere: scrollWidth 375 <= 375; console only the known 401s. No thumbnails on mobile (display none); desktop thumbnails untouched. Zoom/modal not opened.

## Residual
- A visitor landing directly on a colour URL (`?variant=` Gray) still sees the gap at first paint, because first paint was kept as today by decision. It closes on the first swipe or colour change. Option, not done: in Liquid, base the reserve on the selected variant's featured photo when `product.selected_variant` is set. This is server-side, so it adds no shift.
- During a swipe the incoming slide uses the outgoing slide's box until `slideChanged` fires. That is a short letterbox, never a crop.

Rollback: `git revert ab38ad5` via ceo_worktree, then sync-theme (list, then --apply).

# Quality V118 failed ab38ad5 -> one forward fix (2556642) -> REVERTED (c3c4605), 2026-11-27 ~08:50Z

Reproduced first, before touching anything, on /products/tie-shoulder-mommy-and-me-swimsuits (mobile): Green, swipe forward, swipe back gave a 292 px gap. DOM order 287329,739489,… but `sliderItemsToShow` was 739489,…,287329, …: stale order after the colour reorder (global.js `updateMedia`).
Counter "1/7 of 6": caused by my change. The height change makes the slider's ResizeObserver re-run `initPages()` on the stale list, so `slidesPerPage` is 0 and totalPages = items + 1. Before ab38ad5 the height never changed, so this never ran.

Forward fix 2556642: `resetPages()` after the reorder in setActiveMedia, plus measuring the slide nearest the slider centre on slideChanged. Matrix on tie-shoulder: Green OK (373x373, list 385); swipe back OK; 9:16 slide 677 OK; landscape 1.53 slide 244 OK; counter n/9 correct. **FAILED** on the first swipe after the colour change: the slider's currentPage was already 2, so slideChanged did not fire. The portrait slide was drawn 210x373 (shrunk). So per instructions: no second attempt.

Revert c3c4605 (`git revert --no-commit 2556642 ab38ad5` in the work copy, committed via ceo_worktree): sync-theme listed 2, applied 2, re-check 0 differ. `assets/media-gallery.js` and `sections/main-product.liquid` on main (after export) are byte-identical to `ab38ad5^`. Live check: media-gallery.js without the new code, no aspect-ratio transition, scrollWidth 375. Lock held 08:46Z until after the export check. 3 store loads this round.

Lesson for the re-plan: `slideChanged` is page-index based and goes stale after a colour reorder. A height follow should listen to the slider's own scroll (debounced or `scrollend`) and measure the centred slide. It should also call `resetPages()` after `updateMedia`. Test the first swipe after each colour change explicitly.

# Re-plan tested on a theme copy, then released: 6d69186 (2026-11-27 ~09:06Z)

Test copy (left in place for the CEO to delete): **gallery-test 2026-11-27**, `gid://shopify/OnlineStoreTheme/158206558305`, role UNPUBLISHED. Created with Admin API `themeDuplicate` of the MAIN theme (133290917985). Both `themeFilesUpsert` calls first checked the copy's id, name and role UNPUBLISHED. The first upload ran while the copy was still processing, so I uploaded again after `processing: false`.

## Change (assets/media-gallery.js + the ab38ad5 CSS transition in sections/main-product.liquid)
- Only on mobile, and only when a product's photos differ in shape (`hasMixedRatios`, checking `li[data-media-id]`). It listens to the slider's own `scroll`, debounced 100 ms. It then measures the slide nearest the slider's centre (`visibleSlide`, works in RTL), sets `--dlm-mobile-gallery-ratio` to that slide's ratio and syncs the photo counter to it.
- `setActiveMedia` (colour change): `syncSliderOrder()` calls the slider's existing `resetPages()` when the DOM order differs from `sliderItems`, then fits the colour's photo.
- First paint unchanged; desktop code paths return early.

## Matrix on the copy (preview_theme_id; built-in browser, own background tab, 375x812)
I finished transitions with finish(). Swipes used scrollTo plus a dispatched `scroll`, and colour changes were followed by a `scroll` too, because a background tab does not dispatch scroll; a real browser does. The preview bar was not present in the DOM. Format: photo drawn WxH, gap, list height, counter.
- tie-shoulder (9 photos, includes a 1.53 landscape): load 373x663/2/677 1/9. Green 373x373/0/385 1/9 -> swipe 2 373x663/2/677 2/9 -> back 373x373/0/385 1/9 -> 3, 9 (372x244, list 256), 6, all OK. Pink (vertical) 373x663 1/9 -> 2 -> 1 -> 5 (square 385) -> 1, all OK. Green again -> 2 -> 1 OK.
- santa-and-friends (6): Green 373x373 1/6 -> 2 -> 1 OK. Red 373x373 1/6 -> 2 -> 1 -> 5 -> 6 -> 3 OK. Counters n/6 (no "1/7").
- nordic-yoke (6): load 0 layout shifts, var not set. Gray -> 2 -> 1 -> 6 -> 4 OK; Cream -> 2 -> 1 OK.
- Not affected (cream-heart cardigans, all 0.56): swipe, var never set, list 677.
- Desktop 1024 (santa): var never set; Green 325x325; thumbnail click -> 326x579.
- /ar santa (rtl): Green 373x373 -> 2 -> 1 -> 6 OK, counters right.
- No horizontal overflow anywhere (375); console only the known 401s (plus one 422 from the first preview while the copy was still processing).
- The "2/9" counter seen right after a colour change in a background tab came from the stale page index. With the scroll the browser fires, it reads 1/9.
I left preview mode by loading the main theme id (`Shopify.theme.role` main afterwards).

## Release
Lock 09:05Z; commit 6d69186; sync-theme listed 2 in one call, applied 2 in another, re-check 0 differ. Shopify export b5d4c0e leaves both files unchanged. Lock held until 09:09Z.
Live repeat (main theme, tie-shoulder mobile): Green 373x373/0/385 1/9 -> swipe 2 373x663/677 2/9 -> back 373x373/385 1/9, all OK.
9 store loads in total.

Residual: a direct `?variant=` landing still shows the reserve at first paint until the first swipe or colour change, by design. Rollback: `git revert 6d69186` via ceo_worktree, then sync-theme.

# Colour-link entry, page-count race, CLS note: 06dfe4d (2026-11-27 ~09:23Z)

Copy "gallery-test 2026-11-27" (158206558305, UNPUBLISHED, still kept) was first made equal to the published theme. Checksums: 6 files differed (da/nb/no/ro-RO/ro locales and snippets/dlm-transit-map.liquid); I copied them from MAIN, and the re-check showed 0 differ. Every write checked id, name and role UNPUBLISHED first.

## Changes
1. `sections/main-product.liquid`: when `product.selected_variant` (a URL with ?variant=, as Google and Pinterest send) has a featured photo, the mobile first-paint reserve uses that photo's ratio. `snippets/product-media-gallery.liquid` already renders that photo first. Plain product URLs keep the tallest-photo reserve. No JS.
2. `assets/media-gallery.js`: the debounced scroll handler calls the slider's own `update()` before measuring, so its page number follows the real scroll position. `setActiveMedia` also runs that handler after its programmatic `scrollTo`.

## The step that failed once for Quality
I reproduced it: santa, colour change, then a swipe made while the colour was still loading. Dawn's `setActiveMedia` then scrolls back to the colour photo (existing behaviour). The slider's page index stayed at the swipe position and the counter read 2/6 on slide 1. Heights were already right. Cause: `resetPages()` ran `update()` before that scroll, and a programmatic scroll can come without a scroll event. Closed by change 2: after the fix, Green with no extra scroll event read 1/6 on slide 1, and Red plus an immediate swipe settled at slide 1, 1/6, 373x373.
While the 100 ms debounce plus the 0.2 s transition run, the incoming slide still sits in the old box. That transient is inherent; settled states are always right.

## CLS while swiping (not changed)
A swipe is a scroll, not a "recent input", so each height change that moves the content below counts in CLS. The same goes for a colour-change fit that lands more than 500 ms after the tap. I see no clean way: any in-flow height change counts, and reserving the maximum height brings the gap back. I would measure field CLS (CrUX or GA4 web-vitals, p75 on mobile) for the ~50 affected product URLs against the rest, over 28 days. The background-tab pane does not report layout-shift entries, so I could not measure it here.

## Matrix on the copy (mobile 375 unless noted; 9 loads in all including live)
- ?variant entry, square: nordic Gray: reserve 1.0, load 373x373, list 385, 0 shifts, no JS var, then swipe 2 (677) and back (385). tie-shoulder Green: reserve 1.0, 373x373, 1/9, swipe 2 and back OK.
- ?variant entry, vertical: tie-shoulder Pink: reserve 0.5625, 373x663 1/9, swipes 5 (385), 1, 9 (landscape 244), 2, all OK. Then Pink -> swipes OK; Red + immediate swipe settled OK.
- Normal entry santa: reserve 0.5625 (unchanged). Green -> 2 -> 1 -> 5 -> 1 OK with counters. Red race -> then 2, 1, 4, 6 OK.
- Not affected, ?variant entry (cream-heart): reserve 0.5626, list 677, var not set.
- Desktop ?variant (nordic Gray): 325x325, var not set (same as before).
- /ar not re-run this round: the scroll and RTL logic is unchanged from 6d69186, which passed /ar.
- Overflow 375 everywhere; console only the known 401s. I left preview by loading the main theme id.

## Release
Lock 09:22Z; commit 06dfe4d; sync-theme listed 2, applied 2 in a separate call, re-check 0. Shopify export c056cb2 leaves both files unchanged. Lock released 09:26Z.
Live (main theme, mobile): nordic ?variant=Gray reserve 1.0, 373x373, 1/6 -> swipe 2 (677, 2/6) -> back (385, 1/6), all OK. Desktop live: 325x325 unchanged.
Rollback: `git revert 06dfe4d` (keeps 6d69186), then sync-theme.
