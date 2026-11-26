# Content check baseline 2026-11-26 (published articles, pages, collections)

Counts below are finding rows (one per handle, locale, field and rule). Read-only scan of PUBLISHED content.

Scanned: article=121, collection=51, page=16; locales: en,ar,cs,da,de,el,es,fi,fr,he,hi,it,ja,ko,nl,no,pl,pt-BR,ro,ru,sv

Total: 489 rows in 83 resources.

## Rows by resource and category

| resource | duplicate | health_skin | performance | popularity | size_advice | translated_claim | translation_defect | total |
|---|---|---|---|---|---|---|---|---|
| article | 40 | 1 | 28 | 1 | 40 | 364 | 0 | 474 |
| collection | 0 | 0 | 0 | 0 | 0 | 7 | 5 | 12 |
| page | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 3 |

## Rows by rule

| category/rule | rows | proposed fix |
|---|---|---|
| translated_claim/size-advice | 326 | retranslate the sentence without size-up advice |
| translated_claim/performance | 47 | see section |
| duplicate/duplicate-sentence | 40 | delete the repeated sentence |
| size_advice/size-up-kids | 40 | remove 'size up' advice; point to the size chart only |
| performance/fabric-behavior | 12 | see section |
| translation_defect/brand-altered | 5 | see section |
| performance/resistance | 4 | see section |
| performance/long-lasting | 3 | see section |
| performance/uv-upf | 3 | see section |
| performance/body-type-claim | 2 | see section |
| performance/quick-dry | 2 | see section |
| health_skin/gentle-skin | 1 | see section |
| performance/premium-luxury | 1 | see section |
| performance/wrinkle | 1 | see section |
| popularity/trend-claim | 1 | rewrite as a neutral style description (no trend/hottest claim) |
| translated_claim/popularity | 1 | see section |

## Findings grouped by fix pattern

Rows: locale copies of one finding are collapsed (locales column); every row is also in findings.json.


### duplicate/duplicate-sentence (4 groups) - fix: delete the repeated sentence

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | best-fall-colors-for-family-matching-looks | en | body | Open the product page to see all the photos and details for this style. | delete the repeated sentence |
| article | best-fall-colors-for-family-matching-looks | ar,cs +17 | body | افتح صفحة المنتج لمشاهدة جميع الصور والتفاصيل الخاصة بهذا التصميم. | delete the repeated sentence |
| article | mommy-and-me-back-to-school-style-guide | en | body | Open the product page to see all the photos and details for this style. | delete the repeated sentence |
| article | mommy-and-me-back-to-school-style-guide | ar,cs +17 | body | افتح صفحة المنتج لمشاهدة جميع الصور والتفاصيل الخاصة بهذا التصميم. | delete the repeated sentence |

### health_skin/gentle-skin (1 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | sibling-matching-christmas-outfits | en | body | …t cotton shirt under the sweater is usually more comfortable for sensitive ski… | rewrite or remove |

### performance/body-type-claim (2 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | late-summer-family-matching-outfit-ideas | en | body | …easy to wear, and flattering for all body types, which makes them an easy way … | rewrite or remove |
| article | mother-daughter-matching-swimsuits-complete-guide-for-summer | en | body | …suit collection features a range of matching sets to browse for every body typ… | rewrite or remove |

