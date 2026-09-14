# Mobile footer spacing amendment — frozen

Confidence: H for the source defect and minimal correction; rendered after-state awaits root QA.

Root observed Spanish/Spain preview **137881223265**, at **390×844** and maximum scroll: sticky purchase bar top **764**, height **80**; cookie button top **760.17**, bottom **804.17**, height **44**. The hit test at **190,780** reached the purchase button first. [Original geometry](release_candidate_v2/before_geometry.json).

The existing mobile spacing rule requires `body.template-product.sticky-mobile-atc-visible`; the observed body lacks `template-product`. The existing JavaScript already measures the actual bar height into `--sticky-mobile-atc-offset` and removes that property/class when hidden.

IMPLEMENTED: remove only `.template-product` from this selector in `assets/theme-inline-body-static-04.css`. The existing **749px** mobile boundary, measured-height fallback and safe-area padding remain unchanged. No JavaScript, footer, desktop rule, or frozen release file changes. This adds one amended file to the prior combined release.

Before MD5: `a27b45937f8d10c47a761a903868bc70`. After MD5: `ec036a8da2c7bacabd239bada8cde919`. After SHA-256: `532fc7346a84cb2d723a0c594372507bb8b77c06716ac9880ef74f4b97f861ca` (**18,322 bytes**).

VERIFIED: six focused checks pass, including the original selector mismatch, existing height measurement/removal, mobile/desktop boundaries and safe-area geometry calculations. Shopify skill Theme Check **1/1** and whitespace checks pass. These are source/CSSOM/JavaScript checks, not actual browser layout proof.

[Exact payload and receipt](release_candidate_v2/candidate_files_receipt.json), [one-line patch](release_candidate_v2/candidate.patch), and exact rollback are frozen. External writes: **zero**.

Next: root’s independent review and one-file preview stage, then repeat maximum-scroll pointer/keyboard checks on mobile, safe-area and desktop. Continuation: “Verify the frozen mobile-spacing amendment, stage that exact file, and confirm the footer control remains reachable.”
