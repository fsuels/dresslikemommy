Confidence: H. **PASS: 35/35 independent local checks passed.** This verifies operator-supplied receipts; I did not execute mutations or inspect Shopify/MAIN UI.

The four recorded mutations are consistent: primary creation,17 metadata translations, the one-character English correction, and re-registration of the same17 values against the new live source digest. Metafield38590996545633 stayed the same. The primary description remains151 characters; only index101 changed **U+0027→U+2019**. Metafield CAS and translation-source digests were kept distinct.

All **21 final descriptions match literal expected strings**, without entity normalization:17 localized and English on en/pl/ru/sv. Titles, canonicals, routes and language attributes exactly match baseline. The first four English renders containing literal `&#39;` remain recorded failures; all17 localized head values were unchanged by the correction.

Only article `updatedAt` and `descriptionTag` changed. The English body hash remains `01c2e9ab6b5c02346c0653bcc526205b5d52c856679e4f8446698999ba53522d`. All20 locale containers preserve **36 existing values:19 titles and17 bodies**; exactly17 metadata values were added, all `outdated:false`. The17 old bodies remain `outdated:true`; no body-localization certification is implied. Held locales have no added metadata translation.

Root reports cart0, English restored and rollback unused. The first registration receipt omits submitted variables/digest; its results and after-state agree, while the final registration retains exact variables and live digest. This limits historical request reconstruction, not the verified final state.

Next: measure the first full week, September7–13, with the actual GSC cutoff and retained-order reconciliation. No search-snippet change, ranking lift, incremental traffic, sales or profit is established.

Execution SHA256 `e10fedcd99e963cbcc9bfe8deab81a80dbf2861ce0e3aaf6a095421971b8f6d2`; final API `21bf9dd2f1049ff00eabd91da891348dd77f0503f537bbfc805a17681386c5a5`; final heads `e85af9982a734f9820043e61286d1d18fd185a36b1ac90e8c667f624df810ad4`. Paired JSON contains all source bindings and locale checks.
