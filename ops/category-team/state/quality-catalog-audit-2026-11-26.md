# Calidad — auditoria de verdad del catalogo ACTIVO (328 productos), 2026-11-26T12:36Z

Solo API de administracion, lectura. Nada cambiado; la tienda publica no se consulto. Orden dentro de cada tipo: primero los de `_DATA.md` (ventas 60 d / visitas 14 d). Los hallazgos salen de script; revise a mano los graves y descarte falsos positivos. Lo que no marco el script no queda demostrado correcto.

## GRAVE (frena la compra o falta a la verdad)
### G1. El texto promete tallas que no se venden — 9 producto(s)
Arreglo: igualar la linea "Size range" y la tabla a las variantes (o reponer la variante si el proveedor la tiene), en los 20 idiomas.
- `blue-apricot-heart-family-matching-tops`: texto promete adult sizes S–5XL; adults S through 5XL y no se venden Adult 5XL
- `blue-stripe-family-matching-shirts`: texto promete Adult S through Adult 3XL y no se venden Adult 2XL, Adult 3XL, Adult L, Adult XL, Child 4 Years
- `cable-horse-family-matching-tops`: texto promete Children 1-2Y through 9-10Y; adult sizes S–4XL; adults S through 4XL y no se venden Adult 4XL, Child 1-2 Years
- `geometric-blue-family-matching-set`: texto promete Mother S–3XL y no se venden Mother 2XL, Mother 3XL, Mother XL
- `ivory-linen-family-matching-set`: texto promete Mother S–3XL y no se venden Mother 3XL
- `ocean-dot-family-matching-set`: texto promete Mother S–3XL y no se venden Mother 3XL
- `picnic-plaid-family-matching-set`: texto promete Father S-4XL; Mother S-3XL y no se venden Father S, Mother 3XL
- `red-plaid-family-matching-tops`: texto promete adult S–3XL; fathers S-3XL; mothers S-3XL y no se venden Father 2XL, Father 3XL, Father M, Mother 2XL, Mother 3XL, Mother M
- `sunlit-floral-family-matching-set`: texto promete Father S-4XL y no se venden Father 4XL, Father S

### G2. Se vende una talla sin fila en la tabla — 7 producto(s)
Arreglo: añadir la fila desde la tabla del proveedor; si no existe, retirar la variante. (pink-wrap: "12Y" frente a fila "11-12Y", solo unificar nombre; sunflower: fila escrita "6-7 Years L".)
- `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`: sin fila: Father 3XL
- `matching-family-beach-outfits-with-floral-dresses-and-shorts`: sin fila: Father 4XL, Mother 3XL, Mother 4XL
- `matching-family-striped-cardigans-navy-and-red-heart-embroidery-knit-sweaters-for-mom-dad-and-kids`: sin fila: Father S, Father 4XL
- `matching-family-yellow-beach-outfits-summer-vacation-dresses-shorts-set`: sin fila: Father 3XL
- `navy-orange-floral-mommy-and-me-dresses`: sin fila: Girl 6-7 Years
- `pink-wrap-mommy-and-me-bikini-set`: sin fila: 12Y
- `sunflower-mommy-and-me-maxi-dresses`: sin fila: Child 6-7 Years

### G3. Colores prometidos que no existen — 3 producto(s)
Arreglo: reescribir la frase con las opciones reales.
- `color-block-mommy-and-me-swimsuits`: promete rosa, naranja, verde y negro; vende Black, Pink, Brown
- `family-matching-t-shirt-set-with-colorful-heart-brushstroke-design`: "disponible en blanco, rojo y amarillo"; no hay amarillo (opciones: White, Red, Black, Pink, Blue, Green, Purple)
- `sunflower-mommy-and-me-maxi-dresses`: promete "mostaza y negro" (2 combinaciones); vende White y Black

