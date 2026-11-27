# Review of theme search titles changed in commit 1d6c78d (Experto SEO, 2026-11-27, read only)

43 `sections.collection_seo.meta_titles.*` values changed: daddy_me (8 languages), daddy_me_tshirts (17), spring_matching (17), mommy_and_me (de).

## Search Console check (16 months)
- daddy-me pages: 429 clicks, mostly da, no, cs, sv, fi; their `daddy_me` keys did not change.
- Lost 'son' words (de, fr, el, ro, he, ru, ar, hi): de, ro, ar 0 matching queries; fr 'pere fils' 3 impressions, 0 clicks; he 1 impression; el 'πουκαμισα για μπαμπα και γιο' 2 clicks / 3 impressions (substring sample, page not isolated). No restore recommended.
- Spanish `daddy_me` did not change; no 'padre e hijo' query on these pages.
- spring_matching: no collection page with 'easter' in the URL appears; only guides do.
- mommy_and_me de ('und' -> '&'): page has 39 impressions, no query depends on it. Keep.
- English titles are overridden in the snippet and are not affected.

## Adjust (recommended text)
| Key | Lang | Recommended | Chars | Why |
| --- | --- | --- | --- | --- |
| daddy_me_tshirts | pt-BR | Camisetas pai e filho \| Camisetas combinando | 44 | URGENT: shows '<br> Entrega Rápida?' (HTML + fast-delivery promise); 84 chars |
| daddy_me_tshirts | ja | パパと子どものTシャツ｜パパと私のおそろいコーデ | 24 | keeps パパと私, the ja query with a click (1/16) |
| daddy_me_tshirts | fr | T-shirts père et enfant \| Chemises assorties | 44 | 65 chars |
| daddy_me_tshirts | nl | T-shirts vader en kind \| Bijpassende shirts | 43 | 70 chars |
| daddy_me_tshirts | no | T-skjorter til pappa og barn \| Matchende skjorter | 49 | 65 chars |
| daddy_me_tshirts | pl | Koszulki tata i dziecko \| Pasujące T-shirty | 43 | 64 chars |
| daddy_me_tshirts | sv | T-shirts för pappa och barn \| Matchande skjortor | 48 | 62 chars |
| daddy_me_tshirts | es | Camisetas papá e hijos \| Modelos a juego | 40 | broken word order |
| daddy_me_tshirts | fi | Isän ja lapsen paidat \| Yhteensopivat T-paidat | 46 | ungrammatical |
| daddy_me_tshirts | cs | Trička pro tátu a dítě \| Sladěné vzory | 38 | ungrammatical |
| daddy_me_tshirts | ar | قمصان الأب وطفله \| تيشيرتات متطابقة | 35 | 'المحملات' is a mistranslation |
| spring_matching | es | Vestidos de Pascua mamá e hijos \| Looks de primavera | 52 | 61 chars, word order |
| spring_matching | fr | Robes de Pâques mère et fille \| Tenues de printemps | 51 | 61 chars |
| spring_matching | pt-BR | Vestidos de Páscoa mãe e filha \| Looks de primavera | 51 | 63 chars |
| spring_matching | fi | Äidin ja tyttären pääsiäismekot \| Kevään asut | 45 | English 'Easter Dresses' |
| daddy_me_shirts | pt-BR | Camisas pai e filho \| Botão e estampa havaiana | 46 | URGENT, not part of the commit: same '<br> Entrega Rápida?' |
| daddy_me_shirts, daddy_me_tshirts | pt-PT | same two pt-BR texts | <=60 | URGENT: same defect (language not published in Shopify) |

Several of these defects or lengths predate the commit; the commit only swapped the family name. All other changed titles: keep.

Not checked: live pages; the 118 display_titles for demand (they are headings, not search titles).
