# Christmas 2026 Past-Customer Email: Approval Packet

- Prepared: 2026-09-27, Claude Code (CEO session). Status: `AWAITING_OWNER_APPROVAL`. **Nothing has been sent, scheduled or created.** No segment, email draft, discount or automation was made or changed.
- Source: `lanes/email.md` §2 (the Christmas campaign) and §4 (segments). This packet **supersedes the §2 copy and dates** where they differ; see "What changed from the lane pack".
- What the owner does: answer the four questions in §1. Then either build the emails yourself in Shopify Messaging from §4, or tell the CEO session to prepare the Messaging drafts for your final review.

---

## 1. Decisions for the owner (reply with the numbers)

| # | Decision | Recommended | Why |
|---|---|---|---|
| 1 | Approve sending the Christmas campaign (C-1, C-2, C-3) to **subscribed** customers only | **Yes** | Repeat and direct orders fell from 1,493 (2019–21) to 62 (2024–26), and nobody has been emailed. 5,218 subscribed past buyers are the cheapest orders available. Shopify Messaging includes 10,000 free emails a month, and this plan stays under that |
| 2 | Launch date for C-1, wave A | **Tue Oct 6** (lane pack said Oct 20) | The 15 Christmas designs are already live with every size available, so the lane pack's gate is met. With 12–16 day delivery, early planners buy in October. Starting Oct 6 leaves room for 3 cautious waves on the older lists before Halloween week |
| 3 | Put the bundle offer ("buy 2, get 20% off a 3rd set") in the emails | **Yes** | It is live and automatic (no code). Christmas pajamas are sold one set per person, so a family of 3+ qualifies naturally. Keep the discount active until at least **Dec 31, 2026** (it has no end date now) |
| 4 | Send the optional gift-card email C-4 (Dec 9) | **No for now** | You declined republishing the gift card. Revisit only if you publish a digital gift card before Dec 8 |

---

## 2. Facts used, all checked live on 2026-09-27

Re-check items 1–4 on the morning of each send. If one has changed, fix the copy before sending.

| # | Fact | Value | How it was checked |
|---|---|---|---|
| 1 | Christmas designs | 15 live on `/collections/christmas-pajamas`, every size available | Storefront `products.json` |
| 2 | Prices | Child **$32.99**, Mother or Father **$35.99**; the Snowflake Reindeer onesie style is $33.99 / $36.99. Each person's set is sold separately | Storefront `products.json` |
| 3 | Sizes | Child 2–14 Years; Mother S–3XL; Father S–3XL (7 styles go to Father 4XL). **One style (Snowflake Reindeer onesie) also has baby sizes 3–18 months** | Storefront `products.json` and `jolly-crew…js` |
| 4 | Order-by date | **Tue, Dec 8** for *estimated* Christmas arrival. This is exactly the line on every live Christmas product page (`assets/dlm-holiday-order-by.js`: Dec 24 minus the 16-day top of the estimate) | Theme source and the live PDP line from anchor `2026-09-27-family-bundle-discount` |
| 5 | Delivery estimate | 12–16 days, standard shipping included | `locales/en.default.json` `standard_delivery_window` |
| 6 | Bundle offer | "Family bundle: 3rd piece 20% off": buy 2, get 20% off 1 more; applied automatically; once per order; on the lowest-priced qualifying piece; does not combine with other codes. ACTIVE, no end date | Shopify Admin read of `DiscountAutomaticNode/1315733110881` |
| 7 | Returns | Request a return or exchange within 30 days of delivery. Eligible items only. The customer pays return shipping unless the item is damaged, defective or wrong | Live `/policies/refund-policy` |

**Date honesty.** An order on Tue Dec 8 plus a 12–16 day estimate lands about Dec 20–24. That is an estimate with no buffer at the late end. So every email says "estimated", and the reminder emails say plainly that ordering earlier gives more room. Never write "guaranteed by Christmas".

---

## 3. Audience and schedule

**Audience counts** (Shopify segment editor syntax, via the Admin API, 2026-09-27, counts only; no customer data read or stored):

