# Daily Scorecard

Last reconciled: 2026-05-14 11:19 EDT
Data freshness: read-only Google Ads, Pinterest, Merchant, and public/local paid landing reconciliation completed; repo-local GB/CA/AU keyword strategy repair completed; fresh GB/CA/AU Ads monitor and landing gate review completed; post-sanitizer public active-PDP and collection-route preflight completed; owner `$0.15` CPC correction applied; 105-row local keyword universe/rubric created and route holds refined; automation capability inventory and local Merchant capacity diagnosis completed; command-layer integration audit passed with `0` side-document risks; no external writes.

## Required Daily Rows

| Surface | Spend | Clicks | Impr. | Purchases | Revenue | ROAS | Decision | Freshness |
|---|---:|---:|---:|---:|---:|---:|---|---|
| GB exact Search | `$0.00` | `0` | `0` | `0.00` | `$0.00` | n/a | `HEAD_TERMS_REJECTED__015_CPC_VALIDATION_REQUIRED` | Google Ads UI/RPC, `2026-05-14T08:10:31-04:00`; search-term filter cleared; keyword/RSA/final URL checks passed; head terms below first page at `$0.65-$0.74`; active PDP final URL source-clean at `2026-05-14T11:18`; clean-route long-tail rows still need `$0.15` CPC validation |
| CA exact Search | `$0.00` | `0` | `0` | `0.00` | `$0.00` | n/a | `HEAD_TERMS_REJECTED__015_CPC_VALIDATION_REQUIRED` | Google Ads UI/RPC, `2026-05-14T08:10:31-04:00`; search-term filter cleared; keyword/RSA/final URL checks passed; head terms below first page at `$0.65-$0.74`; active PDP final URL source-clean at `2026-05-14T11:18`; clean-route long-tail rows still need `$0.15` CPC validation |
| AU exact Search | `$0.00` | `0` | `0` | `0.00` | `$0.00` | n/a | `HEAD_TERMS_REJECTED__015_CPC_VALIDATION_REQUIRED` | Google Ads UI/RPC, `2026-05-14T08:10:31-04:00`; search-term filter cleared; keyword/RSA/final URL checks passed; head terms below first page at `$0.65-$0.74`; active PDP final URL source-clean at `2026-05-14T11:18`; clean-route long-tail rows still need `$0.15` CPC validation |
| Standard Shopping US | `$0.00` | `0` | `17` | `0.00` | `$0.00` | n/a | `HOLD_MONITOR_NO_WRITE` | Google Ads UI, `2026-05-14T05:35`, reporting day `2026-05-13` |
| Pinterest US paused draft path | n/a | n/a | n/a | n/a | n/a | n/a | `AUTH_BLOCKED_NO_CREATE_CONTROL` | Pinterest public login/sign-up page, `2026-05-14T09:36:32Z` |
| Merchant US/es age_group | n/a | n/a | n/a | n/a | n/a | n/a | `SAMPLE_CLEAR_CURRENT_EXACT_EXPORT_REQUIRED` | Merchant RPC/detail sample readback, `2026-05-14T05:37:54-04:00` |
| Merchant Shopping capacity | n/a | n/a | n/a | n/a | n/a | n/a | `ACCOUNT_WARNING_CONFIRMED__PAID_COHORT_INTERSECTION_PENDING_AUTH_READBACK` | Merchant prioritized fixes page, updated `3:09 AM May 14, 2026`; local diagnosis confirmed Standard Shopping still had `17` impressions yesterday, so exact paid-cohort impact remains unresolved |
| GB/CA/AU active Search landing PDP | n/a | n/a | n/a | n/a | n/a | n/a | `LIVE_SOURCE_CLEAN_CPC_VALIDATION_NEXT` | Public source readback, `2026-05-14 11:18 EDT`: two header/cache variants returned `0` supplier/source-domain hits and `0` URL-like brand attributes on active GB/CA/AU PDP final URLs |
| GB/CA/AU candidate collection routes | n/a | n/a | n/a | n/a | n/a | n/a | `PARTIAL_ROUTE_CLEANNESS__AFFECTED_ROWS_HELD` | Public source preflight, `2026-05-14 11:19 EDT`: `mommy-and-me`, `family-matching`, and `pajamas` clean; `matching-dresses` and `swimsuits` supplier JSON leak; `vacation` `404`; `daddy-and-me` Christmas pattern metadata hits |

## Decision Thresholds To Preserve

