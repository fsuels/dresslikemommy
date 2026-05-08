# Aggressive Controlled Growth Build Report

Date: 2026-05-06

Owner approval phrase:

`APPROVE AGGRESSIVE CONTROLLED GROWTH BUILD TODAY: READ BACK EACH SURFACE BEFORE EDITING; REPAIR BRAND SEARCH GOVERNANCE AND RSA QUALITY WITH BUDGET AT OR BELOW $2/DAY; READ BACK REMARKETING POLICY/AUDIENCES AND ENABLE WARM REMARKETING AT $1/DAY ONLY IF CLEAN; CREATE A NEW PAUSED US-ENGLISH NONBRAND SEARCH REBUILD WITH TIGHT EXACT/PHRASE AD GROUPS, NEGATIVES, LOW-CPC CONTROLS, AND HIGH-QUALITY RSAS; RUN PINTEREST READ-ONLY TAG/CATALOG/CAMPAIGN GATE; PREPARE PAUSED CA/UK/AU EXPANSION NOTES ONLY; KEEP STANDARD SHOPPING BUDGET, PRODUCT SCOPE, FEED LABELS, PRODUCT GROUP STRUCTURE, CONVERSION GOALS, AND CAMPAIGN STATUS UNCHANGED; NO PMAX ENABLE, NO INTERNATIONAL LIVE SPEND, NO PINTEREST LIVE SPEND, NO PRODUCT SCOPE EXPANSION, NO MERCHANT/SHOPIFY FEED EDITS, AND NO CONVERSION-GOAL CHANGES.`

## Executive Result

Completed the approved controlled growth build without expanding live product scope, feed scope, PMax, international spend, Pinterest spend, or conversion goals.

Live changes made:

- Brand Search governance repaired at `$2/day`.
- Brand Search bid strategy changed to controlled `Maximize clicks` with a `$0.15` max CPC bid limit.
- Old poor Brand Phrase RSA paused.
- New cleaner Brand Phrase RSA created.
- New US-English nonbrand Search rebuild created as paused only.

Live changes not left active:

- Remarketing was enabled only after readback, then immediately rolled back to paused when Google surfaced `Most ads limited by policy`.

Blocked/deferred:

- Pinterest read-only gate could not be completed because the browser opened Pinterest Ads to a login form.
- CA / UK / AU were documented as paused expansion notes only.

## Brand Search

Campaign: `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`

Campaign ID: `23805046526`

Pre-edit readback:

- Status: Enabled.
- Type: Search.
- Budget: `$2.00/day`.
- Conversion goals: `Account-default: Purchases`.
- Bidding had drifted to `Maximize conversions`.
- Ads table showed one enabled Exact RSA with `Average` strength and an old enabled Phrase RSA with `Poor` strength.

Actions:

- Changed bidding to `Maximize clicks`.
- Enabled and saved max CPC bid limit at `$0.15`.
- Paused old poor `Brand - Phrase RSA`.
- Created new `Brand - Phrase` RSA with claim-safe official-store copy.
- Did not upload image, logo, price, or promotion assets under the stale 2026-05-01 asset claim.
- Did not change conversion goals.
- Did not change budget above `$2/day`.

Final readback:

- Campaign status: Enabled.
- Budget: `$2.00/day`.
- Optimization score: `96.8%`.
- Bid strategy type: `Maximize clicks`.
- Apr 29-May 5, 2026: `9` clicks, `10` impressions, `$1.30` cost, `$0.14` average CPC, `0.00` conversions, `0.00` conversion value.
- New Phrase RSA row read back as enabled / eligible / pending.
- Old poor Phrase RSA read back as paused.

## Remarketing

Campaign: `Remarketing - Cart Abandoners & Checkout Starters`

Campaign ID: `23609373008`

Readback before enable attempt:

- Status: Paused.
- Type: Display.
- Budget: `$1.00/day`.
- Conversion goals: Account-default.
- Location: United States.
- Location option: people in or regularly in included locations.
- Language: English.
- Bidding: Maximize conversions.
- Warm audiences included `Product viewers (Retail) (AdWords)`, `Cart abandoners`, and `Checkout starters`.
- Exclusion: `All Converters`.
- Active RDA used generic warm copy: `Dress Like Mommy Styles`, `Matching Family Styles From Dress Like Mommy`, and `Shop matching looks for moms, dads, kids, and families.`
- Five older paused RDAs still showed policy history around `Policy (Clickbait)`.

Action and rollback:

- Campaign was enabled only after the readback suggested the active serving path was clean.
- Immediately after enablement, Google surfaced campaign-level status `Most ads limited by policy`.
- Because the approval allowed enablement only if clean, the campaign was immediately paused again.

Final readback:

- Campaign status: Paused.
- Budget: `$1.00/day`.
- Status detail: `Most ads limited by policy`.
- Apr 29-May 5, 2026: `0` clicks, `0` impressions, `$0.00` cost, `0.00` conversions.

Decision:

- Do not enable remarketing until a fresh approval allows removal/replacement of the old policy-limited RDAs or another clean-policy repair path.

## US Nonbrand Search Rebuild

Campaign: `DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506`

Campaign ID: `23827590655`

Packet:

- `nonbrand_search_paused_rebuild/manifest.json`
- `nonbrand_search_paused_rebuild/web_bulk_upload/00_nonbrand_search_paused_rebuild_web_bulk.csv`
- `nonbrand_search_paused_rebuild/01_ad_group_map.csv`
- `nonbrand_search_paused_rebuild/manual_qa/nonbrand_rebuild_post_import_qa.csv`

Build controls:

- Status: Paused only.
- Budget: `$2.00/day`.
- Bid strategy: Manual CPC.
- Default max CPC: `$0.15`.
- Network: Google Search.
- Location: United States.
- Language: English.
- Themes: Mommy & Me Dresses, Family Matching, Vacation Family, Matching Pajamas, Matching Swimwear, Daddy & Me.
- Ad groups: `12`.
- Keywords: `36`.
- Match types: exact and phrase only.
- Campaign negative keywords: `37`.
- Responsive search ads: `12`.

Landing-page checks before upload:

- `https://www.dresslikemommy.com/collections/mother-daughter-matching-dresses`: usable.
- `https://www.dresslikemommy.com/collections/matching-outfits`: usable.
- `https://www.dresslikemommy.com/collections/matching-family-vacation-outfits`: usable.
- `https://www.dresslikemommy.com/collections/family-pajamas`: usable.
- `https://www.dresslikemommy.com/collections/family-swimsuits`: usable.
- `https://www.dresslikemommy.com/collections/daddy-and-me`: usable.
- `/collections/vacation` returned `404`, so it was not used.

Bulk upload:

- First preview failed because Google Ads bulk upload required language code `en` rather than `English`; no changes were applied.
- Builder was patched, test rerun, and a second preview returned `98` successful changes and `0` errors.
- Applied the clean paused upload.
- Uploads table readback: `Finished successfully`, `98 successful`, timestamp `May 6, 2026 6:25:53 AM New York Time`.

Final campaign readback:

- Status: Paused.
- Type: Search.
- Budget: `$2.00/day`.
- Ad groups: `12`.
- Cost: `$0.00`.
- Clicks: `0`.
- Impressions: `0`.
- Conversions: `0.00`.

Final component readbacks:

- Ad groups page showed `12` ad groups, paused by campaign, default max CPC `$0.15`, Manual CPC, zero spend.
- Keywords page showed `36` keywords, exact/phrase only, paused, max CPC `$0.15`, zero spend.
- Negative keywords page showed `37` campaign-level negatives.
- Ads page showed `12` paused RSAs, pending review, zero spend.

Residual before future enable:

- Settings page did not reliably read back the location option summary due Google UI loading state; keep this as a mandatory future activation readback.
- Do not enable this campaign until location option, policy status, conversion goals, ad review, negatives, and CPC controls are read back cleanly.

## Pinterest Read-Only Gate

Attempted:

- Opened `https://ads.pinterest.com/`.
- Clicked through to Pinterest Ads login.

Readback:

- Browser was not logged into Pinterest Ads.
- Page showed login form requiring email/password.

Result:

- Tag, catalog, campaign, event, and spend gates were not verifiable today.
- No Pinterest edits, campaign creation, budget changes, or spend were made.

## CA / UK / AU Notes

Created notes only:

- `CA_UK_AU_PAUSED_EXPANSION_NOTES.md`

Result:

- No CA / UK / AU campaign was created, enabled, uploaded, budgeted, or targeted in live Google Ads.
- No international live spend was launched.

## Guardrail Confirmation

Confirmed unchanged or not touched in this build:

- Standard Shopping campaign status remained Enabled / Eligible at `$20.00/day` in readback.
- Standard Shopping product scope unchanged.
- Standard Shopping feed labels unchanged.
- Standard Shopping product-group structure unchanged.
- Standard Shopping conversion goals unchanged.
- No Merchant Center edits.
- No Shopify feed edits.
- No product-scope expansion.
- No conversion-goal changes.
- No PMax enablement.
- No Pinterest live spend.
- No international live spend.

## Decision

`AGGRESSIVE_CONTROLLED_GROWTH_BUILD_COMPLETED__BRAND_GOVERNANCE_REPAIRED__REMARKETING_ROLLED_BACK_BLOCKED_BY_POLICY__NONBRAND_SEARCH_CREATED_PAUSED__PINTEREST_LOGIN_BLOCKED__NO_SCOPE_GOAL_FEED_PMAX_OR_INTL_SPEND_EXPANSION`
