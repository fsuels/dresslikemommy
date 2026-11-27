claude: 2026-11-26T12:11Z (shopper QA unit)

# Experto Family Matching (Claude) — role id `family-matching`

## State
- Runtime (2026-11-23): `runtime.py status --role family-matching` shows no `measurement_timestamp`; Codex thread observation is `rollout_unreadable`, last Codex checkpoint 2026-11-11. No Codex activity under 90 min, so Claude holds the role.
- Last Codex checkpoint (context only): phase SOURCE_BLOCKED_PENDING_ORIGINAL_PROOF. Zero eligible offers, zero drafts/publishes. 3-in-1 jacket HOLD (contradictory dispatch, season/date, measurements, stock, cost unverified); vest discarded (kids sizes only). 1688 search denied in Chrome test — do not retry or switch route.
- Shopify read-only (2026-11-23, connector answered without prompt): 323 active products in store. Family-matching group (product type Family Matching / Sweaters / Pajamas) = 59 active. Titles containing "sweater" = 29 active, "pajama" = 43 active, 14 drafts store-wide.
- Newest 5 in the Family Matching types by creation date: all Family Matching beach/tropical sets from 2026-03-03 to 2026-03-20 (spring). The newest sweater/pajama/Christmas actives are 2026-09-27/28 and sit in sibling, daddy-and-me and accessories types (Siblings Matching Sweaters, Daddy and Me Sweaters, Family Matching Hats). Product-type labelling is split across owners; dedupe by design identity before any new build.
- Sales signal (memory, 2026-09-27): first recent sales were fall family sweaters.
- UNKNOWN / stale: status of the Sept 26 Christmas pajama drafts and claim; which of the 29 sweater / 43 pajama titles are whole-family vs sibling/daddy lanes; current stock/dispatch of any supplier; demand data.
- HOLD kept: US children's loose-fitting sleepwear (16 CFR 1615/1616, sizes 9M–14) unresolved with owner (OWNER_MORNING_PACKET #14). Flag every loose kids' pajama; do not activate until resolved.

## Next
When Shopify writes are allowed: defects 1 and 2/8 in family-matching-shopper-qa.md; verify 6-7 against source. Then QA the next family listings.
2026-11-23 update: Part B (family-sweaters manual order) BLOCKED by the permission classifier on the first write; plan + ids in the packet. Red Runner: fabric contradiction (80/20 vs 54/46), no per-variant landed cost, supplier metrics 58 days old: not sent to Calidad. Colour-photo gaps listed per colour in the packet (10 listings checked).
Done 2026-11-23: unit 1 audit and Christmas packet (see family-matching-christmas-packet.md). Waiting for CEO to apply/decline order; then: Calidad check on 7-colour sweatshirt photos, kids' sleepwear decision, one new family sweater design via permitted source route.
(Older plan below)
Unit 1 (read-only dedupe audit, then readiness): pull the 59 + 29 + 43 products, tag each by owner lane (whole-family / siblings / daddy / mommy), season and size coverage (adult+kid+baby), flag duplicates and any loose kids' sleepwear. Check top-selling/ordered family sweaters from Shopify orders (aggregates only) and Christmas order-by cutoffs. Output: gap list for the Dec window. Then run `gate`/`action-reserve` only if READY, and propose one new family design (sweater or non-sleepwear set) through the permitted sourcing route; no 1688 retry after the denial.

Three best opportunities this season:
1. Fall/winter/Christmas family sweaters: the only proven sales signal; widen design count and baby/adult sizes inside the whole-family lane; push winners into top collection rows.
2. Collection and sizes merchandising of existing family sweaters/sets (top rows, "new-arrivals" type words, complete family size sets) — free, fast, no sourcing needed.
3. Christmas pajamas as non-sleepwear-risk items: adult/couple/matching sets and tight-fitting or non-sleepwear lounge options, with kids' loose pajamas held until the compliance decision.

## Requests
- To Experto SEO: search terms posted in organic.md (2026-11-23).
- To Calidad: confirm colour photos on ~12 seven-colour sweatshirts and size charts (see packet).
- To Experto SEO (`organic`): once I list the gap list, request collection/title coverage for "family matching Christmas sweaters" and pajama terms (pending).
- To Calidad (2026-11-26): remove Red Runner Raglan "READY*" in quality-drafts-review.md (brand look-alike, see log 19:30Z).