### G4. Piezas incluidas confusas — 1 producto(s)
- `vibrant-rainbow-family-matching-outfits-striped-t-shirts-and-yellow-overalls-set-for-family-outings`: titulo "…and Yellow Overalls Set", pero cada variante es UNA prenda y se elige en un selector llamado "Color" (T-shirt / Short / Overall); precio por prenda no explicado en el titulo. Ademas 8 filas de tallas 10-14 años vacias y la nota pide "la talla siguiente a la mayor de la tabla", que no tiene sentido. Arreglo: renombrar opcion a "Piece", decir "se vende por prenda", y retirar o medir las tallas 11-14.

### G5. Fibra sin verificar — 1 producto(s)
- `argyle-wool-mommy-and-me-cardigans`: titulo "Argyle Wool" y "the fabric is listed as 100% wool" (57.99 USD). Afirmacion de fibra basada en ficha; VERIFICAR composicion real o quitar "Wool" (obligacion de etiquetado textil).

## MEDIO
### M1. La tabla muestra tallas que no se venden (incluye los de G1) — 46 producto(s)
30 trajes/bañadores tienen la fila "Child 5-6 years" sin variante (se salta de 4-5 a 6-8): quitar la fila o crear la variante. Tambien en las demas, quitar filas.
- `abstract-print-mommy-and-me-swimsuits`: filas no vendidas: Child 5-6 years
- `animal-ruffle-mommy-and-me-swimsuits`: filas no vendidas: Child 5-6 years
- `blue-apricot-heart-family-matching-tops`: filas no vendidas: Adult 5XL
- `blue-baroque-mommy-and-me-swimsuits`: filas no vendidas: Child 5-6 years
- `blue-paisley-mommy-and-me-swimsuits`: filas no vendidas: Child 5-6 years
- `blue-stripe-family-matching-shirts`: filas no vendidas: Adult 2XL, Adult 3XL, Adult L, Adult XL, Child 4 Years
- `cable-horse-family-matching-tops`: filas no vendidas: Adult 4XL, Child 1-2 Years
- `chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection`: filas no vendidas: Child 5-6 years
- `color-block-mommy-and-me-swimsuits`: filas no vendidas: Child 5-6 years
- `cow-print-mommy-and-me-swimsuits`: filas no vendidas: Child 5-6 years
- Resto: `cream-chiffon-mommy-and-me-maxi-dresses`, `dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set`, `elegant-matching-family-outfits-light-blue-halter-dresses-casual-t-shirt-set-for-summer`, `father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear`, `father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow`, `father-and-son-matching-swim-trunks-tropical-floral-print-family-swimwear`, `father-and-son-matching-swim-trunks-tropical-paradise-red-and-green-print`, `floral-smocked-mommy-and-me-dresses`, `flower-accent-mommy-and-me-swimsuits`, `geometric-blue-family-matching-set`, `geometric-print-mommy-and-me-swimsuits`, `green-tropical-leaf-daddy-and-me-matching-swim-shorts-for-pool-days`, `ivory-linen-family-matching-set`, `leopard-mesh-mommy-and-me-swimsuits`, `leopard-ruffle-mommy-and-me-swimsuits`, `matching-dad-and-son-green-stripe-swim-trunks-beach-shorts`, `matching-dad-and-son-pink-black-color-block-swim-shorts`, `matching-dad-and-son-pink-orange-chevron-swim-trunks`, `matching-family-yellow-beach-outfits-summer-vacation-dresses-shorts-set`, `ocean-dot-family-matching-set`, `pastel-mermaid-mommy-and-me-swimsuits`, `picnic-plaid-family-matching-set`, `pink-wrap-mommy-and-me-bikini-set`, `rainbow-trim-mommy-and-me-swimsuits`, `red-botanical-mommy-and-me-swimsuits`, `red-plaid-family-matching-tops`, `red-tropical-mommy-and-me-swimsuits`, `ruffle-top-mommy-and-me-swimsuits`, `seaside-blue-plaid-family-matching-set`, `sunflower-mommy-and-me-maxi-dresses`, `sunlit-floral-family-matching-set`, `swirl-print-mommy-and-me-swimsuits`, `tie-shoulder-mommy-and-me-swimsuits`, `tropical-flair-father-and-son-matching-swim-trunks-flamingo-and-foliage-print`, `tropical-floral-mommy-and-me-swimsuits`, `tropical-zip-mommy-and-me-swimsuits`