- Day 1 growth standard: each day without sales growth, usable learning, or a sales-moving improvement is a failure signal that must produce a same-day next action.
- North Star: produce as many profitable Dress Like Mommy paid-growth sales as possible across Google Ads and Pinterest while targeting about `650% ROAS`.
- Target ROAS: about `650%`.
- Repo-known planning AOV: about `$70`.
- Repo-known target CPA: about `$10.77` at `650% ROAS`.
- Repo-known zero-purchase hard-pause review context: about `$16` spend per smallest decision unit.
- CPC hard cap for active Search repair: owner cannot pay more than `$0.15` per click. Do not bid above `$0.15`; do not treat first-page estimates around `$0.65-$0.74` as acceptable; do not use close-head variants as long-tail strategy.
- Keyword universe rule: build large locally, upload small. Promote only scored `GREEN` rows after active-product, clean-landing, `$0.15` CPC, reviewer, and after-state gates. `YELLOW` rows are local/repair-only; `RED` rows are not paid-Search upload candidates.
- Command-layer integration rule: a new strategy/report/data artifact is not progress unless it is registered, action-linked, continuity-logged, or marked generated/archive. Run the integration audit before stopping.

Do not apply thresholds mechanically without fresh campaign/search-term/landing and conversion evidence.

## Daily Operator Questions

- When did the active test start, and which checkpoint is next: T+24, T+72, or T+7d?
- How many paid-growth sales did we get since yesterday, at what revenue, CPA, and ROAS?
- What happened today, what happened yesterday, and is any metric stale or missing?
- What spent money since the last readback?
- Which clicks were qualified versus waste?
- Did any campaign produce purchase/conversion value?
- Are the keywords proving themselves from daily data, or are they still only a starting hypothesis?
- Which actual search terms justify negatives, expansion, ad copy changes, or landing-page fixes?
- Do the keywords/products/audiences still pass the high-intent, low-waste, low-cannibalization rubric in `expert_growth_playbook_2026.md`?
- Is cheap traffic actually likely to buy, or is it cheap because intent is weak?
- Are search terms actionable and free of stale unrelated filters?
- Is there enough data to scale, hold, pause, reduce, or add negatives?
- If there are zero impressions after 24 hours, what same-day serving diagnosis, long-tail candidate test, auction-entry action, or approval packet is due?
- If there is no learning signal, what exact diagnosis or approval packet is due today?
- Which blocker is stopping the next sales-moving action?

## Today

- No campaign produced cost, purchase count, revenue, or ROAS evidence in the readback window.
- GB/CA/AU fresh read-only monitor is done: campaign/ad-group/scope checks passed, stale search-term filters were cleared, keyword/RSA/final URL checks passed, and keyword UI showed `Eligible (Limited)` / below-first-page-bid estimates around `$0.65-$0.74`. Owner corrected that this fails the hard `$0.15` CPC economics, so head terms and close variants are rejected; active PDP final URL sanitizer now passes public source readback, but clean-route long-tail rows still need authenticated `$0.15` CPC validation.
- Local keyword action completed: `ops/marketing/keyword_universe.csv` has `105` scored rows (`60` US, `15` GB, `15` CA, `15` AU; `77` `GREEN`, `20` `YELLOW`, `8` `RED`) plus `keyword_strategy.md` and `keyword_scoring_rubric.md`. This run refined `live_action` holds for rows routed to `matching-dresses`, `swimsuits`, `vacation`, and `daddy-and-me`; no live keyword upload occurred.
- Command-layer integration action completed: initial audit found `4` side-document risks; current audit covers `25` tracked files with `0` risks after registering/linking/archiving the weak docs.
- Automation capability correction completed: shell/repo writes/network/Playwright MCP are usable, but authenticated Chrome/account surfaces are not equivalent in this runtime because Chrome DevTools is profile-locked and Computer Use interactive access is not granted. Merchant/Pinterest account readbacks must stay explicitly gated as `AUTOMATION_CAPABILITY_MISMATCH` when they depend on those surfaces.
- No scale, pause, bid, budget, negative, product-group, or status write is justified from current metrics until fresh readback, reviewer pass, and green-gated authority support the exact action.
- Standard Shopping visible search terms in saved readback had `0` clicks, `$0.00` cost, and `0.00` conversions; no negative action is justified from `family pictures outfits`, `family same outfit`, or `mommy and me wedding guest dresses`.
- Active-product/category prep map now exists from public storefront collections/products plus the existing `780`-row paid cohort: immediate Father's Day direction is Daddy-and-Me/father-inclusive family matching, not generic or stale seasonal traffic.
- Fastest next sales-moving unblocks are authenticated validation of clean-route GB/CA/AU `GREEN` keyword rows at `$0.15`, repair/reroute of blocked collection routes, Pinterest authenticated access, authenticated Merchant capacity and US/es exact readbacks, and US Standard Shopping query/product/title diagnosis using the new universe.
