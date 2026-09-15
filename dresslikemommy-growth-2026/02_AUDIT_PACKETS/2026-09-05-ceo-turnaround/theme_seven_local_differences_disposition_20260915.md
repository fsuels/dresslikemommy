# Seven committed local theme differences

Confidence: H for source findings. Runtime acceptance: NOT RUN.

Compared the seven frozen candidate source blobs with committed local main `da7d37d1cf976613bdfdf8b017dcc278e0125c99`. All seven candidate hashes and seven local hashes matched their recorded values. Five meaningful files form three bounded changes; two files are unused source-parity aliases. No new investigation was performed while recording this disposition.

Frozen binding: [ACTUAL_527_SOURCE_BINDING.json](../2026-09-10-storefront-ux-pagespeed/czech-dresses-title-execution-20260915/ACTUAL_527_SOURCE_BINDING.json), SHA256 `1c7774546b9c58a412fe7e0a6d34c7965ccdbec3755fc22915ca944027bbbbf7`. Its September15 05:07:54.385UTC observation identifies candidate137888792673 as UNPUBLISHED; this is historical source evidence, not a fresh role or live readback.

Original seven-file record SHA256: `6dbeb51cb84a132760d64fd79abbdfafa4f638abc043b62d91f03eb359bd51fd`. The accompanying JSON retains exact source paths, binding row numbers, hashes, source dependency hashes, and verification details.

## Seven-file disposition

### assets/cart.js

**ACTIVE_CART_PAGE_HARDENING__ATOMIC_PAIR**. Local changed lines: 134. Frozen binding filename row: 171.

Changes the main-cart-footer section replacement selector from .js-contents to #main-cart-footer-subtotal.

Loaded by accepted sections/main-cart-items.liquid:23 unless cart_type is drawer, or by snippets/cart-drawer.liquid:12 through layout/theme.liquid:1127-1129 when cart_type is drawer. The changed list is for CartItems on the cart page; assets/cart-drawer.js:169-180 overrides the drawer item render list. Referenced active code, but no current subtotal defect is established: the accepted footer has one .js-contents and templates/cart.json configures subtotal/buttons only. The ID is precise targeting that avoids ambiguity if another matching element is introduced.

Candidate source: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/candidate/assets/cart.js`.

Candidate SHA256: `424bc9441658a476179df100a37ebf66e4162231e0ec97d99fcd805aa1c76fa6` (24541 bytes).

Committed local SHA256: `3e56046d72019380c0d48ecbd7ec5c12473813278eaeff90090fcec4124955be` (24555 bytes).

Inclusion: Include with sections/main-cart-footer.liquid. This JS alone would request a response selector missing from the old footer; cart.js:296-297 dereferences querySelector(selector).innerHTML without a null guard.

Minimum later verification:

- Verify one unique subtotal ID and matching returned section selector.
- At desktop and narrow widths, change quantity and remove an item; confirm totals/discounts update without console errors.
- Preserve the drawer override and unaffected cart controls.

### assets/product-desktop-ux-20260513.js

**UNUSED_DUPLICATE_ALIAS__SOURCE_PARITY_ONLY**. Local changed lines: 482-483. Frozen binding filename row: 1051.

Adds Spanish chooseRoleStep ('Elige para quién es esta pieza') and chooseOptionsStep ('Elige talla y opciones') strings.

No literal loader reference to this alias was found in the accepted bound executable theme sources. Accepted sections/main-product.liquid:933 loads product-desktop-ux-20260513-ruler-sync.js instead. No missing runtime Spanish fix. The accepted active ruler-sync module already contains these exact strings at lines502-503. This alias is byte-identical to assets/product-desktop-ux.js in both compared versions.

Candidate source: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/candidate/assets/product-desktop-ux-20260513.js`.

Candidate SHA256: `4208430b7754b2bb5a644875ff8da0600244bb3ba75d9cdcd1addab0baf6b6dd` (258243 bytes).