### M2. Restos de ficha de proveedor en el texto publico — 19 producto(s)
Arreglo: frase directa sobre la tela/medidas, sin "maker" ni "listed as"; repetir traducciones.
- **[ventas/visitas]** `nordic-yoke-family-matching-sweaters`: "fabric … is listed as / sold as …" (lenguaje de proveedor)
- **[ventas/visitas]** `burgundy-trim-crew-daddy-and-me-sweaters`: "fabric … is listed as / sold as …" (lenguaje de proveedor)
- **[ventas/visitas]** `navy-cable-crew-daddy-and-me-sweaters`: "fabric … is listed as / sold as …" (lenguaje de proveedor)
- `argyle-wool-mommy-and-me-cardigans`: "fabric … is listed as / sold as …" (lenguaje de proveedor)
- `burgundy-ruffle-mommy-and-me-sweaters`: "fabric … is listed as / sold as …" (lenguaje de proveedor)
- `charcoal-cream-collar-mommy-and-me-sweaters`: "fabric … is listed as / sold as …" (lenguaje de proveedor)
- `charcoal-layered-daddy-and-me-sweaters`: "fabric … is listed as / sold as …" (lenguaje de proveedor)
- `chocolate-bandeau-draped-skirt-maternity-photoshoot-set`: "The maker does not publish a body-measurement range…"
- `heart-button-mommy-and-me-cardigan-dress-sets`: "fabric … is listed as / sold as …" (lenguaje de proveedor)
- `ivory-floral-lace-top-tiered-ruffle-skirt-maternity-photoshoot-set`: "The maker does not publish a body-measurement range…"
- Resto: `ivory-pleated-off-shoulder-rosette-maternity-photoshoot-dress`, `navy-pearl-gingham-mommy-and-me-sweaters`, `nordic-half-zip-family-matching-sweaters`, `pom-pom-star-family-matching-sweaters`, `red-cable-cardigan-mommy-and-me-sweaters`, `red-cable-crew-daddy-and-me-sweaters`, `red-lace-bow-mommy-and-me-sweaters`, `red-striped-cuff-daddy-and-me-sweaters`, `white-lace-halter-crop-top-flowing-skirt-maternity-photoshoot-set`

### M3. Caracteres chinos en traducciones — 1 producto(s)
- `meow-star-garden-mommy-and-me-pajamas`: texto chino y "el vendedor lo llama" en de/fr/it

