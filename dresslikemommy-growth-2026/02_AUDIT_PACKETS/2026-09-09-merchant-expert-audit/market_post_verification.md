# Independent market publication post-verification

Confidence: H. **PASS — LIVE_VERIFIED at 2026-09-09T18:14:25.071Z.** Reviewer did not build or execute the correction and made no external writes.

Fresh Shopify Admin readback independently confirms:

| Publication | Active products before | Active products now |
|---|---:|---:|
| Eurozone `77105660001` | 238 | 240 EXACT |
| International `77105823841` | 238 | 240 EXACT |
| United States `77106053217` | 238 | 240 EXACT |

Both products, `7109517770849` and `7227374534753`, now read true on all three publications: **six parent joins verified**.

The products remain ACTIVE with complete connections containing **27 + 21 = 48 variants**, all reading `availableForSale=true`. Google and Online Store publication remain true. All nine app publications per product match the before-state exactly.

Every shared queried nonpublication field matches both the execution before-state and root's after-state: product identity, title, handle, status, tags, SEO, variant identities, titles, SKU, prices, barcodes, inventory settings/counts and selected options. The swimsuit description SHA-256 equals the approved source-body plan; the dress description SHA-256 equals the private original. Both description comparisons are now independently verified. No supplier URLs or raw descriptions were persisted.

Checks performed: current schema discovery; read-only query validation PASS; fresh five-node query without errors; complete variant/app-publication pagination; exact object comparisons; body hashes with two positive controls. Evidence and sanitized readback are in [market_post_verification.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/market_post_verification.json).

**Limits:** this verifies parent publication. Current connector schema lacks variant publication fields; all variant-level publication is unverified. Admin availability does not prove country-specific checkout availability. Merchant receipt, country eligibility, free-listing serving and commercial outcomes remain unverified. Root owns rendered product/cart checks. Preservation covers queried fields only.

**Next:** root verifies localized buyer paths and fresh Merchant receipt/eligibility, which establish whether this Shopify repair reaches shoppers.

Continuation: “Verify Merchant receipt and country-level free-listing eligibility after the six catalog additions.”
