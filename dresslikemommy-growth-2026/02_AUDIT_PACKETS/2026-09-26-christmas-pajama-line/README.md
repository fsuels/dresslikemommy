# Christmas pajama line — sourcing packet (2026-09-26)

Owner request (chat, 2026-09-26): "Update the store for the season. Christmas pajamas are the gap… Listing 15–25 now still leaves time to ship before the holidays."

Continues anchor `2026-09-24-holiday-line-sourcing-captcha-stop`. The owner chose on 2026-09-24 to source a new line rather than revive the 41 archived Christmas pajamas. This packet does not change that decision.

## 1. Verified store state (read-only Admin GraphQL and storefront `products.json`, 2026-09-26 ~15:25 EDT)

| Item | Finding |
|---|---|
| Active Christmas pajamas | 1: `snowflake-reindeer-family-matching-onesie-pajamas`. `christmas-pajamas` shows 1 live product; 41 others are ARCHIVED. |
| Active Christmas sweaters | 13, listed 2026-09-25 through the canonical listing workflow |
| Active Halloween pajamas | 6, all tagged `Halloween Pajamas`. No Halloween collection exists. |
| Hero "Shop Halloween Pajamas" | Links `/collections/family-pajamas` (28 counted, 22 live). Its first card is the Christmas onesie; cards 2–7 are Halloween. |
| Hero "Shop Family Matching Outfits" | Links `/collections/new-women-outfits`. That is the deliberate SEO exact-anchor target from `2026-09-24-family-matching-outfits-seo-target`. Its first 11 live cards are the new Christmas sweaters (CREATED_DESC); summer items follow. |
| Homepage "New Pajama Drop" card | `ladybug-dots-mommy-and-me-pajamas`, short-sleeve |
| Christmas delivery cutoff | Dec 8, 2026 for Christmas Eve, using the store's 12–16 day window (UX ten-fix lane H) |

## 2. Ownership of the other three symptoms (not this lane)

- Halloween button: the UX ten-fix claim, lane H. `2026-09-26-ux-ten-fixes/lanes/holiday/INTEGRATION.md` has an exact packet. It creates smart collection `halloween-family-pajamas` (rule `TAG = Halloween`, BEST_SELLING) and repoints `hero_banner_main.button_link` and `slide_halloween_arches.link`. It needs owner approval.
- `new-women-outfits` ordering: the UX ten-fix lane D sort-order packet recommends keeping CREATED_DESC through Q4, because it surfaces the new holiday products first (verified above).
- Ladybug card: the Storefront visual polish claim, lane L1. The peer replaced it locally with the Snowflake Reindeer onesie card, linked to `family-pajamas`. The release awaits owner approval of that session's preview.

## 3. Sourcing method

- Helper Chrome on CDP 9333 via the Opportunity Scout dashboard (`127.0.0.1:8766`). Read-only: no login, message, purchase, or CAPTCHA bypass.
- Exact searches, 1 results page each: `圣诞亲子睡衣 欧美 跨境` and `圣诞节 全家装 睡衣`. Run `ops/sourcing/2026-09-26-152533-family-matching-us-1688-auto` returned 24 cards (21 already seen). The search-card scorer marked all 24 Reject, mostly for fields that exist only on the detail page (tenure, size chart, dropship). It also applies a "freshness" heuristic that penalizes offers listed before 2025. The trust gates are not weakened. Each candidate is re-judged on detail-page evidence using `ops/scripts/1688_sourcing_detail_enrich.py`, which keeps the ≥5-year supplier-tenure gate, the IP-term gate and the dropship proof.
- Size charts and design lists come from each offer's description images and SKU selector. They are captured read-only into `ops/sourcing/vendor-images/<offer>/desc/`.

## 4. Detail-check results (read-only, 2026-09-26 15:25–17:20 EDT, no CAPTCHA)