| Segment | Query | Count |
|---|---|---|
| All subscribed | `email_subscription_status = 'SUBSCRIBED'` | 10,606 |
| **Wave A**: subscribed buyers since 2024 | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders >= 1 AND last_order_date >= 2024-01-01` | **307** (210 in the US) |
| + recent sign-ups, no order (12 months) | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders = 0 AND customer_added_date > -12m` | **48** |
| **Wave B**: subscribed buyers 2021–2023 | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders >= 1 AND last_order_date >= 2021-01-01 AND last_order_date < 2024-01-01` | **1,728** |
| **Wave C**: subscribed buyers before 2021 | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders >= 1 AND last_order_date < 2021-01-01` | **3,183** |
| Past Christmas-pajama buyers (use the alt subject) | `email_subscription_status = 'SUBSCRIBED' AND products_purchased(tag: 'Christmas Pajamas') = true` | 51 |
| US subscribed buyers | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders >= 1 AND customer_countries CONTAINS 'US'` | 3,754 |

Wave B uses `>= 2021-01-01 AND < 2024-01-01` instead of the lane pack's `BETWEEN`; the Admin API accepted this form.

**Schedule (2026, 10:00 ET).** Most of these addresses have not been emailed in years. The waves protect the sender reputation: if Shopify sees high bounces or spam complaints it can pause sending.

| Email | Date | Audience | Size |
|---|---|---|---|
| C-1 Launch, wave A | **Tue Oct 6** | Wave A + recent sign-ups | ~355 |
| C-1 wave B | **Thu Oct 8**, only if wave A bounce < 2% and spam < 0.1% | Wave B | ~1,728 |
| C-1 wave C | **Tue Oct 13**, only if wave B passes the same check | Wave C | ~3,183 |
| C-2 Plan-ahead reminder | **Thu Nov 19** (before the Black Friday inbox rush) | US subscribers who opened or clicked C-1 in the last 45 days, plus Wave A US. If `shopify_email.opened` is rejected, use all US subscribed buyers (3,754) | ~500–3,754 |
| C-3 Last call | **Fri Dec 4** | US engaged who have not bought Christmas 2026 (lane pack S10) | ~500–3,000 |

Stop rule: if any wave has bounce ≥ 2%, spam complaints ≥ 0.1% or unsubscribes ≥ 0.5%, stop the later waves and ask the CEO session to review.

**Volume:** October ≈ 5,270 plus automations (~300); November ≤ 4,000; December ≤ 3,000. All three months stay under the 10,000 free sends, so no billing change is needed.

---

## 4. The emails (paste-ready for Shopify Messaging)

Personalize `[First name]` with Messaging's First name token, fallback `there`. Messaging adds the unsubscribe link and business address automatically; do not remove them.

### C-1 Launch (waves A, B and C)
- **Subject:** `Our Christmas 2026 family pajamas are here`
- **Alt subject for the 51 past Christmas-pajama buyers:** `New designs for your family's pajama tradition`
- **Preheader:** `New plaids, Fair Isle, reindeer and snowy prints for mom, dad and kids.`
- **Headline:** Cozy nights. Christmas morning. Matching families.
- **Body:**
  > Hi [First name],
  >
  > Our new Christmas family pajamas are here, with fresh designs for the whole crew: mom, dad and the kids.
  >
  > **New this season:**
  > - **Jolly Crew:** cheerful red plaid
  > - **Classic Red Plaid:** the timeless Christmas-morning look
  > - **Evergreen Fair Isle:** a cozy knit-style pattern in deep green
  > - **Let It Snow** and **Snowy Village Stripes:** wintry and bright
  > - **Lights Out Reindeer:** made for movie nights
  > - **Plaid Tree Trio**, **Joyful Merry Blessed** and **We Are Family:** made for the holiday-card photo
  >
  > **Sizes for everyone:** Child 2–14 Years, Mother S–3XL and Father S–3XL (some styles to 4XL). Our Snowflake Reindeer onesie style also comes in baby sizes. Kids' sets are $32.99 and adult sets are $35.99. Each person's set is sold separately, so you build exactly the family you have.
  >
  > **Family bundle:** buy any 2 sets and get **20% off a 3rd**. It's applied automatically at checkout, with no code needed.
  >
  > **Plan ahead:** standard shipping is included and our delivery estimate is 12–16 days. For estimated Christmas delivery in the US, order by **Tuesday, December 8**. Ordering earlier gives you more room for try-ons.
- **Button:** `Shop Christmas pajamas` → `https://www.dresslikemommy.com/collections/christmas-pajamas`
- **Product block (6):** Jolly Crew, Classic Red Plaid, Evergreen Fair Isle, Let It Snow, Lights Out Reindeer, Plaid Tree Trio.
- **Small print under the button:** `Bundle discount: one per order, taken off the lowest-priced qualifying set; can't be combined with other discount codes. Outside the US? Delivery estimates vary by country; check the estimate on any product page before ordering.`

