# Next Continuation Prompt

Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Start from:

`AGENT_CONTINUITY_ANCHOR: 2026-05-07-paid-growth-continuation-readbacks`

Read first:

1. `AGENTS.md`
2. `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
3. `ops/GROWTH_NORTH_STAR.md`
4. `ops/MEMORY_CONTINUITY_PROTOCOL.md`
5. `ops/AGENT_COORDINATION.md`
6. `ops/BROWSER_SUBAGENT_COORDINATION.md`
7. `ops/GOOGLE_ADS_CONTINUITY.md`
8. latest `ops/AGENT_WORKLOG.md`
9. this packet report: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-continuation-readbacks/PAID_GROWTH_CONTINUATION_READBACKS_REPORT.md`
10. this packet lane board: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-continuation-readbacks/LANE_BOARD.md`

Act as the parent/orchestrator. Use parallel subagents on disjoint lanes where supported; do not collapse into one slow agent. Keep a lane board with `moving`, `blocked`, `waiting on approval`, `done`, and `next safe parallel action`.

Important correction: Dress Like Mommy is a dropshipping business with no physical store and no owned physical inventory. Do not write policy, ad, listing, feed, or report copy that implies a retail location, warehouse, stocked local inventory, or guaranteed on-hand stock. Platform labels like Merchant/Pinterest `in_stock`, Shopify `inventory`, or Merchant `Missing local inventory data` are feed/channel salability diagnostics only.

Do not repeat:

- Do not repeat the Merchant Google & YouTube unpublish/republish toggle.
- Do not re-create the prior Google Ads local international Search packet.
- Do not re-create this continuation readbacks packet.
- Do not run duplicate checkout probes in parallel.
- Do not publish Shopify policy/page copy without fresh approval.

Current state:

- Merchant sample `shopify_US_7227254276193_41871113158753` still shows US/en source timestamp `2026-05-07T14:14:02+00:00`; Shopify paid cohort remains `780 already_correct`; diagnostics UI refreshed at `2:33 PM May 7, 2026` and still shows `Missing age group`.
- Google Ads paused international Search local packet exists and validates as paused-only: `17` non-US campaigns, `204` ad groups, `612` exact/phrase keywords, `629` negatives, `204` paused RSAs, max CPC `$0.15`; not imported.
- Pinterest Event Quality still reads `Fair`, updated `5/6/2026`; Events Overview now shows fresh `Api · Tag` Checkout and AddPaymentInfo events on `5/7/2026`; EN source `3041760867124595727` completed `5,663/5,663`, `0` failed, `152` warnings; item-level paid candidate proof is stale.
- Shipping/policy blocker is Admin-managed: Shipping Policy, Shipping Info, and Terms still imply shipping is limited to US/CA/GB/AU; a neutral online-store/checkout-availability repair draft exists at `lanes/policy/SHIPPING_POLICY_REPAIR.md`.
- Checkout QA: NL returned live Standard/Express rates; ES/IT/RO/PT returned `422` because province/county/region fields are required; PT routes are broken/partial (`pt-BR` 404, `/pt` 500, `/pt/policies/shipping-policy` 200).
- Admin markets/rest-of-world shipping exist, but public policy/currency/checkout proof remains the blocker for live international spend.

Guardrails:

- No live spend.
- No campaign enablement.
- No Google Ads import/create unless the exact approval below is given.
- No budgets, bids, statuses, conversion goals, Standard Shopping, PMax, product scope, product groups, feed labels, Merchant uploads, Shopify live product-data edits, or policy/page publishes without fresh explicit action-time approval.

Next safe lanes:

1. Shipping/policy copy repair lane:
   - If the owner gives the exact approval below, update only Shopify Admin Shipping Policy, Shipping Info page, and Terms shipping/pricing sections using `lanes/policy/SHIPPING_POLICY_REPAIR.md`.
   - Read back public pages afterward and verify the four-country-only and worldwide-overclaim phrases are absent.

2. Checkout QA lane:
   - After policy copy repair, run one controlled no-payment checkout pass for ES/IT/RO/PT with required province/county/region values, and recheck NL currency/policy.
   - Do not submit payment or create an order.

3. Merchant lane:
   - Later read-only recheck of sample timestamp and product issues.
   - Do not repeat the Google & YouTube toggle or edit product data without fresh approval.

4. Pinterest lane:
   - Run exact US candidate item-level readback for intended paid-ready rows.
   - Recheck Event Quality after it refreshes beyond `5/6/2026`.
   - Do not create drafts/spend until approval and gates pass.

5. Google Ads lane:
   - Keep paused import parked unless exact approval is given.
   - If approval is given, do just-in-time Ads readbacks and bulk-upload preview first; apply only paused shells if preview is clean and approval still clearly covers the action.

Exact approval for shipping/policy copy repair:

```text
APPROVE SHIPPING POLICY COPY REPAIR: UPDATE SHOPIFY ADMIN SHIPPING POLICY, SHIPPING INFO PAGE, AND TERMS SHIPPING SECTION USING THE 2026-05-07 POLICY LANE DRAFT; DO NOT CHANGE THEME, PRODUCTS, SHIPPING RATES, MARKETS, ADS, FEEDS, BUDGETS, CAMPAIGN STATUSES, OR CONVERSION GOALS; READ BACK PUBLIC PAGES AFTER SAVE.
```

Exact approval for paused international Google/Pinterest infrastructure:

```text
APPROVE PAUSED INTERNATIONAL GROWTH BUILD: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR US, UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; CREATE PAUSED PINTEREST US CATALOG/RETARGETING DRAFTS ONLY IF TAG/CATALOG GATES PASS; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES.
```

End with an updated `AGENT_CONTINUITY_ANCHOR`, evidence packet, coordination row, and the next continuation prompt.
