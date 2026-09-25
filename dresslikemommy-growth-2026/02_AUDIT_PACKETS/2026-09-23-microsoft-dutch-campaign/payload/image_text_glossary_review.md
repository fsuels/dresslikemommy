# Dutch image text glossary review

Confidence: H for source-key preservation, Dutch translation and local length checks. Native asset identity and character limits were not inspected.

`image_text_glossary.json` contains 64 nonempty display keys and 63 nonempty alt keys, plus an empty-to-empty mapping in each category. Every exact English key is retained, including lowercase source entries and `ordinated family tops and bottoms`; the latter is translated according to the explicitly authorized intended meaning, coordinated clothing.

All 127 nonempty translations pass the requested conservative limits: display maximum **35 characters** against 35; alt maximum **60 characters** against 100. The JSON records the actual count for every translation. All characters are in the basic multilingual plane, so these code-point counts also equal UTF-16 code units.

Translations preserve distinctions between adult/child, man/boy, woman/girl and explicitly stated family relationships. Generic shirts remain shirts; button-up source wording permits overhemden met knopen. Product-only descriptions are not converted into claims that someone is wearing the clothes. No new people counts, colors, prints, materials, product availability or photo details were added.

Distinct source phrases can share equivalent Dutch wording; no English keys were merged. Root must match each source string to its actual image/crop and verify the native field limits before saving. Empty source captions or alt text remain empty. No browser, account or external action occurred.
