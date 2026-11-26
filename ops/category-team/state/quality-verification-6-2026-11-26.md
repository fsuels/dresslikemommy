# Verificación 6 (Experto Calidad), 2026-11-26T16:23Z
Método: archivos de origin/main (791538e); script del aviso ejecutado en Node con los 21 idiomas y la ventana de entrega de cada locale; pruebas del repo 24/24; lectura de los textos; lecturas públicas mínimas (portada en, colección navideña ro, estados HTTP). Solo lectura; no cambié nada.

## 1. Aviso de fecha límite (2a06517): PASA 5 de 6, 1 FALLA
- PASA: 21/21 dicen estimada/esperada y ninguna promete llegada.
- PASA: 21/21 calculan miércoles 2 dic 2026 (23 dic menos 21 días) con día de la semana correcto en cada idioma; visible del 18 nov al 2 dic, oculto el 3.
- PASA en vivo: portada en "Order by Wed, Dec 2 for estimated Christmas arrival" con enlace a matching-family-christmas-outfits (200); /ro muestra la frase.
- PASA naturalidad en 20 (juicio no nativo; pl "aby otrzymać szacowaną dostawę" algo rígido, aceptable).
- FALLA T6-1: ro "Comandă până mie., 2 dec. pentru..." falta preposición ("până pe" / "cel târziu").
- Menor: en 2027 el hueco se reserva desde el 1 nov pero la frase sale el 18.

## 2. Portada por fechas (ef42cfb, 62adbe5, 25837d8): PASA lo demás, 3 FALLAN
- PASA: tres ediciones completas en 21 idiomas; sin promesas de envío, stock ni llegada; no aparece la marca en estos textos.
- PASA: botones a family-sweaters, matching-family-christmas-outfits, matching-family-sweatshirts, valentines-day-matching-outfits-1, mommy-and-me: existen, con productos activos y 200.
- PASA fechas: 2/3 dic, 25/26 dic, 31 dic/1 ene, 10/11 ene, 14 feb; hora de la tienda; fotos navideñas solo hasta 25 dic.
- FALLA T6-2: pt usa "Dia dos Namorados" (en Brasil es el 12 de junio) en antetítulo, titular y botón de San Valentín; usar "Dia de São Valentim".
- FALLA T6-3: ro invierno "zile călduroase acasă" significa días calurosos; usar "zile confortabile acasă".
- FALLA T6-4: desde el 15 feb (hasta el 15 oct) la condición no entra y vuelve la edición "Halloween & Winter" ("Spooky nights..."); index.json sigue en halloween_winter. Resolver antes del 15 feb.
- No visto en vivo: las ediciones futuras (solo con "Preview date" del editor).

## 3. Reverificación: PASAN 2 de 2
V5-4: golden-daisy y sunshine-daisy sin "borrador" ni códigos YC (20 idiomas). V5-26: no eucalyptus "stryk på lav varme". 0 outdated.
Menor visto: sunshine-daisy tiene 9 viñetas en nl y no frente a 10 en EN; golden-daisy no 9 frente a 10.
V5-24 y V5-25 esperan a Frank; no reabiertos.
