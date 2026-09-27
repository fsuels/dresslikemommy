# UI Browser Verification Loop

Use this loop for Shopify theme, Liquid, CSS, JavaScript, storefront copy, navigation, PDP, collection, cart, search, contact, account, localization, or checkout-adjacent UI changes.

## Read First

1. `AGENTS.md`
2. `VISION.md`
3. `ops/AGENT_COORDINATION.md` before touching theme files or live storefront surfaces
4. Any relevant problem entry in `ops/PROBLEM_TRACKER.md`

## Implement

- Keep Dawn-compatible Liquid, JSON templates, CSS, and vanilla JavaScript patterns.
- Prefer existing snippets, section settings, translation keys, and theme assets over new abstractions.
- Do not put backend logic, secrets, or operator-only AI surfaces into the storefront.
- Preserve unrelated dirty worktree changes.

## Validate

Run the narrowest relevant checks:

```bash
git diff --check
shopify theme check
```

If `shopify theme check` is unavailable, report that and run the closest available syntax checks, such as `node --check` for touched JavaScript files.

## Live-Store Measurement Hygiene

Live readbacks run on the real storefront, so they count as sessions and can fire ad and analytics pixels. Real Google/Pinterest/Meta bidding learns from those signals (PROB-2026-09-27-AGENT-TEST-TRAFFIC-POLLUTES-ANALYTICS).

- Scripted or headless checks of the live site must block tracking requests. Use a route rule that aborts URLs matching `monorail|trekkie|google|doubleclick|facebook|pinterest|tiktok|bing|clarity|hotjar|klaviyo|snapchat|analytics|pixel`. The reference implementation is `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-ux-ten-fixes/live-verify/verify_live.js`.
- Prefer read-only checks (page text, `/products/<handle>.js`, `/collections/<handle>/products.json`) over interactive ones. Use a local harness with stubbed `fetch` for cart logic.
- No live add-to-cart, checkout start or checkout step without explicit owner approval in the current chat. When approved, record the UTC start/end time and route in the worklog so the sessions can be excluded from funnel reports.
- The shared built-in browser cannot block pixels. Use it for visual checks only, not cart or checkout actions.

## Browser Readback

For affected UI, verify both desktop and mobile. Prioritize the exact routes touched, then a representative revenue-critical path:

- Home: `/`
- Product: `/products/<handle>`
- Collection: `/collections/<handle>`
- Cart: `/cart`
- Search: `/search`
- Contact/account routes if touched
- Localized or country-qualified routes if language, currency, shipping, or paid landing changes are involved

Check:

- No overlapping text or controls.
- Main CTA is visible and correct.
- Variant picker, size guide, cart drawer/page, and sticky CTA behavior work when affected.
- Images, alt text, canonical/SEO snippets, and structured data still render as intended.
- Mobile scroll is normal; no hidden panel, stuck overlay, or unreachable control.
- Console/network errors are either absent or clearly unrelated and documented.

## Done

The loop is done when checks pass, desktop/mobile readbacks match the intended behavior, and any changed strategy/problem state is logged in the repo continuity files required by `AGENTS.md`.
