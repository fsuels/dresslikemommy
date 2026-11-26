# Calidad — verificacion independiente 3 (promesas), 2026-11-26T13:34Z (solo lectura, EE. UU., escritorio)

Commits en origin/main revisados: 85862c9, bec4b2e (posteriores: 16849d8). Carrito de prueba vaciado (0).

## 1. Promesas en vivo (en, es, de, it, fr; portada, ficha, carrito, secure-payments, FAQ, About, Company information, devoluciones, guia de tallas: 45 lecturas): FALLA (1 resto)
- PASA: cifra de familias y año de fundacion: 0 apariciones (texto, titulos y metas; JSON-LD de portada y About tambien). Textos del tema sin envio expres ni "plazo exacto antes de pagar". secure-payments reescrita y generica. Guia de tallas sin consejo de talla mayor en pijamas.
- Texto nuevo ("Estimated delivery is shown on each product page; estimates are not guarantees") no promete mas que la politica. Sigue pendiente de antes: ninguna politica menciona los 12–16 dias.
- FALLA: la pagina /cart incrusta la politica de envio en un bloque desplegable y ahi sigue, en los 5 idiomas, "Checkout shows the exact method, any express upgrade and its price before payment" (en es: "cualquier mejora expres"). Es texto de la politica legal: lo decide Frank (propuesta ya en policy-proposals-2026-11-26.md).
- Nota: /pages/size-guide (en) conserva "if they are between sizes, choose the larger one" para niños en general (no solo pijamas); decision del dueño ya anotada.

## 2. Datos estructurados (nordic-yoke, christmas-reindeer es, heart-button): FALLA (solo plazos)
- PASA: marca "Dress Like Mommy", precio = precio minimo y de la primera variante, InStock = disponible, envio 0 USD, devolucion 30 dias a cargo del cliente.
- Preparacion ahora 1–5 (cuadra en numero con la politica).
- FALLA: transito sigue 11–13, asi que los datos dicen 12–18 dias en total y la ficha visible dice 12–16. Ademas la unidad es "DAY" y la politica habla de dias habiles (5 habiles = hasta 7 naturales). Arreglo (tema / decide CEO): o mostrar la misma ventana en la ficha, o ajustar el transito con evidencia, y expresar la preparacion como dias habiles.

## 3. Fecha limite de Navidad: FALLA respecto al peor caso
- En vivo, coherente: ficha "Order by Thu, Dec 3 for estimated Christmas arrival" y "…to arrive by Wed, Dec 23. Not a guarantee."; carrito igual. bec4b2e mantiene el 3 dic.
- Mi calculo: pedido jue 3 dic + 5 dias habiles = sale jue 10; con 13 dias de transito llega 23; con 14 llega jue 24. La cotizacion del transportista usada en las fichas dice 7–14 dias (EE. UU.). Pedido mie 2 dic + habiles = sale 9, +14 = 23.
- El test nuevo fija transito maximo 13, deducido de la propia ventana del tema; la politica no fija transito y la unica evidencia externa llega a 14. Arreglo (subagente de tema): 2 dic, o evidencia de transito <=13.
- Sin evidencia para otros paises; diciembre puede alargarlo.

## Limites
Solo EE. UU. y escritorio; cajon del carrito no abierto; JSON-LD en 3 fichas.
