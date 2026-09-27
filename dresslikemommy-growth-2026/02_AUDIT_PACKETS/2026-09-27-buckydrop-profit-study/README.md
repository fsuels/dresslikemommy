# BuckyDrop History Profit Study + Growth Plan — 2026-09-27

Scope: read-only study of the full BuckyDrop history (615 orders, 606 parcels; 2023-07 → 2026-09), joined with Shopify analytics (2017 → 2026-09) and the Shopify admin Home insights. No live writes to BuckyDrop or to Shopify prices. Customer PII is excluded, and so are vendor URLs.

Status labels: numbers below are `LIVE_VERIFIED` read-backs on 2026-09-27, except where marked `ESTIMATE`.

## 1. Where the money goes (608 fulfilled BuckyDrop orders)

| | USD | % of item revenue |
|---|---:|---:|
| Item revenue at store price (BuckyDrop `sellingPrice`; matches Shopify gross $41.2k for the period) | 40,355 | 100% |
| Product + China domestic + BuckyDrop purchase fees | 10,876 | 27% |
| International freight + packing + priority outbound | 8,536 | 21% |
| **Landed cost** | 19,412 | **48%** |
| Shopify returns/refunds (analytics) | ~1,490 | ~3.7% |
| Payment fees (ESTIMATE 2.9% + $0.30) | ~1,560 | ~3.9% |
| **Contribution before advertising** | | **~44%** |

**Freight is 44% of landed cost.** It is the biggest lever. The fitted US YunExpress Registered Air Mail cost (2025-06 → now, n=107) is **¥45.4 per parcel + ¥8.2 per 100 g**, including ¥11.5 of bag and priority-outbound fees.

At the paid-growth target of 650% ROAS (ads = 15.4% of revenue), net is about **29%**, below the owner's 35% floor. To reach 35% net at 650% ROAS, landed cost must be **≤ ~42%**.

### Basket size decides profit

| Items per order | Orders | Revenue per order | Landed % |
|---|---:|---:|---:|
| 1 | 70 | $24 | **65%** (loses money after ads) |
| 2 | 292 (48% of orders) | $46 | **52%** |
| 3 | 90 | $66 | 48% |
| 4 | 87 | $96 | 45% |
| 5+ | 69 | $157 | 43% |

The typical order is mom + child, 2 pieces, around 457 g. Freight on that parcel is about $11.20, whether the pieces sell for $15 or $35.

### Price floor problem (catalog-wide)

- **109 of 257 active products start under $20.** Under the free-shipping model, a 2-piece order at under $20 per piece cannot meet the 50% landed rule.
- Break-even rule: landed ≤ 50% on a same-price pair requires unit cost ≤ (price − $11.50) / 2. At $14.99 that means ≤ $1.75, which is impossible. At $24.99 it means ≤ $6.75.
- Worst active sellers are the $14.99–16.99 swimsuits:
  - Chic Family Tides: 76% landed on a pair.
  - Chic Family Bonding: 76%.
  - Vibrant Duo-Tone: 77%.
- The 21 Mommy & Me pajama listings added 2026-04-21 cost $11.59–19.27 per piece and are priced $26.99–35.99. Pair landed:
  - Meow Star: 70%.
  - Red Panda: 68%.
  - Welsh Dinosaur: 63%.
  - Vintage Cottage: 53%.
- By contrast, the new 2026 Christmas family pajamas at $32.99–35.99 run about 31–40% landed. Family Christmas orders average 4–7 pieces, which makes them the most profitable orders the store gets.

### Countries

| Market | Orders | Landed % | Note |
|---|---:|---:|---|
| US | 393 | 49% | YunExpress Registered |
| UK | 69 | 43% | Before the +15% Markets increase |
| AU | 24 | 43% | Before the +20% increase |
| CA | 30 | 49% | C$48 unchanged; candidate for +10–15% |
| EU (DK/DE/GR/NL/CZ/BE …) | ~45 | 47–60% | Before the +15% increase |

**Couriers to avoid:** Mainland China UPS 87%, YunExpress Air Express 67%, EMS 67%. These were December 2024 rush shipments that ran at a loss. Plan Christmas early instead.

## 2. BuckyDrop fees worth reviewing

- **Priority Outbound ¥10 on 604 of 606 parcels** = ¥4,180 (~$588; $1.41/order, about 2% of revenue). It is applied to every parcel, including all 139 in 2026. Recommendation: keep it for November–December; test turning it off January–August if the warehouse's standard SLA is comparable. `OWNER_DECISION`.
- **Tag switch + custom bag replacement:** ¥1,447 value-added services (~$0.12/item). Small; keep, since they support branding.
- **Domestic China freight** ¥4,780 (~$1.10/order), multiplied when one order spans several vendors. Keep "complete the family" bundles within one vendor's line.

## 3. Supplier history (lead = PO created → stocked at BuckyDrop warehouse)

- **Fast and clean (median ≤ 3 d, p90 ≤ 4 d, 0–1 returns): promote to the preferred list.**
  - 广州衣林服饰 (Safari animal pajamas; 23 orders, 2.5 d/3.7 d)
  - 廉江市城北依曼 (20 orders, 2.6/3.9, 0 returns)
  - 广州市佐雅服装厂 (Christmas pajamas; 2.4/3.4)
  - 深圳市斯蒂琪 (2.6/3.2)
  - 东莞市必橙纺织品 (Christmas Crew; 2.7/3.4)
  - 湖州托马拓 (2.6)
  - 广州玺召 (knit sweaters; 26 orders, 2.9/5.2)
