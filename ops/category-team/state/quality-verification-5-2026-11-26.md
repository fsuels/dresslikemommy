# Verificación 5 (Experto Calidad)

## Tanda 1: correcciones de catálogo (b2f5), 2026-11-26T14:47Z
Método: Admin API solo lectura, 328 activos, EN + 20 traducciones. Variantes/precios comparados con volcado 12:26Z. No cambié nada.

Veredicto: PASA 1 de 7 fichas revisadas contra su fallo (rainbow-stripe), más 4 puntos parciales. 6 FALLOS.

| # | Falla | Fichas / idiomas | Responsable |
|---|---|---|---|
| F1 | Sigue visible la viñeta interna "creado para revisión antes de publicar" | red-tropical-leaf: cs, fr, it, nl; pink-resort-ruffle: cs, fr, nl; green-botanical-ruffle: cs, fr, nl | catálogo |
| F2 | La misma nota en otras fichas (el barrido "solo 5 fugas" no la vio) | ocean-bloom: cs, fr, nl; pink-blue-tulle-skirts: cs, el, fi, nl, ro | catálogo |
| F3 | Viñeta interna "variantes respaldadas por gráfico / fila de la fuente / tabla adjunta" (no existe en EN) | pastel-watercolor, ocean-bloom, pink-blue-tulle-skirts: la mayoría de los 20 idiomas | catálogo |
| F4 | "este borrador" en texto público | sunshine-daisy: el, fi; coastal-blue-stripe: el, fi; red-heart-raglan: fi; golden-daisy: fi | catálogo/idiomas |
| F5 | Encabezados de tabla en inglés duplicados ("Size Chart — …") | ivory-linen y ocean-dot: 20 idiomas; "Size Chart - Volangklänning" en sv (pink-resort, green-botanical) | catálogo |
| F6 | ocean-marble: el texto EN y los alt no avisan que los shorts blancos de la foto no se venden | ocean-marble | catálogo |

PASA: rainbow-stripe (título, titles/meta sin camisa, encabezados, alt; fr solo por vistazo pendiente). ocean-marble rangos y encabezados en 20 idiomas. Frase sv 1688/"Asian sizes" quitada (ivory, ocean-dot) y rangos correctos. Variantes y precios sin cambios; 0 traducciones marcadas outdated (7 fichas).

Menores: letra suelta da "ENem pink palette" (pink-resort), de "BAtmungsaktive" (blue-tie-dye-butterfly). Traducciones con una viñeta o párrafos distintos del EN (p. ej. ivory/ocean-dot sin párrafos; ocean-marble es truncado, item 97). Posible redacción de constructor "respaldado por la tabla" en white-crochet, sky-blue, red-heart-raglan (es).

Límite: búsqueda por frases; F2-F4 son mínimos (puede haber otras redacciones). Escaparate público no revisado (429).

## Tanda 2: idiomas, 2026-11-26T15:07Z
Método: Admin API solo lectura; 59 fichas por idioma (it 43) para cifras y fallos anteriores; lectura de muestras nuevas (8 en it/es/de/cs, 6 en los otros ocho = 80 lecturas). No cambié nada. Escaparate público no revisado.

Pasa en el conjunto: 0 traducciones outdated, metatítulos <=70, tablas sin cifras cambiadas, y no reaparecen los fallos anteriores en it, es, de, cs (letras sueltas buscadas, gemelos, Zwillinge, du).

