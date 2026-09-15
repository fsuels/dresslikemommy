# FAQ disclosure failure — diagnostic and local correction

Action: `TA06-FAQ-INLINE-JQUERY-20260914` (TA-06). Read-only diagnostic complete; exact correction prepared and locally verified. No customer-facing correction has been applied.

## Verified defect and owner

The public English FAQ at https://www.dresslikemommy.com/pages/faqs belongs to `gid://shopify/Page/161933381`, handle `faqs`, default page template, last updated `2026-04-28T06:57:44Z`. Its body contains eight inline jQuery click handlers and two legacy inline scripts. Each answer is hidden by an inline `display: none` style.

One normal semantic click on **A. Sizing** at `2026-09-14T22:59:06Z` reproduced `ReferenceError: jQuery is not defined` in the anchor's onclick handler. All eight answers stayed hidden. A separate page-load error came from the body-owned legacy jQuery scroll script. There was no loaded script URL containing jQuery, and the legacy `#nav` and `#goGrid` targets did not exist in the current DOM. The other seven inline handlers are the same dependency pattern; only Sizing was activated on the live page in this diagnostic.

The source route is default `templates/page.json` -> `sections/main-page.liquid:22` -> `page.content`. The defect lives in page content shared by themes.

## Reviewed theme relationship

Fresh Admin readback at `23:01:44Z` still identified theme `137888792673` as `UNPUBLISHED`. Its layout, global JavaScript and main-page section matched the reviewed source byte for byte. The page template matched its supplied checksum and parsed JSON; the API's returned text had a generated comment/formatting wrapper. All 527 files in the reviewed source binding were hash-verified. The scan found no jQuery library, `getWidthBrowser`, `remove_classes_active`, or replacement `question-answer-block` implementation.

The reviewed theme contains no repair for this page-owned defect. Publishing it alone does not replace the FAQ body. This is a source-based conclusion, not a claimed candidate-preview test; no preview was activated and no preview/country cookies were changed.

Final readback at `23:07:05Z` confirmed FAQ source unchanged, theme `133290917985` still `MAIN`, and `137888792673` still `UNPUBLISHED`.

## Exact local correction

`page-proposed.html` replaces the eight script-driven anchors with native `details` / `summary` controls. Each starts closed. The shared name preserves one-open accordion behavior in supporting browsers. Scoped styling keeps disclosure arrows visible, supplies a keyboard focus outline and a minimum 44px target. Both obsolete page-local scripts and the eight inline event handlers are removed. No library, tracking code, global theme shim or theme file is added.

- Before body SHA256: `3ef790830a524e2b2f03585b218d4d679bb97d4bc88554e937b32da6bdebb943`.
- Proposed body SHA256: `c2797437bb4ec0296fbbc5b9ac85f4ea7a4275e7cfd00e5ddf8c5e6ce5dfe0ff`.
- All eight answer HTML fragments, eight labels, 12 href anchors, headings, existing IDs and business text are preserved. The exact rollback is `page-before.html` (raw original bytes, including original line endings).
- Size changes from 12,202 to 9,685 bytes. This is a source-size difference, not measured PageSpeed improvement.

Loading jQuery was rejected because it would introduce a dependency and retain obsolete scroll, debug-alert and global active-class logic. A theme-wide compatibility script would affect a wider surface and leave the broken page dependency in place. Native controls solve the actual owner with no JavaScript requirement.

## Verification

| Check | Result |
| --- | --- |
| Admin queries validated against schema and Shopify skill validator | PASS |
| Current public normal Sizing activation | FAIL, reproduced buyer defect |
| Exact before/proposed answer and link preservation | PASS |
| Independent exact-body review, 14 structural/preservation checks | PASS WITH LIMITS |
| Local desktop 1280x720, all eight normal activations | PASS; matching answer visible and previous answer closes |
| Local Enter/Space keyboard opening and closing | PASS; focus outline visible |
| Keyboard Tab to Sizing Page link | PASS |
| Local mobile 390x844, sizing and long return control, second-click close | PASS; no horizontal overflow and all control targets 47px high |
| Local browser console | PASS; zero warnings/errors |
| Live after-state readback | PASS; no source/theme mutation |

`local-browser-verification.json` records 15 observed cases on the final proposal. Screenshots show desktop and mobile sizing answers. This was an isolated local harness using copied reviewed-theme CSS and current typography variables, with no Shopify scripts or jQuery. It does not certify a deployed page, full storefront shell, other languages, Safari, Firefox, PageSpeed scores, orders or conversion improvement. Older browsers that lack named disclosure grouping may allow several answers open; each remains accessible. The FAQ schema helper is rendered by collection sections, not this main-page route; its behavior was not changed.

An initial local selector mismatch was a test-tool targeting issue (native summary was exposed as a button in accessibility but generic in the DOM locator). The successful tests used the observed text/summary controls. The first screenshot exposed a clipped default marker; the final scoped inside-marker correction was independently reviewed and retested. No live retry or code injection was used.

## Preserved content risks

These existing claims were retained exactly and are not certified by the functional repair:

- Sizing guidance conflicts: one answer says the ordered EU size is sent; a later answer describes automatic two-size Asian substitutions. Product-specific measurement guidance must be reconciled before any factual rewrite.
- The payment answer says all payments are processed through PayPal. Current configured checkout payment methods require a separate readback.
- Operational-location, manufacturer/warehouse, response-time, tracking-time, cancellation-window and automatic tracking-email claims need authoritative business review. Dress Like Mommy's dropshipping model must not be changed into a claim of owned inventory or a physical store.

## Scope and handback

Only this disjoint FAQ subpacket was written. No page, MAIN theme, reviewed candidate, article, tracking, account, spend or shared canonical file was changed. No commit or push was made in this FAQ phase. The task-owned public/local browser tabs were closed, the temporary viewport reset, and the local test server stopped. User and organic-owner tabs were not used.

Parent owns TA-06 and shared canonical integration. The existing single owner Admin publication step for `DLM UX Performance QA 2026-09-10 (137888792673)` remains unchanged; this diagnostic neither authorizes nor substitutes for that step. Any later FAQ page-body release is a separate exact mutation and requires the parent to resolve authority, recheck Page161933381 and its before-body hash, inspect localization implications, apply only the reviewed body, read back the resulting body, and repeat desktop/mobile and keyboard buyer checks. Stop and rebase the proposal if the page body has changed. Rollback uses the exact prior body under the same controlled release boundary.

Continuation: Integrate `TA06-FAQ-INLINE-JQUERY-20260914` into TA-06 from this frozen subpacket, preserving existing owner publication and buyer-verification gates; do not treat local FAQ verification as a live fix or as authority to write the page.