Committed local SHA256: `a2d55e4177b65213ebce2d842f0e8cbedaff486e9aee46bfc20b95c986e33024` (258347 bytes).

Inclusion: Preserve as source-parity work only; do not replace the active ruler-sync module with this older alias.

Minimum later verification:

- If including for source parity, retain the ruler-sync loader and confirm the two Spanish headings on one matching-set PDP.

### assets/product-desktop-ux.js

**UNUSED_DUPLICATE_ALIAS__SOURCE_PARITY_ONLY**. Local changed lines: 482-483. Frozen binding filename row: 1059.

Adds the same two Spanish strings as assets/product-desktop-ux-20260513.js.

No literal loader reference to this alias was found in the accepted bound executable theme sources. The accepted main-product section loads the ruler-sync module instead. Second unused byte-identical parity alias; the active module already contains this Spanish behavior.

Candidate source: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/candidate/assets/product-desktop-ux.js`.

Candidate SHA256: `4208430b7754b2bb5a644875ff8da0600244bb3ba75d9cdcd1addab0baf6b6dd` (258243 bytes).

Committed local SHA256: `a2d55e4177b65213ebce2d842f0e8cbedaff486e9aee46bfc20b95c986e33024` (258347 bytes).

Inclusion: Same parity-only treatment as the dated alias; do not swap the active loader.

Minimum later verification:

- Share the dated alias's narrow parity verification; no separate runtime fix is established.

### assets/recipient-form.js

**REAL_CONDITIONAL_FIXES__GIFT_RECIPIENT**. Local changed lines: 45, 104-107, 120. Frozen binding filename row: 1163.

Stores the cartError unsubscriber in cartErrorUnsubscriber instead of overwriting cartUpdateUnsubscriber, allowing disconnectedCallback to remove both subscriptions. Maps API send_on to the actual send-on DOM ID and sendonInput property, repairing the error-summary link and field aria-invalid/aria-describedby.

snippets/gift-card-recipient-form.liquid:14 loads this script. snippets/buy-buttons.liquid:17-18 and98-99 render that snippet only when show_gift_card_recipient and product.gift_card? are true; the accepted product template enables the setting at line49. Real code defects on a referenced conditional path. Actual gift-card product availability and runtime activation were not inspected.

Candidate source: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/candidate/assets/recipient-form.js`.

Candidate SHA256: `791e56ea26b07b95e7b0e93aca983676c7680a89c58082dcb93c3d2c4e8db1e7` (6504 bytes).

Committed local SHA256: `d677c7894c4681c82dd2c8c4cfc06392d2a3e26c1b92a962bd993bdebd607997` (6659 bytes).

Inclusion: Group with snippets/gift-card-recipient-form.liquid for JS and server-rendered error parity.

Minimum later verification:

- Mount, disconnect, and remount the recipient element; verify the cartUpdate/cartError/variantChange subscriptions clean up without duplicate callbacks.
- Exercise a send_on error and one ordinary-field error; confirm summary links, field error text, and ARIA associations.
- Confirm a successful product-form cart update resets recipient fields.

### sections/main-cart-footer.liquid

**ACTIVE_CART_PAGE_HARDENING__ATOMIC_PAIR**. Local changed lines: 94. Frozen binding filename row: 2867.

Adds id=main-cart-footer-subtotal to the existing subtotal .js-contents wrapper; no pricing or content logic changes.

Accepted templates/cart.json:1 includes main-cart-footer with subtotal and buttons blocks. Active matching half of the precise selector change. The old selector currently resolves the same sole .js-contents wrapper in the accepted footer.

