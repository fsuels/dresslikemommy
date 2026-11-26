# Calidad — promesas al cliente (en y es), 2026-11-26T13:05Z

Solo lectura. Fuentes: 6 politicas publicas en y es, paginas publicadas (API), textos del tema en origin/main, perfil de envio y descuentos (API), lecturas publicas espaciadas (inicio, ficha, carrito antes, ficha con ?country=GB/DE/IT/AU). Politicas legales: solo propongo; decide Frank.

## GRAVE
G1. Envio expres que no existe. Ficha ("Express upgrades and exact carrier options are shown before payment", "Express options may be available…"), cadenas de carrito, politica de envio, pagina de envio y FAQ ("any express upgrade"). El unico perfil de envio tiene un solo metodo, "Free Standard Shipping" (ambas zonas). Arreglo: quitar las menciones del tema (en 20 idiomas); en politicas, Frank decide quitarlas.
G2. "La estimacion exacta de entrega aparece antes de pagar" (cadena de carrito "exact delivery estimate… show before payment"; variantes en ficha/envio). El metodo de envio no tiene descripcion ni plazo (API); no abri el checkout hoy. Arreglo: añadir descripcion "Estimated 12–16 days" a la tarifa o cambiar el texto.
G3. Pagina /pages/secure-payments (publicada, indexable, no enlazada en el pie), en y es: "usamos PayPal para procesar todos los pagos", solo PayPal/tarjetas, "todos los pedidos en USD", selector de "Reference Currency". Contradice checkout de Shopify, varias monedas y metodos. Arreglo: despublicar o redirigir a /pages/faqs.
G4. Prueba social sin respaldo y fechas que chocan: portada (en/es) "8,000+ families since 2017"; About y Company information "since 2016". No hay en los archivos prueba de 8.000 (la API solo muestra pedidos recientes: 102). Arreglo: Frank confirma cifra y año con datos de Shopify, o se quita.
G5. Telefono: las versiones ES (politicas de reembolso, privacidad, terminos y contacto; paginas contact-us y company-information, marcadas desactualizadas) publican (786) 309-6006 L–V 9–17 ET e invitan a llamar; las versiones EN solo dan email (salvo Legal notice). Arreglo: Frank decide si hay telefono; igualar en y es (y revisar los otros idiomas).

## MEDIO
M1. Plazos. La politica solo promete preparar en <=5 dias habiles (habitual ~3) y no da transito; ficha, carrito y datos estructurados prometen 12–16 dias para todos los paises, y los datos estructurados declaran preparacion 1–3 (contradice 5 habiles). Evidencia de transito en el repo solo para EE. UU. (calculadora: 7–14 dias): peor caso 7 naturales + 14 = 21 > 16. Para GB, DE, IT y AU no hallo evidencia que respalde 12–16. Arreglo: preparacion 1–5 habiles en datos estructurados; confirmar transito por pais y mostrar rango propio.
M2. Navidad 3 dic. Aritmetica del tema: 3 dic + (16+4) = 23 dic, igual en US, GB, DE, IT, AU (data-max-days=20). Con 5 habiles (10 dic) + 14 de transito EE. UU. = 24 dic, un dia tarde en el peor caso, y en diciembre la politica avisa de mas retrasos; otros paises sin evidencia. Dice "not a guarantee". Arreglo: adelantar a 1 dic o confirmar plazos.
M3. Size guide: "Between sizes for pajamas…? Size up for comfort" y "more [ease] for… pajamas"; contradice la decision de hoy de no aconsejar holgura en pijama infantil (a2f6ff0). Revisar tambien guias del blog que dicen "consider sizing up". Arreglo: limitar el consejo a adultos.

## BAJO
B1. Pagina "frontpage" publicada: "The largest selection… premium quality" (sin respaldo). "popular-searches": lista de palabras clave. Despublicar.
B2. /pages/size-chart (2019): tabla generica de mujer que contradice "las tallas cambian por producto". Despublicar.
B3. El descuento automatico "3a pieza 20%" no combina con WELCOME10 ni FAMILY10; FAQ solo dice "un codigo por pedido". Aclarar.
B4. Cadenas sin uso visible hoy con "Best-selling family looks" / "Dress best sellers" / "Trending now" y texto de portada "express options shown at checkout" en la configuracion: no los vi renderizados; quitar para que no reaparezcan.

## Tabla de promesas
| Promesa | Valor | Donde | Estado |
|---|---|---|---|
| Preparacion | <=5 dias habiles, ~3 | politica envio, terminos, pagina envio, FAQ | coherente entre si; datos estructurados 1–3 (M1) |
| Entrega | 12–16 dias (todos los paises) | ficha, carrito, datos estructurados | no esta en politicas (M1) |
| Navidad | pedir hasta 3 dic, llega 23 dic, sin garantia | ficha, carrito | M2 |
| Coste envio | estandar incluido | barra, ficha, carrito, politicas, About, FAQ | coherente; tarifa 0 en API |
| Expres | "disponible en checkout" | ficha, carrito, politicas, FAQ | falso hoy (G1) |
| Devolucion | 30 dias desde entrega; enviar en 14 dias tras autorizacion; sin usar y con etiquetas | politica, pagina, FAQ, ficha | coherente (la pagina de devoluciones omite los 14 dias) |
| Quien paga devolucion | cliente, salvo error o daño | politica, pagina, FAQ, ficha, datos estructurados | coherente |
| Exclusiones | bano/intimo sin sello, Final Sale, regalo | politica, pagina, ficha | coherente |
| Daño | avisar idealmente en 7 dias | todas | coherente |
| Cambios | pedido nuevo + reembolso del original | politica, pagina, FAQ | coherente |
| Reembolso | 5–10 dias habiles + banco 2–5 | politica, pagina, FAQ | coherente |
| UE/RU y Australia | 14 dias desistimiento / garantias ACL | politica, pagina | coherente |
| Cancelacion | idealmente 24 h, antes de preparacion | politica, pagina, FAQ | coherente |
| Retraso | aviso antes de 5 habiles, cancelar con reembolso en 7 dias habiles | politica, terminos | coherente |
| Perdido | 15 habiles sin movimiento o 30 dias; entregado: 14 dias | politica, paginas | coherente |
| Aduanas | a cargo del cliente fuera de EE. UU. salvo que checkout diga lo contrario | politica, terminos, FAQ, ficha | coherente |
| Origen | online; fabricado/enviado por socios, muchos/la mayoria en el extranjero | politicas, About, FAQ, envio | coherente; sin tienda ni almacen propio |
| Atencion | email, ~1 dia habil (L–V) | todas | telefono solo en ES y Legal notice (G5) |
| Descuentos | 10% newsletter (WELCOME10 existe); 3a pieza 20% (activo); REVIEW10 existe | pie, FAQ, barra, nota de resenas | B3 |

## Sin hallazgos
No vi afirmaciones de stock, almacen local, envio rapido (la meta de /collections/all ya es neutra), certificaciones ni tienda fisica en las paginas leidas.

## No verificado
Correos de notificacion (la API no los expone); checkout no abierto hoy; resto de idiomas; reseñas de la app; textos del blog.
