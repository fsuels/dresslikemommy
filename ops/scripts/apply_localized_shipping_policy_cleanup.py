#!/usr/bin/env python3
"""Apply approved localized Shipping Policy / Shipping Info translation cleanup.

Scope is intentionally narrow:
- Shopify Admin translations only.
- Resources: Shipping Policy and Shipping Info page body copy.
- Locales: es, it, ro, pt-BR.
- No theme publish, product data, shipping-rate, market, feed, ad, checkout, or
  order changes.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 90
DEFAULT_ARTIFACT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-07-shipping-policy-copy-repair-applied/localized-policy-page-cleanup"
)

SHIPPING_POLICY_ID = "gid://shopify/ShopPolicy/29845782625"
SHIPPING_INFO_PAGE_ID = "gid://shopify/Page/86424617057"
TARGET_LOCALES = ["es", "it", "ro", "pt-BR"]

PUBLIC_URLS = [
    ("shipping_policy_en", "https://www.dresslikemommy.com/policies/shipping-policy"),
    ("shipping_info_en", "https://www.dresslikemommy.com/pages/shipping-info"),
    ("shipping_policy_es", "https://www.dresslikemommy.com/es/policies/shipping-policy"),
    ("shipping_info_es", "https://www.dresslikemommy.com/es/pages/shipping-info"),
    ("shipping_policy_it", "https://www.dresslikemommy.com/it/policies/shipping-policy"),
    ("shipping_info_it", "https://www.dresslikemommy.com/it/pages/shipping-info"),
    ("shipping_policy_ro", "https://www.dresslikemommy.com/ro/policies/shipping-policy"),
    ("shipping_info_ro", "https://www.dresslikemommy.com/ro/pages/shipping-info"),
    ("shipping_policy_pt", "https://www.dresslikemommy.com/pt/policies/shipping-policy"),
    ("shipping_info_pt", "https://www.dresslikemommy.com/pt/pages/shipping-info"),
]

BLOCKER_PHRASES = [
    "we currently ship to",
    "we ship to the united states, canada, united kingdom, and australia",
    "don't see your country",
    "don\u2019t see your country",
    "families worldwide",
    "all prices are in usd unless",
    "currently ship to:",
    "currently ship to",
    "ship to the united states",
    "familias de todo el mundo",
    "env\u00edo gratis en cada pedido",
    "actualmente enviamos a",
    "no ves tu pa\u00eds",
    "famiglie di tutto il mondo",
    "spedizione gratuita per ogni ordine",
    "attualmente spediamo a",
    "non riesci a trovare il tuo paese",
    "familii din \u00eentreaga lume",
    "livrare gratuit\u0103 la fiecare comand",
    "\u00een prezent expediem c\u0103tre",
    "fam\u00edlias em todo o mundo",
    "frete gr\u00e1tis em todos os pedidos",
    "atualmente enviamos para",
    "physical store",
    "brick-and-mortar",
    "warehouse inventory",
    "local inventory",
    "in-store pickup",
    "método estándar gratuito",
    "metodo standard gratuito",
    "metodă standard gratuită",
    "método padrão grátis",
    "inventario local",
    "tienda f\u00edsica",
    "inventario fisico",
    "negozio fisico",
    "inventar fizic",
    "magazin fizic",
    "loja f\u00edsica",
]

GOOD_PHRASES = {
    "es": [
        "pa\u00eds/regi\u00f3n y la direcci\u00f3n introducidos en el checkout",
        "m\u00e9todos y tarifas de env\u00edo disponibles se muestran en el checkout",
    ],
    "it": [
        "paese/regione e dall'indirizzo inseriti al checkout",
        "metodi e tariffe di spedizione disponibili sono mostrati al checkout",
    ],
    "ro": [
        "\u021bara/regiunea \u0219i adresa introduse la checkout",
        "metodele \u0219i tarifele de livrare disponibile sunt afi\u0219ate la checkout",
    ],
    "pt-BR": [
        "pa\u00eds/regi\u00e3o e do endere\u00e7o informados no checkout",
        "m\u00e9todos e tarifas de envio dispon\u00edveis aparecem no checkout",
    ],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def clean_text(value: str) -> str:
    text = re.sub(r"(?is)<(script|style|noscript|svg).*?</\1>", " ", value or "")
    match = re.search(r"(?is)<main\b[^>]*>(.*?)</main>", text)
    if match:
        text = match.group(1)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def blocker_hits(value: str) -> list[str]:
    haystack = clean_text(value).lower()
    return [phrase for phrase in BLOCKER_PHRASES if phrase in haystack]


def good_hits(value: str, locale: str) -> list[str]:
    haystack = clean_text(value).lower()
    return [phrase for phrase in GOOD_PHRASES.get(locale, []) if phrase.lower() in haystack]


def request_json(
    *,
    method: str,
    url: str,
    token: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
        method=method,
    )
    for attempt in range(5):
        try:
            with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code in {429, 500, 502, 503, 504} and attempt < 4:
                time.sleep(2**attempt)
                continue
            if exc.code == 401:
                raise RuntimeError("Stored Shopify Admin token requires regeneration/reinstall: 401") from exc
            raise RuntimeError(f"Shopify HTTP {exc.code}: {body[:1000]}") from exc
    raise RuntimeError(f"Shopify request failed after retries: {method} {url}")


def graphql(
    *,
    store_domain: str,
    token: str,
    query: str,
    variables: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {"query": query, "variables": variables or {}}
    data = request_json(
        method="POST",
        url=f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json",
        token=token,
        payload=payload,
    )
    if data.get("errors"):
        raise RuntimeError(f"Shopify GraphQL errors: {data['errors']}")
    return data["data"]


def translatable_resource_query() -> str:
    return """
