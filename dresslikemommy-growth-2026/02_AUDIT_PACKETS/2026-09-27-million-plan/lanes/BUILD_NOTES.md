# Build notes: "Complete the family" cart upsell (fix 2, spec §3 of conversion.md)

Status: `LOCAL_BUILD_ONLY`. Nothing was committed, pushed, uploaded, synced or added to a real cart. The only network reads were two public GETs: `/products/jolly-crew-family-matching-pajamas.js` and `/es/products/jolly-crew-family-matching-pajamas.js`.

## Files for the parent to commit

New:
- `snippets/dlm-complete-family.liquid`
- `assets/dlm-complete-family.js`
- `assets/dlm-complete-family.css`
- `ops/tests/test_complete_family.mjs`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-27-million-plan/lanes/BUILD_NOTES.md` (this file)

Modified (both files were clean before this build, so the whole diff is this change):
- `snippets/cart-drawer.liquid`: loads the CSS and JS, captures the snippet, prints it inside `#CartDrawer-CartItems` under the line items, and skips the footer "You may also like" strip only while the block has offers.
- `sections/main-cart-items.liquid`: loads the CSS and JS, and renders the snippet inside `.js-contents` under the items table (`max_products: 1`).

No `locales/*.json` file was touched (see Localization).

## How it works

**Server side (Liquid, `snippets/dlm-complete-family.liquid`).** The block is inside the sections Dawn already re-renders: the drawer's `.drawer__inner` and the cart page's `.js-contents`. It refreshes on every add, remove or quantity change, needs no extra fetch, and never appears late, so there is no layout shift. The steps:

1. Takes up to 2 distinct cart products (drawer) or 1 (`/cart`), highest line price first.
2. **Role option.** This is the first option whose values carry at least two family roles. Option names and values are translated per storefront language: the live `/es` JSON returns `Talla`, `Mamá S` and `Infantil 2 años`. So the role is read from the value, not from the option name. Each value's first two words, first word, first hyphen segment, or last word is looked up in a multilingual alias table (`dcf_alias`) that covers all 7 roles in all 35 storefront languages. The table has no ambiguous aliases and matches `ROLE_DEFINITIONS` in `assets/product-desktop-ux-20260513-ruler-sync.js`; the test file enforces both. The rest of the value becomes the size label (`Mother S` → `S`, `Infantil 2 años` → `2 años`).
3. **Roles offered.** These are the product's roles that are not in the cart. `Kid` and `Adult` can also be offered again as "Another kid" or "Another adult". At most 4 chips per product.
4. **Variants offered.** Only available variants of that role are offered. Every non-role option (Color, Style or Type) must equal the cart line's value whenever that role has the value. If the role never has it (a Type-like option), the option is not matched and its value is appended to the size label, so the shopper sees exactly what they get.
5. **Markup.** Chips are `<button>`s, for example `+ Dad $35.99`. The price shows on the chip only when every size of that role has the same price. Each chip controls a hidden panel containing a labelled `<select>` (a "Size" placeholder, then each size, with its price when prices differ), a price line, and an **Add** button. The footer line reads "Each piece is sold separately." There is also a `role="alert"` error line and a `role="status"` line. The drawer uses an `h3` heading and `/cart` uses an `h2`.
6. **No forms or names.** The block sits inside `<form id="CartDrawer-Form">` and `<form id="cart">`, so it uses no `<form>`, no `name` attributes, and only `type="button"` buttons.

**Client side (`assets/dlm-complete-family.js`, ES5, delegated listeners, no re-binding needed):**
- A chip toggles its panel, and only one panel is open per block. Opening a panel preselects the last size used for that role in this session (`sessionStorage` `dlm:lastSize:<role>`, wrapped in try/catch), updates the price, and moves focus to the select.
- The select's `change` event is handled and stopped in the capture phase. Otherwise Dawn's `<cart-items>` / `<cart-drawer-items>` would treat it as a line quantity update. Verified: the handler count stayed at 0.
- **Add** sends `POST /cart/add.js` (locale-aware URL) with `{items:[{id, quantity:1}], sections, sections_url}`. The sections come from the host's own `getSectionsToRender()`. The response sections are swapped in place, as in Dawn's `updateQuantity`. The drawer stays open and keeps its scroll position. Focus returns to the block heading, or to the new line if the block is gone. A delayed status message then announces "Added to bag: Dad · L". `cartUpdate` is published with `source: 'cart-items'`, Dawn's signal that the sections have already been re-rendered, which avoids a second fetch.
- On error, the block shows Shopify's `description` (for example a sold-out message) or the localized fallback, and does not re-render. If the add succeeds but the swap fails, the page falls back to `/cart` instead of showing a false error.
- Analytics: `dataLayer.push({event:'dlm_complete_family', action:'open_role'|'add', product_id, role, surface})`. It sends ids and role keys only: no PII, no prices.

