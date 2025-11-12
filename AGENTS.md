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
- Also review this AGENTS.md and the diffs in layout/theme.liquid, sections/main-product.liquid, snippets/cart-drawer.liquid, snippets/meta-tags.liquid, assets/analytics.js for context.
- If context is tight, search for the string: AGENT_CONTINUITY_ANCHOR in the worklog to jump to the latest checkpoint.

Coding conventions
- Liquid, snippets, sections: Prefer small, composable snippets. Avoid heavy inline <style> where possible.
- JavaScript: Plain ES modules in assets/, avoid framework dependencies unless justified.
- Analytics: Push to window.dataLayer only; destination wiring (GA4/GTM/Meta) is configured outside the theme.

Agent roadmap (from paper)
- L1→L2 Product Finder (front-end widget + App Proxy backend).
- Merchandiser (bundles/threshold nudges); Support (policy RAG); SEO/meta enrichment; Experiment harness + LM judge.

Testing
- Start with targeted manual checks; if adding tests, keep them lightweight and colocated under ops/tests/ (do not add frameworks unless agreed).