query LocalizedShippingCleanup($policyId: ID!, $pageId: ID!) {
  policy: translatableResource(resourceId: $policyId) {
    resourceId
    translatableContent { key value digest locale }
    es: translations(locale: "es") { key value outdated locale }
    it: translations(locale: "it") { key value outdated locale }
    ro: translations(locale: "ro") { key value outdated locale }
    ptbr: translations(locale: "pt-BR") { key value outdated locale }
  }
  page: translatableResource(resourceId: $pageId) {
    resourceId
    translatableContent { key value digest locale }
    es: translations(locale: "es") { key value outdated locale }
    it: translations(locale: "it") { key value outdated locale }
    ro: translations(locale: "ro") { key value outdated locale }
    ptbr: translations(locale: "pt-BR") { key value outdated locale }
  }
  shopLocales { locale primary published }
}
"""


def fetch_resources(store_domain: str, token: str) -> dict[str, Any]:
    return graphql(
        store_domain=store_domain,
        token=token,
        query=translatable_resource_query(),
        variables={"policyId": SHIPPING_POLICY_ID, "pageId": SHIPPING_INFO_PAGE_ID},
    )


def content_digest(resource: dict[str, Any], key: str) -> str:
    for row in resource.get("translatableContent") or []:
        if row.get("key") == key:
            return str(row.get("digest") or "")
    raise RuntimeError(f"Missing digest for key {key}")


def current_translation(resource: dict[str, Any], locale: str, key: str) -> dict[str, Any] | None:
    alias = "ptbr" if locale == "pt-BR" else locale
    for row in resource.get(alias) or []:
        if row.get("key") == key:
            return row
    return None


def register_translations(
    *,
    store_domain: str,
    token: str,
    resource_id: str,
    translations: list[dict[str, str]],
) -> dict[str, Any]:
    mutation = """
mutation RegisterLocalizedShippingTranslations($resourceId: ID!, $translations: [TranslationInput!]!) {
  translationsRegister(resourceId: $resourceId, translations: $translations) {
    translations {
      key
      locale
      outdated
      value
    }
    userErrors {
      field
      message
    }
  }
}
"""
    data = graphql(
        store_domain=store_domain,
        token=token,
        query=mutation,
        variables={"resourceId": resource_id, "translations": translations},
    )["translationsRegister"]
    if data.get("userErrors"):
        raise RuntimeError(json.dumps(data["userErrors"], ensure_ascii=False))
    return data


def public_get(url: str) -> dict[str, Any]:
    req = request.Request(
        url,
        headers={
            "Accept": "text/html,*/*",
            "User-Agent": "DressLikeMommyOps/1.0 (+slow localized policy readback)",
        },
    )
    try:
        with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            return {
                "url": url,
                "final_url": response.geturl(),
                "http_status": response.status,
                "body": response.read().decode("utf-8", errors="replace"),
            }
    except error.HTTPError as exc:
        return {
            "url": url,
            "final_url": exc.geturl(),
            "http_status": exc.code,
            "body": exc.read().decode("utf-8", errors="replace"),
        }


def public_readback(artifact_dir: Path, stage: str, *, delay_seconds: float) -> dict[str, Any]:
    results: dict[str, Any] = {}
    target_dir = artifact_dir / stage
    for index, (key, url) in enumerate(PUBLIC_URLS):
        if index:
            time.sleep(delay_seconds)
        response = public_get(url)
        body = response.get("body") or ""
        write_text(target_dir / f"{key}.html", body)
        locale = key.rsplit("_", 1)[-1]
        if locale == "pt":
            locale = "pt-BR"
        results[key] = {
            "url": url,
            "final_url": response.get("final_url"),
            "http_status": response.get("http_status"),
            "text_excerpt": clean_text(body)[:900],
            "blocker_hits": blocker_hits(body),
            "good_hits": good_hits(body, locale),
        }
        if response.get("http_status") == 429:
            results["_stop_rule"] = {
                "stopped_after": key,
                "reason": "HTTP 429 storefront protection; do not continue probing until cooldown.",
            }
            break
    write_text(target_dir / "readback.json", json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    return results


def policy_copy(locale: str) -> str:
    copies = {
        "es": """<h1>Política de envío</h1>
<p><strong>Última actualización:</strong> 28 de enero de 2026</p>
<p>En <strong>Dress Like Mommy</strong>, queremos que tus conjuntos a juego lleguen con la mayor claridad y fiabilidad posible. Revisa el método de envío, la tarifa y la estimación de entrega que aparecen en el checkout antes de realizar tu pedido.</p>

