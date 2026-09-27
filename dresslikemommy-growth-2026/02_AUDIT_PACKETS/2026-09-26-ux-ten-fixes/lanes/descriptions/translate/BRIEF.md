# Translation brief: 41 product-description text pieces

Input: `strings_en.json`, a JSON list of 41 English strings. Each one is a text piece that sits between HTML tags in a live Shopify product description for Dress Like Mommy, a family matching-outfit store that drop-ships (it has no physical store or stock).

Output: for each of your assigned locales, write `tr_<locale>.json` next to this file. Each file is a JSON object whose keys are the exact English strings and whose values are the translations, so it has all 41 keys. Use UTF-8 and `ensure_ascii=False`.

Rules:
1. Leading and trailing whitespace must match the English exactly. Many pieces start with one space; keep it.
2. Keep all numbers, sizes and units unchanged: S, M, L, XL, 2XL, 4XL, S/M, S-M, cm, 95%, ≈150 cm, 1-3 cm, and age ranges like 9-10 or 10–12 (keep the same dash). Keep product/print names that are proper nouns in English: "Shine Star", "White, Green, Blue, or Pink" → translate the color words.
3. Translate size-group words naturally: Child/Adult/Baby/Women's/Men's/Mother/Boys. Example: "Child 2 Years" → Spanish "Niño 2 años", German "Kinder 2 Jahre". Use the same size-label wording consistently across all pieces.
4. Glossary (`ops/content/translation_glossary.json`): use it where its terms appear. Never translate the brand "Dress Like Mommy".
5. Keep the meaning exact, including every honesty caveat: "not included", "sold separately", "styling only", "measurements are garment measurements", "estimated". Do not add claims such as "free", "in stock" or "best". Do not drop sentences.
6. Tone: clear, friendly shopper copy in the target language's normal conventions (quotes, decimal style for words only; do NOT change digits).
7. Piece #40 contains "converted from jin to kilograms" and "the source omits". Translate it faithfully anyway; it will be cleaned separately.
8. Validate before finishing: load each file, and check it has exactly the 41 keys, identical leading and trailing whitespace, and every digit sequence from the English present in the translation.
