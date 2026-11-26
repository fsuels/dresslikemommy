# Verificación 8 (Experto Calidad), 2026-11-26T17:21Z
Carrito y pastilla: 465c7ea, 0bc9d91, 33bf221, 0b82daa. Método: lectura de origin/main (e590285) y Admin API (descuentos, colección). Solo lectura; sin pruebas de carrito en vivo; no cambié nada.

## 1. Mensaje de descuento
Los textos viven en snippets/automatic-discount-promo.liquid (20 idiomas + en; los publicados quedan cubiertos; idiomas no publicados muestran inglés), no en los 35 archivos.
- PASA estados: 0-1 piezas solo la oferta; 2 "añade una más"; aplicado solo si el carrito tiene el descuento; 3+ sin él no muestra nada.
- PASA contra el descuento activo: compra 2, 3.ª al 20 %, una vez por pedido; las 328 fichas activas están en family-bundle-eligible.
- PASA naturalidad en 21 (juicio no nativo).
- FALLA T8-1 (veracidad, texto anterior que sigue): estado 2 piezas, "Add 1 more piece and get 20% off it": si la pieza añadida es más cara, el 20 % va a otra más barata, y la línea siguiente dice "lowest-priced piece". Todos los idiomas. Propuesta: "Add 1 more piece: 20% off your lowest-priced piece".
- Observación: con 0-1 piezas ya no se dice en ningún sitio del aviso que el 20 % es sobre la pieza más barata.

## 2. Pago seguro (cs, sk, ro, ro-RO, sv, nl, vi, ar): PASA 8 de 8
Frases nominales naturales. Fuera de este cambio: ja "安全な" queda incompleto (publicado); zh "安全的" igual (no publicado); pl/ru adjetivo suelto.

## 3. Formato de moneda: PASA (leyendo Liquid)
US con USD: sin código; CAD, CZK, EUR y cualquier otro caso: money_with_currency. Líneas, precios tachados de línea, descuentos, ahorro, total y sugerencias usan la misma regla en cajón y página.
Menor: las tablas de precios por cantidad siguen siempre con código (solo si hubiera reglas de cantidad). No probado en vivo el formato "1.301,00 CZK" (depende del ajuste de moneda de la tienda).

## 4. Pastilla de temporada
- PASA fechas: Navidad 16 oct-25 dic, San Valentín 11 ene-14 feb, nada el resto (límites 15/16 oct, 25/26 dic, 10/11 ene, 14/15 feb y cambio de año); solo si la colección tiene productos; claves en los 35 idiomas.
- FALLA T8-2: pt-BR (y pt-PT) etiqueta "Dia dos Namorados" para San Valentín (en Brasil es en junio); misma corrección que T6-2.
- Menor: tr "Yılbaşı" (Año Nuevo) para Navidad; tr no publicado.

No verificado: diseño del cajón en móvil e iconos de pago (0bc9d91), fuera de lo pedido.

## Reverificación de f49942a y 584c8ce, 2026-11-26T17:29Z
- PASA T8-1: los 20 idiomas + en dicen que el 20 % es sobre la pieza más barata.
- PASA T8-2: 0 "Namorados" en origin/main; /pt muestra "São Valentim".
- PASA T7-5: detección por handle y etiquetas; en vivo /es (swirl, ruffle-top, tie-shoulder) y /de (mom-child) sin "por prenda" visible; Nordic conserva "Precio por prenda". La frase aún aparece dentro de un script de textos en esas páginas, no visible al cargar (no probé el constructor tras elegir tallas).
- No verificado: colección fall outfits (item 41), no pedido.

## Verificación ampliada (584c8ce, f49942a, item 41), 2026-11-26T17:31Z
Solo lectura; no cambié nada.
1. T7-5 PASA: en vivo es, de, fr, it en swirl, ruffle-top, mom-child two-piece y pijama eucalyptus: solo "elige una talla para cada persona", sin "por prenda"; Nordic Yoke conserva "por prenda" en los cuatro (20 de 20).
2. T8-1 y T8-2 PASAN (detalle arriba: 20 idiomas + en; 0 "Namorados" en el tema; /pt con "São Valentim"). La portada de San Valentín no es visible en vivo hasta enero.
3. Colección thanksgiving-family-outfits:
- PASA contenido: 29 productos activos (1 archivado); lo nombrado existe (camisa de cuadros, punto trenzado y Fair Isle, cárdigans, sudaderas, parejas mamá/papá, colores). Título, descripción y SEO sin Acción de Gracias, fecha ni "pide pronto" en 20 idiomas, 0 outdated; es, it, fr naturales.
- PASA enlaces: ventana 1 oct-26 nov en collection-guide-english-terms y collection-related-guides; hoy (26) se ven las guías de Acción de Gracias en en, es, it, de, fr.
- FALLA T8-3: de, descripción sin verbo completo: "Seht euch die passenden Weihnachtspyjamas ... und die passenden Familienpullover." falta "an".
- Menor: solo 1 de 29 productos es de cuadros aunque el título SEO diga "Sweaters & Plaid" y el texto "plaid button-ups" en plural.
- Observación: en /es, /it, /de, /fr la página muestra como introducción una frase genérica ("Examine ... y compare estilos") y no la descripción traducida; solo el inglés muestra texto propio.