<h2>Dónde enviamos</h2>
<p>El envío está disponible para los países y regiones que aparecen en el checkout. La disponibilidad depende del destino, del producto y de los métodos de envío mostrados durante el checkout. Usa el selector de país/región o el paso de envío del checkout para confirmar si podemos enviar a tu dirección antes de comprar.</p>
<p>Si tu destino no aparece en el checkout, o si no se muestra ningún método de envío para tu dirección, escríbenos a <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> antes de hacer el pedido.</p>

<h2>Tarifas de envío</h2>
<p>El envío estándar está incluido en los precios de los productos para países y regiones donde haya un método estándar disponible. El checkout muestra el método exacto, la estimación de entrega y cualquier mejora express antes del pago.</p>

<h2>Tiempo de procesamiento</h2>
<p>Los pedidos se procesan en 1-3 días laborables después de la confirmación del pago. Durante festivos, promociones o periodos de mucho volumen, el procesamiento puede tardar 1-2 días laborables adicionales.</p>
<p>Recibirás un correo electrónico con la información de seguimiento cuando tu pedido se envíe.</p>

<h2>Plazos de entrega</h2>
<p>Las estimaciones de entrega varían según el destino, el transportista, el procesamiento aduanero y el método de envío mostrado en el checkout.</p>
<ul>
  <li><strong>Entrega estándar:</strong> la estimación actual del checkout se muestra antes del pago.</li>
  <li><strong>Entrega express:</strong> disponible para algunos destinos cuando aparece en el checkout.</li>
</ul>
<p>Son estimaciones. Los plazos reales pueden variar por aduanas, retrasos del transportista, clima, festivos o condiciones locales.</p>

<h2>Cómo funciona nuestro envío</h2>
<ol>
  <li><strong>Pedido realizado:</strong> recibes un correo de confirmación.</li>
  <li><strong>Procesamiento:</strong> tu pedido se prepara después de confirmar el pago.</li>
  <li><strong>Enviado:</strong> te enviamos el seguimiento cuando esté disponible.</li>
  <li><strong>En tránsito:</strong> usa el enlace de seguimiento para ver las actualizaciones del transportista.</li>
  <li><strong>Entregado:</strong> el paquete llega a la dirección indicada en el checkout.</li>
</ol>

<h2>Seguimiento del pedido</h2>
<p>Cada pedido incluye un número de seguimiento cuando el transportista lo proporciona. El seguimiento puede tardar 24-48 horas en actualizarse después de emitirse.</p>

<h2>Aduanas, aranceles e impuestos de importación</h2>
<p>Para pedidos enviados fuera de Estados Unidos, el país de destino o el transportista puede cobrar aranceles de importación, impuestos, gastos de gestión o cargos aduaneros. Estos cargos son responsabilidad del cliente salvo que el checkout indique explícitamente que están incluidos.</p>
<p>No podemos predecir estos cargos, marcar pedidos como regalo ni reducir el valor declarado de un pedido. Consulta con la oficina de aduanas local antes de comprar.</p>

<h2>Problemas de envío</h2>
<p>Si tu paquete se retrasa, falta o aparece como entregado pero no lo recibiste, escríbenos a <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> con tu número de pedido y seguimiento. Te ayudaremos a revisar la información del transportista y los próximos pasos disponibles.</p>

<h2>Contacto</h2>
<p>Para preguntas de envío, escribe a <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>.</p>
""",
        "it": """<h1>Politica di spedizione</h1>
<p><strong>Ultimo aggiornamento:</strong> 28 gennaio 2026</p>
<p>Da <strong>Dress Like Mommy</strong>, vogliamo che i tuoi outfit coordinati arrivino nel modo più chiaro e affidabile possibile. Controlla il metodo di spedizione, la tariffa e la stima di consegna mostrati al checkout prima di completare l'ordine.</p>

<h2>Dove spediamo</h2>
<p>La spedizione è disponibile per i paesi e le regioni mostrati al checkout. La disponibilità dipende dalla destinazione, dal prodotto e dai metodi di spedizione mostrati durante il checkout. Usa il selettore paese/regione o la fase di spedizione al checkout per confermare se possiamo spedire al tuo indirizzo prima di ordinare.</p>
<p>Se la tua destinazione non appare al checkout, o se non viene mostrato alcun metodo di spedizione per il tuo indirizzo, contattaci a <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> prima di ordinare.</p>

<h2>Tariffe di spedizione</h2>
<p>La spedizione standard è inclusa nei prezzi dei prodotti per paesi e regioni in cui è disponibile un metodo standard. Il checkout mostra il metodo esatto, la stima di consegna ed eventuali upgrade express prima del pagamento.</p>

<h2>Tempo di elaborazione</h2>
<p>Gli ordini vengono elaborati entro 1-3 giorni lavorativi dalla conferma del pagamento. Durante festività, promozioni o periodi di alto volume, l'elaborazione può richiedere 1-2 giorni lavorativi aggiuntivi.</p>
<p>Riceverai un'email con le informazioni di tracciamento quando l'ordine verrà spedito.</p>

<h2>Tempi di consegna</h2>
<p>Le stime di consegna variano in base alla destinazione, al corriere, alle procedure doganali e al metodo di spedizione mostrato al checkout.</p>
<ul>
  <li><strong>Consegna standard:</strong> la stima corrente del checkout viene mostrata prima del pagamento.</li>
  <li><strong>Consegna express:</strong> disponibile per alcune destinazioni quando mostrata al checkout.</li>