- **High volume, acceptable:** 绍兴涟可 (47 orders, family dress/shirt sets, 3.5/10.3 — slow p90). Swimwear 嗨鱼 (63 orders, 3.9/7.1).
- **Problems:**
  - 温州陈东弟: winter nightgown best-seller, but 10 of 45 items returned (22%) and p90 14 d. Re-source the nightgown.
  - 东莞虎门昱宝贝 (Ivory Meadow): 6 of 8 items returned.
  - 广州千程: p90 15.7 d.
  - 广州布莱士: median 8.2 d.
  - 深圳丹维尔: p90 44 d.
  - Xingcheng 兴城 swim cluster: #9566 never shipped.
- Only 18 orders were returned and 3 cancelled out of 615; 103 items were returned in total.

## 4. What changed: why sales fell from $121k (2020) to $6.7k (2025)

| Year | Orders | Net sales |
|---|---:|---:|
| 2018 | 1,143 | $57.4k |
| 2019 | 1,490 | $76.1k |
| **2020** | **2,264** | **$117.1k** |
| 2021 | 1,629 | $86.8k |
| 2022 | 874 | $51.7k |
| 2023 | 470 | $25.3k |
| 2024 | 229 | $14.5k |
| 2025 | 103 | $6.5k |
| 2026 YTD | 143 | $9.1k |

| Referrer | 2019–2021 orders / net | 2024–2026 orders / net | Change |
|---|---:|---:|---:|
| Google search | 2,271 / $117.0k | 178 / $10.9k | −92% |
| Direct "dresslikemommy" (repeat + brand) | 1,493 / $82.0k | 62 / $3.7k | −96% |
| Bing + Yahoo + DDG | 392 / $20.0k | 76 / $5.4k | −81% |
| Social (IG/FB/Pinterest) | 140 / $6.3k | 3 / $0.3k | small either way |

**Diagnosis:** the store lost its Google visibility (organic and Shopping) and its repeat-customer engine. Product-market fit did not fail. AOV has been stable at $55–68 throughout.

## 5. Shopify admin signals (Home, last 30 days, read 2026-09-27)

- Conversion rate 0.21% (−43%). Treat this as diagnostic only: the owner's spike-day exclusions apply (`DEC-20260926-SPIKE-DAY-EXCLUSIONS`), so the real conversion rate is `LIVE_READBACK_REQUIRED`.
- **Abandoned-checkout email is not live** ("ready… before it goes live").
- No post-purchase flow: 21 first-time buyers in the last 90 days.
- No win-back: 43 subscribed one-time buyers 90–180 days old.
- The **Gift Card is archived** while October–December was 31.2% of 2025 sales.

## 6. Path to $1M/year (realistic staging)

$1M/year ≈ 10,000 orders at $100 AOV, or 15,000 at $67 AOV. That is 4.4–6.6× the 2020 peak. It needs every engine, not one.

### Stage 1 — next 90 days: get back to a $100k+ run-rate (Q4 is 31% of the year)

1. **Activate the 11 Christmas 2026 drafts** (owner). Images are rolling in. US last safe order date is about **Dec 5** (≈4 d dispatch + 12–16 d Registered).
2. **Email the dormant customer base.** Shopify holds 10,000+ customer records, and the store had about 7,600 orders in 2017–2022. The exact subscribed-buyer count needs a Segments readback.
   - Turn on abandoned checkout, welcome, post-purchase and win-back flows.
   - Send a "Christmas 2026 family pajamas" launch.
   - Shopify Messaging includes 10,000 free emails a month.
   - The direct/repeat channel was $82k in 2019–2021.
3. **Republish the Gift Card** for the holidays: no fulfillment cost.
4. **Fix the unit economics:**
   - Free shipping over **$69**, and a flat shipping fee (e.g. $6.95) below it; this also lifts AOV. **Or** raise the price floor to adult ≥ $24.99 and child ≥ $19.99.
   - Reprice the Mommy & Me pajama line to ≥ $44.99 (mom) / $39.99 (child), or re-source it.
   - Test one of these first; both change conversion. `OWNER_DECISION`.
5. **Google Shopping / free listings for the Christmas line.** Google was 42% of peak revenue. Paid work follows `ops/marketing/` gates; the Google identity verification is still owner-blocked.

### Stage 2 — 2027 H1: rebuild Google and the catalog (target $250k)

- SEO rebuild of the intent pages that used to rank:
  - Collections for "mommy and me outfits", "family christmas pajamas", "matching family swimsuits", "daddy and me".
  - Product reviews, since the store needs review volume and stars.
  - Localized markets.
- Weekly expansion rounds (5–15 designs from preferred suppliers), with seasonal pushes listed 8–10 weeks ahead.
- Pinterest organic plus Pinterest/Google catalog ads within the ROAS gate.

### Stage 3 — 2027 H2+: scale engines (target $1M)

- Meta (Facebook/Instagram) Advantage+ catalog ads with UGC/Codex lifestyle video. This category is visual; it is how the big family-matching brands scale.
- TikTok Shop / marketplaces for reach.
- A **US 3PL for the top 20 best-sellers** once volume justifies it (sea freight in bulk, 3–5 day US delivery). A 12–16 day delivery window caps conversion at scale. This is only an honest customer claim once real stock exists there.

## 7. Next single owner action

Activate the Christmas 2026 drafts as each gets its 4 images. Q4 is the one window where the store already has proven high-basket demand, and the season is time-boxed.
