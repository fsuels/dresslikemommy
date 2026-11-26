# Verificación 7 (Experto Calidad), 2026-11-26T17:13Z
Cambios de ficha: 32c785b/8c1dc8c, e49b7e0/fc190c8, 3d5c796/8f3c54a. Método: origin/main, Admin API (328 activos) y lecturas en vivo espaciadas. Solo lectura; no cambié nada.

## 1. Línea de precio
- PASA lógica, 8 de 8 en vivo = mínimo del grupo (API): Nordic Yoke 37.99/49.99, Christmas Reindeer 31.99/34.99, Red Heart 45.99/51.99, Double Heart 38.99/43.99, Heart Button 54.99/60.99, bikini dos piezas 19.99/23.99; bañador blue-paisley solo $19.99 y vestido maternidad solo $107.99 (no aparece la línea).
- PASA catálogo (simulado): 280 fichas mostrarían la línea, 48 no; ningún caso en que el mínimo difiera entre variantes disponibles y totales (22 variantes no disponibles). El código no filtra disponibilidad: riesgo futuro menor.
- FALLA T7-1 (textos): "{{ group }}: Desde" deja mayúscula tras dos puntos en es, it, de, fr, nl, da, sv, no/nb, pl, cs, sk, sl, hr, lt, pt, ro, el, fi, id, vi ("Bambini: Da $31.99", "Kinder: Ab").
- FALLA T7-2: es dice "Infantil: A partir de" (adjetivo); debe ser "Niños".
- FALLA T7-3: hu y tr con doble dos puntos ("Gyerekek: Legalacsonyabb ár: ...", "Çocuk: Başlangıç fiyatı: ...").
- Menor: fr sin espacio antes de dos puntos; zh-TW "從 ... 起" correcto; en, ja, ko, hi, zh, ar, he sin objeción (juicio no nativo). La marca no aparece en la clave.
- No probado: precio tras elegir talla y color.

## 2. Fecha navideña en ficha (Christmas Reindeer, en/es/it/de/fr)
- PASA: una sola línea navideña por ficha, con "no es garantía", miércoles 2 dic y llegada miércoles 23 dic.
- FALLA T7-4: fr muestra "Ce n&#39;est pas une garantie." (código visible; doble escape en snippets/christmas-order-by.liquid) y además "23 déc.." con dos puntos.
- Menor: es "pide antes del mié, 2" y fr "avant le" sugieren que el día 2 ya no vale; mejor "hasta el" / "au plus tard le".

## 3. Precio tachado / "antes"
- PASA: los tres cambios no añaden compare-at, <s> ni "antes" (diff revisado); en vivo ninguna de las 8 fichas muestra tachado nuevo (el del vestido de maternidad $117.99 viene de compare-at ya existente; los otros tachados vistos son tarjetas de relacionados).

## Barra móvil (vistazo extra, fr 375x812)
Visible, 66 px, con dos precios, "Livraison standard incluse" y botón: sin fallo visto.

Cambios de carrito (0bc9d91, 33bf221): aún sin línea en el Log; pendientes.

## Reverificación y rec. 6 (0492632, 60bc1e5, 753d8cd), 2026-11-26T17:19Z
Archivos de origin/main, simulación sobre 328 activos y lecturas en vivo; no cambié nada.
- PASA T7-1, T7-2, T7-3: 35 idiomas en minúscula sin dos puntos; es "Niños desde"; hu/tr sin doble dos puntos (hu/tr no publicados en la tienda).
- T7-4 PARCIAL: apóstrofo francés corregido; sigue "mer. 23 déc.. Ce n'est pas..." (punto doble). FALLA menor.
- PASA nota bajo el precio en: Nordic Yoke (en/es), conjunto heart-button (en/de, frase "What you get"), vestido de maternidad sin nota.
- FALLA T7-5: 8 bañadores de dos piezas muestran "Priced per piece" / "Precio por prenda" (mom-child two-piece, pink-tropical, cow-print, chic two-piece, ruffle-top, tie-shoulder, swirl-print, abstract-print). Cada talla incluye las dos piezas, así que se puede entender que top y braga se cobran aparte. Comprobados en vivo: mom-child y swirl. Arreglo: tratar dos piezas como conjunto o no mostrar la nota. La misma frase ya existía en el constructor; ahora está junto al precio.
- Simulado: 178 fichas con nota por persona, 1 conjunto con su frase, 125 conjuntos sin nota, 24 sin nota.
Carrito: sigue sin línea en el Log.

## Reverificación de 8425985, 2026-11-26T17:24Z
- PASA T7-4: fr "mer. 23 déc. Ce n'est pas une garantie." en vivo.
- T7-5 PASA solo en inglés (8 bañadores marcados; en vivo mom-child y cow-print dicen "Pick a size for each person."; Nordic conserva "Priced per piece").
- FALLA T7-5 en otros idiomas: la detección usa el título traducido y las etiquetas, que no contienen "two-piece". En vivo /es swirl, ruffle-top y tie-shoulder siguen con "Precio por prenda"; /de mom-child con "Preis pro Teil". Simulado: 126 casos ficha-idioma en 20 idiomas (5 bañadores en los 20; pink-tropical y abstract en 9; cow-print en 8). Arreglo: detectar sin depender del título traducido (etiqueta o metacampo).
- copy_person natural en los idiomas publicados.
