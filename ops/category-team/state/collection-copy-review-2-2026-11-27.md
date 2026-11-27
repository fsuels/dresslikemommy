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

## Addendum: pt-BR (the Portuguese actually served) and Calidad V95 fixes

**Locales (Admin API `shopLocales`, read-only, 06:3xZ):** Portuguese published = `pt-BR` only. `pt-PT` is not added as a shop locale at all, so the reviewed pt-PT text above is not visible to anyone; `/pt` serves `lang="pt-BR"`. Adding/publishing pt-PT is the owner's decision; nothing changed.

**pt-BR:** 93 keys rewritten by hand from the reviewed pt-PT, adapted to real Brazilian Portuguese (você, combinando, moda praia, maiô, shorts de banho, camiseta, suéter, moletom, bebê, Dia dos Pais, encontros a dois). Kept the pt-BR short lines that were already reviewed (body sweaters/christmas/pajamas lines, metas for mommy_and_me, dresses, family_matching, daddy_me, family_pajamas, titles mommy_and_me, daddy_me, dresses, swimsuits, sweaters, pajamas). Includes `meta_titles.swimsuits` ("Moda praia combinando para a família | Mãe e filha"), `meta_titles.family_swimsuits`, and broken H1s (trunks "Natação correspondente Shorts de banho" -> "Shorts de banho combinando", tops, maxi/midi/mini/sundresses, spring, rompers, new_matching_outfits, family_matching, pants). No stock, fast shipping, reviews, bestseller or dates; no shipping wording added. Validation as above plus pt-PT term scan (fato de banho, a condizer, camisola, bebé, t-shirt, calções, amament/lactação): pass.

**Maternity:** I had nursing wording in maternity titles (nl/pl/sv/pt-PT, from the English "Maternity and Nursing Styles"). Experto SEO commit f1ca110 replaced all maternity headings in every locale before my round; I dropped my own maternity change, so f1ca110 stands.

**sv (Calidad V95):** `body.daddy_me_shirts_html` "…som ändå ser välklädda ut" -> "…som ändå känns eleganta"; `rich_parts.daddy_me_shirts.part_4_html` "…skjortor med krage ser mer välklädda ut" -> "…ser finare ut". Only these two sv keys touched (round 2).

| round | commit | pt-BR | other |
|---|---|---|---|
| 1 | 5279228 | 20 | - |
| 2 | e4b65be | 20 | sv 2 |
| 3 | 9109f9e | 20 | - |
| 4 | ee94323 | 20 | - |
| 5 | b564b4a | 13 | - |

Lock written, re-read after 5 s, 60 s after each round; waited for Experto SEO lock (seo-maternity-i18n) to clear before round 1. After each round: sync-locales apply, read-only "in sync"; final `sync-theme` 392 files, 0 differ. Origin/main after last write-back fb63a29 holds all values: pt-BR 93/93, nl 80, pl 89, pt-PT 138, sv 91. Work copy colcopy5 finished.

**Live /pt readback (2 pages, 7 s apart, 200 each):** `/pt/collections/swimsuits` tab "Moda praia combinando para a família | Mãe e filha", guide title and FAQ question 3 in new text; `/pt/collections/new-women-outfits` shows "Como escolher looks combinando para a família" and "Veja os looks Mãe e filha"; no "mamãe e eu", "Troncos" or "Natação correspondente" left on either page.

**Still open:** pt-BR `meta_titles.new_women_outfits` (tab) is "Roupas combinando para a família | Vestidos, Trajes de Banho e Família Conjuntos" and other pt-BR/nl/pl/sv meta titles are word-by-word; the inline `collection-guide-*` `pt` branch was not reviewed in this unit.

## Addendum 2: pt-BR pending, da / no / fi (STOPPED after round 1)

- Published check (Admin `shopLocales`, read-only): da, fi and `no` published; `nb` is not a shop locale (worked `locales/no.json` only); pt-BR published, pt-PT not added.
- Prepared (scratch, validated: placeholders, tags, links, banned terms): da 77 keys, no 87, fi 99 (fi used "yhteensopiva" = technically compatible throughout; rewritten with samikset / samanlaiset; old new_women_outfits structure replaced). pt-BR: `meta_titles.new_women_outfits` -> "Looks combinando para mãe, pai e filhos | Dress Like Mommy"; `body.family_swimsuits_html` calque from Calidad V100 rewritten.
- `pt` guide snippets read in full against English: already natural Brazilian Portuguese. Changed 3 lines: family-pajamas and christmas-pajamas no longer say "so they arrive in time" (now: order early and check the estimated delivery on each product page / with the photo day in mind); daddy-me "camisas de gola" -> "camisas com colarinho".
- Round 1 = commit 53fb766 (da/no/fi 20 keys each, pt-BR 2, 3 snippets). Push first failed over SSH, parked, then `push-pending` pushed it. `sync-theme --apply`: 3 snippets applied and verified; `sync-locales --apply` upserted the 4 locale files, but the read-only re-run still showed the same 20/20/20/2 keys differing.
- 60 s later Shopify's "Update from Shopify" commit 81184c7 REVERTED all locale values of round 1 on main (da, fi, no, pt-BR back to the old text). Snippets were kept (sync-theme 0 differ). Following the rule, I did not re-apply and stopped all further rounds.
- One live check of /fi/collections/new-women-outfits returned 403, so live requests stopped there.
- State now: main = old locale text for da/no/fi and those 2 pt-BR keys; the `sync-locales` read-only check reports 20/20/20/2 keys differing between live and main (live may hold my new values). It needs a look at why the upsert did not hold before any retry. Work copy colcopy6 finished; lock released.