### performance/fabric-behavior (12 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | best-matching-family-outfits-for-winter | en | body | Sweaters usually keep their shape better when laid flat to dry, while pajama se… | rewrite or remove |
| article | couples-matching-sweaters-valentines-guide | en | body | …s, turn printed sweatshirts inside out, and fold knits so they keep their shap… | rewrite or remove |
| article | daddy-and-me-fall-outfit-ideas | en | body | Most pieces keep their shape and color with basic care. | rewrite or remove |
| article | family-matching-outfits-for-cold-weather-outings | en | body | Some combinations that keep their shape: | rewrite or remove |
| article | holiday-family-matching-outfits-complete-guide | en | body | Basic care helps pieces keep their shape and color. | rewrite or remove |
| article | matching-family-outfits-for-august-vacations | en | body | Basic care helps pieces keep their shape and color. | rewrite or remove |
| article | matching-family-outfits-visiting-grandparents-christmas | en | body | Look for pieces that hold their shape in a bag and are comfortable for hours in… | rewrite or remove |
| article | mommy-and-me-christmas-outfits-guide | en | body | …rst time, and fold knits to store them so they keep their shape for next winte… | rewrite or remove |
| article | mommy-and-me-sweaters-guide | en | body | A pullover keeps its shape, shows the neckline detail clearly and needs no adju… | rewrite or remove |
| article | mommy-and-me-sweaters-guide | en | body | …er than hanging them helps them keep their shape, and a quick check of buttons… | rewrite or remove |
| article | mothers-day-matching-outfits-mommy-and-me-guide | en | body | …ction that feels special to mom, keep the color palette soft, and choose a fit… | rewrite or remove |
| article | spring-matching-outfits-for-mommy-and-me | en | body | …oral or watercolor anchor piece, keep the color palette soft, and choose silho… | rewrite or remove |

### performance/long-lasting (3 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | cozy-matching-outfits-for-the-thanksgiving-holiday | en | body | Here are the categories we'd browse first for style, comfort, and durability: | rewrite or remove |
| article | mommy-and-me-outfits-for-every-budget | en | body | …et spot for most families — nice enough for photos, durable enough for everyda… | rewrite or remove |
| article | mommy-and-me-sweaters-guide | en | body | If the child is between sizes, the larger one will last longer. | rewrite or remove |

### performance/premium-luxury (1 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | what-to-wear-for-family-photos-matching-outfit-ideas | en | body | Emerald, sapphire, ruby, and gold — rich and luxurious. | rewrite or remove |

### performance/quick-dry (2 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | mother-daughter-matching-swimsuits-complete-guide-for-summer | en | body | Quick-dry materials — nobody wants to sit in a wet suit | rewrite or remove |
| article | summer-matching-family-outfits | en | body | Swimwear and quick-dry pieces make sense for beach and pool plans, while airy c… | rewrite or remove |

### performance/resistance (4 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | matching-family-new-years-day-outfits | en | body | Pick pieces that resist wrinkles after a long car ride, and pack a spare top fo… | rewrite or remove |
| article | mother-daughter-matching-swimsuits-complete-guide-for-summer | en | body | Chlorine-resistant fabric — lasts longer if you're pool regulars | rewrite or remove |
| article | mother-daughter-matching-swimsuits-complete-guide-for-summer | en | body | Rinse in cold water after every wear (salt and chlorine fade colors fast) | rewrite or remove |
| article | summer-matching-family-outfits | en | body | …pieces tend to see sunscreen, salt, chlorine, sweat, and frequent washing, so … | rewrite or remove |

### performance/uv-upf (3 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | daddy-and-me-matching-outfits-the-ultimate-guide | en | body | Pair with matching rash guards for extra sun protection and style points. | rewrite or remove |
| article | mother-daughter-matching-swimsuits-complete-guide-for-summer | en | body | If sun protection is a priority (and it should be!), matching rash guard sets a… | rewrite or remove |
| article | mother-daughter-matching-swimsuits-complete-guide-for-summer | en | body | Sun-protective fabric — especially important for kids; check the product details | rewrite or remove |

### performance/wrinkle (1 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | matching-family-new-years-day-outfits | en | body | Pick pieces that resist wrinkles after a long car ride, and pack a spare top fo… | rewrite or remove |

