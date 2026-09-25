# Mobile cart-to-checkout drop — 2026-09-24

Trigger: owner forwarded an outside review. It said 72% of mobile carts never reach checkout. It asked for a phone test of cart and checkout and a check that the abandoned-checkout email is on.

No external writes. No theme commit. No payment details or personal data entered, and no order placed.

## 1. Funnel numbers (LIVE_VERIFIED, ShopifyQL through the Shopify connector, aggregate only)

90 days to 2026-09-24, sessions:

| Device | Sessions | With cart add | Reached checkout | Completed |
|---|---|---|---|---|
| mobile | 5,756 | 362 | 101 | 28 |
| desktop | 14,231 | 90 | 49 | 5 |

The review's numbers match exactly. Mobile cart→checkout is 27.9%.

Mobile by referrer:

| Source | Cart | Checkout | Completed | Cart→checkout |
|---|---|---|---|---|
| Google search | 233 | 46 | 9 | 20% |
| Direct | 111 | 51 | 18 | 46% |

The drawer and checkout are the same for both sources. So the drop is mostly Google-search mobile shoppers who add to cart and leave. It is not a cart UI that blocks everyone.

Mobile by country, checkout → completed: US 31→14. Italy 45 carts → 8 checkouts → 0. Romania 28→11→0. Netherlands 16→9→0. Non-US checkout completion is 14/70 (20%) vs US 45%.

## 2. Phone test (375×812, built-in browser, product `little-pear-mommy-and-me-pajamas`, Mother M)

- **US / USD / English.** Drawer: `$32.99 USD`, "Standard included", Check out button in view (y≈498 of 812). Checkout loaded in about 2.5 s at `/checkouts/.../en-us`, with country US and total `$32.99`. `/cart/shipping_rates.json` for a US ZIP returned Free Standard `0.00` and Priority `12.99`. There was no surprise shipping line or currency switch. Express at checkout: PayPal, Google Pay, Amazon Pay, Venmo, and more options.
- **Italy / EUR / Italian** (set through the storefront localization form). Cart `€29,95`. Checkout at `/it-it` with country Italia and total `29,95 €`. No VAT or shipping added. Standard delivery showed "10 - 14 giorni". Express: Shop Pay, PayPal, Google Pay, Venmo.
- **Back from checkout** (drawer → checkout → Back): the cart still showed 1 item, and the server cart held 1 item. `PROB-2026-09-06-CART-RETURN-DISPLAY` did not reproduce on this path. That problem stays with its owner.
- Cleanup: test line removed, cart 0.

## 3. Findings

1. **No express-pay button before checkout.** The cart drawer (`cart_type: drawer`) has no `content_for_additional_checkout_buttons`. The PDP matching-set builder shows no `payment_button` either, even though `show_dynamic_checkout: true`. Only `/cart` shows wallets: Shop Pay, Amazon Pay, PayPal and Google Pay, in a 248 px stack at 375 px width.
   - Layout constraint (measured by inserting a 248 px block, browser only): the drawer footer grows from 467 to 731 px and the item list shrinks from 276 to **12 px** on an 812 px phone.
   - The drawer footer already holds "You may also like" (191 px).
   - A local change adding the wallets was built and passed theme check (0 offenses). It was **reverted, not shipped**, because it would hide the cart lines.
   - Viable version: move the upsell out of the fixed footer, or into the scrolling item list, before adding wallets. This needs an owner design decision.
2. **Pre-ticked marketing consent at checkout.** "Inviami email con notizie e offerte" was checked by default on the Italian checkout (screenshot in session). Shopify: Settings → Checkout → Marketing options → "Preselect the sign-up option". A pre-ticked box is not valid consent under GDPR. This weakens the `SUBSCRIBED` audience rule in `2026-09-24-email-retention/EMAIL_RETENTION_PLAN.md` for EU buyers.
3. **Abandoned-checkout automation status: BLOCKED.**
   - The built-in browser lands on the Shopify login page. The owner's personal Chrome is not a shared surface (`ops/BROWSER_SUBAGENT_COORDINATION.md`).
   - The Admin API has no read path: `marketingActivities` returns 0 nodes, and `AbandonedCheckout` has no recovery-email field.
   - Indirect data: 29 abandoned checkouts with contact info since 2026-06-26 (`abandonedCheckoutsCount`, EXACT). 0 email-referred orders in 365 days (`order_referrer_source`: none 104, search 68, social 1). This fits no recovery email being sent, but does not prove it.
