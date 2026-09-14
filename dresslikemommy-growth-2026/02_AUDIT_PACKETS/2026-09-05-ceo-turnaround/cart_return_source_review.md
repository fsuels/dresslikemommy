Confidence: M for the hypothesis; H for scoped source mapping. **Enough saved MAIN source exists for a local check, not a verified cause or fix.** Reviewed 2026-09-06, source checks through 13:57:53 UTC.

Root's [buyer receipt](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/sunshine_mobile_cart_readback.json:46) records two lines/USD46.98, checkout entry, Back displaying an empty header/drawer, reload restoring both lines, and cleanup to zero. Server-cart loss and bfcache attribution remain unproven. I performed no browser replay.

**Provenance:** saved [MAIN cart source](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/cart_draft_after_main/assets/cart.js:38) matches the [06:45 source readback](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/draft_preview_source_readback.json:69) and [07:07 complete manifest](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/draft_render_complete_manifest.json:20): MAIN `133290917985`, MD5 `6303a25065e3d6757ea9dc9be25dac92`. Draft `137782591585` is `61c560a479ad1e32ec4e84d4bf685f09`; current repository `assets/cart.js` is `96cdcd3049a35662312d95ab4447ad2a`, matching neither. It was excluded as live-source proof. Eight related repository files matched saved MAIN checksums, including drawer, product-form, global/PDP runtime, notification and their Liquid wiring. These are dated snapshots, not freshly fetched assets.

**Verified source facts:**

- MAIN `CartItems.connectedCallback` only subscribes to cart-update messages (saved cart.js:53–59). No return-event registration appears in the nine mapped files examined.
- [Drawer open](/Users/fsuels/Projects/dresslikemommy/assets/cart-drawer.js:26) changes presentation/focus/scroll without fetching current cart state. Initial empty state and header count come from Liquid ([drawer](/Users/fsuels/Projects/dresslikemommy/snippets/cart-drawer.liquid:20), [header](/Users/fsuels/Projects/dresslikemommy/sections/header.liquid:390)).
- [Existing refresh](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/cart_draft_after_main/assets/cart.js:77) replaces drawer-items and searches `.cart-drawer__footer`; [actual markup](/Users/fsuels/Projects/dresslikemommy/snippets/cart-drawer.liquid:576) uses `.drawer__footer`. It does not reconcile the outer empty class or header count. Simply calling that method on return would be incomplete.
- The [staged cart patch](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/cart_draft_release.patch:3) concerns recently viewed recommendations, not checkout-return refresh.

**Hypothesis:** restored/cached empty markup persists because this cart code does not reconcile on return/open. Reload recovery fits this explanation, but return response, navigation type, cart identity and other scripts were not measured; a checkout/session effect or another updater remains possible.

**Next local check:** simulate empty restored markup with a two-line mock cart using the exact saved MAIN sources. Observe return/open requests, then exercise existing refresh and verify header, outer empty class, lines, footer and total together. A mapped updater already restoring all state falsifies the missing-refresh premise; reproduction only proves a local gap, not production causality. No source edit or external action occurred.

SHA-256:

- MAIN cart: `6050b1dbcf8b64de7aa81714d25cb32ea5e87e2be33b6d65a51db1ace4781fd4`
- Complete manifest: `b49d932d658324111edd74d44c3c57ea815a41c244b491d612e61d624c289821`
- Root receipt: `ffc0bf2efac52220f17882841d6781cfcf5baae4346ea0c7e29f3f077f014309`