Search-run offers checked with `1688_sourcing_detail_enrich.py`: 15 in total (1 alone, then a batch of 14).
- Passed the hard gates (tenure ≥5 years, dropship, no IP term): 广州市赛美人制衣 (smr factory, 12 years, dispatch 7 days) `989011278121`, 广州娴公主 (7 years, same smr brand, likely a reseller) `988913643690`, and 惠州市天穗服饰 (6 years, dispatch **15 days**) `667146727364`, `677435372992`, `678475715893`, `677475732005`.
- Rejected: 广州市艾莉雅 (4 years) `1078193697768`, `1068770076374`, `986921510839`, `965796001454`; `989524551402` (1 year, 卡通); `1063210400525` (2 years); `1073358036890` (1 year); `850703215675` and `973951080562` (卡通 IP-term gate); `671664841334` (MOQ 4); `987956332824` (fewer than 10 sold, weak).

The smr factory store (`shop1413825186771`) has these Christmas family categories: 2026 (6), 2025 (76) and a best-seller group (217). Its data response (read over CDP) gave 36 offers: all 6 from 2026 and the first 30 from 2025. The category's paging did not respond.
- Visual screen removed 12 by offer ID: Grinch (`1085715644746`, `1085723536346`, `1085720836538`, `1073499141984`, `988334981445`, `955761017426`, `1020697049487`, `989779334689`, `964789486768`), Stitch/Disney (`1073500189946`), a Rudolph-style red-nose design at ¥10 (`973468959401`), and polyester `944723477140`. Also set aside: short-sleeve `1083372114596` and `965886973423`, and dark-photo `1079361574035`.
- Kept 22 long-sleeve, whole-family designs. Each was captured with `capture_desc.py`: the gallery, the shadow-DOM description images, the SKU list and the page text.

