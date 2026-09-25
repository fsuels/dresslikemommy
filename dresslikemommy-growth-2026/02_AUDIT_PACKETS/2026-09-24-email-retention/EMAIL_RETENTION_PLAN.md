# Email & Repeat-Sales Launch Plan — 2026-09-24

Status: `PREPARED_LOCAL__ADMIN_ENABLEMENT_BLOCKED` (see Blockers). No email has been sent, no automation enabled, no discount created.

## Live readback (Shopify Admin API, 2026-09-24, store dresslikemommy-com)

| Metric | Value | Source |
| --- | --- | --- |
| 2026 orders / buying customers | 143 / 132 | ShopifyQL `FROM sales ... SINCE 2026-01-01` |
| Returning customers 2026 | 6 (4.5%) | same |
| Net sales 2026 | USD 9,116.76 | same |
| Email-subscribed customers (all) | 10,606 | segment `email_subscription_status = 'SUBSCRIBED'` |
| Subscribed buyers, last order 2026 | 82 of 132 | segment query |
| Subscribed buyers, last order since 2024 | 307 | segment query |
| Subscribed buyers, all time | 5,218 | segment query |
| Subscribed non-buyers | 5,388 | segment query |
| New subscribers, last 60 days | 39 | customersCount `created_at` |
| Abandoned checkouts, last 30 days | 14 | `abandonedCheckoutsCount` |
| Welcome/first-order discount code | none exists (`WELCOME10` free) | `discountNodes`, `codeDiscountNodeByCode` |
| Active Christmas/holiday products | 1 of 238 active; all 41 `Christmas Pajamas` tagged products ARCHIVED | `productsCount` |

Notes:
- `customersCount` silently ignores `orders_count` / `email_marketing_state` filters (returned the 15,536 total for every filter); segment queries are the reliable counter.
- Theme already publicly promises "Get 10% off your first order" (footer, `sections/footer-group.json`) and "Get styling tips + 10% off" (`locales/en.default.json`), but no code backs it. The welcome code must be 10% to match.
- Email platform: no Klaviyo/Omnisend in theme; use Shopify Email / Shopify Messaging automations (admin UI only — no Admin API for enabling marketing automations).

## Consent rule

All four sends are marketing: send only to `email_subscription_status = SUBSCRIBED`. 50 of 132 2026 buyers are not subscribed and must not receive them. Store serves EU markets (GDPR).

## 1. Welcome series (trigger: customer subscribes to email marketing)

Discount: `WELCOME10` — 10% off, once per customer, all products, no end date, does not combine with other product/order discounts.

Email 1 (immediately)
- Subject: Your 10% off is inside
- Preview: Matching outfits for the whole family, starting with your first order.
- Body: Welcome to Dress Like Mommy. As promised, here's 10% off your first order: **WELCOME10**. We pick matching looks for moms, daughters, dads, sons and the whole family — dresses, pajamas, swimwear and more. Every item ships directly to you; check the delivery estimate for your country on each product page before you order.
- CTA: Shop matching outfits → /collections/matching-outfits

Email 2 (+3 days, skip if ordered)
- Subject: How to match the whole family (without it looking forced)
- Body: 3 tips + size-chart reminder (sizes run by chart, not by age) + code reminder.
- CTA: Find your family's sizes → best-sellers collection

## 2. Abandoned checkout (trigger: checkout abandoned)

Email 1 (+1 hour)
- Subject: Your family's outfits are still in your cart
- Body: You left something behind. Your cart is saved — pick up where you left off. Questions about sizing? Contact us or check the size chart on the product page.
- CTA: Return to checkout (dynamic checkout link)
- No discount in email 1.

Email 2 (+24 hours, skip if ordered)
- Subject: Still deciding? Here's the size chart
- Body: size reassurance + link to shipping & returns policy pages. No new discount (protect margin; do not train cart-abandonment for codes).

## 3. "Complete the family set" (trigger: order fulfilled; wait 14 days; skip if another order placed)

Rationale: dropshipped delivery is multi-week; 14 days after fulfillment lands near delivery, when the outfit is in hand.

- Subject: Complete the look for the rest of the family
- Preview: The matching pieces for dad, siblings and baby.
- Body: We hope the family is loving the new outfits. Many of our sets come in matching sizes for the whole family — add the pieces for dad, siblings or baby so everyone is in the photo.
- Dynamic block: product recommendations based on the purchased product (Shopify Email "recommended products"). Fallback link: /collections/popular-family-matching and /collections/daddy-and-me.
- CTA: Complete the set
- Optional discount: none by default (owner decision; a returning-customer code would need its own approval).

