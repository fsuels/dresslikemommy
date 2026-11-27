# Collection copy review 2: nl pl pt-PT sv (2026-11-27)

Same method as `collection-copy-review-2026-11-27.md` (es fr cs de ro): theme locale keys under `sections.collection_seo` only, read against `en.default.json` (origin/main 7197d73), rewritten by hand, no machine translation. Released through `ceo_worktree.py` work copy `colcopy4`, rounds of at most 20 keys per locale file, THEME_LOCK taken for each round (`collection-copy-4 <UTC> colcopy4`), released after each verified round. Work copy finished (removed).

## Scope

- Rendered keys reviewed (97 of 203, same rendered set as the first review): rendered `rich_parts`, `body.*`, `meta_descriptions`, `swimsuits.*` guide and FAQ, `note_eyebrow`, `closer_look_at`. Skipped like the first review: dead keys, `rich_parts.dresses.*`, `rich_parts.family_matching.part_1-3`, the spring/Easter group.
- Added beyond the first review: `display_titles.*` that were broken (they are the collection H1, rendered by `collection-seo-fallback`), and `meta_titles.swimsuits` (browser tab, Calidad V91 finding; pt-PT also `meta_titles.family_swimsuits`).
- Register: nl je (the few `u` forms removed); pl impersonal (warto, można, noun-phrase link texts; old `Kupuj`/`Twój` forms removed); sv du; pt-PT European Portuguese (a condizer, fato de banho, calções de banho, t-shirts, camisolas, bebé, formal imperative, no você).
- Category names from `ops/sourcing/translation_style/category-names.json` (nl Mama en dochter / Papa en kind; pl Mama i córka / Tata i dziecko; sv Mamma & dotter / Pappa & barn). pt-PT has no entry: used Mãe e filha / Pai e filho (pt-BR menu names).
- pl, sv, pt-PT `new_women_outfits.part_1-9` still had the old English structure (wedding-guest link to dresses, links to `daddy_me_shirts_url`, `family_swimsuits_url`), and `family_sets.part_3` used `matching_outfits_url`; all now follow the current English parts and placeholders.

## Keys changed

| locale | keys | notes |
|---|---|---|
| nl | 81 | 63 copy keys + 17 titles + meta_titles.swimsuits; nl new_women_outfits parts 1-6 were already fine and kept |
| pl | 90 | everything rendered except the short already-reviewed body lines; 9 titles |
| sv | 92 | same as pl; 12 titles |
| pt-PT | 139 | almost everything: Brazilian machine text, 9 keys still in English (`meta_descriptions.family_pajamas`, 8 short `body.*` lines); 46 titles; 2 meta titles. `body.christmas_tops_html` was already European Portuguese and kept |

Validation (code, every proposed value): placeholder multiset equal to English, HTML tag sequence equal, class/href attributes equal, digits equal; banned-term scan per locale (mamãe/papai/você/camiseta/combinando/maiô, mama en ik, mama i ja/Kupuj, mamma och jag, stock/warehouse/free shipping words). All pass. Truth: no stock, warehouse, fast-shipping, review, bestseller or free-shipping wording; no dates. "Standard shipping included" in the English pajama meta was dropped in pt-PT (as es/fr/cs/de). "weddings" in `body.daddy_me_shirts_html` dropped (as de/ro). No new pajama mention added: pajamas appear only where the English has them (couples meta, family hub tips link, family_matching meta, pajama collection lines).

## Commits (all on main, each followed by Shopify write-back that kept the values)

| round | commit | nl | pl | pt-PT | sv |
|---|---|---|---|---|---|
| 1 | c3ea1da | 20 | 20 | 20 | 20 |
| 2 | 8755143 | 20 | 20 | 20 | 20 |
| 3 | f138fdc | 20 | 20 | 20 | 20 |
| 4 | 16be3a2 | 20 | 20 | 20 | 20 |
| 5 | 6782e76 | - | 9 | 20 | 11 |
| 6 | b4f425e | - | - | 20 | - |
| 7 | 93dfb1c | 1 | 1 | 19 | 1 |

After every round: `sync-locales --apply`, re-run "locales in sync", 60 s wait, fetch, check origin/main holds every value of all rounds so far: 0 mismatches each time (last check after write-back 435d5c2: nl 81, pl 90, pt-PT 139, sv 92). Round 4 entered 2 s after Experto SEO commit 12cce9d (lock clash noted by the coordinator); read-only checks after round 5 and round 7: `sync-theme` 392 files, 0 differ; `sync-locales` in sync. From round 6 the lock was re-read 5 s after writing.

## Before / after (5 per locale)

### nl

| key | before | after |
|---|---|---|
| `swimsuits.title` | Gecoördineerde badkleding voor moeders, dochters en gezinsabonnementen | Bijpassende badmode voor moeders, dochters en het hele gezin |
| `rich_parts.family_swimsuits.part_5_html` | …Voeg bijpassende koffers toe… | …Voeg bijpassende zwembroeken toe… |
| `rich_parts.couples.part_6_html` | …zijn bijpassende T-shirts de snelste overwinning… werk naar buiten toe… | Zoek je een casual outfit voor elke dag, dan zijn bijpassende T-shirts de snelste keuze… breid uit naar gelang de reis… |
| `display_titles.maternity` | Zwangerschaps- en verpleegstijlen | Zwangerschaps- en voedingskleding |
| `meta_titles.swimsuits` | Overeenkomende familie Badpakken \| Moeder & Dochter | Bijpassende badmode voor het gezin \| Moeder & dochter |

