# Italian Search original launch scope

Confidence: H. **Historical May 19 execution only; not current settings or authority.** Campaign `23866684201` / `DLM_IT_SEARCH_NATIVE_IT_EXACT_015_TEST_20260519`, customer 3990976848.

The 13:48:51 UTC run was validate-only and left zero campaigns. The 13:58:36 UTC live run reports 87 operations; its before-state has zero campaigns and after-state one ENABLED/ELIGIBLE campaign. All four before/after readbacks have zero query errors.

| Ad group / ID | Original EXACT keywords | Keyword and RSA final URL |
|---|---|---|
| Family Matching / `196333557283` | `abiti coordinati famiglia` | [https://www.dresslikemommy.com/it/collections/matching-outfits?country=IT](https://www.dresslikemommy.com/it/collections/matching-outfits?country=IT) |
| Mommy & Me Dresses / `196333557323` | `abiti mamma e figlia`; `abiti mamma figlia` | [https://www.dresslikemommy.com/it/collections/mommy-and-me?country=IT](https://www.dresslikemommy.com/it/collections/mommy-and-me?country=IT) |
| Pajamas / `196333557483` | `pigiami coordinati`; `pigiami famiglia`; `pigiami famiglia coordinati`; `pigiami mamma e figlia`; `pigiami mamma figlia` | [https://www.dresslikemommy.com/it/collections/pajamas?country=IT](https://www.dresslikemommy.com/it/collections/pajamas?country=IT) |
| Swimwear / `196333557523` | `costumi famiglia` | [https://www.dresslikemommy.com/it/collections/family-swimsuits?country=IT](https://www.dresslikemommy.com/it/collections/family-swimsuits?country=IT) |

**Checks:** all 9 positive rows match the launch CSV exactly by group, keyword, match type and URL. The 4 RSAs agree with their groups’ keyword URLs. Historical negatives match CSV/API: 47 campaign PHRASE and 19 ad-group PHRASE (Family Matching 5, Mommy & Me Dresses 5, Pajamas 5, Swimwear 4). Terms remain in the original negative CSV; these are not current exclusions.

The landing CSV records four HTTP 200 responses with unchanged Italian final URLs; it has no per-row timestamp and is not a fresh availability check.

**Source inventory:** [structured extraction](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/italian_search_original_scope.json) contains full artifact paths, SHA256 hashes for all 9 source files, nine criterion IDs and exact JSON pointers. Sources are the four before/after JSONs, both execution reports, launch-keyword CSV, negative CSV and localized-landing CSV in the May 19 packet. The authoritative scope is the [13:58 after-state](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-19-it-it-native-search-exact-015-approval/google_ads_api_it_it_after_readback_20260519T135836Z.json); earlier validate-only data is not launch proof.

No current keyword/query performance, present settings, authority, attribution or profit is established. Parent-supplied campaign aggregates are not assigned to these keywords. Only the two owned files changed; no browser/API/network or external action occurred. Continuation: root joins its current rows to this historical inventory before any market, bid or pause decision.
