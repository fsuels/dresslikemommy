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
Session: Inline CSS cleanup + predictive search vendor
Date: 2025-11-13

Changes applied (evidence-first)
- layout/theme.liquid: Added the `theme-inline-overrides.css` `stylesheet_tag` ahead of `</head>` and removed all trailing inline `<style>` blocks after `content_for_layout` to keep the markup valid (layout/theme.liquid:1373-1410).
- assets/theme-inline-overrides.css (new): Collected the ten legacy override blocks into a single asset so they continue to load after global styles without polluting the layout (assets/theme-inline-overrides.css:1).
- config/settings_data.json: Enabled `predictive_search_show_vendor` so predictive search now reveals vendor context along with price (config/settings_data.json:1).
- config/settings_schema.json:1474 - Added Theme Settings -> Experiments controls for enabling the harness plus flag and notes inputs.
- config/settings_data.json:1 - Seeded `experiments_enabled`, `experiment_flags`, and `experiment_notes` defaults so the new schema renders safely.
- layout/theme.liquid:1394/1459/1473 - Emits experiment data attributes on `<body>`, hydrates `window.experimentConfig`, and defers `experiments.js` for telemetry.
- assets/experiments.js:1 - Pushes an `experiments_ready` event to `window.dataLayer` and logs active flags in design mode.
- ops/tests/experiments.md:1 - Added LM judge prompt template and rubric to keep future evaluations consistent.

Open TODOs (next session)
1) Product Finder Agent (from paper L1+L2)
   - No live widget; agent is developer-side only. Use agent-backend/ as a dev service if needed during development; do not link from theme.
   - Backend app: scaffolded under agent-backend/ (Express, Storefront GraphQL). App Proxy signature verification added (prod); L2-lite planner extracts budget/terms and filters results. Optional LM + RAG (dev-only) for richer planning and policy grounding. See ops/AGENT_PROXY_SPEC.md.
   - Contract: { message, session } + { reply, items[], clarify? }.
2) Merchandiser Agent (AOV)
   - Nudge threshold (sync with progress bar); suggest bundles; later: discount via Shopify Functions.
3) Analytics destinations
   - NEEDS_DATA: GA4/GTM/Meta IDs and consent mode decisions.

Session: Shipping SLA consolidation + estimator
Date: 2025-11-13

Changes applied (evidence-first)
- config/settings_schema.json:1506 & config/settings_data.json:1 — Added a “Shipping promise” settings group (processing windows, per-country overrides, holiday cutoff + delay banner toggles) and default values so merchants can update SLA copy without code edits.
- snippets/shipping-promise-data.liquid:1 & assets/shipping-promises.js:1 — Emit a single JSON payload of the SLA plus a front-end helper that converts it into country-aware arrival dates (e.g., “Delivers to CA by Dec 18–22”), updates `[data-shipping-summary]`, and surfaces holiday cutoffs automatically.
- snippets/shipping-estimate-inline.liquid:1, snippets/shipping-promise-list.liquid:1, snippets/shipping-delay-banner.liquid:1 — Reusable UI blocks for PDP, cart, FAQ, and the optional global delay banner; assets/theme-inline-overrides.css:210 now styles these components consistently.
- layout/theme.liquid:1394/1459/1476 — Body now carries customer country data, renders the delay banner, injects the shipping JSON payload, and loads the new estimator script on every page.
- sections/main-product.liquid:166/738/799 — Replaced conflicting copy (“2d processing + 7–10d” vs. “75.4% within 11 days”) with the shared snippet + destination list so PDP, FAQ, and accordion stay in sync.
- sections/announcement-bar.liquid:188, snippets/cart-drawer.liquid:73, sections/main-cart-footer.liquid:68 — Cart drawer, cart footer, and fallback announcement now consume the same snippet so shoppers see the identical promise everywhere.

Open TODOs (next session)
1) Product Finder Agent (from paper L1+L2)
   - No live widget; agent is developer-side only. Use agent-backend/ as a dev service if needed during development; do not link from theme.
   - Backend app: scaffolded under agent-backend/ (Express, Storefront GraphQL). App Proxy signature verification added (prod); L2-lite planner extracts budget/terms and filters results. Optional LM + RAG (dev-only) for richer planning and policy grounding. See ops/AGENT_PROXY_SPEC.md.
   - Contract: { message, session } + { reply, items[], clarify? }.
