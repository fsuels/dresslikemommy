# Owner Morning Packet — yes/no decisions only the owner can make

Prepared by the CEO session overnight (2026-09-27). The items are ranked by how fast each turns into money. Each one lists the exact action, why it matters, and how to undo it. Answer in chat with the numbers you approve (e.g. "yes 1, 2, 4").

Everything that doesn't need you keeps running without you. Tonight that means conversion fixes on the site, Christmas catalog growth with ChatGPT photoshoots, and the product-visibility fixes. See `ops/AGENT_WORKLOG.md`.

**Sep 27 result (Shopify, LIVE_VERIFIED):** 2 orders, **$164.66**, including Together Heart. That's up from 0 orders the previous day. Real funnel: about 22 carts → 6 checkouts → 2 orders. Test carts from QA were excluded.

## Why these matter (LIVE_VERIFIED 2026-09-27 ~02:00 EDT, Shopify analytics)

- In the last 30 days the store had 6.7k sessions, 151 add-to-carts and **9 orders**.
- In the last 14 days: 77 carts → 18 reached checkout → 5 orders.
- US over 60 days: 115 carts → 48 checkouts → **10 completed (21%)**.
- Money is being left at the cart and checkout. Example: on 2026-09-22 a US shopper built a **$249.91, 9-piece family cart** (Pink Horizon + Light Blue Halter + Coastal Blue Stripe), entered an address, and left. Nothing followed up, because no recovery email is on.

## Urgent operations (orders; read 2026-09-28 ~10:00 CST in BuckyDrop)

- **#9572** = BuckyDrop S3117776666001 / PO P3117776666001. 4 raglan tees, ships to Germany, paid Sep 24.
  - Status: **"Shipment From Seller"**. The supplier shipped to BuckyDrop, but the warehouse hasn't stocked it in.
  - You authorized me to ask BuckyDrop to ship and update tracking. My WhatsApp send was blocked because the app is on another desktop Space, where I can't reach it in the background, and the full-screen approval timed out.
  - The ready-to-paste message is below.
- **#9574** (Greece, paid Sep 27): Color-Block knit, **Mother XL + Child 1-2 Years**. **Not placed at BuckyDrop**: the original 玺召 offer is delisted.
  - The exact design exists only on old 1688 offer 934491728301. It fails: listed 2025-06, 15-day dispatch, only adult size M, so no Mother XL.
  - Best in-stock alternatives (sourcing session, read-only):
    1. **Taobao 739904873782**: rainbow-stripe knit with a bear, Dongguan, ships ≤3 days, ¥103–109, Mother XL + toddler 90 in stock. Top pick.
    2. Taobao 692948627113: similar, ¥110.
  - **Your call:** message the buyer to offer #1 or a refund. Customer messaging needs your yes.
Ready-to-send buyer email for **#9574**. It goes out only if you approve; customer messaging is your call. Attach 2–3 photos of the Taobao 739904873782 sweater.

```
Subject: Your Dress Like Mommy order #9574 – an update on your sweaters

Hi [first name],

Thank you for your order! We're sorry: the Color-Block knit sweater you chose was just discontinued by our maker, and we can't get it in Mother XL and Child 1-2 Years.

We'd love to offer you a similar matching set instead, a cozy rainbow-stripe knit with a little bear, in the same sizes (Mother XL and Child 1-2 Years), at no extra cost. Photos attached.

Would you like us to send this set instead? If you'd prefer, we'll refund your order in full right away. Just reply "swap" or "refund".

Thank you for your patience,
Fernando
Dress Like Mommy
```

- **Also stuck at BuckyDrop:**
  - **#9560**: "Purchased" since Aug 16 (6 weeks; Xingcheng swim supplier).
  - **#9566**: "In Procurement" since Sep 8.
  - Both are now long past our 12–16 day promise. Chase them, or refund plus an apology.
- **Order #9574 sourcing is now active**, per your 2026-09-28 request. It was previously marked owner-owned.

Ready-to-paste WhatsApp message for the "BD-suelsferro@hotmail.com" group (Scott is in it):

```
Hi Scott and team, Fernando here (Dress Like Mommy).
1) #9572 = S3117776666001 / P3117776666001 (4 raglan tees, to Germany). Placed Sep 24 and still "Shipment From Seller". Please check with the seller, stock it in, ship to the customer as soon as possible and update the tracking number. Thank you!
2) #9574 (new order, Greece): we need our Color-Block knit sweater in Mother XL + Child 1-2 Years (Multi Color). The original 1688 seller delisted it. Can you help find an in-stock seller of the same design on 1688/Taobao? Photos: https://www.dresslikemommy.com/products/color-block-mommy-and-me-sweaters
Backup option if the exact one can't be found: Taobao 739904873782, 妈妈XL + 女宝90码. Please confirm stock for those 2 sizes, but do NOT buy yet until I confirm.
Thanks!
```

