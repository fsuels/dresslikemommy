Agent Guide – dresslikemommy

Scope and purpose
- This file applies to the entire repository. It explains how agents should work on this theme and how to resume work across sessions.

Principles
- Evidence-first: Base every finding on repo files; never invent facts.
- Minimal, focused changes: Keep edits surgical and consistent with Dawn style.
- Shopify constraints: No secrets in theme; no server code in Liquid; use App Proxies for backend.
- Observability: Always leave notes in ops/AGENT_WORKLOG.md when you change or defer something.

Continuity (resume work in new sessions)
- Read ops/AGENT_WORKLOG.md (latest entries at bottom) to get current status, decisions, TODOs, and next steps.
- Read `ops/AGENT_COORDINATION.md` before touching external systems or shared workstreams; honor active locks and claims.
- Also review this AGENTS.md and the diffs in layout/theme.liquid, sections/main-product.liquid, snippets/cart-drawer.liquid, snippets/meta-tags.liquid, assets/analytics.js for context.
- If context is tight, search for the string: AGENT_CONTINUITY_ANCHOR in the worklog to jump to the latest checkpoint.
- Treat this `AGENTS.md` file as the automatic bootstrap memory. If the user pastes an older continuation prompt or stale anchor, reconcile it against `AGENTS.md`, `ops/AGENT_COORDINATION.md`, and the durable continuity file before acting.
- Shopify Admin API continuity: operator-managed Admin API access exists via the `n8n Integration` app. Canonical local credential sources are `~/.config/dresslikemommy/shopify-admin.env`, `~/.config/dresslikemommy/admin-api-token.json`, and `~/.config/dresslikemommy/translation-helper-token.json`; credentials must stay outside the repo/worklog/theme files. If environment variables are unset in a future shell, describe that as "credentials not loaded in this shell" rather than "no API access exists." If a provided token starts returning `401 Invalid API key or access token`, treat that as "stored token requires regeneration/reinstall" rather than assuming the store lacks API access.

Active workstream coordination (critical)
- Before editing Google Ads, Merchant Center, Shopify Admin, GA4/GTM, Pinterest, live product data, paid-feed artifacts, or theme files, check `ops/AGENT_COORDINATION.md`.
- One writer per campaign/feed/product cohort/theme area. Read-only audits may run in parallel, but writes require a narrow active claim in `ops/AGENT_COORDINATION.md`.
- Do not clear or override another agent's lock unless the owner explicitly says the workstream is transferred, abandoned, or complete.
- Standard Shopping supplier/source-url repair was completed on 2026-05-01 after owner-directed continuation. After fresh owner approval and clean just-in-time readbacks, `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` was re-enabled on 2026-05-01 with no budget, product-scope, product-group, feed-label, feed, or conversion-goal changes. Do not pause/disable/re-enable it again, change budget, edit product groups/feed labels, upload feeds, or change conversion goals without fresh explicit owner approval.

