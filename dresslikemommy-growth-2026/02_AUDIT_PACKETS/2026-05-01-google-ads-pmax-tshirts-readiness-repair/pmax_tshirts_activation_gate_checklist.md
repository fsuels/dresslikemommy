# PMax USA Google Shopping T-Shirts Activation Checklist

Status: `LOCAL_PACKET_READY_OWNER_APPROVAL_REQUIRED`.

No live Google Ads, Merchant Center, Shopify Admin, feed, budget, conversion-goal, asset, audience, campaign-status, or product data edits were made in this pass.

## Must Pass Before Any Live Upload Or Enable

- Campaign remains paused before gate starts.
- Owner gives fresh exact approval for the specific live action.
- Budget readback is exact and owner-approved; current continuity says keep PMax paused and do not raise budgets without explicit approval.
- Merchant Center readback confirms account `124884876 - Dresslikemommy`.
- Product scope is the clean review-only cohort in `pmax_tshirts_clean_cohort_review_only.csv` or a newer owner-approved clean cohort.
- Product scope does not overlap the active Standard Shopping test unless the owner explicitly accepts overlap; safest launch waits until the Standard Shopping 48-hour review decision.
- Product rows are all `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready`.
- Product rows are T-shirt-only: no dresses, shorts, overalls, swimwear, trunks, hoodies, sweatshirts, pajamas, or mixed outfit rows.
- Landing URL returns HTTP 200 and does not expose supplier/source domains.
- Final URL expansion is off, or URL expansion is allowlisted only to the approved product URL and other owner-approved T-shirt URLs.
- Brand exclusions are configured if Google Ads UI allows it without enabling AI Max or weakening Brand Search control.
- Campaign URL options/tracking are present or intentionally documented.
- Asset copy uses `pmax_tshirts_asset_copy_final_review_only.csv`; remove old unsupported claims.
- Search themes and audience signals use `pmax_tshirts_search_theme_audience_url_plan.csv`; do not upload Customer Match/PII.
- Conversion goal remains account-default Purchases unless owner approves a separate conversion-goal workstream.
- Final just-in-time readback confirms: paused status, correct budget, correct Merchant, clean product scope, URL control, brand-exclusion posture, English/US scope, asset strength not Poor, and no supplier/source URL text.
- Rollback trigger and owner decision are documented before enabling.

## Current Result

`DO_NOT_ENABLE_YET`.

The local repair packet resolves the broken URL, mixed product scope, weak copy, search-theme/audience plan, and activation checklist on paper. Live upload/enable remains blocked by owner approval and just-in-time readbacks.
