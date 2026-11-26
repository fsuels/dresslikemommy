# Calidad — verificacion independiente 2, 2026-11-26T13:15Z (solo lectura, muestreo)

## 1. Veracidad de catalogo (10 fichas): FALLA
Muestra: argyle-wool, vibrant-rainbow, color-block, blue-paisley, tropical-floral, red-plaid, blue-stripe, sunflower, beach floral dresses+shorts, nordic-yoke.
Linea base: mi volcado de las 12:26–12:30Z (anterior a los cambios) + recibos. 10/10: mismas variantes, precio, compare-at y estado; traducciones es/de/fr/it vigentes; tablas bien formadas.
PASA 8: argyle-wool (lana retirada tambien del titulo y de es/de/fr/it), vibrant-rainbow (dice prenda por prenda y que faltan medidas 10–14), color-block (3 colores reales), blue-paisley y tropical-floral (fila 5-6 retirada; filas = variantes), red-plaid y blue-stripe (rango = variantes), sunflower (blanco/negro; fila 6-7 corregida).
FALLA:
a) Afirmacion de fibra reforzada (grave). 13 fichas pasaron de "the main fabric is listed as modal" a "the main fabric is modal" (nordic-yoke, burgundy x2, charcoal x2, navy x2, red x4, pom-pom, y las traducciones leidas en nordic-yoke); heart-button pasa a "composition of…" y nordic-half-zip a "made of modal yarn, with viscose (70%) as the main fiber". La unica prueba en los archivos es el atributo del proveedor (en argyle la misma clase de dato se retiro). No hay prueba nueva. Mi recomendacion M2 ("quitar listed as") contribuyo: la corrijo. Arreglo: o verificar composicion, o quitar la fibra no verificada ("Thick, soft knit"), nunca afirmarla como hecho; revisar los 20 idiomas.
b) matching-family-beach-outfits-with-floral-dresses-and-shorts: siguen sin fila Father 4XL, Mother 3XL y Mother 4XL (defecto G2 abierto). La version it muestra 2 tablas (en: 1; ya era asi antes).
Nota anterior a este cambio: en red-plaid y blue-stripe la traduccion es tiene 2 lineas menos que en (falta la de tela).

## 2. Textos de interfaz (ar, hi, he, ko, ru, pl, nl, sv, da, fi): FALLA (1 error, 2 menores)
Lei los valores nuevos de 54eeecf, dc0ad38 y ce59252 en origin/main y la tabla de meses usada por d954a6c.
- fi storefront.journal.styling_guide = "Tyylioppaa" (caso partitivo); debe ser "Tyyliopas". FALLA.
- da breadcrumbs.label_new_arrivals = "Nye ankomster" (calco); tienda diria "Nyheder". Menor.
- ru journal: "Руководство по стилю" / "Читать руководство" suenan a manual; natural "Гид по стилю" / "Читать гид". Menor.
- ar, hi, he, ko, pl, nl, sv y meses: sin objeciones. (Juicio de revisor, no hablante nativo certificado.)

## 3. Colecciones 7ec755e y relacionadas (es, de, it, fr; 24 paginas en vivo + productos por API): FALLA en 2 de 6
- pajamas (25, todos mama-hija): PASA. sweaters (13: 9 mama-hija, 4 familia): PASA. dresses (37 mama-hija): PASA. mommy-and-me (116): PASA.
- matching-outfits: FALLA. Intro y descripcion de Google prometen trajes de baño ("bañadores", "Bademode", "costumi", "maillots") y de sus 193 productos activos ninguno es de baño. (Texto de un lanzamiento anterior de hoy; no lo detecte en mi revision previa.) Arreglo: quitar la palabra o añadir los productos.
- valentines-day-matching-outfits-1: FALLA. Titulo de Google dice mama e hija ("Looks de Mamá y Yo", "Mama & Tochter", "mamma e figlia", "Mère-fille") y 15 de 19 productos son de familia (1 de papa). Encabezado e intro correctos. Arreglo: titulo "para toda la familia".

## Limites
10 de 69 fichas; traducciones comparadas solo en es/de/fr/it; no verifique composicion real de ninguna tela.