Google Ads continuity (critical memory)
- Before any Google Ads, Merchant Center, GA4, Shopify tracking, or paid-campaign work, read `ops/GOOGLE_ADS_CONTINUITY.md` first, then the latest `ops/AGENT_WORKLOG.md` entries.
- Latest Google Ads continuity anchor as of 2026-05-01: `AGENT_CONTINUITY_ANCHOR: 2026-05-01-paid-media-combined-memory-refresh`.
- Supersedes stale Google Ads prompt/anchor `AGENT_CONTINUITY_ANCHOR: 2026-04-30-google-ads-continuity-memory`; do not use the old anchor as current state.
- Current paid-media posture as of that anchor:
  - Owner reported pausing `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` after finding an unacceptable supplier/source URL exposure risk.
  - Owner then gave the exact approval phrase `APPROVE RE-ENABLE DLM_US_STANDARD_SHOPPING_TEST_PAID_READY NOW WITH NO BUDGET, PRODUCT SCOPE, OR CONVERSION GOAL CHANGES`.
  - Standard Shopping was re-enabled on 2026-05-01 only after just-in-time clean readbacks: Merchant Center supplier-domain searches returned `0` rows for `1688.com`, `detail.1688.com`, `alibaba.com`, and `aliexpress.com`; Google Ads row readback showed status icon `Enabled`, `$20.00/day`, campaign ID `23802638621`, and no supplier-domain text; Shopify paid-cohort readback showed `780` paid rows across `81` active Online Store products and `780` available variants with `0` inactive/unavailable rows.
  - The original controlled 48-hour Standard Shopping test was `$20.00/day`, started 2026-04-30 19:09 EDT, review/rollback due 2026-05-02 19:09 EDT.
  - CPC guardrail remains max CPC `0.25`.
  - Product scope remains `custom_label_4=us_test_ready` AND `custom_label_0=paid_eligible`; product group `Everything else in "All products"` is excluded.
  - Location remains United States with `Presence: People in or regularly in your included locations`.
  - Brand Search `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` is live/eligible as a controlled test at `$5.00/day`, after owner approval and owner budget change from `$1.00/day`.
  - Brand Search readback shows `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions, `Maximize clicks`, Google Search Network only, and `Account-default: Purchases`.
  - Brand Search repair status: Poor Phrase RSA is paused; clean Exact and Phrase RSAs read `Eligible / Pending`; core exact/phrase brand keywords are eligible; two low-search-volume exact keywords remain paused.
  - Brand Search expert pass on 2026-05-01 reconciled an external AI review against live readbacks. No additional live edits were applied: the Poor RSA was already paused, low-search-volume keywords were already paused, conversion primary changes remain blocked without separate explicit approval, and negative pruning/promo/social-proof claims were not evidence-supported.
  - Brand Search fresh premium asset pass on 2026-05-01 superseded the reused-image recommendation set. Upload-ready packet exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-fresh-premium-assets/` with 5 new image assets, 1 official-logo export, proof-backed price rows, and promotion deferred. No live asset upload/association was made; upload requires fresh owner action-time approval.
  - Both PMax campaigns remain paused/blocked. A 2026-05-01 PMax/Remarketing repair packet exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-remarketing-repair-pass/`.
  - `PMax: Shopping ads (United States)` should not be repaired in place for launch because of wrong Merchant/no-products risk; replacement/archive is safer. A local replacement-readiness packet exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-shopping-replacement-readiness/`. No live PMax edit, shell creation, asset upload, budget change, product-scope change, conversion-goal change, archive/rename, or enable was made; next live step requires fresh exact owner approval.
  - `PMax: USA Google Shopping T-Shirts` now has a local-only readiness repair packet at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-tshirts-readiness-repair/`. It supersedes the old draft URL `/collections/matching-t-shirts` because that URL returned 404; the packet narrows scope to one clean paid-ready T-shirt product / 42 variants with claim-safe copy and activation gates. No live upload, product-scope change, asset association, budget change, campaign unpause/enable, Merchant/feed edit, Shopify product edit, or conversion-goal edit was made; live PMax remains blocked pending fresh owner approval and just-in-time readbacks.
  - Remarketing launch-control repair later completed as warm remarketing, not pure cart/checkout-only. It remains paused at `$1.00/day`; `Product viewers (Retail) (AdWords)` was added as the eligible warm serving bridge, `Cart abandoners` and `Checkout starters` remained targeted, `All Converters` remained excluded, optimized targeting remained off, dynamic ads remain connected to Merchant feed `124884876`, feed product filter remains `Labels is us_test_ready` AND `Labels is paid_eligible`, and the active RDA was rewritten to generic warm policy-safe copy with `Excellent` ad strength. Evidence packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-remarketing-launch-control-repair/`.
  - Remarketing enable still requires fresh exact owner approval; do not enable it by inference.
  - Shopify vendor/source URL cleanup removed exact supplier URL tags from `263` live products; post-cleanup live Shopify scans found `0` vendor URL tags/title/body/SEO/metafield leaks across `803` products.
  - Merchant Center stale supplier-domain rows were removed for affected archived/unpublished products and Google-unpublished safety-hold products; one newly surfaced active Google-published product (`6724261019745`) was safety-unpublished from Google & YouTube before stale Merchant rows were deleted.
- If a new session starts after 2026-05-02 19:09 EDT and no newer owner approval is documented, immediately run the `$20/day` review from `ops/GOOGLE_ADS_CONTINUITY.md`; if the owner is unavailable, the safe default remains the documented rollback procedure.
- Never enable PMax or Remarketing; never raise Brand Search above `$5.00/day`; and never pause/disable/re-enable Standard Shopping, increase budgets, expand product scope, or change conversion goals without fresh explicit owner approval in the current session.
- Never write vendor/source URLs into Shopify tags, title, SEO, body copy, product type, customer-visible metafields, feed-visible metafields, or any sales-channel-visible product data. Source URLs belong only in local operator evidence files.
- For a fresh Google Ads session, the reusable handoff prompt lives at `ops/prompts/google-ads-continuation-prompt.md`.

