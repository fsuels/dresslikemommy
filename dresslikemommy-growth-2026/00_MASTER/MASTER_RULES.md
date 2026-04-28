# Dress Like Mommy Growth 2026 Master Rules

## Purpose

This workspace holds evidence, analysis, implementation plans, screenshots, and rollback notes for Dress Like Mommy growth work in 2026.

## Rules

- Preserve raw exports exactly as received under `01_EXPORTS_RAW/`.
- Put derived analysis in `03_LOCAL_ANALYSIS/`, not inside raw export folders.
- Keep audit-ready evidence in `02_AUDIT_PACKETS/` with source filenames, dates, and screenshots when relevant.
- Store screenshots in `05_SCREENSHOTS/` with descriptive, dated filenames.
- Write implementation plans in `04_IMPLEMENTATION_PLANS/` before making broad channel, feed, ad, or storefront changes.
- Put rollback notes and restore artifacts in `06_ROLLBACKS/` before or immediately after any live change.
- Do not place secrets, credentials, access tokens, billing details, or private customer data in this workspace.
- Do not make live changes to Shopify, ads, feeds, Pinterest, Merchant Center, Search Console, or analytics unless the action is explicitly approved by the operator or already requested in the active task.
- Every recommendation should cite concrete evidence from exports, screenshots, repo files, or a captured external-system state.
- Use dated filenames in `YYYY-MM-DD-topic.ext` form unless a source export already has a canonical name.

## Paid Spend Economics

- Current operator economics assumption: all-in non-marketing cost is 50% of selling price, including product cost, shipping, and fees.
- Shopify Cost per item should be populated automatically as `variant price x 0.50` for current active listings and future listings.
- If Shopify Cost per item is missing, `paid_eligible` is false; product-level margin labels are not a substitute for unit cost.
- Marketing cost, returns, and chargebacks are deducted after that 50% all-in cost.
- Current AOV benchmark: $63.25.
- Max CAC at the current AOV is $9.49, calculated as AOV x 15%.
- Required ROAS is 6.67, calculated as revenue / max CAC.
- Product or collection eligibility for paid spend requires known cost/AOV economics. Low-AOV products or unknown-cost products should be excluded until bundled, repriced, or backed by a reliable cost basis.

## Evidence Standard

Each audit packet or implementation plan should answer:

- What source data was used?
- What issue or opportunity was found?
- What action is proposed?
- What result is expected?
- What could go wrong?
- How would the change be rolled back?
