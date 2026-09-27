# Owner Morning Packet — yes/no decisions only the owner can make

Prepared by the CEO session overnight (2026-09-27). The items are ranked by how fast each turns into money. Each one lists the exact action, why it matters, and how to undo it. Answer in chat with the numbers you approve (e.g. "yes 1, 2, 4").

Everything that doesn't need you keeps running without you. Tonight that means conversion fixes on the site, Christmas catalog growth with ChatGPT photoshoots, and the product-visibility fixes. See `ops/AGENT_WORKLOG.md`.

## Why these matter (LIVE_VERIFIED 2026-09-27 ~02:00 EDT, Shopify analytics)

- In the last 30 days the store had 6.7k sessions, 151 add-to-carts and **9 orders**.
- In the last 14 days: 77 carts → 18 reached checkout → 5 orders.
- US over 60 days: 115 carts → 48 checkouts → **10 completed (21%)**.
- Money is being left at the cart and checkout. Example: on 2026-09-22 a US shopper built a **$249.91, 9-piece family cart** (Pink Horizon + Light Blue Halter + Coastal Blue Stripe), entered an address, and left. Nothing followed up, because no recovery email is on.

## Urgent operations

- **Order #9572** ($95.36, 4 raglan tees, placed Sep 24) is paid but **unfulfilled after 3 days**. Please place it with BuckyDrop; late shipping hurts reviews and repeat buying.

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
