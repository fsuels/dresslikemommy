# 1688 Sourcing Market Focus Fresh Vendor Gates

Date: 2026-05-08

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-08-sourcing-market-focus-fresh-vendor-gates`

## What Changed

- Added sourcing market profiles in `ops/sourcing/sourcing-categories.json`:
  - `balanced`
  - `us` / American Market
  - `eu` / European Market
- Added a `Market focus` selector to the local sourcing dashboard.
- Passed `market_target` through dashboard API calls, helper-browser search opening, collector runs, run metadata, candidate JSON/CSV output, listing prompts, and dashboard cards.
- Added market-specific query modifiers:
  - US: `欧美`, `美国站`, `跨境`, `外贸`
  - Europe: `欧洲站`, `欧美`, `跨境`, `外贸`
- Split search-history rotation by category plus market, so `mommy-and-me:us` and `mommy-and-me:eu` can rotate independently while still skipping already-seen offer IDs across the category.
- Tightened search-stage scoring in US/EU mode:
  - Requires visible current-year/new-style signal or the newer 1688 offer-ID recency proxy.
  - Requires reputable-vendor or demand proof on the search card, such as strong supplier badges, buyer/quality protection, official logistics, repeat-buyer rate, sales volume, years on 1688, or shop rating.
  - Keeps detail-page proof as the `Gold` gate.

## Navigation Repair

After the first market-focus dashboard runs, saved run metadata showed a real bug: the requested query could be Maternity US/EU while the actual loaded 1688 `page_url` was an older unrelated search. That made the app look like it was searching correctly in the browser while no correct new listings appeared.

Fixed on 2026-05-08:

- The CDP collector now opens a controlled tab for the run instead of relying on whichever 1688 tab was already active.
- Before saving any products, it verifies the loaded 1688 `keywords=` URL matches the requested category/market search URL.
- If the page is stale, mismatched, CAPTCHA, or not loaded, the collector fails loudly and saves no mismatched products.
- Target-reviewable runs can now score up to `600` deduped raw cards, so early reject-heavy pages do not fill the old `200` card cap before later queries can produce useful leads.
- The dashboard `Open 1688 Login/Search` flow can recreate a helper tab through CDP when Chrome is connected but has no normal page tabs.
- Dashboard failure messages now distinguish no new cards, requested-search load failure, browser disconnection, and 1688 login/CAPTCHA.

Live readback:

- `ops/sourcing/2026-05-08-024659-maternity-us-1688-auto/` saved `34` new American-market maternity search cards from `9` matching requested pages.
- Navigation mismatch count: `0`.
- Browser/CDP error happened after partial collection in the first readback; the collector now handles that path gracefully for future runs.
- Scoring kept `0` of those `34` cards in Buyer Shortlist because the visible products were generic/ordinary or missing strict maternity photoshoot proof. They are still present in Stored Cards and correctly rejected rather than silently missing.
- A later EU readback hit 1688 CAPTCHA/interception. The repaired collector refused to save mismatched products and the dashboard asks for normal helper-browser recovery.
- Volatile 1688 CAPTCHA query tokens were sanitized from local search history; stable blocked-page paths remain only as blocker evidence.

## Verification

- `jq empty ops/sourcing/sourcing-categories.json`
- `python3 -m py_compile ops/scripts/1688_sourcing_cdp_collect.py ops/scripts/1688_sourcing_score.py ops/scripts/1688_sourcing_dashboard.py`
- `python3 ops/tests/test_1688_sourcing_search_queries.py`
- `python3 ops/tests/test_1688_sourcing_score_detail_gate.py`
- `python3 ops/scripts/1688_sourcing_cdp_collect.py --category maternity --market-target us --limit 80 --port 9333 --query-index -1 --target-reviewable 3 --max-pages-per-query 1`
- `python3 ops/scripts/1688_sourcing_cdp_collect.py --category maternity --market-target eu --limit 60 --port 9333 --query-index -1 --target-reviewable 1 --max-pages-per-query 1`
- `curl -s http://127.0.0.1:8766/api/data`
- `jq empty ops/sourcing/state/search-history.json`
- `rg -n "x5secdata|x5step=" ops/sourcing ops/AGENT_WORKLOG.md ops/AGENT_COORDINATION.md AGENTS.md || true`
- Temporary dashboard smoke test on `http://127.0.0.1:8876/`:
  - `/api/data` returned market profiles `balanced`, `us`, and `eu`.
  - Rendered HTML contained the `Market focus` selector.
- Restarted the local LaunchAgent dashboard on port `8766`; live `/api/data` returned market profiles `balanced`, `us`, and `eu`.
- Dashboard `/api/data` returned `2702` candidates total and `34` candidates from the new Maternity US run.
- `git diff --check` passed for touched sourcing files.

## Guardrails

- No live Shopify product edit.
- No listing draft creation.
- No supplier/source URL written to customer-facing or feed-visible data.
- No Google Ads, Merchant Center, Pinterest, GA4/GTM, theme, feed, campaign, budget, bid, conversion-goal, product-scope, product-group, or feed-label change.
- No 1688 login/CAPTCHA bypass and no credential storage.

## Next

Use the dashboard selector at `http://127.0.0.1:8766/` before clicking `Find 20 Leads`, or use CLI:

```bash
python3 ops/scripts/1688_sourcing_cdp_collect.py --category mommy-and-me --market-target us --limit 200 --query-index -1 --target-reviewable 20 --max-pages-per-query 2
python3 ops/scripts/1688_sourcing_cdp_collect.py --category mommy-and-me --market-target eu --limit 200 --query-index -1 --target-reviewable 20 --max-pages-per-query 2
```

If 1688 shows login/CAPTCHA, use `Open 1688 Login/Search`, clear the normal browser check, and rerun.
