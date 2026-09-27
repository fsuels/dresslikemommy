# Owner Morning Packet — yes/no decisions only the owner can make

Prepared by the CEO session overnight (2026-09-27). The items are ranked by how fast each turns into money. Each one lists the exact action, why it matters, and how to undo it. Answer in chat with the numbers you approve (e.g. "yes 1, 2, 4").

Everything that doesn't need you keeps running without you. Tonight that means conversion fixes on the site, Christmas catalog growth with ChatGPT photoshoots, and the product-visibility fixes. See `ops/AGENT_WORKLOG.md`.

## Why these matter (LIVE_VERIFIED 2026-09-27 ~02:00 EDT, Shopify analytics)

- In the last 30 days the store had 6.7k sessions, 151 add-to-carts and **9 orders**.
- In the last 14 days: 77 carts → 18 reached checkout → 5 orders.
- US over 60 days: 115 carts → 48 checkouts → **10 completed (21%)**.
- Money is being left at the cart and checkout. Example: on 2026-09-22 a US shopper built a **$249.91, 9-piece family cart** (Pink Horizon + Light Blue Halter + Coastal Blue Stripe), entered an address, and left. Nothing followed up, because no recovery email is on.

## Decisions

| # | Decision (owner does it or says "yes") | Why | Undo |
|---|---|---|---|
| 1 | **Turn on the abandoned-checkout email** (Shopify Messaging → Automations → "Recover abandoned checkout", 2 emails at 1 h and 24 h, no discount). Copy ready: `lanes/email.md` §1A. | This is the cheapest money we have. About 14 contactable abandoned checkouts come in every 30 days (average ~$60, some $100–250). Typical recovery is 5–15%. | Turn the automation off. |
| 2 | **Add the `read_markets` scope** to the "DLM Operator Scripts" Dev Dashboard app, then reinstall. Say "go" and the feed session rebuilds the US Merchant feed. | The US custom Google Shopping feed has been down (503) since 09-23. Google free listings brought 738 clicks in 28 days before that. Christmas shopping on Google Shopping starts now. | Remove the scope. |
| 3 | **Christmas email to past customers** (C-1 to about 5,218 subscribed buyers, Oct). Copy ready: `lanes/email.md`. You declined this on 09-27; it's re-asked because 17 Christmas designs are now live (12 more coming), versus 1 when you declined. | Repeat buyers were 1,493 orders in 2019–21 and 62 since. This is the single biggest lever to win them back. | You can't unsend. Start with a 10% test segment if you prefer. |
| 4 | **Judge.me past-order review import** (you declined it; re-asked because it is the fastest route to real reviews). Review requests for new fulfilled orders are already on: 150 sent, 15 in 30 days. The template gains an honest-review line with REVIEW10; see anchors `2026-09-27-judgeme-fake-reviews-hidden` and `2026-09-27-honest-social-proof-families-since-2017`. | 0 reviews show on 35/35 sampled products. Reviews are the #1 trust signal for a store shoppers don't know. | Stop the import in Judge.me. |
| 5 | **Place one real test order** (any cheap item, then refund) to validate purchase tracking. | Google/Microsoft Ads show "0 conversions" partly because tracking is unverified. We can't scale ads profitably until this is proven. | Refund. |
| 6 | **Microsoft Ads: opt out of the audience/partner network** (~255 of the clicks, 0 sales). | Stops paying for junk clicks. | Opt back in. |
| 7 | **Republish the Gift Card** (declined 09-27; re-ask). | Q4 was 31% of 2025 sales; gift cards are a late-December save when shipping can't arrive in time. | Unpublish. |

## Not asking you (already doing under your standing CEO approval)

- Theme conversion builds:
  - an honest value strip under the price (arrival dates, standard shipping included, returns);
  - the Christmas order-by date shown now;
  - a visible "Size chart" link;
  - Shop Pay / Apple Pay / PayPal buttons inside the cart drawer.
- Christmas catalog expansion: 12 new 2026 designs are being photographed by ChatGPT-Codex, and the Mommy & Me winter pajamas are next.
- Fixed tonight: 5 restored Christmas best-sellers were ACTIVE but invisible (404) because they were missing from the Markets catalogs. They are now live; `/collections/christmas-pajamas` shows 17 designs, up from 12. The activation script now checks this, so it can't recur.