## Decisions

| # | Decision (owner does it or says "yes") | Why | Undo |
|---|---|---|---|
| 1 | **UPDATED 05:20:** the abandoned-checkout email is already ON, but it is Shopify's plain default: one email, 0 clicks. To upgrade it (better copy plus a 24h reminder), **install the free Shopify Flow app** (Apps → Shopify Flow → Install), which only you can do. Then I build the upgrade under your existing yes. | Recovers carts like the $249.91 family cart. | Uninstall Flow / revert the email. |
| 2 | **Add the `read_markets` scope** to the "DLM Operator Scripts" Dev Dashboard app, then reinstall. Say "go" and the feed session rebuilds the US Merchant feed. | The US custom Google Shopping feed has been down (503) since 09-23. Google free listings brought 738 clicks in 28 days before that. Christmas shopping on Google Shopping starts now. | Remove the scope. |
| 3 | **Christmas email to past customers** (C-1 to about 5,218 subscribed buyers, Oct). Copy ready: `lanes/email.md`. You declined this on 09-27; it's re-asked because 17 Christmas designs are now live (12 more coming), versus 1 when you declined. | Repeat buyers were 1,493 orders in 2019–21 and 62 since. This is the single biggest lever to win them back. | You can't unsend. Start with a 10% test segment if you prefer. |
| 4 | **Judge.me past-order review import** (you declined it; re-asked because it is the fastest route to real reviews). Review requests for new fulfilled orders are already on: 150 sent, 15 in 30 days. The template gains an honest-review line with REVIEW10; see anchors `2026-09-27-judgeme-fake-reviews-hidden` and `2026-09-27-honest-social-proof-families-since-2017`. | 0 reviews show on 35/35 sampled products. Reviews are the #1 trust signal for a store shoppers don't know. | Stop the import in Judge.me. |
| 5 | **Place one real test order** (any cheap item, then refund) to validate purchase tracking. | Google/Microsoft Ads show "0 conversions" partly because tracking is unverified. We can't scale ads profitably until this is proven. | Refund. |
| 6 | **Microsoft Ads: opt out of the audience/partner network** (~255 of the clicks, 0 sales). | Stops paying for junk clicks. | Opt back in. |
| 7 | **Republish the Gift Card** (declined 09-27; re-ask). | Q4 was 31% of 2025 sales; gift cards are a late-December save when shipping can't arrive in time. | Unpublish. |
| 8 | **Turn on EU local payment methods** in Shopify Payments (Settings → Payments): iDEAL (NL), Bancontact (BE), Klarna, BLIK (PL), MobilePay (DK), wherever Shopify Payments offers them. | Non-US checkout completion is 20% vs 45% in the US. Italy had 8 checkouts and 0 orders. EU shoppers expect their local method. No monthly cost, only per-transaction fees. | Turn each method off. |
| 9 | **Solve the 1688 CAPTCHA** in the helper Chrome (CDP 9333) used by the Christmas catalog session. | 1688 search is blocked, which stalls new Christmas designs: the family pajamas, Mommy & Me winter pajamas, and the new Mommy & Me Christmas dresses line (6–10 designs; we sell none today). | n/a |
| 10 | **Allow "Free standard shipping" wording** on the storefront, instead of "Standard shipping included" (your 2026-05-09 choice after a Denmark mix-up). | Checkout already shows "Free Standard Shipping — FREE" in every zone. "Free shipping" is the phrase shoppers look for and a top purchase driver. | Revert the copy. |
| 11 | **Compare-at / "Sale" badges:** collection cards show "Sale -13%", but product pages show no "was" price. The compare-at is set by formula (price + $10), not from a real past selling price. Options: (a) show compare-at on product pages too; (b) keep it only where the item really sold at that price recently; (c) remove the badges. | Showing a "was" price that never applied is a US FTC and EU pricing-law risk, and the card/PDP mismatch looks inconsistent. I recommend (b). | Reversible. |
| 12 | **Delete unpublished preview themes** I and other sessions created, e.g. 156142436449 (Christmas hero preview) and the older visual-polish and occasion previews. | Housekeeping; they don't affect the live store. | n/a (deletion is permanent, so it's your call). |
| 13 | **Fast-ship Christmas pilot: Printify Premium US print-on-demand** for 3 original matching family Christmas sweatshirt designs (adult, youth, toddler, baby). Memo: `lanes/FAST_SHIP_VENDOR_MEMO.md`. | US delivery in ~4–10 business days lets us sell until **~Dec 10 (standard) and ~Dec 15 (priority)** instead of Dec 8, covering the peak days. Family basket landed ≈46–48%, net ≈35%. Kill gate: ROAS < 4 or landed > 50% by Nov 25. | You: create the Printify account, install its Shopify app, approve Premium ($299/yr or $39/mo) and a ~$70–90 sample order. Undo: cancel and uninstall. **Timing: decide by ~Oct 5** so samples arrive and listings are live by Oct 15. |
| 14 | **Compliance check: US children's sleepwear rule (16 CFR 1615/1616).** Kids' sleepwear in sizes 9M–14 sold in the US must be flame-resistant OR tight-fitting (with labeling). Many of our kids' pajama sets are loose cotton-blend. | Legal and recall risk on our biggest Q4 category. | Your call: ask the suppliers for flammability test reports, or list only tight-fitting kids' sets for the US; I can then update listings and size wording accordingly. I have changed nothing. **Waiting on this decision:** 4 ready drafts of coral-fleece Mommy & Me sets (nordic-blossom, rosy-leopard, sky-stripe, cream-leopard; kids 5–11) are held, not activated. Already live and possibly affected: the 5 new velvet Mommy & Me sets, the 3 new 衣林 Christmas family pajamas, and the older pajama catalog. |
| 15 | **Supplier exception: 阳春市小番茄服饰店** (Guangdong; offer 1049143744816, red family Christmas sweaters, a 2026 design). Only 1 year on 1688, so it fails our ≥5-year rule, but its 30-day readings are strong: 98.6% 48h pickup, 100% fulfillment, 2,262 orders, 0% quality returns, 0% disputes, AA credit. | Adds another 2026 Christmas family sweater design close to the BuckyDrop warehouse. | Say "exception OK" and the sourcing session lists one test design (Tier B, promoted only after an on-time order). Otherwise we skip it. |

