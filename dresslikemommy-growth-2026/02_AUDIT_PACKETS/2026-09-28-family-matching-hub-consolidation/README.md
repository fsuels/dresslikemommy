# Family matching outfits hub consolidation (2026-09-28)

Owner brief: the family-matching collection gets ~23.7k Google impressions at ~position 58; nightgown and Hawaiian searches sit at positions 6–12; translated pages work; the "Grinch" trademark must stay out of ads and titles.

## Evidence (Search Console, sc-domain:dresslikemommy.com, read 2026-09-28, LIVE_VERIFIED)

- 3 months, English collection pages: `/collections/matching-outfits` 7,697 impr / 5 clicks / pos 47.1; `/collections/new-women-outfits` 247 / 1 / 27.2; `popular-family-matching` 46.
- 12 months: `/collections/matching-outfits` 12,048 impr, pos 48.7. `/collections/family-matching` does not exist; it 301s to matching-outfits (UrlRedirect 344233574497), with ~30 other legacy URLs.
- Top queries on matching-outfits (3 mo): matching family outfits 763 (pos 42), family matching outfits 542 (52), matching outfits for family 332 (40), matching outfits 273, family outfits 253, family matching dresses 240, coordinating family outfits 222.
- Localized new-women-outfits all locales: 2,045 impr / 51 clicks (sv 15.4, it 8.0, da 10.2). Localized matching-outfits ~725 impr / 25 clicks.
- Hawaiian (3 mo): Google ranks `/collections/daddy-me-shirts` pos 17.6 overall; "father son matching hawaiian shirts" 40 impr pos 14.3, "father and son matching hawaiian shirts" 44 pos 12.7, "hawaiian themed outfits" 65 pos 11.6 (product page).
- Nightgown (3 mo): ~110 impr total, pos 15–28, ranked page `/collections/pajamas` pos 22.5. Only 1 ACTIVE nightgown product (grapevine-mommy-and-me-pajamas); 7 archived.
- Grinch: 6 products, all ARCHIVED; 0 ACTIVE/DRAFT; 0 page impressions for Grinch URLs in 3 months. A peer session removed Grinch product blocks from 3 blog posts (its own anchor).

Decision: Google already chose matching-outfits for the head term, so it becomes the hub instead of new-women-outfits (reverses anchor `2026-09-24-family-matching-outfits-seo-target`, whose GSC premise was the Apr-2026 export).

## Changes (all LIVE_VERIFIED 2026-09-28)

| Surface | Change | Rollback |
|---|---|---|
| Collection 377555589 `matching-outfits` rules | + `TAG EQUALS Family Matching` (disjunctive). Live products 79 → 182; 0 new-women-outfits products missing | Remove that rule (before: `matching_outfits_before.json`) |
| same, SEO + description | seo.title/description set; description: daddy-and-me→daddy-me link, pajamas→family-pajamas link, sizes FAQ softened to "most styles", swimwear sentence aligned to refund policy (was "final sale") | `matching_outfits_description_before.html`, `matching_outfits_before.json` |
| Collection 355558883425 `daddy-me-shirts` SEO | "Father and Son Matching Hawaiian Shirts \| Dress Like Mommy" + description | `daddy_me_shirts_seo_before.json` |
| Menu `main-menu` item 479417106529 | FAMILY MATCHING → collection 377555589 (was 33122287713); 8 children unchanged | `main_menu_before.json` |
| Theme commit 7aafd97 (15 files) | hub links → matching-outfits; canonical popular-family-matching + EN new-women-outfits → matching-outfits; EN H1/title/meta/intro for matching-outfits and daddy-me-shirts; EN matching-outfits renders its admin buyer guide + FAQ schema | `git revert 7aafd97`, then `sync_live_theme_from_main.py --apply` |

Readback: theme check 298 files 0 offenses; `sync_live_theme_from_main.py` 0/366 drift after `--apply` (GitHub sync did not apply within 90 s); live HTML: titles, meta, canonicals as intended; H1 "Family Matching Outfits", 182 products, FAQPage JSON-LD; `/sv/collections/new-women-outfits` and `/de/collections/matching-outfits` unchanged; product breadcrumb "Family Matching Outfits → /collections/matching-outfits"; mobile 375 px no horizontal scroll.

## Measure (external clock)

GSC on/after 2026-10-26 (28 days): query "family matching outfits" + "matching family outfits" by page. Success: one URL (matching-outfits) carries them and average position improves from ~45–52 toward ≤20. Kill: English family-matching impressions drop >30% with no seasonal cause → revert 7aafd97's canonical lines first. Same check for daddy-me-shirts Hawaiian queries (success: top 10).

## Routed, not done here

- Nightgowns: the quick win needs product, not copy (1 active). Merch queue: source 2026 mommy-and-me nightgowns (owner rules: 2026 releases, BuckyDrop fast vendors); then a `mommy-and-me-nightgowns` collection and repoint the 5 peer redirects (406752165985…297057).
- Translated pages: localized dresses/swimsuits rank 5–10 in no/da/fi/cs/ro/he; extend native collection copy to the hub + daddy-me-shirts in those locales (translation lane).
