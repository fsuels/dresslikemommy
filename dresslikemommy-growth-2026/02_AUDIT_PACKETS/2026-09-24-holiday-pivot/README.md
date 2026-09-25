# Holiday Pivot — Readiness Packet (2026-09-24)

Status: `PREPARED_LOCAL__RESTORE_APPROVAL_REQUIRED`. Every Shopify figure below was read live and read-only through the Shopify Admin analytics and product APIs on 2026-09-24. No products, feeds or ads were changed, and no money was spent.

## 1. Premise check: the cable-knit sweater page's "72 visitors, 0 add-to-cart"

Product `7241063825505`, `/products/family-matching-cable-knit-sweaters-heart-embroidered-unisex-pullovers`, ACTIVE, USD29.99–34.99, 64 variants.

| Metric (last 30 days) | Sweater page | Real-shopper landing pages on this store |
|---|---|---|
| Sessions / visitors | 72 / 72 | — |
| Bounce rate | 100% | 41–72% |
| Avg session duration | ~0.01 s | 25–197 s |
| Source | 65 direct with no UTM tags, 7 Facebook | mixed |
| Days | Sep 9: 49, Sep 10: 12, Sep 16: 10, Sep 7: 1 | spread out |

The same pattern hit two unrelated product pages on the same days. The cartoon pajama page had 34 sessions on Sep 9, 12 on Sep 10 and 8 on Sep 16. The one-shoulder swimsuit page had 34, 5 and 9. All three pages averaged under 0.2 seconds per session.

Conclusion (`LIVE_VERIFIED` metrics, source is `INFERENCE`): these visits look automated. They could be a crawler, a link-preview fetcher or an audit tool. They are not shoppers who looked at the page and turned it down. **The 0 add-to-carts do not tell us whether the photos, price or sizing are wrong.** Nobody stayed long enough to judge them.

## 2. Holiday demand in this store's own data (Oct 1 – Dec 31, 2025)

- Total USD2,381 gross. Christmas and holiday items were about USD1,870 of that, roughly 79%.
- Holiday sales began in October: about USD727 of holiday products sold in the weeks of Oct 6–20. That matches the owner's read that demand starts in October. The sample is small, at 29 orders.
- Top sellers: Holiday Safari Animal Pajamas (`7230717886561`, 4 orders, USD641), Christmas Elf Pajamas (`7232295043169`, USD355) and **Matching Family Cable Knit Sweaters – Cozy Holiday Outfits (`7234945155169`, 2 orders, USD270)**. That last one is a *different* product from the sweater page in section 1.

## 3. Current catalog gap

- **0 ACTIVE products** match Christmas / Xmas / tag `Christmas` / `Christmas Pajamas` / `Christmas Sweaters`.
- Every holiday product that sold last season is ARCHIVED. Their `updatedAt` timestamps are all 2026-04-30/05-01 UTC. The worklog entry of 2026-05-19 records that the owner archived a group of listings but gives no reason. The likely reason is the season ending (`INFERENCE`).
- The `christmas-sweaters` and `christmas-tops` collections have tag-based rules. They still exist, but on the storefront they show only active products.
- The sweater that *is* active (`7241063825505`) is tagged `Valentine's Day`, not Christmas. Its title has no family, holiday or Christmas wording.

## 4. Proposed restore candidates (needs owner approval before any write)

| Product ID | Handle (short) | 2025 holiday gross |
|---|---|---|
| 7230717886561 | holiday-safari-animal-pajamas | USD640.75 |
| 7232295043169 | christmas-elf-pajama-set | USD354.84 |
| 7234945155169 | matching-family-cable-knit-sweaters-cozy-holiday-outfits | USD269.92 |
| 7232297795681 | christmas-pajama-set-naughty-or-nice (licensed character — see gate G1) | USD119.94 |
| 7234564063329 | christmas-pajamas-joy-love-peace-polar-bear | USD89.08 |
| 7232312770657 | christmas-pajama-set-happy-holidays-snowman | USD65.97 |
| 7232285835361 | christmas-pajama-set-santa-ho-ho-ho | USD42.29 |
| 7234552168545 | christmas-pajamas-christmas-tree | USD42.14 |
| 6677481652321 | christmas-deer-snowflake-pjs | USD38.40 |
| 7231319474273 | let-it-snow-merry-christmas-pajamas | USD28.08 |