| Idioma | Muestra OK | Veredicto | Fallos de la muestra |
|---|---|---|---|
| it | 6/8 | FALLA | autumn-woodland-bunny "Edettagli elevati"; eucalyptus-bunny "Gamma di dimensioni" y "mantiene il freddo" (dice lo contrario que EN "keeps the chill off") |
| es | 6/8 | FALLA | eucalyptus "Nuestro conejito de eucalipto Gasa Pijamas", "sin atajos para camisetas"; ocean-bloom "Niñas de 4 años a niños de 9 a 10" |
| de | 7/8 | FALLA | bamboo-panda "tosenden Babypandas" (rugientes), "Mutter & Passform für Tochter" |
| cs | 6/8 | FALLA | polar-adventure "maminku a já", "Vyhovujte každému okamžiku", "2Y... matka S", texto automático; panda MD "z měkký bavlněný úplet" (en 6 fichas: happy-faces, hooray-sun, make-life-sweet, one-big-star, panda, scribble-heart) |
| fr | 5/6 | FALLA | coral-blossom "Volants aux épaules froides"; además "jumelage/jumelée" en autumn-bunny, bamboo-panda, polar-adventure |
| nl | 5/6 | FALLA | cream-heart "hartvormige gebreide vesten" (vestidos con forma de corazón), "garanderen" mal construido |
| pl | 5/6 | FALLA | eucalyptus "dla mamy i dla mnie", "schłodzić do prasowania", "miękka jak maślana" |
| sv | 4/6 | FALLA | eucalyptus "Care:" en inglés, "Mother S", "E byxa"; red-heart-raglan nota interna "Källans väljare... förblir olistade" |
| da | 4/6 | FALLA | ocean-bloom nota interna "ikke synligt fra det leverede bevis"; coral "kolde skuldre" |
| no | 4/6 | FALLA | coral "Utskrift", "kalde skulder"; polar-adventure "gasbind" (venda), "mamma-og-meg", "Eenkel", "2Y" |
| fi | 4/6 | FALLA | we-are-family título "jouluset pyjamat" (3 fichas plaid/we-are-family); red-heart-sweaters "Pehmeä neule sekoitus", "Kokoluokka... V", "neulosta" |
| ro | 5/6 | FALLA | cream-heart "Mama și Eu", "cardigane tricotate cu inimă asortate drăguțe" |

Total: 61/80 lecturas OK, 19 con fallo; 12 idiomas FALLAN.

Fallo grave fuera de la muestra (catálogo + idiomas):
- red-heart-raglan: viñeta interna "selector de la fuente / valores sin listar" o "datos verificados del producto" en cs, da, es, fi, nl, no, pl, ro, sv (EN ya no la tiene; no revisé los otros idiomas).
- da: nota interna "la composición no era visible en la evidencia aportada" (ocean-bloom, red-tropical-leaf, pink-resort, green-botanical, sunlit-tropical, coastal-stripe, pastel-watercolor, willow-wildflower y varias tops).

Patrón: las descripciones largas antiguas (eucalyptus, polar-adventure, bamboo-panda, autumn-bunny, cream-heart, coral-blossom) siguen en traducción automática; conviene reescribirlas enteras en los 12 idiomas.

Dudas declaradas: rumano "asortate" es correcto, mantener. sv/da/no "matchande/matchende" y collegetröjor/collegegensere aceptables. Finés: "yhteensopivat" suena a compatibilidad técnica y "koissa/kooissa" es dudoso; recomiendo "samanlaiset" y revisión nativa (juicio mío, no es FALLA).
EN (origen): cardigans descritos como "knit sweater" en navy-pearl y red-cable. Menor preexistente: nl eucalyptus fila Mama L sin lbs.
Nota: en esta lectura ocean-bloom ya no mostraba la viñeta "respaldada por gráfico" en it/es (parece en corrección); la tanda 1 se reverificará con la línea del Log.

## Tanda 3: reverificación de v5-fixes (log 21:30Z), 2026-11-26T15:26Z
Admin API solo lectura, datos frescos; no cambié nada; escaparate no revisado.

PASAN 12: V5-1, 2, 3, 5, 6, 9, 12, 15, 16, 18, 19, 20 (V5-20 salvo denim-blue da, declarado pendiente). Frases nuevas de coral, cream-heart, bamboo, polar no, ocean-bloom leídas: correctas.

SIGUEN EN FALLA 8:
- V5-4: golden-daisy y sunshine-daisy fi, "tässä luonnoksessa" (borrador).
- V5-7: it autumn-bunny "Edettagli"; eucalyptus "Gamma di dimensioni", "mantiene il freddo".
- V5-8: es eucalyptus (3 frases sin cambio). ocean-bloom pasa.
- V5-10: cs polar-adventure "Koordinační sady" (resto corregido; "z měkký" pasa).
- V5-11: fr autumn-bunny "jumelage familial". Coral pasa.
- V5-13: pl eucalyptus (3 frases sin cambio).
- V5-14: sv eucalyptus "Care:", "Mother S/XL", "E byxa". Raglan pasa.
- V5-17: fi red-heart-sweaters "Kokoluokka", MD "neulosta". Título joulupyjamat pasa.
Eucalyptus, autumn-bunny y polar parecen fichas excluidas por item 98/99: necesitan dueño.