## BAJO
### B1. Titulo con "Set" y tallas por persona sin decir en el texto que cada talla se compra aparte — 72 producto(s)
No demostrado falso: en las paginas vistas hoy el selector dice "Priced per piece". Arreglo barato: una frase fija en esas descripciones.
- **[ventas/visitas]** `tropical-palm-floral-family-matching-shirt-and-dress-set`: Tropical Palm Floral Family Matching Shirt and Dress Set
- **[ventas/visitas]** `vintage-cottage-floral-mommy-and-me-pajama-set`: Vintage Cottage Floral Mommy and Me Pajamas — Short-Sleeve Set
- `autumn-woodland-bunny-mommy-and-me-pajamas`: Autumn Woodland Bunny Mommy and Me Pajamas — Long-Sleeve Set
- `bamboo-garden-panda-cotton-mommy-and-me-pajamas`: Bamboo Garden Panda Mommy and Me Pajamas — Long-Sleeve Set
- `bird-chirping-mommy-and-me-pajamas`: Bird Chirping Fruit Orchard Mommy and Me Pajamas — Short-Sleeve Set
- `blue-paisley-mommy-and-me-swimsuits`: Blue Paisley Mommy and Me Swimsuits — Royal Blue High-Neck Halter Set
- `blue-striped-family-matching-set`: Blue Striped Family Matching Set — Dress & Shirt
- `blue-tropical-floral-family-matching-beach-dress-and-shirt-set`: Blue Tropical Floral Family Matching Beach Dress and Shirt Set
- `citrus-bloom-family-matching-set`: Citrus Bloom Family Matching Set — Dress & Shirt
- `colorful-i-love-family-matching-t-shirts-set-for-the-whole-family`: Family Matching T-Shirts – Colorful I Love Family Set
- Resto: `cute-matching-mom-and-daughter-cartoon-pajama-set-fun-and-cozy-sleepwear`, `daddy-baby-bestie-heart-matching-t-shirt-onesie-set-adorable-father-and-child-outfit`, `daddy-baby-matching-daddysaurus-and-babysaurus-t-shirt-set-fun-dinosaur-dad-and-baby-outfit`, `daddy-me-beer-monster-milk-monster-matching-t-shirt-set`, `daddy-me-matching-family-t-shirt-set-heartfelt-father-child-bond-outfit`, `dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set`, `elegant-matching-family-outfits-light-blue-halter-dresses-casual-t-shirt-set-for-summer`, `emerald-leaf-family-matching-set`, `eucalyptus-bunny-gauze-mommy-and-me-pajamas`, `family-matching-original-remix-encore-t-shirt-set-fun-family-outfits-for-all-ages`, `father-and-baby-matching-ctrl-c-ctrl-v-t-shirt-set-copy-and-paste-duo`, `father-and-baby-matching-pizza-slice-t-shirts-whole-pizza-slice-set`, `father-baby-matching-big-trouble-and-little-trouble-t-shirt-onesie-set-playful-family-outfit`, `father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads`, `father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift`, `fluttering-butterflies-mommy-and-me-pajamas`, `fresh-blue-plaid-family-matching-set`, `good-night-song-of-the-sea-mommy-and-me-pajamas`, `grape-vineyard-mommy-and-me-pajamas`, `green-palm-safari-family-matching-set`, `indigo-pocket-family-matching-set`, `ivory-cascade-mommy-and-me-set`, `ivory-linen-family-matching-set`, `ladybug-dots-mommy-and-me-pajamas`, `lavender-hydrangea-family-matching-set`, `little-pear-mommy-and-me-pajamas`, `little-sheep-meadow-mommy-and-me-pajamas`, `matching-dad-son-tropical-cotton-button-up-shirts-set-navy-leaf-print-short-sleeve`, `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`, `matching-family-yellow-beach-outfits-summer-vacation-dresses-shorts-set`, `meow-star-garden-mommy-and-me-pajamas`, `navy-red-floral-family-matching-set`, `need-more-family-matching-drink-t-shirt-set-beer-coffee-milk-juice-family-outfit`, `ocean-marble-family-matching-set`, `peach-sweetheart-mommy-and-me-pajamas`, `picnic-plaid-family-matching-set`, `pink-horizon-family-matching-set`, `polar-adventure-mommy-and-me-pajamas`, `rainbow-stripe-family-matching-set`, `red-panda-mommy-and-me-pajamas`, `safari-caravan-family-matching-set`, `scarlet-blossom-family-matching-set`, `seaside-blue-plaid-family-matching-set`, `sky-blue-family-matching-set`, `skyfade-family-matching-set`, `summer-plaid-family-matching-set`, `summer-puppies-mommy-and-me-pajamas`, `summer-sky-stripe-family-matching-set`, `sunset-ombre-family-matching-set`, `sunshine-daisy-family-matching-set`, `terracotta-tile-family-matching-set`, `top-dad-and-top-son-matching-t-shirt-onesie-set-inspired-family-outfit`, `tropical-floral-family-matching-shirt-and-dress-outfit-set`, `tropical-floral-mommy-and-me-swimsuits`, `tropical-garden-family-matching-set`, `tropical-matching-family-beach-outfits-colorful-leaf-print-summer-dresses-shorts-set`, `tropical-meadow-family-matching-set`, `tropical-zip-mommy-and-me-swimsuits`, `vibrant-rainbow-family-matching-outfits-striped-t-shirts-and-yellow-overalls-set-for-family-outings`, `watercolor-bunny-garden-mommy-and-me-pajamas`, `welsh-dinosaur-mommy-and-me-pajamas`, `willow-wildflower-family-matching-set`