</ul>
<p>Sono stime. I tempi effettivi possono variare per dogana, ritardi del corriere, meteo, festività o condizioni locali.</p>

<h2>Come funziona la spedizione</h2>
<ol>
  <li><strong>Ordine effettuato:</strong> ricevi un'email di conferma.</li>
  <li><strong>Elaborazione:</strong> l'ordine viene preparato dopo la conferma del pagamento.</li>
  <li><strong>Spedito:</strong> inviamo le informazioni di tracciamento quando disponibili.</li>
  <li><strong>In transito:</strong> usa il link di tracciamento per gli aggiornamenti del corriere.</li>
  <li><strong>Consegnato:</strong> il pacco arriva all'indirizzo inserito al checkout.</li>
</ol>

<h2>Tracciamento dell'ordine</h2>
<p>Ogni ordine include un numero di tracciamento quando il corriere lo fornisce. Il tracciamento può richiedere 24-48 ore per aggiornarsi dopo l'emissione del numero.</p>

<h2>Dogane, dazi e tasse di importazione</h2>
<p>Per ordini spediti fuori dagli Stati Uniti, il paese di destinazione o il corriere può addebitare dazi di importazione, tasse, spese di intermediazione o oneri doganali. Questi costi sono responsabilità del cliente salvo che il checkout indichi esplicitamente che sono inclusi.</p>
<p>Non possiamo prevedere questi costi, contrassegnare ordini come regalo o ridurre il valore dichiarato di un ordine. Contatta l'ufficio doganale locale prima di ordinare.</p>

<h2>Problemi di spedizione</h2>
<p>Se il pacco è in ritardo, mancante o segnato come consegnato ma non ricevuto, contattaci a <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> con numero d'ordine e tracciamento. Ti aiuteremo a controllare le informazioni del corriere e i prossimi passaggi disponibili.</p>

<h2>Contattaci</h2>
<p>Per domande sulla spedizione, scrivi a <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>.</p>
""",
        "ro": """<h1>Politica de livrare</h1>
<p><strong>Ultima actualizare:</strong> 28 ianuarie 2026</p>
<p>La <strong>Dress Like Mommy</strong>, vrem ca ținutele tale asortate să ajungă cât mai clar și fiabil posibil. Verifică metoda de livrare, tariful și estimarea de livrare afișate la checkout înainte de a plasa comanda.</p>

<h2>Unde livrăm</h2>
<p>Livrarea este disponibilă pentru țările și regiunile afișate la checkout. Disponibilitatea depinde de destinație, produs și metodele de livrare afișate în timpul checkout-ului. Folosește selectorul de țară/regiune sau pasul de livrare din checkout pentru a confirma dacă putem livra la adresa ta înainte de comandă.</p>
<p>Dacă destinația ta nu apare la checkout sau nu se afișează nicio metodă de livrare pentru adresa ta, contactează-ne la <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> înainte de comandă.</p>

<h2>Tarife de livrare</h2>
<p>Livrarea standard este inclusă în prețurile produselor pentru țările și regiunile unde este disponibilă o metodă standard. Checkout-ul afișează metoda exactă, estimarea de livrare și orice upgrade express înainte de plată.</p>

<h2>Timp de procesare</h2>
<p>Comenzile sunt procesate în 1-3 zile lucrătoare după confirmarea plății. În perioade de sărbători, promoții sau volum ridicat, procesarea poate dura încă 1-2 zile lucrătoare.</p>
<p>Vei primi un e-mail cu informații de urmărire după expedierea comenzii.</p>

<h2>Termene de livrare</h2>
<p>Estimările de livrare variază în funcție de destinație, transportator, procesarea vamală și metoda de livrare afișată la checkout.</p>
<ul>
  <li><strong>Livrare standard:</strong> estimarea curentă din checkout este afișată înainte de plată.</li>
  <li><strong>Livrare express:</strong> disponibilă pentru unele destinații unde apare la checkout.</li>
</ul>
<p>Acestea sunt estimări. Timpii reali pot varia din cauza vămii, întârzierilor transportatorului, vremii, sărbătorilor sau condițiilor locale.</p>

<h2>Cum funcționează livrarea</h2>
<ol>
  <li><strong>Comandă plasată:</strong> primești un e-mail de confirmare.</li>
  <li><strong>Procesare:</strong> comanda este pregătită după confirmarea plății.</li>
  <li><strong>Expediată:</strong> trimitem informațiile de urmărire când sunt disponibile.</li>
  <li><strong>În tranzit:</strong> folosește linkul de urmărire pentru actualizările transportatorului.</li>
  <li><strong>Livrată:</strong> coletul ajunge la adresa furnizată la checkout.</li>
</ol>

<h2>Urmărirea comenzii</h2>
<p>Fiecare comandă include un număr de urmărire atunci când transportatorul îl furnizează. Urmărirea poate dura 24-48 de ore să se actualizeze după emiterea numărului.</p>