Nuevo, visto en el barrido:
- N1: ar ocean-marble, blue-stripe-shirts, red-stripe-tops: viñeta "respaldado por la tabla del vendedor adjunta" (nombra al vendedor). ocean-marble además "selector respaldado por gráfico" en cs, da, de, hi, ko.
- N2: cs sunlit-tropical-bloom "S Rozsah velikostí ... přiloženou zdrojovou tabulkou" (letra suelta + nota de fuente); el similar.
Declarado pendiente por el subagente (no reprobado aquí): denim-blue, blue-daisy-skirted, red-tropical-leaf sin línea de tela, bamboo-panda truncado.

## Tanda 4: reverificación de v5-fixes 2 (log 22:30Z), 2026-11-26T15:28Z
Admin API solo lectura; no cambié nada; escaparate no revisado.
PASAN: V5-10 (cs polar, "Koordinační" quitado en polar); bamboo-panda-cotton estructura de bloques igual a EN en 20 idiomas; red-tropical-leaf línea de tela en 20 idiomas; 0 outdated y cifras de tablas iguales en las fichas revisadas (en árabe "2 años" va en palabras).
SIGUE: denim-blue con nota de panel/informe/"gráfico del vendedor" en ar, he, hi, ja, ko (declarado pendiente; ar nombra al vendedor; hi, ja, ko, pt-BR además con una viñeta menos); blue-daisy-skirted menciona selector/tabla adjunta al menos en ar, ja, ko, ru.
Menor: bamboo cs conserva "Koordinační spánkové sady"; polar con un párrafo menos que EN en 11 idiomas (no reclamado).
SIN CORRECCIÓN REGISTRADA (siguen en FALLA desde tanda 3): V5-4, 7, 8, 11, 13, 14, 17, 21, 22. autumn-woodland-bunny y eucalyptus-bunny esperan la línea del otro agente.

## Tanda 5: reverificación de v5-fixes 3 y 4 correcciones de fotos, 2026-11-26T15:40Z
Admin API solo lectura; fotos vistas en el navegador integrado (CDN público); no cambié nada; escaparate público no revisado.

Texto: PASAN 9 de 10 (V5-7, 8, 11, 13, 14, 17, 21, 22, 23).
FALLA V5-4: golden-daisy fi sigue con "tässä luonnoksessa" (este borrador) y fi + nl muestran códigos internos YC8970/YC8971; sunshine-daisy fi sigue con "tässä luonnoksessa". (En la tanda 3 y en el registro se dio por limpio: mi búsqueda de entonces sobre las 61 fichas no incluía estas dos.)

Fotos: PASAN 4 de 4.
- Hooray Sun: foto crema muestra adulto HOORAY y niño con sol; variantes enlazadas a su color.
- Argyle Wool: gris y rojo con foto propia coherente; cada color/talla enlazado a su foto.
- Cárdigan de rayas: primera foto limpia (la familiar sigue segunda; es solo reordenación).
- Camisetas corazón: textos comprobados coinciden; menor: foto 6 (blanca) dice "vibrant colors". Variantes siguen igual.

Nuevo (barrido de 328 fichas):
- V5-24 (idiomas, cs): letra suelta "S Rozsah velikostí" en 47 fichas.
- V5-25 (catálogo/idiomas): texto de proveedor/"tabla adjunta" en 13 fichas: cable-horse, red-plaid, playful-graphic, geometric-blue, coastal-blue-stripe, willow-wildflower, sunlit-floral (ar y en parte de/el); seaside-blue-plaid, fresh-blue-plaid, fluttering-butterflies (el/fi); scarlet-blossom (ko); blue-apricot-heart y black-white-spelling ("tabla adjunta" en 16-17 idiomas). Mínimo; búsqueda por frases.
- V5-26 (idiomas): no eucalyptus "avkjøl strykejernet" (enfríe la plancha; EN "cool iron").
Dudas del subagente: es "sin conformarse con una camiseta" y no "loungetøy" aceptables; ja/ko/he/hi sin nota interna detectada, naturalidad no evaluada; bamboo sv/da/no sigue declarado pendiente. Menor: fi red-heart "Kokoluokka" (mejor "Kokovalikoima").
