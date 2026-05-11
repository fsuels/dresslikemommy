# Google Ads Native-Language Import Gates

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-keyword-quality-expert-hardening`

These rows are marked `REVIEW_ONLY_NOT_UPLOAD` and are not upload-ready. Before any native-language Google Ads preview/import:

1. Native reviewer signs off each keyword, headline, and description for the target locale.
2. Country-qualified landing QA passes for PDP, cart, checkout entry, currency, rates, and policy links.
3. The parent creates a one-country paused native CSV only after exact owner approval.
4. Google Ads preview must return clean row validation before apply.
5. Read back campaign, language, location presence-only settings, networks, statuses, budgets, bids, ads, keywords, and final URLs after any approved apply.
6. Keep every campaign, ad group, ad, and keyword paused until separate live-spend approval.

Stop immediately if the flow requires budget/bid/status changes outside the exact approval, any PMax/Shopping/product/feed/conversion change, Merchant upload, Shopify product edit, or campaign enablement.
