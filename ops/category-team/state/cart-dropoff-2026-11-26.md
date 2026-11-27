# Cart -> checkout drop-off (Experto SEO, 2026-11-26, Shopify analytics, read-only)

Organic = referrer_source 'search' without ad parameters (gad_, gclid, gbraid, wbraid, msclkid, cpc). Direct = referrer_source 'direct', same exclusions. All figures are sessions: Carts / Checkout reached / Purchased. "%" = checkout reached over carts.

## Answer
The drop is concentrated in non-US traffic, and within the US in mobile. It is long-standing, not a recent break.

| Organic, 60 days | Carts | Checkout | % | Purchased |
| --- | --- | --- | --- | --- |
| US desktop | 51 | 22 | 43% | 16 |
| US mobile | 127 | 21 | 17% | 10 |
| US tablet | 2 | 1 | | 1 |
| Non-US desktop | 77 | 8 | 10% | 2 |
| Non-US mobile | 367 | 34 | 9% | 12 |
| Non-US tablet | 4 | 1 | | 1 |
| Total | 628 | 88 | 14% | 42 |

Non-US mobile holds 58% of organic carts.

## (a) Country, 60 days
| Country | Organic sessions / carts / checkout / bought | Direct |
| --- | --- | --- |
| United States | 2768/180/44/27 | 4542/215/87/34 |
| Canada | 522/77/9/5 | 362/21/8/4 |
| Romania | 208/54/3/0 | 106/18/1/0 |
| Australia | 362/42/6/2 | 120/7/0/0 |
| Czech Republic | 341/33/6/3 | 128/19/5/3 |
| Italy | 238/28/4/0 | 177/14/3/2 |
| Denmark | 311/25/3/1 | not in top rows |
| Sweden | 345/19/1/1 | not in top rows |
| Mexico | 194/18/3/1 | 122/7/3/1 |
| United Kingdom | 125/17/0/0 | 64/7/0/0 |
| Germany | 124/8/1/0 | 104/16/4/0 |
| Greece | 208/14/3/0 | |
| Poland | 137/12/0/0 | 78/6/1/0 |
| Netherlands | 182/11/0/0 | |
| Switzerland | 62/10/0/0 | |

Organic 14 days: US 1096/58/13/6; Romania 105/29/2/0; Canada 172/28/4/2; Australia 124/15/2/1; Czech 125/12/3/1; Italy 94/10/0/0; UK 50/8/0/0; Denmark 72/8/1/1; Switzerland 31/7/0/0; Mexico 81/7/2/1.

## (b) Device
| | 14 d organic | 14 d direct | 60 d organic | 60 d direct |
| --- | --- | --- | --- | --- |
| Mobile (sess/carts/co/bought) | 2090/180/20/6 | 1153/88/30/16 | 6368/494/56/22 | 4206/324/72/34 |
| Desktop | 836/52/9/6 | 548/30/23/7 | 1739/128/30/18 | 3847/76/79/15 |
| Tablet | 15/3/1/1 | | 43/6/2/2 | 15/1/0/0 |

Direct desktop shows more checkouts than carts: those visits reach checkout without adding in the same visit (returning to a cart or checkout link). So session ratios overstate how many shoppers are lost.

## (c) Entry page, organic 60 days (sess/carts/co/bought)
| Page | |
| --- | --- |
| / | 300/20/5/1 |
| Nordic Yoke product | 123/19/5/2 |
| /cs Christmas collection | 65/13/1/0 |
| /ro Christmas collection | 43/13/0/0 |
| /ro family pajamas | 29/12/0/0 |
| Grapevine pajamas product | 49/7/0/0 |
| /es home | 30/6/0/0 |
| /collections/family-sweaters | 69/6/0/0 |
| Cream Heart cardigans product | 14/6/4/3 |
| Christmas Reindeer product | 22/5/0/0 |

By entry type, 60 d: Product organic 3732/349/59/35 vs direct 4461/243/58/31; Collection 2234/185/20/6 vs 1870/90/17/6; Home 777/62/6/1 vs 913/45/18/7; Article 1390/31/3/0.
Product added to cart: Shopify's session data has no per-product add-to-cart dimension. Not available.

## (d) Language (organic 60 d, by landing URL prefix)
English: 315 carts, 62 checkout (20%), 35 bought. Localized pages: 313 carts, 26 checkout (8%), 7 bought. Language and country overlap; this does not separate them.

## (e) New vs returning
Not available: the only field is the order count of identified customers, filled in mostly after purchase (60 d organic: unidentified 8100/583/46/0; 1 order 45/36/36/36). It cannot show who was returning when they added to cart.