### C-2 Plan-ahead reminder (Thu Nov 19)
- **Subject:** `Christmas pajamas: order by Dec 8 (US)`
- **Preheader:** `Our 12–16 day delivery estimate makes Dec 8 the date to plan around.`
- **Body:**
  > Hi [First name],
  >
  > If matching pajamas are on your Christmas list, here's the date to plan around:
  >
  > **Order by Tuesday, December 8** for estimated US delivery before Christmas.
  >
  > Why that date? Our standard delivery estimate is **12–16 days**. It's an estimate, not a guarantee, and December carrier volume is high, so ordering sooner gives you extra room for try-ons and exchanges.
  >
  > **Quick checklist:**
  > 1. Pick your design.
  > 2. Choose a size for each person (Child 2–14 Years, Mother and Father S–3XL, some styles to 4XL).
  > 3. Check the size chart on the product page. If someone is between sizes, size up for pajamas.
  >
  > **Family bundle:** buy any 2 sets and get 20% off a 3rd, applied automatically at checkout.
  >
  > Standard shipping is included.
- **Button:** `Shop Christmas pajamas` → `https://www.dresslikemommy.com/collections/christmas-pajamas`
- **Product block (4):** Snowy Village Stripes, Joyful Merry Blessed, We Are Family, Blue Plaid Reindeer.
- **Small print:** same as C-1.
- **Do not use:** "last chance", "hurry", "while supplies last". The date is the message.

### C-3 Last call (Fri Dec 4)
- **Subject:** `Last call for estimated Christmas delivery (US)`
- **Preheader:** `Tuesday, Dec 8 is our recommended last order date for Christmas.`
- **Body:**
  > Hi [First name],
  >
  > A quick, honest reminder: **Tuesday, December 8** is our recommended last order date for estimated US Christmas delivery.
  >
  > Our standard delivery estimate is 12–16 days, so orders placed by then are expected to arrive in the days before Christmas. It's an estimate, not a guarantee. Orders placed after December 8 may arrive after Christmas, and we'd rather tell you now than disappoint you later.
  >
  > Buying for three or more? The family bundle takes 20% off a 3rd set automatically.
- **Button:** `Shop Christmas pajamas` → `https://www.dresslikemommy.com/collections/christmas-pajamas`
- **Product block (4):** Jolly Crew, Classic Red Plaid, Let It Snow, We Are Family.
- **Small print:** same as C-1. No countdown timer. This refers to the delivery estimate, not a sale ending or stock.

---

## 5. Pre-send checklist (each send)

1. The facts in §2 rows 1–4 still hold. The order-by line on a live Christmas product page still says Dec 8.
2. The bundle discount is ACTIVE (Shopify → Discounts → "Family bundle: 3rd piece 20% off").
3. Send a test email to yourself and open it on your phone. Every link opens the Christmas pajamas page and every product block shows a live product.
4. The segment is the one in §3 and includes `email_subscription_status = 'SUBSCRIBED'`.
5. After each wave, record sent, delivered, opens, clicks, orders, bounces, spam complaints and unsubscribes in `ops/AGENT_WORKLOG.md`.

**Hard rules** (from `lanes/email.md` §0): no invented urgency or scarcity; no stock, warehouse or "local" claims; no "guaranteed by Christmas"; no "bestseller", star ratings or review counts; subscribed customers only; never mention suppliers or where products ship from.

---

## 6. What changed from the lane pack (`lanes/email.md` §2)

- Order-by date Dec 5 → **Dec 8**, to match the live product pages. The reminder copy now says the estimate has no buffer, instead of "expected by about December 21".
- Launch Oct 20 → **Oct 6**, because the pack's gate is already met (designs live with final images, all sizes available).
- C-3 Thu Dec 3 → **Fri Dec 4** (still 4 days before the order-by date); C-4 moved to Dec 9 and stays off.
- Added the live family bundle offer, with its conditions in the small print.
- Corrected "no baby sizes": one style now has baby sizes.
- Filled in real segment counts. Wave B uses explicit dates instead of `BETWEEN`.
- The pack's other Christmas items (the 2D Dec 6 link housekeeping and the automations) are unchanged; if the date moves to Dec 8, do that housekeeping on **Dec 9** instead of Dec 6.

## 7. Measurement

- Per wave: bounce < 2%, spam < 0.1%, unsubscribes < 0.5% (the stop rule above).
- Revenue: orders and sales attributed to C-1, C-2 and C-3 in the Messaging report, plus the share of orders with 3+ pieces (baseline 44%, from the family-bundle anchor).
- Review dates: Nov 5 (after C-1) and Jan 10 (after the season).
