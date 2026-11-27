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