### B2. Variantes agotadas — 5 producto(s)
- `eternal-love-family-matching-t-shirts-colorful-heart-design`: 15 de 75 variantes agotadas (p. ej. Child 2-3 Years / Yellow)
- `golden-daisy-mommy-and-me-set`: 1 de 21 variantes agotadas (p. ej. Pants / Child 1-2 Years)
- `playful-graphic-family-matching-tops`: 3 de 26 variantes agotadas (p. ej. Father 2XL / White Graphic)
- `red-plaid-family-matching-tops`: 1 de 22 variantes agotadas (p. ej. Father XL / Red Plaid)
- `together-heart-family-matching-sweaters`: 2 de 98 variantes agotadas (p. ej. Adult S / Red)

### B3. Rango en cm (80/85/90–150) en el texto cuando el selector usa edades — 9 producto(s)
Revisar que no sugiera tallas inexistentes.
- `black-white-spelling-family-matching-tops`: child sizes 90–15…
- `blue-apricot-heart-family-matching-tops`: adults S through 5XL…
- `cable-horse-family-matching-tops`: Children 1-2Y through 9-10Y…
- `coastal-blue-stripe-family-matching-set`: Child 80–15…
- `fluttering-butterflies-mommy-and-me-pajamas`: Child 90–15…
- `meow-star-garden-mommy-and-me-pajamas`: Child 90–15…
- `playful-graphic-family-matching-tops`: Child 85–15…
- `red-heart-raglan-family-matching-tops`: Child sizes from 90 through 15…
- `red-plaid-family-matching-tops`: mothers S-3XL…

### B4. Traducciones desactualizadas (es/de/fr/it) — 2 producto(s)
- `citrus-bloom-family-matching-set`: traduccion desactualizada: es, de
- `red-heart-raglan-family-matching-tops`: traduccion desactualizada: de, fr, it

### B5. Ingles suelto en traduccion — 1 producto(s)
- `summer-puppies-mommy-and-me-pajamas`: "Family Story:" en ingles en de

### B6. Sin tabla de tallas (gorros puede ser correcto) — 2 producto(s)
- `christmas-knit-family-matching-hats`: sin tabla de tallas
- `ring-accent-mommy-and-me-swimsuits`: sin tabla de tallas

## Sin defectos detectados
- Precio 0: 0. Compare-at menor o igual que el precio: 0. Productos sin ninguna variante vendible: 0. (101 productos sin compare-at en alguna variante; no es defecto.)
- Titulo/cuerpo/meta en en, es, de, fr, it: sin "| DLM", sin texto cortado detectado, sin entidades rotas, sin titulos o cuerpos sin traducir.
- Tela: 184 productos con metacampo de fibra, 144 sin el. Ninguna contradiccion demostrada con el texto (1 aviso descartado). Limite: la tienda solo tiene Cotton, Denim, Faux leather, Polyester, Silk, Viscose; acrilico, modal, nylon y lana no se pueden registrar.

## Limites del metodo
Colores: solo frases del tipo "colores:/disponible en"; colores nombrados de otro modo no se comprobaron. Piezas: heuristica; las imagenes no se miraron. Traducciones: solo es, de, fr, it; no se comparo el sentido. Medidas contra proveedor: no comprobadas.