## 4. October past-buyer holiday email (one-time campaign)

BLOCKED on catalog: the holiday line is not live (all 41 Christmas pajama listings archived; 1 active holiday product). Do not email "the holiday line" until at least one reviewed holiday collection is live with in-stock, supplier-verified products (listing workflow: `ops/prompts/START-HERE.md`).

Audience, in tiers to protect sender reputation (most subscribed buyers last ordered years ago):
- Tier 1: subscribed buyers, last order since 2024 — 307. Send first.
- Tier 2: subscribed buyers with older orders — ~4,911. Send only if Tier 1 shows bounce < 2% and spam complaints < 0.1%.
- Exclude unsubscribed; exclude anyone who ordered in the last 14 days.

Draft
- Subject: Matching Christmas pajamas for this year's family photo
- Preview: Matching sets for the whole family — order early for the holidays.
- Body: Holiday photos are coming. Our matching family Christmas pajamas and holiday outfits are here — sizes for mom, dad, kids and baby. Because each order ships directly to you, order early and check the delivery estimate for your country on the product page.
- CTA: Shop the holiday collection → /collections/christmas-pajamas
- No "back in stock", "bestseller", countdown or guaranteed-by-Christmas claims unless verified at send time.

Target date: 2026-10-08 (Tier 1), Tier 2 ≥ 48h later after readback. Requires explicit owner go on final content + audience at send time.

Cost note: Shopify Email includes a monthly free allowance; Tier 2 volume may exceed it and incur usage billing — owner decides; agent does not change billing.

## Blockers

1. Discount `WELCOME10` creation denied by the session's permission classifier (feature-flag/write gate). Owner must allow it or create it in Admin → Discounts with the parameters above.
2. Shopify admin not signed in in the task-owned in-app browser (`accounts.shopify.com` login page). Automations can only be enabled in the admin UI. Owner signs in; agent does not handle passwords.
3. Holiday catalog not live (see §4).

## Success measures (review 2026-10-24)

- Welcome: `WELCOME10` redemptions / new subscribers.
- Abandoned checkout: recovered orders / abandoned checkouts (baseline 14 per 30 days).
- Complete-the-set: second orders within 45 days of first.
- North metric: 2026 returning-customer rate from 4.5% baseline (ShopifyQL `returning_customer_rate`).

## Holiday line sourcing (owner chose: source new, 2026-09-24)

Detail-page checks on the 5 unverified family Christmas pajama leads from run `2026-09-24-171547-family-matching-1688-auto` (reviewed plan hash a6a2cb648be8813b):

| 1688 offer | Supplier (years) | Verdict | Why |
| --- | --- | --- | --- |
| 989011278121 | 广州市赛美人制衣 (12y, brand smr, 69% repeat, 100% fulfilment) | Test (66) | Red + green "Merry Christmas" tree set; 95% cotton; Dad S–4XL, Mom S–4XL, Kids 2–14, Baby 3–24m; ¥25; dropship yes. Missing: size-chart image, consistent stock proof. Listed 2025-10-27. |
| 988913643690 | 广州娴公主服饰 (7y, also brand smr) | Test (66) | Gingerbread print incl. baby romper + dog suits; same size range; ¥18; dropship yes. Likely a reseller of the same smr factory. Missing: size chart, stock proof. |
| 1083920823413 | 3y supplier | Reject | tenure < 5y, IP term (卡通) |
| 1080011501650 | 1y supplier | Reject | tenure < 5y |
| 1080770657831 | 6y supplier | Reject | IP term (卡通), MOQ 2 |

Only 3 of 8 downloaded images per survivor are real (the jpg files are SVG placeholders).

Stopped: two extra exact searches (`圣诞亲子睡衣 欧美 跨境`, `圣诞节 全家装 睡衣`) hit a 1688 CAPTCHA/punish page in the helper browser. Not bypassed. Owner clears it in the helper Chrome window, then: re-run the two searches, capture size-chart images for the two survivors, prefer the original smr factory (989011278121) and check its store for more Christmas designs.

Timeline check: draft listings + photos + localization before the 2026-10-08 Tier 1 email; supplier-to-customer delivery is multi-week, so the email must carry the per-country delivery estimate, not a Christmas guarantee.
