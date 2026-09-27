# Merchandising lane: category and catalog plan for the weekly expansion rounds (2026-09-27)

Lane: merchandising, planning only. Parent packet: `2026-09-27-million-plan`.
Task class: `BUILD` (local plan). Everything was read-only: Shopify Admin GraphQL (products, drafts, nodes) and ShopifyQL (sales, sessions). There were no Shopify writes and no 1688/BuckyDrop browsing. No credential or vendor URL appears here.

Coordination: the ACTIVE claim "Product expansion round 1" (`ops/AGENT_COORDINATION.md`, 2026-09-27) owns Christmas family pajamas plus Mommy & Me long-sleeve winter/Christmas pajamas, `TRUSTED-SUPPLIERS.md` and `decisions.json`. Briefs 1–2 below are inputs to that claim holder, not a second writer.

## Evidence labels

| Label | Meaning |
|---|---|
| `LIVE_VERIFIED 2026-09-27` | Read in this session: Admin GraphQL (257 ACTIVE and 15 DRAFT products) and ShopifyQL through the Shopify connector (same shop). |
| `REPO_KNOWN` | From a repo file: the profit study, `TRUSTED-SUPPLIERS.md`, the Christmas-line packet, the workflow or the worklog. |
| `ESTIMATE` | Keyword classification of products into categories, garment weights, or model arithmetic. Replace these with real readings. |
| `LIVE_READBACK_REQUIRED` | Must be read on the exact surface before any action depends on it. |
| `OWNER_DECISION` | Needs the owner's choice. |

Data limits:
- Categories come from a keyword classifier over title and productType. Boundaries are about ±10% (`ESTIMATE`).
- ShopifyQL net sales since 2023-07-01 total $34.4k across still-existing products. Another ~$4.7k sits on deleted products and is not attributable.
- 90-day landing-page sessions include crawler traffic (see `2026-09-26-traffic-quality-crawler-and-audience-network`). They are diagnostic only.

---

## 1. Priority order (what the rounds do, in order)

1. **Christmas family pajamas.** Brief 1; urgent and the highest-margin orders.
2. **Winter nightgowns + Mommy & Me winter pajamas (re-source).** Brief 2; a short window, and it replaces an Avoid supplier and 3 loss-makers.
3. **Spring 2027 mother-daughter dresses + jumpsuits.** Brief 3. This is the largest season, and jumpsuits have 0 active items today.
4. **Valentine's 2027 capsule** (heart knits and dresses; tees only if they pass the price rule).
5. **Summer 2027 Hawaiian/vacation family sets + Daddy & Me shirts** from one vendor line.
6. **Summer 2027 swim re-source**, replacing 14 zero-sale swim listings at a workable price.
7. **Fall knits refresh** from 广州玺召, for Fall/Christmas 2027.
8. **Test lanes:** couples, maternity, siblings. Up to 5 designs each, and only when earlier rounds are on schedule.

Prune actions (§6) run alongside the rounds. Each archive is a Shopify write and needs an owner-approved packet.

## 2. Seasonal list-by deadlines (from 2026-09-27)

"Live by" means ACTIVE, with 4 images and localization closeout done.

Seasonality basis: 2018–2022 monthly net sales (`LIVE_VERIFIED 2026-09-27`, ShopifyQL):
- Mar–May is **35%** of the year.
- Nov–Dec is 23%, Jun–Aug 19%, Sep–Oct 12% and Jan–Feb 11%.
- April alone is 12.9%.