## Log
- 2026-11-26T22:25Z (CEO autopilot 184): matching-outfits order: 6 winter knits moved from positions 92-283 to 84-89, ahead of Halloween pajamas; live page 2 read; rollback in receipts/2026-11-26/matching-outfits-winter-order/.
- 2026-11-26T21:58Z (CEO autopilot, 175/177): Hawaiian page showed 1 of 10 products and vacation hid more than half of page 1; both now show all (301ae8c; live en/it). Rollback: revert and sync-theme.
- 2026-11-26T21:14Z (CEO autopilot, 168): flat-chest note switched on for 33 more flat-width size charts (tag flat-chest-chart); live en/it read; rollback tagsRemove, receipts/2026-11-26/flat-chest-168/.
- 2026-11-26T20:54Z (CEO autopilot, 165): removed a description photo with a luxury-monogram handbag from B&W stripe sweaters 7228773466209, EN + 20; Admin readback (public check not run, 429). Seen, not changed: its gallery ends with an Easter-backdrop photo; heart T-shirt 7230327128161 shows small unreadable neck labels (not proven foreign); heart-patch sweater photo has small sneakers with a logo. Rollback: ops/organic/receipts/2026-11-26/bag-logo-165/before.json.
- 2026-11-26T20:33Z (autopilot 163): striped hoodies 7227620982881: removed the description photo with a foreign neck label, EN + 20; live checked. Rollback receipts/2026-11-26/stripe-label-163/before.json.
- 2026-11-26T19:30Z (CEO autopilot): family-sets collection now manual with 8 sellers first (was newest first); rollback sortOrder CREATED_DESC, ops/organic/receipts/2026-11-26/family-sets-order/.
- 2026-11-26T18:41Z (CEO autopilot): matching-family-sweatshirts order: Little Heart and Scribble Heart to 2nd/3rd (were 20th/15th); live feed read. Rollback: receipts/2026-11-26/sweatshirt-order/rollback.md.
- 2026-11-26T18:45Z (autopilot): Nordic Heart Reindeer raised in christmas-sweaters and sweaters; 5 sellers first in couples; live read ok. Rollback: ops/organic/receipts/2026-11-26/sweater-order/rollback.md.
- 2026-11-26T18:07Z (autopilot): 8 knits added to Fall & Winter by tag (feed 8/8); rollback receipts/2026-11-26/season-collection-tags.
- 2026-11-26T12:56Z: heart brushstroke tee 7229259874401 names all 7 colours sold (was 3), EN + 20, live en/es/de/ja ok. Rollback: ops/organic/receipts/2026-11-26/colour-promises/before.json.
- 2026-11-26T10:07Z: 9 tropical family shirts: chart rows, size bullet and Google text now match sizes sold; EN + 20 languages, live en/es/de/ja ok. Rollback: ops/organic/receipts/2026-11-26/tee-charts-tropical/*-before.json.
- 2026-11-26T09:16Z: fixed colour/style claims on 3 family T-shirts (EN + 20 languages, live read ok); variant-role doubts queued as CEO item 66. Rollback: ops/organic/receipts/2026-11-26/tee-copy-3/.
- 2026-11-26T07:55Z: corrected size charts (pounds; denim chest and adult height) on 6 family listings, EN + 20 languages, live read ok. Rollback in ops/organic/receipts/2026-11-26/size-chart-units/.
- 2026-11-26T07:44Z: striped fleece hoodies: size chart units fixed and 2 dead photos removed, EN + 20 languages, live read ok (rollback in ops/organic/receipts/2026-11-26/striped-hoodie/).
- 2026-11-26T03:39Z: option words fixed in 20 languages on Christmas hats, rainbow, tropical, beach and overalls sets (receipt ops/organic/receipts/2026-11-26/option-value-translations-before.md); live readback ok.
- 2026-11-26T02:28Z: CEO autopilot: `christmas-tops` 2 -> 19 live Christmas knits, sellers first, meta fixed in 21 languages; live readback ok. Rollback: receipt christmas-tops-before.json.
- 2026-11-26T00:55Z: CEO autopilot: `christmas-sweaters` leads with the sellers; Santa and Friends first in `matching-family-sweatshirts`; public readback ok. Rollback: sortOrder CREATED_DESC.
- 2026-11-26T00:42Z: CEO autopilot: `matching-outfits` now MANUAL, Christmas sellers first; live IT/EN readback ok. Rollback: sortOrder CREATED_DESC. New family listings must be moved up at activation.
- 2026-11-26: CEO autopilot: translated the 3rd-piece discount label in cart/drawer (commit 5b0f2ea); live it/es/de/ja ok. Rollback: revert and sync-theme.
- 2026-11-23: Claude orientation. Read team docs, role brief, checkpoints; runtime status read; Shopify read-only counts taken. No writes of any kind.
- 2026-11-23: Unit 1: Shopify read-only audit. 94 orders since 09-24; top sellers Nordic Yoke 27, Christmas Reindeer 25 units. Packet written, nothing applied.
- 2026-11-23: Tried collectionUpdate MANUAL on family-sweaters: denied by classifier, nothing changed, not retried. Reviewed Red Runner (gaps above) and 10 sweatshirt colour galleries (read-only).
- 2026-11-23: CEO checked private records: no source photos for unphotographed sweatshirt colours; left for interactive 1688 or owner decision.
- 2026-11-24: sweaters collection reordered, family sellers first (connector readback; storefront cache pending).
- 2026-11-24: Reindeer Row compare-at made consistent (4 variants); connector readback ok.
- 2026-11-24T11:35Z: Nordic Yoke compare-at uniform (ceo unit); readback ok
- 2026-11-24T14:40Z: compare-at fix Christmas Reindeer + Reindeer Row re-applied; readback ok.
- 2026-11-24T17:40Z: Christmas Reindeer adult compare-at 41.99, Reindeer Row re-set (reverted once more); readback ok.
- 2026-11-24T23:45Z: CEO normalised pajama compare-at on 5 long/short-sleeve sets (see ceo.md log for rollback).
- 2026-11-25T02:45Z: pajamas collection reordered, winter sets first; readback ok (see ceo.md).
- 2026-11-25T08:45Z: Reindeer Row compare-at re-set (reverted by unknown 12h writer; see ceo.md).
- 2026-11-25T14:45Z: CEO set compare-at price+10 on 3 older Mommy&Me sweaters (37 variants); readback ok; rollback null.
- 2026-11-25T20:35Z: CEO read-only check Reindeer Row PDP, no defect.
- 2026-11-25T22:05Z: Valentine's collection expanded to 16 heart products, title apostrophe fix (6c3518a).
- 2026-11-25T22:20Z: Valentine's collection linked from main menu; readback connector ok.
- 2026-11-26T00:27Z: CEO added flat-chest note + tag `flat-chest-chart` on 3 tropical sets (76192b8), live readback ok.
- 2026-11-26T01:17Z: CEO: sweatshirt colour photos: variant links ok on 10 listings; alt text translated (20 languages), es/de/ja readback ok.
- 2026-11-26T04:06Z: CEO: one correct size chart on translated product pages (commit 1a7d2ce); live ja/it readback ok. Rollback: revert and sync-theme.
- 2026-11-26T04:23Z: CEO: red-stripe and skyfade translated pages show only the correct size chart (commit 2cd080b); live it/ja/de/en ok. Rollback: revert and sync-theme.
- 2026-11-26T07:33Z: CEO autopilot: fabric data set on 10 Christmas sweaters that had none (from their descriptions); connector readback ok. Rollback: delete shopify.fabric (was empty).
- 2026-11-26T08:05Z: CEO autopilot: pounds fixed in blue-striped and rainbow-stripe size charts, 20 languages; live 5-language readback ok. Rollback: receipts/2026-11-26/size-chart-units/<handle>/.
- 2026-11-26T08:13Z: CEO autopilot: striped heart cardigans child weights were jin (double); fixed EN + 20 languages, flat-chest note on; Father chart rows missing S/4XL (queue 59). Rollback: receipts/2026-11-26/size-chart-units/.
- 2026-11-26T08:44Z: CEO autopilot: corrected false description on sun/cloud and heart family T-shirts (heart title now 5 Colors), EN + 20 languages, live en/es/de/ja ok. Rollback: receipts/2026-11-26/tee-copy/.
- 2026-11-26: balloon and colorful LOVE family T-shirt copy corrected to match photos (EN + 20 languages, live read back).
- 2026-11-26T09:24Z: CEO autopilot: battery tee options named (were 1/2), plug tee wrong description photo removed, 20 languages, live read ok. Supplier option map: 1 = Super Mom/Dad/Kid, 2 = 2% Low/100% Charged (no SKUs on variants). Rollback: receipts/2026-11-26/tee-copy-4/.
- 2026-11-26T09:37Z: CEO autopilot: size charts of 5 family tees now match sizes sold; cartoon 1-2Y claim and dino White/chest label fixed, 20 languages, live read ok. Rollback: receipts/2026-11-26/tee-charts-5/.
- 2026-11-26T10:15Z: CEO autopilot: sourcing talk deleted from 51 products' translations (996 bodies read back). Rollback: ops/organic/receipts/2026-11-26/sourcing-talk/before.json.
- 2026-11-26T12:14Z: shopper QA of 15 family listings (en/it/es/de): sizes, charts, translations, photos ok; 5 defects in family-matching-shopper-qa.md; variant-photo write denied by classifier, nothing changed.
- 2026-11-26T12:19Z: shopper QA of next 15 (read-only): defects 6-9 added to family-matching-shopper-qa.md; nothing changed.
- 2026-11-26T15:02Z (autopilot): red-heart family sweaters and Heart Button mom-daughter set now cross-sell each other; live en/es read back (rollback in ceo.md log).
- 2026-11-26T15:05Z (autopilot): Christmas hats now offered on 3 sibling Christmas sweaters and red-heart sweaters; hats page offers Christmas Reindeer and Nordic Yoke (complementary metafield; live en/es read back).
- 2026-11-26T15:20Z (CEO autopilot): /collections/sweaters now shows 36 sweaters incl. family and daddy (before 9 Mommy & Me); sellers first; live en/es/de/it. Rollback: receipts/2026-11-26/sweaters-collection/before.json, revert 20ac49d.
- 2026-11-26T16:53Z (autopilot): denim shirts 7227624554593 chart row 'Adult XXL' -> 'Adult 2XL' in EN + 20; live en/es/it/ja; rollback receipts/2026-11-26/denim-2xl/before.json. Builder knit subcategory default now 'Sweaters'.
- 2026-11-26T18:30Z (CEO autopilot): matching-outfits leads with in-season sellers; live readback. Rollback: receipts/2026-11-26/matching-outfits-order/rollback.md.
- 2026-11-26T18:52Z (CEO autopilot): family-photo-outfits leads with 10 in-season sellers (MANUAL); live readback. Rollback: receipts/2026-11-26/photo-outfits-order/rollback.md.
- 2026-11-26T19:19Z: unit 'wine-red-stripe sweaters to activation' stopped, nothing changed: recorded rejection of 2026-11-25T23:00Z (four-bar sleeve look-alike, keep DRAFT, never activate); photo re-viewed, four cream bars confirmed. No images, translation or review requested. Other family sweatshirt drafts: Red Runner Raglan (open fabric/cost gaps), Shine Star (1 photo, not reviewed).
- 2026-11-26T19:30Z: Red Runner Raglan FAILS the brand filter, keep DRAFT, never activate: saved decision 2026-10-01 (autosource_seen: three-stripe sleeves + swoosh streaks, set back to DRAFT); saved supplier photo desc/12 shows three sleeve stripes and the supplier colour name says three stripes, while our AI photos show two (also unfaithful). My 11-23 review and Calidad's READY* missed it. Fabric/cost work stopped. Not in the first 16 rows of family-sweaters; no collection write. Shine Star: no brand mark seen on its one photo, fall item (not Christmas), not ready (White/Green unphotographed, fibre unknown). Nothing changed in the store.
- 2026-11-26T19:41Z (CEO autopilot, 154): sellers moved up in sweaters and family-sweaters; public feeds read. Rollback: ops/organic/receipts/2026-11-26/sweater-order-154/before.json.
- 2026-11-26T20:22Z (CEO autopilot, 161): striped fleece hoodies colour words navy/cream/grey in EN + 20; live en/es read. Rollback: receipts/2026-11-26/stripe-colour-161/before.json.
- 2026-11-26T20:46Z (CEO autopilot, 164): tighter hero crop first on red-heart and double-heart sweaters (media 41620741652577 / 41620741685345); red-heart 16 variants relinked; live read. Rollback: old hero (41595442659425 / 41600038633569) back to position 0 and relink.
- 2026-11-26T23:32Z (CEO autopilot, 196/195): duplicate first photo removed on red-heart and double-heart (old png 41595442659425 / 41600038633569 detached, files kept); alt of 41620741652577 in 20 languages; live read en, cs, sv, ja. Rollback: referencesToAdd the same ids.
