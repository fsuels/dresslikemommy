# Product-data and payment findings

Observed 2026-09-10 UTC during the website UX audit. These are separate from the theme repair.

## Together Heart sizing and customer copy

- Product 7672336646241; public handle together-heart-family-matching-sweaters.
- The visible description includes internal supplied-image/source-chart wording and explicitly states formulas for hip and waist.
- Independent read-only review inspected ops/listings/source-size-chart-together-heart-family-matching-sweaters.png and matched all14rows x4 original garment measurements (length/chest/shoulder/sleeve),56cells, to ops/listings/size-chart-together-heart-family-matching-sweaters.json with zero differences. This proves transcription, not physical measurement.
- The source image contains no hip/waist values. There are28 derived cells across14rows. The runner ops/scripts/create-thrt-together-heart-family-matching-sweatshirts.sh:950 and listing master prompt:264 require these derivations, so body-only cleanup would recur on a runner repeat.
- Concrete proposed correction: replace the28 derived hip/waist cells with an unavailable marker; preserve supported measurements/table structure; remove internal process wording without fabric claims; prepare the corresponding existing translations and inverse payload; reconcile product-scoped runner validation. Do not rerun product creation against the live product.
- Status: OPEN_SOURCE_AND_WORKFLOW_REMEDIATION. No product, translation or listing-prompt mutation was made by this audit. Current live variant/price and user-visible copy were read; the entire catalog was not certified.

## Amazon Pay

- Both live and preview cart buttons announced: Amazon Pay is currently not available on this site. Try a different payment option.
- The normal checkout button reached Checkout - Dress Like Mommy with Contact/Delivery/Shipping method/Payment sections and the expected53.98USD total.
- No buyer contact/payment details, payment submission or order was created. The test line was removed; cart0 was verified afterward.
- Status: PROVIDER_ACCEPTANCE_UNVERIFIED. Configuration/account-wide outage is not established. Do not change financial settings or hide the symptom solely to improve an audit score.

