# Free Distribution Lane — $0 marketing that can bring orders now (2026-09-27)

Owner request (2026-09-27, chat): "No one is buying. Do marketing and distribution for free. Get me customers to order and buy from my store."

Status: `REPO_KNOWN` plan + ready-to-post kit. Nothing below was posted, sent or spent. Live numbers are `LIVE_VERIFIED 2026-09-27` via Shopify Admin API/ShopifyQL in session `claude/marketing-distribution-strategy-88o5mn`.

## 1. What the live data says

| Fact | Value | Meaning |
|---|---|---|
| Orders, Aug 15 – Sep 27 | 15 orders, $31–$216, most $50–$110 | People do buy, but only ~2 per week. |
| Sessions, last 30 days | 6,783 total: direct 4,838 · search 1,629 · unknown 237 · social 71 · paid 5 | Search traffic converts; social is almost zero. |
| Carts → completed checkouts, 30 days | direct 86 → 5 · search 80 → 4 · social 3 → 0 | Social is the empty channel, not a broken one. |
| Sales channels | 10 channels; all 270 active products published to each (Online Store, Google & YouTube, Facebook & Instagram, Pinterest, TikTok, Microsoft, Microsoft Copilot, Meta AI, Buy Button, POS) | Channel publishing is already maxed. More "connect a channel" work will not add orders. |
| Discount codes | `WELCOME10` and `REVIEW10` exist and are active (0 uses each) | The storefront's 10% promise is backed. |
| Shopify plan | Basic | Shopify Collabs requires the Shopify plan or higher, and Collabs is not taking new creator signups, so it is not an option. Use per-creator discount codes instead (§4.5). |
| Shopify Messaging email cost | 10,000 free marketing emails per calendar month; abandoned-checkout automations are always free ([Shopify Help](https://help.shopify.com/en/manual/promoting-marketing/create-marketing/shopify-messaging/email/pricing)) | Emailing all ~5,218 subscribed past buyers costs $0. |
| Unfulfilled paid orders | `#9572` (Sep 24, $95.36) and `#9560` (Aug 16, $36.98) show `UNFULFILLED` | Late or missing shipments kill repeat buying and reviews. If `#9560` shipped outside Shopify, mark it fulfilled with tracking. |

**Diagnosis:** the store is not invisible. It has search traffic and occasional buyers. The free levers that are missing are (1) the customer list nobody is emailing, (2) social/creator reach, which is near zero, and (3) Google Shopping's custom feed, down since 09-23. All three are free. Two need the owner's yes.

## 2. Free levers ranked by expected orders

| Rank | Lever | Cost | Who acts | Why this rank |
|---|---|---|---|---|
| 1 | **Christmas email C-1 to subscribed past buyers** (copy in `email.md`) | $0 (inside 10k free) | Owner yes → owner or agent sets it up in Shopify Messaging | 2019–21 repeat/direct buyers drove 1,493 orders; 62 since. These are people who already bought and already trust delivery. No other free lever reaches 5,000 warm buyers. Start with a 10% test segment if preferred. |
| 2 | **Restore the Google Shopping feed** (`read_markets` scope, packet item 2) | $0 | Owner grants scope (2 minutes) | Free Google listings gave 738 clicks in 28 days before the 503. Christmas shopping on Google Shopping has started. |
| 3 | **Owner's own network post** (§4.1) | $0 | Owner posts once on personal Facebook, Instagram and WhatsApp | Friends-and-family reach converts far better than cold social, and the store has had 71 social sessions in 30 days, so anything is an increase. |
| 4 | **Organic Pinterest pins** (§4.2) | $0 | Owner (or the Pinterest lane session) | "Matching family Christmas pajamas" is a planning search that people save months ahead. Pinterest is where that planning happens. The catalog (~5.2k items) is ingested but has no designed pins pointing at the 2026 collection or guides. |
| 5 | **Creator codes, commission only** (§4.5) | Commission only on sales; no fees until a sale | Owner approves the terms; agent creates codes | Moms with 2k–50k followers post family-photo content in Oct–Nov. A code means you pay only after a sale. |
| 6 | **Gift-guide pitches** (§4.6) | $0 | Owner sends from store email | One inclusion in a "best matching family pajamas 2026" roundup can send buyers for weeks. |
| 7 | **Facebook group posts where rules allow** (§4.4) | $0 | Owner | Low odds per post; only in groups with a promo thread. |
| 8 | **Judge.me past-order review import** (packet item 4) | $0 | Owner yes | 0 reviews show. Reviews lift every channel above, especially cold social. |

Not recommended: Reddit self-promotion (bans, and it harms the domain), paid "shoutout" pages, fake reviews or giveaways that require money you haven't approved, and any "limited stock" or "selling fast" wording.

## 3. Tracking: tag every link so we learn what works

Use these UTM links. Shopify analytics then shows orders by `utm_source` (Analytics → Reports → Sessions/Sales by referrer, or ShopifyQL `GROUP BY referrer_source` / `utm_source`).

| Where | Link |
|---|---|
| Owner's Facebook | `https://www.dresslikemommy.com/collections/christmas-pajamas?utm_source=facebook&utm_medium=organic&utm_campaign=xmas2026_owner` |
| Owner's Instagram (bio/story link) | `https://www.dresslikemommy.com/collections/christmas-pajamas?utm_source=instagram&utm_medium=organic&utm_campaign=xmas2026_owner` |
| WhatsApp / text | `https://www.dresslikemommy.com/collections/christmas-pajamas?utm_source=whatsapp&utm_medium=organic&utm_campaign=xmas2026_owner` |
| Pinterest pins | `…?utm_source=pinterest&utm_medium=organic&utm_campaign=xmas2026_pins` (appended to each pin's link below) |
| Facebook groups | `…?utm_source=facebook&utm_medium=group&utm_campaign=xmas2026_groups` |
| Creator codes | Track by the code itself (Discounts → code → usage) plus `utm_source=creator&utm_campaign=xmas2026_<code>` |

Live pages used below (all returned HTTP 200 on 2026-09-27):
- `/collections/christmas-pajamas` (Matching Family Christmas Pajamas)
- `/collections/christmas-sweaters`
- `/collections/family-pajamas`
- `/blogs/news/matching-family-christmas-pajamas-guide-2026`
- `/blogs/news/matching-family-christmas-sweaters-guide-2026`
- `/blogs/news/family-christmas-photo-outfits-2026`

## 4. Ready-to-post kit

### Honesty rules for every post (same as `email.md` §0)

- Allowed facts: child $32.99, mother or father $35.99 on the 2026 pajama sets; each person's piece sold separately; standard shipping included; estimated delivery 12–16 days; "Order by Dec 8 for estimated Christmas arrival" (US, the site's own wording); 30-day return window on eligible items.
- Never: "in stock", "selling fast", "limited", "only X left", "bestseller", review counts, "ships from our warehouse", "guaranteed by Christmas", "cotton".
- Images: download from the product pages on dresslikemommy.com. Never use supplier photos or links.

### 4.1 Owner's personal network post (Facebook, Instagram, WhatsApp) — highest-odds free post

> I've been running Dress Like Mommy since 2017: matching outfits for moms, dads, kids, and the whole family. Our new 2026 Christmas pajamas just went live: plaid reindeer, "We Are Family", snowy village stripes, and more. 🎄
>
> Kids' sets are $32.99 and adult sets $35.99, each sized separately so you only buy what your family needs. Standard shipping is included. For Christmas morning in the US, order by Dec 8 (estimated arrival).
>
> If you've ever wanted that matching Christmas-morning photo, this is the year. And if you know a family who'd love this, a share means a lot to a small business. ❤️
>
> [link: owner Facebook/Instagram/WhatsApp UTM link from §3]

Photo: the lifestyle image from `/products/classic-red-plaid-family-matching-pajamas` or `/products/we-are-family-red-family-matching-pajamas`.

WhatsApp/text short version:
> Our 2026 matching family Christmas pajamas are live! Kids $32.99, adults $35.99, shipping included. Order by Dec 8 for estimated Christmas arrival (US). Would love a share 🎄 [WhatsApp UTM link]

### 4.2 Pinterest: 12 pins (post 2 per day, not all at once)

Board names: `Matching Family Christmas Pajamas 2026`, `Family Christmas Photo Ideas`, `Matching Family Christmas Sweaters`. Pin image: 2:3 vertical (1000×1500) product lifestyle photo from the product page, with a short text overlay (the "Overlay" column). Append `?utm_source=pinterest&utm_medium=organic&utm_campaign=xmas2026_pins` to every link.

Coordination: a separate session owns Pinterest API publishing (`README.md` §3). If that session already publishes designed pins, give it this table instead of posting duplicates by hand.

| # | Overlay | Pin title | Description | Link path |
|---|---|---|---|---|
| 1 | Matching Christmas PJs 2026 | Matching Family Christmas Pajamas 2026 — Plaid, Reindeer & More | New 2026 matching Christmas pajamas for mom, dad and kids. Kids $32.99, adults $35.99, each sized separately. Standard shipping included. | `/collections/christmas-pajamas` |
| 2 | Classic red plaid | Classic Red Plaid Family Christmas Pajamas | The timeless red plaid Christmas-morning look for the whole family. Choose a size for each person on one page. | `/products/classic-red-plaid-family-matching-pajamas` |
| 3 | "We Are Family" | We Are Family Matching Christmas Pajamas (Red) | Matching "We Are Family" holiday pajamas for parents and kids. Made for the Christmas-morning photo. | `/products/we-are-family-red-family-matching-pajamas` |
| 4 | Blue plaid reindeer | Blue Plaid Reindeer Family Matching Pajamas | A softer blue-plaid take on Christmas pajamas, for families who skip the red. | `/products/blue-plaid-reindeer-family-matching-pajamas` |
| 5 | Snowy village stripes | Snowy Village Stripe Family Christmas Pajamas | Cozy striped Christmas pajamas with a snowy village print, sized for kids 2–14 and adults S–3XL. | `/products/snowy-village-stripes-family-matching-pajamas` |
| 6 | Green plaid tree | Green Plaid Merry Tree Matching Family Pajamas | Green plaid Christmas-tree pajamas for the whole family's holiday photos. | `/products/green-plaid-merry-tree-family-matching-pajamas` |
| 7 | How to pick family PJs | How to Choose Matching Family Christmas Pajamas (2026 Guide) | Sizing for every family member, prints that photograph well, and when to order for Christmas. | `/blogs/news/matching-family-christmas-pajamas-guide-2026` |
| 8 | Family photo outfit ideas | Family Christmas Photo Outfit Ideas 2026 | Coordinated and matching outfit ideas for your family Christmas photos: pajamas, sweaters and more. | `/blogs/news/family-christmas-photo-outfits-2026` |
| 9 | Matching Christmas sweaters | Matching Family Christmas Sweaters 2026 Guide | Knit Christmas sweaters for mom, dad and kids: reindeer, Santa and Nordic designs. | `/blogs/news/matching-family-christmas-sweaters-guide-2026` |
| 10 | Nordic reindeer knit | Nordic Reindeer Family Matching Christmas Sweaters | Snowflake-and-reindeer knit tops for the whole family. | `/products/nordic-reindeer-family-matching-sweaters` |
| 11 | Hooded reindeer onesies | Snowflake Reindeer Family Matching Onesie Pajamas | Hooded matching Christmas onesies for kids and adults. | `/products/snowflake-reindeer-family-matching-onesie-pajamas` |
| 12 | Santa sweater set | Jingle Bells Santa Family Matching Sweaters | Green Christmas knit with Santa for family photos and holiday parties. | `/products/jingle-bells-santa-family-matching-sweaters` |

### 4.3 Instagram / Facebook page / TikTok (3 posts + 2 short videos)

Post A (carousel, 4–6 product images):
> New for Christmas 2026: matching pajamas for the whole crew 🎄 Swipe for plaid reindeer, "We Are Family", snowy village stripes and green plaid trees. Kids $32.99 · Adults $35.99 · standard shipping included. Order by Dec 8 for estimated US Christmas arrival. Link in bio.
> #matchingfamilypajamas #familychristmaspajamas #christmaspajamas #matchingpajamas #familyphotos #mommyandme

Post B (single image, sweaters):
> Christmas photo, sorted. Matching family knit sweaters, from reindeer rows to Santa, sized for mom, dad and kids. Link in bio. #matchingchristmassweaters #familychristmasphoto

Post C (guide, carousel of text slides):
> Slide 1: "Matching family Christmas PJs: 3 things to get right". Slide 2: "Size each person by the chart, not by age." Slide 3: "Pick a print that reads in photos: plaid, bold reindeer, stripes." Slide 4: "Order early: estimated delivery is 12–16 days. For US Christmas arrival, order by Dec 8." Slide 5: "Shop the 2026 collection — link in bio."

Short video 1 (Reels/TikTok, 7–10 s): quick cuts of 5 product lifestyle images on beat. On-screen text: "POV: you finally got the whole family to match 🎄" → "2026 matching Christmas pajamas" → "dresslikemommy.com". Caption as Post A.

Short video 2 (10–15 s): "Which one is your family?" with images labeled 1–5. Caption: "Comment your number 👇 Kids $32.99, adults $35.99. Link in bio."

Instagram bio link: the Instagram UTM link from §3.

### 4.4 Facebook groups (only where the group rules allow business posts)

Look for mom, parenting and holiday groups with a weekly "small business" or "promo" thread. Post only there, once per group, and reply to comments.

> Hi everyone! I run a small matching-outfit shop, Dress Like Mommy, since 2017. Our 2026 matching family Christmas pajamas are out: kids $32.99, adults $35.99, standard shipping included. For US Christmas arrival the estimate says order by Dec 8. Happy to help with sizing if anyone has questions! 🎄 [group UTM link]

### 4.5 Creator codes (commission only, no Shopify Collabs needed)

Collabs is unavailable on Basic, so run a simple code-based program. Each creator gets a unique code, e.g. `JESS10`. Usage shows in Shopify Discounts, and you pay commission monthly on delivered, unrefunded orders.

Recommended terms, pending the owner's yes:
- Follower gets 10% off with a **$120 minimum** (about a family of 4). Creator earns 10% of the order subtotal after the discount.
- Why the minimum: from the BuckyDrop profit study, landed cost is ~65% of a 1-item order but ~43–45% of a 4+ item order. At $120: revenue $108 after the code; landed ≈ $54; fees ≈ $3.50; commission ≈ $10.80; net ≈ $39.70 (≈37%). This clears the 35% net floor. A lower minimum does not (`ESTIMATE`).
- No free product gifting without an owner yes, because gifting costs product plus freight.

Who to invite: Instagram/TikTok moms with 2k–50k followers who already post family-photo or "matching outfits" content. Search the hashtags `#matchingfamilypajamas`, `#mommyandmeoutfits`, `#familychristmaspajamas`. Look for real comments, not only likes.

DM template:
> Hi [name]! I run Dress Like Mommy, a small matching-family-outfit shop (since 2017). I love your family photos. Would you like a personal code for your followers for our 2026 Christmas pajamas and sweaters? Your followers get 10% off family orders over $120, and you earn 10% of every order that uses your code, paid monthly. No posting schedule required. Just share it if you like it. Here's the collection: [creator UTM link]

### 4.6 Gift-guide / blogger pitches

Find targets: search Google for `"matching family christmas pajamas" 2026`, `best family christmas pajamas 2026`, `family christmas photo outfit ideas`. Pitch the writers of the non-major-publisher results (parenting blogs, local mom sites). Big publishers rarely add small shops.

> Subject: 2026 matching family Christmas pajamas for your holiday roundup
>
> Hi [name], I enjoyed your [article title]. I run Dress Like Mommy, a small shop that has made matching family outfits since 2017. Our 2026 Christmas pajama line has plaid reindeer, "We Are Family" and snowy village designs. Kids' sets are $32.99 and adult sets $35.99, each sized separately with standard shipping included.
>
> If you're updating the list for 2026, here are the images and details: [collection link]. Happy to answer any questions.
>
> [Owner name], Dress Like Mommy

## 5. Success and kill criteria (measure 14 days after each lever starts)

- Email C-1: success is ≥ 5 orders from ~5,218 recipients (~0.1%). Kill or rethink if < 1 order and unsubscribes > 1%.
- Owner network post: success is ≥ 1 order or ≥ 5 carts from `xmas2026_owner`.
- Pinterest: success is sessions from `xmas2026_pins` trending up week over week. Pinterest lags, so judge at 30 days, not 14.
- Creator codes: keep the creators whose codes produce ≥ 1 order in 14 days; drop the rest.
- Every order is read from Shopify (`GROUP BY utm_source` / discount-code usage), never from platform claims.

## 5b. Built after the kit (2026-09-27, same session)

- **Pinterest bulk pin pack.** 56 designed 2:3 pins (2 per live Christmas design: 14 pajamas, 1 onesie, 13 sweaters) with the design name, product type, the real "from" price and honest size wording ("Kids & adult sizes"; onesies "Baby, kids & adult sizes"). They are hosted in Shopify Files (alt text ends "Dress Like Mommy Pinterest pin"). Two CSVs are in Pinterest's bulk format (`Title, Media URL, Pinterest board, Thumbnail, Description, Link, Publish date, Keywords`; max 200 per file, missing boards are auto-created, a future date schedules the pin): `../pinterest/pinterest_bulk_xmas2026_batch1.csv` and `../pinterest/pinterest_bulk_xmas2026_batch2.csv` (preview: `../pinterest/pin_pack_preview.jpg`; regenerate with `makepins.py` / `makecsv.py`), 2 pins per day at 10:00 and 21:00 ET. Each link carries `utm_source=pinterest&utm_campaign=xmas2026_pins&utm_content=<handle>-pinN`.
  - Owner step: Pinterest (desktop) → Create → Create Pin → Bulk create → upload batch 1. If Pinterest refuses dates more than ~2 weeks out, upload batch 2 about 14 days later, or clear its Publish date column to post now.
  - Coordination: the Pinterest API lane owns automated publishing. This is an owner-run organic upload of new pins. It does not touch the catalog feed, `item_group_id` grouping or ads.
  - Rollback: delete the pins in Pinterest; `fileDelete` the 56 Shopify Files.
- **Family-share tracking** (theme; committed on branch `claude/marketing-distribution-strategy-88o5mn`, NOT live): the product-page share icon now shares a localized "Should we all match?" note (35 locales) plus `utm_source=family_share&utm_medium=pdp_share&utm_campaign=matching_look`. Browser-tested against the live PDP with the new JS swapped in (native share payload and clipboard fallback both correct). Release to `main` was blocked by this session's permission guard and needs the owner's OK.
- **Shop app:** Shopify's help center says eligible stores are added to Shop automatically, even without the Shop channel installed. Appearing in Shop *search* also needs a custom domain, a long selling history, steady order volume and positive reviews ([Shopify Help](https://help.shopify.com/en/manual/online-sales-channels/shop/eligibility/requirements)). Low reviews and low volume are the likely blockers, so the Judge.me past-order review import (owner packet item 4) also unlocks Shop. Installing the free Shop channel (owner, Apps → Sales channels) adds the store-page settings.

## 6. Queue

1. **Needs owner yes now:** email C-1 (or a 10% test); `read_markets` scope; Judge.me import; creator-code terms (§4.5). Fulfil or mark `#9572` and `#9560`.
2. **Owner can do in 10 minutes, no approval needed:** §4.1 personal network post.
3. **Agent next, after owner yes on §4.5:** create the creator discount codes (reversible) and a tracking sheet.
4. **Pinterest lane:** give it §4.2 if it isn't already publishing designed pins.