**Spring (Easter plus Mother's Day) is historically the biggest peak, larger than Christmas.**

| Peak | Peak date | Live by | Status / note |
|---|---|---|---|
| Christmas 2026 | Dec 25 | **Oct 15, 2026** for any design beyond the drafts. Hard stop Nov 1 for new Christmas listings. | **LATE**: the workflow target was early Sep. The homepage/menu Christmas gate opens Oct 15. Black Friday is Nov 27. The last safe US order is about **Dec 5** (`REPO_KNOWN`, profit study). The UX lane's Dec 8 does not visibly include 7-day dispatch, so use Dec 5. |
| Winter / New Year (nightgowns, fleece, knits) | Nov–Feb demand | **Nov 1, 2026** | Replaces the Avoid nightgown supplier before demand. |
| Valentine's 2027 | Sun Feb 14 | **Dec 5, 2026** | Last US order about Jan 25. 2026-release designs pass the year gate if they are listed in 2026. |
| Easter 2027 | Sun Mar 28 | **Jan 15, 2027** | Listing happens in 2027, so the release-year gate means 2027 designs. The round starts once 1688 shows 2027 spring releases. |
| Mother's Day 2027 | Sun May 9 | **Mar 1, 2027** | Same dress/jumpsuit lines as Easter; add prints. |
| Summer / vacation / swim 2027 | May–Jul | **Mar 1, 2027** | May–Jun 2026 were 2026's best months ($1.7k, $2.3k). |
| Back to school 2027 | Aug | May 2027 | Low priority for this store. |
| Halloween 2027 | Oct 31 | Early Aug 2027 | 5 active + 1 draft now. No new Halloween listings this season. |
| Christmas 2027 | Dec 25 | **Sep 1, 2027** | Source in Jul–Aug as 2027 designs appear. Target 45 live designs (§7). |

## 3. Top 3 expansion-round briefs

### Brief 1 — Christmas family pajamas (round 1 continuation; the claim holder executes)

- **Category / collections:** Family Matching → `christmas-pajamas`, `family-pajamas`, `matching-family-christmas-outfits`.
- **Why first:**
  - Christmas pajamas were 11% of net sales since 2023-07 ($3.7k, 45 orders), with **3.5 items per order**, the highest of any category (`LIVE_VERIFIED`, `ESTIMATE` classification).
  - Family Christmas orders run 4–7 pieces at 31–40% landed (`REPO_KNOWN`).
  - Today there is **1 ACTIVE** design (the Snowflake Reindeer onesie) plus **11 DRAFTS** (`LIVE_VERIFIED`).
- **Garment types:**
  - Long-sleeve 2-piece top and pants sets: 8 designs.
  - One-piece fleece family onesies: 2 designs.
  - Whimsical, non-IP animal Christmas prints in the "Holiday Safari Animal" style: 2 designs. That line is the #2 best-seller since 2023-07: $933, 9 orders, **37 units**.
- **Roles:** Dad (S–3XL, 4XL where the line has it), Mom (S–XL/3XL), Kid (2–14).
  - Baby (3–24M romper) is an `OWNER_DECISION`. The 2026-09-26 run excluded baby SKUs, but 4–7 piece family orders usually include a baby.
- **Season:** Christmas 2026. Live by Oct 15; stop at Nov 1.
- **N = 12 new designs.** With the 11 drafts and the onesie, that makes 24 live this season.
- **Suppliers, in order** (proven history `REPO_KNOWN`; re-read the 1688 gate per offer):
  1. 广州市佐雅服装厂: Christmas Elf. 13 orders, lead 2.4/3.4 d, 1 of 39 items returned. The Elf set sold 21 items in 3 orders.
  2. 广州衣林服饰: Holiday Safari Animal. 23 orders, 2.5/3.7 d. Re-check each offer for IP terms, because of an earlier flag on other offers.
  3. 东莞市必橙纺织品: Christmas Crew. 6 orders, 2.7/3.4 d, 0 of 25 returned.
  4. Tier A 广州市赛美人 (smr): only orderable 2026 designs not already drafted. Its composition field often says polyester, so list honest fabric.
  5. One test design each from Tier B 深圳市诗茹梦 (fleece onesies; read its dispatch promise) and 南通市万趣 (48h pickup is 87%, so 1 design only).
- **Hard gates:** 2026 release year; no Grinch/Stitch/Rudolph-style/skull; the offer's own size chart (or disclosed same-line reuse); dropship MOQ 1.
- **Price:**
  - Adult $35.99 / Kid $32.99; onesie $36.99 / $33.99. This is the live precedent.
  - **Unit-cost ceiling:** average ≤ $8.07 for 42% landed, and ≤ $10.83 at the 50% rule (560 g pair). Onesie: ≤ $7.10 / ≤ $9.94.
  - smr at ¥37/¥27 lands about 32% (`ESTIMATE`).
- **Kill rule:** any design that cannot be live by Nov 1 is dropped from this season and queued for Christmas 2027.

### Brief 2 — Winter nightgowns + Mommy & Me winter pajamas (re-source)

- **Category / collections:** Mommy & Me sleepwear → `pajamas`, `family-pajamas`. A `nightgowns` smart collection is an `OWNER_DECISION`; none exists.
- **Why:**
  - The Winter Fleece Nightgown made $658 in 9 orders since 2023-07, and mother-daughter nightgowns made $4.0k in 2019–21 (`LIVE_VERIFIED`).
  - Its supplier 温州陈东弟 is **Avoid**: 10 of 45 items returned, p90 14.3 d (`REPO_KNOWN`).
  - Only 1 nightgown is active.
  - Three active M&M pajamas lose money at their prices: Red Panda, Meow Star Garden and Welsh Dinosaur, at 63–70% pair landed (`REPO_KNOWN`, reprice anchor).
- **Garment types:**
  - Fleece, flannel or coral-velvet long-sleeve nightgowns: 4.
  - Long cotton "classic white" nightgowns: 2. This type made $260 since 2023-07 and $1.2k in 2019–21.
  - Long-sleeve 2-piece M&M pajama sets in winter prints that are not Christmas-specific, so they sell Nov–Feb: 4.
- **Roles:** Mom (S–XL, 2XL where offered) and Girl (2–12).
- **Season:** Winter 2026–27. Live by Nov 1.
- **N = 10.**
- **Suppliers:**
  - No proven nightgown supplier exists yet.
  - Start with Tier B 深圳市诗茹梦: 6 years, 99.6% fulfillment, 10k+ dropship resellers. It makes fleece family pajamas; read its dispatch promise.
  - Then check the M&M and women's sleepwear categories at 广州衣林 (pajama factory, proven) and 广州市赛美人 (women's basics).
  - Then a new Guangdong search, e.g. `2026 冬季 亲子睡裙 母女 法兰绒 广州`.
  - Exclude 温州陈东弟.
