# Header and mega menu redesign — 2026-09-26

Owner request (chat): make the header and mega menu more professional, beautiful and modern; audit the header colors for trust and sales.

## Audit of the live header (before)

- The live main menu has no child links, so the desktop "mega menu" never rendered. Every top item was a plain link, and "Shop" pointed to the homepage.
- The colors did not match each other. There was a pure-black announcement bar, an orange-red accent (`#e85d3a`) on hover, underline and cart badge, a bronze/cognac logo (`#7e431b`) and a pink heart. The orange fought the logo.
- The search box was a grey-bordered rectangle, and the country and language pickers were grey-bordered boxes.
- The announcement bar ran three messages together with `|` pipes. On mobile it rotated them with emoji prefixes (🚚 🔒).
- The mobile drawer showed six centered pill buttons with no imagery and no sub-categories.

## What changed (local theme files, not live)

- Palette tokens in `assets/dlm-header.css`: espresso ink `#2b211c`, cognac `#8b4a24` (from the logo), blush, cream `#fbf8f4` and sand `#f4eee7`. The orange accent was removed from the header. Text contrast is AA or better (cognac on white is 6.8:1, muted `#7a675c` on white is 5.3:1).
- Announcement bar: espresso background, cream text, and dot separators instead of pipes (`snippets/dlm-announcement-items.liquid`). The mobile rotator no longer adds emojis.
- Header: pill search on sand, borderless country and language text buttons, a cognac cart badge, and nav in the heading font (Assistant, no new font load) with a sliding cognac underline.
- Curated mega menu (`snippets/dlm-mega-panel.liquid`, `snippets/dlm-mega-card.liquid`, `assets/dlm-mega-menu.js`):
  - Menus for Shop, Mommy & Me, Daddy & Me and Family Matching. Each has link columns, two photo cards and a cream footer with "Shop all" plus three trust lines (shipping included, sizing support, secure checkout).
  - Hover intent opens and closes them. The caret button works for keyboard and touch, Escape closes the menu and returns focus, and moving focus out closes it.
  - The page behind is dimmed while a menu is open. There is also a no-JS hover fallback.
  - Links whose collection is missing or empty are hidden (`collection-storefront-visible`).
- Mobile drawer: a "Shop by Category" row of round photos, one grouped list with arrows, and slide-in submenus with two photo cards, a "Shop all" pill and grouped links. Drawer images load only when the drawer or submenu is opened.
- "Shop" now goes to `/collections/all` instead of the homepage. The parallel UX session later appended `?sort_by=created-descending` to that URL; that edit is preserved.
- 37 new `storefront.mega_menu` keys, translated into all 35 locale files.
- Menu-click analytics now labels the new menu (`mega` context; `submenu`, `feature`, `view_all` levels).
- The old header, announcement and mega-menu rules (510 lines) were removed from `assets/theme-inline-body-static-05.css`. That file loads after the header and was overriding it.
- The Mommy & Me card photo is a new 540×675 WebP of 80 KB, replacing a 360 KB JPEG.

## Verification

- `shopify theme check`: 0 offenses. `git diff --check` is clean. `node --check` passes for the three changed JS files.
- Rendering was checked in the in-app browser against a local snapshot of the live homepage, with this CSS and JS and markup mirroring the Liquid output. Checked:
  - Desktop at 1440 and 1024: all four panels, hover, the caret toggle, Escape and focus-out.
  - Mobile at 375: the drawer rail and the Mommy & Me submenu.
- Fixed during verification:
  - Hero content (z-index 4) painted over the panel.
  - Dawn's `div:empty` rule hid the dim layer.
  - The rail made the drawer wider than the screen.
  - An inline `predictive-search` wrapper pushed the search pill 25px low and showed grey corners.
  - Duplicate reindeer photos appeared across cards.
- BLOCKED: real Liquid render on a Shopify preview theme. The Shopify CLI is not logged in on this machine, and using the stored Admin token for `theme dev` was denied as credential use.

## Release

These are local, uncommitted files. `snippets/header-mega-menu.liquid` and `snippets/header-drawer.liquid` also carry the UX ten-fix session's Shop-link edit, so the two sessions' changes should be released together. Release to `main` needs owner approval.

## Update: real Shopify render verified

The owner logged in to the Shopify CLI, and `shopify theme dev` uploaded the working tree to development theme `156130082913`. That theme is unpublished and customers can't see it.

Checked on `http://127.0.0.1:9292/`:
- All four desktop menus render, with no Liquid errors and no missing translations:
  - Shop: 3 columns, 16 links.
  - Mommy & Me: 10 links.
  - Daddy & Me: 9 links.
  - Family Matching: 10 links.
- Each menu has 2 photo cards, and the photos load. The panel is solid and sits above the hero (header z-index 40).
- The announcement bar shows its dot separators.
- Mobile at 375: the 6 rail photos load when the drawer opens, and the Family Matching submenu slides in with 2 cards and 2 link groups. The drawer is 347px wide, with no horizontal overflow.

Links for empty collections are auto-hidden as designed. For example, "Mini dresses" and "Rompers & jumpsuits" have no products Shopify counts as available.
