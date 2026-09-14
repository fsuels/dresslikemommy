# Buyer selector localization — independent payload review

Reviewed 2026-09-09 18:30:42 UTC. Confidence: high for coverage and the identified wording corrections; medium for editorial quality across all languages. The reviewer did not build the payload, edit theme assets or make external writes.

**Verdict: PASS — all 100 labels accepted for this bounded selector-copy review.** Root applied the seven requested corrections across five locales. Final reviewed payload: `buy_button_locale_replacements.json`, SHA-256 `2f9860735c8d0948fec437adb377dd93545edae8c86626b90fe72bb8abd6698e`.

The correction pass passed 129 checks. Reversing only the seven values below reproduces the original reviewed file exactly (SHA-256 `fa0aa98d34cd71252c17c01715560fba802257a0c11fecaa0d1a838b1eb9b969`); the other 93 labels and complete structure are unchanged.

**Coverage and structure: PASS, 324 checks.** There are exactly 20 locale roots and five nonempty, single-line labels per root: 100 labels, no duplicate JSON keys, no missing/extra fields, and NFC Unicode throughout. The roots exactly match the 20 published non-English locales in the saved Shopify readback (`coral_copy_after.json`, shopLocales). English is the sole primary locale; the published `pt-BR` locale maps to the `pt` payload root. English copy itself is outside this payload and was not reviewed.

| Locale | Key | Original | Verified replacement | Reason |
|---|---|---|---|---|
| ar | readyToAdd | جاهز للإضافة | جاهزة للإضافة | Agree with feminine القطعة, the selected piece. |
| fr | readyToAdd | Prêt à être ajouté | Prête à être ajoutée | Agree with feminine pièce. |
| no | readyToAdd | Klar til å legges i handlekurven | Klart til å legges i handlekurven | Agree with neuter plagget. |
| ja | chooseRoleCta | ご家族を選んでください | 着る方を選んでください | Ask which person will wear the item; avoid asking the buyer to choose a family. |
| da | chooseRoleStep | Vælg, hvem denne del er til | Vælg, hvem dette stykke tøj er til | Identify one garment clearly; del can mean a part/component. |
| da | addCurrentPiece | Læg denne del i kurven | Læg dette stykke tøj i kurven | Keep the same clear single-garment referent. |
| da | readyToAdd | Klar til at blive lagt i kurven | Kan lægges i kurven | Natural neutral status, consistent with the revised garment wording. |

All 100 labels were read for meaning. They concern choosing a wearer, size/options and adding the currently selected piece/item. None promises a complete matching set, extra pieces, material quality, shipping speed, inventory or a discount. The proposed corrections preserve that meaning. The longest current add label is 39 Unicode characters; this is a layout consideration, not a verified display failure.

Implementation must retain the reviewed 20-root/five-key payload. A ready/add label describes UI readiness only and must follow actual valid-variant state. Runtime locale selection, English fallback, RTL presentation, mobile wrapping and cart behavior were not inspected in this payload-only review. This is an independent language/meaning review, not native-buyer or rendered acceptance.