Evidence:
- `shortlist.json` and `shortlist_sheet.jpg` (numbered #1–#22) in this folder.
- Per offer: `ops/sourcing/vendor-images/<offer>/desc/manifest.json` and its images.
- Search run: `ops/sourcing/2026-09-26-152533-family-matching-us-1688-auto`.
- Detail checks: `ops/sourcing/detail-enrichment/<offer>/`.

## 5. Shortlist facts (all 22 from 广州市赛美人制衣, brand smr)

- Supplier: 12 years on 1688, dropship (代发) yes, MOQ 1, 4,000+ dropship distributors, 48-hour pickup rate 100%, return rate 69%, service score 4.0, fulfilment 100%.
- Vendor cost per piece set: Dad/Mom ¥37 (¥35–38), Children ¥27 (¥27–28), Baby ¥25 (¥25–26).
- Dispatch: "Ships in 7 days" on every page that shows it.
- Fabric: 95% cotton on 19 offers. #22 `937463864110` is CVC at 35% cotton. #11 and #17 do not state a percentage.
- Sizes:
  - 2026 offers (24 SKUs): Dad S–3XL, Mom S–XL, Children 2–14, Baby 3–18M.
  - 2025 offers (26 SKUs): the same, plus Mom 2XL–3XL.
  - #3 `989011278121`: Dad and Mom S–4XL, Baby up to 24M.
- Size chart: only #21 `1073505941343` publishes one (`factory_size_chart_from_1073505941343.jpg`).
  - It has Kid 80(2T)–160(14T), Men S–3XL and Women S–3XL (top length, bust, sleeve, pants length, waist, hip), and Baby 60(3–6M)–75(12–18M) (top only).
  - Its rows map one-to-one to the SKU labels.
  - The Baby 18–24M row is cut off in the image.
  - Using this chart for the other 21 designs is an inference (same factory, same base garment). It needs owner confirmation or a supplier answer before any listing uses it. This follows the precedent that the owner reuses one attached chart across offers.
- Weak point: the "已售900+" sold label repeats identically on five new Sept-2026 offers. It is probably not per-offer demand, so it was not used for ranking.
- Photo notes: #18's lifestyle photo shows a baseball-team cap, so use its flat-lay photos. #21 is a cartoon reindeer with a red nose; confirm it is not Rudolph-licensed. The images come from the supplier. As with every listing, publication relies on the supplier's dropship image permission.

## 6. Economics and timing

- Price precedent: live two-piece family pajamas are Child 32.99 / Adult 35.99 (Boo Stripe, Trick or Treat). The onesie is 33.99 / 36.99.
- Proposed prices (owner decides): Adult 35.99 and Child/Baby 32.99. Compare-at follows the workflow's `round_up(x1.15, .99)`: 41.99 / 37.99. Cost is set to 50% of price by rule.
- Vendor cost ≈ USD 5.20 adult and 3.80 child. International shipping is not included and not verified here.
- The Christmas Eve order-by cutoff is Dec 8, based on the 12–16 day window. That window does not visibly include supplier dispatch (7 days here, compared with 15 at 天穗). The owner should confirm the window already covers processing, which is why the smr factory is preferred.

## 7. Blockers and next steps

1. **BLOCKED: Admin API 401** (`PROB-2026-09-26-ADMIN-API-TOKEN-401`), starting about 16:40 EDT. It is probably the effect of the owner's same-day Shopify app removal and automation shutdown. Until the owner restores an Admin API token or chooses a manual route (Shopify admin or CSV import), the listing runners cannot create drafts, and their localization closeout cannot run.
2. Owner picks the designs (15–25; #1–#20 recommended, with #21 and #22 optional), confirms prices, and confirms the size chart for all designs (or asks the supplier via Wangwang, which the owner does).
3. Canonical listing workflow (`ops/prompts/START-HERE.md`): one `LISTING REQUEST` per design, with `LISTING_MODE: Family Matching`, `DESIGNS_TO_LIST: auto` (#3 and #19 carry 2 colorways, so they become one product with a `Color` option), and the factory chart. Drafts only. Each runner needs its localization closeout. That is about 20 runs, so split them across sessions with one writer per product handle.
4. Owner reviews the drafts, sets inventory, and publishes. Then the `christmas-season-collection` gate turns the homepage section and the menu "Christmas" item on automatically from Oct 15, because `christmas-pajamas` will have products. The Sept-24 redirect rollback (74 redirects back to `christmas-pajamas`) becomes relevant then.

## 8. 2026 draft listings (owner request 2026-09-26: one draft per 2026 design, one vendor image each)

Scope rule: only offers first listed on 1688 in 2026, from the 12-year smr factory. The whole store was read through its own data API (234 Christmas family offers; 44 created in 2026).
Excluded from the 44, with reasons:
- IP: 7 Grinch, 1 Stitch/Disney. Brand fit: 1 HAIL SANTA skull design. 1 blank custom-print template.
- Not orderable for this buyer account ('Upgrade➜Buy', price hidden): 8 offers, including the dabbing-Santa pair.
- Duplicate item code: 1 (08911 listed twice).
- No size chart and a different collared button-up cut: 1.

Result: 24 Shopify DRAFTs, created by the canonical runners `ops/scripts/create-<code>-<handle>.sh`. They are generated from `tools/specs/<handle>.json` plus `tools/runner_engine.py` via `tools/generate_runner.py`.
- Every runner passed preflight, the variant-model validator, the taxonomy guard and final verification: DRAFT, publishedAt null, no channel publication, exactly 1 vendor image, SKUs, price/compare-at/cost parity, 10-column size table, tags and metafields.
- Size charts: 22 offers publish the factory chart in their own description (the factory line; the 4XL line adds Men 4XL / Women 4XL). 2 (Snowy Village Stripes, Lights Out Reindeer) publish none and reuse the 4XL-line chart; this is disclosed in their listing.md.
- Fabric follows the offer's material-composition field. 'Imitation cotton' is listed as polyester, not cotton.
- Prices: 35.99 adult and 32.99 child (the Boo Stripe / Trick or Treat precedent). Baby romper SKUs are excluded, because baby is not a Family Matching role.
- Translations: Google's free endpoint is blocked (PROB-2026-09-25-...-GOOGLE-429). 4,420 validated model translations (20 locales) were written by 4 subagents, checked by `tools/seed_cache.py`, and registered directly on each draft by `tools/register_direct.py`. The shared cache was not written while peer pollers ran, per PROB-...-CONCURRENT-LOST-UPDATE.
- Canonical closeout: `tools/closeout_all.sh` waits for peer pollers to go idle, seeds the cache, then runs each runner with `finalize_shopify_listing_localization.py`. Results are in `tools/run_logs/`.
- Image sheet: `drafts_2026_sheet.jpg`. Inventory: `tools/run_logs/drafts_inventory.json`.

| # | Handle | Draft ID | Offer | Listed | Sizes | Fabric | Chart |
|---|---|---|---|---|---:|---|---|
| 1 | beary-cozy-family-matching-pajamas | 9473583022177 | 1081615050631 | 2026-09-10 | 21 | polyester | factory |
| 2 | candy-tree-christmas-family-matching-pajamas | 9473583054945 | 1080736515512 | 2026-09-10 | 21 | polyester | factory |
| 3 | classic-red-plaid-family-matching-pajamas | 9473583087713 | 1032775642583 | 2026-03-19 | 21 | polyester | factory |
| 4 | cookie-baking-crew-family-matching-pajamas | 9473583218785 | 1033288412830 | 2026-03-16 | 21 | polyester | factory |
| 5 | cozy-reindeer-family-matching-pajamas | 9473583775841 | 1073505941343 | 2026-08-08 | 21 | polyester | factory |
| 6 | evergreen-fair-isle-family-matching-pajamas | 9473584529505 | 1061758229843 | 2026-06-25 | 21 | polyester | factory |
| 7 | green-merry-christmas-family-matching-pajamas | 9473584857185 | 1079361574035 | 2026-09-02 | 21 | cotton | factory |
| 8 | here-for-the-cookies-family-matching-pajamas | 9473584889953 | 1081815371723 | 2026-09-14 | 21 | polyester | factory |
| 9 | jolly-crew-family-matching-pajamas | 9473584922721 | 1080356577298 | 2026-09-02 | 22 | polyblend | line4xl |
| 10 | jolly-santa-family-matching-pajamas | 9473585512545 | 1082663865858 | 2026-09-10 | 21 | polyester | factory |
| 11 | joyful-merry-blessed-family-matching-pajamas | 9473586266209 | 1037079642878 | 2026-03-28 | 21 | polyester | factory |
| 12 | let-it-snow-family-matching-pajamas | 9473586561121 | 1081367024239 | 2026-09-02 | 22 | polyblend | line4xl |
| 13 | lights-out-reindeer-family-matching-pajamas | 9473586626657 | 1076610891971 | 2026-08-26 | 22 | polyblend | line4xl |
| 14 | merry-xmas-lights-family-matching-pajamas | 9473577746529 | 1082696802900 | 2026-09-14 | 21 | polyester | factory |
| 15 | plaid-reindeer-family-matching-pajamas | 9473586659425 | 1080353625335 | 2026-09-02 | 22 | polyblend | line4xl |
| 16 | plaid-tree-trio-family-matching-pajamas | 9473586692193 | 1078423171906 | 2026-09-02 | 22 | polyblend | line4xl |
| 17 | reindeer-forest-family-matching-pajamas | 9473587314785 | 1030872819566 | 2026-03-16 | 21 | polyester | factory |
| 18 | santas-crew-family-matching-pajamas | 9473588035681 | 1082668769741 | 2026-09-10 | 21 | polyester | factory |
| 19 | snowy-reindeer-family-matching-pajamas | 9473588396129 | 1083372114596 | 2026-09-16 | 21 | polyester | factory |
| 20 | snowy-village-stripes-family-matching-pajamas | 9473588494433 | 1034014187785 | 2026-03-23 | 22 | polyblend | line4xl |
| 21 | team-santa-family-matching-pajamas | 9473588527201 | 1081603250990 | 2026-09-10 | 21 | cvc | factory |
| 22 | vintage-tree-truck-family-matching-pajamas | 9473588559969 | 1082489147641 | 2026-09-16 | 21 | polyester | factory |
| 23 | we-are-family-evergreen-family-matching-pajamas | 9473588592737 | 1080381493063 | 2026-09-02 | 22 | polyblend | line4xl |
| 24 | we-are-family-red-family-matching-pajamas | 9473588658273 | 1081388156651 | 2026-09-02 | 21 | polyester | factory |

Closeout result (2026-09-26 19:45–20:17 EDT): peers went idle at 19:45. 2,520 seeded cache values were filled (1,900 already present). Then all 24 runners exited 0 with `localization-closeout.json` `status=passed`.

Independent readback at 20:18 EDT (fresh Admin API query, separate from the runners): 24/24 DRAFT, publishedAt null, no sales-channel publication, exactly 1 image, 21 or 22 variants, and unit cost = 50% of price on every variant.
