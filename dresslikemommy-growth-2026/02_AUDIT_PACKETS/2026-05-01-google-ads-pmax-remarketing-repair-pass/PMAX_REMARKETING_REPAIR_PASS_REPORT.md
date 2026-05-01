# 2026-05-01 Google Ads PMax And Remarketing Repair Pass

Confidence: H for live status/ad-policy readbacks; M for final launch timing because PMax and Remarketing still depend on product/feed/audience repairs that were not safe to force live in this pass.

## Scope

Owner request: work on fixing the other campaigns so they can eventually become active too.

Coordination respected:
- Did not touch `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`; it remains locked by another agent.
- Did not change Brand Search; it remains the separate `$5/day` controlled test.
- Claimed only the PMax and Remarketing repair workstreams in `ops/AGENT_COORDINATION.md`.

## Non-Negotiable Result

No campaign was enabled.

No budget was raised.

No conversion goals were changed.

No Merchant Center, feed, product-group, audience-upload, or customer-list edit was made.

No new ad copy was uploaded because replacing ads is representational communication to future shoppers and needs action-time owner confirmation before upload.

## Live Readback Summary

| Campaign | ID | Type | Current live status | Budget | Spend | Main live blocker |
|---|---:|---|---|---:|---:|---|
| `PMax: Shopping ads (United States)` | `18154132278` | Performance Max | Paused / `No products for any locations` | `$1.00/day` | `$0.00` | Asset group says products from `truehairwigs`; settings previously read Merchant Center `513542500 - truehairwigs`. |
| `PMax: USA Google Shopping T-Shirts` | `18154132284` | Performance Max | Paused / all asset groups paused | `$1.00/day` | `$0.00` | Asset strength `Poor`, no audience signals/search themes, generic copy, mixed/non-T-shirt product evidence. |
| `Remarketing - Cart Abandoners & Checkout Starters` | `23609373008` | Display | Paused / all ads limited by policy | `$1.00/day` | `$0.00` | Five responsive display ads are `Not eligible` for `Policy (Clickbait)`; Cart/Checkout audiences not eligible. |

## Expert Decision

### `PMax: Shopping ads (United States)`

Decision: `DO_NOT_REPAIR_IN_PLACE_FOR_LAUNCH`.

Reason:
- The live campaign still has `No products for any locations`.
- The asset group readback says `Products from truehairwigs`.
- Prior settings readback recorded Merchant Center `513542500 - truehairwigs / CSS: Google Shopping`.
- A PMax campaign with wrong Merchant/product source is not a cleanup candidate; it is an archive/replace candidate.

Safe next path:
1. Keep paused.
2. Rename/archive later as `DO_NOT_USE_WRONG_MERCHANT_CENTER` only with owner approval.
3. Build a replacement PMax only after Standard Shopping and Merchant Center supplier-domain cleanup pass.
4. Replacement PMax must use `124884876 - Dresslikemommy`, non-overlapping paid-ready products, presence-only US, English, final URL expansion off or URL allowlisted, brand exclusion, audience signals, and campaign-specific assets.

### `PMax: USA Google Shopping T-Shirts`

Decision: `REPAIR_DRAFT_ONLY_DO_NOT_ENABLE`.

Reason:
- The campaign is paused at `$1/day`, but every asset group is paused.
- Asset group readback is `Poor`.
- Current copy says `Matching outfits, dresses` and includes unsupported/weak claims: `Top quality`, `Largest selection`, `factory low prices`, and `free delivery`.
- Product readback shows mixed product and language evidence, including dresses, family sets, shirts, Spanish-language items, and products marked `Excluded product or listing group`.
- This is not a trustworthy T-shirt-only PMax test yet.

Safe next path:
1. Keep paused.
2. Do not enable until there is a verified T-shirt-only paid cohort with AOV, gross margin, and clean landing-page proof.
3. Replace generic asset copy with T-shirt-specific, claim-safe copy from `pmax_tshirts_asset_copy_draft.csv`.
4. Add search themes and audience-signal plan from the drafts in this packet.
5. Only after the feed/product cohort is proven, run a separate activation gate with exact product count, listing groups, final URL setting, brand exclusion, conversion action, budget, and rollback trigger.

### `Remarketing - Cart Abandoners & Checkout Starters`

Decision: `REPAIR_POLICY_AND_AUDIENCES_DO_NOT_ENABLE`.

Reason:
- The campaign is paused at `$1/day`.
- All five RDAs are `Not eligible` because of `Policy (Clickbait)`.
- Current copy uses clickbait/pressure language such as `You Left Something Behind!` and `Complete Your Purchase Today`.
- Two audience segments, `Cart abandoners` and `Checkout starters`, read `Not eligible` with `Audience not eligible`.

Safe next path:
1. Keep paused.
2. Pause or replace the five policy-limited RDAs only after owner confirms the exact upload/edit action.
3. Use `remarketing_policy_safe_rda_copy_draft.csv` for compliant, product-led copy.
4. Repair audience eligibility by lengthening membership duration or broadening the recovery audience only after live audience settings are reviewed.
5. Add converter exclusions before activation.
6. Verify dynamic remarketing/feed status before launch.
7. Run a separate activation gate after ad review and audience eligibility pass.

## Activation Readiness

None of the remaining blocked campaigns is activation-ready today.

Readiness order:
1. Remarketing can become the next repair candidate after policy-safe ads are uploaded and audiences become eligible.
2. PMax T-Shirts can become a later candidate only after a verified T-shirt-only cohort and economics exist.
3. PMax Shopping United States should be replaced, not enabled.

## Owner Confirmation Needed Before Live Uploads

Before I upload or save new ad copy/assets in Google Ads, owner must confirm the exact action because this changes ads that can later be shown to shoppers.

Suggested exact confirmation phrase for the next step:

`APPROVE UPLOAD PAUSED REMARKETING POLICY-SAFE ADS AND KEEP CAMPAIGN PAUSED`

This confirmation should not enable the campaign, raise budget, change conversion goals, upload customer lists, or touch Standard Shopping.