<h2>Vamă, taxe și impozite de import</h2>
<p>Pentru comenzile expediate în afara Statelor Unite, țara de destinație sau transportatorul poate percepe taxe de import, impozite, taxe de brokeraj sau taxe vamale. Aceste costuri sunt responsabilitatea clientului, cu excepția cazului în care checkout-ul spune explicit că sunt incluse.</p>
<p>Nu putem prezice aceste costuri, marca comenzile ca daruri sau reduce valoarea declarată a unei comenzi. Contactează biroul vamal local înainte de comandă.</p>

<h2>Probleme de livrare</h2>
<p>Dacă pachetul tău întârzie, lipsește sau apare ca livrat dar nu a fost primit, contactează-ne la <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> cu numărul comenzii și informațiile de urmărire. Te vom ajuta să verifici informațiile transportatorului și pașii disponibili.</p>

<h2>Contact</h2>
<p>Pentru întrebări despre livrare, scrie la <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>.</p>
""",
        "pt-BR": """<h1>Política de envio</h1>
<p><strong>Última atualização:</strong> 28 de janeiro de 2026</p>
<p>Na <strong>Dress Like Mommy</strong>, queremos que seus looks combinando cheguem com a maior clareza e confiabilidade possível. Confira o método de envio, a tarifa e a estimativa de entrega exibidos no checkout antes de fazer o pedido.</p>

<h2>Para onde enviamos</h2>
<p>O envio está disponível para os países e regiões exibidos no checkout. A disponibilidade depende do destino, do produto e dos métodos de envio mostrados durante o checkout. Use o seletor de país/região ou a etapa de envio do checkout para confirmar se podemos enviar para o seu endereço antes de comprar.</p>
<p>Se o seu destino não aparecer no checkout, ou se nenhum método de envio for exibido para o seu endereço, entre em contato pelo e-mail <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> antes de fazer o pedido.</p>

<h2>Tarifas de envio</h2>
<p>O envio padrão está incluído nos preços dos produtos para países e regiões onde um método padrão está disponível. O checkout mostra o método exato, a estimativa de entrega e qualquer upgrade expresso antes do pagamento.</p>

<h2>Tempo de processamento</h2>
<p>Os pedidos são processados em 1-3 dias úteis após a confirmação do pagamento. Durante feriados, promoções ou períodos de alto volume, o processamento pode levar mais 1-2 dias úteis.</p>
<p>Você receberá um e-mail com as informações de rastreamento quando o pedido for enviado.</p>

<h2>Prazos de entrega</h2>
<p>As estimativas de entrega variam conforme o destino, a transportadora, o processamento alfandegário e o método de envio exibido no checkout.</p>
<ul>
  <li><strong>Entrega padrão:</strong> a estimativa atual do checkout aparece antes do pagamento.</li>
  <li><strong>Entrega expressa:</strong> disponível para alguns destinos quando exibida no checkout.</li>
</ul>
<p>Essas são estimativas. Os prazos reais podem variar por causa da alfândega, atrasos da transportadora, clima, feriados ou condições locais.</p>

<h2>Como funciona o envio</h2>
<ol>
  <li><strong>Pedido feito:</strong> você recebe um e-mail de confirmação.</li>
  <li><strong>Processamento:</strong> seu pedido é preparado após a confirmação do pagamento.</li>
  <li><strong>Enviado:</strong> enviamos as informações de rastreamento quando disponíveis.</li>
  <li><strong>Em trânsito:</strong> use o link de rastreamento para acompanhar as atualizações da transportadora.</li>
  <li><strong>Entregue:</strong> o pacote chega ao endereço informado no checkout.</li>
</ol>

<h2>Rastreamento do pedido</h2>
<p>Cada pedido inclui um número de rastreamento quando a transportadora o fornece. O rastreamento pode levar 24-48 horas para atualizar depois que o número é emitido.</p>

<h2>Alfândega, tributos e impostos de importação</h2>
<p>Para pedidos enviados para fora dos Estados Unidos, o país de destino ou a transportadora pode cobrar tributos de importação, impostos, taxas de intermediação ou encargos alfandegários. Esses custos são responsabilidade do cliente, a menos que o checkout diga explicitamente que estão incluídos.</p>
<p>Não podemos prever esses custos, marcar pedidos como presente ou reduzir o valor declarado de um pedido. Consulte a alfândega local antes de comprar.</p>

<h2>Problemas de envio</h2>
<p>Se o pacote atrasar, estiver faltando ou aparecer como entregue mas não recebido, escreva para <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> com o número do pedido e o rastreamento. Vamos ajudar a revisar as informações da transportadora e os próximos passos disponíveis.</p>

<h2>Contato</h2>
<p>Para dúvidas sobre envio, escreva para <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>.</p>
""",
    }
    return copies[locale]


def page_copy(locale: str) -> str:
    copies = {
        "es": """<h2>Información de envío</h2>
<p>En <strong>Dress Like Mommy</strong>, somos una tienda online que envía conjuntos familiares a juego a los destinos disponibles en el checkout mediante nuestros socios de envío y preparación de pedidos. Así puedes confirmar el envío, los tiempos de entrega y el seguimiento antes de comprar.</p>

