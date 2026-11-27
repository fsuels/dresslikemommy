# Fichas gratuitas de Google, 2026-11-27 (solo lectura)

Merchant 513542500, perfil Chrome `test` verificado. Estado leído ~05:43-05:58 hora de la cuenta; rendimiento 28 días (30 oct-26 nov). Nada cambiado en Merchant, feeds, Shopify ni Pinterest.

## 1. Estado (filtro: solo listados gratuitos; unidades = ofertas variante x país/idioma)

| País | Aprobadas | Limitadas | No aprobadas | En revisión | Total |
|---|---|---|---|---|---|
| Todos | 245.825 | 7.863 | 611 | 0 | 254.299 |
| US | 16.046 | 12 | 59 | 0 | 16.117 |
| CA | 15.308 | 0 | 2 | 1 | 15.311 |
| GB | 7.654 | 0 | 1 | 0 | 7.655 |
| AU | 7.647 | 0 | 2 | 0 | 7.649 |
| DE | 15.286 | 19 | 0 | 0 | 15.305 |
| SE | 15.313 | 0 | 6 | 0 | 15.319 |

### Problemas (todos los países; 8.266 ofertas con aviso; una oferta puede tener varios)

| # | Problema | Ofertas | Ejemplo | Origen visto |
|---|---|---|---|---|
| 1 | Falta envío en algunos países | 8.111 | Father & Son Matching Shirts, Soft Teal Floral, 9-10 años | Ajuste Merchant (BG, HR, MT, IN, IL, KR; países leídos el 23-11) |
| 2 | Falta precio | 102 (US 52) | Bañador mamá e hija en hindi, India | "Online store" (rastreo de Google), 7-11 |
| 3 | Moneda de envío distinta | 33 | Bañador animal print en rumano | Ajuste de envío (ficha no abierta) |
| 4 | Moneda no admitida | 28 | Set de maternidad en coreano | Mercado/ajuste (ficha no abierta) |
| 5 | Falta disponibilidad | 16 (US 3) | Good Luck Smile sweatshirts en ruso, Rusia | Rastreo de Google |
| 6 | Página no disponible | 8 (US 1) | Ho Ho Santa Child 6-7 Green, GB (API, 15-11) | Fichas archivadas en Shopify |
| 7 | "Venta de animales vivos" | 7 | Vestido de maternidad en hindi, India | Rastreo; falso positivo |
| 8 | Imagen pequeña | 5 (US 2) | Safari Caravan en hindi | Rastreo (ejemplo abierto: India) |
| 9 | Imagen rota | 1 (US) | Pijama esqueleto en alemán | Rastreo; URL vieja que hoy redirige |

Para 2, 5, 7, 8 y 9 solo se abrió un ejemplo de cada uno; en los demás renglones vistos el título no tiene formato de la app (inferencia: mismo origen).
Problema 6: los 8 son Ho Ho Santa (3), mono reno copos (2), pijama panda (2) y un bañador floral (1). Los tres primeros están ARCHIVED en Shopify; el bañador no se emparejó por ID (los 5 candidatos revisados están archivados).

## 2. Clics e impresiones gratuitas, 28 días (anuncios: 0)

Total 868 clics (+48,9%), 453.730 impresiones (+95,8%), CTR 0,2% (-23,9%), 10 compras orgánicas, USD 882. Google avisa que cambió su forma de medir.

| País | Clics | Impresiones | Compras |
|---|---|---|---|
| US | 442 | 184,55 mil | 6 |
| CA | 112 | 35,79 mil | 2 |
| AU | 99 | 47,76 mil | 0 |
| GB | 79 | 74,36 mil | 0 |
| MX | 58 | 73,47 mil | 2 |
| CH | 18 | 2,43 mil | 0 |
| DE | 7 | 2,1 mil | 0 |
| SE | 1 | 503 | 0 |

### 10 productos con más clics (suma por título; 862 de 868 clics; otros idiomas cuentan aparte)