1688 sourcing dashboard continuity (critical memory)
- The user is building a semi-automated 1688 -> Shopify product pipeline for Dress Like Mommy. Current goal: keep a beautiful local dashboard full of pre-filtered 1688 candidates by website category, let the user Keep/Reject, save evidence, then generate a draft package for Shopify listing/image agents.
- Do not restart this from scratch. Phase 1 already exists as a browser-assisted sourcing scorecard and local dashboard.
- Main local app:
  - Dock/app path: `/Users/fsuels/Applications/Dress Like Mommy Sourcing.app`
  - Desktop backup: `/Users/fsuels/Desktop/Dress Like Mommy Sourcing.app`
  - Bundle id: `com.dresslikemommy.sourcingdashboard`
  - Dashboard URL: `http://127.0.0.1:8766/`
  - Auto-start LaunchAgent: `/Users/fsuels/Library/LaunchAgents/com.dresslikemommy.sourcing-dashboard.plist`
  - Start script: `ops/sourcing/start-sourcing-dashboard.sh`
  - Branded icon source/assets: `ops/sourcing/app-icon/`
- Dashboard implementation:
  - `ops/scripts/1688_sourcing_dashboard.py`
  - Reads all `scored-candidates.json` files under `ops/sourcing/**`.
  - Serves `/api/data` and a local image proxy `/image?url=...`.
  - Product images are cached under `ops/sourcing/image-cache/` because Alibaba hotlinking can show blank images in Chrome.
  - User-facing controls include Find 20 Leads, Open 1688 Login/Search, Ask project memory, Save, Reject/Restore, Open 1688, Verify Detail Proof, Save Proof, Draft Package, Copy Listing Agent Prompt, Copy 6-Image Prompt, and category/status filters.
  - `Ask project memory` is backed by the local MemPalace pilot under `~/.cache/dresslikemommy/mempalace-pilot-*`. It must show a plain-English answer first and keep technical source snippets hidden behind source details; the user does not want code-like memory output.
  - Plain-language labels are intentional: Stored Cards = all raw saved cards; Buyer Shortlist = fresh/category-fit leads not rejected; Saved = user clicked Save/Keep; Ready for Draft = proof fields filled; Rejected = remembered rejects; Best Leads = internal Gold; Unverified Leads = internal Test.
  - Dashboard candidate loading dedupes repeated 1688 offer IDs and keeps the best/current card, so repeated searches should not show the same product over and over.
  - `/api/browser-status` checks the Chrome helper tab before collection. If 1688 is on login, CAPTCHA, `Captcha Interception`, `_____tmd_____`, or a punish URL, the dashboard must show the blocker and not create a fake empty run.
  - `Open 1688 Login/Search` must reuse the existing helper Chrome tab through CDP when possible. Do not open a fresh tab every click.
- Sourcing/scoring implementation:
  - `ops/scripts/1688_sourcing_cdp_collect.py`: logged-in Chrome DevTools Protocol collector for real 1688 searches, default CDP port `9333`.
    - `Find 20 Leads` passes roughly `--query-index -1 --target-reviewable 20 --limit 200 --max-pages-per-query 2`, which tries configured category keywords and aims for 20 `Test`/`Gold` candidates without opening blind server scraping.
    - Query order rotates via `ops/sourcing/state/search-history.json`, and the collector skips already-seen offer IDs from prior scored runs/search history so repeated clicks do not keep collecting the same first-page products.
  - `ops/sourcing/1688-browser-collector.js`: fallback browser-console collector when CDP is blocked by login/CAPTCHA.
  - `ops/scripts/1688_sourcing_score.py`: scores candidates and writes `shortlist.html`, `scored-candidates.csv`, `scored-candidates.json`, and `summary.md`.
    - Search-stage scoring should keep plausible products as `Test`/`Unverified Leads` only when they have real visible category fit, usable images, low MOQ, visible 2025/2026/new-style signal or a newer 1688 offer ID plus demand/fulfillment signal, and at least one good signal such as sales, repeat rate, dropship wording, stock/dispatch, or strong score. Do not mark a product `Gold` until detail-page proof is strong.
    - Detail-stage scoring is the Best Lead gate. `Gold` is impossible unless the product has supplier proof, size-chart proof, dropship/one-piece proof, dispatch or ready-stock proof, usable vendor images, category fit, freshness/no-IP-risk evidence, and enough score. Missing critical detail proof should keep the product `Test` or `Reject`, not `Gold`.
    - `MIN_FRESH_OFFER_ID` is currently `850000000000`. This is a practical 1688 recency proxy: old offers can have edited titles that say 2026, so search-stage cards below this threshold should be hidden from the Buyer Shortlist unless future detail-page proof justifies changing the rule.
    - Hard rejects at search stage are for previous operator rejects, older 1688 offer IDs, stale year signals such as 2020-2024 in 2026, no visible freshness signal and no newer-offer/demand proxy, wrong category, missing URL/image, high MOQ, explicit no-dropship/no-size-chart evidence, or brand/IP risk.
    - The scorer rechecks visible text for category fit; do not trust old `category_match=5` values or the search keyword alone if the title/raw card text does not actually mention mother/daughter, father/child, family, couple, maternity, or a clear men+women/couple product pattern. This prevents broad queries from filling Mommy & Me with generic women's dresses.
    - Search-card `Sales` is only the number visible on 1688. If the page does not show a time window, treat it as a popularity clue and confirm on the detail page.
    - If 1688 redirects to a `Captcha Interception` / `_____tmd_____` page, the collector should fail loudly and ask for browser recovery; do not create a normal empty/successful run. If CAPTCHA happens after partial collection, keep the saved run artifacts but report the collection as blocked.
  - `ops/scripts/1688_sourcing_detail_enrich.py`: logged-in Chrome detail-page verifier for shortlisted products.
    - Opens normal 1688 detail pages through CDP port `9333`; it must not bypass login/CAPTCHA.
    - Extracts supplier name/URL, badges, years/rating when visible, dropship terms, dispatch/stock text, size-chart text, availability, IP-risk text, sales/repeat clues, and product images.
    - Downloads vendor images under `ops/sourcing/vendor-images/<offer-id>/` and writes detail artifacts under `ops/sourcing/detail-enrichment/<offer-id>/`.
    - Updates `ops/sourcing/state/decisions.json` with structured proof fields and updates `ops/sourcing/state/vendors.json` when supplier identity is captured.
    - Detail outputs should override search outputs for the same offer ID in the dashboard so a detail `Reject` cannot remain visible as a search `Test`.
  - Always pass `--decision-state ops/sourcing/state/decisions.json` when scoring real candidates so rejected products stay rejected.
