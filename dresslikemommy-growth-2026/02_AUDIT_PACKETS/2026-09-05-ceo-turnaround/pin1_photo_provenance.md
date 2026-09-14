# Pin 1 photo provenance

2026-09-06 · Local provenance lookup complete. **AI generation/editing: UNKNOWN. Whether either depicted person was AI-generated: UNKNOWN.** No appearance-based inference was made.

Verified binding: product7533081133153 → `vintage-cottage-floral-mommy-and-me-pajama-set-01.png` in [saved Shopify image metadata:58](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/pinterest_organic_product_source.json:58) → `VC_ORGANIC_01`, `/pins/0/image`, in the [organic queue:58](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/pinterest_organic_pins.json:58). The queue's `modified=false` means the September Pin preparation reused the existing image; it does not certify its original creation history or real-person photography.

The referenced [creation runner:75](/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-vintage-cottage-floral.sh:75) creates product fields/options and then variants. Neither its current147-line version nor its original committed version contains the exact image filename or an image-generation/upload pipeline. Its original tracked addition is commit `41bb31f`, April22,2026, “Add listing assets and automated Shopify product translations.” That commit adds the runner, listing Markdown and Shopify import CSV; its title is not a generation receipt.

The [listing image plan:133](/Users/fsuels/Projects/dresslikemommy/vintage-cottage-floral-listing.md:133) describes a mother-and-daughter lifestyle hero and alt text. A separate hero filename appears at:75. These are proposed content and placement, without a model/tool name, generation prompt, source-image mapping, editing record or photographer/person provenance.

Bounded searches covered the exact filename/product/runner in current packet, canonical worklog/problem tracker, repository text references and named-file Git history. Exact-filename matches were Shopify/feed/Pin references; no original PNG appeared in the repository-visible image filename inventory. Raw exports, external sites/accounts, rollouts and user media folders were not opened. No source URLs or image bytes were copied.

**Disclosure gate:** this evidence supports neither “AI-generated person” nor “unaltered real-person photo.” The smallest missing evidence is the original image-generation/edit receipt or the creator's exact-file confirmation; keep the answer unknown until that evidence exists.

SHA256 source bindings:

- Runner: `3d3d151ced51e7e53262fd6e5c8bf5b96f1f52a12781d3cd7ead916bf0f0963d`
- Listing: `6ba067dcd9e126854142d6bca0fe55fb4a8e09936100470e80bb831418957b9a`
- Organic queue: `27dcaa1644a84f9935b37402db5665f001cbcf3c6392302ce112c1e37c297b8d`