4. No defect found in: currency, country preselection, shipping price vs drawer promise, or checkout speed. A shipping-policy "At , we want…" text was a split-element artifact. The live policy reads "At Dress Like Mommy".

## 4. Open questions

- Why Google-search mobile shoppers leave the cart. Hypotheses to test next:
  - The price in the Google listing vs the per-piece price. The builder sells each family member's piece separately under a "Mommy and Me … Set" title.
  - Delivery time.
- Why Italy, Romania and Netherlands checkouts don't complete.

## 5. Follow-up: carts → orders, Google search, last 30 days (2026-09-25 UTC)

Trigger: owner asked to fix three suspected causes. The causes were shipping cost that only appears at checkout, long delivery time, and a weak or missing return policy.

Funnel (LIVE_VERIFIED, ShopifyQL, `referrer_source = 'search'`, 30d): 1,413 sessions → 69 cart → 11 checkout → 4 completed. 58 of the 69 carts never reach checkout, so the leak is in the cart itself.

| Suspected cause | Finding | Evidence |
|---|---|---|
| Shipping cost appears only at checkout | **Disproven.** The single delivery profile charges $0 standard in both zones (Countries Epacket and Rest of world). Priority $12.99 is an optional upgrade. PDP and drawer say "Standard shipping included"; checkout shows "Free Standard Shipping — FREE". | Admin `deliveryProfiles` read; `/cart/shipping_rates.json` for DK/GB/NL/DE returned 0.00 standard; checkout readback (cart cleared to 0). |
| Delivery time | **Real gap: timing was never shown before checkout.** The PDP row said "See shipping options at checkout." The drawer estimate is permanently `hidden`. Checkout shows no estimate until an address is entered. The localized "Estimated delivery: 12-16 days" string exists in all 35 locales and in the FAQ schema, but commit `9ee5c13` (2026-09-14) stopped rendering it. | Shipped orders since March with a carrier delivered date (n=3): order→delivered 9.3 d (DE standard), 12.0 d (US standard), 12.6 d (US priority). IT checkout showed "10 - 14 giorni" (section 2). Order→fulfilment median ≈3.8 d (n=15). So 12-16 days is conservative. |
| Return policy | **Policy exists but was invisible in the cart.** Refund policy: 30 days from delivery; unworn, with tags; customer pays return shipping; returns start by email. The PDP shows it; the drawer trust strip showed only Secure and Shipping included. The Arabic and Thai "30-day returns" strings translated "returns" as financial yield. | Admin `shopPolicies` read; `locales/*.json`. |

Theme fix: commit `e3d0e07` on `main`.
- The PDP shipping row shows the localized delivery estimate.
- The drawer and /cart show the estimate under the shipping line.
- The drawer trust strip adds "30-day returns".
- The ar/th returns wording is fixed.
- Theme Check passes: 277 files, 0 offenses.

**Not live.** The GitHub→theme sync skipped this commit. It synced other sessions' later commits at 03:35 UTC, but MAIN `133290917985` still holds the pre-change checksums (`cart-drawer` e80244dd…, `main-cart-footer` ff8dd259…, `pdp-purchase-confidence` 3b82a09b…). The new snippet is absent.
- A scoped `shopify theme push --only` of the 4 Liquid files was refused by the session permission classifier (production deploy). It was not retried.
- Live Liquid checksums equal git `e3d0e07~1`, so a scoped push of the 4 Liquid files overwrites nothing else.
- The live locale JSONs differ from git (Shopify reformats them), so push them only through sync.
- Rollback: `e3d0e07~1` versions.

Not changed (owner business decisions): the return terms themselves (customer-paid return shipping, email-initiated returns) and actual transit time (supplier/carrier).