## Addendum 3: restore of round 1 on main (07:16-07:24Z)

- Coordinator diagnosis: 81184c7 was a delayed export; live kept 53fb766. Restored the same values on main with commit 49fe1ff (commit only, no apply; SSH push failed once, `push-pending` pushed it). Values checked identical to 53fb766 before commit.
- `sync-locales` read-only after commit: da, fi, no differ only in `meta_titles.daddy_me` (autopilot commit 7cbda6c, not mine, not yet live). pt-BR differs in my 2 keys (`body.family_swimsuits_html`, `meta_titles.new_women_outfits`): live does not hold them. Not applied; question sent to coordinator.
- Lock held 3 minutes after the commit; fetch at 07:23Z: no new export, main keeps pt-BR 94/94 and da/no/fi 20 each. Lock released.
- Remaining da (57), no (67), fi (79) keys are prepared and validated but not released: a `sync-locales --apply` now would also push pt-BR and the autopilot's `meta_titles.daddy_me`, so it waits for the coordinator's decision. Work copy colcopy7 left open for that.

## Addendum 4: da / no / fi completed (07:33-07:49Z)

- 07:33Z read-only `sync-locales`: in sync (other publishers had already carried main to live, including my 2 pt-BR keys and the autopilot's `meta_titles.daddy_me`); nothing for me to apply.
- Rounds, each with lock written + re-read at 5 s, read-only drift list checked (only my keys), apply, lock held 3 min, fetch, export confirmed before release:
  | round | commit | da | no | fi |
  |---|---|---|---|---|
  | 2 | ab504b0 | 20 | 20 | 20 |
  | 3 | 96ba5ee | 20 | 20 | 20 |
  | 4 | 543f4d9 | 17 | 20 | 20 |
  | 5 | bfa4f01 | - | 7 | 19 |
- After each apply the immediate re-check sometimes still listed the keys (live lag); 3 min later it was in sync every time. No export reverted anything. Final (write-back d7162af): main holds da 77/77, no 87/87, fi 99/99, pt-BR 94/94; `sync-locales` in sync. Work copy colcopy7 finished; lock released.
- Live readback: the first request after 07:32Z (/da/collections/swimsuits) still returned 403 "Verifying your connection" (bot check), so I stopped; no, fi and /pt not read live. Live state is evidenced by `sync-locales` in sync only.

## Addendum 5: Finnish fixes (Calidad V109) and "yhteensopiva" sweep (08:01-08:15Z)

- Calidad V109 fixes: `meta_descriptions.new_women_outfits` "koissa" -> "kokoina"; `swimsuits.faq_question_1` -> "Mitä kokoja samanlaisista uima-asuista on saatavilla?"; `body.family_swimsuits_html` second paragraph rewritten, cover-up = "rantamekko"; `rich_parts.family_swimsuits.part_8_html` "rantamekko". Also `body.daddy_me_tshirts_html` reordered so "jotka sopivat lahjaksi" refers to the shirts.
- "matching" in fi: "yhteensopiva" (technical "compatible") replaced by "samanlaiset" / "samikset" (category name "Perheen samikset") in 38 rendered collection keys (H1 titles, tab titles, descriptions, short intros); "omissa koissa" -> "jokaiselle oma koko". Dead keys (swimsuits.copy_1/2, body.mommy_and_me/daddy_me/swimsuits, unreferenced rich parts, spring group, withheld family_matching.part_3) left as they are. Finnish branches of 8 snippets: guides (christmas-hubs, christmas-pajamas, daddy-me, family-pajamas, mommy-and-me, swimsuits), collection-christmas-cluster and the fi string in collection-seo-fallback; "koissa" there -> "kokoina".
- Commits cb2c99f (20 keys + 8 snippets), 36a22f3 (20), 1bc849b (2). Each: lock written + re-read at 5 s, listing, apply, 3 min held, export confirmed. Final: fi 136/136 on main after write-back 422ecf1; sync-theme 0 differ.
- Incident: in round 36a22f3 the apply ran in the same batch as the listing and also published 66b585f (SEO routine: en/cs/sv mommy_and_me meta title and description; main's own values). Reported to the coordinator; listing and apply now in separate calls. In round 1bc849b the listing showed it.json 4 keys from 3760ced (Experto SEO); applied only after the coordinator authorized it; export kept them.
- Work copy colcopy8 finished; lock released. No live reads (coordinator: browser check only).