**Honesty:** real variant prices only, available variants only, no bundle price, no discount, no stock or urgency copy, and "each piece is sold separately" is always shown.

**Placement:** the block sits inside the scrolling item list, above the fixed checkout footer. In the drawer it cannot push Check out down. While the block shows, the footer's "You may also like" strip (about 150px) is skipped, which gives the item list more height. When there are no family offers, that strip renders exactly as before.

## Localization

This follows the in-file dictionary pattern of `snippets/automatic-discount-promo.liquid` and `assets/dlm-family-builder.js`. The `locales/*.json` files have a "may be overwritten by the Shopify admin language editor" header and uncommitted edits from other sessions, so this build does not touch them. 15 strings × 32 language groups are defined in the snippet: ar, cs, da, de, el, en, es, fi, fr, he, hi, hr, hu, id, it, ja, ko, lt, nb/nn/no, nl, pl, pt (with a pt-PT variant), ro, ru, sk, sl, sv, th, tr, vi, zh-CN and zh-TW. Together they cover all 35 storefront locale files. The JS gets its two runtime messages (added and error) from `data-` attributes rendered by Liquid.

## Test results (2026-09-27, local)

| Check | Result |
|---|---|
| `node --check assets/dlm-complete-family.js` | PASS |
| `node --test ops/tests/test_complete_family.mjs` | PASS, 12/12. Covers size memory (including throwing storage), request body, section dedupe and the 5-section cap, locale-aware URL, add success and error parsing, analytics payload, announcement text, alias table uniqueness and coverage, parity with `ROLE_DEFINITIONS`, and missing-role choice on live Jolly Crew values (en and es) plus adult/child, suffix, hyphen and colour cases |
| `node --test ops/tests/test_family_builder.mjs` | PASS, 10/10 (unchanged) |
| `shopify theme check --path .` (CLI 3.90.0, offline) | PASS, 0 offenses repo-wide. A deliberately broken copy of the snippet was flagged, which confirms the parser really checks it |
| `git diff --check` on the modified files, plus a trailing-whitespace / final-newline scan on the new files | PASS |
| Liquid logic | Shopify Liquid cannot be rendered locally. The algorithm was checked with a line-by-line Python port (Ruby `split` semantics) against live Jolly Crew JSON and against 10 local product structures in `tmp_products.json` (Child/Adult sweaters, Mother/Father/Child sweaters, a Style option). Results: Mother M in cart → `+ Dad $35.99`, `+ Kid $32.99`. With Mother and Child in cart → `+ Dad`, `+ Another kid`. Spanish gives the same roles with sizes `2 años`…. Child/Adult sweaters → `+ Another kid`, `+ Adult` |
| Browser (headless Chromium through Playwright, local harness with the real theme CSS and the real JS, `fetch` mocked, so no cart) | PASS at 375×812 and 1440×900, plus RTL. Block height 150px inside the scroll list. Check out stayed at y=734 (mobile) before and after a panel opened and after an add. Keyboard Enter opens a chip. Only one panel is open at a time. Add stays disabled until a size is chosen. Error path shows the alert and re-enables Add. The success path swapped the sections, left only `+ Kid $32.99`, focused the heading, announced "Added to bag: Dad · L" and stored the size. Console errors: none |

## Not verified / residual risk

- **No live Liquid render.** This needs a preview theme, with owner approval, to confirm that `options_with_values` value drops, `sort: 'final_line_price'` and `#` comments inside `{% liquid %}` behave as they do in the port. Rollback: remove the two `render` lines (and the capture) and restore the `if cart != empty` guard on the upsell.
- The `/cart` page was not rendered in a browser. At `max_products: 1` it adds about 150px above the cart footer. Measure Check out's position at 375×812 on the preview theme.
- Locales whose translated option values use words outside the alias table render nothing for that product (fail-closed). The table covers the builder's aliases plus common words for the other 20+ languages.
- The PDP handoff in spec §3.4 (builder intro line, preselecting the next role after a single add) is not part of this build.
- `ops/AGENT_WORKLOG.md` anchor: not added, because that file has other sessions' uncommitted edits. Add one when committing.