- **Price:**
  - Nightgown: Mom $36.99 / Girl $32.99 (650 g pair). Unit-cost ceiling ≤ $7.76 for 42%, ≤ $10.56 at 50%.
  - M&M pajama set: $34.99 / $31.99 (520 g pair). Ceiling ≤ $7.88 / ≤ $10.56.
- **Kill rule:** if an offer only passes above $39.99, reject it rather than price up. The red-panda line ($11.6–19.3 per piece) is the counter-example.

### Brief 3 — Spring 2027 mother-daughter dresses + jumpsuits

- **Category / collections:** `mommy-and-me`, `mother-daughter-matching-dresses`, `sundresses`, `maxi-dresses`, plus a new jumpsuit/romper line. No jumpsuit collection exists; creating one is an `OWNER_DECISION`.
- **Why:**
  - Mar–May is 35% of the historical year.
  - Mother-daughter dresses are the largest category since 2023-07: ~$7.7k, 22%, 146 orders.
  - **The all-time #1 product** is the Floral Long-Sleeve Maxi with Pockets: $10.7k in 2019–21, $766 since 2023-07.
  - **Jumpsuits/rompers have 0 active designs.** Floral Print Jumpsuits made $848 in 19 orders since 2023-07, and six jumpsuit/romper titles made ~$13k in 2019–21 (`LIVE_VERIFIED`).
  - The #1 seller since 2023-07, **Pastel Tie-Dye Ruffle Dresses** ($1,172, 21 orders), is ARCHIVED.
