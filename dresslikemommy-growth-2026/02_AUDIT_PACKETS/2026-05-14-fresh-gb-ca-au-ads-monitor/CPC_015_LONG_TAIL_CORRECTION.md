# $0.15 CPC Long-Tail Correction

Timestamp: 2026-05-14 08:24 EDT

Mode: repo-local packet correction only. No Google Ads, Shopify, Merchant, Pinterest, GA4/GTM, billing, budget, bid, status, keyword, ad, feed, product, conversion, or theme write occurred.

## Correction

Owner CPC ceiling is hard: do not pay more than `$0.15` per click.

The first blocked packet still contained close head-term variants such as `[mummy and me dresses]`, `[mommy and me dresses canada]`, and `[mummy and me dresses australia]`. Those are now rejected as live-action candidates. They are too close to the same obvious auction that already reads `Eligible (Limited)` because `$0.15` is below first-page estimates around `$0.65-$0.74`.

## Revised Rule

No GB/CA/AU keyword addition, phrase test, or auction-entry repair can move from packet to live unless all gates pass:

- Live paid landing sanitizer passes with zero supplier/source URL hits.
- Candidate is a real market-specific long-tail buyer-moment query, not a head term with only `mummy`, `canada`, or `australia` attached.
- Max CPC remains `$0.15`; no bid raise above the cap.
- Read-only Keyword Planner or keyword UI validation shows first-page estimate `<= $0.15`, or the keyword does not show a below-first-page warning at max CPC `$0.15`.
- Landing promise matches the current PDP or a separately approved clean landing.
- Reviewer pass, before-state readback, and after-state readback plan exist.

## Rejected Now

- `[mommy and me dresses]`
- `[mom and daughter matching outfits]`
- `[mother daughter dresses]`
- `[mummy and me dresses]`
- `[mommy and me dresses canada]`
- `[mummy and me dresses australia]`

These may remain live as current diagnostic starter controls until a separately approved change removes or replaces them, but they are not expansion ideas and should not receive bid increases under the `$0.15` economics.

## Revised Packet

Use `exact_scope_bounded_action_packet_blocked.csv`. Its actionable rows are now `long_tail_exact_validation_candidate` only, with status `blocked_landing_and_cpc_validation_required`.

This is not an upload file. It is a bounded validation packet to run after the landing sanitizer gate is clean.
