# Pinterest: feed alojado viejo — paquete para decisión del CEO (2026-11-26, NADA APLICADO)

Corrige mi nota de 12:13Z: los productos de Navidad no faltan en Pinterest. Faltan solo en el feed de Cloudflare.

## Diagnóstico (LIVE_VERIFIED, lectura; perfil Chrome test; anunciante dresslikemommy.com, catálogo 3041764155561548387)

Dos orígenes conviven:

1. **App de Shopify** (fuentes "Shopify (US, xx)", ~19 idiomas). Ingesta 25-26 nov, 7.264–7.659 aceptados por fuente. `Shopify (US, en)` 3041760867124595727: 26 nov 03:35 EST, 7.533, 0 fallos, 0 avisos en la última ingesta. Shopify: 328 de 328 activos publicados en el canal Pinterest (7.659 variantes).
2. **Worker de Cloudflare** `dlm-pinterest-feed-worker`: `DLM Cloudflare Grouped Feed 2026-05-18` 3041760873378113572, URL `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`, US/en-US, diaria 02:00 EST, última 26 nov 02:02: 28.078 aceptados, 0 fallos (la lista marca 44 con aviso).

**Causa:** el Worker solo sirve un TSV fijo de R2 (`pinterest/pinterest_unified_all_markets.tsv`, generado en mayo; SHA y filas fijos en `wrangler.deploy.toml`). No hay proceso que lo regenere. Pinterest lo reingiere cada día sin error, así que re-publica datos de mayo.

Comparación del TSV con Shopify hoy (`28.122` filas, 223 grupos):
- 16 grupos ya no activos o borrados (1.668 filas: 1.110 inactivas, 558 inexistentes).
- 121 de 328 productos activos no están.
- Filas US (4.687): 2.812 con precio **menor** que la tienda, 3 mayor, 278 no activas, 1.594 iguales. Es información de precio falsa para el comprador.

Otras 3 fuentes URL del mismo Worker (210 filas cada una, ingeridas 25-26 nov; creadas para anuncios, ya terminados): `3041760893334979315` (ES), `DLM US Paid Parent Collection Intent 2026-05-20`, `DLM US Paid Parent Isolated 2026-05-21` (IDs de las dos últimas: leer en su ficha antes de actuar). Su contenido frente a Shopify no se comparó.
`dresslikemommy.com` 3041760916127467912 ya está en pausa.

## 5 suéteres/conjuntos activados hoy
Ya están en Pinterest por la app de Shopify: filtro por 5 item ID (1.ª variante de cada uno) = 64 resultados entre fuentes. La tabla de Pinterest no pintó filas, así que no se leyó cuál fuente contiene cuál. **No** entrarán solos en el feed de Cloudflare, ni siquiera tras "arreglar" el Worker, salvo que alguien lo regenere.

## Arreglo recomendado (A): pausar las 4 fuentes del Worker
Motivo: duplican a la app de Shopify, que ya está al día; regenerar crea otro archivo que vuelve a envejecer.

Paso 0 (condición, sin escritura): comprobar en el archivo de la fuente `Shopify (US, en)` que las variantes comparten `item_group_id` y qué `image_link` usan (muestra: 9584752984161 Double Heart, 2 colores). Hoy NO verificado: exige descargar el archivo desde Pinterest (permiso de Frank). La guarda local no lee esa fuente. Si usa foto de variante en vez de la del padre, no cumple la regla del repo: parar y decidir; no cambiar el mapeo sin aprobación.

Estado antes: 4 fuentes activas (principal 28.078 + 210 x 3); total catálogo mostrado 174.225 productos. Antes de pausar, guardar captura de Data sources y comprobar en Product groups qué grupos usan estas fuentes y si sus Pins orgánicos traen tráfico (no medido).

Cambio: Pinterest > Catalogs > Data sources > abrir cada fuente > Manage ingestion > Pause. Primero solo la principal. No borrar. Sin cambios en Shopify ni Cloudflare.

Relectura (inmediata y tras 24-48 h): fuente en "Paused", sin ingesta 02:00; fuentes Shopify siguen "Completed"; el total baja o no (desconocido si pausar retira los productos ya ingeridos; si siguen, la alternativa es borrar la fuente, irreversible, decisión aparte); filtro por los 5 item ID sigue > 0.

Vuelta atrás: Manage ingestion > Resume en la misma fuente; la URL y el Worker no cambian.

## Alternativa (B): regenerar el TSV (no recomendada)
`python3.13 ops/scripts/generate_pinterest_feed_grouped.py` (image_link y link del padre, item_group_id obligatorio) + `build_pinterest_unified_feed.py`; `check_pinterest_feed_grouping.py --strict`; subir a R2 `dlm-pinterest-feeds/<clave>`, actualizar SHA/filas en `wrangler.deploy.toml`, `wrangler deploy`. Rollback: volver a subir el TSV de `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/` y SHA anterior. Pros: mantiene imagen del padre. Contras: escritura Cloudflare, duplicado, sin refresco automático. No probado hoy.

## Guarda
`check_pinterest_feed_grouping.py --strict` hoy: 10 instantáneas locales, 0 FAIL, 3 WARN, 0 ERROR. TSV alojado: 0 filas sin item_group_id.

Login de Frank: no hace falta (sesión activa).
