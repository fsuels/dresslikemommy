# Delivery arrival dates on PDP, cart drawer and /cart (2026-09-26)

Owner request: present the 12-16 day shipping window more persuasively, as an estimated arrival date.

## Change (commit `ffdc450` on `main`)

- `assets/dlm-delivery-dates.js` (new, loaded site-wide with `defer`): turns every `[data-dlm-delivery-window]` into a calendar range in the storefront locale, e.g. `Thu, Oct 8 – Mon, Oct 12`. Uses 12-16 calendar days from today; a date that lands on Sunday rolls to Monday. It re-renders cart drawer and /cart sections through a MutationObserver. Unparseable windows keep the Liquid text.
- `snippets/delivery-estimate-copy.liquid`: wraps the localized window in `<strong class="dlm-delivery-window" data-dlm-delivery-window>`. The day window stays as the no-JS fallback.
- `snippets/pdp-purchase-confidence.liquid`: the shipping row renders the same snippet, so the PDP, drawer and /cart share one source. Removed the now-unused `pc_shipping_checkout` assign.
- `layout/theme.liquid`: one `<script defer>` tag.
- `ops/tests/test_delivery_dates.mjs`: 5 node tests (Sep 26 → Oct 8–12, Sunday roll, localized windows, fallback, locale formatting).

The window is conservative: carrier-delivered orders took 9.3–12.6 days (n=3, see `2026-09-24-cart-to-checkout`). Copy keeps the localized "Estimated delivery:" prefix in all 35 locales; no new strings.

## Release

- Pushed 2026-09-26. The GitHub→Shopify sync had not reached the storefront after 10 minutes. A read-only `tools/theme_release_upsert.py read` then showed all 4 live MAIN `133290917985` files already equal to `ffdc450`, so no manual upsert was run.
- `release/after_state.json`: all 4 files equal `ffdc450`.

## Live readback (2026-09-26)

- EN PDP: `Estimated delivery: Thu, Oct 8 – Mon, Oct 12`; cart drawer note same.
- IT PDP (375×812): `Consegna stimata: gio 08 – lun 12 ott`, no horizontal overflow.
- DA PDP markup: `Forventet levering: <strong … data-dlm-delivery-window="12-16 dage">`.
- /cart: footer note renders the range; a simulated section re-render also re-dated.
- No console errors.
- Not run: a real add-to-cart drawer re-render. Adding a test item to the live cart was blocked by the session permission check.

## Rollback

Revert `ffdc450` and push. If the sync stalls, upsert the 4 files from `f997093` (the tool refuses to overwrite files that match neither commit).

## Measure

Cart → checkout rate from the Google-search funnel (baseline 30 days to 2026-09-24: 69 carts → 11 checkouts). Traffic is too low for an A/B test; compare 2–4 weeks after release.