<h3>Opciones de envío estándar y express</h3>
<p>El envío estándar está incluido en los precios de los productos para países y regiones donde haya un método estándar disponible. El checkout muestra el método exacto, la estimación de entrega y cualquier mejora express antes del pago.</p>

<h3>Dónde enviamos</h3>
<p>La disponibilidad de envío se basa en el país/región y la dirección introducidos en el checkout. Si el checkout muestra un método de envío para tu dirección, podemos enviar allí bajo el método y la tarifa mostrados.</p>
<p>Si tu destino no aparece en el checkout, o si no se muestra ningún método de envío, escríbenos a <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> antes de hacer el pedido.</p>

<h3>Procesamiento y plazos de entrega</h3>
<p>Los pedidos se procesan en 1-3 días laborables después de la confirmación del pago. Durante festivos, promociones o periodos de mucho volumen, el procesamiento puede tardar 1-2 días laborables adicionales.</p>
<p>Las estimaciones de entrega varían según el destino, el transportista, la aduana y el método de envío mostrado en el checkout. Revisa el método y la estimación durante el checkout antes de comprar.</p>
<p>El seguimiento puede tardar 24-48 horas en actualizarse después de emitirse.</p>

<h3>Seguimiento del pedido</h3>
<p>Cuando tu pedido se envíe, revisa tu correo electrónico para ver la información de seguimiento. También puedes usar el enlace de seguimiento del correo de confirmación de envío cuando esté disponible.</p>

<h3>Aduanas, aranceles e impuestos de importación</h3>
<p>Para pedidos fuera de Estados Unidos, el país de destino o el transportista puede cobrar aranceles de importación, impuestos, gastos de gestión o cargos aduaneros. Estos cargos son responsabilidad del cliente salvo que el checkout indique explícitamente que están incluidos.</p>
<p>No podemos predecir estos cargos, marcar pedidos como regalo ni reducir el valor declarado de un pedido. Consulta con la oficina de aduanas local antes de comprar.</p>
""",
        "it": """<h2>Informazioni sulla spedizione</h2>
<p>Da <strong>Dress Like Mommy</strong>, siamo un negozio online che spedisce outfit coordinati per la famiglia verso le destinazioni disponibili al checkout tramite i nostri partner di spedizione e preparazione ordini. Ecco come confermare spedizione, tempi di consegna e tracciamento prima di ordinare.</p>

<h3>Opzioni di spedizione standard ed express</h3>
<p>La spedizione standard è inclusa nei prezzi dei prodotti per paesi e regioni in cui è disponibile un metodo standard. Il checkout mostra il metodo esatto, la stima di consegna ed eventuali upgrade express prima del pagamento.</p>

<h3>Dove spediamo</h3>
<p>La disponibilità della spedizione dipende dal paese/regione e dall'indirizzo inseriti al checkout. Se il checkout mostra un metodo di spedizione per il tuo indirizzo, possiamo spedire lì con il metodo e la tariffa indicati.</p>
<p>Se la tua destinazione non appare al checkout, o se non viene mostrato alcun metodo di spedizione, scrivici a <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> prima di ordinare.</p>

<h3>Elaborazione e tempi di consegna</h3>
<p>Gli ordini vengono elaborati entro 1-3 giorni lavorativi dalla conferma del pagamento. Durante festività, promozioni o periodi di alto volume, l'elaborazione può richiedere 1-2 giorni lavorativi aggiuntivi.</p>
<p>Le stime di consegna variano in base alla destinazione, al corriere, alle procedure doganali e al metodo di spedizione mostrato al checkout. Controlla metodo e stima durante il checkout prima di ordinare.</p>
<p>Il tracciamento può richiedere 24-48 ore per aggiornarsi dopo l'emissione del numero.</p>

<h3>Tracciamento dell'ordine</h3>
<p>Quando l'ordine viene spedito, controlla la tua email per le informazioni di tracciamento. Puoi anche usare il link di tracciamento nell'email di conferma spedizione quando disponibile.</p>

<h3>Dogane, dazi e tasse di importazione</h3>
<p>Per ordini fuori dagli Stati Uniti, il paese di destinazione o il corriere può addebitare dazi di importazione, tasse, spese di intermediazione o oneri doganali. Questi costi sono responsabilità del cliente salvo che il checkout indichi esplicitamente che sono inclusi.</p>
<p>Non possiamo prevedere questi costi, contrassegnare ordini come regalo o ridurre il valore dichiarato di un ordine. Contatta l'ufficio doganale locale prima di ordinare.</p>
""",
        "ro": """<h2>Informații despre livrare</h2>
<p>La <strong>Dress Like Mommy</strong>, suntem un magazin online care livrează ținute asortate pentru familie către destinațiile disponibile la checkout prin partenerii noștri de livrare și pregătire a comenzilor. Iată cum poți confirma livrarea, timpul estimat și urmărirea înainte de comandă.</p>

<h3>Opțiuni de livrare standard și express</h3>
<p>Livrarea standard este inclusă în prețurile produselor pentru țările și regiunile unde este disponibilă o metodă standard. Checkout-ul afișează metoda exactă, estimarea de livrare și orice upgrade express înainte de plată.</p>