- **Garment types:**
  - Sleeveless tiered, ruffle or smocked dresses: 8, including 3 pastel tie-dye.
  - Floral long-sleeve maxi dresses with pockets: 6. They work for Easter as well as spring.
  - Mother-daughter jumpsuits/rompers in floral print and rainbow stripe: 6.
- **Roles:** Mom (S–XL, 2XL where offered) and Girl (2–12). A baby-girl romper is an optional role for jumpsuits.
- **Season:** Easter (Mar 28) → Mother's Day (May 9) 2027. Live by Jan 15, 2027; add prints by Mar 1.
- **N = 20.**
- **Suppliers:**
  1. 廉江市城北依曼: Mommy & Me dresses. 20 orders, 2.6/3.9 d, **0 of 45 returned**.
  2. 深圳市斯蒂琪: off-shoulder dress sets. 2.6/3.2 d.
  3. 湖州托马拓: family sets, 0 of 22 returned. `decisions.json` holds a 2026-04-25 search-card Reject for it; re-judge it on the detail page.
  4. The original factories of the archived Floral Print Jumpsuits and Floral LS Maxi. Read them from the products' private vendor field (`LIVE_READBACK_REQUIRED`; never copy the URL into packets), then run the full gate.
  - Avoid: 深圳丹维尔 (the tie-dye dress supplier; p90 44.5 d), 广州千程, 广州布莱士 and 东莞虎门昱宝贝.
- **Price:**

  | Garment | Mom / Girl | Pair weight | Unit-cost ceiling (42% / 50%) |
  |---|---|---|---|
  | Sundress / midi | $34.99 / $31.99 | 400 g | ≤ $8.57 / ≤ $11.25 |
  | Maxi | $39.99 / $34.99 | 550 g | ≤ $9.38 / ≤ $12.38 |
  | Jumpsuit | $34.99 / $29.99 | 450 g | ≤ $7.86 / ≤ $10.46 |

## 4. Collection gaps (demand categories under 20 active items)

Counts are `LIVE_VERIFIED 2026-09-27`. Category boundaries are `ESTIMATE`.

