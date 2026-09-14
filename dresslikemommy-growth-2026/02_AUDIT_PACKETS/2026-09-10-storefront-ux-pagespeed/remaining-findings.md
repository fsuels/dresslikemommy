# Product-data and payment findings

Observed 2026-09-10 UTC during the website UX audit. These are separate from the theme repair.

## Together Heart sizing and customer copy

- Original audit found28 derived hip/waist cells and internal source-process wording. Independent image comparison matched56 supported garment measurements; no hip/waist measurements existed in that source. This is historical diagnosis, not a current uncorrected source claim.
- The separate source owner completed the primary body and20 existing body translations plus four product-local recurrence artifacts at03:55–03:56UTC. The repair preserved98 variants,11publication relationships,80othertranslations and supported measurements; independent200-check after-readback passed. See ../2026-09-10-together-heart-source-repair/READBACK.md. Do not repeat the source mutation or run product creation.
- This audit then repaired two theme defects in its existing unpublished preview: Arabic dropped49 child offers, and cleanup erased native Japanese prose. V6 actual browser checks verify child/cart/fit-guide behavior and complete Japanese paragraphs with unchanged source tables. See localized-pdp-v6/READBACK.md and browser-after.json.
- Status: SOURCE_AND_RECURRENCE_COMPLETE__THEME_PREVIEW_VERIFIED__PUBLISHED_ACCEPTANCE_PENDING. The published page must be checked after the combined theme release. This task did not write product bodies, variants, translations or the listing prompt.

## Amazon Pay

- Both live and preview cart buttons announced: Amazon Pay is currently not available on this site. Try a different payment option.
- The normal checkout button reached Checkout - Dress Like Mommy with Contact/Delivery/Shipping method/Payment sections and the expected53.98USD total.
- No buyer contact/payment details, payment submission or order was created. The test line was removed; cart0 was verified afterward.
- Status: PROVIDER_ACCEPTANCE_UNVERIFIED. Configuration/account-wide outage is not established. Do not change financial settings or hide the symptom solely to improve an audit score.


## September 11 remaining localization polish

V7 removed the unsupported zero-review endorsement/arrival fallback and repaired runtime collection-name loss in 35 locale templates. Actual English/Spanish/Japanese/Arabic context labels and relevant destinations pass. This is not whole-store localization completion.

- Japanese and Arabic mobile size-selection hints still contain English (for example Pick a size; Arabic also Pick a goal), visibly observed in V7 screenshots.
- Existing Arabic collection names include underscore punctuation. Localized collection classification and all catalog titles were not exhaustively audited.
- These existing source/runtime copy gaps were preserved during the bounded three-file V7 repair. See pdp-clarity-v7/browser-after.json. Keep them open for a separate scoped localization repair; do not label the website perfect.