### popularity/trend-claim (1 groups) - fix: rewrite as a neutral style description (no trend/hottest claim)

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | best-matching-outfits-for-thanksgiving-dinner | en | body | Burgundy is the color of the season. | rewrite as a neutral style description (no trend/hottest cl… |

### size_advice/size-up-kids (40 groups) - fix: remove 'size up' advice; point to the size chart only

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | adorable-matching-valentines-day-looks-for-the-whole-family | en | body | Pro tip: consider a size up for children so they can enjoy the outfit for more … | remove 'size up' advice; point to the size chart only |
| article | apple-picking-matching-outfits-for-the-whole-family | en | body | Pro tip: order a size up for children so they can enjoy the outfit for more tha… | remove 'size up' advice; point to the size chart only |
| article | babys-first-christmas-matching-family-outfits | en | body | If your baby is between sizes, sizing up gives room for a growth spurt and more… | remove 'size up' advice; point to the size chart only |
| article | back-to-school-daddy-and-me-photo-outfits | en | body | Pro tip: consider sizing up for children so they can enjoy the outfit for more … | remove 'size up' advice; point to the size chart only |
| article | best-family-matching-outfits-for-harvest-season | en | body | For kids, sizing up one size can leave growing room. | remove 'size up' advice; point to the size chart only |
| article | best-matching-outfits-for-family-beach-trips | en | body | Pro tip: order a size up for children so they can enjoy the outfit for more tha… | remove 'size up' advice; point to the size chart only |
| article | coordinating-family-outfits-for-october-events | en | body | Pro tip: consider sizing up for children so they can enjoy the outfit for more … | remove 'size up' advice; point to the size chart only |
| article | daddy-and-me-christmas-outfits | en | body | …e, so if a child is between sizes, sizing up gives room to grow, while staying… | remove 'size up' advice; point to the size chart only |
| article | daddy-and-me-fall-outfit-ideas | en | body | For kids, we suggest sizing up one size for growing room — these pieces are too… | remove 'size up' advice; point to the size chart only |
| article | easter-sunday-family-matching-outfits | en | body | Pro tip: consider sizing up for children so they can enjoy the outfit for more … | remove 'size up' advice; point to the size chart only |
| article | end-of-summer-mommy-and-me-beach-style | en | body | For kids, consider sizing up for growing room. | remove 'size up' advice; point to the size chart only |
| article | fall-family-photo-outfits-for-november | en | body | Pro tip: consider a size up for children so they can enjoy the outfit for more … | remove 'size up' advice; point to the size chart only |
| article | fall-family-photo-session-complete-matching-outfit-guide | en | body | Pro tip: consider sizing up for children so they can enjoy the outfit for more … | remove 'size up' advice; point to the size chart only |
| article | fall-festival-matching-outfits-for-the-whole-family | en | body | For kids, sizing up one size gives growing room — these pieces are too cute to … | remove 'size up' advice; point to the size chart only |
| article | father-and-son-matching-button-up-shirts | en | body | For a growing boy, sizing up gives room to grow, and the sleeves can be rolled … | remove 'size up' advice; point to the size chart only |
| article | floral-matching-outfits-for-spring | en | body | For kids, consider sizing up for growing room. | remove 'size up' advice; point to the size chart only |
| article | holiday-family-matching-outfits-complete-guide | en | body | Pro tip: order a size up for children so they can enjoy the outfit for more tha… | remove 'size up' advice; point to the size chart only |
| article | hot-weather-family-coordinating-outfit-ideas | en | body | For kids, sizing up one can leave growing room. | remove 'size up' advice; point to the size chart only |
| article | last-chance-summer-matching-family-outfits | en | body | Pro tip: order a size up for children so they can enjoy the outfit for more tha… | remove 'size up' advice; point to the size chart only |
| article | late-summer-family-matching-outfit-ideas | en | body | For kids, many parents size up one size for growing room — these pieces are too… | remove 'size up' advice; point to the size chart only |
| article | matching-family-christmas-shirts | en | body | …e, so if a child is between sizes, sizing up leaves room to grow, while stayin… | remove 'size up' advice; point to the size chart only |
| article | matching-family-outfits-for-august-vacations | en | body | For kids, sizing up one size gives growing room. | remove 'size up' advice; point to the size chart only |
| article | matching-family-outfits-for-mothers-day-brunch | en | body | …ach product page, measure rather than guessing, and consider sizing up for kid… | remove 'size up' advice; point to the size chart only |
| article | matching-family-outfits-for-pumpkin-patch-photos | en | body | For kids, sizing up one size gives growing room — these pieces are too cute to … | remove 'size up' advice; point to the size chart only |
| article | matching-family-shirts-for-pictures | en | body | …if a child is between sizes you can size up for room to grow, or stay true to … | remove 'size up' advice; point to the size chart only |
| article | mommy-and-me-fall-fashion-cozy-coordinating-outfits | en | body | Pro tip: consider a size up for children so they can enjoy the outfit for more … | remove 'size up' advice; point to the size chart only |
| article | mommy-and-me-halloween-outfits-that-are-actually-stylish | en | body | For kids, consider sizing up one size for growing room. | remove 'size up' advice; point to the size chart only |
| article | mommy-and-me-summer-dress-guide | en | body | For kids, consider sizing up one size for growing room. | remove 'size up' advice; point to the size chart only |
| article | mommy-and-me-thanksgiving-style-guide | en | body | …instead of guessing, and consider sizing up for children who are between sizes. | remove 'size up' advice; point to the size chart only |
| article | mommy-and-me-winter-sweatshirts-and-loungewear | en | body | If a child is between sizes, size up for growing room. | remove 'size up' advice; point to the size chart only |
| article | mommy-and-newborn-holiday-matching-outfits | en | body | A relaxed family sweater in a size up from your usual gives room to move and to… | remove 'size up' advice; point to the size chart only |
| article | new-year-new-matching-looks-family-fashion | en | body | For kids, sizing up one size can leave growing room. | remove 'size up' advice; point to the size chart only |
| article | october-family-style-cozy-matching-looks-for-autumn | en | body | Pro tip: order a size up for children so they can enjoy the outfit for more tha… | remove 'size up' advice; point to the size chart only |
| article | one-family-outfit-for-thanksgiving-and-christmas | en | body | If a child is between sizes, sizing up gives room to move, to layer a sweater o… | remove 'size up' advice; point to the size chart only |
| article | pumpkin-spice-and-everything-nice-fall-family-fashion | en | body | Pro tip: order a size up for children so they can enjoy the outfit for more tha… | remove 'size up' advice; point to the size chart only |
| article | september-style-guide-transitional-family-matching-looks | en | body | For kids, sizing up one can leave growing room. | remove 'size up' advice; point to the size chart only |
| article | spring-break-matching-looks-for-the-whole-family | en | body | …age, measure rather than guess, and consider sizing up for kids who are growin… | remove 'size up' advice; point to the size chart only |
| article | summer-vacation-matching-family-outfits-guide | en | body | For kids, consider sizing up one size for growing room. | remove 'size up' advice; point to the size chart only |
| article | transitional-weather-family-matching-style-guide | en | body | …age, measure rather than guess, and consider sizing up for kids who are growin… | remove 'size up' advice; point to the size chart only |
| article | transitioning-from-summer-to-fall-family-matching-tips | en | body | For kids, sizing up one size gives growing room — these pieces are too cute to … | remove 'size up' advice; point to the size chart only |

### translated_claim/performance (24 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | autumn-matching-family-style-plaid-flannel-and-more | de | body | Hochwertige passende Outfits sind eine Investition in Familienerinnerungen. | rewrite or remove |
| article | daddy-and-me-fall-outfit-ideas | de | body | Hochwertige Partnerlooks sind eine Investition in Familienerinnerungen. | rewrite or remove |
| article | daddy-and-me-spring-outfits | de | body | Hochwertige Partnerlooks sind eine Investition in Familienerinnerungen. | rewrite or remove |
| article | holiday-family-matching-outfits-complete-guide | de | body | Hochwertige Partnerlook-Outfits sind eine Investition in Familienerinnerungen. | rewrite or remove |
| article | how-to-style-cozy-mommy-and-me-looks-in-january | de | body | Hochwertige Partnerlook-Outfits sind eine Investition in Familienerinnerungen. | rewrite or remove |
| article | matching-family-cruise-outfits | pt-BR | body | …de mão para que as fotos principais fiquem garantidas mesmo se uma mala atrasa… | rewrite or remove |
| article | matching-family-outfits-for-august-vacations | de | body | Hochwertige Partnerlook-Outfits sind eine Investition in Familienerinnerungen. | rewrite or remove |
| article | matching-family-outfits-visiting-grandparents-christmas | es,nl | body | Enróllalos en lugar de doblarlos y saldrán de la maleta casi sin arrugas. | rewrite or remove |
| article | matching-outfit-sizing-guide-right-fit-for-everyone | es,nl | seo_title | …a de Tallas para Conjuntos a Juego: Cómo Conseguir el Ajuste Perfecto para Tod… | rewrite or remove |
| article | matching-outfit-sizing-guide-right-fit-for-everyone | es,nl | title | …a de Tallas para Conjuntos a Juego: Cómo Conseguir el Ajuste Perfecto para Tod… | rewrite or remove |
| article | mommy-and-me-back-to-school-style-guide | de | body | Hochwertige passende Outfits sind eine Investition in Familienerinnerungen. | rewrite or remove |
| article | mommy-and-me-fall-fashion-cozy-coordinating-outfits | de,pl | body | Hochwertige Partnerlooks sind eine Investition in Familienerinnerungen. | rewrite or remove |
| article | mommy-and-me-outfits-for-every-budget | cs,de +2 | body | Prémiové sladění: $60+ | rewrite or remove |
| article | mother-daughter-matching-swimsuits-complete-guide-for-summer | cs,de +6 | body | Rychleschnoucí materiály — nikdo nechce sedět v mokrých plavkách | rewrite or remove |
| article | summer-matching-family-outfits | cs,de +6 | body | Plavky a rychleschnoucí kousky dávají smysl na pláž a k bazénu, zatímco vzdušné… | rewrite or remove |
| article | winter-family-photo-outfits-matching-looks-for-cold-weather | de | body | Hochwertige Partner-Outfits sind eine Investition in Familienerinnerungen. | rewrite or remove |
| collection | dresses | it | body | …l’acquisto sapendo che l’ordine è garantito da spedizione gratuita e resi entr… | rewrite or remove |
| collection | family-sets | it | body | …l’acquisto sapendo che l’ordine è garantito da Spedizione gratuita + resi entr… | rewrite or remove |
| collection | formal-dresses | it | body | …l’acquisto sapendo che l’ordine è garantito da spedizione gratuita e resi entr… | rewrite or remove |
| collection | matching-couples-t-shirts | it | body | …l’acquisto sapendo che l’ordine è garantito da spedizione gratuita e resi entr… | rewrite or remove |
| collection | matching-outfits | fr | body | …choix de tenues assorties adorables et de qualité supérieure à prix abordables. | rewrite or remove |
| collection | maxi-dresses | it | body | …l’acquisto sapendo che l’ordine è garantito da spedizione gratuita e resi entr… | rewrite or remove |
| collection | trunks | it | body | …l’acquisto sapendo che l’ordine è garantito da spedizione gratuita e resi entr… | rewrite or remove |
| page | size-guide | es,it,nl | body | …medir a su familia y leer esas tablas, y obtendrá un ajuste perfecto para todo… | rewrite or remove |

### translated_claim/popularity (1 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | mother-daughter-matching-swimsuits-complete-guide-for-summer | de | body | Die beliebtesten Stile für Partnerlook-Badeanzüge für Mutter und Tochter | rewrite or remove |

### translated_claim/size-advice (54 groups) - fix: retranslate the sentence without size-up advice

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| article | adorable-matching-valentines-day-looks-for-the-whole-family | cs,de +5 | body | Tip: pro děti zvažte o velikost větší, aby si outfit mohly užít déle než jednu … | retranslate the sentence without size-up advice |
| article | apple-picking-matching-outfits-for-the-whole-family | cs,de +5 | body | Tip: objednejte dětem o velikost větší, aby si outfit užily víc než jednu sezón… | retranslate the sentence without size-up advice |
| article | babys-first-christmas-matching-family-outfits | de,es +3 | body | …schen zwei Größen liegt, lässt eine Größe größer Platz für einen Wachstumsschu… | retranslate the sentence without size-up advice |
| article | back-to-school-daddy-and-me-photo-outfits | cs,de +5 | body | Tip: pro děti zvažte o velikost větší, aby si outfit mohly užít déle než jednu … | retranslate the sentence without size-up advice |
| article | best-family-matching-outfits-for-harvest-season | cs,de +3 | body | U dětí může o velikost větší nechat prostor k růstu. | retranslate the sentence without size-up advice |
| article | best-matching-family-outfits-for-winter | cs,de +5 | body | …ejte podle požadovaného střihu: o velikost větší pro volný zimní vzhled, nebo … | retranslate the sentence without size-up advice |
| article | best-matching-outfits-for-family-beach-trips | cs,de +5 | body | Tip: pro děti objednejte o velikost větší, aby si outfit užily déle než jednu s… | retranslate the sentence without size-up advice |
| article | best-matching-outfits-for-thanksgiving-dinner | de,fr +3 | body | …er Produktseite und wählen Sie eine Größe größer, wenn jemand zwischen zwei Gr… | retranslate the sentence without size-up advice |
| article | coordinating-family-outfits-for-october-events | cs,de +5 | body | Tip: zvažte o velikost větší pro děti, aby si outfit mohly užít i déle než jedn… | retranslate the sentence without size-up advice |
| article | couples-matching-sweaters-valentines-guide | de,es +4 | body | …r einen Oversize-Look probiert eine Größe größer; für eine schmale Passform ri… | retranslate the sentence without size-up advice |
| article | daddy-and-me-christmas-outfits | de,es +3 | body | …schen zwei Größen liegt, lässt eine Nummer größer Platz zum Wachsen, während d… | retranslate the sentence without size-up advice |
| article | daddy-and-me-fall-outfit-ideas | cs,de +5 | body | U dětí doporučujeme o velikost větší kvůli růstu - tyto kousky jsou příliš rozt… | retranslate the sentence without size-up advice |
| article | easter-sunday-family-matching-outfits | cs,de +5 | body | Tip: zvažte pro děti o velikost větší, aby outfit mohly nosit déle než jednu se… | retranslate the sentence without size-up advice |
| article | end-of-summer-matching-family-beach-looks | nl | body | …tussen twee maten in, kies dan een maat groter voor een ruimere pasvorm of je … | retranslate the sentence without size-up advice |
| article | end-of-summer-mommy-and-me-beach-style | de,es +4 | body | Bei Kindern lohnt sich eine Nummer größer, damit noch Platz zum Wachsen bleibt. | retranslate the sentence without size-up advice |
| article | fall-family-photo-outfits-for-november | cs,de +4 | body | Tip: pro děti zvažte o velikost větší, aby si outfit užily víc než jednu sezónu. | retranslate the sentence without size-up advice |
| article | fall-family-photo-session-complete-matching-outfit-guide | cs,de +5 | body | Tip: zvažte o velikost větší pro děti, aby si outfit mohly užít déle než jednu … | retranslate the sentence without size-up advice |
| article | fall-festival-matching-outfits-for-the-whole-family | cs,de +5 | body | U dětí o velikost větší nechává prostor k růstu - tyhle kousky jsou příliš rozt… | retranslate the sentence without size-up advice |
| article | family-matching-outfits-for-cold-weather-outings | cs,de +5 | body | …společný svetr oblékněte tenké triko místo toho, abyste volili o velikost větš… | retranslate the sentence without size-up advice |
| article | family-matching-pajamas-our-top-picks-for-cozy-nights | de,es +4 | body | …rschlafbekleidung nicht automatisch eine Nummer größer, um Wachstum einzuplane… | retranslate the sentence without size-up advice |
| article | father-and-son-matching-button-up-shirts | es,fr +3 | body | Para un niño que crece, elegir una talla más grande deja margen y se pueden rem… | retranslate the sentence without size-up advice |
| article | floral-matching-outfits-for-spring | cs,de +4 | body | U dětí zvažte o velikost větší, aby měly prostor na růst. | retranslate the sentence without size-up advice |
| article | holiday-family-matching-outfits-complete-guide | cs,de +4 | body | Tip: pro děti objednejte o velikost větší, aby si outfit užily déle než jednu s… | retranslate the sentence without size-up advice |
| article | hot-weather-family-coordinating-outfit-ideas | cs,de +4 | body | U dětí může o velikost větší kousek nechat prostor k růstu. | retranslate the sentence without size-up advice |
| article | last-chance-summer-matching-family-outfits | cs,de +4 | body | Tip: pro děti objednejte o velikost větší, aby si outfit užily víc než jednu se… | retranslate the sentence without size-up advice |
| article | late-summer-family-matching-outfit-ideas | cs,de +5 | body | U dětí si mnoho rodičů bere o velikost větší, aby měly prostor k růstu — tyhle … | retranslate the sentence without size-up advice |
| article | matching-couples-christmas-pajamas-and-sweaters | cs,de +5 | body | …jak chcete, aby kousek působil: o velikost větší pro volný střih příjemný na s… | retranslate the sentence without size-up advice |
| article | matching-couples-sweatshirts-and-hoodies-for-winter | de,fr,nl | body | …versized-Look mögt, prüft das Brustmaß, statt blind eine Größe größer zu nehme… | retranslate the sentence without size-up advice |
| article | matching-family-christmas-shirts | de,es +3 | body | …nd zwischen zwei Größen, lässt eine Nummer größer Platz zum Wachsen, während d… | retranslate the sentence without size-up advice |
| article | matching-family-christmas-sweatshirts-guide | cs,de +5 | body | Pro uvolněný oversize vzhled dospělí často volí o velikost větší. | retranslate the sentence without size-up advice |
| article | matching-family-outfits-for-august-vacations | cs,de +4 | body | U dětí nechává o velikost větší prostor k růstu. | retranslate the sentence without size-up advice |
| article | matching-family-outfits-for-mothers-day-brunch | cs,de +5 | body | …ránce každého produktu, měřte místo odhadování a u dětí zvažte o velikost větš… | retranslate the sentence without size-up advice |
| article | matching-family-outfits-for-pumpkin-patch-photos | cs,de +3 | body | U dětí o velikost větší dá prostor k růstu - tyhle kousky jsou příliš roztomilé… | retranslate the sentence without size-up advice |
| article | matching-family-pajamas-sizing-newborn-to-adult | de,es +4 | body | Wenn du weite Nachtwäsche magst, nimm eine Größe größer. | retranslate the sentence without size-up advice |
| article | matching-family-shirts-for-pictures | de,it,nl | body | …inem Kind zwischen zwei Größen eine Nummer größer nehmen, damit es noch wachse… | retranslate the sentence without size-up advice |
| article | matching-outfit-sizing-guide-right-fit-for-everyone | es,fr +2 | body | No des por hecho que una talla más grande resolverá todas las dudas de ajuste. | retranslate the sentence without size-up advice |
| article | matching-outfit-sizing-guide-right-fit-for-everyone | es,fr +2 | seo_description | …y recomendaciones sobre cuándo elegir una talla más grande o la talla habitual. | retranslate the sentence without size-up advice |
| article | matching-outfits-for-couples-guide | cs,de +3 | body | Jeden si může vzít o velikost větší pro volný vzhled, zatímco druhý se bude drž… | retranslate the sentence without size-up advice |
| article | mommy-and-me-fall-fashion-cozy-coordinating-outfits | cs,de +5 | body | Tip: zvažte pro děti o velikost větší, aby si outfit užily víc než jednu sezonu. | retranslate the sentence without size-up advice |
| article | mommy-and-me-halloween-outfits-that-are-actually-stylish | cs,de +4 | body | U dětí zvažte o velikost větší, aby měly prostor k růstu. | retranslate the sentence without size-up advice |
| article | mommy-and-me-summer-dress-guide | cs,de +5 | body | U dětí zvažte o velikost větší, aby měly prostor na růst. | retranslate the sentence without size-up advice |
| article | mommy-and-me-thanksgiving-style-guide | cs,de +5 | body | …měřte místo odhadování a zvažte o velikost větší pro děti, které jsou mezi dvě… | retranslate the sentence without size-up advice |
| article | mommy-and-me-winter-sweatshirts-and-loungewear | cs,de +3 | body | …zůstane u své běžné velikosti a o velikost větší bere jen pro vrstvený vzhled … | retranslate the sentence without size-up advice |
| article | mommy-and-newborn-holiday-matching-outfits | cs,fr +3 | body | Volný rodinný svetr o velikost větší, než nosíte obvykle, dává prostor k pohybu… | retranslate the sentence without size-up advice |
| article | new-year-new-matching-looks-family-fashion | cs,de +5 | body | U dětí může o velikost větší oblečení nechat prostor pro růst. | retranslate the sentence without size-up advice |
| article | october-family-style-cozy-matching-looks-for-autumn | cs,de +5 | body | Tip: pro děti objednejte o velikost větší, aby si outfit užily víc než jednu se… | retranslate the sentence without size-up advice |
| article | pumpkin-spice-and-everything-nice-fall-family-fashion | cs,de +5 | body | Tip: pro děti objednejte o velikost větší, aby si outfit mohly užít víc než jed… | retranslate the sentence without size-up advice |
| article | red-white-and-blue-patriotic-family-matching-looks | de,nl | body | …schen zwei Größen liegt, wählt eine Größe größer für eine lockerere Passform o… | retranslate the sentence without size-up advice |
| article | september-style-guide-transitional-family-matching-looks | de,es +4 | body | Bei Kindern kann eine Nummer größer Platz zum Wachsen lassen. | retranslate the sentence without size-up advice |
| article | spring-break-matching-looks-for-the-whole-family | cs,de +5 | body | …ce produktu, měřte místo odhadování a u rostoucích dětí zvažte o velikost větš… | retranslate the sentence without size-up advice |
| article | summer-matching-family-outfits | nl | body | …tussen twee maten in, kies dan een maat groter als de outfit meerdere uren in … | retranslate the sentence without size-up advice |
| article | summer-vacation-matching-family-outfits-guide | cs,de +5 | body | U dětí zvažte o velikost větší, aby měly prostor na růst. | retranslate the sentence without size-up advice |
| article | transitional-weather-family-matching-style-guide | cs,de +5 | body | …, raději změřte, než abyste hádali, a u rostoucích dětí zvažte o velikost větš… | retranslate the sentence without size-up advice |
| article | transitioning-from-summer-to-fall-family-matching-tips | cs,de +4 | body | U dětí o velikost větší nechá prostor k růstu — tyhle kousky jsou příliš roztom… | retranslate the sentence without size-up advice |

### translation_defect/brand-altered (2 groups) - fix: rewrite or remove the matched text

| resource | handle | locales | field | matched text | proposed fix |
|---|---|---|---|---|---|
| collection | mommy-and-me | cs,de +2 | seo_title | Máma a dcera: sladěné šaty, plavky a soupravy | rewrite or remove |
| collection | rompers | ko | body | Dresslikemommy은 어떤 상황에도 딱 맞는 세련되고 저렴한 다양한 롬퍼를 제공합니다. 공원에 가거나, 파티에 가거나, 심부름을 가거나… | rewrite or remove |
