#!/usr/bin/env python3
"""Polish Golden Daisy product title and SEO translations."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "ops/scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "ops/scripts"))

from ops.scripts.poll_shopify_product_translations import ShopifyClient, clean  # noqa: E402
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


PRODUCT_GID = "gid://shopify/Product/7546613530721"
HANDLE = "golden-daisy-mommy-and-me-set"
REPORT_PATH = ROOT / "ops/listings/golden-daisy-title-translation-polish-report.json"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "ar": {
        "title": "Golden Daisy للأم وابنتها - توب أو بنطال",
        "meta_title": "Golden Daisy للأم وابنتها | Dress Like Mommy",
        "meta_description": "قطع متناسقة للأم وابنتها: اختاري التوب الأصفر بزخرفة الأقحوان أو البنطال العاجي واسع الساق. مقاسات البنات 1-10 سنوات ومقاسات الأم S-L.",
    },
    "cs": {
        "title": "Golden Daisy maminka a dcera - top nebo kalhoty",
        "meta_title": "Golden Daisy maminka a dcera | Dress Like Mommy",
        "meta_description": "Sladěné kousky pro maminku a dceru: vyberte žlutý top s kopretinami nebo slonovinové široké kalhoty. Dívčí 1-10 let a maminka S-L.",
    },
    "da": {
        "title": "Golden Daisy mor og datter - top eller bukser",
        "meta_title": "Golden Daisy mor og datter | Dress Like Mommy",
        "meta_description": "Matchende dele til mor og datter: vælg den gule marguerit-top eller de elfenbensfarvede bukser med brede ben. Piger 1-10 år og mor S-L.",
    },
    "de": {
        "title": "Golden Daisy Mama und Tochter - Oberteil oder Hose",
        "meta_title": "Golden Daisy Mama und Tochter | Dress Like Mommy",
        "meta_description": "Passende Einzelteile für Mama und Tochter: gelbes Gänseblümchen-Oberteil oder elfenbeinfarbene Hose mit weitem Bein. Mädchen 1-10 Jahre und Mama S-L.",
    },
    "el": {
        "title": "Golden Daisy μαμά και κόρη - τοπ ή παντελόνι",
        "meta_title": "Golden Daisy μαμά και κόρη | Dress Like Mommy",
        "meta_description": "Ασορτί κομμάτια για μαμά και κόρη: επιλέξτε το κίτρινο τοπ με μαργαρίτες ή το ιβουάρ φαρδύ παντελόνι. Κορίτσια 1-10 ετών και μαμά S-L.",
    },
    "es": {
        "title": "Golden Daisy Mamá e hija - top o pantalón",
        "meta_title": "Golden Daisy Mamá e hija | Dress Like Mommy",
        "meta_description": "Prendas a juego para mamá e hija: elige el top amarillo con margaritas o el pantalón marfil de pierna ancha. Niñas 1-10 años y mamá S-L.",
    },
    "fi": {
        "title": "Golden Daisy äiti ja tytär - toppi tai housut",
        "meta_title": "Golden Daisy äiti ja tytär | Dress Like Mommy",
        "meta_description": "Yhteensopivat osat äidille ja tyttärelle: valitse keltainen päivänkakkaratoppi tai norsunluunväriset leveälahkeiset housut. Tytöt 1-10 v ja äiti S-L.",
    },
    "fr": {
        "title": "Golden Daisy maman et fille - haut ou pantalon",
        "meta_title": "Golden Daisy maman et fille | Dress Like Mommy",
        "meta_description": "Pièces assorties maman et fille : choisissez le haut jaune à marguerites ou le pantalon ivoire à jambe large. Fille 1-10 ans et maman S-L.",
    },
    "he": {
        "title": "Golden Daisy לאמא ובת - טופ או מכנסיים",
        "meta_title": "Golden Daisy לאמא ובת | Dress Like Mommy",
        "meta_description": "פריטים תואמים לאמא ובת: בחרי בטופ הצהוב עם דייזי או במכנסיים הרחבים בצבע שנהב. מידות ילדות 1-10 ואמא S-L.",
    },
    "hi": {
        "title": "Golden Daisy माँ और बेटी - टॉप या पैंट",
        "meta_title": "Golden Daisy माँ और बेटी | Dress Like Mommy",
        "meta_description": "माँ और बेटी के लिए मैचिंग अलग पीस: पीला डेज़ी टॉप या आइवरी वाइड-लेग पैंट चुनें। लड़कियों 1-10 वर्ष और माँ S-L.",
    },
    "it": {
        "title": "Golden Daisy mamma e figlia - top o pantaloni",
        "meta_title": "Golden Daisy mamma e figlia | Dress Like Mommy",
        "meta_description": "Capi coordinati per mamma e figlia: scegli il top giallo con margherite o i pantaloni avorio a gamba larga. Bambina 1-10 anni e mamma S-L.",
    },
    "ja": {
        "title": "Golden Daisy ママと娘 - トップスまたはパンツ",
        "meta_title": "Golden Daisy ママと娘 | Dress Like Mommy",
        "meta_description": "ママと娘のおそろい単品。黄色のデイジートップス、またはアイボリーのワイドパンツを選べます。女の子1-10歳、ママS-L。",
    },
    "ko": {
        "title": "Golden Daisy 엄마와 딸 - 상의 또는 바지",
        "meta_title": "Golden Daisy 엄마와 딸 | Dress Like Mommy",
        "meta_description": "엄마와 딸을 위한 매칭 단품: 노란 데이지 상의 또는 아이보리 와이드 팬츠를 선택하세요. 여아 1-10세, 엄마 S-L.",
    },
    "nl": {
        "title": "Golden Daisy mama en dochter - top of broek",
        "meta_title": "Golden Daisy mama en dochter | Dress Like Mommy",
        "meta_description": "Matchende losse items voor mama en dochter: kies de gele madeliefjestop of de ivoorkleurige broek met wijde pijpen. Meisjes 1-10 jaar en mama S-L.",
    },
    "no": {
        "title": "Golden Daisy mamma og datter - topp eller bukse",
        "meta_title": "Golden Daisy mamma og datter | Dress Like Mommy",
        "meta_description": "Matchende deler for mamma og datter: velg den gule tusenfrydtoppen eller den elfenbensfargede buksen med vide ben. Jente 1-10 år og mamma S-L.",
    },
    "pl": {
        "title": "Golden Daisy mama i córka - top lub spodnie",
        "meta_title": "Golden Daisy mama i córka | Dress Like Mommy",
        "meta_description": "Dopasowane elementy dla mamy i córki: wybierz żółty top w stokrotki lub spodnie z szeroką nogawką w kolorze kości słoniowej. Dziewczynki 1-10 lat i mama S-L.",
    },
    "pt-BR": {
        "title": "Golden Daisy mamãe e filha - top ou calça",
        "meta_title": "Golden Daisy mamãe e filha | Dress Like Mommy",
        "meta_description": "Peças combinando para mamãe e filha: escolha o top amarelo com margaridas ou a calça marfim de perna larga. Meninas 1-10 anos e mamãe S-L.",
    },
    "ro": {
        "title": "Golden Daisy mamă și fiică - top sau pantaloni",
        "meta_title": "Golden Daisy mamă și fiică | Dress Like Mommy",
        "meta_description": "Piese asortate pentru mamă și fiică: alege topul galben cu margarete sau pantalonii ivory largi. Fete 1-10 ani și mamă S-L.",
    },
    "ru": {
        "title": "Golden Daisy мама и дочка - топ или брюки",
        "meta_title": "Golden Daisy мама и дочка | Dress Like Mommy",
        "meta_description": "Парные вещи для мамы и дочки: выберите желтый топ с ромашками или широкие брюки цвета айвори. Девочки 1-10 лет и мама S-L.",
    },
    "sv": {
        "title": "Golden Daisy mamma och dotter - topp eller byxor",
        "meta_title": "Golden Daisy mamma och dotter | Dress Like Mommy",
        "meta_description": "Matchande delar för mamma och dotter: välj den gula prästkragetoppen eller elfenbensvita byxor med vida ben. Flickor 1-10 år och mamma S-L.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Register polished title and SEO translations.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between translation chunks.")
    return parser.parse_args()


def fetch_state(client: ShopifyClient) -> dict[str, Any]:
    query = """
    query GoldenDaisyTitleTranslationState($id: ID!) {
      shopLocales { locale primary published }
      product(id: $id) {
        id
        handle
        status
        publishedAt
        onlineStoreUrl
        resourcePublicationsV2(first: 20) {
          nodes { isPublished publication { name } }
        }
      }
      translatableResource(resourceId: $id) {
        resourceId
        translatableContent { key value digest locale }
      }
    }
    """
    return client.graphql(query, {"id": PRODUCT_GID})


def digest_by_key(resource: dict[str, Any]) -> dict[str, str]:
    return {clean(row.get("key")): clean(row.get("digest")) for row in resource.get("translatableContent") or []}


def register_in_chunks(client: ShopifyClient, translations: list[dict[str, str]], pause_ms: int) -> int:
    count = 0
    for index in range(0, len(translations), 10):
        chunk = translations[index : index + 10]
        result = client.register_translations(PRODUCT_GID, chunk)
        count += len(result.get("translations") or [])
        if pause_ms > 0 and index + 10 < len(translations):
            time.sleep(pause_ms / 1000)
    return count


def main() -> None:
    args = parse_args()
    store_domain = resolve_store_domain(fallback_domain="dresslikemommy-com.myshopify.com")
    client = ShopifyClient(store_domain, load_access_token())
    state = fetch_state(client)
    product = state["product"]
    if product["handle"] != HANDLE:
        raise RuntimeError(f"Unexpected product handle: {product['handle']}")

    published_locales = [
        clean(row.get("locale"))
        for row in state["shopLocales"]
        if clean(row.get("locale")) and row.get("published") and not row.get("primary")
    ]
    digests = digest_by_key(state["translatableResource"])
    translations = []
    missing_locales = []
    for locale in published_locales:
        values = TRANSLATIONS.get(locale)
        if not values:
            missing_locales.append(locale)
            continue
        for key in ["title", "meta_title", "meta_description"]:
            translations.append(
                {
                    "locale": locale,
                    "key": key,
                    "value": values[key],
                    "translatableContentDigest": digests[key],
                }
            )

    registered = register_in_chunks(client, translations, max(args.pause_ms, 0)) if args.execute else 0
    live_publications = sorted(
        node["publication"]["name"]
        for node in product["resourcePublicationsV2"]["nodes"]
        if node["isPublished"]
    )
    report = {
        "execute": bool(args.execute),
        "store_domain": store_domain,
        "product_gid": PRODUCT_GID,
        "handle": HANDLE,
        "status": product["status"],
        "published_at": product["publishedAt"],
        "online_store_url": product["onlineStoreUrl"],
        "live_publications": live_publications,
        "published_locales": published_locales,
        "missing_locale_mappings": missing_locales,
        "translation_count": len(translations),
        "registered_count": registered,
        "checks": {
            locale: {
                "title_length": len(values["title"]),
                "meta_title_length": len(values["meta_title"]),
                "meta_description_length": len(values["meta_description"]),
                "forbidden_source_tokens": [
                    token
                    for token in ["1688", "Alibaba", "detail.1688.com"]
                    if token.lower() in " ".join(values.values()).lower()
                ],
            }
            for locale, values in TRANSLATIONS.items()
            if locale in published_locales
        },
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
