# Owner "Ads, keywords and SEO brief" triage (2026-09-27)

Source: an owner-pasted brief dated Sep 26 2026, built from GA4, Search Console via GA4, and Shopify. It is treated as data. Its companion CSVs were not supplied, so `dlm_negative_keywords.csv` here is rebuilt from the brief's term list and checked against the live catalog.

## Already done before this brief (read back 2026-09-27)

| Brief item | State |
|---|---|
| 301 `/products/mother-daughter-matching-beach-swimwear` → `/collections/swimsuits` | Exists (UrlRedirect 394105716833) |
| Grinch product rename | All 6 Grinch products ARCHIVED; none active |
| Microsoft Audience Network | Opt-out no longer offered; 25-site exclusion list applied (anchor `2026-09-27-microsoft-audience-exclusions`) |
| US swimwear in Q4 | US swimsuit ad group paused; CA swimsuit ad group awaits owner decision |
| Abandoned-checkout automation | Active (anchor `2026-09-27-apply-all-recommendations`) |
| Christmas pajama, Hawaiian and dresses collection SEO | Titles and meta already rewritten |
| `/collections/family-matching` | Already redirects to `/collections/matching-outfits` |

## Done in this session (standing authority, LIVE_VERIFIED)

Five archived Mommy & Me nightgown/pajama product URLs returned 404. They were the pages ranking for "mother daughter nightgowns" (pos 6) and "mommy and me nightgowns" (pos 9). Each now 301s to `/collections/pajamas`: kitty-pajamas, matching-nightgowns, vintage-nightwear, retro-pjs, palace-princess-pajamas. Rollback: `urlRedirectDelete` on ids 406752165985, 406752198753, 406752231521, 406752264289, 406752297057.

## Corrections to the brief

- **The checkout-completion drop is at least partly measurement pollution.** On 09-27, 51% of 30-day sessions were US/direct/desktop agent tests: 17 checkout starts and 0 orders (PROB-2026-09-27-AGENT-TEST-TRAFFIC-POLLUTES-ANALYTICS). Re-measure the Jul–Sep checkout rate on clean traffic before treating it as a real leak.
- **The negatives exclude "maternity" for now,** but maternity is an owner category. There are 0 active maternity products today; remove the negative when maternity listings go live.
- **The brief's starting CPC caps ($0.40 / $0.30 / $0.15) are above the owner's $0.20 hard cap** (`lanes/paid.md`). The owner's cap wins unless the owner raises it.
- **PMax 24247604341 was recorded Paused on 09-21.** The brief's "Cross-network" spike on 09-26 needs a live readback first: either it was re-enabled, or that traffic comes from somewhere else.
- **Organic SEO items (family-matching consolidation, nightgown/Hawaiian collections) are owned by the session "Family-matching collection SEO ranking".** Its GSC read: Google ranks `matching-outfits` for the head term.

## Needs owner yes (ad-account writes; nothing done)

1. Upload `dlm_negative_keywords.csv` (32 terms) as one shared negative list on Google Ads 650-997-2886 and Microsoft 477439, attached to all Search and Shopping campaigns. It cuts wasted clicks and costs nothing.
2. Microsoft tracking template: replace `utm_term={searchterm}` with `utm_term={QueryString}`. This makes real search terms visible in GA4 and Shopify.
3. Pause Italy campaign `DLM_IT_SEARCH_NATIVE_IT_EXACT_015_TEST_20260519`: 545 sessions, 1 order.
4. Google Ads: read back PMax/cross-network status. If it is live, pause it or set location to US "Presence" only. Confirm Purchase is the only primary conversion.
5. GA4: add shopifybooster.pro and trafficheap.cc as unwanted referrals (a measurement-only change).
