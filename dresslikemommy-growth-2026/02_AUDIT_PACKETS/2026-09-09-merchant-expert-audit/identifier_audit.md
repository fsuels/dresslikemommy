# Active-variant identifier audit

Confidence: H for format/checksum results. Before-correction snapshot: **2026-09-09 16:57:16–16:58:58 UTC**. No external mutations or canonical changes.

[JSON evidence](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/identifier_audit.json) preserves raw IDs/barcodes, exact cohorts, timestamps, controls and validation.

**4,945 distinct variants across 240 ACTIVE parents**; 20 pages (19×250 +195), final `hasNextPage=false`. Every product's variant count matches the earlier market inventory. No nonactive-parent rows were returned or included.

| Classification | Variants | Products affected |
|---|---:|---:|
| Empty barcode | 3,712 | 170 |
| Non-GTIN format/length | 0 | 0 |
| Failed checksum | 1,108 | 70 |
| Checksum-valid, manufacturer-unverified | 125 | 57 |

Product sets can overlap. The 170 empty-barcode products have no populated variant barcodes. All 70 other products have populated barcodes and at least one failed checksum.

**All 1,233 nonempty values are 13 ASCII digits.** None are nonnumeric/internal-label strings or unsupported lengths. **89.86% of nonempty values fail checksum.** Their origin remains unknown; numeric format does not establish manufacturer assignment.

Nine barcode values repeat across 18 variants belonging to different products; seven repeated values fail checksum and two pass. Product equivalence was not evaluated.

The check uses [GS1's modulo-10 rule](https://www.gs1.org/services/how-calculate-check-digit-manually): alternating 3/1 weights from the right of the body, then the final check digit. Fifteen positive/negative controls cover GTIN-8/12/13/14, empties, wrong lengths, text, whitespace and Unicode digits. The official GS1 example `6291041500213` is included. Independent Python validation using the complete code, including its check digit, agrees on **every row and control**. Schema and installed-skill query validation passed.

Exact correction cohorts are in JSON:

- **43 failures / two products** belong to root's existing correction: `7109517770849` (25) and `7227374534753` (18). Do not duplicate that work.
- **1,065 failures / 68 other products** form the separate barcode-only review cohort.
- **3,712 empty values** require identifier availability/provenance investigation.
- **125 checksum-passing values** require manufacturer assignment and product-match evidence.

Limits: this is a paginated snapshot, not an atomic transaction. Root's subsequent corrections supersede affected rows. A checksum pass is not a verified GTIN. Never manufacture corrected digits, infer that identifiers do not exist, set `identifier_exists=false`, or mark products custom from this audit.

**Next action:** integrate the exact remaining cohort into root's reviewed containment and provenance work after the current two-product repair.

Full readback design (**NOT RUN**): JSON `validationReadbackDesign` contains the independently validated `VerifyActiveVariantIdentifiers` query. Scan all pages; require identical 4,945 variant IDs/240 ACTIVE parents. Compare every barcode against this snapshot and root's executed clear manifest; untouched values must match exactly. For `k` actual clears: empty `3712+k`, failed checksum `1108−k`, checksum-valid-unverified `125`, format failures `0`. These are conditional expectations. Schema proof: artifact `782ec9f9-f51e-4ee8-9728-73e388f38937`, revision1. No rescan performed.

Continuation: [existing canonical prompt](/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md).