## Reverificación de 40ba187, 2026-11-26T17:39Z
- PASA T8-3: de termina "... die passenden Familienpullover an." (API, no outdated).
- PASA intro de la colección de otoño: en vivo en, es, it, de, fr con H1, intro y título propios, sin frase genérica; claves fall_family traducidas en los 20 idiomas publicados (0 en inglés).
- No verificados (no pedidos): 6726bb8 iconos de pago en ficha, b8f68cd botón de guía de tallas.

## Ficha: 6726bb8 y b8f68cd, 2026-11-26T17:40Z
Solo lectura: origin/main (6585411), 35 locales y una ficha en vivo (/da Nordic Yoke, 1024 px).
6726bb8 iconos de pago
- PASA: salen de shop.enabled_payment_types (15 en vivo, incluidos Amazon Pay y USDC según los ajustes de la tienda); sin métodos escritos a mano, sellos ni promesas nuevas.
- FALLA T8-4: etiqueta "We accept" (solo para lector de pantalla) sin traducir en da (publicado); también en 15 locales no publicados (hr, hu, id, lt, nb, pt-PT, ro-RO, sk, sl, th, tr, vi, zh-CN, zh-TW).
b8f68cd guía de tallas
- PASA: "Size Chart" y la línea de ayuda existen traducidas en los 35 archivos; no aconsejan subir ni bajar talla; en vivo la ayuda sale una vez y existe la tabla más abajo (a unos 1.900 px, tras "Sammenlign familiestørrelser").
- FALLA T8-5 (menor): en da la etiqueta del botón parte la palabra ("Størrelsesskem/a"). En es, de, fr, it, nl, sv, no, fi, pl, cs, ro, ru, el, pt no se parte (medido a 1024 px).
- Observación: redacción automática en es ("cuadro", "tamaños"), pt ("gráfico"), he en masculino singular.
Tarjeta flotante a 1024 px
- Defecto confirmado en vivo: tapa el selector de color y parte de "Construye tu conjunto". Corrección aún no está en origin/main: PENDIENTE.

## Reverificación de f3d5d28 y 3602001, 2026-11-26T17:46Z
Origin/main y Nordic Yoke en vivo; solo lectura (no añadí nada al carrito).
- PASA T8-4: "We accept" traducido en los 35 archivos (da "Vi accepterer").
- PASA T8-5: etiqueta de guía de tallas en una línea en /da.
- PASA tarjeta flotante: oculta siempre que el constructor está en pantalla (990x700, 1024x500, 1440x900), aparece al pasarlo y muestra la línea de precio, no la frase del constructor.
- PASA móvil 375x812: barra visible abajo (66 px) como antes; la de escritorio oculta.
- Observación menor: en ventana baja (1024x500), antes de llegar al constructor la tarjeta se muestra y al bajar 200 px tapa la etiqueta "Farve" del selector de color.
- Nota de método: con el panel del navegador oculto hacen falta 2-3 s tras cada desplazamiento; una primera pasada con esperas cortas dio lecturas falsas y las descarté.

## Verificación de 77235ad (doble control de color), 2026-11-26T18:02Z
Origin/main, Admin API (328 fichas activas) y en vivo Double Heart en en + 20 idiomas (escritorio). Solo lectura.
- PASA color: el nombre traducido coincide con la lista o el filtro en los 20 idiomas, en las 277 opciones de color; nombres iguales en /xx/...double-heart....js; en vivo ningún idioma muestra desplegable de color sobre el constructor.
- FALLA T8-6 talla en neerlandés: la opción se llama "Maat" (327 opciones) y la lista de talla del Liquid (product-variant-picker.liquid) no incluye "maat" (la del script sí). En vivo /nl muestra un desplegable nativo de talla "Kind 6-12 maanden" encima del constructor: dos controles. Los otros 19 idiomas y en: solo el constructor.
- Arreglo sugerido: añadir "maat" a la condición de talla (como palabra completa) o hacer la regla independiente del idioma.

## Reverificación de 9533428 (T8-6), 2026-11-26T18:07Z
- PASA T8-6: en vivo sin desplegable nativo sobre el constructor y con pastillas presentes en Double Heart (nl, de, ja, ar, en), pijama rainbow-hearts (nl) y Nordic Yoke (hi).
- PASA control negativo: vestido de maternidad sin constructor (nl) conserva su selector de color propio.
- No revisé de nuevo los 20 idiomas ni probé añadir al carrito.
