#!/usr/bin/env python3
"""Poll Shopify for newly created products and translate missing product content automatically."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import (  # noqa: E402
    DEFAULT_CONFIG_DIR,
    clean,
    load_access_token,
    resolve_store_domain,
)
from ops.scripts.sync_shopify_translations import DEFAULT_GLOSSARY, human_facing  # noqa: E402
from ops.scripts.translation_utils import TranslationBackend  # noqa: E402


API_VERSION = "2026-01"

RECENT_PRODUCTS_QUERY = """
query RecentProducts($first: Int!, $after: String, $reverse: Boolean!) {
  products(first: $first, after: $after, sortKey: CREATED_AT, reverse: $reverse) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        legacyResourceId
        handle
        title
        status
        createdAt
        updatedAt
      }
    }
  }
}
"""

PRODUCT_OPTION_VALUES_QUERY = """
query ProductOptionValues($id: ID!) {
  product(id: $id) {
    options(first: 10) {
      id
      optionValues {
        id
        name
      }
    }
  }
}
"""

SHOP_LOCALES_QUERY = """
query ShopLocales {
  shopLocales {
    locale
    name
    primary
    published
  }
}
"""

REGISTER_TRANSLATIONS_MUTATION = """
mutation RegisterTranslations($resourceId: ID!, $translations: [TranslationInput!]!) {
  translationsRegister(resourceId: $resourceId, translations: $translations) {
    userErrors {
      field
      message
    }
    translations {
      locale
      key
      value
    }
  }
}
"""

DEFAULT_STATE_PATH = DEFAULT_CONFIG_DIR / "shopify-product-translation-state.json"
DEFAULT_LOG_PATH = Path.home() / "Library" / "Logs" / "dresslikemommy" / "shopify-product-translation.jsonl"
DEFAULT_CACHE_PATH = REPO_ROOT / "ops" / "content" / "shopify-product-translation-live-cache.json"
DEFAULT_BULK_JSONL_PATH = REPO_ROOT / "ops" / "content" / "shopify-product-translation-bulk-repair.jsonl"
DEFAULT_NESTED_LIMIT = 100

RESOURCE_FIELD_ALLOWLIST = {
    "Product": {"title", "body_html", "product_type", "meta_title", "meta_description"},
    "Metafield": {"value"},
    "ProductOption": {"name"},
    "ProductOptionValue": {"name", "value"},
}
OPTION_RESOURCE_TYPES = {"ProductOption", "ProductOptionValue"}

OPTION_NAME_TRANSLATIONS = {
    "type": {
        "ar": "النوع",
        "cs": "Typ",
        "da": "Type",
        "de": "Typ",
        "el": "Τύπος",
        "es": "Tipo",
        "fi": "Tyyppi",
        "fr": "Type",
        "he": "סוג",
        "hi": "प्रकार",
        "it": "Tipo",
        "ja": "タイプ",
        "ko": "유형",
        "nl": "Type",
        "no": "Type",
        "pl": "Typ",
        "pt": "Tipo",
        "ro": "Tip",
        "ru": "Тип",
        "sv": "Typ",
        "zh": "类型",
    },
    "size": {
        "ar": "المقاس",
        "cs": "Velikost",
        "da": "Størrelse",
        "de": "Größe",
        "el": "Μέγεθος",
        "es": "Talla",
        "fi": "Koko",
        "fr": "Taille",
        "he": "מידה",
        "hi": "आकार",
        "it": "Taglia",
        "ja": "サイズ",
        "ko": "사이즈",
        "nl": "Maat",
        "no": "Størrelse",
        "pl": "Rozmiar",
        "pt": "Tamanho",
        "ro": "Mărime",
        "ru": "Размер",
        "sv": "Storlek",
        "zh": "尺寸",
    },
    "color": {
        "ar": "اللون",
        "cs": "Barva",
        "da": "Farve",
        "de": "Farbe",
        "el": "Χρώμα",
        "es": "Color",
        "fi": "Väri",
        "fr": "Couleur",
        "he": "צבע",
        "hi": "रंग",
        "it": "Colore",
        "ja": "カラー",
        "ko": "색상",
        "nl": "Kleur",
        "no": "Farge",
        "pl": "Kolor",
        "pt": "Cor",
        "ro": "Culoare",
        "ru": "Цвет",
        "sv": "Färg",
        "zh": "颜色",
    },
}

ROLE_TRANSLATIONS = {
    "child": {
        "ar": "للأطفال عمر",
        "cs": "Dítě",
        "da": "Barn",
        "de": "Kind",
        "el": "Παιδί",
        "es": "Infantil",
        "fi": "Lapsi",
        "fr": "Enfant",
        "he": "גיל",
        "hi": "बच्चों के लिए",
        "it": "Bimbi",
        "ja": "子供",
        "ko": "아동",
        "nl": "Kind",
        "no": "Barn",
        "pl": "Dziecko",
        "pt": "Infantil",
        "ro": "Copil",
        "ru": "Дети",
        "sv": "Barn",
        "zh": "儿童",
    },
    "girl": {
        "ar": "للبنات عمر",
        "cs": "Dívka",
        "da": "Pige",
        "de": "Mädchen",
        "el": "Κορίτσι",
        "es": "Niña",
        "fi": "Tyttö",
        "fr": "Fille",
        "he": "ילדה",
        "hi": "लड़की",
        "it": "Bambina",
        "ja": "女の子",
        "ko": "여아",
        "nl": "Meisje",
        "no": "Jente",
        "pl": "Dziewczynka",
        "pt": "Menina",
        "ro": "Fată",
        "ru": "Девочка",
        "sv": "Flicka",
        "zh": "女孩",
    },
    "boy": {
        "ar": "للأولاد عمر",
        "cs": "Chlapec",
        "da": "Dreng",
        "de": "Junge",
        "el": "Αγόρι",
        "es": "Niño",
        "fi": "Poika",
        "fr": "Garçon",
        "he": "ילד",
        "hi": "लड़का",
        "it": "Bambino",
        "ja": "男の子",
        "ko": "남아",
        "nl": "Jongen",
        "no": "Gutt",
        "pl": "Chłopiec",
        "pt": "Menino",
        "ro": "Băiat",
        "ru": "Мальчик",
        "sv": "Pojke",
        "zh": "男孩",
    },
    "mother": {
        "ar": "الأم",
        "cs": "Maminka",
        "da": "Mor",
        "de": "Mama",
        "el": "Μητέρα",
        "es": "Mamá",
        "fi": "Äiti",
        "fr": "Maman",
        "he": "אמא",
        "hi": "माँ",
        "it": "Mamma",
        "ja": "ママ",
        "ko": "엄마",
        "nl": "Mama",
        "no": "Mamma",
        "pl": "Mama",
        "pt": "Mãe",
        "ro": "Mamă",
        "ru": "Мама",
        "sv": "Mamma",
        "zh": "妈妈",
    },
    "father": {
        "ar": "الأب",
        "cs": "Tatínek",
        "da": "Far",
        "de": "Papa",
        "el": "Πατέρας",
        "es": "Papá",
        "fi": "Isä",
        "fr": "Papa",
        "he": "אבא",
        "hi": "पिता",
        "it": "Papà",
        "ja": "パパ",
        "ko": "아빠",
        "nl": "Papa",
        "no": "Pappa",
        "pl": "Tata",
        "pt": "Pai",
        "ro": "Tată",
        "ru": "Папа",
        "sv": "Pappa",
        "zh": "爸爸",
    },
    "adult": {
        "ar": "للكبار",
        "cs": "Dospělý",
        "da": "Voksen",
        "de": "Erwachsene",
        "el": "Ενήλικας",
        "es": "Adulto",
        "fi": "Aikuinen",
        "fr": "Adulte",
        "he": "מבוגר",
        "hi": "वयस्क",
        "it": "Adulto",
        "ja": "大人",
        "ko": "성인",
        "nl": "Volwassene",
        "no": "Voksen",
        "pl": "Dorosły",
        "pt": "Adulto",
        "ro": "Adult",
        "ru": "Взрослый",
        "sv": "Vuxen",
        "zh": "成人",
    },
}

SIZE_ROLE_RE = re.compile(r"^(Child|Girl|Boy|Mother|Father|Adult)\s+(.+)$", flags=re.I)
AGE_SUFFIX_RE = re.compile(r"^(\d+(?:\s*[-–]\s*\d+)?)\s+Years?$", flags=re.I)
SIZE_CHART_TABLE_RE = re.compile(
    r"(<table\b(?=[^>]*(?:id=[\"'][^\"']*size-chart|class=[\"'][^\"']*size-chart))[^>]*>)(.*?)(</table>)",
    flags=re.I | re.S,
)
TABLE_ROW_RE = re.compile(r"(<tr\b[^>]*>)(.*?)(</tr>)", flags=re.I | re.S)
TABLE_CELL_RE = re.compile(r"(<td\b[^>]*>)(.*?)(</td>)", flags=re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")

GARMENT_TRANSLATIONS = {
    "Dress": {
        "ar": "فستان",
        "cs": "Šaty",
        "da": "Kjole",
        "de": "Kleid",
        "el": "Φόρεμα",
        "es": "Vestido",
        "fi": "Mekko",
        "fr": "Robe",
        "he": "שמלה",
        "hi": "ड्रेस",
        "it": "Vestito",
        "ja": "ワンピース",
        "ko": "드레스",
        "nl": "Jurk",
        "no": "Kjole",
        "pl": "Sukienka",
        "pt": "Vestido",
        "ro": "Rochie",
        "ru": "Платье",
        "sv": "Klänning",
        "zh": "连衣裙",
    },
    "Shirt": {
        "ar": "قميص",
        "cs": "Košile",
        "da": "Skjorte",
        "de": "Hemd",
        "el": "Πουκάμισο",
        "es": "Camisa",
        "fi": "Paita",
        "fr": "Chemise",
        "he": "חולצה",
        "hi": "शर्ट",
        "it": "Camicia",
        "ja": "シャツ",
        "ko": "셔츠",
        "nl": "Shirt",
        "no": "Skjorte",
        "pl": "Koszula",
        "pt": "Camisa",
        "ro": "Cămașă",
        "ru": "Рубашка",
        "sv": "Skjorta",
        "zh": "衬衫",
    },
    "Shorts": {
        "ar": "شورت",
        "cs": "Šortky",
        "da": "Shorts",
        "de": "Shorts",
        "el": "Σορτς",
        "es": "Shorts",
        "fi": "Shortsit",
        "fr": "Short",
        "he": "מכנסיים קצרים",
        "hi": "शॉर्ट्स",
        "it": "Shorts",
        "ja": "ショーツ",
        "ko": "반바지",
        "nl": "Shorts",
        "no": "Shorts",
        "pl": "Szorty",
        "pt": "Shorts",
        "ro": "Șorturi",
        "ru": "Шорты",
        "sv": "Shorts",
        "zh": "短裤",
    },
    "Top": {
        "ar": "توب",
        "cs": "Top",
        "da": "Top",
        "de": "Top",
        "el": "Τοπ",
        "es": "Top",
        "fi": "Yläosa",
        "fr": "Haut",
        "he": "טופ",
        "hi": "टॉप",
        "it": "Top",
        "ja": "トップス",
        "ko": "상의",
        "nl": "Top",
        "no": "Topp",
        "pl": "Top",
        "pt": "Top",
        "ro": "Top",
        "ru": "Топ",
        "sv": "Topp",
        "zh": "上衣",
    },
    "Romper": {
        "ar": "رومبر",
        "cs": "Overal",
        "da": "Heldragt",
        "de": "Strampler",
        "el": "Φορμάκι",
        "es": "Pelele",
        "fi": "Haalari",
        "fr": "Barboteuse",
        "he": "אוברול",
        "hi": "रोम्पर",
        "it": "Pagliaccetto",
        "ja": "ロンパース",
        "ko": "롬퍼",
        "nl": "Boxpakje",
        "no": "Romper",
        "pl": "Rampers",
        "pt": "Macacão",
        "ro": "Salopetă",
        "ru": "Ромпер",
        "sv": "Romper",
        "zh": "连体衣",
    },
    "Shirt & Shorts Set": {
        "ar": "طقم قميص وشورت",
        "cs": "Set košile a šortek",
        "da": "Skjorte- og shortssæt",
        "de": "Hemd- und Shorts-Set",
        "el": "Σετ πουκάμισο και σορτς",
        "es": "Conjunto de camisa y shorts",
        "fi": "Paita- ja shortsisetti",
        "fr": "Ensemble chemise et short",
        "he": "סט חולצה ומכנסיים קצרים",
        "hi": "शर्ट और शॉर्ट्स सेट",
        "it": "Set camicia e shorts",
        "ja": "シャツ＆ショーツセット",
        "ko": "셔츠와 반바지 세트",
        "nl": "Shirt- en shortset",
        "no": "Skjorte- og shortsett",
        "pl": "Zestaw koszula i szorty",
        "pt": "Conjunto de camisa e shorts",
        "ro": "Set cămașă și șorturi",
        "ru": "Комплект рубашка и шорты",
        "sv": "Skjorta och shorts-set",
        "zh": "衬衫短裤套装",
    },
}

YEAR_UNITS = {
    "ar": ("سنة", "سنوات", " "),
    "cs": ("rok", "let", " "),
    "da": ("år", "år", " "),
    "de": ("Jahr", "Jahre", " "),
    "el": ("έτος", "ετών", " "),
    "es": ("año", "años", " "),
    "fi": ("vuosi", "vuotta", " "),
    "fr": ("an", "ans", " "),
    "he": ("שנה", "שנים", " "),
    "hi": ("वर्ष", "वर्ष", " "),
    "it": ("anno", "anni", " "),
    "ja": ("歳", "歳", ""),
    "ko": ("세", "세", ""),
    "nl": ("jaar", "jaar", " "),
    "no": ("år", "år", " "),
    "pl": ("rok", "lat", " "),
    "pt": ("ano", "anos", " "),
    "ro": ("an", "ani", " "),
    "ru": ("год", "лет", " "),
    "sv": ("år", "år", " "),
    "zh": ("岁", "岁", ""),
}

BODY_LABEL_TRANSLATIONS = {
    "fabric": {
        "ar": "القماش", "cs": "Látka", "da": "Stof", "de": "Stoff", "el": "Ύφασμα",
        "es": "Tela", "fi": "Kangas", "fr": "Tissu", "he": "בד", "hi": "कपड़ा",
        "it": "Tessuto", "ja": "生地", "ko": "원단", "nl": "Stof", "no": "Stoff",
        "pl": "Materiał", "pt": "Tecido", "ro": "Țesătură", "ru": "Ткань",
        "sv": "Tyg", "zh": "面料",
    },
    "family story": {
        "ar": "قصة عائلية", "cs": "Rodinný příběh", "da": "Familiehistorie", "de": "Familiengeschichte",
        "el": "Οικογενειακή ιστορία", "es": "Historia familiar", "fi": "Perhetarina", "fr": "Histoire familiale",
        "he": "סיפור משפחתי", "hi": "पारिवारिक कहानी", "it": "Storia di famiglia", "ja": "ファミリーストーリー",
        "ko": "가족 이야기", "nl": "Familieverhaal", "no": "Familiehistorie", "pl": "Historia rodzinna",
        "pt": "História familiar", "ro": "Poveste de familie", "ru": "Семейная история", "sv": "Familjeberättelse",
        "zh": "家庭故事",
    },
    "print": {
        "ar": "النقشة", "cs": "Potisk", "da": "Print", "de": "Muster", "el": "Μοτίβο",
        "es": "Estampado", "fi": "Kuosi", "fr": "Imprimé", "he": "הדפס", "hi": "प्रिंट",
        "it": "Stampa", "ja": "柄", "ko": "프린트", "nl": "Print", "no": "Mønster",
        "pl": "Wzór", "pt": "Estampa", "ro": "Imprimeu", "ru": "Принт", "sv": "Mönster",
        "zh": "印花",
    },
    "design details": {
        "ar": "تفاصيل التصميم", "cs": "Detaily designu", "da": "Designdetaljer", "de": "Designdetails",
        "el": "Λεπτομέρειες σχεδίου", "es": "Detalles de diseño", "fi": "Suunnittelun yksityiskohdat",
        "fr": "Détails du design", "he": "פרטי העיצוב", "hi": "डिज़ाइन विवरण", "it": "Dettagli del design",
        "ja": "デザインの詳細", "ko": "디자인 디테일", "nl": "Ontwerpdetails", "no": "Designdetaljer",
        "pl": "Detale projektu", "pt": "Detalhes do design", "ro": "Detalii de design", "ru": "Детали дизайна",
        "sv": "Designdetaljer", "zh": "设计细节",
    },
    "care": {
        "ar": "العناية", "cs": "Péče", "da": "Pleje", "de": "Pflege", "el": "Φροντίδα",
        "es": "Cuidado", "fi": "Hoito", "fr": "Entretien", "he": "טיפול", "hi": "देखभाल",
        "it": "Cura", "ja": "お手入れ", "ko": "관리", "nl": "Onderhoud", "no": "Pleie",
        "pl": "Pielęgnacja", "pt": "Cuidados", "ro": "Îngrijire", "ru": "Уход", "sv": "Skötsel",
        "zh": "护理",
    },
    "size range": {
        "ar": "نطاق المقاسات", "cs": "Rozsah velikostí", "da": "Størrelsesudvalg", "de": "Größenbereich",
        "el": "Εύρος μεγεθών", "es": "Rango de tallas", "fi": "Kokovalikoima", "fr": "Gamme de tailles",
        "he": "טווח מידות", "hi": "साइज़ रेंज", "it": "Gamma taglie", "ja": "サイズ展開",
        "ko": "사이즈 범위", "nl": "Maatbereik", "no": "Størrelsesutvalg", "pl": "Zakres rozmiarów",
        "pt": "Faixa de tamanhos", "ro": "Gama de mărimi", "ru": "Диапазон размеров", "sv": "Storleksintervall",
        "zh": "尺码范围",
    },
    "key features": {
        "ar": "الميزات الرئيسية", "cs": "Klíčové vlastnosti", "da": "Nøglefunktioner", "de": "Wichtige Merkmale",
        "el": "Βασικά χαρακτηριστικά", "es": "Características principales", "fi": "Tärkeimmät ominaisuudet",
        "fr": "Caractéristiques principales", "he": "מאפיינים עיקריים", "hi": "मुख्य विशेषताएँ",
        "it": "Caratteristiche principali", "ja": "主な特徴", "ko": "주요 특징", "nl": "Belangrijkste kenmerken",
        "no": "Viktige funksjoner", "pl": "Najważniejsze cechy", "pt": "Principais características",
        "ro": "Caracteristici principale", "ru": "Основные характеристики", "sv": "Viktiga egenskaper",
        "zh": "主要特点",
    },
    "size chart": {
        "ar": "جدول المقاسات", "cs": "Tabulka velikostí", "da": "Størrelsesskema", "de": "Größentabelle",
        "el": "Πίνακας μεγεθών", "es": "Tabla de tallas", "fi": "Kokotaulukko", "fr": "Guide des tailles",
        "he": "טבלת מידות", "hi": "साइज़ चार्ट", "it": "Tabella taglie", "ja": "サイズ表",
        "ko": "사이즈 차트", "nl": "Maattabel", "no": "Størrelsestabell", "pl": "Tabela rozmiarów",
        "pt": "Tabela de tamanhos", "ro": "Tabel de mărimi", "ru": "Таблица размеров", "sv": "Storlekstabell",
        "zh": "尺码表",
    },
}

TABLE_HEADER_TRANSLATIONS = {
    "size": {"es": "Talla", "ja": "サイズ", "ar": "المقاس", "cs": "Velikost", "da": "Størrelse", "de": "Größe", "el": "Μέγεθος", "fi": "Koko", "fr": "Taille", "he": "מידה", "hi": "आकार", "it": "Taglia", "ko": "사이즈", "nl": "Maat", "no": "Størrelse", "pl": "Rozmiar", "pt": "Tamanho", "ro": "Mărime", "ru": "Размер", "sv": "Storlek", "zh": "尺码"},
    "age": {"es": "Edad", "ja": "年齢", "ar": "العمر", "cs": "Věk", "da": "Alder", "de": "Alter", "el": "Ηλικία", "fi": "Ikä", "fr": "Âge", "he": "גיל", "hi": "उम्र", "it": "Età", "ko": "연령", "nl": "Leeftijd", "no": "Alder", "pl": "Wiek", "pt": "Idade", "ro": "Vârstă", "ru": "Возраст", "sv": "Ålder", "zh": "年龄"},
    "weight (kg/lbs)": {"es": "Peso (kg/lb)", "ja": "体重 (kg/lb)", "ar": "الوزن (كجم/رطل)", "cs": "Hmotnost (kg/lb)", "da": "Vægt (kg/lb)", "de": "Gewicht (kg/lb)", "el": "Βάρος (kg/lb)", "fi": "Paino (kg/lb)", "fr": "Poids (kg/lb)", "he": "משקל (קג/ליברה)", "hi": "वजन (kg/lb)", "it": "Peso (kg/lb)", "ko": "체중 (kg/lb)", "nl": "Gewicht (kg/lb)", "no": "Vekt (kg/lb)", "pl": "Waga (kg/lb)", "pt": "Peso (kg/lb)", "ro": "Greutate (kg/lb)", "ru": "Вес (кг/фунты)", "sv": "Vikt (kg/lb)", "zh": "体重 (kg/lb)"},
    "height (cm/in)": {"es": "Altura (cm/in)", "ja": "身長 (cm/in)", "ar": "الطول (سم/بوصة)", "cs": "Výška (cm/in)", "da": "Højde (cm/in)", "de": "Größe (cm/in)", "el": "Ύψος (cm/in)", "fi": "Pituus (cm/in)", "fr": "Taille (cm/in)", "he": "גובה (סמ/אינץ')", "hi": "ऊँचाई (cm/in)", "it": "Altezza (cm/in)", "ko": "키 (cm/in)", "nl": "Lengte (cm/in)", "no": "Høyde (cm/in)", "pl": "Wzrost (cm/in)", "pt": "Altura (cm/in)", "ro": "Înălțime (cm/in)", "ru": "Рост (см/дюйм)", "sv": "Längd (cm/in)", "zh": "身高 (cm/in)"},
    "chest/bust (cm/in)": {"es": "Pecho/busto (cm/in)", "ja": "胸囲/バスト (cm/in)", "ar": "الصدر/البست (سم/بوصة)", "cs": "Hrudník/prsa (cm/in)", "da": "Bryst (cm/in)", "de": "Brust (cm/in)", "el": "Στήθος (cm/in)", "fi": "Rinta (cm/in)", "fr": "Poitrine (cm/in)", "he": "חזה (סמ/אינץ')", "hi": "छाती/बस्ट (cm/in)", "it": "Petto/busto (cm/in)", "ko": "가슴/버스트 (cm/in)", "nl": "Borst (cm/in)", "no": "Bryst (cm/in)", "pl": "Klatka/biust (cm/in)", "pt": "Peito/busto (cm/in)", "ro": "Piept/bust (cm/in)", "ru": "Грудь/бюст (см/дюйм)", "sv": "Bröst (cm/in)", "zh": "胸围 (cm/in)"},
    "skirt length (cm/in)": {"es": "Largo de falda (cm/in)", "ja": "スカート丈 (cm/in)", "ar": "طول التنورة (سم/بوصة)", "cs": "Délka sukně (cm/in)", "da": "Nederdelslængde (cm/in)", "de": "Rocklänge (cm/in)", "el": "Μήκος φούστας (cm/in)", "fi": "Hameen pituus (cm/in)", "fr": "Longueur de jupe (cm/in)", "he": "אורך חצאית (סמ/אינץ')", "hi": "स्कर्ट लंबाई (cm/in)", "it": "Lunghezza gonna (cm/in)", "ko": "스커트 길이 (cm/in)", "nl": "Roklengte (cm/in)", "no": "Skjørtlengde (cm/in)", "pl": "Długość spódnicy (cm/in)", "pt": "Comprimento da saia (cm/in)", "ro": "Lungime fustă (cm/in)", "ru": "Длина юбки (см/дюйм)", "sv": "Kjollängd (cm/in)", "zh": "裙长 (cm/in)"},
    "pant/short or — (cm/in)": {"es": "Pantalón/short o — (cm/in)", "ja": "パンツ/ショーツまたは — (cm/in)", "ar": "بنطال/شورت أو — (سم/بوصة)", "cs": "Kalhoty/šortky nebo — (cm/in)", "da": "Bukser/shorts eller — (cm/in)", "de": "Hose/Shorts oder — (cm/in)", "el": "Παντελόνι/σορτς ή — (cm/in)", "fi": "Housut/shortsit tai — (cm/in)", "fr": "Pantalon/short ou — (cm/in)", "he": "מכנסיים/שורט או — (סמ/אינץ')", "hi": "पैंट/शॉर्ट्स या — (cm/in)", "it": "Pantaloni/shorts o — (cm/in)", "ko": "팬츠/쇼츠 또는 — (cm/in)", "nl": "Broek/short of — (cm/in)", "no": "Bukse/shorts eller — (cm/in)", "pl": "Spodnie/szorty lub — (cm/in)", "pt": "Calça/short ou — (cm/in)", "ro": "Pantaloni/șorturi sau — (cm/in)", "ru": "Брюки/шорты или — (см/дюйм)", "sv": "Byxa/shorts eller — (cm/in)", "zh": "裤长/短裤或 — (cm/in)"},
    "hip (cm/in)": {"es": "Cadera (cm/in)", "ja": "ヒップ (cm/in)", "ar": "الورك (سم/بوصة)", "cs": "Boky (cm/in)", "da": "Hofte (cm/in)", "de": "Hüfte (cm/in)", "el": "Γοφοί (cm/in)", "fi": "Lantio (cm/in)", "fr": "Hanches (cm/in)", "he": "ירכיים (סמ/אינץ')", "hi": "कूल्हे (cm/in)", "it": "Fianchi (cm/in)", "ko": "힙 (cm/in)", "nl": "Heup (cm/in)", "no": "Hofte (cm/in)", "pl": "Biodra (cm/in)", "pt": "Quadril (cm/in)", "ro": "Șold (cm/in)", "ru": "Бедра (см/дюйм)", "sv": "Höft (cm/in)", "zh": "臀围 (cm/in)"},
    "waist (cm/in)": {"es": "Cintura (cm/in)", "ja": "ウエスト (cm/in)", "ar": "الخصر (سم/بوصة)", "cs": "Pas (cm/in)", "da": "Talje (cm/in)", "de": "Taille (cm/in)", "el": "Μέση (cm/in)", "fi": "Vyötärö (cm/in)", "fr": "Taille (cm/in)", "he": "מותן (סמ/אינץ')", "hi": "कमर (cm/in)", "it": "Vita (cm/in)", "ko": "허리 (cm/in)", "nl": "Taille (cm/in)", "no": "Midje (cm/in)", "pl": "Talia (cm/in)", "pt": "Cintura (cm/in)", "ro": "Talie (cm/in)", "ru": "Талия (см/дюйм)", "sv": "Midja (cm/in)", "zh": "腰围 (cm/in)"},
    "garment length (cm/in)": {"es": "Largo de prenda (cm/in)", "ja": "着丈 (cm/in)", "ar": "طول القطعة (سم/بوصة)", "cs": "Délka oděvu (cm/in)", "da": "Tøjlængde (cm/in)", "de": "Kleidungsstücklänge (cm/in)", "el": "Μήκος ρούχου (cm/in)", "fi": "Vaatteen pituus (cm/in)", "fr": "Longueur du vêtement (cm/in)", "he": "אורך הבגד (סמ/אינץ')", "hi": "परिधान लंबाई (cm/in)", "it": "Lunghezza capo (cm/in)", "ko": "의류 길이 (cm/in)", "nl": "Kledinglengte (cm/in)", "no": "Plagglengde (cm/in)", "pl": "Długość ubrania (cm/in)", "pt": "Comprimento da peça (cm/in)", "ro": "Lungime articol (cm/in)", "ru": "Длина изделия (см/дюйм)", "sv": "Plagglängd (cm/in)", "zh": "衣长 (cm/in)"},
}


@dataclass
class RecentProduct:
    product_gid: str
    product_id: str
    handle: str
    title: str
    status: str
    created_at: str
    updated_at: str


@dataclass
class ExistingTranslation:
    locale: str
    key: str
    value: str
    outdated: bool


@dataclass
class ResourceSnapshot:
    resource_id: str
    resource_type: str
    translatable_content: list[dict[str, str]]
    existing_translations: dict[tuple[str, str], ExistingTranslation]
    nested_resources: list["ResourceSnapshot"] = field(default_factory=list)
    nested_truncated: bool = False


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso8601(value: str) -> datetime:
    return datetime.fromisoformat(clean(value).replace("Z", "+00:00"))


def isoformat_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "created_at_cursor": "",
            "processed_ids_at_cursor": [],
            "initialized_at": "",
            "last_run_at": "",
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def append_log(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def initialize_state(
    path: Path,
    *,
    initialize_now: bool,
    bootstrap_hours: int,
) -> dict[str, Any]:
    state = load_state(path)
    if clean(state.get("initialized_at")):
        return state

    if initialize_now or bootstrap_hours <= 0:
        cursor_time = utc_now()
    else:
        cursor_time = utc_now() - timedelta(hours=max(bootstrap_hours, 0))

    state["created_at_cursor"] = isoformat_utc(cursor_time)
    state["processed_ids_at_cursor"] = []
    state["initialized_at"] = isoformat_utc(utc_now())
    state["last_run_at"] = ""
    save_state(path, state)
    return state


def is_newer_than_cursor(product: RecentProduct, state: dict[str, Any]) -> bool:
    cursor = clean(state.get("created_at_cursor"))
    if not cursor:
        return True
    if product.created_at > cursor:
        return True
    if product.created_at == cursor and product.product_id not in set(state.get("processed_ids_at_cursor") or []):
        return True
    return False


def update_cursor_state(state: dict[str, Any], finalized: list[RecentProduct]) -> None:
    if not finalized:
        return

    current_cursor = clean(state.get("created_at_cursor"))
    current_ids = set(state.get("processed_ids_at_cursor") or [])
    newest_created_at = finalized[-1].created_at

    if newest_created_at > current_cursor:
        state["created_at_cursor"] = newest_created_at
        state["processed_ids_at_cursor"] = [item.product_id for item in finalized if item.created_at == newest_created_at]
        return

    if newest_created_at == current_cursor:
        for item in finalized:
            if item.created_at == current_cursor:
                current_ids.add(item.product_id)
        state["processed_ids_at_cursor"] = sorted(current_ids)


def resource_type_from_gid(resource_id: str) -> str:
    parts = clean(resource_id).split("/")
    return parts[3] if len(parts) >= 4 else ""


def locale_alias_fragment(locales: list[str]) -> tuple[str, dict[str, str]]:
    alias_to_locale: dict[str, str] = {}
    lines: list[str] = []
    for idx, locale in enumerate(locales):
        alias = f"loc_{idx}"
        alias_to_locale[alias] = locale
        lines.append(
            f"""{alias}: translations(locale: "{locale}") {{
              key
              value
              outdated
              locale
            }}"""
        )
    return "\n".join(lines), alias_to_locale


def parse_resource_node(node: dict[str, Any], alias_to_locale: dict[str, str]) -> ResourceSnapshot:
    existing: dict[tuple[str, str], ExistingTranslation] = {}
    for alias, locale in alias_to_locale.items():
        for item in node.get(alias) or []:
            key = clean(item.get("key"))
            existing[(locale, key)] = ExistingTranslation(
                locale=clean(item.get("locale")) or locale,
                key=key,
                value=item.get("value") or "",
                outdated=bool(item.get("outdated")),
            )

    nested_root = node.get("nestedTranslatableResources") or {}
    nested_resources = [
        parse_resource_node(edge.get("node") or {}, alias_to_locale)
        for edge in nested_root.get("edges") or []
        if edge.get("node")
    ]

    return ResourceSnapshot(
        resource_id=clean(node.get("resourceId")),
        resource_type=resource_type_from_gid(clean(node.get("resourceId"))),
        translatable_content=[
            {
                "key": clean(item.get("key")),
                "value": item.get("value") or "",
                "digest": clean(item.get("digest")),
                "locale": clean(item.get("locale")),
            }
            for item in node.get("translatableContent") or []
            if clean(item.get("key"))
        ],
        existing_translations=existing,
        nested_resources=nested_resources,
        nested_truncated=bool(nested_root.get("pageInfo", {}).get("hasNextPage")),
    )


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str):
        self.store_domain = store_domain
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Shopify-Access-Token": access_token,
            }
        )

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        last_errors: list[dict[str, Any]] = []
        for attempt in range(6):
            response = self.session.post(
                self.endpoint,
                json={"query": query, "variables": variables or {}},
                timeout=90,
            )
            if response.status_code == 429 and attempt < 5:
                time.sleep(min(30, 2 ** attempt))
                continue
            response.raise_for_status()
            payload = response.json()
            errors = payload.get("errors") or []
            if not errors:
                return payload["data"]

            last_errors = errors
            throttled = any(
                (error.get("extensions") or {}).get("code") == "THROTTLED"
                for error in errors
            )
            if throttled and attempt < 5:
                time.sleep(min(30, 2 ** attempt))
                continue
            raise RuntimeError(json.dumps(errors, ensure_ascii=False))

        raise RuntimeError(json.dumps(last_errors, ensure_ascii=False))

    def shop_locales(self) -> list[dict[str, Any]]:
        return self.graphql(SHOP_LOCALES_QUERY)["shopLocales"]

    def recent_products(self, *, max_pages: int, page_size: int) -> list[RecentProduct]:
        rows: list[RecentProduct] = []
        after: str | None = None
        for _ in range(max_pages):
            data = self.graphql(
                RECENT_PRODUCTS_QUERY,
                {"first": page_size, "after": after, "reverse": True},
            )["products"]
            for edge in data.get("edges") or []:
                node = edge.get("node") or {}
                rows.append(
                    RecentProduct(
                        product_gid=clean(node.get("id")),
                        product_id=clean(node.get("legacyResourceId")),
                        handle=clean(node.get("handle")),
                        title=clean(node.get("title")),
                        status=clean(node.get("status")),
                        created_at=clean(node.get("createdAt")),
                        updated_at=clean(node.get("updatedAt")),
                    )
                )
            if not data.get("pageInfo", {}).get("hasNextPage"):
                break
            after = clean(data.get("pageInfo", {}).get("endCursor"))
        return rows

    def products_by_handles(self, handles: list[str]) -> list[RecentProduct]:
        rows: list[RecentProduct] = []
        query = """
        query ProductByHandle($handle: String!) {
          productByHandle(handle: $handle) {
            id
            legacyResourceId
            handle
            title
            status
            createdAt
            updatedAt
          }
        }
        """
        for handle in handles:
            product = self.graphql(query, {"handle": handle}).get("productByHandle")
            if not product:
                continue
            rows.append(
                RecentProduct(
                    product_gid=clean(product.get("id")),
                    product_id=clean(product.get("legacyResourceId")),
                    handle=clean(product.get("handle")),
                    title=clean(product.get("title")),
                    status=clean(product.get("status")),
                    created_at=clean(product.get("createdAt")),
                    updated_at=clean(product.get("updatedAt")),
                )
            )
        return rows

    def product_option_value_ids(self, product_gid: str) -> list[str]:
        product = self.graphql(PRODUCT_OPTION_VALUES_QUERY, {"id": product_gid}).get("product")
        if not product:
            return []

        option_value_ids: list[str] = []
        seen: set[str] = set()
        for option in product.get("options") or []:
            for option_value in option.get("optionValues") or []:
                option_value_id = clean(option_value.get("id"))
                if not option_value_id or option_value_id in seen:
                    continue
                seen.add(option_value_id)
                option_value_ids.append(option_value_id)
        return option_value_ids

    def fetch_resource(self, resource_id: str, locales: list[str], nested_first: int) -> ResourceSnapshot:
        translations_fragment, alias_to_locale = locale_alias_fragment(locales)
        query = f"""
        query ResourceSnapshot($id: ID!, $nestedFirst: Int!) {{
          translatableResource(resourceId: $id) {{
            resourceId
            translatableContent {{
              key
              value
              digest
              locale
            }}
            {translations_fragment}
            nestedTranslatableResources(first: $nestedFirst) {{
              pageInfo {{
                hasNextPage
                endCursor
              }}
              edges {{
                node {{
                  resourceId
                  translatableContent {{
                    key
                    value
                    digest
                    locale
                  }}
                  {translations_fragment}
                }}
              }}
            }}
          }}
        }}
        """
        node = self.graphql(query, {"id": resource_id, "nestedFirst": nested_first})["translatableResource"]
        if not node:
            raise RuntimeError(f"Missing translatable resource for {resource_id}")
        return parse_resource_node(node, alias_to_locale)

    def register_translations(self, resource_id: str, translations: list[dict[str, str]]) -> dict[str, Any]:
        data = self.graphql(
            REGISTER_TRANSLATIONS_MUTATION,
            {"resourceId": resource_id, "translations": translations},
        )["translationsRegister"]
        if data["userErrors"]:
            raise RuntimeError(json.dumps(data["userErrors"], ensure_ascii=False))
        return data

    def staged_upload(self, jsonl_path: Path) -> str:
        mutation = """
        mutation CreateStagedUpload($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets {
              url
              resourceUrl
              parameters {
                name
                value
              }
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        data = self.graphql(
            mutation,
            {
                "input": [
                    {
                        "resource": "BULK_MUTATION_VARIABLES",
                        "filename": jsonl_path.name,
                        "mimeType": "text/jsonl",
                        "httpMethod": "POST",
                    }
                ]
            },
        )["stagedUploadsCreate"]
        if data["userErrors"]:
            raise RuntimeError(json.dumps(data["userErrors"], ensure_ascii=False))

        target = data["stagedTargets"][0]
        form = {item["name"]: item["value"] for item in target["parameters"]}
        with jsonl_path.open("rb") as handle:
            response = requests.post(
                target["url"],
                data=form,
                files={"file": (jsonl_path.name, handle, "text/jsonl")},
                timeout=300,
            )
            response.raise_for_status()

        resource_url = clean(target.get("resourceUrl"))
        if "/admin/tmp/files/" in resource_url:
            return resource_url.split("/admin/tmp/files/", 1)[-1]
        if form.get("key"):
            return form["key"]
        return resource_url

    def run_bulk_translation_mutation(self, staged_upload_path: str) -> str:
        mutation = """
        mutation RunTranslationsBulk($mutation: String!, $stagedUploadPath: String!) {
          bulkOperationRunMutation(mutation: $mutation, stagedUploadPath: $stagedUploadPath) {
            bulkOperation {
              id
              status
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        mutation_body = """
        mutation call($resourceId: ID!, $translations: [TranslationInput!]!) {
          translationsRegister(resourceId: $resourceId, translations: $translations) {
            userErrors {
              field
              message
            }
          }
        }
        """
        data = self.graphql(
            mutation,
            {
                "mutation": mutation_body,
                "stagedUploadPath": staged_upload_path,
            },
        )["bulkOperationRunMutation"]
        if data["userErrors"]:
            raise RuntimeError(json.dumps(data["userErrors"], ensure_ascii=False))
        return clean(data["bulkOperation"]["id"])

    def current_bulk_operation(self) -> dict[str, Any] | None:
        query = """
        query {
          currentBulkOperation {
            id
            status
            errorCode
            objectCount
            fileSize
            url
            partialDataUrl
          }
        }
        """
        return self.graphql(query)["currentBulkOperation"]

    def bulk_operation_by_id(self, operation_id: str) -> dict[str, Any] | None:
        query = """
        query BulkOperationById($id: ID!) {
          node(id: $id) {
            __typename
            ... on BulkOperation {
              id
              status
              errorCode
              objectCount
              fileSize
              url
              partialDataUrl
            }
          }
        }
        """
        node = self.graphql(query, {"id": operation_id})["node"]
        if not node or node.get("__typename") != "BulkOperation":
            return None
        return {key: value for key, value in node.items() if key != "__typename"}

    def poll_bulk_operation(self, operation_id: str) -> dict[str, Any] | None:
        while True:
            current = self.current_bulk_operation()
            if current and current.get("id") == operation_id:
                if current.get("status") in {"CREATED", "RUNNING", "CANCELING"}:
                    print(
                        f"bulk status={current.get('status')} objects={current.get('objectCount')}",
                        flush=True,
                    )
                    time.sleep(3)
                    continue
                return current

            by_id = self.bulk_operation_by_id(operation_id)
            if by_id and by_id.get("status") in {"CREATED", "RUNNING", "CANCELING"}:
                print(
                    f"bulk status={by_id.get('status')} objects={by_id.get('objectCount')}",
                    flush=True,
                )
                time.sleep(3)
                continue
            return by_id


def resolve_target_locales(client: ShopifyClient, requested_locales: str) -> list[str]:
    if requested_locales:
        return [item.strip() for item in requested_locales.split(",") if item.strip()]

    locales = []
    for item in client.shop_locales():
        locale = clean(item.get("locale"))
        if not locale or item.get("primary") or not item.get("published"):
            continue
        locales.append(locale)
    return locales


def locale_root(locale: str) -> str:
    root = clean(locale).replace("_", "-").split("-", 1)[0]
    return "zh" if root == "zh" else root


def locale_lookup(mapping: dict[str, str], locale: str, fallback: str = "") -> str:
    root = locale_root(locale)
    return mapping.get(locale) or mapping.get(root) or fallback


def leading_age_number(age_span: str) -> int:
    match = re.match(r"^\d+", clean(age_span))
    return int(match.group(0)) if match else 0


def translated_option_name(value: str, locale: str) -> str | None:
    normalized = clean(value).lower()
    if normalized not in OPTION_NAME_TRANSLATIONS:
        return None
    return locale_lookup(OPTION_NAME_TRANSLATIONS[normalized], locale, clean(value))


def translated_garment(value: str, locale: str) -> str | None:
    source = clean(value)
    if source in GARMENT_TRANSLATIONS:
        return locale_lookup(GARMENT_TRANSLATIONS[source], locale, source)
    return None


def translated_age_label(role: str, age_span: str, locale: str) -> str:
    role_label = locale_lookup(ROLE_TRANSLATIONS[role], locale, role.title())
    root = locale_root(locale)
    singular, plural, joiner = YEAR_UNITS.get(root, ("Year", "Years", " "))
    normalized_age = clean(age_span).replace("–", "-")
    if root == "ar" and normalized_age == "2":
        return f"{role_label} سنتين"
    number = leading_age_number(normalized_age)
    if "-" not in normalized_age:
        if root == "cs":
            plural = "roky" if 2 <= number <= 4 else plural
        elif root == "pl":
            last = number % 10
            last_two = number % 100
            plural = "lata" if 2 <= last <= 4 and not 12 <= last_two <= 14 else plural
        elif root == "ru":
            last = number % 10
            last_two = number % 100
            if last == 1 and last_two != 11:
                plural = singular
            elif 2 <= last <= 4 and not 12 <= last_two <= 14:
                plural = "года"
    unit = plural if "-" in normalized_age or normalized_age != "1" else singular
    return f"{role_label} {normalized_age}{joiner}{unit}"


def strip_markup(value: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", clean(value))).strip()


def infer_product_context(product: RecentProduct | None, snapshots: list[ResourceSnapshot]) -> dict[str, Any]:
    text_parts = [clean(product.handle if product else ""), clean(product.title if product else "")]
    for snapshot in snapshots:
        if snapshot.resource_type != "Product":
            continue
        for item in snapshot.translatable_content:
            if item.get("key") in {"title", "body_html", "product_type", "meta_title", "meta_description"}:
                text_parts.append(clean(item.get("value")))
    haystack = strip_markup(" ".join(text_parts)).lower()

    girl_score = sum(
        1
        for token in (
            "girl",
            "girls",
            "daughter",
            "daughters",
            "mother daughter",
            "mom and daughter",
            "mom + daughter",
            "girl dress",
            "mommy and me dress",
            "mommy-and-me dress",
        )
        if token in haystack
    )
    boy_score = sum(
        1
        for token in (
            "boy",
            "boys",
            "son",
            "sons",
            "father son",
            "dad and son",
            "dad + son",
            "boy shirt",
            "daddy and me",
            "daddy-and-me",
        )
        if token in haystack
    )

    child_role = "child"
    if girl_score and not boy_score:
        child_role = "girl"
    elif boy_score and not girl_score:
        child_role = "boy"

    return {
        "ambiguous_child_role": child_role,
        "has_girl_context": bool(girl_score),
        "has_boy_context": bool(boy_score),
    }


def child_role_for_table(source_prefix: str, source_table: str, product_context: dict[str, Any] | None) -> str:
    product_context = product_context or {}
    context_text = strip_markup(f"{source_prefix[-500:]} {source_table}").lower()

    if "dress" in context_text and product_context.get("has_girl_context") and not product_context.get("has_boy_context"):
        return "girl"
    if "shirt" in context_text and product_context.get("has_boy_context") and not product_context.get("has_girl_context"):
        return "boy"
    if "girl" in context_text or "daughter" in context_text:
        return "girl"
    if "boy" in context_text or "son" in context_text:
        return "boy"
    return clean(product_context.get("ambiguous_child_role")) or "child"


def translated_role_word(
    role: str,
    locale: str,
    *,
    product_context: dict[str, Any] | None = None,
    table_child_role: str = "",
) -> str:
    source_role = clean(role).lower()
    if source_role == "child":
        product_context = product_context or {}
        source_role = clean(table_child_role) or clean(product_context.get("ambiguous_child_role")) or "child"
        if source_role not in ROLE_TRANSLATIONS:
            source_role = "child"
    return locale_lookup(ROLE_TRANSLATIONS.get(source_role, {}), locale, role.title())


def translate_embedded_role_words(
    value: str,
    locale: str,
    *,
    product_context: dict[str, Any] | None = None,
    table_child_role: str = "",
) -> str:
    def replace_role(match: re.Match[str]) -> str:
        return translated_role_word(
            match.group(1),
            locale,
            product_context=product_context,
            table_child_role=table_child_role,
        )

    return re.sub(r"\b(Child|Girl|Boy|Mother|Father|Adult)\b", replace_role, value, flags=re.I)


def translated_role_size_label(
    source: str,
    locale: str,
    *,
    product_context: dict[str, Any] | None = None,
    table_child_role: str = "",
) -> str | None:
    size_match = SIZE_ROLE_RE.match(clean(source))
    if not size_match:
        return None

    role = size_match.group(1).lower()
    suffix = clean(size_match.group(2))
    resolved_role = role
    if role == "child":
        product_context = product_context or {}
        resolved_role = clean(table_child_role) or clean(product_context.get("ambiguous_child_role")) or "child"
        if resolved_role not in ROLE_TRANSLATIONS:
            resolved_role = "child"

    age_match = AGE_SUFFIX_RE.match(suffix)
    if resolved_role in {"child", "girl", "boy"} and age_match:
        return translated_age_label(resolved_role, age_match.group(1), locale)

    role_label = translated_role_word(
        resolved_role,
        locale,
        product_context=product_context,
        table_child_role=table_child_role,
    )
    suffix = translate_embedded_role_words(
        suffix,
        locale,
        product_context=product_context,
        table_child_role=table_child_role,
    )
    return f"{role_label} {suffix}"


def first_body_cell_text(row_html: str) -> str:
    match = TABLE_CELL_RE.search(row_html)
    if not match:
        return ""
    return strip_markup(match.group(2))


def replace_first_body_cell(row_html: str, replacement: str) -> str:
    return TABLE_CELL_RE.sub(
        lambda match: f"{match.group(1)}{replacement}{match.group(3)}",
        row_html,
        count=1,
    )


def translated_body_label(label_key: str, locale: str) -> str:
    source = clean(label_key).lower()
    return locale_lookup(BODY_LABEL_TRANSLATIONS.get(source, {}), locale, clean(label_key).title())


def translated_table_header(label_key: str, locale: str) -> str:
    source = clean(label_key).lower()
    return locale_lookup(TABLE_HEADER_TRANSLATIONS.get(source, {}), locale, clean(label_key))


def translated_size_chart_heading(match: re.Match[str], locale: str) -> str:
    prefix = match.group(1)
    chart_label = translated_body_label("size chart", locale)
    garment = clean(match.group(2))
    garment_label = translated_garment(garment, locale) or garment
    return f"{prefix}{chart_label} - {garment_label}"


def repair_common_product_html_labels(translated_html: str, locale: str) -> str:
    repaired = translated_html
    if not repaired:
        return repaired

    for source in sorted(BODY_LABEL_TRANSLATIONS, key=len, reverse=True):
        target = translated_body_label(source, locale)
        repaired = re.sub(
            rf"(?<![A-Za-z]){re.escape(source)}(\s*:)",
            lambda match, target=target: f"{target}{match.group(1)}",
            repaired,
            flags=re.I,
        )

    repaired = re.sub(
        r"((?:>|^)\s*)Size\s+Chart\s*-\s*([A-Za-z &]+)(?=\s*(?:<|$))",
        lambda match: translated_size_chart_heading(match, locale),
        repaired,
        flags=re.I,
    )

    for source in sorted(TABLE_HEADER_TRANSLATIONS, key=len, reverse=True):
        target = translated_table_header(source, locale)
        repaired = re.sub(
            rf"(>\s*){re.escape(source)}(\s*<)",
            lambda match, target=target: f"{match.group(1)}{target}{match.group(2)}",
            repaired,
            flags=re.I,
        )

    return repaired


def repair_product_html_size_labels(
    source_html: str,
    translated_html: str,
    locale: str,
    product_context: dict[str, Any] | None = None,
) -> str:
    if not source_html or not translated_html or "size-chart" not in source_html:
        return translated_html

    source_tables = list(SIZE_CHART_TABLE_RE.finditer(source_html))
    translated_tables = list(SIZE_CHART_TABLE_RE.finditer(translated_html))
    if not source_tables or not translated_tables:
        return translated_html

    repaired = translated_html
    offset = 0
    all_replacement_labels: list[tuple[str, str]] = []
    for table_index, source_table_match in enumerate(source_tables):
        if table_index >= len(translated_tables):
            break
        translated_table_match = translated_tables[table_index]
        translated_start = translated_table_match.start() + offset
        translated_end = translated_table_match.end() + offset
        translated_table_html = repaired[translated_start:translated_end]
        source_table_html = source_table_match.group(0)
        table_child_role = child_role_for_table(source_html[: source_table_match.start()], source_table_html, product_context)
        source_rows = list(TABLE_ROW_RE.finditer(source_table_html))
        translated_rows = list(TABLE_ROW_RE.finditer(translated_table_html))
        next_row_index = 0
        replacement_labels: list[tuple[str, str]] = []

        for source_row_match in source_rows:
            source_row_html = source_row_match.group(0)
            source_label = first_body_cell_text(source_row_html)
            if not source_label:
                continue
            repaired_label = translated_role_size_label(
                source_label,
                locale,
                product_context=product_context,
                table_child_role=table_child_role,
            )
            if not repaired_label:
                continue
            replacement_labels.append((source_label, repaired_label))
            all_replacement_labels.append((source_label, repaired_label))

            while next_row_index < len(translated_rows):
                translated_row_match = translated_rows[next_row_index]
                next_row_index += 1
                translated_row_html = translated_row_match.group(0)
                if not first_body_cell_text(translated_row_html):
                    continue
                new_row_html = replace_first_body_cell(translated_row_html, repaired_label)
                row_start, row_end = translated_row_match.span()
                translated_table_html = (
                    translated_table_html[:row_start]
                    + new_row_html
                    + translated_table_html[row_end:]
                )
                delta = len(new_row_html) - (row_end - row_start)
                if delta:
                    translated_rows = list(TABLE_ROW_RE.finditer(translated_table_html))
                    next_row_index = min(next_row_index, len(translated_rows))
                break

        for source_label, repaired_label in replacement_labels:
            translated_table_html = re.sub(re.escape(source_label), repaired_label, translated_table_html)

        repaired = repaired[:translated_start] + translated_table_html + repaired[translated_end:]
        offset += len(translated_table_html) - (translated_end - translated_start)

    # Catch English labels that leaked outside the chart, such as "Child 1-2Y-10Y".
    for source_label, repaired_label in sorted(set(all_replacement_labels), key=lambda item: len(item[0]), reverse=True):
        repaired = repaired.replace(source_label, repaired_label)

    return repaired


def repair_product_html_translation(
    source_html: str,
    translated_html: str,
    locale: str,
    product_context: dict[str, Any] | None = None,
) -> str:
    repaired = repair_product_html_size_labels(
        source_html,
        translated_html,
        locale,
        product_context=product_context,
    )
    return repair_common_product_html_labels(repaired, locale)


def deterministic_option_translation(
    resource_type: str,
    key: str,
    value: str,
    locale: str,
    product_context: dict[str, Any] | None = None,
) -> str | None:
    source = clean(value)
    if not source:
        return None

    if resource_type == "ProductOption" and key == "name":
        return translated_option_name(source, locale)

    if resource_type != "ProductOptionValue" or key not in {"name", "value"}:
        return None

    garment = translated_garment(source, locale)
    if garment:
        return garment

    return translated_role_size_label(source, locale, product_context=product_context)


def should_translate_field(resource_type: str, key: str, value: str, *, option_resources_only: bool = False) -> bool:
    if option_resources_only and resource_type not in OPTION_RESOURCE_TYPES:
        return False
    allowed_fields = RESOURCE_FIELD_ALLOWLIST.get(resource_type)
    if not allowed_fields or key not in allowed_fields:
        return False
    return human_facing(value, key)


def collect_resource_snapshots(
    client: ShopifyClient,
    product_gid: str,
    locales: list[str],
    nested_limit: int,
) -> list[ResourceSnapshot]:
    product_snapshot = client.fetch_resource(product_gid, locales, nested_limit)
    snapshots_by_id: dict[str, ResourceSnapshot] = {product_snapshot.resource_id: product_snapshot}

    option_ids = []
    for nested in product_snapshot.nested_resources:
        if nested.resource_type == "ProductOption":
            snapshots_by_id[nested.resource_id] = nested
            option_ids.append(nested.resource_id)
        elif nested.resource_type == "Metafield":
            snapshots_by_id[nested.resource_id] = nested

    for option_id in option_ids:
        option_snapshot = client.fetch_resource(option_id, locales, nested_limit)
        snapshots_by_id[option_id] = option_snapshot
        for nested in option_snapshot.nested_resources:
            if nested.resource_type == "ProductOptionValue":
                snapshots_by_id[nested.resource_id] = nested

    for option_value_id in client.product_option_value_ids(product_gid):
        if option_value_id in snapshots_by_id:
            continue
        option_value_snapshot = client.fetch_resource(option_value_id, locales, nested_limit)
        if option_value_snapshot.resource_type == "ProductOptionValue":
            snapshots_by_id[option_value_id] = option_value_snapshot

    return list(snapshots_by_id.values())


def build_translation_payload(
    snapshots: list[ResourceSnapshot],
    locales: list[str],
    translator: TranslationBackend,
    *,
    progress_prefix: str,
    product: RecentProduct | None = None,
    force_refresh: bool = False,
    option_resources_only: bool = False,
    deterministic_repairs_only: bool = False,
) -> tuple[dict[str, list[dict[str, str]]], dict[str, Any]]:
    pending_rows = []
    texts_by_locale: dict[str, list[str]] = defaultdict(list)
    skipped = defaultdict(int)
    product_context = infer_product_context(product, snapshots)

    for snapshot in snapshots:
        for item in snapshot.translatable_content:
            key = item["key"]
            default_value = item["value"]
            digest = item["digest"]
            if not should_translate_field(
                snapshot.resource_type,
                key,
                default_value,
                option_resources_only=option_resources_only,
            ):
                skipped[f"filtered:{snapshot.resource_type}:{key}"] += 1
                continue
            for locale in locales:
                existing = snapshot.existing_translations.get((locale, key))
                deterministic_value = deterministic_option_translation(
                    snapshot.resource_type,
                    key,
                    default_value,
                    locale,
                    product_context=product_context,
                )
                repaired_existing_value = None
                if (
                    existing
                    and clean(existing.value)
                    and snapshot.resource_type == "Product"
                    and key == "body_html"
                ):
                    repaired_existing_value = repair_product_html_translation(
                        default_value,
                        existing.value,
                        locale,
                        product_context=product_context,
                    )
                if (
                    existing
                    and clean(existing.value)
                    and not existing.outdated
                    and not TranslationBackend._contains_placeholder_tokens(existing.value)  # noqa: SLF001
                    and (
                        deterministic_value is None
                        or clean(deterministic_value) == clean(existing.value)
                    )
                    and (
                        repaired_existing_value is None
                        or clean(repaired_existing_value) == clean(existing.value)
                    )
                    and not force_refresh
                ):
                    skipped[f"already_current:{locale}"] += 1
                    continue
                if (
                    deterministic_repairs_only
                    and repaired_existing_value is None
                    and deterministic_value is None
                ):
                    skipped[f"deterministic_repair_only:{locale}"] += 1
                    continue
                pending_rows.append(
                    {
                        "resource_id": snapshot.resource_id,
                        "resource_type": snapshot.resource_type,
                        "key": key,
                        "locale": locale,
                        "default": default_value,
                        "digest": digest,
                        "outdated": bool(existing.outdated) if existing else False,
                        "existing_value": clean(existing.value) if existing else "",
                        "deterministic_value": repaired_existing_value
                        if repaired_existing_value is not None
                        else deterministic_value,
                    }
                )
                if repaired_existing_value is None and deterministic_value is None:
                    texts_by_locale[locale].append(default_value)

    translated_by_locale: dict[str, dict[str, str | None]] = {}
    for locale, texts in texts_by_locale.items():
        unique_texts = list(dict.fromkeys(texts))
        translated_by_locale[locale] = translator.translate_many(
            locale,
            unique_texts,
            progress_label=f"{progress_prefix} locale={locale}",
        )

    payload_by_resource: dict[str, list[dict[str, str]]] = defaultdict(list)
    translated_count = 0
    failed_count = 0
    for row in pending_rows:
        translated_value = row.get("deterministic_value")
        if translated_value is not None:
            skipped[f"deterministic:{row['locale']}"] += 1
        else:
            translated_value = translated_by_locale[row["locale"]].get(row["default"])
        if translated_value is None:
            failed_count += 1
            skipped[f"translation_failed:{row['locale']}"] += 1
            continue
        if row["resource_type"] == "Product" and row["key"] == "body_html":
            translated_value = repair_product_html_translation(
                row["default"],
                translated_value,
                row["locale"],
                product_context=product_context,
            )
        if row["existing_value"] and clean(translated_value) == row["existing_value"] and not row.get("outdated"):
            skipped[f"already_matches_generated:{row['locale']}"] += 1
            continue
        payload_by_resource[row["resource_id"]].append(
            {
                "locale": row["locale"],
                "key": row["key"],
                "value": translated_value,
                "translatableContentDigest": row["digest"],
            }
        )
        translated_count += 1

    summary = {
        "resource_count": len(snapshots),
        "candidate_count": len(pending_rows),
        "translated_count": translated_count,
        "failed_count": failed_count,
        "skipped": dict(sorted(skipped.items())),
        "product_context": product_context,
        "resources": {
            snapshot.resource_id: snapshot.resource_type for snapshot in snapshots
        },
        "deterministic_repairs_only": deterministic_repairs_only,
    }
    return payload_by_resource, summary


def process_product(
    client: ShopifyClient,
    translator: TranslationBackend,
    product: RecentProduct,
    locales: list[str],
    *,
    nested_limit: int,
    pause_ms: int,
    execute: bool,
    force_refresh: bool = False,
    option_resources_only: bool = False,
    deterministic_repairs_only: bool = False,
) -> dict[str, Any]:
    snapshots = collect_resource_snapshots(client, product.product_gid, locales, nested_limit)
    payload_by_resource, summary = build_translation_payload(
        snapshots,
        locales,
        translator,
        progress_prefix=f"product={product.handle}",
        product=product,
        force_refresh=force_refresh,
        option_resources_only=option_resources_only,
        deterministic_repairs_only=deterministic_repairs_only,
    )

    registered_counts = {}
    if execute:
        for resource_id, translations in payload_by_resource.items():
            if not translations:
                continue
            result = client.register_translations(resource_id, translations)
            registered_counts[resource_id] = len(result.get("translations") or [])
            if pause_ms > 0:
                time.sleep(pause_ms / 1000)

    summary.update(
        {
            "handle": product.handle,
            "product_id": product.product_id,
            "created_at": product.created_at,
            "locales": locales,
            "resource_payload_counts": {key: len(value) for key, value in payload_by_resource.items()},
            "registered_counts": registered_counts,
            "execute": bool(execute),
            "force_refresh": bool(force_refresh),
            "option_resources_only": bool(option_resources_only),
            "deterministic_repairs_only": bool(deterministic_repairs_only),
        }
    )
    return summary


def merge_payload(
    target: dict[str, list[dict[str, str]]],
    source: dict[str, list[dict[str, str]]],
) -> None:
    for resource_id, translations in source.items():
        target.setdefault(resource_id, []).extend(translations)


def write_bulk_jsonl(payload_by_resource: dict[str, list[dict[str, str]]], path: Path) -> dict[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    resource_count = 0
    translation_count = 0
    with path.open("w", encoding="utf-8") as handle:
        for resource_id, translations in payload_by_resource.items():
            deduped = []
            seen = set()
            for item in translations:
                signature = (item["locale"], item["key"])
                if signature in seen:
                    continue
                seen.add(signature)
                deduped.append(item)
            if not deduped:
                continue
            resource_count += 1
            translation_count += len(deduped)
            handle.write(json.dumps({"resourceId": resource_id, "translations": deduped}, ensure_ascii=False) + "\n")
    return {"resource_count": resource_count, "translation_count": translation_count}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--state-path", default=str(DEFAULT_STATE_PATH), help="Persistent worker state path.")
    parser.add_argument("--jsonl-log", default=str(DEFAULT_LOG_PATH), help="Append-only JSONL log path.")
    parser.add_argument("--cache-path", default=str(DEFAULT_CACHE_PATH), help="Shared translation cache path.")
    parser.add_argument("--bulk-jsonl-path", default=str(DEFAULT_BULK_JSONL_PATH), help="JSONL path for staged bulk translation repair.")
    parser.add_argument("--glossary", default=str(DEFAULT_GLOSSARY), help="Optional glossary JSON path.")
    parser.add_argument("--locales", default="", help="Comma-separated locale list. Defaults to live published non-primary shop locales.")
    parser.add_argument("--handles", default="", help="Comma-separated product handles to process, bypassing cursor state.")
    parser.add_argument("--created-since", default="", help="Process recent products created on/after this ISO timestamp, bypassing cursor state.")
    parser.add_argument("--min-age-seconds", type=int, default=300, help="Only process products older than this.")
    parser.add_argument("--page-size", type=int, default=25, help="Recent products page size.")
    parser.add_argument("--max-pages", type=int, default=4, help="Maximum recent-products pages per run.")
    parser.add_argument("--max-products-per-run", type=int, default=3, help="Maximum products handled per run.")
    parser.add_argument("--max-nested-resources", type=int, default=DEFAULT_NESTED_LIMIT, help="Nested translatable resources fetched per product or option.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live translation writes.")
    parser.add_argument("--execute", action="store_true", help="Apply translations live instead of dry-run.")
    parser.add_argument("--bulk", action="store_true", help="Stage one bulk translationsRegister mutation instead of direct per-resource writes.")
    parser.add_argument("--force-refresh", action="store_true", help="Rebuild current translations and rewrite only values that differ.")
    parser.add_argument("--option-resources-only", action="store_true", help="Only repair ProductOption and ProductOptionValue translations.")
    parser.add_argument(
        "--deterministic-repairs-only",
        action="store_true",
        help="Only stage deterministic option/body size-label repairs; skip machine translation for missing prose.",
    )
    parser.add_argument("--initialize-now", action="store_true", help="Initialize first-run cursor to now.")
    parser.add_argument("--bootstrap-hours", type=int, default=0, help="On first run only, process products this many hours back.")
    args = parser.parse_args()

    state_path = Path(args.state_path).expanduser()
    log_path = Path(args.jsonl_log).expanduser() if args.jsonl_log else None
    cache_path = Path(args.cache_path).expanduser()

    state = initialize_state(
        state_path,
        initialize_now=args.initialize_now,
        bootstrap_hours=args.bootstrap_hours,
    )

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    client = ShopifyClient(store_domain, access_token)
    locales = resolve_target_locales(client, args.locales)
    if not locales:
        raise SystemExit("No non-primary published locales were found to translate.")

    translator = TranslationBackend(
        cache_path,
        args.glossary,
        batch_size=60,
        pause_seconds=0.05,
        request_timeout=15,
        batch_char_limit=12000,
    )

    explicit_handles = [item.strip() for item in args.handles.split(",") if item.strip()]
    created_since = clean(args.created_since)

    if explicit_handles:
        eligible_new = client.products_by_handles(explicit_handles)
    else:
        recent_products = client.recent_products(max_pages=max(args.max_pages, 1), page_size=max(args.page_size, 1))
        if created_since:
            since_dt = parse_iso8601(created_since)
            eligible_new = [
                product
                for product in recent_products
                if parse_iso8601(product.created_at) >= since_dt
            ]
        else:
            eligible_new = [product for product in recent_products if is_newer_than_cursor(product, state)]
    eligible_new.sort(key=lambda item: (item.created_at, item.product_id))

    if args.bulk:
        merged_payload: dict[str, list[dict[str, str]]] = {}
        product_summaries = []
        processed_count = 0
        blocked_by_error = False
        min_age_delta = timedelta(seconds=max(args.min_age_seconds, 0))

        for product in eligible_new:
            if processed_count >= max(args.max_products_per_run, 1):
                break

            if clean(product.status).upper() == "ARCHIVED":
                append_log(
                    log_path,
                    {
                        "event": "skipped",
                        "reason": "archived",
                        "product_id": product.product_id,
                        "handle": product.handle,
                        "created_at": product.created_at,
                    },
                )
                processed_count += 1
                continue

            created_at_dt = parse_iso8601(product.created_at)
            if utc_now() - created_at_dt < min_age_delta:
                append_log(
                    log_path,
                    {
                        "event": "deferred",
                        "reason": "product_too_new",
                        "product_id": product.product_id,
                        "handle": product.handle,
                        "created_at": product.created_at,
                    },
                )
                continue

            try:
                snapshots = collect_resource_snapshots(
                    client,
                    product.product_gid,
                    locales,
                    max(args.max_nested_resources, 1),
                )
                payload_by_resource, summary = build_translation_payload(
                    snapshots,
                    locales,
                    translator,
                    progress_prefix=f"product={product.handle}",
                    product=product,
                    force_refresh=args.force_refresh,
                    option_resources_only=args.option_resources_only,
                    deterministic_repairs_only=args.deterministic_repairs_only,
                )
                merge_payload(merged_payload, payload_by_resource)
                summary.update(
                    {
                        "handle": product.handle,
                        "product_id": product.product_id,
                        "created_at": product.created_at,
                        "locales": locales,
                        "resource_payload_counts": {
                            key: len(value) for key, value in payload_by_resource.items()
                        },
                        "execute": bool(args.execute),
                        "bulk": True,
                        "force_refresh": bool(args.force_refresh),
                        "option_resources_only": bool(args.option_resources_only),
                        "deterministic_repairs_only": bool(args.deterministic_repairs_only),
                    }
                )
                product_summaries.append(summary)
                append_log(
                    log_path,
                    {
                        "event": "bulk_prepared",
                        "product_id": product.product_id,
                        "handle": product.handle,
                        "created_at": product.created_at,
                        "summary": summary,
                    },
                )
                processed_count += 1
            except Exception as exc:  # noqa: BLE001
                blocked_by_error = True
                append_log(
                    log_path,
                    {
                        "event": "error",
                        "product_id": product.product_id,
                        "handle": product.handle,
                        "created_at": product.created_at,
                        "message": str(exc),
                    },
                )
                break

        bulk_jsonl_path = Path(args.bulk_jsonl_path).expanduser()
        bulk_counts = write_bulk_jsonl(merged_payload, bulk_jsonl_path)
        bulk_result = None
        if args.execute and bulk_counts["translation_count"] > 0:
            staged_upload_path = client.staged_upload(bulk_jsonl_path)
            operation_id = client.run_bulk_translation_mutation(staged_upload_path)
            bulk_result = client.poll_bulk_operation(operation_id)

        report = {
            "store_domain": store_domain,
            "locales": locales,
            "candidate_products": len(eligible_new),
            "processed_products": processed_count,
            "blocked_by_error": blocked_by_error,
            "execute": bool(args.execute),
            "bulk": True,
            "option_resources_only": bool(args.option_resources_only),
            "deterministic_repairs_only": bool(args.deterministic_repairs_only),
            "bulk_counts": bulk_counts,
            "bulk_jsonl_path": str(bulk_jsonl_path),
            "bulk_result": bulk_result,
            "cache_path": str(cache_path),
        }
        append_log(log_path, {"event": "bulk_complete", "summary": report})
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    finalized: list[RecentProduct] = []
    processed_count = 0
    blocked_by_error = False
    min_age_delta = timedelta(seconds=max(args.min_age_seconds, 0))

    for product in eligible_new:
        if processed_count >= max(args.max_products_per_run, 1):
            break

        if clean(product.status).upper() == "ARCHIVED":
            append_log(
                log_path,
                {
                    "event": "skipped",
                    "reason": "archived",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                },
            )
            if args.execute and not (explicit_handles or created_since):
                finalized.append(product)
                processed_count += 1
            continue

        created_at_dt = parse_iso8601(product.created_at)
        if utc_now() - created_at_dt < min_age_delta:
            append_log(
                log_path,
                {
                    "event": "deferred",
                    "reason": "product_too_new",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                },
            )
            continue

        try:
            summary = process_product(
                client,
                translator,
                product,
                locales,
                nested_limit=max(args.max_nested_resources, 1),
                pause_ms=max(args.pause_ms, 0),
                execute=args.execute,
                force_refresh=args.force_refresh,
                option_resources_only=args.option_resources_only,
                deterministic_repairs_only=args.deterministic_repairs_only,
            )
            append_log(
                log_path,
                {
                    "event": "processed",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                    "summary": summary,
                },
            )
            processed_count += 1
            if args.execute and not (explicit_handles or created_since):
                finalized.append(product)
                update_cursor_state(state, [product])
                state["last_run_at"] = isoformat_utc(utc_now())
                save_state(state_path, state)
        except Exception as exc:  # noqa: BLE001
            blocked_by_error = True
            append_log(
                log_path,
                {
                    "event": "error",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                    "message": str(exc),
                },
            )
            break

    if args.execute and finalized and not (explicit_handles or created_since):
        update_cursor_state(state, finalized)
        state["last_run_at"] = isoformat_utc(utc_now())
        save_state(state_path, state)

    print(
        json.dumps(
            {
                "store_domain": store_domain,
                "locales": locales,
                "candidate_products": len(eligible_new),
                "processed_products": processed_count,
                "finalized_product_ids": [item.product_id for item in finalized],
                "blocked_by_error": blocked_by_error,
                "execute": bool(args.execute),
                "option_resources_only": bool(args.option_resources_only),
                "deterministic_repairs_only": bool(args.deterministic_repairs_only),
                "state_path": str(state_path),
                "cache_path": str(cache_path),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
