# Lane F: verification notes (2026-09-26)

## Findings from studying the live page (read-only)

- The live PDP loads `assets/product-desktop-ux-20260513-ruler-sync.js`, from `sections/main-product.liquid` line 934. The builder markup comes from `snippets/product-desktop-ux.liquid`.
- The builder keeps an `instances` array internally, but the live step UI ("1 Choose who…", "2 Choose size…") always shows exactly one instance. `selectRoleGroup()` resets `instances` to one, and the button posts that single line as FormData `items[0]` to `/cart/add`.
- The "who" is not a separate option. It is the prefix of the Size values (for example `Mother M`, `Child 4-5 Years`). The builder groups by role. `ProductMatchingSetData-<section id>` JSON holds every variant with its id, `available`, `price` (cents) and `price_text` ("$32.99 USD").
- `#price-<sid> .price[data-price-variant-id]` holds the resolved variant id once a size is picked. When nothing is picked it holds the product id, which the module ignores because it is not a variant id.
- The cart uses Dawn `cart-drawer`, whose `getSectionsToRender()` returns `cart-drawer` and `cart-icon-bubble`. `renderContents(parsed)` opens the drawer.

## Checks

| Check | Result |
|---|---|
| `node --check assets/dlm-family-builder.js` | VERIFIED (pass) |
| `node --test ops/tests/test_family_builder.mjs` | VERIFIED, 10/10 pass |
| `shopify theme check` | VERIFIED: 0 offenses in lane files. The only offending file is the unrelated `snippets/dlm-mega-card.liquid` (2). |
| `git diff --check` | Fails only on the pre-existing, unrelated tracked CSVs under `2026-05-10-localized-product-size-chart-*`. The lane files are untracked; a grep for trailing whitespace across them is clean. |
| Built-in browser, live Beanie Ghost PDP, desktop | VERIFIED on an earlier revision: the source was injected (SHA-256 matched the file at that time), `window.fetch` was stubbed for `/cart/*`, and Mother M → Father L → Child 4-5 ×2 was checked by readback plus a screenshot |
| Headless Chromium harness on live PDPs (`tools/shoot_family_builder.js`) with the final file | VERIFIED at desktop 1440×900 and mobile 375×812 |

The final revision (synchronous capture of button writes, plus the sticky-bar state) was verified in the headless harness rather than the built-in pane. The pane would not load local files: localhost fetches and scripts are blocked. The harness injects the exact file contents from disk and intercepts cart writes at the network layer, which is stricter than a `window.fetch` stub. Ad and analytics hosts were aborted.

## Harness results (see `harness-results-beanie-ghost-family-matching-pajamas.json`)

- Flow at both viewports: Mother M kept → picker moves to Father; L kept → Child; 4-5 Years ×2 kept. The button reads `Add all to bag (4) · $137.96 USD`. After removing Father it reads `(3) · $101.97 USD`, and focus moves to the next line's Remove button.
- Exact payload (one request):
  `POST /cart/add.js` `application/json`
  `{"items":[{"id":47169572929633,"quantity":1},{"id":47169572765793,"quantity":2}],"sections":"cart-drawer,cart-icon-bubble","sections_url":"/products/beanie-ghost-family-matching-pajamas"}`
- Stubbed 422: the list is kept and the alert shows Shopify's description.
- Triple click with a slow stubbed success sends exactly one request. The button is `disabled` and `aria-busy` while the request is in flight.
- Stubbed success (real read-only section HTML from `/?sections=cart-drawer,cart-icon-bubble`): the cart drawer opens, the list clears, the builder is back to "Pick a size", the builder's localized success text is shown and announced, and both sticky bars go back to the builder's own state.
- Desktop and mobile sticky bars read "Your family list (N)", the total and `Add all to bag (N) · …` while the list is in use. A mobile sticky-bar tap on the Mother/Child product submits the whole list, 2 items in one `/cart/add.js`.
- Empty list: the builder's single-add still posts its own FormData `items[0]` to `/cart/add`. The flow is unchanged.
- `lavender-mommy-and-me-floral-applique-sleeveless-ruffle-dress` has no "who" roles, so the module does not mount.
- There is no horizontal overflow at 375px (`scrollWidth <= innerWidth` at every step). The Remove button is ≥ 44×44 CSS px and "+ Add another" is 48px tall.

## Screenshots (`screenshots/`)

`desktop-0..4`, `mobile375-0..4` (loaded, three people, after remove, error kept list, drawer after stubbed success), `other-bamboo-garden-panda-…-list.png` and `other-lavender-…-not-mounted.png`.

Because of the stub, the drawer screenshots show the real current empty cart.
