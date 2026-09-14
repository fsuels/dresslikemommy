# Fresh-theme cart candidate — local preparation only

**IMPLEMENTED locally. Fifteen relevant tests pass; the full frozen suite retains one independently reproduced baseline failure. NOT_STAGED.** Owner: `/root/cart_market_fix`; root retains integration and any future external mutation. Only the candidate, release patch and these two preparation files were written.

`cart_draft_before.json` identifies Dress Like Mommy shop15571635, MAIN133290917985 and UNPUBLISHED137782591585. Both returned cart bodies match `cart_draft_before/assets/cart.js` byte for byte, MD5 `6303a25065e3d6757ea9dc9be25dac92`. The original cached-dollar-price/unlocalized-history behavior was present. The dirty root `assets/cart.js` was not copied or changed.

All four hunks of the existing `cro_recently_viewed_only.patch` matched their entire old content exactly once in the fresh baseline. Zero fuzzy context was accepted; each match has the same −5 line-number offset. A separate `patch --dry-run --fuzz=0` succeeds. `cart_draft_release.patch` contains the same intended change with fresh-baseline line positions.

Only the recently-viewed IIFE changes: baseline lines381–448 become candidate lines381–493. Its 15,233-byte prefix and 4,168-byte suffix are byte-identical. Existing quantity, subtotal, AJAX, swipe and delivery code is preserved. Cached prices are omitted, links use one active locale, localized PDP visits are tracked, invalid storage/URLs and unsafe interpolation are handled, and history renders after cart updates.

## Dependencies and tests

The fresh cart defines `getLocaleAwareRoute` at line16 and already consumes `subscribe`/`PUB_SUB_EVENTS` at lines54/252. Local definitions exist in `assets/pubsub.js:3` and `assets/constants.js:3`; `layout/theme.liquid:315–316` loads those deferred scripts. This confirms local architecture and existing cart usage; those dependency files were not freshly fetched by this worker.

Verbatim copies of the frozen tests and each actual cart body were placed in equivalent temporary layouts under `/private/tmp/dlm-cart-draft-validation-y88l993t/`. Commands used the bundled Node runtime:

```text
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check <packet>/cart_draft_candidate/assets/cart.js
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --test --test-reporter=tap ops/tests/test_cart_recently_viewed.mjs
/usr/bin/patch --dry-run --fuzz=0 -p1 -i <packet>/cro_recently_viewed_only.patch
```

The test command ran from both temporary `baseline` and `candidate` directories. Complete commands, layouts, results and TAP paths are in `cart_draft_preparation.json`. Syntax and zero-fuzz checks pass. Baseline: **2 pass/14 fail**. Candidate: **15 pass/1 fail**, including both drawer/page, market switches, malformed storage, unsafe URLs/text/images, localized tracking and post-removal rendering. No candidate failure is new.

Test16 expects the unrelated dirty-local `main-cart-title`/`#main-cart-footer-subtotal` fix, which the fresh theme lacks. Both bodies fail with the same fingerprint: `TypeError`, `ERR_TEST_FAILURE`, `testCodeFailure`, `Cannot read properties of undefined (reading 'selector')`. It is not suppressed or counted as a pass. Initial output parsing expected TAP but Node defaulted to a human-readable reporter; both suites were rerun with explicit TAP without changing any assertion.

## Bound hashes and remaining gates

| Artifact | SHA256 |
|---|---|
| Fresh baseline | `6050b1dbcf8b64de7aa81714d25cb32ea5e87e2be33b6d65a51db1ace4781fd4` |
| Candidate | `e2fed4a6ae3abbba3b39d481dfee9eb755f623e7856b2d1c2a8747fe6c059cf7` |
| Release patch | `3f782948ba0526cebadf92fd9db3aaa92560975c57fb426db9f9164f9a654277` |
| Original reviewed patch, unchanged | `64ef531dae5eb4b852a74826efcdd8f12a9890a372d2d3c0087b9b8dca2742fd` |
| Frozen tests, unchanged | `1399787b95f13de129b290dbe829e24f21339d9ab5fe2439c0f7a705cb0fdc8f` |

Candidate MD5: `61c560a479ad1e32ec4e84d4bf685f09`. No browser, image fetch, account, draft/theme mutation, publication or shared-state edit occurred. Rendered behavior on Shopify remains NOT RUN. Root's next action is an independent delta/failure review before considering any separately permitted unpublished-only staging. This preparation is not a full-suite pass, live repair or release authority.
