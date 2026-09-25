# Norwegian Bokmål local payload validation

Result: **PASS_LOCAL_WITH_DOCUMENTED_LIMITATIONS**. This is attachment extraction and local validation, not a Microsoft campaign completion or account readback.

`campaign_payload.json` contains source English/group Norwegian mappings, eight URLs and path pairs, exact ordered positive entries, all RSA fields, every group/campaign negative, tracking source text, extensions and associations. `group_01.json` through `group_08.json` and matching keyword copy files expose the same records per group. `build_payload.py` reproduces the extraction from the supplied paste and records its SHA-256.

| Content | Verified count |
|---|---:|
| Ad groups / RSAs | 8 / 8 |
| Positive keywords | 144: 62 Exact, 82 Phrase |
| Headlines / descriptions | 120 / 32 |
| Campaign negatives | 233: 138 Norwegian Phrase, 84 supplemental English Phrase, 11 provisional Exact |
| Group negatives | 54: 30 Exact, 24 Phrase |
| Sitelinks / group associations | 8 / 32 |
| Callouts / snippets / snippet values | 6 / 8 / 24 |
| Image caption pairs actually supplied | 0 of the referenced 160 |

Per-group positive/negative counts, in attachment order: **17/8, 20/8, 18/9, 17/0, 15/10, 16/13, 18/0, 23/6**. All eight RSAs have exactly 15 headlines and four descriptions. Zero negative entries were dropped: the eight Exact exclusions in family outfits and 13 in mother/daughter outfits retain their explicit recipient-eligibility conditions. All 30 Exact group exclusions have an inferred destination based on another supplied group's positive phrases, including Norwegian ASCII variants. This mapping does not guarantee Microsoft routes traffic there.

The deterministic local check passed all **222 text-length checks**, expected counts, assignment references and routing-recipient matches. Maximum lengths: headline 30, description 90, URL paths 13/8, sitelink title 25, sitelink description lines 34/32, callout 25 and snippet value 24. No within-scope keyword duplicates, cross-group positive duplicate tuples or literal positive/negative conflicts were found. Phrase checks compare normalized contiguous tokens; Exact checks compare normalized whole phrases. No Microsoft semantic, editorial or close-variant behavior was simulated.

Current scope correction and material limits:

- The latest user correction, relayed by the parent, is “in that case you need to do Norwegian with language norsk with instructions I gave you”. The parent resolved current scope as **Norway / Norwegian Bokmål**, so the effective payload is now **DLM | MS | NO | NB | Search | 202609**, location **Norway**. The original request said `NB | NB` and the attachment said `US | NB` / United States; both remain recorded as historical provenance. The source attachment/hash was not changed.
- A **separate new paused source copy** is required, with new campaign ID still **null** pending creation/readback. Campaign `506256099` is confirmed Polish-owned, renamed `PL | PL` and Paused, and is permanently excluded from Norwegian work.
- Eight `candidate_final_url_suffix` values now contain `utm_campaign=dlm_ms_no_nb_search_202609`; original US strings remain under `source_final_url_suffix`. No tracking suffix was applied, and duplicate-free inheritance has **NOT RUN**. The `final_url_suffix` fields remain **null** until the parent checks inherited/automatic tracking.
- Parent current native source readback verified **USD10/day, Maximize Clicks, checked USD0.20 maximum CPC**. The payload records this source monetary baseline for the paused copy; it conveys no activation or spend-increase authority. This delegated lane did not independently access the account.
- The paste references a ZIP, workbook and **160 caption/alt-text pairs** but provides none of those contents or links. All 320 absent fields are **NOT RUN** for validation. Preserve source pictures; no caption or image was invented.
- Parent reports seven groups in the live English source; the eighth mother/daughter outfits group is expressly supplied by the attachment. Native copying and identity reconciliation belong to the parent.
- Supplemental English negatives are intentionally retained as instructed by the parent and attachment. No shared list should be overwritten.
- All URLs use `/no/collections/`. Landing-page claims in the paste are historical; no destination, inventory, pricing, cart, checkout, live tracking inheritance or recipient serving eligibility was checked here. Eleven provisional assortment negatives remain marked as provisional.

Commands run: `python3 .../payload/build_payload.py` (PASS) and an independent JSON readback/count/identity-null check (PASS). Files created only in this owned payload directory; no Git, browser, account, source/peer or canonical-state writes.
