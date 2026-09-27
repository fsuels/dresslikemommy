# Full description translation brief (715 text pieces)

Input: `full_leaves_en.json`, a JSON list of 715 English text pieces. Each is the text between HTML tags in live product descriptions for Dress Like Mommy, a family matching-outfit store that drop-ships (no physical store or stock). The pieces include prose, bullet text, and size-chart labels and headers (e.g. "Size", "Chest (cm)", "Mother S", "Kid 4T", "Height").

Output: for each assigned locale, `tr_full_<locale>.json`, a JSON object mapping every English string (exact key) to its translation, with all 715 keys. Write it with a Python script using `ensure_ascii=False`.

Rules (same as BRIEF.md, plus):
1. The pieces here are stripped, with no surrounding whitespace, so the values must have no leading or trailing whitespace either.
2. Keep every digit sequence and unit exactly: cm, kg, %, S/M/L/XL/2XL…, 2T/4T, ≈, ranges such as 9-10, and the same dash characters. Keep "Dress Like Mommy" and proper product names in English.
3. Size-chart labels: translate the size-group word and keep the code, e.g. "Mother S" → es "Mamá S", de "Mama S"; "Kid 4T" → es "Niño 4T". Headers: "Chest (cm)" → es "Pecho (cm)". Be consistent across all pieces.
4. Keep the meaning exact, including every honesty caveat (not included, sold separately, styling only, estimates, garment measurements). Add no claims such as free, in stock or best.
5. Follow the glossary `ops/content/translation_glossary.json`. Tone: clear shopper copy, using the form of address the theme uses (tú, vous, Sie, tu, você, du/je, etc.).
6. Korean: check every syllable. Hebrew: no ASCII apostrophes inside words (use ׳). Use Western digits only.
7. Validate with a script before finishing: exactly 715 keys, no empty values, no leading or trailing whitespace, every digit sequence of the key present in the value, and no `<` or `>`.
