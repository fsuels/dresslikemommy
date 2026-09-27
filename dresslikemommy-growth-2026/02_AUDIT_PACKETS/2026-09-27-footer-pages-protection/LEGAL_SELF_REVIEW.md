# Legal self-review against primary sources + catalog compliance (2026-09-27)

The owner can't pay for an attorney ("I do not have money for that, needs to be free done by you"). What was done instead:

- An independent research agent checked every protective clause against primary government sources: govinfo/eCFR, ftc.gov, leg.state.fl.us, cppa.ca.gov, legislation.gov.uk, eur-lex and accc.gov.au.
- A second agent audited the live catalog, read-only.
- The fixes were applied and read back.

This is not legal advice. It is a verification of the text against the cited rules.

## Policy fixes applied (LIVE_VERIFIED: all 5 policies match `after/policy-*.html`; 20-locale translations re-registered and validated)

| Finding | Source | Fix |
|---|---|---|
| "Processed within 1–3 business days" is read as a ship-by promise under the FTC Mail Order Rule. Real data (16 fulfilled orders since 2025): median 3, 94% within 5, max 10 business days | 16 CFR 435 | Now "ship within 5 business days (most in about 3)". Missed deadline: delay notice before the deadline, with a cancel option; refund within 7 working days or one billing cycle |
| Risk of loss "on delivery" is invalid for EU/UK consumers | CRD Art. 20; UK CRA s.29/31 | Added the EU/UK physical-possession carve-out (Terms §9, Shipping) |
| EU/UK withdrawal can't be conditioned on tags, packaging or Final Sale | CRD Art. 14(2), 16(e); UK CCR reg 34(9), 28(3)(a) | Added override paragraph, sealed-hygiene-only exception, and the Annex I(B) model form with address and signature |
| Hard 7-day defect deadline and "we choose replace/refund" | ACCC 2025 sweep; ACL | "Ideally within 7 days; later reports accepted"; the customer chooses; mandatory ACL guarantee text added |
| Financial-incentive notice lacked a value and method | Cal. Code Regs. tit. 11 §7016(d)(5), §7081 | About $8.50 = 10% of a ~$85 average order (Shopify orders since 2025), method stated |
| Indemnity "including reasonable legal fees" | Fla. Stat. §57.105(7) reciprocity | Removed |
| Reporting deadlines could be read as shortening limitation periods | Fla. Stat. §95.03 | Clarifying clause added. The earlier 1-year limit had already been removed |
| Review removal must be sentiment-neutral | 16 CFR 465.7 | Wording: "the same way regardless of the rating" |
| Final Sale must be disclosed at point of sale | Fla. Stat. §501.142 | Terms state that Final Sale items are labelled on the product page |

Kept as RISKY-low, with hedges in place:
- Collier County venue, with small-claims and local-court carve-outs.
- Class waiver without arbitration, "to the extent permitted".

Not applicable at current size:
- CCPA: thresholds are $26.6M revenue or 100k California consumers.
- Florida Digital Bill of Rights: $1B.

Open, low enforcement risk: a GDPR/UK GDPR Art. 27 representative. It is unverified and costs money.

## Catalog compliance (read-only audit of 270 active products; `compliance/kids_sleepwear.csv`)

- **Country of origin (16 CFR 303.34):** 270 of 270 listings lacked "Imported". Fixed store-wide in the theme (`18a809a`, key `storefront.origin_imported` in 35 locale files). Live locale files were upserted, and theme translations were registered for 20 locales, because ar, he and no ignored the file value. Readback shows "Imported" or its translation on the product page in all 20 locales.
- **Unprovable claims:** "natural and organic materials" on 5 swimsuits and "sun protection / keeping your skin safe" on the long-sleeve cover-up. Removed in English (`productUpdate`) and in 120 translations (20 locales × 6 products; the HTML skeleton equals the live original). Before-state: `before/swimsuit_claim_products.json`.
- **Kids' sleepwear (16 CFR 1615/1616), HIGH RISK:**
  - 42 active pajama listings cover sizes 12M–14.
  - 16 are described as loose or relaxed.
  - None states snug-fit or flame resistance.
  - **Owner decision 2026-09-27: keep selling; ask suppliers for CPSC 1615/1616 test reports or snug-fit measurements + CPC.**
  - The request message (CN/EN) and the per-style supplier list are kept outside the repo, because they contain vendor URLs. They are in the session scratchpad `compliance/SUPPLIER_REQUEST.md` and were sent to the owner. 9 styles need their offer found via BuckyDrop history.
- **Drawstrings (16 CFR 1120):**
  - `summer-plaid-family-matching-set`: the description says "Drawstring Hood… drawcords" on the kids' Hooded Shirt (Child 1–10). The AI photos show no drawstring, and the original listing notes don't mention one.
  - The 1688 source offer is **delisted** (商品已下架). The product may be unfulfillable.
  - **Owner decision: check the photos first. Unresolved:** the real garment can't be confirmed, and there is no source.
