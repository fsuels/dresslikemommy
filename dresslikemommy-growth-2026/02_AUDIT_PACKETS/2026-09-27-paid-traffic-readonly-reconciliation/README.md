# Paid traffic read-only reconciliation — 2026-09-27

Scope: read-only. No change was made in Google Ads, Microsoft Ads, Merchant or Shopify. Sources were Google Ads UI (owner's Chrome, account DLM 650-997-2886 under manager 700-107-9966) and ShopifyQL via the Shopify connector.

## Google Ads, Sep 6–26 2026 (UI campaign table, LIVE_VERIFIED)
| Campaign | Budget | Type / bidding | Cost | Impr | Clicks | Conv |
|---|---|---|---|---|---|---|
| DLM \| GADS \| US \| EN \| Shopping \| 202609 \| Daily | $20/day | Shopping, Manual CPC | $19.06 | 4,717 | 87 | 0 |
| DLM \| GADS \| US \| EN \| Search \| 202609 \| Daily | $10/day | Search, Max clicks | $6.29 | 278 | 18 | 0 |
| DLM \| GADS \| AU \| EN \| Search \| 202609 \| Daily | $10/day | Search, Max clicks | $3.43 | 146 | 12 | 0 |
| DLM \| GADS \| GB \| EN \| Search \| 202609 \| Daily | $10/day | Search, Max clicks | $2.36 | 60 | 8 | 0 |
| DLM \| GADS \| CA \| EN \| Search \| 202609 \| Daily | $10/day | Search, Max clicks | $1.21 | 63 | 6 | 0 |
| Campaign #1 | $5/day | Performance Max, tROAS | $0.80 | 356 | 5 | 0 |
| DLM \| GADS \| US \| EN \| Search \| 202609 | $200 total, Sep 22–Oct 10 | Search, Max clicks | $0 | 0 | 0 | 0 |
Account total: $60/day budget, $33.15 cost, 5,620 impressions, 136 clicks, 0 conversions. Delivery is about $1.6/day against $60/day of budgets, so bids or caps limit volume, not budget.
- Conversion goals: Purchase goal Active, used by 5 of 5 campaigns (1 primary action), 0 results. The Engagement and YouTube follow-on goals show "Misconfigured" (not used by campaigns).
- No account-level verification, suspension or policy banner was found on Overview (accessibility-tree search).

## Shopify side, last 30 days (ShopifyQL, LIVE_VERIFIED)
- Orders by source: 7 direct or unknown, 4 Google organic search, 1 Google free listings (`utm_source=google&utm_medium=product_sync&utm_campaign=sag_organic`), **0 with utm_medium=cpc**. The Google Ads zero conversions therefore matches the Shopify order truth, and is not evidence of broken tracking.
- Paid sessions by UTM: Microsoft Ads (`bing / cpc`, campaigns `DLM | MS | US/CA/AU/GB/Latinos …`) had about 413 sessions, 3 carts, 0 checkouts. Google `cpc` (campaign IDs 24288861079, 24281367822, 24281589099, 23805046526, 24286768070) had about 104 sessions, 6 carts, 2 checkouts, 0 orders.
- ChatGPT referrals (`chatgpt.com`, `chatgpt.com / feed`): 207 sessions, 23 carts, 3 checkouts, 0 orders. This is the highest-intent unpaid source.

## Not read (next reconciliation steps)
Microsoft Ads spend and search terms; Google search terms and Shopping product performance; Merchant diagnostics after the Shopify-app feed switch. `current_marketing_state.md` Authoritative Execution Control is unchanged (`STALE_READBACK_REQUIRED`), because this is a partial readback.

## Microsoft Advertising, 8/28–9/26/2026 (UI campaign table, owner's Chrome, account aid=477439, LIVE_VERIFIED)
- 15 campaigns, $150/day combined budgets: **$57.71 spend, 407 clicks, 21,018 impressions, 0 conversions**.
- **Audience ads total $37.59 (65% of spend), 255 clicks, CTR 1.50%.** Search ads total $20.12, 152 clicks.
- Largest campaign: `DLM | MS | US | EN | Search | 202609` $44.03, 301 clicks, 11,994 impressions (includes its audience-network serving). CA $8.29 (53 clicks), EUR $1.85, GB $1.57, Latinos $1.40, AU $0.50, IT $0.07. DE, FR&CA, PL, NO, BR&PT, NL, DK and US Shopping: $0.
- Shopify truth: about 413 `bing / cpc` sessions, 3 carts, 0 checkouts, 0 orders.

## Combined paid (about 30 days): Google $33.15 + Microsoft $57.71 = **$90.86, 543 clicks, 0 orders**.
No change was made on either platform.
