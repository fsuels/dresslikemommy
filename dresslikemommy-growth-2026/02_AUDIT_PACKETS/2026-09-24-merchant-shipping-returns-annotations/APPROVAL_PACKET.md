# Merchant 513542500 — $0 shipping + 30-day returns approval packet

Status: `PACKET_READY__MC_BEFORE_STATE_BLOCKED` · Prepared 2026-09-24 · No external write made.

Goal: let Google show a free-delivery label and a "30-day returns" label on US/AU/CA/GB listings, using only claims the store actually honours. A "free returns" label is out of scope: the customer pays return shipping.

## 1. Evidence

| Item | State | Source |
|---|---|---|
| Shopify standard rate, US/AU/CA/GB | `LIVE_VERIFIED` 2026-09-24: "Free Standard Shipping" costs 0.00 USD and has no conditions (no order minimum). The zone "Countries Epacket" contains all four countries. The rest-of-world rate is the same. | `shopify_shipping_returns_readback.json` |
| Shopify optional upgrade | `LIVE_VERIFIED`: "Priority Shipping" costs 12.99 USD for orders of 0–5 lb. | same |
| Processing time | Shipping policy and Terms: 1–3 business days. | Shopify policies 29845782625 / 14695813 |
| Storefront delivery estimate | `REPO_KNOWN`: the theme shows `standard_delivery_window` "12-16 days". | `locales/en.default.json:306` |
| Refund policy 14695685 (updated 2026-01-26) | `LIVE_VERIFIED`: 30 days from delivery; items must be new (unworn, tags attached); customer pays return shipping unless the item is damaged or defective; no restocking fee stated; exchanges accepted; refund in 5–10 business days. Exclusions: swimwear/intimates, items marked "Final Sale", gift cards. | Shopify Admin read |
| Terms 14695813 (updated 2026-05-09) | `LIVE_VERIFIED` **conflict**: says "Sale items and personalized items are final sale", and "Return shipping ... customer's responsibility unless we made an error". | Shopify Admin read |
| MC return policies | `STALE_OR_SUPERSEDED` (last repo read 2026-09-12/14): only `returnpolicy9309759641`, Austria, verified. **None for US/AU/CA/GB.** | `ops/marketing/current_marketing_state.md:536` |
| MC swimwear scope | `REPO_KNOWN`: 700 nondefective swimwear offers across 46 parents per country. The current 18-column feed has no `return_policy_label` field. | `ops/marketing/current_marketing_state.md:500-502` |
| MC shipping services | `LIVE_READBACK_REQUIRED`. Before-state unknown. The only repo evidence is an unapplied CA:::0.00 CAD / GB:::0.00 GBP product-level proposal. | `ops/marketing/current_marketing_state.md:265` |

### Merchant Center before-state read: BLOCKED

- Merchant API / Content API with this machine's `gcloud` token returns `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT` for `ShippingSettingsService.GetShippingSettings`. The same 403 is returned for `onlineReturnPolicies`, and for Content API `shippingsettings` and `returnpolicyonline`.
- The built-in browser pane opened Merchant Center and was redirected to Google sign-in (`ACCESS_RECOVERY_REQUIRED`). The agent did not enter any credentials.
- Recovery options: (a) the owner signs the built-in browser in to the Merchant account, or (b) the owner allows a read of an already signed-in Chrome tab, or (c) a token with the `https://www.googleapis.com/auth/content` scope is used.

## 2. Pre-conditions (all required before any write)

1. **MC before-state readback** for each of US/AU/CA/GB. Record:
   - every existing shipping service (name, countries, currency, rate, minimum order, delivery times);
   - every return policy.

   Save screenshots or JSON here as `mc_before_*.{png,json}`.
2. **Owner decision — Terms vs refund policy.** Pick one truthful definition and make Terms match the refund policy. Recommended: replace the Terms returns bullets with the refund-policy wording, namely "Items marked Final Sale", "unless the item arrived damaged or defective", and a link to the Return Policy. Also check how Terms covers personalized items. Changing Terms is a separate Shopify policy write and needs its own approval.
3. **Swimwear exception path.** A blanket 30-day policy must not be applied to the 700 nondefective swimwear offers per country. This needs a `return_policy_label` (for example `no_returns_swim_intimates`) on those offers, emitted by the current Merchant feed writer. The owner of `~/.config/dresslikemommy/merchant-us-feed-writer.lock` would do this under their own claim. It also needs a matching MC "non-returnable" policy.
4. A claim row in `ops/AGENT_COORDINATION.md` for the Merchant settings surface, which is separate from the feed-source writer.

## 3. Proposed writes

### A. Shipping services (account level), one per country

| Country | Service name | Currency | Rate | Min order | Handling | Transit |
|---|---|---|---|---|---|---|
| US | Standard shipping included | USD | 0.00 | none | 1–3 business days | **OWNER_CONFIRM** (proposal 9–13 business days) |
| AU | Standard shipping included | AUD | 0.00 | none | 1–3 | OWNER_CONFIRM |
| CA | Standard shipping included | CAD | 0.00 | none | 1–3 | OWNER_CONFIRM |
| GB | Standard shipping included | GBP | 0.00 | none | 1–3 | OWNER_CONFIRM |

- Transit: the proposed maximum of 3 + 13 = 16 business days covers the storefront's "12-16 days". Business days are longer than calendar days, so this does not promise faster delivery than the store gives. Confirm it against current carrier data. Google must never show a delivery time faster than real delivery.
- Priority Shipping (12.99 USD) can stay out of Merchant Center. Google uses the cheapest service for the label.
- If the before-state shows an existing Shopify-app-synced service for a country, **edit that service** rather than adding a duplicate.
- Leave the CA/GB product-level `shipping` override proposal unused if account-level services are applied. Using both is redundant.

### B. Return policies (one each for US, AU, CA, GB, or one multi-country policy if the UI allows it)

| Field | Value |
|---|---|
| Policy URL | Published refund policy / page 161929989, the same URL already verified for Austria |
| Returns accepted | Yes, 30 days from delivery |
| Item condition | New |
| Return method | By mail |
| Return shipping fee | Customer pays (**not** free) |
| Restocking fee | None (confirmed by the owner 2026-09-11 for Austria) |
| Exchanges | Accepted |
| Refund processing days | Blank (the source uses business days plus bank time; same as the Austria decision) |
| Exception | `return_policy_label = no_returns_swim_intimates` → non-returnable. Only after pre-condition 3. |

## 4. Expected result, verification and rollback

- `EXPECTED`: free-delivery and "30-day returns" annotations become eligible on Shopping ads and free listings in the four countries within days. There is no promised lift in traffic or orders.
- After-state: re-read each service and each policy in MC and save `mc_after_*` files. Check that there are no new item issues in Diagnostics for shipping or returns. Spot-check one approved offer per country for the annotation.
- Rollback: restore each service/policy to its recorded before-state. For services or policies newly added with no before-state, delete them.
- Kill criteria: stop if MC shows any item issue "Incorrect shipping" or "Return policy mismatch". Also stop if the Shopify rate is no longer 0.00 with no minimum.

## 5. Approval requested (exact)

> Approve Merchant 513542500: (A) $0 standard shipping services for US/USD, AU/AUD, CA/CAD, GB/GBP with no minimum, handling 1–3 and transit ___–___ business days. (B) 30-day, new-condition, by-mail, customer-paid-return-shipping, no-restocking-fee return policies for the same four countries, linked to the published refund policy. (B) applies only after Terms is reconciled and the swimwear exception label is live.

(A) can go ahead independently of (B) once the before-state has been read.