- Categories are configured in `ops/sourcing/sourcing-categories.json`:
  - `mommy-and-me` / Mommy & Me
  - `daddy-and-me` / Daddy & Me
  - `family-matching` / Family Matching
  - `couples` / Couples
  - `maternity` / Maternity
- Persistent memory:
  - Keep/Reject decisions and evidence live in `ops/sourcing/state/decisions.json`.
  - Supplier memory lives in `ops/sourcing/state/vendors.json` once detail enrichment captures supplier identity.
  - Search/query memory lives in `ops/sourcing/state/search-history.json`; use it to rotate starting queries, track blocked runs, and avoid already-seen offer IDs.
  - A rejected 1688 offer ID must not be researched again unless the user restores it.
  - Evidence fields saved by the dashboard: size chart source, vendor images path, generated images path, dropship confirmation, dispatch confirmation, supplier confirmation, and notes.
  - A product becomes `Ready` only after required proof fields are filled.
- Draft package handoff:
  - Dashboard writes packages under `ops/sourcing/draft-packages/<1688-offer-id>/`.
  - Package files: `candidate.json`, `listing-request.txt`, `photoshoot-prompt.md`, `draft-agent-prompt.md`, `README.md`.
  - `draft-agent-prompt.md` is the safest handoff for creating a Shopify DRAFT product. It explicitly says not to publish live unless the operator asks.
- Canonical prompts connected to the dashboard:
  - Listing prompt wrapper points to `ops/prompts/START-HERE.md`, `ops/prompts/shopify-listing-master-prompt.md`, and `ops/prompts/shopify-listing-from-1688.md`.
  - Six-image photoshoot prompt source is `ops/prompts/dlm-6-image-photoshoot.md`.
  - Photoshoot workflow generates one 9:16 image at a time and waits for `NEXT`; do not create collages/grids.
