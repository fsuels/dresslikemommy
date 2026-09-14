Confidence: H for file findings; Merchant account logo and approval remain UNKNOWN.

**PASS — independent review; no upload-ready replacement.** I inspected four distinct images, verified the duplicate by hash, and independently matched all five assets to their metadata receipts. Eleven binary checks pass; no image was edited.

Google’s current brand-profile requirements specify a square 500–2000 px image, PNG/BMP/JPEG, at most 5 MB, and small-scale legibility. Brand-management eligibility is separate from file dimensions. [Google requirements](https://support.google.com/merchants/answer/15575415).

- **Current storefront source:** 779×317, PNG/RGB, 170,041 bytes. The gold/brown dress-and-wordmark with pink heart is recognizable, but this rectangular file fails the square specification. It does not establish the Merchant account’s current logo.
- **Old squares:** both 1200×1200 PNG/RGBA, 277,890 bytes, identical SHA-256 `e9dd8804…5b2761`. Genuine outer transparency surrounds a mostly opaque white wordmark band at `(120,404)–(1080,795)`, only **26.07%** of the canvas. Extensive padding and detailed text create a small-scale readability concern; dimensions alone do not make these suitable replacements.
- **Generated v1/v2:** both 1254×1254 PNG/RGB, under 5 MB, but **zero transparency** and visibly baked gray/white checkerboards. Their heavier gold dress outlines retain the motif while omitting the wordmark and heart. Both remain **NOT_FOR_UPLOAD_FAILED_TRANSPARENCY**.

Google identifies excessive whitespace and nontransparent logo backgrounds as quality problems; passing dimensions does not establish approval. [Google logo-quality guidance](https://support.google.com/merchants/answer/15098801).

**Next:** keep the existing account logo unchanged until root can read its actual asset, approval status and brand-profile eligibility. No third generation, image repair, upload or account change occurred. Continuation: “Resume the native logo readback; retain these failed drafts as evidence only.”