| Producto | Clics | Compras |
|---|---|---|
| Nordic Yoke Family Sweaters | 37 | 1 |
| Sky Blue Stripe Family Sweatshirts | 20 | 0 |
| Polar Mommy & Me Pajamas | 14 | 0 |
| Reindeer Row Family Christmas Sweaters | 14 | 0 |
| Tiered Ruffle Tulle Maternity Gown | 14 | 0 |
| Grapevine Mommy & Me Nightgowns | 13 | 0 |
| Blue Plaid Reindeer Family Pajamas | 12 | 0 |
| Jolly Crew Family Pajamas | 11 | 1 |
| Ruffled Tulle Off-Shoulder Maternity Gown | 11 | 0 |
| Triple empate: Hoodies Fleece / Confetti Dots / Cardigans Navy Red Striped | 11 | 0 |

### Oportunidad: muchas impresiones, casi sin clics (solo las 50 ofertas con más impresiones, de 31.133)

- Verano (temporada baja, 0 clics): Bluebell Meadow 12.520; Summer Sky Stripe 7.880; Skyfade 7.500; Fresh Blue Plaid 7.010; Ivory Stripe Cargo 4.680; Pink Horizon 4.560.
- Navidad: Plaid Reindeer Family Pajamas 5.450 / 2 clics; "Navidad Alegre y Bendecida" 5.180 / 2; "Que Nieve" 3.080 / 0. Son las candidatas a probar foto principal o título (hipótesis; precio y foto no comparados con competidores).

## 3. Qué se arregla dónde

**Con datos de producto en Shopify (verificado):**
- Metafield de variante `mm-google-shopping.age_group`: 302 tallas de niño en 12 productos siguen como adulto (simulación de hoy: 188 kids, 107 toddler, 7 infant). No es uno de los 9 avisos. Sigue esperando el sí del dueño (bloqueo anterior de la app).
- Ninguno de los 9 avisos pide hoy un cambio de campo en Shopify: los 8 de "página no disponible" son ofertas viejas de fichas archivadas (esperar sincronización; no reactivar); imagen pequeña: Safari Caravan no tiene en Shopify ninguna imagen menor de 500 px (primeras 30).

**Solo ajustes de Merchant (dueño):**
- Países de envío (8.111): quitar IN, IL, KR y añadir BG, HR, MT (ya en `_OWNER.md`).
- Moneda de envío (33) y moneda no admitida (28).
- Fichas del rastreo de Google (avisos 2, 5, 7, 8, 9; hasta 131 avisos): se gestionan en las fuentes de Merchant. Impacto bajo (casi todo en países/idiomas sin venta; en US, 52 sin precio, 3, 2 y 1).

## 4. Cambio de hoy (código de moneda y galería): 3 ofertas

Nordic Yoke, Child 1-2 Years Gray (`…_48855064248417`):

| País | Merchant (App API) | Shopify | Datos estructurados de la página ahora |
|---|---|---|---|
| CA | CA$55 (antes CA$70), aprobado | 55 / 70 CAD | 55 CAD, InStock |
| GB | £34 (£43), aprobado | 34 / 43 GBP | 34 GBP, InStock |
| SE | SEK 453, aprobado | 453 SEK sin precio anterior | 453 SEK, InStock |

- Precio y moneda coinciden en las tres. Las ofertas vienen de la app (API), no del texto visible de la tienda.
- Importa: en Merchant está activada "Price updates" (1,18 mil productos actualizados desde la web). Los datos estructurados siguen con número y código correctos.
- Imagen: Merchant muestra la foto gris de la variante (coincide con Shopify). La página declara en datos estructurados la foto principal del producto, no la de la variante; no se sabe si cambió hoy. Se vio la miniatura, no la URL `image_link`.
- Las ofertas se actualizaron el 26-11 ~16:35-16:40 (hora de la cuenta); no verificado si fue antes o después del cambio. Repetir tras la próxima sincronización si el cambio fue posterior.
- Enlaces de oferta CA y GB llevan `country` y `currency` correctos; el de SE no se abrió.

## Efectos colaterales
Un clic en "Analyze performance" abrió el asistente de Google y dejó un chat ("Report Analysis...") en Merchant. Solo se usaron filtros de vista. Pestaña cerrada.
