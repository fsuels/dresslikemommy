# Email and Retention Lane: Million Plan (2026-09-27)

Status: `LOCAL_DRAFT`. Nothing has been sent. No Shopify automation, segment, discount, gift card, form or product was created or changed. Everything below is ready to paste into Shopify Messaging (the app formerly called Shopify Email). The owner does every admin step.

Builds on: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-24-email-retention/EMAIL_RETENTION_PLAN.md`. That plan has the 2026-09-24 live counts (10,606 subscribed; 5,218 subscribed buyers; 307 subscribed buyers since 2024; 14 abandoned checkouts per 30 days). It also records that `WELCOME10` does not exist yet, even though the storefront already promises 10% off.

---

## 0. Voice, facts and honesty rules (read before editing any email)

**Brand voice.** This comes from `VISION.md`, the homepage hero in `templates/index.json` and `locales/en.default.json`.
- Warm, practical and centred on family moments: "moments they want to remember", photos, holidays, pajama mornings.
- Short, rhythmic headlines, for example the live hero "Spooky nights. Snowy mornings. Matching families."
- Plain words and no hype. Clarity first: who each piece is for, what size to pick, when it arrives.
- Use the store's own phrases: "Standard shipping included", "Build your matching set", "each piece is sold separately", "30-day return window" (always with "eligible items").

**Facts every email may use.** Confirm them again on the day you send.
| Fact | Value | Source |
|---|---|---|
| Standard delivery estimate | 12–16 days | `locales/en.default.json` `standard_delivery_window` |
| Shipping | Standard shipping included. Express options, where available, are shown at checkout | locale `free_shipping`, `premium_delivery_window` |
| Returns | Request within 30 days of delivery, eligible items only (unworn, unwashed, tags on). Swimwear, intimates and gift cards are excluded. Return shipping is paid by the customer unless the item arrived damaged | locale `purchase_confidence.returns_*` |
| Christmas 2026 pajama sizes | Child 2–14 Years, Mother S–3XL, Father S–3XL (some styles go to 4XL). **No baby sizes** | `ops/listings/*-family-matching-pajamas-listing.md` |
| Christmas 2026 prices | Child $32.99, Mother or Father $35.99. Each person's set is sold separately | same listing files |
| Fabric | Soft polyester or polyester-blend knit (never write "cotton") | same listing files |
| Collection | `https://dresslikemommy.com/collections/christmas-pajamas` (Matching Family Christmas Pajamas) | listing smart-collection map |

**Hard rules.** A pre-send reviewer rejects any email that breaks one of these.
1. No invented urgency or scarcity. Never write "selling fast", "only X left", "limited stock", "almost gone", a countdown timer, or "back in stock".
2. No stock or place claims. Never write "in stock", "ships from our warehouse", "on hand", "local", "same-day" or "store". Where a shipping line is needed, use "ships directly to you".
3. Never promise delivery faster than 12–16 days. Never write "guaranteed by Christmas". Always call delivery dates estimates.
4. Never write "bestseller", "#1", "loved by thousands", star ratings or review counts unless someone checks them on the day of sending.
5. Send marketing only to `email_subscription_status = 'SUBSCRIBED'`. The store sells into EU markets. Shopify Messaging adds the unsubscribe link and the business address.
6. Never mention suppliers, factories, 1688 or China-specific wording. The delivery estimate carries the honesty.

**Personalization.** Use Messaging's Personalize → First name with the fallback `there`. Where it says `[First name]` below, insert that token.

---

## 1. Automation set (9 emails)

Setup path: **Shopify admin → Marketing → Automations → Create automation → pick the template named below → edit each "Send marketing email" step**. Template labels in the admin change from time to time. If a label differs, match on the trigger and the behaviour.

Discount codes the owner creates in **Discounts** before turning anything on:
- `WELCOME10`: 10% off the order. Eligibility: all customers. Limit one use per customer. No minimum. Does not combine with other discounts. No end date. This backs the promise the site already makes publicly.
- `WELCOMEBACK10`: 10% off the order. Customer eligibility is limited to the segment **S5 Win-back 90–180d** (section 4). Limit one use per customer. Does not combine with other discounts. No end date, because a static automation should not carry a deadline that goes stale.

### 1A. Abandoned checkout (2 emails)

- **Template:** "Recover abandoned checkout".
- **Trigger:** customer abandons checkout.
- **Audience:** email subscribers, which is what the Messaging automation sends to.
- **Exit:** the checkout is completed, or any order is placed.
- **No discount in either email.** A code here would train shoppers to abandon carts to get one.
- **Do not also turn on** the built-in Settings → Checkout "abandoned checkout emails" setting, or customers get duplicates. Home shows neither as live today.

**Email AC-1** (Wait **1 hour** after abandonment, then send)
- Subject: `Your family's outfits are still in your cart`
- Preheader: `Everything you picked is saved. Pick up right where you left off.`
- Body:
  > Hi [First name],
  >
  > You were putting together a matching look, and we saved it for you. Your cart still has everything you chose, sizes included.
  >
  > **A quick size check before you finish:** our sizes follow each product's size chart, not age alone. If you're unsure, open the size chart on the product page and compare it with a favourite piece at home.
  >
  > Standard shipping is included, and your order ships directly to you. The estimated delivery is 12–16 days, and checkout shows the exact estimate for your address before you pay.
  >
  > Questions about sizing? Just reply to this email and we'll help.
- CTA button: `Return to my cart` → dynamic checkout link (the template's default button)
- Block: the template's abandoned-items product block, showing image, title, size and price.

**Email AC-2** (Wait **23 more hours**, about 24h after abandonment. Condition: checkout still not completed. Then send)
- Subject: `Still deciding? Here's what to know`
- Preheader: `Sizes, delivery and returns: the answers most families ask for.`
- Body:
  > Hi [First name],
  >
  > Choosing outfits for a whole family takes a minute. Here are the answers families ask us for most:
  >
  > **Sizing.** Every product page has a size chart with measurements for each family member. Kids' sizes run by chart (2–14 years on our pajamas), and adults by S–3XL or larger where offered.
  >
  > **Delivery.** The standard estimate is 12–16 days, with standard shipping included. For a date like a birthday, a photo shoot or a holiday, please order with that window in mind.
  >
  > **Returns.** You can request a return or exchange on eligible items within 30 days of delivery (unworn, unwashed, tags attached). The full details are in our return policy.
  >
  > Your cart is still saved whenever you're ready.
- CTA button: `Finish my order` → dynamic checkout link
- Secondary text links: `Shipping policy` → `/policies/shipping-policy` · `Return policy` → `/policies/refund-policy`

### 1B. Welcome series (3 emails)

- **Template:** "Welcome new subscribers" (the discount-code variant).
- **Trigger:** customer subscribes to email marketing (pop-up, footer, blog or checkout checkbox).
- **Exit:** the customer places an order. Put a "customer has placed an order?" check before emails 2 and 3.
- **Code:** `WELCOME10`.

**Email W-1** (Send **immediately**)
- Subject: `Welcome! Your 10% off is inside`
- Preheader: `Matching looks for mom, dad and the kids, starting with your first order.`
- Body:
  > Hi [First name], welcome to Dress Like Mommy.
  >
  > We're here for the moments you'll want to remember: holiday mornings, family photos, birthdays, beach days and cozy nights in, all in matching outfits.
  >
  > As promised, here's **10% off your first order**:
  >
  > **WELCOME10**
  >
  > *(Enter it at checkout. One use per customer.)*
  >
  > **How it works:** pick a look, then use "Build your matching set" on the product page to choose a size for each person. Each piece is sold separately, so you only buy what your family needs.
- CTA button: `Shop matching family outfits` → `https://dresslikemommy.com/collections/family-pajamas`. From Oct 15 to Dec 5, swap this to `/collections/christmas-pajamas`.
- Product block: 4 products from the current seasonal collection.

**Email W-2** (Wait **2 days**. Check: no order placed. Then send)
- Subject: `How to size the whole family in 5 minutes`
- Preheader: `One tape measure, one chart, no guessing.`
- Body:
  > Hi [First name],
  >
  > The most common question we get is "what size should I pick for everyone?" Here's the quick way:
  >
  > 1. **Measure, don't guess by age.** Kids grow at their own pace. Measure chest and height, then match them to the size chart on the product page.
  > 2. **Compare with something that fits.** Lay a favourite pajama or tee flat and compare its length and chest with the chart.
  > 3. **Between sizes? Size up** for pajamas and loungewear, so there's room to grow and room to be comfy.
  > 4. **Use "Compare family sizes"** on the product page to see mom, dad and kids side by side.
  >
  > Your code **WELCOME10** is still waiting whenever you're ready.
- CTA button: `Find your family's sizes` → `https://dresslikemommy.com/collections/family-pajamas`

**Email W-3** (Wait **4 days**, day 6 overall. Check: no order placed. Then send)
- Subject: `Planning a family photo? Start here`
- Preheader: `Holidays, birthdays, trips: how to time your matching outfits.`
- Body:
  > Hi [First name],
  >
  > Matching outfits are made for the big moments, so here's how to have them ready in time:
  >
  > **Plan for delivery.** Our standard delivery estimate is 12–16 days, with standard shipping included. For a holiday, a photo session or a trip, we suggest ordering at least 3 weeks ahead so there's time to try everything on.
  >
  > **Pick a look for the moment:**
  > - Christmas morning and holiday cards: matching family Christmas pajamas
  > - Mother–daughter days: mommy-and-me outfits
  > - Dad and the kids: daddy-and-me looks
  >
  > **We're here to help.** Reply to this email with your kids' ages and measurements, and we'll help you choose sizes.
  >
  > Your **WELCOME10** code works on your first order.
- CTA button: `Shop Christmas pajamas` → `/collections/christmas-pajamas` (Oct 15–Dec 5). Off-season: `Shop mommy and me` → `/collections/mommy-and-me`.
- Secondary links: `Daddy and me` → `/collections/daddy-and-me`

### 1C. First-purchase follow-up and cross-sell (2 emails)

- **Template:** "Thank customers after their first purchase" (also listed as "First purchase upsell").
- **Trigger:** order created, with the condition that it is the customer's **first** order (`numberOfOrders = 1`).
- **Exit:** another order is placed (check before FP-2).
- **Why:** 21 first-time buyers came in during the last 90 days and none received a follow-up.
- **Consent note:** this is a marketing automation, so it reaches subscribers only. The owner can also paste FP-1's shipping paragraph into Settings → Notifications → *Order confirmation*. That reaches every buyer as a service message, but it is a separate change for the owner to decide.

**Email FP-1** (Wait **2 days** after the order. Send)
- Subject: `Thank you! Here's what happens next`
- Preheader: `Your delivery estimate, tracking and a few tips for photo day.`
- Body:
  > Hi [First name],
  >
  > Thank you for your first order with Dress Like Mommy. Here's what to expect:
  >
  > **Delivery.** Your order ships directly to you. The standard delivery estimate is 12–16 days. When it's on the way you'll get a shipping email with a tracking link, and that link always has the latest carrier update.
  >
  > **When it arrives.** Try everything on before you wash it. For eligible items, you have 30 days from delivery to request a return or exchange (unworn, unwashed, tags attached).
  >
  > **Photo-day tips.** Shoot near a window in soft morning light, get down to the kids' eye level, and take a "silly one" first. It relaxes everyone.
  >
  > Anything look off? Just reply to this email. We read every message.
- CTA button: `View my order` → the customer account or order status link (Personalize → order status URL, if the template offers it). Otherwise `Visit our shop` → `https://dresslikemommy.com`
- No product block and no discount. This email builds trust and should cut down on "where is my order?" messages.

**Email FP-2** (Wait **19 more days**, about day 21, after typical delivery. Check: no second order. Send)
- Subject: `Complete the look for the whole family`
- Preheader: `Matching pieces for dad, siblings, and the next photo.`
- Body:
  > Hi [First name],
  >
  > We hope the new outfits have made it home and the family is loving them.
  >
  > Many of our looks come in matching sizes for mom, dad and kids, so it's easy to bring everyone into the picture. Add a piece for dad, a sibling, or the cousins you'll see over the holidays.
  >
  > **Heads-up for the holidays:** our Christmas 2026 family pajamas are here, in sizes Child 2–14 Years and Mother and Father S–3XL (some styles to 4XL). With a 12–16 day delivery estimate, ordering early gives you time for try-ons before the big morning.
  >
  > *(If you took a photo in your outfits, reply and share it. We'd love to see it.)*
- CTA button: `Complete the set` → the template's "recommended products" block, based on the purchased product. Fallback: `/collections/christmas-pajamas` (Oct–Dec 5) or `/collections/family-pajamas`
- Discount: none. First-time buyers who come back without a code are the most profitable repeat orders.
- Review the holiday paragraph on Dec 6 and remove it then (see 2D).

### 1D. Win-back (2 emails)

- **Template:** "Win back customers".
- **Trigger:** customer enters segment **S5 Win-back 90–180d**: subscribed, exactly one order, last order 90–180 days ago. That is about 43 people today, plus new entrants each day.
- **Exit:** an order is placed.
- **Code:** `WELCOMEBACK10` in WB-2 only. It is locked to the S5 segment, so it cannot leak into general use.

**Email WB-1** (Send **on segment entry**)
- Subject: `New matching looks for the family`
- Preheader: `A few new favourites since your last order, including Christmas pajamas.`
- Body:
  > Hi [First name],
  >
  > It's been a few months since your last order, and we've added new matching looks since then.
  >
  > **New for Christmas 2026:** family pajamas in red plaid, evergreen Fair Isle, snowy stripes and cheerful reindeer prints, for mom, dad and kids (Child 2–14 Years, adults S–3XL, some to 4XL).
  >
  > Pick a look, then choose a size for each person with "Build your matching set". Standard shipping is included, and the delivery estimate is 12–16 days.
- CTA button: `See what's new` → `/collections/christmas-pajamas` (Oct 15–Dec 5). Otherwise `/collections/family-pajamas`
- Product block: 4 current products.

**Email WB-2** (Wait **7 days**. Check: no order placed. Send)
- Subject: `A thank-you for coming back: 10% off`
- Preheader: `For our returning families: 10% off your next order.`
- Body:
  > Hi [First name],
  >
  > You've shopped with us before, and we'd love to dress the family again. Here's **10% off your next order**:
  >
  > **WELCOMEBACK10**
  >
  > *(One use per customer. Enter it at checkout.)*
  >
  > Planning around a date like a holiday, a birthday or a trip? Our delivery estimate is 12–16 days, so order with that window in mind.
- CTA button: `Use my 10% off` → `/collections/family-pajamas` (or `/collections/christmas-pajamas` from Oct 15 to Dec 5)

---

## 2. Christmas 2026 launch campaign (3 emails and 1 optional)

> **Superseded 2026-09-27** by `../CHRISTMAS_EMAIL_APPROVAL_PACKET.md` for dates and copy. It uses order-by **Dec 8** (to match the live product pages), launches Oct 6, adds the family bundle offer and has real segment counts. Use the packet, not the Dec 5 copy below.

**Pre-send gate.** Every item must pass before email C-1 goes out:
1. The Christmas 2026 designs are **ACTIVE and published to the Online Store**. All of them are DRAFT in `ops/listings/` today.
2. `/collections/christmas-pajamas` shows the designs with final images, not the single vendor placeholder image.
3. A US product page shows "Estimated delivery: 12–16 days" and the size chart renders.
4. Every link in the test email resolves, and a test send to the owner renders on mobile.
5. Segment counts are recorded in section 4.

**Schedule.** Dates are for 2026. Thanksgiving is Thu Nov 26.
| Email | Send | Audience | Purpose |
|---|---|---|---|
| C-1 Launch | Tue **Oct 20**, 10:00 ET. If the gate fails, send on the first Tuesday or Thursday after it passes | Tiers A → B → C in waves (below) | Announce the new designs |
| C-2 Order by Dec 5 | Thu **Nov 19**, 10:00 ET | US engaged: S9 | A real, date-based planning reminder, before the Black Friday inbox rush |
| C-3 Last call | Thu **Dec 3**, 10:00 ET | US engaged who haven't bought Christmas 2026: S10 | The final reminder before the recommended order date |
| C-4 (optional) Gift card | Tue **Dec 8** | S10 | Only if the owner unarchives a digital gift card (section 3) |

**Deadline math** (shown so nobody rounds it into a promise): an order placed Sat Dec 5, plus the 12–16 day standard estimate, lands Dec 17–21. That is an estimate, not a guarantee. The copy says "expected by about December 21" and "estimate". Recheck the US estimate on a product page before C-2 and C-3. If the estimate has changed, move the date. **Never shorten it.**

**Wave plan for C-1, to protect sender reputation.** Most subscribed buyers last ordered 2017–2022 and have not been mailed in a long time. A sudden large send to cold addresses risks bounces and spam complaints, and Shopify can pause sending.
1. Tue Oct 20: **Tier A** (S6a, subscribed buyers since 2024, about 307) plus **S8** (recent subscribers without an order).
2. Thu Oct 22: if Tier A shows bounce under 2% and spam complaints under 0.1% in the Messaging report, send to **Tier B** (S6b, 2021–2023 buyers).
3. Tue Oct 27: if B passes the same thresholds, send to **Tier C** (S6c, pre-2021 buyers).
4. Stop and hold if any wave misses a threshold. Record the readback in `ops/AGENT_WORKLOG.md`.

**Monthly volume against 10,000 free sends.** These are estimates. Record the real counts from section 4.
| Month | Planned sends | Estimate |
|---|---|---|
| Oct | C-1 to all subscribed buyers (about 5,218) plus S8, plus automations (about 300) | about 6,000 |
| Nov | C-2 to US engaged (S9), plus automations | about 2,500–4,000 |
| Dec | C-3 and optional C-4 to S10, plus automations | about 2,000–5,000 |

If a month would go over 10,000, cut the least-engaged tier first. Do not accept usage billing without an owner decision.

### C-1 Launch (Tue Oct 20)
- Subject: `Our Christmas 2026 family pajamas are here`
- Alt subject for an A/B test: `Cozy nights. Christmas morning. Matching families.`
- Preheader: `New plaids, Fair Isle, reindeer and snowy prints for mom, dad and kids.`
- Hero headline: **Cozy nights. Christmas morning. Matching families.**
- Body:
  > Hi [First name],
  >
  > Our new Christmas family pajamas are here. There are fresh designs this year for the whole crew: mom, dad and the kids.
  >
  > **New this season:**
  > - **Jolly Crew:** cheerful red plaid
  > - **Classic Red Plaid:** the timeless Christmas-morning look
  > - **Evergreen Fair Isle:** cozy knit-style pattern in deep green
  > - **Let It Snow** and **Snowy Village Stripes:** wintry and bright
  > - **Lights Out Reindeer:** made for movie nights
  > - **Plaid Tree Trio**, **Joyful Merry Blessed** and **We Are Family:** for the holiday-card photo
  >
  > **Sizes for everyone:** Child 2–14 Years, Mother S–3XL and Father S–3XL (some styles to 4XL). Kids' sets are $32.99 and adult sets are $35.99. Each person's set is sold separately, so you build exactly the family you have.
  >
  > **Plan ahead:** standard shipping is included and the delivery estimate is 12–16 days. For Christmas delivery in the US, we recommend ordering by **Saturday, December 5**. Earlier means more time for try-ons.
- CTA button: `Shop Christmas pajamas` → `https://dresslikemommy.com/collections/christmas-pajamas`
- Product block: 6 products, in this order: Jolly Crew, Classic Red Plaid, Evergreen Fair Isle, Let It Snow, Lights Out Reindeer, Plaid Tree Trio.
- Footer line (non-US readers): `Outside the US? Delivery estimates vary by country. Check the estimate for your country on any product page before ordering.`

### C-2 "Order by Dec 5 for Christmas delivery" (Thu Nov 19)
- Subject: `Christmas pajamas: order by Dec 5 (US)`
- Preheader: `Our 12–16 day delivery estimate means Dec 5 is the date to plan around.`
- Body:
  > Hi [First name],
  >
  > If matching pajamas are on your Christmas list this year, here's the date to plan around:
  >
  > **Order by Saturday, December 5** for US delivery expected by about December 21.
  >
  > Why that date? Our standard delivery estimate is **12–16 days**. It's an estimate, not a guarantee, and December carrier volume is high, so ordering sooner gives you extra room for try-ons and exchanges.
  >
  > **Quick checklist:**
  > 1. Pick your design.
  > 2. Use "Build your matching set" to choose a size for each person (Child 2–14 Years, Mother and Father S–3XL, some to 4XL).
  > 3. Check the size chart on the product page. Between sizes, size up for pajamas.
  >
  > Standard shipping is included.
- CTA button: `Shop Christmas pajamas` → `/collections/christmas-pajamas`
- Product block: 4 products (rotate designs not featured first in C-1: Snowy Village Stripes, Joyful Merry Blessed, We Are Family, Classic Red Plaid).
- **Wording to avoid:** "last chance", "hurry" and "while supplies last". The date is the message.

### C-3 Last call (Thu Dec 3)
- Subject: `Last call for Christmas delivery (US)`
- Preheader: `Saturday, Dec 5 is our recommended last order date for Christmas.`
- Body:
  > Hi [First name],
  >
  > A quick, honest reminder: **Saturday, December 5** is our recommended last order date for US Christmas delivery.
  >
  > With our 12–16 day standard delivery estimate, orders placed by then are expected by about December 21. Orders placed after December 5 may arrive after Christmas, and we'd rather tell you now than disappoint you later.
  >
  > If matching Christmas pajamas are part of your plans this year, this is the week.
- CTA button: `Shop Christmas pajamas` → `/collections/christmas-pajamas`
- Product block: 4 products.
- Real-deadline check: this "last call" refers to the delivery-estimate date only. It is not a sale ending and not a stock claim. Do not add a countdown timer.

### C-4 (optional) "Too late to ship? Give a digital gift card" (Tue Dec 8)
Send only if the owner unarchives a digital gift card and confirms that it is emailed instantly at purchase.
- Subject: `Still shopping? A gift card arrives instantly`
- Preheader: `Delivered by email, so it's there in time for Christmas morning.`
- Body:
  > Hi [First name],
  >
  > It's now past our recommended order date for Christmas delivery of physical orders. If you're still looking for a gift, a **Dress Like Mommy digital gift card** is delivered by email right away, so they can pick their family's matching look in the new year.
- CTA button: `Send a gift card` → the gift card product URL (fill in after unarchiving)

### 2D. Housekeeping on Dec 6
- Swap the Christmas links in W-1, W-3, FP-2 and WB-1 back to `/collections/family-pajamas`, and remove the "Christmas 2026" paragraph from FP-2 and WB-1. After Dec 5 those lines would mislead.
- Add a note in the automations: "Christmas links reverted on 2026-12-06".

---

## 3. Pop-up and signup offer recommendation

**Recommendation: keep 10% off the first order (`WELCOME10`) and add a free printable during Q4. Do not offer physical gift wrap.**

Why 10% and not something else:
1. **The store already promises it publicly.** The footer says "Get 10% off your first order" (`sections/footer-group.json`) and the blog says "Get styling tips + 10% off" (`locales/en.default.json`). The code does not exist yet, which is an honesty gap. Backing the existing promise is the smallest change that is fully truthful. Any other offer means editing the theme copy and about 40 locale files.
2. **The margin holds.** Landed cost is about 48% of list price. Example: a family of 4 (2 adult sets at $35.99 and 2 kid sets at $32.99 = $137.96). Payment fees and ad cost are excluded below.

| Offer | Revenue | Gross profit after landed cost | Gross margin |
|---|---:|---:|---:|
| No offer | $137.96 | $71.74 | 52.0% |
| **10% off (recommended)** | $124.16 | $57.94 | 46.7% |
| $10 off $75+ | $127.96 | $61.74 | 48.2% |
| 15% off | $117.27 | $51.05 | 43.5% |
| 20% off | $110.37 | $44.15 | 40.0% |

`$10 off $75+` keeps about 1.5 points more margin, but it means changing the public copy in the theme and all 40 locales. Revisit it after 60 days of `WELCOME10` redemption data, not before.

3. **Deeper codes are rejected.** 15–20% takes away 29–38% of the gross profit on a first order, and it trains subscribers to wait for codes.

**Zero-cost Q4 add-on: a free printable "Christmas Eve pajama reveal" gift tag and card set.** It is a PDF linked in W-1 from Oct 15 to Dec 24. There is no cost of goods, no dependence on fulfilment, and it is delivered instantly. Owner or design task: make the PDF, upload it to Content → Files, and paste the link into W-1 as `Download your free Christmas Eve reveal cards`.

**Why not free gift wrap.** Orders ship directly from our fulfilment partner to the customer. We cannot inspect or guarantee the wrapping, so a gift-wrap promise would be a claim we cannot verify. Reconsider it only if the fulfilment partner confirms a gift-wrap service in writing, with photos and a cost.

**Gift card (currently archived).** Recommend that the owner unarchive a **digital** gift card before Dec 1. After Dec 5 it is the only honest "arrives before Christmas" product (C-4), and it has no fulfilment risk. Gift cards are already excluded from returns in the policy copy. Owner action only.

**Pop-up setup.** Use the Shopify Forms app. Owner action.
- Headline: `Get 10% off your first order`
- Subtext: `Plus matching-outfit ideas and sizing tips. No spam. Unsubscribe anytime.`
- Q4 subtext (Oct 15 to Dec 24): `Plus a free printable Christmas Eve pajama reveal set.`
- Field: email. Button: `Get my 10% off`. Success message: `Check your inbox. Your code is on its way.` Send the code by email (W-1) rather than showing it on screen, so the address is captured and confirmed.
- Consent line: `By signing up you agree to receive marketing emails. See our privacy policy.`
- Behaviour:
  - Desktop: show after 20 seconds or 50% scroll, or on exit intent.
  - Mobile: a small bottom slide-in or teaser tab, not a full-screen interstitial (this protects Google mobile ranking and product-page conversion).
  - Hide on cart and checkout, and for customers who are already subscribed.
  - Show again at most once every 14 days after it is dismissed.

---

## 4. Shopify segment queries (ShopifyQL segment editor)

Paste these into **Customers → Segments → Create segment**. The editor validates syntax live. If an attribute or function is rejected, the fallback column says what to use. Record the count next to each segment after saving. The 2026-09-24 plan found that `customersCount` ignores filters, so the segment editor is the reliable counter.

| ID | Name | Query | Used by | Expected size |
|---|---|---|---|---|
| S1 | Subscribed, all | `email_subscription_status = 'SUBSCRIBED'` | Baseline | about 10,606 |
| S2 | New subscribers, no order (30d) | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders = 0 AND customer_added_date > -30d` | Welcome monitoring | about 20 |
| S3 | Abandoned checkout, subscribed (7d) | `email_subscription_status = 'SUBSCRIBED' AND abandoned_checkout_date > -7d` | AC monitoring | Low single digits |
| S4 | First-time buyers (90d) | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders = 1 AND first_order_date > -90d` | FP monitoring, cross-sell | Part of 21 |
| S5 | Win-back 90–180d | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders = 1 AND last_order_date BETWEEN -180d AND -90d` | Win-back trigger, `WELCOMEBACK10` eligibility | about 43 |
| S5b | Lapsed repeat buyers | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders >= 2 AND last_order_date < -180d` | Christmas tier priority, future VIP win-back | Record it |
| S6a | Xmas Tier A: buyers since 2024 | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders >= 1 AND last_order_date >= 2024-01-01` | C-1 wave 1 | about 307 |
| S6b | Xmas Tier B: 2021–2023 buyers | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders >= 1 AND last_order_date BETWEEN 2021-01-01 AND 2023-12-31` | C-1 wave 2 | Record it |
| S6c | Xmas Tier C: pre-2021 buyers | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders >= 1 AND last_order_date < 2021-01-01` | C-1 wave 3 | Record it (A+B+C is about 5,218) |
| S7 | Past Christmas-pajama buyers | `email_subscription_status = 'SUBSCRIBED' AND products_purchased(tag: 'Christmas Pajamas') = true` | Priority slice of C-1. Use the alt subject `New designs for your family's pajama tradition` | Record it |
| S8 | Recent subscribers, no order (12 months) | `email_subscription_status = 'SUBSCRIBED' AND number_of_orders = 0 AND customer_added_date > -12m` | C-1 wave 1 add-on | Record it |
| S9 | US engaged, for C-2 | `email_subscription_status = 'SUBSCRIBED' AND customer_countries CONTAINS 'US' AND (last_order_date >= 2024-01-01 OR shopify_email.opened(date: -45d) = true OR shopify_email.clicked(date: -45d) = true)` | C-2 | Record it |
| S10 | US engaged, no Christmas 2026 purchase, for C-3 and C-4 | `email_subscription_status = 'SUBSCRIBED' AND customer_countries CONTAINS 'US' AND (shopify_email.opened(date: -45d) = true OR shopify_email.clicked(date: -45d) = true) AND products_purchased(tag: 'Family Christmas Pajamas', date: -60d) = false` | C-3, C-4 | Record it |
| S11 | Christmas 2026 buyers | `products_purchased(tag: 'Family Christmas Pajamas', date: -60d) = true` | Suppression and a January thank-you | Record it |

Notes and fallbacks:
- **Relative dates.** `-30d`, `-45d`, `-12m` and similar are relative to today. `BETWEEN -180d AND -90d` means 90 to 180 days ago.
- **`customer_countries` rejected?** Build S9 and S10 without it, and send the C-1 non-US footer variant to everyone instead.
- **`shopify_email.opened(...)` / `.clicked(...)` rejected, or no email sent yet in the window?** Before C-1 has gone out these match nobody. For C-2, fall back to S6a + S6b + S8 filtered to the US. For C-3, use S9 minus S11 by adding `AND products_purchased(tag: 'Family Christmas Pajamas', date: -60d) = false`.
- **`products_purchased(tag: ...)` rejected?** Use `products_purchased(id: (<product ids>))` with the Christmas 2026 product IDs. Every Christmas 2026 draft is tagged `Family Christmas Pajamas` and `Christmas Pajamas` in its `ops/listings/*-shopify-import.csv`. Older archived Christmas items share the `Christmas Pajamas` tag, which is intended for S7. The `date: -60d` window keeps S10 and S11 focused on this season.
- **Consent.** Every marketing audience includes `email_subscription_status = 'SUBSCRIBED'`. Do not remove it.

---

## 5. Owner setup order and measurement

**Build order.** Everything is owner-run in the admin. Each step is reversible by turning the automation off or deleting the draft.
1. Create the discounts `WELCOME10` and `WELCOMEBACK10`.
2. Create segments S1–S11 and record the counts.
3. Turn on 1A (abandoned checkout) first. It has the highest intent and needs no discount.
4. Turn on 1B (welcome) and the Shopify Forms pop-up.
5. Turn on 1C (first purchase) and 1D (win-back).
6. Publish the Christmas designs. Then run the C-1 gate and the wave plan.

**Readback after each step.** Confirm the automation shows **Active**, send a test email to the owner, and add an anchor in `ops/AGENT_WORKLOG.md`.

**Success measures.** Review on 2026-11-05 and again on 2027-01-10.
| Flow | Metric | Target or baseline |
|---|---|---|
| Abandoned checkout | Recovered orders ÷ abandoned checkouts | Baseline 0 of about 14 per month. Target 8–12% |
| Welcome | `WELCOME10` orders ÷ new subscribers (30d) | Record it |
| First purchase | Second order within 60 days of the first | Baseline 4.5% returning-customer rate (2026) |
| Win-back | `WELCOMEBACK10` orders ÷ S5 entrants | Record it |
| Christmas | Orders and revenue attributed to C-1 to C-3. Bounce under 2%, spam under 0.1% per wave | Q4 is 31% of annual sales |
| Deliverability | Unsubscribes per send under 0.5% | Stop a tier if it goes over |

**Single next owner action:** create `WELCOME10` in Discounts. It turns the store's existing public "10% off your first order" promise into a working code, and the welcome series and pop-up both depend on it.
