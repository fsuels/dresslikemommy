# Website and Google Ads logo release — September 23, 2026

Owner explicitly authorized the new design on both website and Google Ads. Parent task01a0cf24 is sole writer; ad_review is independent read-only reviewer. Scope: header/logo/favicon settings and same campaign24273103416 logo association. No delivery, keyword, budget, bid, billing, tracking, product or translation changes.

## Source and before-state

Candidate creative/dress-like-mommy-matching-dresses-logo-v2.png SHA25650e520b50d3bed2f9a71840a4bdd6d16b1e5e478f3b61799f1e3e6836ace1b08,1254square RGB PNG. Shopify supported upload succeeded as MediaImage33303132962913, filename dress-like-mommy-matching-dresses-logo-v2.png, CDN https://cdn.shopify.com/s/files/1/1557/1635/files/dress-like-mommy-matching-dresses-logo-v2.png?v=1790185616 . This is hosted-media proof, not website publication.

Fresh MAIN133290917985 named dresslikemommy/main, processingfalse. Actual bodies of header.liquid,settings_data.json,settings_schema.json and peer cart.js all equal local388e8f91; remote main also388e8f91. Baseline captured in website-logo-before.json. Catalog owner tool status notLoaded / failed capacity; no active Gitwriter or staged files observed. Exact three-file integration interval claimed, preserving peer scopes.

## Patch

config/settings_data.json selects new logo and favicon,60pxdesktop logo width and opt-in store-name label. config/settings_schema.json adds merchant checkbox defaultfalse. sections/header.liquid adds responsive icon/name layout to both header-position branches; decorative icon alt empty when visible escaped store name supplies accessible name; prior false/absent-logo behavior retained. Native image_url/image_tag resizing preserved. No layout/theme.liquid change needed because existing favicon uses settings.favicon.

## Validation

Skill documentation search succeeded using bundledNode. SystemNode has missing simdjson dylib. Required skill validator was attempted and could not load @shopify/theme-check-common. Used already-installed Shopify CLI with bundledNode as existing documented fallback: theme check exit0 and JSON[] (no reported offenses). Config JSON parses, scoped diff-check passes. Independent ad_review source verdict PASS. This was the pre-release validation checkpoint; live layout, actual bodies, favicon and native Ads after-state subsequently passed as recorded below.

## Release result

Commit587bf21079aec78bc63a41d6af3ad14ecab5ead1 pushed normally to origin/main. Fresh528-file MAIN manifest differed from HEAD only in the exact three logo files, with no missing files; cart.js matched. Native existing MAIN Reset to latest commit confirmed once. Actual published bodies of all three changed files and preserved cart.js now exactly match local source. Website header, name and favicon are LIVE VERIFIED. Shopify API still reports processing=true at the final recorded source read; actual file bodies and public render are stronger release evidence, but processing completion is not claimed.

Root visually verified the home header on desktop (1265px content width), 390px and 320px mobile. Brand fits without overlapping search/cart; 320px has9px gaps. All six saved ad landing URLs and Danish home load the same new mark/name at320px with scrollWidth320. Locale-aware home links preserved. CDN original HTTP200 PNG1254square has different encoded bytes but decoded RGB pixels exactly equal the candidate. Live favicon HTTP200 PNG32square was visually inspected. Temporary viewport override cleared.

After landing consistency passed, root clicked the native Google parent Save once. Fresh campaign Associations table has exactly one enabled Business logo at Campaign level, correct V2 thumbnail, Pending / Under review, added by Advertiser, native last updated Sep23 2026 2:07PM. Campaign24273103416 header remains Paused, USD210/campaign, Sep22–28. The image source is https://tpc.googlesyndication.com/pimgad/11216358216418686120 (image identifier, not asserted asset ID). Logo is applied/submitted; approval and serving are not yet verified. No delivery/status/keyword/bid/budget/tracking change. Excellent ad strength remains unresolved.

Evidence: logo-release-verification.json, website-logo-final-source.json, website-logo-cdn-verification.json and creative/favicon-live-32.png. Smallest rollback: revert only exact logo commit and remove only new campaign logo association; retain uploaded files and unrelated source changes. Original Google tab retained, public home left available, temporary Shopify admin tab closed. Independent final source review is recorded separately.


## Independent final source review

ad_review: PASS_WITH_LIMITS, DID_NOT_BUILD_OR_EXECUTE. Independently recomputed all four saved source bodies against local/declared MD5, preserved cart.js against before-state, candidate decoded RGB hash against recorded CDN hash, and favicon dimensions/hash/visual recognition. CDN raw1254response is not retained, so reviewer did not independently replay CDN decode; root equality check is recorded separately. Public browser and native Google observations are root-supplied, not reviewer replay. Accurate limits retained: Shopifyprocessingtrue metadata, GooglePendingreview, and unresolvedExcellent. Reviewer found one stale pre-release validation sentence; it is corrected above.


## Final closeout checks

Cockpit regeneration PASS; command-layer integration25/25 with0risks PASS; bundledPython strict continuity10/10 CONTINUITY_OK; scoped git diff --check PASS. All3themefiles and preserved cart.js are clean after commit587bf21. Independent final review PASS_WITH_LIMITS above; unrelated dirty operations/peer changes left intact.
