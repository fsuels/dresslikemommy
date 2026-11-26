# Calidad — auditoria en vivo 2026-11-26T12:29Z (solo lectura, nada cambiado)

Alcance: 5 listados activados hoy + Nordic Yoke, Christmas Reindeer, Reindeer Row y los 7 pijamas activos que encabezan christmas-pajamas.

## GRAVE (1)
G1. Tarjetas de talla en pulgadas/libras (vista por defecto en EE. UU.) muestran solo el MINIMO de cada rango escrito con guion largo. Visto en vivo: Nordic Yoke adulto S "Weight 88.2" (real 88.2–110.2 lbs); Double Heart S "Weight 93.7, Height 59.1" (real 93.7–121.3 / 59.1–65); pijama Plaid Reindeer madre S "Waist 25.2" (real 25.2–39.8). El comprador cree que la prenda no le queda o elige mal. Heart Button (guion corto) se ve bien. 93 de 328 productos activos tienen rangos asi en sus tablas.
Arreglo: assets/product-desktop-ux-20260513-ruler-sync.js, convertRangeValue (~linea 3145 en origin/main): `split('-')` -> `split(/\s*[-\u2013\u2014]\s*/)`, conservando el separador; añadir caso a ops/tests; publicar por main y comprobar las 3 paginas.

## MEDIOS
M1. Elegir color en el selector no cambia la foto principal (Double Heart, Nordic Yoke; escritorio, /). Las fotos por color existen y estan ligadas. Arreglo: al pulsar la pastilla de color, activar el medio de la variante.
M2. Plazos: la pagina estima entrega 8–12 dic y "pide antes del 7 dic" para Navidad; datos estructurados: preparacion 1–3 dias + transito 11–13. La politica de envio (27-sep) dice envio en hasta 5 dias habiles (lo habitual ~3). Con 5 dias habiles, un pedido del 7 dic puede pasar el 23 dic. La pagina dice "no es garantia". Arreglo: adelantar la fecha limite o confirmar que el plazo real es 1–3 dias y alinear politica (decision CEO).
M3. Menu en español: "Shop" figura como "Comercio" (usar "Tienda"). Todo el sitio /es. (ja "店", de "Kaufen": mejorables.)

## BAJOS
B1. Alt de fotos sin traducir (ingles en las 20 lenguas): Vintage Argyle, Double Heart, Heart Button (todas las fotos) y las 2 fotos por color de Nordic Yoke: 320 traducciones que faltan.
B2. Columna Edad "6-12 mo" sin traducir (Double Heart, Nordic Yoke; 20 idiomas).
B3. Tabla completa en es/de: la columna de peso con coma decimal ("7,5 kg") se queda en kg mientras el resto pasa a pulgadas. Mismo archivo que G1 (convertMetricChartCell no admite coma).
B4. Buffalo Plaid Tree: manga 68 cm (madre S) a 81,2 (padre 3XL), 12 cm mas que pijamas hermanos, con manga normal en la foto. VERIFICAR contra la tabla del proveedor antes de cambiar.
B5. es: miga de pan "Emparejamiento Familiar" (mejor "Conjuntos familiares").

## Correcto
Admin: 15 ACTIVE, todas las variantes disponibles, precio de comparacion > precio, tablas con una fila por talla y sin saltos, foto ligada en cada color de sueteres/sudaderas (pijamas de un solo color usan la principal). Traducciones de producto (20 idiomas): sin faltantes en titulo/cuerpo/metas/opciones, sin desactualizadas, sin frases en ingles, marca intacta (unica diferencia numerica: arabe usa dual en "2 piezas"). 15 cargas de pagina (es/de/fr/it/ja y en): titulo y tabla traducidos, precio y InStock y marca correctos en datos estructurados (una sola oferta con el precio mas bajo), descuento "3.a pieza 20%" activo en Shopify, columnas vacias ocultas.

## No ejecutado
`audit_localized_pdp_language_leakage.py` sobre paginas publicas: BLOQUEADO, la tienda (Cloudflare) devolvio 429 a las peticiones automaticas durante >10 min; pare. Sustituto: sus reglas aplicadas a las traducciones guardadas en Shopify (no cubre textos del tema; en las paginas leidas no vi ingles salvo los puntos de arriba). Los 5 nuevos se leyeron en un idioma cada uno; Jolly Crew, Plaid Tree Trio, Blue Plaid y Green Plaid solo por Admin, sin cargar la pagina. No se probo movil, ni el boton cm/in tras pulsarlo.
