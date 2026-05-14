# Daily Scorecard

Last reconciled: 2026-05-14 07:52 EDT
Data freshness: read-only Google Ads, Pinterest, Merchant, and public/local paid landing reconciliation completed; no external writes.

## Required Daily Rows

| Surface | Spend | Clicks | Impr. | Purchases | Revenue | ROAS | Decision | Freshness |
|---|---:|---:|---:|---:|---:|---:|---|---|
| GB exact Search | `$0.00` | `0` | `0` | `0.00` | `$0.00` | n/a | `ACTION_DUE_NOW__T24_ZERO_IMPRESSION_DIAGNOSE_LONGTAIL` | Google Ads UI/RPC, `2026-05-14T05:34:01-04:00`, reporting day `2026-05-13` |
| CA exact Search | `$0.00` | `0` | `0` | `0.00` | `$0.00` | n/a | `ACTION_DUE_NOW__T24_ZERO_IMPRESSION_FILTER_BLOCKED` | Google Ads UI/RPC, `2026-05-14T05:34:01-04:00`, reporting day `2026-05-13` |
| AU exact Search | `$0.00` | `0` | `0` | `0.00` | `$0.00` | n/a | `ACTION_DUE_NOW__T24_ZERO_IMPRESSION_FILTER_BLOCKED` | Google Ads UI/RPC, `2026-05-14T05:34:01-04:00`, reporting day `2026-05-13` |
| Standard Shopping US | `$0.00` | `0` | `17` | `0.00` | `$0.00` | n/a | `HOLD_MONITOR_NO_WRITE` | Google Ads UI, `2026-05-14T05:35`, reporting day `2026-05-13` |
| Pinterest US paused draft path | n/a | n/a | n/a | n/a | n/a | n/a | `AUTH_BLOCKED_NO_CREATE_CONTROL` | Pinterest public login/sign-up page, `2026-05-14T09:36:32Z` |
| Merchant US/es age_group | n/a | n/a | n/a | n/a | n/a | n/a | `SAMPLE_CLEAR_CURRENT_EXACT_EXPORT_REQUIRED` | Merchant RPC/detail sample readback, `2026-05-14T05:37:54-04:00` |
| Merchant Shopping capacity | n/a | n/a | n/a | n/a | n/a | n/a | `DIAGNOSE_READONLY` | Merchant prioritized fixes page, updated `3:09 AM May 14, 2026` |
| GB/CA/AU active Search landing PDP | n/a | n/a | n/a | n/a | n/a | n/a | `LOCAL_FIX_READY_LIVE_SYNC_REQUIRED` | Public/live source plus local theme readback, `2026-05-14 06:05 EDT` |

## Decision Thresholds To Preserve

- Day 1 growth standard: each day without sales growth, usable learning, or a sales-moving improvement is a failure signal that must produce a same-day next action.
- North Star: produce as many profitable Dress Like Mommy paid-growth sales as possible across Google Ads and Pinterest while targeting about `650% ROAS`.
- Target ROAS: about `650%`.
- Repo-known planning AOV: about `$70`.
- Repo-known target CPA: about `$10.77` at `650% ROAS`.
- Repo-known zero-purchase hard-pause review context: about `$16` spend per smallest decision unit.
- CPC preference: keep tests tight; user has repeatedly treated `$0.25` CPC as expensive and prefers closer to or below `$0.20` where possible.

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
- GB/CA/AU crossed the T+24 zero-impression action line in saved evidence; same-day serving diagnosis and long-tail/auction-entry planning are now due.
- No scale, pause, bid, budget, negative, product-group, or status write is justified from current metrics until fresh readback, reviewer pass, and green-gated authority support the exact action.
- Standard Shopping visible search terms in saved readback had `0` clicks, `$0.00` cost, and `0.00` conversions; no negative action is justified from `family pictures outfits`, `family same outfit`, or `mommy and me wedding guest dresses`.
- Active-product/category prep map now exists from public storefront collections/products plus the existing `780`-row paid cohort: immediate Father's Day direction is Daddy-and-Me/father-inclusive family matching, not generic or stale seasonal traffic.
- Fastest next sales-moving unblocks are a scoped paid-landing theme sanitizer sync/readback, Pinterest authenticated access, and current exact Merchant readback so old US/es age_group evidence does not keep driving repair packets.