The exact write would change each product's status from `ARCHIVED` to `ACTIVE` and republish it only to the channels it had before. That change can be undone by archiving the product again.

Gates before any restore:
- **G1 IP.** The "Naughty or Nice" design uses a licensed character. Leave it out unless the owner confirms the supplier has the rights.
- **G2 Supplier.** This is a dropship store, so for each product we must confirm that the supplier still offers every sold size and color at a known cost. The inventory counts in Shopify are placeholders, not stock; one variant shows 88,054 units.
- **G3 Listing truth.** Re-check price and margin against the current 50% cost sync. Check localized size charts, translations, `item_group_id` and parent image for Pinterest grouping (`check_pinterest_feed_grouping.py --strict`), and that no copy claims stock, reviews or bestseller status.
- **G4 Feed.** The Merchant and Pinterest feeds must pick up the restored products before any paid traffic. Spend authority stays with the `ops/marketing/` command layer.

## 5. Active sweater page (`7241063825505`): observed fixes, none proven to be the cause

1. **Fixed locally, not deployed:** the "Back to Sweaters &amp;amp; Jackets" link showed a literal `&amp;`. The cause: Shopify's `t` filter already escapes the collection title, and the theme escaped it a second time in the `data-back-to-results-label-default` attribute. `assets/global.js` then copies that attribute into `textContent`. The fix uses `escape_once` in `snippets/breadcrumbs.liquid` and `snippets/buy-box-similar-styles.liquid`. This bug appears on every product page reached from a collection with `&` in its name.
2. The title "Cable Knit Sweaters Heart Embroidered Unisex Pullovers | DLM" drops "Family Matching" and has no holiday wording. Proposed title: "Family Matching Cable Knit Heart Sweaters — Holiday Pullovers". Needs owner approval.
3. The tag is `Valentine's Day` with no `Christmas Sweaters`. Adding `Christmas Sweaters` would place the product in the existing `christmas-sweaters` collection. Needs owner approval.
4. The hero image (`family-sweaters-1152x2048-fixed.png`) and one gallery image (`ChatGPT_Image_Mar_23_2026...png`) look AI-generated. Before any ads, confirm they match the colors and knit the supplier actually ships.
5. There are no reviews. Do not add review or bestseller claims.

## 6. Order of work

1. Owner approves the restore list (all 10, or 9 without the licensed design), or edits it.
2. Check each approved product with the supplier (G2), then run the listing checks (G3), then restore.
3. Read back the storefront, collections, feeds and Pinterest grouping.
4. Only then build any paid holiday campaigns under the existing command-layer gates. Real shopper traffic is also needed before judging photos, price or sizing on these pages.

## 7. Two-year ranking of archived Christmas products (follow-up, 2026-09-24)

Read-only. Source: ShopifyQL `sales` grouped by product for 2024-09-01 to 2026-09-24, plus per-season windows (Sep 1 – Jan 31) and a live `nodes` status read. All 27 products below read `ARCHIVED`, archived 2026-04-30/05-01 (the nightgown on 2026-05-19). Store gross for Oct–Dec 2025 was USD2,380.95, or 19.7% of the last four quarters. Oct–Dec 2024 was USD6,066.04.

