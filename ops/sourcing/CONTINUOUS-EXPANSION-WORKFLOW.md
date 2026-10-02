# Continuous Product Expansion Workflow

Owner goal (2026-09-26): Claude is the merchandise expert and is responsible for finding the best products to sell at a good margin. keep expanding the selection so the store always sells the best possible products, sourced only from the most reliable suppliers: years of reputation, stock on hand, fast shipping, good quality, no problems. Claude owns this loop and brings the owner finished DRAFT listings to approve.

This file is the recurring loop. It sits on top of the existing tools:

- Sourcing dashboard and detail gate: `ops/sourcing/AGENT-SOURCING-WORKFLOW.md`
- Listing contract: `ops/prompts/START-HERE.md` (master prompt and 1688 template)
- Photoshoot prompt: `ops/prompts/dlm-6-image-photoshoot.md`
- Supplier scorecard, updated every round: `ops/sourcing/TRUSTED-SUPPLIERS.md`
- Reference tooling from the 2026 Christmas run: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools/`. It contains the spec builder, runner engine and generator, translation seeding and direct registration, image jobs, attach and inventory scripts.

## Owner product rules (read first, every session; they apply to Claude, Codex and every subagent)

These are standing owner instructions. Details are in the numbered sections below. Changing any of them requires the owner's explicit yes.

1. **Keep expanding, every round:** new designs AND new vendors, within the owner's focus categories: **Mommy & Me, family matching, maternity, couples, Father & Me (Daddy & Me), and siblings** (owner 2026-09-27). **No pet products until the owner says so** (owner 2026-09-27: "Do not do pets yet"). Use `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-27-million-plan/lanes/CATEGORY_OPPORTUNITIES.md` for timing and ideas, but skip its pet items.
2. **Vendor discovery every round** (owner 2026-09-27: "Keep looking for new better vendors!"):
   - test Tier B suppliers;
   - find new Guangdong factories for weak categories;
   - use Taobao/Tmall via BuckyDrop only under the same gates;
   - **BuckyDrop sourcing (owner 2026-10-01, chose "Source via BuckyDrop" to avoid 1688 CAPTCHAs; test on one run first):** BuckyDrop may replace 1688 searching and offer browsing, but **vendor quality must still be checked** (owner 2026-10-01: "You must be able to check the quality of the vendors"). Every vendor passes the full supplier gate in rule 3 (years, 48h pickup, fulfillment, service, returns, disputes, orders) before a product is built; when BuckyDrop does not show those stats, read the store's 1688 credit page (one page per store, verdict cached and applied to all its offers);
   - record every reading in `TRUSTED-SUPPLIERS.md`;
   - new vendors stay Tier B until an on-time order proves them.
3. **Supplier gate (§3):** ≥5 years on 1688 — or **3–4 years only with strict stats** (owner 2026-09-28: "3 years is ok with good reputation and good delivery times?" → chose the strict option): 48h pickup ≥97%, fulfillment ≥97%, quality returns ≤1%, disputes ≈0%, service ≥4.0 and 500+ orders in the last 30 days, plus the 24/48h promise; ≥97% fulfillment, **ships in 24h, 48h at most, ALWAYS** (owner 2026-09-28: "I need shipments faster 24 max 48 hours." / "ALWAYS"): the offer's dispatch promise must be 24h or 48h and the store's 48h pickup rate ≥95%; a 3-, 7- or 15-day promise fails, even under a supplier exception. Dropship MOQ 1, service ≥4.0, Guangdong preferred. **Exceptions (e.g. <5 years) only with the owner's explicit yes.** **Young stores (owner 2026-10-01, chose "Yes, strict stats"):** a store with 0–2 years (or unreadable years) passes only with 48h pickup ≥97%, fulfillment ≥97%, 1,000+ orders in the last 30 days, service ≥4.0, quality returns ≤1% and disputes ≈0, plus the 24/48h promise. It stays Tier B until a real order ships on time. Reason: maternity and couples stores on 1688 are mostly 2026-founded, and none older qualified.
4. **Current-year designs only (§4):**
   - BOTH the 1688 listing date AND the release-year attribute must be the current year.
   - **Fresh and in season** (owner 2026-09-28: "always make sure the listings we are adding are fresh! year 2026 for the correct season"):
     - The release attribute (上市年份季节 / "Year and season of release") must name the current year AND a season that fits the selling window.
     - Fall, winter and holiday lines need 2026 Autumn/Fall/Winter (秋季/冬季/秋冬). Spring/summer lines need 2026 Spring/Summer.
     - A "Spring 2026" tag on a Christmas or winter item fails. So does a year-only attribute, unless the listing date and the design clearly place it in the season.
     - Record the exact attribute text in the spec evidence.
     - **Missing season tag (owner 2026-10-01, chose "Missing season tag OK"):** an offer with NO release attribute at all passes the season check when its 1688 listing date is on or after 2026-08-01. An attribute that names another year or season (Spring/Summer 2026, 2025, 2027) still fails. The 24/48h dispatch, supplier gate, design and price rules are unchanged.
   - Never restore archived or old designs as "new". The owner rejected the 5 restored 2025 Christmas winners on 2026-09-27.
   - No licensed characters or look-alikes. Read the real fabric composition.
5. **Pricing (§6):** landed cost ≤50% of price on a single-item order; net ≥35%. The BuckyDrop shortcut is (CNY cost + domestic) / 7.11 × 4.2, with compare-at = price + $10; always run the 50% test. Record the real unit cost.
6. **Listing:**
   - canonical DRAFT with 100 stock per variant;
   - 4 photoshoot images (1, 3, 5, 6) made with the ChatGPT app's Codex on the owner's Pro plan, never the OpenAI API, and reviewed against the vendor photos;
   - the localization closeout must pass.
7. **Activation (Claude may activate after QA)** with `activate_listing.py`. It must read back:
   - all channels;
   - the Markets catalog publications, with `publishedInContext` US/DE/GB/AU/CA true;
   - a storefront 200.
8. **After activation, make it findable:**
   - MANUAL collections append new products at the bottom, so move seasonal winners into the top rows;
   - the product TYPE must contain a word the `new-arrivals` rule matches (Dresses, Family Matching, Tops, Pajamas, Swimsuits, Bottoms, Sweaters, Sets, Swimwear, Outerwear, Skirts).
9. **Never archive seasonal products** the supplier still offers (§9). If you must archive, 301 the URL to the same-intent collection.
10. **Honesty:** this is dropshipping. No stock, warehouse, fast-shipping, review or bestseller claims.
11. **Compliance open item:** the US children's sleepwear rule (16 CFR 1615/1616; kids' sizes 9M–14 must be flame-resistant or tight-fitting) awaits the owner's decision (`OWNER_MORNING_PACKET.md` #14). Flag every new loose-fitting kids' pajama until it is resolved.
12. **Stop conditions:** a 1688/Taobao CAPTCHA or login wall means stop and ask the owner. Never bypass it.
13. **A photo for every colour** (owner 2026-10-01: "make sure when you offer different colors in the listing the images in the listing for each color show!"): every colour a listing offers needs its own reviewed photo of the garment in that colour, attached to that colour's variants, so choosing a colour shows it. Offer only colours you can show this way. Tool: `ops/sourcing/gown_listing.py` (colour photos + variant media links).
14. **Owner-picked maternity photoshoot batch exceptions (2026-10-01, this batch only):** the 21 offers the owner pasted on 2026-10-01 (seed offer 1086097243184) may ship with a 5–10-day dispatch promise, and each page says honestly that it is made to order and when it ships (`custom.made_to_order_days` moves the PDP delivery window). The owner also allowed a Summer/Spring/year-only release tag for these photoshoot gowns and sets, because they are not seasonal clothing. Every other rule applies; the owner kept offer 1020871680362 skipped (service 3.5).
15. **Western maternity photoshoot gowns may be made to order** (owner 2026-10-02, standing): 1688's European/American maternity photoshoot gowns are sewn to order, so for that product type only, a dispatch promise of up to 10 days is allowed. Each listing sets `custom.made_to_order_days` (the PDP shows the later delivery date) and says it is made to order. The 48h pickup and 48h fulfillment stats do not apply to these stores; everything else stays strict: ≥5 years on 1688, service ≥4.0, quality returns ≤1%, disputes ≈0, Fall/Winter 2026 release tag (or none and listed ≥ 2026-08-01), real fabric, landed cost ≤50%, a photo for every colour. Western look only (owner: "the dresses look too asian I need something more european and american!"); skip Asian 影楼 studio sets.

## Cadence

- **Weekly expansion round:** add 5–15 new designs to one or two categories. Continue a round when the owner says "run a product expansion round".
- **Seasonal pushes:** finish listing about 8–10 weeks before each peak, so dispatch plus the store's 12–16 day delivery window still arrives in time.

| Peak | List by |
|---|---|
| Valentine's | early Dec |
| Easter / spring | mid Jan |
| Summer / vacation / swim | Mar |
| Back to school | May |
| Halloween | early Aug |
| Christmas / New Year | early Sep |

## The Loop

### 0. Retrieve (always first)

Read `AGENTS.md`, the latest relevant `ops/AGENT_WORKLOG.md` anchor, `TRUSTED-SUPPLIERS.md`, and `ops/sourcing/state/decisions.json` (never re-research rejected offers). Check `ops/AGENT_COORDINATION.md` for claims, and register one for the round.

### 1. Decide what to add (demand first)

- **What sells:** read Shopify orders and sessions for the last 90 days by category and product (Shopify connector or ShopifyQL). Expand winners: more prints of a best-selling garment type, and the next season of a proven category.
- **Gaps:** collections with few live products (e.g. Christmas pajamas, maternity, couples), categories below about 20 active items, and holiday collections before their season gate opens.
- **Output:** a short brief listing category, garment types, roles, season, and the target number of designs.

### 2. Source supplier-first

Platforms: 1688 is primary. Through BuckyDrop the store can also buy from Taobao, Tmall, Xianyu, JD, Weidian, Vipshop and Dewu; use those only when they beat 1688 on design or quality at a workable margin, under the same gate.


1. Start with **Tier A suppliers** in `TRUSTED-SUPPLIERS.md`. Read their store category lists through the store's own offer-list data (the page's `lib.mtop` request with `catId`, `pageNum` and `count`, read-only). Collect current-year releases.
2. Then search for new suppliers:
   - Search in the logged-in browser pane or the helper Chrome: exact Chinese queries that include the current year, e.g. `2026 圣诞亲子睡衣`. Add city words for Guangdong (`广州`, `东莞`, `深圳`, `惠州`).
   - Prefer Guangdong: orders go to BuckyDrop's Huizhou warehouse.
   - If 1688 shows a CAPTCHA or login wall, stop and ask the owner. Never bypass it.

### 3. Supplier reliability gate (hard; all must pass)

| Check | Pass |
|---|---|
| Years on 1688 (入驻N年) | ≥ 5 (prefer ≥ 8); 3–4 only if 48h pickup ≥97%, fulfillment ≥97%, quality returns ≤1%, disputes ≈0%, service ≥4.0, 500+ orders/30d (owner 2026-09-28) |
| Overall fulfillment (综合履约率) | ≥ 97% |
| Dispatch promise (发货时效) AND 48h pickup rate (48h揽收率) | promise 24h or 48h (never 3/7/15 days) AND pickup ≥ 95% (owner rule 2026-09-28, always) |
| Dropship / one-piece orders (代发, 1件起批) | yes, MOQ 1 |
| Orderable by our account | price visible, no `Upgrade➜Buy` |
| Stock | stock shown for the sizes we list |
| Service score (服务分) | ≥ 4.0 |
| Ship-from | Guangdong preferred; any province only if dispatch is fast. Never known-slow origins such as Xingcheng (兴城) swim vendors. |

Tie-breakers: more dropship distributors (铺货分销商数), higher repeat-buyer rate (回头率), then Guangdong over farther provinces. **If the existing Tier A supplier is the best, stay with it.**

### 4. Design gate (per offer)

- **Current-year design (BOTH required):**
  - The offer's 1688 listing date (上架时间) must be in the current year.
  - Its "Year and season of release" attribute (年份季节) must also be the current year.
  - Suppliers relabel old offers: on 2026-09-27, 12 佐雅 offers tagged "2026" had listing dates from 2021–2025, and the owner rejected them.
  - Never bring back archived or old designs as new listings.
- **No licensed characters or look-alikes:** Grinch (小怪), Disney/Stitch, Rudolph-style, cartoon IP (卡通 in an IP sense). Also no brand-unsafe themes (e.g. skull or "HAIL SANTA").
- **Size chart:** the offer's own chart covers every size we list. If none is published, the same factory line's chart may be reused only with disclosure in `listing.md`, and flagged to the owner.
- **Photos:** clear product photos are available for image references.
- **No duplicates:** not a duplicate of an existing store product or of another offer (same item code).
- **Honest fabric:** read the material-composition field. 仿棉 "imitation cotton" is polyester.

### 5. Rank and choose

Score the passing designs on demand fit, design strength, and supplier score. Take the best N for the round. Record every rejection reason in `decisions.json` and every supplier reading in `TRUSTED-SUPPLIERS.md`.

### 6. Create DRAFT listings (owner defaults)

- Use the canonical runner per design (see `ops/prompts/START-HERE.md`). The generated-runner tooling in the reference `tools/` folder does this in bulk: spec → `ops/scripts/create-<code>-<handle>.sh`.
- **Create as DRAFT, then activate after QA.** The owner granted full store control on 2026-09-27: "activate them … you will have total control of the store". Claude activates each listing once its 4 images pass review, inventory is 100 per size, and the localization closeout has passed. Use `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools/activate_listing.py`, which publishes to all 8 channels, sets ACTIVE, and reads back.
- **Inventory:** available **100 per variant** at `gid://shopify/Location/19326085`.
- **Prices: the owner's 50% rule.**
  - Landed cost must be ≤ 50% of the selling price. Landed cost = product + China domestic shipping + YunExpress freight by weight + about ¥13.50 packing/services, converted at 7.11 CNY/USD.
  - That leaves ≥ 35% net after marketing, refunds and fees.
  - Pick the most competitive price that passes on a **single-item order**. Start from the live category precedent. The BuckyDrop 4.2× formula (multiply cost, compare-at +$10) is a shortcut that can fail on cheap, light items, so always run the 50% test.
  - Shopify "Cost per item" stays 50% of price by the listing-workflow rule.
