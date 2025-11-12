AGENT_CONTINUITY_ANCHOR

Session: Quick Wins + Continuity Setup
Date: 2025-11-12

Changes applied (evidence-first)
- layout/theme.liquid
  - Meta author now uses {{ shop.name }}.
  - Removed duplicate {{ content_for_header }} instance; only one remains near top.
  - Added assets/analytics.js include (after global.js) to push basic events (view_item, add_to_cart, begin_checkout).
  - Deduped base.css include by removing print/onload lazy variant; kept stylesheet_tag include.
  - Removed placeholder RAF CSS loader; consolidated tail CSS into a valid <style> block before </body>.
  - Removed previously added agent widget mount and script; no AI UI on site per owner’s requirement.
- snippets/meta-tags.liquid
  - Added robots noindex for search/cart/404/password.
- templates/collection.json
  - Reduced products_per_page from 36 → 24 to improve performance.
- sections/main-product.liquid
  - Removed duplicate title (H1+H2); kept a single H1.
  - Commented out randomized urgency/sold script and urgency banner; added factual low-stock message based on true inventory (<=5).
- snippets/cart-drawer.liquid
  - Replaced progress bar with static free-shipping note (all clothing ships free) and delivery estimate (2d processing + 7–10d).
- assets/analytics.js (new)
  - Parses ProductJSON script to push view_item; listens to pubsub cart-update for add_to_cart; intercepts checkout button for begin_checkout.
- Removed assets/agent.js to ensure no on-site AI UI.
- ops/AGENT_PROXY_SPEC.md (new)
  - Contract for App Proxy endpoint and tool orchestration aligned with L1→L2 agent design.

Not fully changed (to keep diff safe)
- layout/theme.liquid still contains trailing style blocks after </html>; a follow-up will delete them now that CSS is consolidated before </body>.
- config/settings_data.json predictive flags (price/vendor) — can be toggled in the customizer; patching minified JSON line was avoided.

Open TODOs (next session)
1) Clean up layout/theme.liquid
   - Deleted RAF CSS loader; consolidated tail CSS before </body>.
   - Removed trailing style blocks after </html> to finalize validity.
2) Predictive search enrichment
   - Turn on price/vendor in settings or confirm preference.
3) Product Finder Agent (from paper L1→L2)
   - No live widget; agent is developer-side only. Use agent-backend/ as a dev service if needed during development; do not link from theme.
   - Backend app: scaffolded under agent-backend/ (Express, Storefront GraphQL). App Proxy signature verification added (prod); L2-lite planner extracts budget/terms and filters results. Optional LM + RAG (dev-only) for richer planning and policy grounding. See ops/AGENT_PROXY_SPEC.md.
   - Contract: { message, session } → { reply, items[], clarify? }.
4) Merchandiser Agent (AOV)
   - Nudge threshold (sync with progress bar); suggest bundles; later: discount via Shopify Functions.
5) Experiment harness + LM Judge
   - Add simple feature flags via data attributes; create eval prompts + rubric.
6) Analytics destinations
   - NEEDS_DATA: GA4/GTM/Meta IDs and consent mode decisions.

How to resume
- Read from AGENT_CONTINUITY_ANCHOR, apply TODOs in order.
- Maintain evidence-first approach; cite files:lines in notes.
- sections/announcement-bar.liquid
  - Added default announcement message fallback when no blocks: “Free shipping on all clothing • 2d processing • 7–10d delivery”.
- snippets/card-product.liquid
  - Added a small “Ships free” badge on product cards (PLP).
- sections/main-product.liquid
  - Added shipping reassurance under price: “Standard shipping: Free · Est. delivery: 2d processing + 7–10d”.