| # | Product ID | Short name | 2-yr gross | Orders | 2024 season | 2025 season | Note |
|---|---|---|---|---|---|---|---|
| 1 | 7230717886561 | Holiday Safari Animal PJs | 933.29 | 9 | 129.95 | 685.73 | |
| 2 | 7232295043169 | Christmas Elf PJs | 468.48 | 3 | 113.64 | 354.84 | |
| 3 | 7232053936225 | Reindeer Fair Isle PJs (green/white) | 400.82 | 3 | 400.82 | 0 | 2024 only |
| 4 | 7231104712801 | "Christmas Crew" plaid PJs | 354.85 | 3 | 354.85 | 0 | 2024 only |
| 5 | 7234945155169 | Cable Knit Holiday Sweaters | 334.90 | 3 | 0 | 334.90 | |
| 6 | 7230848696417 | Christmas Fair Isle PJs (red/green) | 320.87 | 4 | 320.87 | 0 | 2024 only |
| 7 | 7231319474273 | "Let It Snow" navy PJs | 263.99 | 3 | 235.91 | 28.08 | |
| 8 | 7234564063329 | "Joy Love Peace" polar bear PJs | 130.06 | 2 | 40.98 | 89.08 | |
| 9 | 4814804418657 | Reindeer print + plaid pants PJs | 129.94 | 3 | 109.95 | 0 | |
| 10 | 7234294055009 | "We Are Family" plaid PJs | 124.95 | 2 | 124.95 | 0 | 2024 only |
| 11 | 7232297795681 | "Naughty or Nice" Grinch PJs | 119.94 | 2 | 0 | 119.94 | G1 licensed character |
| 12 | 7234558197857 | Grinch-inspired PJs | 71.93 | 1 | 71.93 | 0 | G1 licensed character |
| 13 | 7234512715873 | Dancing Santa PJs | 65.97 | 1 | 65.97 | 0 | |
| 14 | 7232312770657 | "Happy Holidays" snowman PJs | 65.97 | 1 | 0 | 65.97 | |
| 15 | 7232317030497 | Santa Gnome PJs | 59.97 | 1 | 59.97 | 0 | |
| 16 | 7230645665889 | "Merry Christmas" sweatshirts | 56.97 | 1 | 56.97 | 0 | |
| 17 | 7234248573025 | Reindeer Christmas T-shirts | 49.97 | 1 | 49.97 | 0 | |
| 18 | 7230874157153 | Gnome Fair Isle PJs | 48.98 | 1 | 48.98 | 0 | |
| 19 | 7232285835361 | Santa "Ho Ho Ho" PJs | 42.29 | 2 | 0 | 42.29 | |
| 20 | 7234552168545 | Christmas Tree PJs | 42.14 | 1 | 0 | 42.14 | |
| 21 | 6677481652321 | Nordic Reindeer PJs | 38.40 | 1 | 0 | 38.40 | |
| 22–24 | 7234245984353, 7234911109217, 7230650908769 | Christmas T-shirts (3 designs) | 35.98 each | 1 each | 35.98 each | 0 | |
| 25 | 7230851645537 | Christmas Tree Fair Isle PJs | 26.99 | 1 | — | — | outside both windows |
| 26 | 7231451267169 | "Merry Christmas" tree plaid PJs | 15.99 | 1 | — | — | outside both windows |
| W | 6675120848993 | Mother-daughter fleece nightgown (winter, not Christmas) | 437.89 | 7 | 437.89 | 0 | 2024 only |

The 26 Christmas products total about USD4,276 over two years. The top four (Safari, Elf, Reindeer Fair Isle, Christmas Crew) total USD2,157.44.

Findings that change the plan:
- **There is no supplier record to check.** None of these products has a supplier metafield or a unit cost, and most variants have no SKU. The one exception is the nightgown, which has a cost of USD12.50. There are also no matching records under `ops/sourcing/`. So "check the supplier" means finding each design again on 1688 by image, and 1688 is currently stopped on a CAPTCHA (see the worklog anchor `2026-09-24-holiday-line-sourcing-captcha-stop`). Margin (G3) cannot be confirmed until a cost is found.
- **Five of the top ten sold only in 2024.** They sold USD0 in the 2025 season, when they were probably still active (`INFERENCE`: all were archived in May 2026, but their status in Q4 2025 was not read). The 2024 sales are therefore weaker evidence for this season than the 2025 winners (Safari, Elf, Cable Knit, Joy Love Peace).
- **Timing.** Dropshipping has no stocking lead time. The reason to be live by about October 10 is that this store's holiday sales began in the weeks of Oct 6–20. The 2–3 week delivery time instead sets a truthful Christmas order cutoff in early December, and that date must match the real carrier times.
- **SEO.** A product's URL serves again as soon as the product is active, because Shopify redirects only fire on a 404. That includes the 74 redirects repointed to `/collections/pajamas` today. Rankings lost during about five months of redirects are not guaranteed to return right away.
- **Decision conflict.** Earlier today the owner chose to source a new holiday line rather than revive the archived pajamas (see the anchor `2026-09-24-holiday-line-sourcing-captcha-stop`). Reviving products needs a fresh owner choice. The two paths can run side by side.