<h3>Unde livrăm</h3>
<p>Disponibilitatea livrării se bazează pe țara/regiunea și adresa introduse la checkout. Dacă checkout-ul afișează o metodă de livrare pentru adresa ta, putem livra acolo folosind metoda și tariful afișate.</p>
<p>Dacă destinația ta nu apare la checkout sau nu se afișează nicio metodă de livrare, scrie-ne la <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> înainte de comandă.</p>

<h3>Procesare și termene de livrare</h3>
<p>Comenzile sunt procesate în 1-3 zile lucrătoare după confirmarea plății. În perioade de sărbători, promoții sau volum ridicat, procesarea poate dura încă 1-2 zile lucrătoare.</p>
<p>Estimările de livrare variază în funcție de destinație, transportator, procesarea vamală și metoda de livrare afișată la checkout. Verifică metoda și estimarea în checkout înainte de comandă.</p>
<p>Urmărirea poate dura 24-48 de ore să se actualizeze după emiterea numărului.</p>

<h3>Urmărirea comenzii</h3>
<p>După expedierea comenzii, verifică e-mailul pentru informațiile de urmărire. Poți folosi și linkul de urmărire din e-mailul de confirmare a expedierii, atunci când este disponibil.</p>

<h3>Vamă, taxe și impozite de import</h3>
<p>Pentru comenzile din afara Statelor Unite, țara de destinație sau transportatorul poate percepe taxe de import, impozite, taxe de brokeraj sau taxe vamale. Aceste costuri sunt responsabilitatea clientului, cu excepția cazului în care checkout-ul spune explicit că sunt incluse.</p>
<p>Nu putem prezice aceste costuri, marca comenzile ca daruri sau reduce valoarea declarată a unei comenzi. Contactează biroul vamal local înainte de comandă.</p>
""",
        "pt-BR": """<h2>Informações de envio</h2>
<p>Na <strong>Dress Like Mommy</strong>, somos uma loja online que envia looks combinando para família aos destinos disponíveis no checkout por meio de nossos parceiros de envio e preparação de pedidos. Veja como confirmar envio, prazo de entrega e rastreamento antes de comprar.</p>

<h3>Opções de envio padrão e expresso</h3>
<p>O envio padrão está incluído nos preços dos produtos para países e regiões onde um método padrão está disponível. O checkout mostra o método exato, a estimativa de entrega e qualquer upgrade expresso antes do pagamento.</p>

<h3>Para onde enviamos</h3>
<p>A disponibilidade de envio depende do país/região e do endereço informados no checkout. Se o checkout mostrar um método de envio para o seu endereço, podemos enviar para lá pelo método e tarifa exibidos.</p>
<p>Se o seu destino não aparecer no checkout, ou se nenhum método de envio for exibido, escreva para <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> antes de fazer o pedido.</p>

<h3>Processamento e prazos de entrega</h3>
<p>Os pedidos são processados em 1-3 dias úteis após a confirmação do pagamento. Durante feriados, promoções ou períodos de alto volume, o processamento pode levar mais 1-2 dias úteis.</p>
<p>As estimativas de entrega variam conforme destino, transportadora, processamento alfandegário e método de envio exibido no checkout. Confira o método e a estimativa no checkout antes de comprar.</p>
<p>O rastreamento pode levar 24-48 horas para atualizar depois que o número é emitido.</p>

<h3>Rastreamento do pedido</h3>
<p>Depois que o pedido for enviado, verifique seu e-mail para as informações de rastreamento. Você também pode usar o link de rastreamento no e-mail de confirmação de envio quando disponível.</p>