- **Localization closeout** must pass. If Google translation is blocked, use the validated seeding and direct-registration fallback, and run closeouts only when no peer poller is running.

### 7. Photoshoot images (owner's Pro plan, never the OpenAI API)

- **Selection:** 4 images per listing from the photoshoot prompt: IMAGE 1 Hero, 3 Best Occasion, 5 Product-Only, 6 Alternate Lifestyle. All 9:16, with European models who are different people from the vendor photos, and the same family across the set.
- **How it runs:** the Codex CLI bundled in the ChatGPT app, one session per listing, run in a scratch directory outside the repo:
  `/Applications/ChatGPT.app/Contents/Resources/codex exec --skip-git-repo-check -C <dir> -s workspace-write -i ref1.jpg -i ref2.jpg -i ref3.jpg - < prompt.txt`
  Pass the prompt on stdin; the `-i` option swallows a positional prompt.
- **Review:** check every image against the vendor photos (spelling, print, colors, no invented items). Then attach images 1, 3, 5 and 6 and remove the placeholder vendor image.

### 8. Hand off to the owner

Send one sheet of the new drafts: image, draft link, vendor link, supplier and score. Add a worklog anchor and a packet under `dresslikemommy-growth-2026/02_AUDIT_PACKETS/`.

### 9. Measure and prune (keep only the best)

