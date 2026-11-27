# Translation typo scan, 300 products (2026-11-27, read-only; replaces the earlier version)

Tool: `python3 ops/scripts/check_translation_typos.py` (now also image alt texts; cs vocalised prepositions v/s/z/k in safe cases, "na plocho", comma before zatímco/pokud/kde/což/takže/protože/aby/že). Locales it, cs, de, es, fr, ro. Nothing was written to any product.

Note: cs "s/z" before a word starting with s/z/š/ž should be "se/ze" (se žebrovaným, se šortkami, ze živého). "s černými" is not flagged because both forms occur.

| Batch | Products | Findings |
|---|---|---|
| top50 (hand-top20 + hand-next30) | 51 | 20 |
| 51-100 | 50 | 17 |
| 101-150 | 50 | 6 |
| 151-200 | 50 | 1 |
| 201-250 | 52 | 0 |
| 251-300 | 50 | 0 |

## top50 (hand-top20 + hand-next30)
| Handle | Locale | Check | Text |
|---|---|---|---|
| black-and-white-stripe-mommy-and-me-sweaters | cs | cs-spelling | → naplocho: rudník/prsa je šířka oděvu změřená na plocho, od podpaží k podpaží. Pro porovná |
| black-and-white-stripe-mommy-and-me-sweaters | cs | cs-vocal | [alt] v → ve: Matka a dcera v sladěných černobílých pruhovaných svetrech |
| blue-paisley-mommy-and-me-swimsuits | cs | cs-comma |  se ladně přizpůsobuje vaší postavě takže plavky lichotí a zároveň nesvazují |
| happy-faces-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| matching-father-son-hawaiian-shirts-100-cotton-tropical-print | cs | cs-vocal | s → se: bílém podkladu se snadno kombinuje s šortkami nebo chinos – ideální na dovolenou,  |
| navy-orange-floral-mommy-and-me-dresses | cs | cs-vocal | [alt] v → ve: Matka a dcera v sladěných šatech s květinovým potiskem na plá |
| scribble-heart-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| sky-blue-stripe-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| smiley-heart-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| burgundy-trim-crew-daddy-and-me-sweaters | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| christmas-reindeer-family-matching-sweaters | cs | cs-vocal | z → ze: rovedení: Pulovr s dlouhým rukávem z žakárového úpletu s kulatým výstřihem; výstři |
| cream-heart-mommy-and-me-cardigans | cs | cs-spelling | → naplocho: rudník/prsa je šířka oděvu změřená na plocho, od podpaží k podpaží. Pro porovná |
| double-heart-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| little-heart-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| navy-cable-crew-daddy-and-me-sweaters | cs | cs-vocal | s → se: nkovým vzorem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| navy-cable-crew-daddy-and-me-sweaters | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| nordic-yoke-family-matching-sweaters | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| red-heart-family-matching-sweaters | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| santa-and-friends-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| vintage-argyle-family-matching-sweaters | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |

## 51-100
| Handle | Locale | Check | Text |
|---|---|---|---|
| pom-pom-star-family-matching-sweaters | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| charcoal-cream-collar-mommy-and-me-sweaters | cs | cs-vocal | s → se: or: Antracitově šedý pletený svetr s širokým kulatým výstřihem nad krémovou pleten |
| red-striped-cuff-daddy-and-me-sweaters | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| red-cable-crew-daddy-and-me-sweaters | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| charcoal-layered-daddy-and-me-sweaters | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| eternal-bliss-hearts-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| good-luck-smile-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| moon-and-star-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| starry-sky-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| little-lamb-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| hooray-sun-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| cute-happy-bunny-bear-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| panda-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| make-life-sweet-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| duck-parade-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| one-big-star-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |
| san-francisco-family-matching-sweatshirts | cs | cs-vocal | s → se: ouhým rukávem a kulatým výstřihem, s žebrovaným výstřihem, manžetami i spodním lem |

## 101-150
| Handle | Locale | Check | Text |
|---|---|---|---|
| tropical-floral-family-matching-shirt-and-dress-outfit-set | cs | cs-spelling | → naplocho: elikostí. Rozměry mohou být měřeny na plocho, počítejte proto s drobnou odchylk |
| gradient-ombre-family-matching-outfits-pink-blue-t-shirts-with-white-shorts-set | cs | cs-vocal | [alt] v → ve: Rodina v sladěných tričkách s ombré přechodem z růžové |
| navy-floral-cotton-short-sleeve-button-down-shirt-for-men-boys | cs | cs-vocal | s → se:  po celé ploše se snadno kombinují s šortkami, chinos kalhotami nebo džínami. |
| sunflower-mommy-and-me-maxi-dresses | cs | cs-vocal | [alt] v → ve: Máma a dcera v shodných šatech s potiskem slunečnic na den v |
| sunshine-yellow-mommy-and-me-maxi-dresses | cs | cs-vocal | [alt] v → ve: Matka a dcera v sladěných žlutých letních šatech na pláži |
| sunshine-yellow-mommy-and-me-maxi-dresses | cs | cs-vocal | [alt] v → ve: Matka a dcera v sladěných žlutých šatech u oceánu |

## 151-200
| Handle | Locale | Check | Text |
|---|---|---|---|
| bright-paint-splash-family-matching-tops | cs | cs-vocal | z → ze: ečkem a zapínáním na knoflíky dělá z živého potisku snadný středobod pro dovolenou |

## 201-250
No findings.

## 251-300
No findings.