### pl

| key | before | after |
|---|---|---|
| `rich_parts.new_women_outfits.part_5_html` | Kup sukienki dla gości weselnych matki i córki… (old English part, dresses link) | Pasujące stroje na rodzinne wakacje na plażę, rejsy i dni w kurorcie. (family_sets link, current English) |
| `display_titles.sundresses` | Mama i córka Sukienki przeciwsłoneczne | Letnie sukienki dla mamy i córki |
| `rich_parts.couples.part_4_html` | Pary pasują do strojów na podróże, plany weekendowe i zdjęcia towarzyskie… | Pasujące stroje dla par na podróże, weekendowe wyjścia i zdjęcia do mediów społecznościowych… |
| `swimsuits.trunks_title` | Pasuje do Kąpielówki | Pasujące kąpielówki |
| `meta_titles.swimsuits` | Pasująca rodzina Stroje kąpielowe \| Mama i córka | Pasujące stroje kąpielowe dla rodziny \| Mama i córka |

### sv

| key | before | after |
|---|---|---|
| `display_titles.couples_tshirts` | Par som matchar utslagsplatser | Matchande t-shirts för par |
| `rich_parts.couples.part_4_html` | Par som matchar kläder… Gifta hans-och-hennes utseende… | Matchande kläder för par… Looks för honom och henne att ge bort… |
| `swimsuits.faq_answer_2` | …shoppa den matchande familjens baddräkter och trunkkollektionen… simstilarna för mamma och jag. | …titta i kollektionen med matchande familjebaddräkter och kollektionen med badshorts… badkläderna för mamma och dotter. |
| `display_titles.rompers` | Matchande tröja | Matchande playsuits |
| `meta_titles.swimsuits` | Matchande familj Baddräkter \| Mamma & Dotter | Matchande badkläder för familjen \| Mamma & dotter |

### pt-PT

| key | before | after |
|---|---|---|
| `body.valentines_html` | Heart sweaters, sweatshirts and dresses… (English) | Camisolas, sweatshirts e vestidos com corações para fotografias e presentes do Dia dos Namorados… |
| `meta_descriptions.daddy_me` | Compre camisetas, camisetas, camisetas e roupas combinando… | Camisas, t-shirts e roupa a condizer para pai e filho… |
| `swimsuits.trunks_title` | Troncos correspondentes | Calções de banho a condizer |
| `note_eyebrow` | Nota de Coleta | Sobre a coleção |
| `display_titles.mommy_and_me` | Roupas mamãe e eu | Roupa para mãe e filha |

Full proposals (all keys): scratch `prop_<locale>.json` used for release; the applied values are in `locales/{nl,pl,pt-PT,sv}.json` on main.

## Live readback (one request per 7 s, no 429/403)

- nl, pl, sv `/collections/new-women-outfits` and `/collections/swimsuits`: 200. Swimsuits tab titles now "Bijpassende badmode voor het gezin | Moeder & dochter", "Pasujące stroje kąpielowe dla rodziny | Mama i córka", "Matchande badkläder för familjen | Mamma & dotter"; swimsuits guide title, FAQ question 3 and meta description present with the new text. Hub pages show the new link texts (nl "Bekijk outfits voor mama en dochter", pl "Stroje Mama i córka", sv "Se kläder för mamma och dotter") and the new H1 (pl "Pasujące stroje rodzinne").
- pt-PT: BLOCKED for live view. `/pt-pt/...` returns 404 and `/pt/...` serves `lang="pt-BR"`, so the pt-PT locale is not published on the storefront today; its theme file matches live (sync-locales in sync).

## Swimsuits tab title (Calidad V91)

Source: theme key `sections.collection_seo.meta_titles.swimsuits` (picked in `snippets/collection-seo-fallback.liquid` line ~190), not the Admin SEO title. Fixed in round 7 for nl, pl, sv and pt-PT (values above; pt-PT "Fatos de banho a condizer para a família | Mãe e filha").

## Open (not done, for the owner/CEO)

1. pt-BR (`/pt`, the Portuguese that is actually served) still has machine/Brazilian collection copy of the same kind as pt-PT had; same review needed there. The inline guide snippets (`collection-guide-*`) have one `pt` branch shared by pt-BR and pt-PT and use Brazilian forms.
2. Other `meta_titles.*` in nl, pl, sv, pt-PT are still word-by-word (e.g. pl `meta_titles.pajamas` "Pasująca rodzina Piżamy", pt-PT ones with "combinando"); not changed (browser tab only; pajamas under owner hold).
3. `meta_descriptions.mommy_and_me` in nl/pl/sv (like es/fr/cs) mentions pajamas although the English does not; kept as in the first review, flag for the owner's pajama hold.
4. Not done: native-speaker read.
