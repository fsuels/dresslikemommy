# Portuguese image-caption translation review

Confidence: H for translation and character validation of the exact supplied text. Image contents and native asset bindings were not independently inspected by this worker.

Prepared `127` exact-English-key → Portuguese-value mappings from `69` supplied title/alt pairs. This contains `64` unique titles and `63` unique alt phrases. Shared English phrases occur once in the dictionary and retain the same translation across associations.

All 64 unique titles pass 35 characters; maximum 35. All 63 unique alt texts pass the requested 90 characters; maximum 55. Unicode characters, spaces and punctuation count once each. No empty translations, conflicting duplicate keys or duplicate source title/alt pairs were found. JSON round-trip validation passed.

Source typo: the exact dictionary key `ordinated family tops and bottoms` is preserved. Its intended “coordinated” meaning is faithfully corrected in Portuguese to “Partes de cima e de baixo coordenadas para a família”. No other source key is normalized or silently changed.

Translations preserve described people, counts, garments, colors, prints, angles and poses. They add no shipping, stock, pricing, guarantees or promotions. Brand-like English garment descriptions are translated naturally into Brazilian Portuguese consistent with the existing campaign. Generic “swimsuits” is translated as “roupas de banho”; only explicit “one-piece swimsuits” becomes “maiôs inteiros”, avoiding an unsupported garment-type assumption. Similar source phrases may legitimately share a Portuguese translation. Display text and alt text remain separately mapped even when their claims differ; the root must maintain the supplied actual image associations.

This is local preparation only. No browser, external write, image replacement, shared-asset edit, policy appeal or attempt to avoid the native Adult content rejection occurred. The current pajamas sitelink/snippet rejection is unchanged and outside this file's purpose. Passing the requested field-length checks does not establish native platform acceptance or policy approval; if a live field exposes a different limit, preserve the editor state and reconcile it directly.

Owned files only: `image_caption_translations.json` and `image_caption_review.md`. Existing payload, landing evidence and other agents' files remain unchanged.

Next action: root review these translations against the exact existing image associations and current native field limits before an authorized target-only save, then read back the resulting text.
