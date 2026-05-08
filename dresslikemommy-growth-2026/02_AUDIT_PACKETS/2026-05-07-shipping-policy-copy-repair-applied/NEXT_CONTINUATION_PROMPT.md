Continue paid-growth from `AGENT_CONTINUITY_ANCHOR: 2026-05-07-localized-policy-page-cleanup-admin-clean-public-partial`.

Read first:

1. `AGENTS.md`
2. `ops/MEMORY_CONTINUITY_PROTOCOL.md`
3. `ops/AGENT_COORDINATION.md`
4. `ops/BROWSER_SUBAGENT_COORDINATION.md`
5. `ops/GOOGLE_ADS_CONTINUITY.md`
6. `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-shipping-policy-copy-repair-applied/SHIPPING_POLICY_COPY_REPAIR_APPLIED_REPORT.md`
7. `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-shipping-policy-copy-repair-applied/LOCALIZED_POLICY_PAGE_CLEANUP_REPORT.md`
8. Latest `ops/AGENT_WORKLOG.md` entries

Critical corrections:

- Dress Like Mommy is dropshipping, has no physical store, and has no owned physical inventory.
- Do not imply warehouses, retail inventory, local inventory, stocked inventory, or in-store pickup.
- Return shipping is customer-paid; do not confuse outbound checkout delivery rates with return postage.
- Do not import, create, enable, or spend internationally yet.

What is done:

- Shopify Admin source Shipping Policy, Shipping Info page, and Terms shipping/pricing sections were updated with checkout-availability wording.
- A slow cooldown public readback confirmed English Shipping Policy and English Shipping Info are clean.
- A separate approved localized cleanup registered Shopify native translations for:
  - Shipping Policy `body`: `es`, `it`, `ro`, `pt-BR`.
  - Shipping Info page `body_html`: `es`, `it`, `ro`, `pt-BR`.
- Admin translation readback is clean for all 8 target translations: `outdated=false`, no stale blocker phrases, checkout-availability wording present.
- Post-write public readback returned HTTP `200` for all checked URLs with no `429`.

Still blocked for international paid launch:

- Public storefront propagation is partial:
  - Spanish Shipping Policy is localized and clean.
  - Romanian Shipping Info is localized and clean.
  - Romanian and Portuguese Shipping Policy pages fall back to clean English copy.
  - Spanish Shipping Info still serves stale translated worldwide/free-shipping copy.
  - Italian Shipping Policy still serves stale four-country translated copy.
  - Italian Shipping Info still serves stale translated worldwide/free-shipping copy.
  - Portuguese Shipping Info still serves stale translated worldwide/free-shipping copy.
- Read-only check found no Eurozone market-specific translation overrides for the target native translation resources.
- Product pages on localized routes still need currency/readiness QA before international paid traffic.
- ES/IT/RO/PT checkout QA should not run as a paid launch gate until public copy is clean or explicitly accepted as a non-launch blocker by the owner.

Next safest lane:

1. Wait for a longer storefront/translation cache window.
2. Recheck only the still-stale public URLs slowly, one at a time:
   - `/es/pages/shipping-info`
   - `/it/policies/shipping-policy`
   - `/it/pages/shipping-info`
   - `/pt/pages/shipping-info`
3. If still stale, inspect Translate & Adapt / translation app / storefront translation-serving layer for overrides; do not rewrite products, rates, Markets, theme, or ads.
4. After public copy is clean, run one slow no-payment checkout QA for ES/IT/RO/PT with required region fields:
   - ES `Comunidad de Madrid`
   - IT `Roma`
   - RO `București`
   - PT `Lisboa`
5. Keep Google Ads/Pinterest international paid import/spend parked until policy/currency/route/checkout readbacks pass and the owner gives exact fresh approval.

Do not create/import/enable paid campaigns or spend from this prompt. No PMax, Standard Shopping, product scope, feed label, product group, budget, bid, status, conversion-goal, Merchant upload, or Shopify product-data changes.