<h3>Alfândega, tributos e impostos de importação</h3>
<p>Para pedidos fora dos Estados Unidos, o país de destino ou a transportadora pode cobrar tributos de importação, impostos, taxas de intermediação ou encargos alfandegários. Esses custos são responsabilidade do cliente, a menos que o checkout diga explicitamente que estão incluídos.</p>
<p>Não podemos prever esses custos, marcar pedidos como presente ou reduzir o valor declarado de um pedido. Consulte a alfândega local antes de comprar.</p>
""",
    }
    return copies[locale]


def build_plan(resources: dict[str, Any], artifact_dir: Path) -> dict[str, Any]:
    published_locales = {
        row["locale"]
        for row in resources.get("shopLocales", [])
        if row.get("published") or row.get("primary")
    }
    policy_digest = content_digest(resources["policy"], "body")
    page_digest = content_digest(resources["page"], "body_html")
    targets: list[dict[str, Any]] = []

    for locale in TARGET_LOCALES:
        for resource_key, resource_id, field_key, digest, value in [
            ("shipping_policy", SHIPPING_POLICY_ID, "body", policy_digest, policy_copy(locale)),
            ("shipping_info_page", SHIPPING_INFO_PAGE_ID, "body_html", page_digest, page_copy(locale)),
        ]:
            current = current_translation(resources["policy" if resource_key == "shipping_policy" else "page"], locale, field_key)
            before_value = str((current or {}).get("value") or "")
            target_path = artifact_dir / "target-translations" / resource_key / f"{locale}.html"
            write_text(target_path, value)
            if before_value:
                write_text(artifact_dir / "before-translations" / resource_key / f"{locale}.html", before_value)
            targets.append(
                {
                    "resource": resource_key,
                    "resource_id": resource_id,
                    "locale": locale,
                    "key": field_key,
                    "published_locale": locale in published_locales,
                    "before_exists": bool(current),
                    "before_outdated": (current or {}).get("outdated"),
                    "changed": before_value != value,
                    "before_sha256": sha256_text(before_value),
                    "after_sha256": sha256_text(value),
                    "before_blocker_hits": blocker_hits(before_value),
                    "after_blocker_hits": blocker_hits(value),
                    "after_good_hits": good_hits(value, locale),
                    "translatableContentDigest": digest,
                    "target_artifact": str(target_path),
                }
            )

    plan = {
        "generated_at": utc_now(),
        "resources": {
            "shipping_policy": SHIPPING_POLICY_ID,
            "shipping_info_page": SHIPPING_INFO_PAGE_ID,
        },
        "target_locales": TARGET_LOCALES,
        "published_target_locales": sorted(locale for locale in TARGET_LOCALES if locale in published_locales),
        "targets": targets,
        "blocked_actions": [
            "international campaign import/create/enable/spend",
            "ad budget/bid/status/conversion-goal changes",
            "Merchant upload/feed/product-scope/feed-label/product-group changes",
            "Shopify product data, inventory, shipping-rate, market, checkout, or theme changes",
        ],
    }
    write_text(artifact_dir / "translation_plan.json", json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    return plan


def execute_plan(store_domain: str, token: str, plan: dict[str, Any]) -> dict[str, Any]:
    execution: dict[str, Any] = {"applied": [], "skipped": []}
    for resource_key, resource_id in [
        ("shipping_policy", SHIPPING_POLICY_ID),
        ("shipping_info_page", SHIPPING_INFO_PAGE_ID),
    ]:
        translations = []
        for target in plan["targets"]:
            if target["resource"] != resource_key or not target["changed"]:
                continue
            translations.append(
                {
                    "locale": target["locale"],
                    "key": target["key"],
                    "value": policy_copy(target["locale"]) if resource_key == "shipping_policy" else page_copy(target["locale"]),
                    "translatableContentDigest": target["translatableContentDigest"],
                }
            )
        if translations:
            result = register_translations(
                store_domain=store_domain,
                token=token,
                resource_id=resource_id,
                translations=translations,
            )
            execution["applied"].append(
                {
                    "resource": resource_key,
                    "resource_id": resource_id,
                    "locales": [item["locale"] for item in translations],
                    "result_count": len(result.get("translations") or []),
                }
            )
        else:
            execution["skipped"].append({"resource": resource_key, "reason": "no_changed_translations"})
    return execution


def readback_summary(resources: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for resource_key, resource_name, field_key in [
        ("policy", "shipping_policy", "body"),
        ("page", "shipping_info_page", "body_html"),
    ]:
        summary[resource_name] = {}
        for locale in TARGET_LOCALES:
            row = current_translation(resources[resource_key], locale, field_key) or {}
            value = str(row.get("value") or "")
            summary[resource_name][locale] = {
                "exists": bool(row),
                "outdated": row.get("outdated"),
                "sha256": sha256_text(value),
                "blocker_hits": blocker_hits(value),
                "good_hits": good_hits(value, locale),
                "text_excerpt": clean_text(value)[:500],
            }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--public-only", action="store_true")
    parser.add_argument("--skip-public", action="store_true")
    parser.add_argument("--public-stage", default="")
    parser.add_argument("--public-delay-seconds", type=float, default=12.0)
    parser.add_argument("--cooldown-seconds", type=float, default=0.0)
    parser.add_argument("--approval-note", default="")
    args = parser.parse_args()

    artifact_dir = args.artifact_dir
    artifact_dir.mkdir(parents=True, exist_ok=True)

    if args.cooldown_seconds > 0:
        time.sleep(args.cooldown_seconds)

    if args.public_only:
        stage = args.public_stage or "public-readback"
        public_result = public_readback(artifact_dir, stage, delay_seconds=args.public_delay_seconds)
        print(json.dumps({"public_readback": public_result}, indent=2, ensure_ascii=False))
        return

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    token = load_access_token(args.access_token)
    before_resources = fetch_resources(store_domain, token)
    plan = build_plan(before_resources, artifact_dir)
    before_readback = readback_summary(before_resources)
    execution = {"execute": False, "applied": [], "skipped": []}
    if args.execute:
        execution = {"execute": True, **execute_plan(store_domain, token, plan)}
    after_resources = fetch_resources(store_domain, token)
    after_readback = readback_summary(after_resources)
    public_result = {}
    if not args.skip_public:
        stage = args.public_stage or ("post-public-readback" if args.execute else "dry-run-public-readback")
        public_result = public_readback(artifact_dir, stage, delay_seconds=args.public_delay_seconds)
    result = {
        "generated_at": utc_now(),
        "mode": "execute" if args.execute else "dry-run",
        "approval_note": args.approval_note,
        "store_domain": store_domain,
        "plan_path": str(artifact_dir / "translation_plan.json"),
        "before_admin_translation_readback": before_readback,
        "execution": execution,
        "after_admin_translation_readback": after_readback,
        "public_readback": public_result,
    }
    write_text(artifact_dir / "summary.json", json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