## Not asking you (already doing under your standing CEO approval)

- Theme conversion builds:
  - an honest value strip under the price (arrival dates, standard shipping included, returns);
  - the Christmas order-by date shown now;
  - a visible "Size chart" link;
  - Shop Pay / Apple Pay / PayPal buttons inside the cart drawer.
- Christmas catalog expansion: 12 new 2026 designs are being photographed by ChatGPT-Codex, and the Mommy & Me winter pajamas are next.
- Tonight, LIVE_VERIFIED:
  - value strip under the price on every product page;
  - "Order by Dec 8 for estimated Christmas arrival" on Christmas products;
  - visible "Size guide & fit" link;
  - Google structured data with 30-day returns and delivery time;
  - wallet buttons in the cart drawer (Shop Pay, PayPal, Amazon Pay and G Pay, verified with a real cart on 4 phone sizes by the Conversion session; a more compact layout is in progress);
  - 46 blog articles now link to the main collections (written with ChatGPT);
  - Christmas Pajamas sorted best-selling first;
  - 15 Christmas/Halloween redirects;
  - "From $32.99" prices, with no "USD" for US shoppers;
  - one-tap "+ Father / + Child" family chips;
  - Size filter grouped by Mom / Dad / Kids / Baby;
  - Christmas pajama buying guide;
  - native Google titles and descriptions for the main landing pages in 6 languages, now current in all 20 languages (186 fields);
  - cart drawer totals now refresh after quick adds;
  - 3 Christmas articles (pajama guide, sweater guide, family photo outfits), each also in German, Spanish, French, Italian, Dutch, Danish, Swedish and Polish;
  - homepage hero switches automatically to a Christmas edition on Oct 16, after the Halloween cutoff. It's live and dormant until then, and verified on a preview.
- Market-catalog visibility check: restored products could be ACTIVE yet 404 because they were missing from the Markets catalogs. `activate_listing.py` now verifies US/DE/GB/AU/CA visibility on every activation.
  - The 5 restored 2025 winners it surfaced are ARCHIVED again per your 2026-09-27 decision (old designs and prices).
  - `/collections/christmas-pajamas` shows the 11 new 2026 designs plus the onesie. 3 more new 衣林 designs are in draft.
