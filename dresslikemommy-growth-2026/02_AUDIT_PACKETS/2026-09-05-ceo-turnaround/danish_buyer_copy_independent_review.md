Confidence: H for local scope and snapshot consistency; rendered behavior remains unverified.

**PASS — bounded candidate/action review.** Reviewer did not author either candidate. Evidence is parent-captured Shopify readback, independently checked locally; no reviewer external access or mutation occurred.

Runtime comparison finds one insertion of five Danish entries: `chooseRoleStep`, `chooseOptionsStep`, `chooseRoleCta`, `addCurrentPiece`, `readyToAdd`. The Danish dictionary grows from 17 to 22 keys. Every preexisting Danish entry, every other locale map, and every other runtime byte remains identical. The supplied patch reconstructs exactly; Node syntax passes. Independent extraction of the actual dictionary and seven unchanged helper functions reproduces baseline English fallback, verifies Danish output for `da`, `da-DK`, `da_DK`, preserves interpolation, and passes all 22 English-map-key lookups for `en`, `es`, `nl`, and unknown `zz`. Root's earlier incomplete-helper test failure was harness-only; the corrected test required no candidate edit.

The 2026-09-06 04:58:18 UTC readback identifies MAIN `133290917985` and UNPUBLISHED `137782591585`. Both runtime MD5s equal local-before `61ded53111ee5002eb5c37b42a2c4b3f`; candidate MD5 is `379cc0f86d1ed46e357ceca745687c3e`. Both include MD5s equal local `8ef13387dda2b02fb6b4ce04df170424`; [main-product.liquid](../../../sections/main-product.liquid:933) includes this exact runtime asset. This is checksum binding, not direct returned server-body text. The 05:00:45 UTC manifests contain 525 unique filenames each, complete terminal pagination, and only preexisting `assets/cart.js`, `locales/da.json`, `locales/nl.json` differences.

Skyfade `7536992976993` / `da` / `body_html` passes exact omission equality: remove the single 92-character clause beginning `; det n&oslash;jagtige fiberindhold` and ending `blokerede leverand&oslash;rside`, and the result is exactly the candidate. Both patches reconstruct. All remaining factual text, numeric tokens, links, and three table byte strings remain identical: 13 + 13 + 14 = 40 data rows. No material composition is newly asserted. This does not resolve measurement truth or certify existing claims.

**FAIL:** none within the bounded local checks.

**GATES:** one-file staging on existing UNPUBLISHED `137782591585` is supported, subject to normal action-time tool review and fresh exact role/checksum checks. Preserve its three existing differences. After staging, verify the candidate checksum and full manifests: MAIN unchanged; only the intended fourth draft difference added. Keep active-product prose local because a product translation also affects MAIN. Mac-locked rendered preview, native-language certification, publication, Denmark readiness, and measured sales lift remain unverified. Restore only the same draft file if needed, after an exact-current conflict check.

SHA-256 bindings:

- Runtime before: `a2d55e4177b65213ebce2d842f0e8cbedaff486e9aee46bfc20b95c986e33024`
- Runtime candidate: `964872eee1ecbbef337628e14bcd2336022ccffb1e8fdbe1bdd6e635c66b2d50`
- Include: `6ab7ac0a8d9a68df637a35a5f900217b372ef6704a12232935f1651fb2c18fcd`
- Danish body before: `7c6cf0a3a2e53a04e9b439da34003669e633bc6b6f833146f89592fba34108eb`
- Danish body candidate: `2959051958b028be1971112e826ed65044437a039ddc0bbcdbba229ba0cb5d0d`
- Translatable source digest: `660d6c0aa25bc69bb7a95e89100282735a508cab37ca60a50f3374d4d04ce001` (distinct from translated-body hash).

**Postwrite addendum — 2026-09-06, through 05:08:16.906 UTC. PASS.** The former staging next action is completed root-operator work. Independently compared saved prewrite/after readbacks, complete before/after manifests, local candidate, and execution receipt; no API calls or repeated helper tests.

Shop/theme identities and MAIN/UNPUBLISHED roles persist. MAIN `133290917985`: zero file changes. Draft `137782591585`: exactly one changed file, `assets/product-desktop-ux-20260513-ruler-sync.js`, matching candidate MD5 `379cc0f86d1ed46e357ceca745687c3e` and SHA-256 `964872eee1ecbbef337628e14bcd2336022ccffb1e8fdbe1bdd6e635c66b2d50`. Both manifests contain 525 unique files with complete pagination. Four current cross-theme differences are the runtime plus preserved cart/DA/NL files; 521 files match. The receipt records one successful upsert, no job/errors, active-product write, publication, or spend. Binding uses server MD5, not returned server-body text.

Active-product prose remains local; measurements remain unchanged and unresolved. Native-language review, rendered preview, customer publication, Denmark readiness, and sales lift remain unverified. Normal Mac unlock is required for preview. Per the parent's canonical-action handoff, the sole pending owner action remains the exact Greek approval; this review creates no additional approval request or spend authority.