## Pieces per cart
Cart contents of visits that never reach checkout are not in analytics. Completed orders, 60 days (105, all channels): 1 piece 19%, 2 pieces 33%, 3 or more 48%; average 2.7.

## Trend, organic, human sessions, weekly checkout/carts
Sep 28 5/27, Oct 5 8/43, Oct 12 5/52, Oct 19 12/61, Oct 26 11/64, Nov 2 14/110, Nov 9 14/100, Nov 16 15/108, Nov 23 (part week) 4/58. Roughly 10-20% throughout.

## Is "added to cart" inflated?
No evidence of it.
- All 628 organic add-to-cart sessions also viewed a product page.
- Bots: 464 organic bot sessions in 14 d, 1 with a cart.
- Cart sessions without checkout average about 5.7 pages and 4.5 minutes (search+direct, 60 d).
- Theme code: the add requests found sit in submit/click handlers; the sticky button only forwards a shopper's click; no add on drawer open or variant change was found (read of the main call sites, not a full trace).
- Limits: "removed from cart" is false in all 1,029 cart sessions, so removals appear unrecorded. GA4 / pixel counts were not compared (the GA4 pixel listens to Shopify's same product_added_to_cart event).

## Not tested (hypotheses only)
Higher local prices without sale label in Europe, tax/duty uncertainty and mandatory phone at checkout are already listed in _OWNER.md; nothing here proves which one causes the drop.

## Follow-up: Romania and United Kingdom (60 days, same day)

### Source (all sessions / carts / checkout / bought)
| Source | Romania | United Kingdom |
| --- | --- | --- |
| Google search, human | 206/54/3/0 | 142/18/0/0 |
| Direct, human | 106/18/1/0 | 65/7/0/0 |
| Other referrers (Bing, Ecosia, Yahoo, Brave, Facebook, ChatGPT), human | 4/0/0/0 | 6/0/0/0 |
| Bots | 2/0/0/0 | 3/0/0/0 |
| Of which with ad parameters | 0 | 27 sessions, 1 cart, 0 checkout |
No separate referral source brought carts.

### Device and engagement, human sessions
| | Sessions | Pages per session | Avg seconds | Bounces | Checkout |
| --- | --- | --- | --- | --- | --- |
| RO mobile, no cart | 233 | 2.0 | 58 | 144 | 0 |
| RO mobile, cart | 62 | 4.5 | 216 | 0 | 4 |
| RO desktop, cart | 10 | 4.8 | 270 | 0 | 0 |
| GB mobile, no cart | 167 | 1.9 | 34 | 109 | 0 |
| GB mobile, cart | 23 | 3.7 | 233 | 0 | 0 |
| GB desktop, cart | 2 | 2.0 | 68 | 0 | 0 |

### Entry pages of cart sessions
Romania: /ro Christmas collection 14, /ro family pajamas 13, /ro home 5, then 4 or fewer each across about 20 pages (checkouts: swimsuits 1, trunks 1, two product pages 1 each).
United Kingdom: no page above 2 (Nordic Yoke 2, Christmas collection 2, the rest 1).

### Origin spread (cart sessions)
Cities: Bucharest 14 across Android, Windows and iPhone; Ploiesti 4, Suceava 4, many others with 1-3. Browsers mixed (Chrome Mobile, Safari, Samsung Internet, desktop Chrome). UK: no city above 2 in the top rows.

### Time of day (hour in the shop timezone, America/New_York) sessions/carts
RO: 00-05: 76/16; 06-11: 106/27; 12-17: 121/27; 18-23: 15/2.
GB: 00-05: 31/4; 06-11: 65/7; 12-17: 94/12; 18-23: 26/3.
Both have one quiet block, as daily human traffic would. RO carts per day grew in November (0-1 a day in early October, 2-5 a day since 11-03).

### Non-human or single origin?
No sign of it: almost no bots, cart sessions browse several pages for minutes, spread across cities, devices, pages and hours. This cannot rule out people who never intended to buy (for example price checking).

### Organic funnel without Romania, 60 days
| | Carts | Checkout | Bought | Checkout/cart |
| --- | --- | --- | --- | --- |
| All organic | 628 | 88 | 42 | 14.0% |
| Without Romania | 574 | 85 | 42 | 14.8% |
| Non-US without Romania | 394 | 41 | 15 | 10.4% |
Removing Romania changes little: the non-US drop is general.

### Ads versus real organic, 60 days
| Search traffic | Sessions | Carts | Checkout | Bought |
| --- | --- | --- | --- | --- |
| All "search" | 9104 | 696 | 97 | 45 |
| With ad parameters | 949 | 68 | 9 | 3 |
| Real organic | 8155 | 628 | 88 | 42 |
Ad sessions (all sources) are mainly Italy 564/39/2/0 and United States 307/26/7/3.