2) Merchandiser Agent (AOV)
   - Nudge threshold (sync with progress bar); suggest bundles; later: discount via Shopify Functions.
3) Analytics destinations
   - NEEDS_DATA: GA4/GTM/Meta IDs and consent mode decisions.
4) Shopify admin shipping policy
   - Update the admin-managed Shipping Policy + FAQ content so the live policy page reflects the new SLA (2–3d processing + region-specific transit windows).

Session: Shipping SLA surfaces expansion
Date: 2025-11-13

Changes applied (evidence-first)
- snippets/cart-notification.liquid:30 and snippets/quick-order-list.liquid:165 — Both surfaces now render the reusable `shipping-estimate-inline` block so the instant modal and bulk-order tooling echo the same “Delivers to XX by…” copy.
- sections/shipping-faq.liquid (new) and assets/theme-inline-overrides.css:230 — Added a dedicated shipping FAQ section (with schema + FAQ blocks) and lightweight styles so policy/FAQ pages can drop in the shared SLA + region list without bespoke markup.
- templates/page.shipping.json / templates/page.faq.json — New page templates that append the Shipping FAQ section beneath the standard page content so merchants can assign their Shipping Policy + FAQ pages without re-building blocks.
- ops/SHIPPING_SLA.md — Playbook covering the new Theme Settings, where the snippet is consumed, and how to sync Shopify’s admin shipping policy text with the canonical SLA.

Session: Featured product + script polish
Date: 2025-11-13

Changes applied (evidence-first)
- sections/featured-product.liquid:131 & assets/theme-inline-overrides.css:224 — Featured Product (home hero) now renders `shipping-estimate-inline`, so the same “Delivers to …” copy appears even when products are highlighted outside the PDP.
- assets/shipping-promises.js:1 — ETA strings now use ASCII hyphens, the summary text mirrors the detailed phrasing, and the shopper’s country name (fallback “Worldwide”) is used instead of only the ISO code.
- layout/theme.liquid:1374 — `data-customer-country-name` defaults to “Worldwide” rather than the shop name, ensuring clean fallback text when localization data isn’t available.

Open TODOs (next session)
1) Product Finder Agent (from paper L1+L2)
   - No live widget; agent is developer-side only. Use agent-backend/ as a dev service if needed during development; do not link from theme.
   - Backend app: scaffolded under agent-backend/ (Express, Storefront GraphQL). App Proxy signature verification added (prod); L2-lite planner extracts budget/terms and filters results. Optional LM + RAG (dev-only) for richer planning and policy grounding. See ops/AGENT_PROXY_SPEC.md.
   - Contract: { message, session } + { reply, items[], clarify? }.
2) Merchandiser Agent (AOV)
   - Nudge threshold (sync with progress bar); suggest bundles; later: discount via Shopify Functions.
3) Analytics destinations
   - NEEDS_DATA: GA4/GTM/Meta IDs and consent mode decisions.
4) Shopify admin shipping policy
   - Update the admin-managed Shipping Policy + FAQ content so the live policy page reflects the new SLA (2–3d processing + region-specific transit windows).
Session: Homepage hero foundation
Date: 2025-11-13

Changes applied (evidence-first)
- sections/hero-family-fit.liquid (new)
  - Built a reusable hero section with schema controls, shipping reassurance that auto-pulls theme shipping settings, and CTA buttons tagged with data-cta-id hooks for upcoming analytics (sections/hero-family-fit.liquid:1).
  - Added optional badge blocks plus layout/color controls so Merchandiser Agent can tell seasonal stories without duplicating markup.
- templates/index.json:1
  - Registered hero_family_fit_FvXq4J at the top of the homepage order with copy/CTA defaults and starter badge text so every visit now opens with a value-prop instead of a wall of collection tiles.