- Real runs already exist:
  - Original family matching run: `ops/sourcing/2026-04-25-family-dress-shirt-1688/`
  - Automatic category runs: `ops/sourcing/2026-04-24-2354-*-1688-auto/`
  - Last known tuned Mommy & Me run before the offer-ID gate: `ops/sourcing/2026-04-25-0056-mommy-and-me-1688-auto/` produced 32 candidates, 8 fresh `Test` / `Unverified Leads`, 0 `Gold`, 24 `Reject` after stale-year/no-freshness filtering.
  - After the offer-ID freshness gate was added, the dashboard showed 63 deduped stored cards but only 6 active Buyer Shortlist leads total, with 3 in Mommy & Me and 3 in Family Matching. This lower number is intentional until detail-page enrichment can prove more products are worth listing.
  - Operator test on 2026-04-25 with the 20-lead target: `ops/sourcing/2026-04-25-0150-mommy-and-me-1688-auto/` was rescored to 2 real Mommy & Me `Test` leads and 47 rejects. A later app run `ops/sourcing/2026-04-25-015839-mommy-and-me-1688-auto/` checked 3 pages of one Mommy & Me query, found only generic women's dresses, saved 0 reviewable leads, and then 1688 forced `Captcha Interception`.
  - Latest app run on 2026-04-25: `ops/sourcing/2026-04-25-023954-mommy-and-me-1688-auto/` collected 108 new Mommy & Me cards and 16 new `Test` leads before 1688 forced `Captcha Interception`. Dashboard counts after the run: Mommy & Me 21 active/Test, Family Matching 3 active/Test, Daddy & Me 0, Couples 0, Maternity 0. Continue with Daddy & Me only after the user clears the helper-browser CAPTCHA.
- How to open/run:
  - Preferred: open `/Users/fsuels/Applications/Dress Like Mommy Sourcing.app` or click the Dock icon.
  - Manual: `python3 ops/scripts/1688_sourcing_dashboard.py --open`
  - In the app, click `Find 20 Leads` to run the collector from the dashboard. It tries configured keywords for the selected category, skips seen offers, checks up to two pages per query, and targets up to 20 reviewable products. If 1688 requires login/CAPTCHA, click `Open 1688 Login/Search`, let the user handle login/CAPTCHA, then click `Find 20 Leads` again.
  - Fill one category with the current 20-lead behavior: `python3 ops/scripts/1688_sourcing_cdp_collect.py --category mommy-and-me --limit 200 --query-index -1 --target-reviewable 20 --max-pages-per-query 2`
  - Fill all categories: `python3 ops/scripts/1688_sourcing_cdp_collect.py --category all --limit 200 --query-index -1 --target-reviewable 20 --max-pages-per-query 2`
- Browser/login safety:
  - Use logged-in browser-assisted workflows; do not do blind server scraping.
  - Do not store 1688 credentials in the repo, worklog, prompts, or generated files.
  - Do not bypass CAPTCHA, browser safety barriers, paywalls, or HTTPS warnings.
  - If 1688 asks for manual login/CAPTCHA, ask the user to take over or use the console collector after login.
- Next best product-finder improvements:
  - Follow `ops/sourcing/SOURCING-IMPROVEMENT-ROADMAP.md` for the agreed audit plan.
  - Add detail-page enrichment behind saved `Unverified Leads` products so supplier evidence, dispatch speed, dropship support, size chart detection, and image download paths can be filled automatically before marking products Gold.
  - Tune category-specific queries next for Daddy & Me, Couples, and Maternity using the same "target up to 20 reviewable candidates" loop, but do not loosen category-fit so much that generic clothing fills the shortlist.
  - Keep all generated tooling dev/operator-side only; do not add AI UI or backend agent references to the live Shopify theme.

Canonical listing workflow
- For any task that creates or updates Shopify product listings from vendor pages, size charts, or dropship source material, first read `ops/prompts/START-HERE.md`.
- Treat `ops/prompts/shopify-listing-master-prompt.md` as the canonical operator spec and `ops/prompts/shopify-listing-from-1688.md` as the canonical request template.
- In a fresh session, read `ops/prompts/START-HERE.md` and then the two canonical prompt files before drafting or shipping any new listing workflow, runner, CSV, or metafield plan.
- Prefer the `ops/prompts/` versions over older ad hoc prompt files under `GPT/` unless the user explicitly asks for those legacy files.
- If a listing task seems ambiguous, align to the rules in the canonical prompt files first, then document any deviation in `ops/AGENT_WORKLOG.md`.

Coding conventions
- Liquid, snippets, sections: Prefer small, composable snippets. Avoid heavy inline <style> where possible.
- JavaScript: Plain ES modules in assets/, avoid framework dependencies unless justified.
- Analytics: Push to window.dataLayer only; destination wiring (GA4/GTM/Meta) is configured outside the theme.

Agent usage policy
- No AI UI on the live website. The assistant is developer-side only (this terminal).
- Any backend agent code in this repo is for development/reference and must not be referenced from the theme.

Agent roadmap (from paper, dev-only)
- L1→L2 Product Finder (dev tool): offline analysis to propose improvements and content; no site widget.
- Merchandiser/Support/SEO agents used as operators’ tools in development; outputs are reviewed and merged manually.

Testing
- Start with targeted manual checks; if adding tests, keep them lightweight and colocated under ops/tests/ (do not add frameworks unless agreed).
