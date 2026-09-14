# Independent hosted-image verification

Confidence: H for visible content, dimensions and current CDN availability; M for original-source fidelity.

**RELEASE for the exact six description-image URL substitutions on Product7109517770849.** No image-content blocker was found. This verdict covers replacing the six existing source references with their ordered Shopify-hosted copies. Additional wording, product claims, image order, variant/gallery associations and translated-text changes are outside this image review.

I freshly retrieved the product through Shopify `get_product`, downloaded all six hosted assets plus its 13 current gallery images from Shopify CDN, inspected each hosted image at 800×800, and compared the gallery contact sheet and matching originals.

| Hosted index | Visible content | Gallery comparison |
|---|---|---|
| 1 | Yellow/lime/teal matching adult-and-child top/skirt layout | Closely matches gallery8 |
| 2 | Same colorway; smaller top, skirt and brief flat lay | Consistent design; additional view |
| 3 | Black/green/white matching top/skirt layout | Consistent with gallery2/7/13 colorway |
| 4 | Same colorway; smaller top, skirt and brief flat lay | Consistent design; additional view |
| 5 | Pink/orange matching adult-and-child top/skirt layout | Closely matches gallery4 |
| 6 | Same colorway; smaller top, skirt and brief flat lay | Consistent design; additional view |

All six are decodable RGB JPEGs, **800×800**, approximately **33–48KB**, served at six distinct Shopify CDN URLs. They show clear garments on white backgrounds, without visible seller URLs, watermarks, contact text, people or privacy-sensitive content. No broken frames or material clipping were observed; mild JPEG softness is visible.

Hosted1→gallery8 and hosted5→gallery4 have mean RGB differences of **0.777/255** and **0.696/255**. Neither is pixel-identical. The manifest also reports equal 800×800 dimensions but changed bytes/pixels for source comparisons5/6. These differences are consistent with JPEG reencoding and do not justify a hold.

Privacy metadata checks found no GPS, email/URL text, comments or XMP. EXIF/ICC metadata remains, including an opaque HostComputer tag whose origin was not established. No personal identity was inferred.

**Limit:** direct source comparisons1–4 remain blocked by the previously observed HTTP420; no source retries or bypass occurred. Independent exact source fidelity is therefore unproven. Root's ordered `upload_image(sourceUrl)` provenance plus consistent visible product content is sufficient for this narrow reference replacement, not a claim of byte identity or manufacturer verification.

Evidence: [hosting manifest](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/image_rehosting.json); private inspection receipts, images and comparison sheet under [/tmp/dlm-merchant-audit-20260909/image-inspection](/tmp/dlm-merchant-audit-20260909/image-inspection).

**Next:** root substitutes only the six references, then verifies that only intended URLs changed and images render in affected locales. No external writes or original-audit edits by this verifier.