Open TODOs (next session)
1) Drop in approved desktop/mobile hero imagery (or video) for hero_family_fit_FvXq4J once creative is finalized.
2) Extend assets/analytics.js to emit select_promotion events for data-cta-id="hero_primary"/"hero_secondary" clicks so we can measure engagement.
3) Continue Merchandiser Agent plan: add best-seller/product storytelling sections beneath the hero to diversify the fold (ref. templates/index.json:1).
Session: Sora hero prompt kit
Date: 2025-11-13

Changes applied (evidence-first)
- GPT/sora.md: Added detailed Sora prompts for desktop video, mobile video, and still exports so creative partners can generate approved hero assets without re-briefing (GPT/sora.md:1).

Open TODOs (next session)
1) Produce hero media via Sora using the new prompts and upload the selected files to the theme settings for hero_family_fit_FvXq4J.
Session: Sora prompt refinement (beach shoot)
Date: 2025-11-13

Changes applied (evidence-first)
- GPT/sora.md: Updated both video prompts to reflect a white European-American family in luxe resort styling so visual direction matches the latest creative request (GPT/sora.md:1).

Open TODOs (next session)
1) Generate the updated beach-shoot hero media via Sora and apply assets to hero_family_fit_FvXq4J once approved.
Session: Sora prompt refinement (matching catalog)
Date: 2025-11-13

Changes applied (evidence-first)
- GPT/sora.md: Updated prompts to reference actual catalog looks (Blue Coconut swim + lavender floral maxis) so the generated hero imagery mirrors live inventory (GPT/sora.md:1).

Open TODOs (next session)
1) Render new hero media via Sora using the catalog-specific prompts and upload assets to hero_family_fit_FvXq4J once approved.
Session: Sora prompt refinement (family-safe)
Date: 2025-11-13

Changes applied (evidence-first)
- GPT/sora.md: Adjusted prompts to emphasize modest layering (tankini tops under maxi wrap skirts, shirts for men/boys) to keep Sora within nudity guardrails while retaining catalog accuracy (GPT/sora.md:1).
Session: Sora prompt refinement (modesty guardrail)
Date: 2025-11-13

Changes applied (evidence-first)
- GPT/sora.md: Reworded prompts to feature fully covered maxi dresses and linen sets (no swimwear language) so Sora stops flagging the content as suggestive (GPT/sora.md:1).
Session: Hero liquid compat fix
Date: 2025-11-13

Changes applied (evidence-first)
- sections/hero-family-fit.liquid: Replaced the boolean expression assignment with a Liquid-safe conditional so the theme server stops throwing Expected end_of_string but found comparison during shopify theme dev (sections/hero-family-fit.liquid:105).
- sections/hero-family-fit.liquid: Also converted the layout == 'media_left' assignment to a Liquid-safe conditional so dev server can parse the section without comparison expressions (sections/hero-family-fit.liquid:109).
- sections/hero-family-fit.liquid: Added a non-empty default for the shipping_message schema field to satisfy Shopify's schema validator (sections/hero-family-fit.liquid:64).
Session: Hero video support
Date: 2025-11-13

Changes applied (evidence-first)
- sections/hero-family-fit.liquid: Added native video support (desktop/mobile MP4 URLs, poster image, overlay opacity) and rendering logic so the Family Fit hero can autoplay the new Sora footage with graceful fallbacks (sections/hero-family-fit.liquid:1-220).
- templates/index.json: Wired the section settings to the Shopify CDN videos (desktop + portrait orientations) and enabled the overlay defaults (templates/index.json:1).

Open TODOs (next session)
1) Upload desktop/mobile poster stills and set the ideo_poster_image field once final frame grabs are ready.
2) Extend analytics (ssets/analytics.js) to fire events when the new hero CTAs are clicked and when the video enters the viewport.
- sections/hero-family-fit.liquid: Converted the video/image boolean checks into Liquid-safe conditional assignments so theme dev no longer errors on != blank expressions (sections/hero-family-fit.liquid:129-140).
- sections/hero-family-fit.liquid: Set has_media via chained conditionals instead of or expressions so Liquid accepts the assignment in strict mode (sections/hero-family-fit.liquid:141).
