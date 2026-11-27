# Interface strings review 5: Danish, Norwegian, Brazilian Portuguese, Finnish (2026-11-27)

I reviewed the interface strings in `da.json`, `no.json`, `pt-BR.json` and `fi.json` with the same method as review 4. I hand-read the 802 in-scope leaves per file against English at origin/main 3bf0e41. All `sections.collection_seo.*` keys were left alone (the fi collection copy is being fixed by the Finnish agent).

Also not touched:
- the category-name keys
- `storefront.home_title` and `home_description`
- the legacy `shopify.checkout.*` block in `no.json`
- pt-PT and `nb.json`

**Changed:** da 49, no 64, pt-BR 54, fi 94 (261 keys). The Calidad V113 fixes for sv 1, nl 1 and pl 4 went in round 1. The product-page copy map was rebuilt only for these 7 locales. Every value has the same `{{ }}` placeholders and HTML as the English (script-checked), and `ceo_worktree check` passed in every round.

## Rules applied
- pt-BR uses você.
- "Free" in `free_shipping_short` became "included" in all four files (da "Gratis fragt", no "Gratis frakt", pt "Frete grátis", fi "Ilmainen toimitus").
- New "fresh arrivals" claims were removed where the English now says "Mommy and Me pajama sets".
- In fi, "yhteensopiva" (technical "compatible") in interface keys became "samis-" wording, consistent with the category name "Perheen samikset".

## Examples by language (before → after)

### da
| Key | Before | After |
|---|---|---|
| `products.additional_info.return_policy_line_3` | …badetøj og intimiteter… endeligt salg og personlige varer… | …badetøj og undertøj…; varer uden returret og personaliserede varer er også undtaget. |
| `sections.product_navigation.compare_collection_copy` | …sammenligne et par tætte kampe… ("close fights") | …sammenligne et par lignende modeller, før du handler videre. |
| `sections.collection_navigation.collection_categories` | Indsamlingskategorier ("fundraising") | Kollektionskategorier |
| `sections.collection_navigation.within_maternity` | Inden for barsel ("parental leave") | I kategorien Graviditetstøj |

### no
| Key | Before | After |
|---|---|---|
| `storefront.journal.about_eyebrow` | How to use the Stiljournal | Slik bruker du Stiljournalen |
| `storefront.journal.shop_family_swim` | Shop familie svømme | Handle familiebadetøy |
| `accessibility.complementary_products` | Komplimentære produkter ("compliment") | Utfyllende produkter |
| `products.shipping_country.checker_trigger` | Sender vi til landet ditt? | Sender vi til landet mitt? |

### pt-BR
| Key | Before | After |
|---|---|---|
| `storefront.journal.shop_family_swim` | Compre natação em família | Comprar moda praia para a família |
| `sections.product_navigation.back_to_family_sets` | Voltar para a família Conjuntos | Voltar para Conjuntos em família |
| `customer.activate_account.title` | (invisible BOM character)Ativar conta | Ativar conta |
| `storefront.mega_menu.valentines_short` | Dia de São Valentim (Portugal) | Dia dos Namorados |

### fi
| Key | Before | After |
|---|---|---|
| `products.product.review_widget.heading_uppercase` | ASIAKASARVELLUKSET (typo) | ASIAKKAIDEN ARVOSTELUT |
| `products.additional_info.shipping_title` | Toimitus ja toimitus | Lähetys ja toimitus |
| `recipient.form.name_label` | Vastaanottajan sähköpostiosoite (says "email") | Vastaanottajan nimi (valinnainen) |
| `sections.product_navigation.view_similar_styles` (4 keys) | samanlaisia ​​tyylejä (zero-width spaces) | samanlaisia tyylejä |

## Calidad V113 (sv, nl, pl)
- sv `storefront.callout.new_matching_outfits.callout_title`: «Se de senaste matchande looksen här».
- nl `use_fewer_filters_html`: «Gebruik minder filters of <a…>verwijder alles</a>», with the HTML unchanged.
- pl `inventory_low_stock`: «Zostało niewiele»; `inventory_low_stock_show_count`: «Zostało niewiele: {{ quantity }}».
- pl «Powrót do Topy»: comes from the interface key `sections.product_navigation.back_to_context`, not from collection copy. It now reads «Powrót do kategorii: {{ context }}».
- pl `browse_more_from` (interface key) now reads «Więcej z kolekcji: {{ collection }}», so the case after the preposition no longer matters.

## Commits and release

| Round | Commit | Keys |
|---|---|---|
| 1 | 171f562 | da 20, no 20, pt-BR 20, fi 20, sv 1, nl 1, pl 4 |
| 2 | 0d44952 | da 20, no 20, pt-BR 20, fi 20 |
| 3 | e36e8e8 | da 9, no 20, pt-BR 14, fi 20 |
| 4 | c30c76d | no 4, fi 20 |
| 5 | 16e9459 | fi 14 |

For every round:
- I wrote THEME_LOCK and re-read it after 5 s.
- Before each apply, `sync-locales` listed only my keys.
- I held the lock 3 minutes after each commit, then fetched.
- Every "Update from Shopify" export kept all my keys: 0 mismatches, and the final check at origin/main 06801a8 found all values in place with locales in sync. Nothing was reverted.

The Finnish agent's commit fbe9ccb (20 fi collection keys plus `breadcrumbs.prefix_family_matching`) did not overlap with any of my keys.

**Incident:** in round 1, `sync-theme --apply` uploaded 10 files. Besides my copy map, it pushed 9 theme files from 3760ced (another session's dresses-collection consolidation), which the GitHub sync had not delivered yet. That set live equal to main, which is what that commit intended. From round 2 on I previewed `sync-theme` before applying, and it only ever listed my copy map.

## Live readback (4 loads at least 10 s apart, no 429 or 403)

`/da/`, `/no/`, `/pt/` and `/fi/` product page (nordic-yoke sweaters): each shows "standard shipping included" in its language and contains none of the old strings ("Gratis", "Sikker logistik", "intimiteter", "ASIAKASARVELLUKSET", zero-width spaces). The new titles are in the copy map.

Two outside-scope things showed up in the HTML. They are unused data, not shown text:
- On /no, the copy map also includes the `nb` block, which still has the old texts ("Sikker logistikk", "nærkamper", "KUNDENS ANMELDELSER"); the page reads the `no` block.
- On /pt, the pt-PT block shares the root "pt" and still has the old pt texts.

## Follow-ups and English defects
1. `nb.json` needs the same review as `no.json` (follow-up unit; nb is not a published locale).
2. The Finnish product titles use "Yhteensopivat" (product content, not interface).
3. These English defects carry over from review 4: "In stock" and "Low stock" are stock claims; the gift card text says "QR code in-store"; `review_thanks_note` makes a 10% promise; `safe_payment_description` makes payment claims; and "New arrivals" / "Fresh arrivals" are newness claims.
4. The `breadcrumbs.prefix_*` keys are unused (dead keys). Their da/no/fi values are wrong but never shown.