| Priority | Demand category | Active now | Drafts | Demand evidence | Action |
|---:|---|---:|---:|---|---|
| 1 | Christmas family pajamas | **1** | 11 | 11% of net since 2023-07, 3.5 items/order. Archived Christmas lifetime $8.4k plus $11.4k on deleted products (`REPO_KNOWN`, 2026-09-24 ranking) | Brief 1 |
| 2 | Jumpsuits / rompers | **0** | 0 | Floral Print Jumpsuits $848 (#3 since 2023-07); ~$13k in 2019–21 | Brief 3 |
| 3 | Nightgowns | **1** | 0 | $1.27k since 2023-07; $5.2k in 2019–21 | Brief 2 |
| 4 | Hawaiian family sets (`matching-hawaiian-outfits`) | 9 | 0 | Dad & Son Hawaiian $841; Hawaiian shirt + floral dress $481; light-blue Hawaiian beach dress + shirt $434 | Round 5 (summer; live by Mar 1) |
| 5 | Dad-son swim trunks | 11 | 0 | $1.1k since 2023-07; 3 of 11 have 0 sales | Round 6 |
| 6 | Fall knits (non-Christmas) | ~12 | 0 | $3.3k since 2023-07 (Knitted Sweater Fall $627; Cable Knit $335) | Round 7 (广州玺召) |
| 7 | Christmas sweaters | 13 | 0 | New on 2026-09-25; 1 historical order | Hold at 13; judge after the season |
| 8 | Halloween family pajamas | 5 | 1 | New in 2026; no history | Hold until Halloween 2027 |
| 9 | Valentine's (`valentines-day-matching-outfits-1`) | 3 | 0 | The Bestie Heart tee made $7.4k in 2019–21, but its 2024 heart-tee successors have 0 sales | Round 4 (live by Dec 5) |
| 10 | Easter / maternity / couples / siblings | 0 / 0 / 2 / 0 | 0 | Easter and Maternity were deferred "until sourcing" by the owner (shop-by-occasion claim) | Easter is folded into Brief 3; the rest are test lanes |

Above 20 (no count gap, but see §6 for margin and prune):
- Mother-daughter dresses: ~40.
- Family dress + shirt sets: ~46.
- Mom-kid swim: 35.
- Daddy & Me shirts: 23.
- Graphic tees/tops: ~46.
- Everyday M&M pajamas: ~21.

## 5. Winners to expand with more prints from the same proven supplier

Finding: **all 10 of the top 10 best-sellers since 2023-07 are ARCHIVED**; the first ACTIVE product is the Sunflower Maxi at #25 (`LIVE_VERIFIED`). #9 is the archived Floral Smocked Midi ($479, 10 orders; supplier `LIVE_READBACK_REQUIRED`), which Brief 3's smocked designs replace. Proposed `OWNER_DECISION`: re-list a proven winner as-is when its original offer still sells, it passes today's supplier gate, and its pair price passes §8. A proven design beats a new one. This is separate from the current-year gate, which governs new designs.

| Rank | Winner (net since 2023-07, orders) | Status | Proven supplier (`REPO_KNOWN` study) | Expansion |
|---:|---|---|---|---|
| 1 | Pastel Tie-Dye Ruffle Dresses ($1,172, 21) | ARCHIVED | Tie-dye dress = 深圳丹维尔, which is **Avoid** (p90 44.5 d) | Re-source 3 tie-dye ruffle designs from 廉江依曼 or 斯蒂琪 (Brief 3) |
| 2 | Holiday Safari Animal Pajamas ($933, 9 orders / 37 units) | ARCHIVED | 广州衣林 (preferred for pajamas) | +2–4 whimsical Christmas prints (Brief 1) |
| 3 | Floral Print Jumpsuits ($848, 19) | ARCHIVED | Not in the study (`LIVE_READBACK_REQUIRED`) | +6 jumpsuits (Brief 3); re-list the original if it passes |
| 4 | Dad & Son Hawaiian Shirts ($841, 18) | ARCHIVED | Not named (`LIVE_READBACK_REQUIRED`) | Round 5: Hawaiian family sets from one vendor line |
| 5 | Floral Long-Sleeve Maxi ($766, 12; all-time #1) | ARCHIVED | Not named (`LIVE_READBACK_REQUIRED`) | +6 (Brief 3); re-list the original if it passes |
| 6 | Winter Fleece Nightgown ($658, 9) | ARCHIVED | 温州陈东弟, **Avoid** | Re-source (Brief 2) |
| 7 | Knitted Sweater, Fall ($627, 13) | ARCHIVED | 广州玺召 (preferred for fall knits; 26 orders) | +6–8 knits, heart designs first for Valentine's (rounds 4 and 7) |
| 8 | Hawaiian Shirt + Floral Dress set ($481, 4 orders / 19 units) | ARCHIVED | Family dress + shirt sets = 绍兴涟可 (47 orders, top revenue; slow p90 10.3 d) | Round 5: +10 vacation family sets from 涟可 or 湖州托马拓. One vendor line per family set cuts multi-vendor domestic freight. |
| 9 | Christmas Elf Pajamas ($468, 3 orders / 21 items) | ARCHIVED | 广州佐雅 | Brief 1 |
| 10 | Christmas Crew Pajamas ($355, 3 orders / 15 items; rank #17) | ARCHIVED | 东莞必橙 | Brief 1 |

These active winners stay live, and each gets more prints from the same line in its season:
- Sunflower Maxi ($292, 6 orders).
- Skyfade Set ($289, 5).
- One-Shoulder Swim ($236, 5).
- Cream Chiffon Maxi ($249, 4).
- Tropical Palm Floral Set ($212, 3).
- Two-Piece Swim with Skirt ($175, 5).
- Color-Block One-Piece Swim ($145, **8 orders**).
- Green Tropical Leaf Trunks ($173, 4).

Also keep the `elegant-matching-family-outfits-light-blue-halter-dresses-…` set. It has 0 sales but **8 add-to-carts from 93 landing sessions**, the best ATC rate in the catalog. Check its checkout path or price rather than prune it.

## 6. Products to prune (archive, never delete; each batch needs an owner-approved packet)

`LIVE_VERIFIED`: 50 ACTIVE products created before 2026-03 have **0 sales since 2023-07**. They have gone through at least one or two full seasons.

| Priority | Batch | Count | Evidence | When |
|---:|---|---:|---|---|
| 1 | Non-heart graphic family tee sets at $19.99: remix-encore, need-more drink, battery, plug-lightbulb, cartoon sun-cloud, love-grows, happy-flower, beautiful-rainbow | 8 | 0 sales since they were created in 2024-10/11. 74–132 landing sessions each in 90 days, **0 add-to-cart**. $19.99 passes the pair rule only if cost ≤ $4.90. | Now |
| 2 | Father-baby tee/onesie sets at $19.99: big-trouble, ctrl-c-ctrl-v, top-dad, daddy-me heartfelt, beer-monster, striped-tie, bestie-heart | 7 | 0 sales since 2024-10 | Now |
| 3 | Mom-kid swimsuits and dad-son trunks from 2022 and 2024-02 with 0 sales in 3 summers (11 swimsuits, 3 trunks: red/green tropical-paradise, cow print, flamingo-foliage) | 14 | 0 sales; off-season, so archiving now costs no revenue | Now, before the summer 2027 swim round replaces them |
| 4 | Summer 2024 dresses/sets with 0 sales in 2 summers: smocked vibrant sundresses, watercolor maxi, vibrant printed maxi, beige chiffon, yellow beach set, palm-tree beach set, tropical leaf beach set, rainbow overalls set | 8 | 0 sales; ≤2 ATC each | Now (off-season) |
| 5 | Heart/love tee sets: heart-brushstroke, love-balloon, love-lettering, I-love, eternal-love | 5 | 0 sales, but Valentine's-relevant | Hold through Feb 14, 2027; archive if still 0 ATC |
| 6 | 2024 knits with 0 sales: striped heart cardigans, color-block, star knit dress, striped fleece hoodies, 3 heart cable knits | 7 | In season now | Hold through Dec 31, 2026; archive in Jan if still 0 ATC |
| 7 | Red Panda, Meow Star Garden and Welsh Dinosaur M&M pajamas | 3 | 63–70% pair landed; need +60–115% price (`REPO_KNOWN`). The owner declined archiving "for now". | After the Brief 2 replacements go live (`OWNER_DECISION`) |
| 8 | Any active item still sourced from an Avoid supplier (陈东弟, 昱宝贝, 千程, 布莱士, 丹维尔, 兴城 swim cluster) | ? | Product-to-supplier mapping is not in the repo (`LIVE_READBACK_REQUIRED` via BuckyDrop or the private vendor field) | After the readback |
| — | IP check (not a prune): `cute-matching-mom-and-daughter-cartoon-pajama-set-…` | 1 | "Cartoon" title; 134 sessions, 0 ATC | Review the print for licensed characters |

Batches 1–4 archive now: **37 products**. Batches 5–7 are conditional: 15 more.
- No active product matched licensed-IP terms. The keyword scan's only hits were false positives ("sunflower", sewing "stitch").
- Leave the 73 products added in Mar–Jul 2026 that have no sales yet. Judge them 30 days after their next in-season traffic (workflow §9).

## 7. Target designs per category to support $1M/yr

Model (`ESTIMATE`; shares blend 2019–21 peak mix, 2023–26 mix and seasonality):
- $1M ≈ 10,000–15,000 orders at a $67–100 AOV (profit study).
- At the peak (~$94k/yr over 2019–21), the best design earned about $3.6k/yr.
- $1M across ~470 designs averages **~$2.1k per design per year**. That needs roughly 5× the peak per-design productivity.
- So **traffic engines (Google, email, Meta), not design count alone, decide $1M.** Design count is necessary but not sufficient.

| Category | Share of $1M | Assumed $/design/yr | Target active designs | Active now (+drafts) | Net change |
|---|---:|---:|---:|---:|---:|
| Mother-daughter dresses (maxi, tie-dye, smocked, sundress) | 22% ($220k) | $2.2k | 100 | ~40 | +60 |
| Family dress + shirt / Hawaiian vacation sets | 15% ($150k) | $2.5k | 60 | ~46 | +14, plus 8 replacements |
| Christmas family pajamas | 14% ($140k) | $3.1k | 45 | 1 (+11) | +33 (24 this season, 45 by Christmas 2027) |
| Swim (mom-kid + dad-son) | 12% ($120k) | $2.0k | 60 | 46 | +14, plus 14 replacements |
| Winter/everyday M&M pajamas + nightgowns | 8% ($80k) | $2.0k | 40 | ~22 | +18, plus 3 replacements |
| Knits (fall + Christmas sweaters) | 8% ($80k) | $2.3k | 35 | ~25 | +10 |
| Jumpsuits / rompers | 6% ($60k) | $2.0k | 30 | 0 | +30 |
| Daddy & Me shirts | 6% ($60k) | $2.0k | 30 | 23 | +7 |
| Graphic tees / tops (occasion, Valentine's) | 5% ($50k) | $1.25k | 40 | ~46 | −20 pruned, +14 better-priced |
| Halloween family pajamas | 2% ($20k) | $2.0k | 10 | 5 (+1) | +4 (2027) |
| Tests: couples, maternity, siblings | 2% ($20k) | $1.0k | 20 | 2 | +18 only if tests earn it |
| **Total** | 100% | ~$2.1k | **~470** | 257 active | **~+215 net, ~+260 gross after prunes** |

That is about 20–35 weekly rounds of 5–15 designs, with seasonal pushes front-loaded to §2.
- **Falsifier / reallocation rule:** after 60 days of in-season qualified traffic, if a category's median design earns < 25% of its assumed $/design pro rata, stop adding to it and move its slots to the best-performing category.

## 8. Pricing rule per category (2-piece order must pass the 50% landed rule)

**Rule.** Let c = unit cost per piece (product + China domestic + BuckyDrop fees, USD), P = average piece price of the pair, and F = pair freight = (¥45.4 + ¥8.2 × pair grams / 100) / 7.11.
- **Floor (owner's 50% rule):** P ≥ max(4.2 × c, 2c + F). This is the formula used in the 2026-09-27 reprice. It is equivalent to c ≤ (P − F)/2; at 457 g, F ≈ $11.50.
- **Target at 650% ROAS (≤ 42% landed):** P ≥ (2c + F) / 0.84.
- **Role split:** adult = P + $1.50, child = P − $1.50 (the $35.99/$32.99 precedent). Round to .99. Compare-at follows the workflow.
- **The 4.2× shortcut is unsafe when c < F/2.2.** It underprices cheap items there. When 4.2× gives a price above the category ceiling below, **reject the offer** rather than price up (the red-panda lesson).

Pair weights are `ESTIMATE`; replace them with the offer's SKU weight.

| Category | Pair g | F | Price adult / child (avg P) | Max unit cost @50% | Max @42% | 4.2× unsafe below c = | Notes |
|---|---:|---:|---|---:|---:|---:|---|
| Christmas family PJ, 2-piece | 560 | $12.84 | 35.99 / 32.99 (34.49) | $10.83 | $8.07 | $5.84 | smr ¥37/¥27 → ~32% landed ✓ |
| Fleece onesie PJ | 800 | $15.61 | 36.99 / 33.99 (35.49) | $9.94 | $7.10 | $7.10 | Heavy; watch the weight |
| M&M winter/everyday PJ | 520 | $12.38 | 34.99 / 31.99 (33.49) | $10.56 | $7.88 | $5.63 | Cap $39.99 |
| Fleece/flannel nightgown | 650 | $13.88 | 36.99 / 32.99 (34.99) | $10.56 | $7.76 | $6.31 | |
| Mother-daughter sundress/midi | 400 | $11.00 | 34.99 / 31.99 (33.49) | $11.25 | $8.57 | $5.00 | Typical cost $7.9 → 40% ✓ |
| Long-sleeve maxi dress | 550 | $12.73 | 39.99 / 34.99 (37.49) | $12.38 | $9.38 | $5.79 | |
| Jumpsuit / romper | 450 | $11.58 | 34.99 / 29.99 (32.49) | $10.46 | $7.86 | $5.26 | |
| Family dress + shirt set | 420 | $11.23 | dress 32.99 / shirt 29.99 (31.49) | $10.13 | $7.61 | $5.10 | Orders average 2.8 items, which is better than the pair case |
| Daddy & Me Hawaiian shirt | 380 | $10.77 | 27.99 / 24.99 (26.49) | $7.86 | $5.74 | $4.89 | **All 23 active sit at $19.99, which passes only if c ≤ $4.61** (`LIVE_READBACK_REQUIRED` cost). Raise or bundle with a dress. |
| Mom-kid swimsuit | 300 | $9.85 | 26.99 / 22.99 (24.99) | $7.57 | $5.57 | $4.48 | The $19.99 floor passes 50% only at c ≤ $5.07 and 42% only at c ≤ $3.47. The abstract-print swim (c $4.92) runs 49%. |
| Dad-son swim trunks | 280 | $9.61 | 24.99 / 21.99 (23.49) | $6.94 | $5.06 | $4.37 | Active items are $21.99 |
| Knit sweater / cardigan | 750 | $15.04 | 39.99 / 34.99 (37.49) | $11.23 | $8.23 | $6.83 | Heaviest; the shortcut often fails |
| Graphic tee | 330 | $10.19 | 24.99 / 21.99 (23.49) | $6.65 | $4.77 | $4.63 | $19.99 tees fail 42% at any realistic cost |

Single-item orders are 11.5% of orders at 65% landed (`REPO_KNOWN`). No price rule fixes those. That is the pending free-shipping-threshold vs. price-floor `OWNER_DECISION` from the profit study.

## 9. Evidence index (all read 2026-09-27)

- Active catalog: Admin GraphQL `products(query:"status:active")` = 257. Types: Family Matching 52, Swimwear 44, Matching Family Sets 40, Matching Family Pajamas 27 and others. By creation year: 2022 = 5, 2024 = 93, 2026 = 159. `LIVE_VERIFIED`.
- Drafts: 15. That is 11 Christmas family pajamas, 1 Halloween onesie, and 3 from 2026-09-04 (a set, sweatshirts, dresses). `LIVE_VERIFIED`.
- Sales by product since 2023-07-01 (ShopifyQL, 252 products resolved via `nodes`). The top 10 are all ARCHIVED; the first active item is the Sunflower Maxi at #25 ($292). `LIVE_VERIFIED`.
- Sales by product 2019–2021 (ShopifyQL top 80) and monthly net sales 2017–2026. `LIVE_VERIFIED`.
- 90-day landing-page sessions and add-to-cart (ShopifyQL). Diagnostic only, because crawler traffic is present. `LIVE_VERIFIED`.
- Supplier history, freight fit, reprice plan and costs: `2026-09-27-buckydrop-profit-study/README.md`, `reprice_plan.json`. `REPO_KNOWN`.
- Supplier tiers: `ops/sourcing/TRUSTED-SUPPLIERS.md`. Rejections: `ops/sourcing/state/decisions.json` (36 items; 25 of them from the family-matching Christmas search). `REPO_KNOWN`.
- Christmas line state and prices: `2026-09-26-christmas-pajama-line/README.md`. Archived Christmas ranking: `2026-09-24-christmas-relaunch-ranking/README.md`. `REPO_KNOWN`.

## 10. Single next action

Hand Brief 1 to the round-1 claim holder and have it live by Oct 15. It is the only time-boxed, highest-margin lane, and it has 1 live design against a demand that averages 3.5 items per order. The owner's parallel action is to activate the 11 Christmas drafts as their images land.
