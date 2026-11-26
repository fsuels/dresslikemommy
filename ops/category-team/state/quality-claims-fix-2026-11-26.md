# Calidad V10: arreglo de reclamos sin respaldo en productos, 2026-11-26T18:12Z
Solo lectura (Admin API: EN, es, de, ja, cs frente a before). Muestra de 12 productos con recibo de aplicado; 47 aplicados al revisar. Escaparate público no revisado. No cambié nada.

## Pasa
- Frases señaladas fuera en EN, es, de, cs en la muestra, y en ja salvo los idiomas saltados.
- Tablas de medidas idénticas a before; líneas de lavado conservadas.
- 0 traducciones outdated en 12 de 12.
- beer-monster: recibo marca en_ok false, pero el texto vivo muestra solo los 2 cambios esperados.

## Fallos (dueño único: agente claims-fix)
- C1. Idiomas saltados: el reclamo sigue publicado en 18 traducciones de 13 productos. daddy-baby-matching-daddysaurus-and-babysaurus-t-shirt-set-fun-dinosaur-dad-and-baby-outfit: it,ja; cow-print-mommy-and-me-swimsuits: nl; battery-themed-matching-family-t-shirt-set-super-tired-parents-energetic-kids: nl; geometric-print-mommy-and-me-swimsuits: ja; beautiful-rainbow-family-matching-t-shirts-colorful-sunshine-design: ja; top-dad-and-top-son-matching-t-shirt-onesie-set-inspired-family-outfit: ja,ko; father-and-baby-matching-pizza-slice-t-shirts-whole-pizza-slice-set: ja; father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads: fr,ja; father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow: ja; pastel-mermaid-mommy-and-me-swimsuits: ar,it,ja; swirl-print-mommy-and-me-swimsuits: ja; dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set: fr; tropical-floral-mommy-and-me-swimsuits: nl. Comprobado en la muestra: swirl ja y paisley ja sin cambios.
- C2. Se borró una característica real: father-and-son paisley, "convenient back pocket with a drainage hole" desapareció de toda la descripción (todos los idiomas aplicados). Restaurar solo el bolsillo.
- C3. Frase nueva repetida dos veces en la misma ficha: cow-print, tropical-zip, color-block, chic-mother-daughter floral cover-up, need-more drink tees, top-dad-and-top-son (en y traducciones).

## Observaciones (fuera de las filas del escáner)
- Quedan "quick-dry" sueltos (swirl, paisley, dynamic-duo, tropical-floral) y en la meta de tropical-zip ("Quick-Dry Set"); también "ensure the perfect fit" en swirl. Decidir si entran.
- es/cs de cow-print dicen "garantiza/zaručuje" donde EN dice "ensures you stand out".
