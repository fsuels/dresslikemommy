# Primary image audit

At 19:12 UTC on September 9, 2026, the Shopify Admin read completed all three pages: **240 distinct active products, each with a Shopify-hosted featured image and known original dimensions**. The product set exactly matches the independently verified full variant scan.

Seven reconciliation checks pass. Every image is at least 500 pixels on both axes and below 64 megapixels. The smallest short edge is 756 pixels. Two images are 1536 × 2730; the other 238 have a short edge below 1500. There are 98 empty alternative-text fields.

Google has announced a 500 × 500 minimum for January 31, 2027, and recommends 1500 × 1500 or higher. The observed parent featured images meet the announced dimensional minimum. Higher-resolution original photography is an improvement opportunity, with the actual purchased piece, color and pattern preserved. [Google image specifications](https://support.google.com/merchants/answer/6324350?hl=en), [2026 changes and enforcement date](https://support.google.com/merchants/answer/16989427?hl=en)

No images or alternative text changed in this audit. The 98 empty alternative-text fields are a storefront accessibility opportunity; they are not established Merchant disapprovals. No synthetic upscaling was used to claim higher original quality.

This is a complete **parent featured-image dimension audit**, not a full visual audit. It does not prove which image Google received for each variant, Google crawl access, file byte size, AI provenance metadata, absence of overlays, product accuracy or eligibility. Variant-specific image matching remains part of the Merchant receiver audit.

Evidence: `primary_image_inventory.json`, `primary_image_verification.json`; comparison denominator: `identifier_post_verification.json`.