- **30 days after activation:** sessions, add-to-cart, orders and returns per product. Promote winners by adding more prints from the same supplier line. Flag products with 0 add-to-cart after meaningful traffic.
- **Supplier incidents** downgrade a supplier in `TRUSTED-SUPPLIERS.md`: purchase pending over 3 days, stockouts, late dispatch, quality complaints. Two incidents move it to Watch; a serious or repeated incident moves it to Avoid.
- **After each season:** do NOT archive seasonal products that the supplier still offers. Keep them ACTIVE and published out of season: sort them to the bottom and exclude them from paid ads. Each archive cycle throws away the URL's rankings and reviews; SEO audit 2026-09-27 found 152 of 305 ranking pages gone.
  - Archive (never delete) only when the supplier drops the offer, stock is gone, or the design loses money.
  - Then 301 the URL to the same-intent collection (Christmas → `christmas-pajamas`, swim → `swimsuits`), never to a generic one.

## Start-a-round prompt

```text
Run a product expansion round for Dress Like Mommy: follow ops/sourcing/CONTINUOUS-EXPANSION-WORKFLOW.md end to end.
Category focus: <category or "pick from demand">. Target: <N> new designs.
Use only suppliers that pass the reliability gate, current-year designs only, drafts with 100 stock per size,
4 photoshoot images via the ChatGPT app's Codex (never the API). Do not publish.
```