Candidate source: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/theme-buyer-truth-successor-20260915/candidate-after/sections/main-cart-footer.liquid`.

Candidate SHA256: `837bb2c9890cc26d7e46c30c172cd11bb75518d917b01cc580ce3339a1eac6a1` (16559 bytes).

Committed local SHA256: `7a32f8dea8d3f853dcbf79c5374527df9970142cc4b1e9ed22dd656a48014e45` (16590 bytes).

Inclusion: Include with assets/cart.js; preserve existing successor footer content.

Minimum later verification:

- Run the shared cart-pair verification and assert the subtotal ID remains unique.

### sections/main-password-header.liquid

**REAL_CONDITIONAL_FIX__LOCALIZED_ACCESSIBILITY**. Local changed lines: 70. Frozen binding filename row: 2947.

Changes the label for value from translated login_form_password_label to stable Password, matching the password input ID at line61.

Accepted layout/password.liquid:203 renders main-password-header. Real localized label-association defect. English translation Password already matches, but accepted Spanish Contraseña and French Mot de passe do not. Actual password-page exposure is unknown.

Candidate source: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/candidate/sections/main-password-header.liquid`.

Candidate SHA256: `0c7a0fc6290d2a5d20e622198e17eb47a7379b4e7c0bc9614d81e52435b62b5f` (4327 bytes).

Committed local SHA256: `4dfbd8a1e7b4c136df268443b936affec15b3aae09b0b0f43e3eb10b1570afc7` (4276 bytes).

Inclusion: No source dependency among the other six files; retain existing storefront protection settings.

Minimum later verification:

- Render the password modal in English and one translated locale; verify label.control identifies the Password input and clicking the label focuses it.
- Do not change storefront protection or enter authentication material to perform this check.

### snippets/gift-card-recipient-form.liquid

**REAL_CONDITIONAL_FIX__SERVER_RENDERED_GIFT_ERROR**. Local changed lines: 68-72. Frozen binding filename row: 3323.

Maps server-rendered send_on error-summary anchors to Recipient-send-on-<section ID>, matching the date input. Other field anchors are preserved.

Rendered through snippets/buy-buttons.liquid:17-18,98-99 only for gift-card products with the recipient feature enabled; accepted templates/product.json:49 enables that setting. Real server-rendered counterpart to the JS error mapping. The existing date input and send_on error IDs are confirmed in the candidate at lines198 and214.

Candidate source: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/candidate/snippets/gift-card-recipient-form.liquid`.

Candidate SHA256: `1c26367bbd9ce7f29d61c51e2b8bf991969151f67430f2975934900406430dfa` (8416 bytes).

Committed local SHA256: `75353f37457130bcc93b98320b47c6a22abfaaa5096000927e3fcfff28c13d37` (8609 bytes).

Inclusion: Group with assets/recipient-form.js; actual gift-card catalog activation remains unknown.

Minimum later verification:

- Render a server-side send_on form error and verify its summary link targets the date input.
- Retain correct ordinary-field links and verify consistency with the JS error path.

## Loading and evidence limits

The accepted main-product source at `selector-recovery-20260911/native-deeplink-repair/proposed/sections/main-product.liquid:933` loads `product-desktop-ux-20260513-ruler-sync.js`. Its source is `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/theme-buyer-truth-successor-20260915/french-unit-correction/after.js`, SHA256 `dbd748d10828f52bb24c2dfb22d019261f4abeb7f3e9f61eb86d350ee96c1bcb`; both Spanish strings are already present at lines502-503. An exact old-alias reference lookup across228 bound Liquid/JavaScript executable source paths returned zero loader hits. This limited lookup does not certify runtime behavior injected outside those source files.

The cart footer's single `.js-contents` and accepted subtotal/buttons configuration do not demonstrate a present subtotal failure. Treat its two-file change as precise selector hardening. The gift-recipient pair and password label address real conditional source defects, but actual gift-card availability, recipient activation, and password-page exposure remain UNKNOWN.

No tests, browser checks, API calls, external actions, Git writes, or theme-source changes were performed by this lane. Only these two disposition artifacts were created. No production-readiness, deployment, release-completeness, sales, conversion, or profit claim follows.

## Next TA06 action

Existing TA06 owner qualifies the five meaningful files as the three bounded changes and preserves the two aliases as source-parity work whose Spanish behavior is already present. Root retains exact scope, current binding, release and canonical-state authority.

The separate one-file mobile CSS action remains root-owned and is not dependent on this disposition.

