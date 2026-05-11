#!/usr/bin/env python3
"""Build local-only keyword/RSA quality artifacts for paid-growth continuation.

This script creates review and evidence files only. It does not create any
Google Ads or Pinterest upload file, and it does not touch external accounts.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PACKET = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-keyword-quality-upgrade"
SPLIT_DIR = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs"
US_CSV = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-aggressive-controlled-growth-build/nonbrand_search_paused_rebuild/web_bulk_upload/00_nonbrand_search_paused_rebuild_web_bulk.csv"
AUTHORITY_PACKET = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep"

DATE = "2026-05-10"
ANCHOR = "AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-keyword-quality-expert-hardening"

THEMES = [
    "Mommy & Me Dresses",
    "Family Matching",
    "Matching Pajamas",
    "Matching Swimwear",
    "Daddy & Me",
]

MARKET_STATE = {
    "US": ("23827590655", "BUILT_PAUSED_US_NONBRAND_DO_NOT_DUPLICATE", "DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506", "en-US"),
    "GB": ("23838895360", "BUILT_PAUSED_READBACK_PASSED", "DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-GB"),
    "CA": ("23834423669", "BUILT_PAUSED_READBACK_PASSED", "DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-CA"),
    "AU": ("23834424182", "BUILT_PAUSED_READBACK_PASSED", "DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-AU"),
    "CH": ("23834425358", "BUILT_PAUSED_READBACK_PASSED", "DLM_CH_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-CH"),
    "DK": ("23838969244", "BUILT_PAUSED_READBACK_PASSED", "DLM_DK_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-DK"),
    "DE": ("23834427575", "BUILT_PAUSED_READBACK_PASSED", "DLM_DE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-DE"),
    "NL": ("23829110118", "BUILT_PAUSED_READBACK_PASSED", "DLM_NL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-NL"),
    "SE": ("23838970036", "BUILT_PAUSED_READBACK_PASSED", "DLM_SE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-SE"),
    "ES": ("23829133584", "BUILT_PAUSED_READBACK_PASSED", "DLM_ES_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-ES"),
    "IT": ("23829232530", "BUILT_PAUSED_READBACK_PASSED", "DLM_IT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-IT"),
    "PL": ("23829238698", "BUILT_PAUSED_READBACK_PASSED", "DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-PL"),
    "CZ": ("23829253812", "BUILT_PAUSED_READBACK_PASSED", "DLM_CZ_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-CZ"),
    "RO": ("", "ABSENT_UPLOAD_THROTTLE_BLOCKED_LOCAL_SPLIT_READY", "DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-RO"),
    "PT": ("", "ABSENT_BEHIND_RO_ONE_COUNTRY_GUARD_LOCAL_SPLIT_READY", "DLM_PT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-PT"),
    "GR": ("", "ABSENT_BEHIND_RO_ONE_COUNTRY_GUARD_LOCAL_SPLIT_READY", "DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-GR"),
    "FR": ("", "PARKED_STALE_ERROR_NO_CHANGES_LOCAL_SPLIT_READY", "DLM_FR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-FR"),
    "BE": ("", "PARKED_UPLOAD_THROTTLE_AND_LANGUAGE_SPLIT_LOCAL_SPLIT_READY", "DLM_BE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507", "en-BE"),
}

LOCALIZED_MARKET_TO_LOCALE = {
    "ES": ["es-ES"],
    "IT": ["it-IT"],
    "RO": ["ro-RO"],
    "PT": ["pt-PT"],
    "DE": ["de-DE"],
    "NL": ["nl-NL"],
    "FR": ["fr-FR"],
    "BE": ["fr-BE", "nl-BE"],
    "SE": ["sv-SE"],
    "DK": ["da-DK"],
    "PL": ["pl-PL"],
    "CZ": ["cs-CZ"],
    "GR": ["el-GR"],
}

LOCALE_STATUS = {
    "es-ES": ("ES", "Spanish", "CONCEPT_READY_NATIVE_REVIEW_REQUIRED", "Spain review for accents, register, and search phrasing."),
    "it-IT": ("IT", "Italian", "CONCEPT_READY_NATIVE_REVIEW_REQUIRED", "Italian fluency and swimwear terminology review."),
    "ro-RO": ("RO", "Romanian", "CONCEPT_READY_NATIVE_REVIEW_REQUIRED", "Romanian diacritics, search phrasing, and RON economics review."),
    "pt-PT": ("PT", "Portuguese", "PLATFORM_USE_BLOCKED_PT_PT_VS_PT_BR_STOREFRONT", "Portugal copy is pt-PT but storefront behavior previously read as pt-BR."),
    "de-DE": ("DE", "German", "NATIVE_REVIEW_REQUIRED_LANDING_LANGUAGE_QA", "German register and native landing-language proof required."),
    "nl-NL": ("NL", "Dutch", "NATIVE_REVIEW_REQUIRED_LANDING_LANGUAGE_QA", "Dutch anglicism and native landing-language proof required."),
    "fr-FR": ("FR", "French", "NATIVE_REVIEW_REQUIRED_LANDING_LANGUAGE_QA", "French register and native landing-language proof required."),
    "fr-BE": ("BE", "French for Belgium", "PLATFORM_USE_BLOCKED_BE_FR_NL_SPLIT", "Belgium French/Dutch split decision and route proof required."),
    "nl-BE": ("BE", "Dutch for Belgium", "PLATFORM_USE_BLOCKED_BE_FR_NL_SPLIT", "Belgium French/Dutch split decision and route proof required."),
    "sv-SE": ("SE", "Swedish", "NATIVE_REVIEW_REQUIRED_LANDING_LANGUAGE_QA", "Swedish singular/plural and native landing-language proof required."),
    "da-DK": ("DK", "Danish", "PLATFORM_USE_BLOCKED_DANISH_REWRITE", "Prior Danish row contained likely non-Danish wording; native rewrite required."),
    "pl-PL": ("PL", "Polish", "NATIVE_REVIEW_REQUIRED_LANDING_LANGUAGE_QA", "Polish grammar/case and native landing-language proof required."),
    "cs-CZ": ("CZ", "Czech", "NATIVE_REVIEW_REQUIRED_LANDING_LANGUAGE_QA", "Czech formal/informal and native landing-language proof required."),
    "el-GR": ("GR", "Greek", "NATIVE_REVIEW_REQUIRED_LANDING_LANGUAGE_QA", "Greek phrasing, accents, and native landing-language proof required."),
}

NATIVE_KEYWORDS = {
    "es-ES": {
        "Mommy & Me Dresses": ["vestidos mamá e hija", "vestidos madre hija", "ropa madre e hija", "looks mamá e hija", "conjuntos mamá e hija"],
        "Family Matching": ["ropa familiar a juego", "looks familiares", "outfits familiares", "conjuntos familiares", "looks familia coordinados"],
        "Matching Pajamas": ["pijamas familiares", "pijamas a juego", "pijamas madre hija", "pijamas familia a juego", "pijamas mamá e hija"],
        "Matching Swimwear": ["bañadores familiares", "trajes de baño familiares", "bañadores madre hija", "moda baño familiar", "bañadores a juego"],
        "Daddy & Me": ["ropa papá e hijo", "looks padre e hijo", "outfits padre hijo", "camisas papá e hijo", "ropa padre hijo a juego"],
    },
    "it-IT": {
        "Mommy & Me Dresses": ["abiti mamma figlia", "vestiti madre figlia", "look mamma figlia", "abiti mamma e figlia", "outfit mamma figlia"],
        "Family Matching": ["outfit famiglia coordinati", "look famiglia", "abiti coordinati famiglia", "vestiti famiglia coordinati", "look famiglia coordinati"],
        "Matching Pajamas": ["pigiami famiglia", "pigiami coordinati", "pigiami mamma figlia", "pigiami famiglia coordinati", "pigiami mamma e figlia"],
        "Matching Swimwear": ["costumi famiglia", "costumi coordinati famiglia", "costumi mamma figlia", "costumi da bagno famiglia", "moda mare famiglia"],
        "Daddy & Me": ["outfit papà figlio", "look padre figlio", "magliette papà figlio", "camicie papà figlio", "vestiti papà figlio"],
    },
    "pt-PT": {
        "Mommy & Me Dresses": ["vestidos mãe filha", "vestidos mãe e filha", "looks mãe filha", "roupa mãe e filha", "conjuntos mãe filha"],
        "Family Matching": ["roupa família a combinar", "looks família", "roupa familiar", "conjuntos família", "roupa família coordenada"],
        "Matching Pajamas": ["pijamas família", "pijamas a combinar", "pijamas mãe filha", "pijamas família a combinar", "pijamas mãe e filha"],
        "Matching Swimwear": ["moda praia família", "fatos de banho família", "moda praia a combinar", "fatos de banho mãe filha", "praia em família"],
        "Daddy & Me": ["looks pai filho", "roupa pai e filho", "pai filho a combinar", "camisas pai filho", "roupa pai filho"],
    },
    "ro-RO": {
        "Mommy & Me Dresses": ["rochii mamă fiică", "rochii mama fiica", "ținute mamă fiică", "haine mamă fiică", "rochii asortate mamă fiică"],
        "Family Matching": ["ținute familie asortate", "haine familie asortate", "outfit familie", "haine familie", "look familie asortat"],
        "Matching Pajamas": ["pijamale familie", "pijamale asortate", "pijamale mamă fiică", "pijamale familie asortate", "pijamale mamă copil"],
        "Matching Swimwear": ["costume baie familie", "costume baie asortate", "costume baie mamă fiică", "costume familie asortate", "modă baie familie"],
        "Daddy & Me": ["ținute tată copil", "haine tată fiu", "tată copil asortat", "haine tată copil", "look tată copil"],
    },
    "de-DE": {
        "Mommy & Me Dresses": ["mama tochter kleider", "mutter tochter kleider", "partnerlook kleider", "mama kind kleider", "mutter kind outfits"],
        "Family Matching": ["familien outfits", "partnerlook familie", "matching familie outfits", "familienkleidung", "familien look"],
        "Matching Pajamas": ["familien pyjamas", "partnerlook pyjama", "mama kind pyjama", "familien schlafanzug", "pyjama familie"],
        "Matching Swimwear": ["bademode familie", "partnerlook bademode", "mama kind badeanzug", "familien badeanzug", "badeanzug mutter tochter"],
        "Daddy & Me": ["papa kind outfits", "vater kind outfits", "vater sohn shirts", "papa sohn shirts", "vater kind kleidung"],
    },
    "nl-NL": {
        "Mommy & Me Dresses": ["mama dochter jurken", "moeder dochter jurken", "matching jurken", "mama dochter kleding", "moeder dochter outfits"],
        "Family Matching": ["familie outfits", "matching familie kleding", "familie look", "familiekleding", "bijpassende familie outfits"],
        "Matching Pajamas": ["familie pyjama's", "matching pyjama's", "moeder dochter pyjama", "mama dochter pyjama", "familie pyjama set"],
        "Matching Swimwear": ["familie badmode", "matching badmode", "mama kind badpak", "moeder dochter badpak", "badmode familie"],
        "Daddy & Me": ["papa kind outfits", "vader kind kleding", "vader zoon shirts", "papa zoon shirts", "vader kind outfits"],
    },
    "fr-FR": {
        "Mommy & Me Dresses": ["robes mère fille", "robes maman fille", "looks mère fille", "tenues mère fille", "robes assorties mère fille"],
        "Family Matching": ["tenues famille assorties", "looks famille", "vêtements famille", "tenues familiales", "vêtements assortis famille"],
        "Matching Pajamas": ["pyjamas famille", "pyjamas assortis", "pyjamas maman fille", "pyjamas mère fille", "pyjamas famille assortis"],
        "Matching Swimwear": ["maillots famille", "maillots assortis", "maillots mère fille", "maillots maman fille", "maillots de bain famille"],
        "Daddy & Me": ["tenues père enfant", "looks papa enfant", "tenues papa fils", "chemises père fils", "vêtements papa fils"],
    },
    "fr-BE": {},
    "nl-BE": {},
    "sv-SE": {
        "Mommy & Me Dresses": ["mamma dotter klänningar", "mor dotter klänningar", "matchande klänningar", "mamma barn klänningar", "matchande mamma dotter"],
        "Family Matching": ["familjeoutfits", "matchande familj", "familjekläder", "matchande familjekläder", "familj kläder"],
        "Matching Pajamas": ["familjepyjamas", "matchande pyjamas", "mamma barn pyjamas", "familj pyjamas", "pyjamas familj"],
        "Matching Swimwear": ["familjebadkläder", "matchande badkläder", "mamma barn badkläder", "badkläder familj", "badmode familj"],
        "Daddy & Me": ["pappa barn outfits", "far barn outfits", "pappa son kläder", "far son kläder", "matchande pappa barn"],
    },
    "da-DK": {
        "Mommy & Me Dresses": ["mor datter kjoler", "mor og datter kjoler", "matchende kjoler", "mor barn kjoler", "matchende mor datter"],
        "Family Matching": ["familie outfits", "matchende familie", "familietøj", "matchende familietøj", "familie tøj"],
        "Matching Pajamas": ["familie pyjamas", "matchende pyjamas", "mor barn pyjamas", "familie nattøj", "pyjamas familie"],
        "Matching Swimwear": ["familie badetøj", "matchende badetøj", "mor barn badetøj", "badetøj familie", "badetøj mor barn"],
        "Daddy & Me": ["far barn outfits", "far søn tøj", "far barn looks", "matchende far barn", "far og søn tøj"],
    },
    "pl-PL": {
        "Mommy & Me Dresses": ["sukienki mama córka", "sukienki dla mamy i córki", "styl mama córka", "ubrania mama córka", "zestawy mama córka"],
        "Family Matching": ["stylizacje rodzinne", "ubrania rodzinne", "dopasowane stroje rodzinne", "rodzinne zestawy ubrań", "ubrania dla rodziny"],
        "Matching Pajamas": ["piżamy rodzinne", "piżamy dla rodziny", "piżamy mama dziecko", "dopasowane piżamy", "piżamy mama córka"],
        "Matching Swimwear": ["stroje kąpielowe rodzina", "moda plażowa rodziny", "stroje mama dziecko", "stroje kąpielowe rodzinne", "stroje rodzinne plaża"],
        "Daddy & Me": ["stroje tata dziecko", "styl tata dziecko", "ubrania tata syn", "koszule tata syn", "ubrania tata dziecko"],
    },
    "cs-CZ": {
        "Mommy & Me Dresses": ["šaty máma dcera", "šaty pro mámu a dceru", "look máma dcera", "oblečení máma dcera", "sladěné šaty máma dcera"],
        "Family Matching": ["rodinné outfity", "sladěné outfity", "rodinné oblečení", "oblečení pro rodinu", "sladěné rodinné oblečení"],
        "Matching Pajamas": ["rodinná pyžama", "sladěná pyžama", "pyžama máma dítě", "pyžama pro rodinu", "pyžama máma dcera"],
        "Matching Swimwear": ["rodinné plavky", "sladěné plavky", "plavky máma dítě", "plavky pro rodinu", "plavky rodina"],
        "Daddy & Me": ["táta dítě outfity", "oblečení táta syn", "look táta dítě", "táta syn košile", "oblečení táta dítě"],
    },
    "el-GR": {
        "Mommy & Me Dresses": ["φορέματα μαμά κόρη", "στυλ μαμά κόρη", "ασορτί φορέματα", "ρούχα μαμά κόρη", "φορέματα μαμάς κόρης"],
        "Family Matching": ["οικογενειακά σύνολα", "ασορτί οικογένεια", "οικογενειακά ρούχα", "ασορτί οικογενειακά ρούχα", "σύνολα οικογένειας"],
        "Matching Pajamas": ["οικογενειακές πιτζάμες", "ασορτί πιτζάμες", "πιτζάμες μαμά παιδί", "πιτζάμες οικογένειας", "πιτζάμες μαμά κόρη"],
        "Matching Swimwear": ["οικογενειακά μαγιό", "ασορτί μαγιό", "μαγιό μαμά παιδί", "μαγιό οικογένειας", "μαγιό μαμά κόρη"],
        "Daddy & Me": ["σύνολα μπαμπά παιδί", "στυλ μπαμπά παιδί", "ρούχα μπαμπά γιος", "ρούχα μπαμπά παιδί", "ασορτί μπαμπά παιδί"],
    },
}
NATIVE_KEYWORDS["fr-BE"] = NATIVE_KEYWORDS["fr-FR"]
NATIVE_KEYWORDS["nl-BE"] = NATIVE_KEYWORDS["nl-NL"]

NEGATIVE_KEYWORD_REVIEW_PLAN = {
    "es-ES": ["gratis", "patrón", "patrones", "coser", "costura", "segunda mano", "usado", "mayorista", "disfraz", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "it-IT": ["gratis", "cartamodello", "cartamodelli", "cucire", "cucito", "seconda mano", "usato", "ingrosso", "costume", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "pt-PT": ["grátis", "molde", "moldes", "costurar", "costura", "segunda mão", "usado", "grossista", "fantasia", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "ro-RO": ["gratis", "tipar", "tipare", "cusut", "croitorie", "second hand", "folosit", "angro", "costum", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "de-DE": ["kostenlos", "schnittmuster", "nähen", "nähanleitung", "gebraucht", "second hand", "großhandel", "kostüm", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "nl-NL": ["gratis", "patroon", "naaipatroon", "naaien", "tweedehands", "gebruikt", "groothandel", "kostuum", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "fr-FR": ["gratuit", "patron", "patrons", "couture", "coudre", "occasion", "seconde main", "grossiste", "costume", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "fr-BE": ["gratuit", "patron", "patrons", "couture", "coudre", "occasion", "seconde main", "grossiste", "costume", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "nl-BE": ["gratis", "patroon", "naaipatroon", "naaien", "tweedehands", "gebruikt", "groothandel", "kostuum", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "sv-SE": ["gratis", "mönster", "symönster", "sy", "sömnad", "begagnad", "second hand", "grossist", "kostym", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "da-DK": ["gratis", "mønster", "symønster", "sy", "syning", "brugt", "second hand", "engros", "kostume", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "pl-PL": ["za darmo", "wykrój", "wykroje", "szyć", "szycie", "używane", "second hand", "hurt", "kostium", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "cs-CZ": ["zdarma", "střih", "střihy", "šít", "šití", "použité", "second hand", "velkoobchod", "kostým", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
    "el-GR": ["δωρεάν", "πατρόν", "ράψιμο", "μεταχειρισμένα", "second hand", "χονδρική", "στολή", "pdf", "temu", "shein", "amazon", "aliexpress", "alibaba"],
}

COMMON_HEADLINES = {
    "es-ES": ["Dress Like Mommy", "Looks coordinados", "Para fotos familiares", "Tallas por separado", "Moda familiar", "Ideas para familia", "Momentos especiales", "Looks a juego", "Para madres e hijos", "Estilo familiar", "Compra looks a juego"],
    "it-IT": ["Dress Like Mommy", "Look coordinati", "Per foto in famiglia", "Taglie separate", "Moda famiglia", "Idee per famiglia", "Momenti speciali", "Look abbinati", "Per mamme e bambini", "Stile famiglia", "Scegli le taglie"],
    "pt-PT": ["Dress Like Mommy", "Looks coordenados", "Fotos em família", "Tamanhos separados", "Moda em família", "Ideias para família", "Momentos especiais", "Looks a combinar", "Para mães e filhos", "Estilo familiar", "Escolha tamanhos"],
    "ro-RO": ["Dress Like Mommy", "Ținute coordonate", "Poze de familie", "Mărimi separate", "Idei de familie", "Momente speciale", "Lookuri asortate", "Pentru mame și copii", "Stil de familie", "Alege mărimi", "Zile în familie"],
    "de-DE": ["Dress Like Mommy", "Abgestimmte Looks", "Für Familienfotos", "Größen separat wählen", "Familienmode", "Ideen für Familien", "Besondere Momente", "Partnerlook Ideen", "Für Eltern und Kinder", "Looks für Fotos", "Familienstil"],
    "nl-NL": ["Dress Like Mommy", "Gecoördineerde looks", "Voor familiefoto's", "Aparte maten kiezen", "Familiemode", "Ideeën voor familie", "Bijpassende looks", "Voor ouders en kinderen", "Looks voor foto's", "Familiestijl", "Speciale momenten"],
    "fr-FR": ["Dress Like Mommy", "Looks coordonnés", "Pour photos famille", "Tailles séparées", "Mode famille", "Idées pour famille", "Moments spéciaux", "Tenues assorties", "Pour parents et enfants", "Looks pour photos", "Style famille"],
    "fr-BE": ["Dress Like Mommy", "Looks coordonnés", "Pour photos famille", "Tailles séparées", "Mode famille", "Idées pour famille", "Moments spéciaux", "Tenues assorties", "Pour parents et enfants", "Looks pour photos", "Style famille"],
    "nl-BE": ["Dress Like Mommy", "Gecoördineerde looks", "Voor familiefoto's", "Aparte maten kiezen", "Familiemode", "Ideeën voor familie", "Bijpassende looks", "Voor ouders en kinderen", "Looks voor foto's", "Familiestijl", "Speciale momenten"],
    "sv-SE": ["Dress Like Mommy", "Samordnade looks", "För familjefoton", "Välj storlekar", "Familjemode", "Idéer för familjen", "Särskilda stunder", "Matchande looks", "För föräldrar och barn", "Looks för foton", "Familjestil"],
    "da-DK": ["Dress Like Mommy", "Koordinerede looks", "Til familiebilleder", "Vælg størrelser", "Familietøj", "Idéer til familien", "Særlige øjeblikke", "Matchende looks", "Til forældre og børn", "Looks til billeder", "Familiestil"],
    "pl-PL": ["Dress Like Mommy", "Dopasowane stroje", "Na rodzinne zdjęcia", "Osobne rozmiary", "Moda rodzinna", "Pomysły dla rodziny", "Wyjątkowe chwile", "Pasujące stylizacje", "Dla rodziców i dzieci", "Styl do zdjęć", "Styl rodzinny"],
    "cs-CZ": ["Dress Like Mommy", "Sladěné outfity", "Pro rodinné fotky", "Vyberte velikosti", "Rodinná móda", "Nápady pro rodinu", "Zvláštní chvíle", "Sladěné looky", "Pro rodiče a děti", "Looky na fotky", "Rodinný styl"],
    "el-GR": ["Dress Like Mommy", "Ασορτί σύνολα", "Για οικογενειακές φωτό", "Ξεχωριστά μεγέθη", "Μόδα για οικογένεια", "Ιδέες για οικογένεια", "Ξεχωριστές στιγμές", "Ασορτί στιλ", "Για γονείς και παιδιά", "Στιλ για φωτογραφίες", "Οικογενειακό στιλ"],
}

DESCRIPTION_TEMPLATES = {
    "es-ES": ["{t} para fotos, cumpleaños y días en familia.", "Elige tallas por separado para adultos, niñas y niños.", "Compra estilos coordinados para momentos especiales en familia.", "Usa la página del producto para elegir cada talla."],
    "it-IT": ["{t} per foto, compleanni e giornate in famiglia.", "Scegli taglie separate per adulti, bambine e bambini.", "Crea look coordinati per momenti speciali in famiglia.", "Usa la pagina prodotto per scegliere ogni taglia."],
    "pt-PT": ["{t} para fotos, aniversários e momentos em família.", "Escolha tamanhos separados para adultos e crianças.", "Crie looks coordenados para momentos especiais.", "Use a página do produto para escolher cada tamanho."],
    "ro-RO": ["{t} pentru poze, aniversări și zile în familie.", "Alege mărimi separate pentru adulți și copii.", "Creează ținute coordonate pentru momente speciale.", "Folosește pagina produsului pentru fiecare mărime."],
    "de-DE": ["{t} für Fotos, Geburtstage und Familienmomente.", "Wähle Größen für Erwachsene und Kinder separat.", "Erstelle abgestimmte Looks für besondere Momente.", "Nutze die Produktseite, um jede Größe auszuwählen."],
    "nl-NL": ["{t} voor foto's, verjaardagen en familiedagen.", "Kies aparte maten voor volwassenen en kinderen.", "Maak bijpassende looks voor bijzondere momenten.", "Gebruik de productpagina om elke maat te kiezen."],
    "fr-FR": ["{t} pour photos, anniversaires et moments en famille.", "Choisissez des tailles séparées pour adultes et enfants.", "Créez des looks coordonnés pour les moments spéciaux.", "Utilisez la page produit pour choisir chaque taille."],
    "fr-BE": ["{t} pour photos, anniversaires et moments en famille.", "Choisissez des tailles séparées pour adultes et enfants.", "Créez des looks coordonnés pour les moments spéciaux.", "Utilisez la page produit pour choisir chaque taille."],
    "nl-BE": ["{t} voor foto's, verjaardagen en familiedagen.", "Kies aparte maten voor volwassenen en kinderen.", "Maak bijpassende looks voor bijzondere momenten.", "Gebruik de productpagina om elke maat te kiezen."],
    "sv-SE": ["{t} för foton, födelsedagar och familjedagar.", "Välj separata storlekar för vuxna och barn.", "Skapa samordnade looks för särskilda stunder.", "Använd produktsidan för att välja varje storlek."],
    "da-DK": ["{t} til billeder, fødselsdage og familiedage.", "Vælg separate størrelser til voksne og børn.", "Skab koordinerede looks til særlige øjeblikke.", "Brug produktsiden til at vælge hver størrelse."],
    "pl-PL": ["{t} na zdjęcia, urodziny i rodzinne dni.", "Wybierz osobne rozmiary dla dorosłych i dzieci.", "Twórz dopasowane stylizacje na wyjątkowe chwile.", "Użyj strony produktu, aby wybrać każdy rozmiar."],
    "cs-CZ": ["{t} na fotky, narozeniny a rodinné dny.", "Vyberte zvlášť velikosti pro dospělé i děti.", "Tvořte sladěné outfity pro zvláštní chvíle.", "Použijte stránku produktu pro výběr každé velikosti."],
    "el-GR": ["{t} για φωτογραφίες, γιορτές και οικογενειακές μέρες.", "Επιλέξτε ξεχωριστά μεγέθη για ενήλικες και παιδιά.", "Δημιουργήστε ασορτί στιλ για ξεχωριστές στιγμές.", "Χρησιμοποιήστε τη σελίδα προϊόντος για κάθε μέγεθος."],
}

ENGLISH_EXPANSION = {
    "Mommy & Me Dresses": ["mommy and me matching dresses", "mother daughter matching dresses", "mommy and me outfits", "mommy daughter dresses", "mother daughter outfits"],
    "Family Matching": ["matching family outfits", "family matching clothes", "coordinated family outfits", "family photo outfits", "family matching sets"],
    "Matching Pajamas": ["matching family pajamas", "family pajama sets", "mommy and me pajamas", "mother daughter pajamas", "family matching sleepwear"],
    "Matching Swimwear": ["matching family swimsuits", "mommy and me swimsuits", "family swimwear", "mother daughter swimsuits", "matching family swimwear"],
    "Daddy & Me": ["daddy and me outfits", "father son matching outfits", "dad and son matching outfits", "daddy and me matching shirts", "father son matching shirts"],
}

FORBIDDEN_PATTERNS = [
    r"\bfast shipping\b",
    r"\bfree shipping\b",
    r"\bwarehouse\b",
    r"\bin stock now\b",
    r"\bguaranteed\b",
    r"\bbest seller\b",
    r"\bbestseller\b",
    r"\blimited time\b",
    r"\bdiscount\b",
    r"\bsale\b",
    r"\b1688\b",
    r"\balibaba\b",
    r"\baliexpress\b",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def norm_theme(ad_group: str) -> str:
    return re.sub(r" - (Exact|Phrase)$", "", ad_group or "")


def norm_match_type(match_type: str) -> str:
    value = (match_type or "").strip()
    return {
        "Exact match": "Exact",
        "Phrase match": "Phrase",
        "Broad match": "Broad",
    }.get(value, value)


def natural_headline(text: str) -> str:
    """Preserve language-specific casing while making a headline-like first char."""
    text = text.strip()
    if not text:
        return text
    return text[0].upper() + text[1:]


def claim_hits(text: str) -> list[str]:
    return [p for p in FORBIDDEN_PATTERNS if re.search(p, text, re.I)]


def summarize_google_csv(market: str, path: Path, source_kind: str) -> tuple[dict[str, object], list[dict[str, object]]]:
    rows = read_csv(path)
    counts = Counter(row["Row Type"] for row in rows)
    campaign_names = sorted({row.get("Campaign", "") for row in rows if row.get("Campaign")})
    campaign_statuses = sorted({row.get("Campaign status", "") for row in rows if row.get("Campaign status")})
    ad_statuses = sorted({row.get("Ad status", "") for row in rows if row.get("Ad status")})
    keyword_statuses = sorted({row.get("Keyword status", "") for row in rows if row.get("Keyword status")})
    ad_group_statuses = sorted({row.get("Ad group status", "") for row in rows if row.get("Ad group status")})
    max_cpc = 0.0
    for row in rows:
        try:
            max_cpc = max(max_cpc, float(row.get("Default max. CPC") or 0))
        except ValueError:
            pass
    final_urls = [row.get("Final URL", "") for row in rows if row.get("Final URL")]
    country_url_hits = sum(1 for url in final_urls if f"country={market}" in url)
    # Supplier/source domains can and should appear as negative keywords. The
    # forbidden scan for this audit is limited to customer-facing/positive rows.
    all_text = "\n".join("|".join(row.values()) for row in rows if row.get("Row Type") != "Negative keyword")
    forbidden = sorted(set(claim_hits(all_text)))
    ads = [r for r in rows if r["Row Type"] == "Ad"]
    headline_counts = [sum(1 for i in range(1, 16) if a.get(f"Headline {i}")) for a in ads]
    desc_counts = [sum(1 for i in range(1, 5) if a.get(f"Description {i}")) for a in ads]
    max_headline_len = max([len(a.get(f"Headline {i}", "")) for a in ads for i in range(1, 16)] or [0])
    max_desc_len = max([len(a.get(f"Description {i}", "")) for a in ads for i in range(1, 5)] or [0])
    keyword_rows = []
    by_theme = defaultdict(lambda: defaultdict(set))
    for row in rows:
        if row["Row Type"] == "Keyword":
            theme = norm_theme(row.get("Ad group", ""))
            by_theme[theme][norm_match_type(row.get("Type", ""))].add(row.get("Keyword", ""))
    for theme, types in by_theme.items():
        for match_type, kws in types.items():
            for kw in sorted(kws):
                keyword_rows.append({
                    "market": market,
                    "source_kind": source_kind,
                    "campaign": campaign_names[0] if campaign_names else "",
                    "theme": theme,
                    "match_type": match_type,
                    "keyword": kw,
                    "quality_note": "Core high-intent exact/phrase term already staged in paused Search structure.",
                })
    campaign_id, account_state, expected_name, current_locale = MARKET_STATE.get(market, ("", "UNKNOWN", "", ""))
    language_quality = "ENGLISH_NATIVE_OR_ACCEPTABLE" if market in {"US", "GB", "CA", "AU"} else "ENGLISH_FIRST_ONLY__NATIVE_LANGUAGE_SECOND_STAGE_REQUIRED"
    if market in {"CH", "BE"}:
        language_quality = "ENGLISH_FIRST_ONLY__COUNTRY_LANGUAGE_SPLIT_REQUIRED"
    if market in {"ES", "IT", "RO"}:
        language_quality = "ENGLISH_FIRST_NOW__NATIVE_CONCEPT_READY_REVIEW_REQUIRED"
    if market in {"PT", "DK"}:
        language_quality = "ENGLISH_FIRST_NOW__NATIVE_PLATFORM_USE_BLOCKED"
    summary = {
        "market": market,
        "campaign_id": campaign_id,
        "expected_campaign": expected_name,
        "source_campaign": campaign_names[0] if campaign_names else "",
        "source_kind": source_kind,
        "account_state": account_state,
        "current_campaign_language": "en",
        "current_locale_posture": current_locale,
        "language_quality_status": language_quality,
        "row_count": len(rows),
        "campaign_rows": counts["Campaign"],
        "ad_group_rows": counts["Ad group"],
        "keyword_rows": counts["Keyword"],
        "negative_keyword_rows": counts["Negative keyword"],
        "ad_rows": counts["Ad"],
        "campaign_statuses": "|".join(s for s in campaign_statuses if s),
        "ad_group_statuses": "|".join(s for s in ad_group_statuses if s),
        "keyword_statuses": "|".join(s for s in keyword_statuses if s),
        "ad_statuses": "|".join(s for s in ad_statuses if s),
        "max_default_cpc": f"{max_cpc:.2f}",
        "final_url_rows": len(final_urls),
        "country_qualified_final_url_rows": country_url_hits if market != "US" else "US local URL set",
        "rsa_min_headlines": min(headline_counts or [0]),
        "rsa_max_headlines": max(headline_counts or [0]),
        "rsa_min_descriptions": min(desc_counts or [0]),
        "rsa_max_descriptions": max(desc_counts or [0]),
        "rsa_max_headline_length": max_headline_len,
        "rsa_max_description_length": max_desc_len,
        "forbidden_pattern_hits": "|".join(forbidden),
        "launch_quality_decision": "CORE_PAUSED_SEARCH_STRUCTURE_COMPLETE__DO_NOT_ADD_LIVE_CHANGES" if not forbidden else "HOLD_FOR_FORBIDDEN_PATTERN_REVIEW",
        "next_quality_action": "Native-language campaign/RSA review before local-language platform use; keep existing English-first campaigns as paused core or first controlled enable path after measurement gate.",
    }
    if market == "US" and any(r["theme"] == "Vacation Family" for r in keyword_rows):
        summary["launch_quality_decision"] = "CORE_PAUSED_SEARCH_COMPLETE_EXCEPT_VACATION_FAMILY_HOLD"
        summary["next_quality_action"] = "Do not enable Vacation Family ad groups until beach/Christmas metadata blocker is solved or those ad groups are explicitly excluded from the enable action."
    return summary, keyword_rows


def build_native_keyword_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for locale, themes in NATIVE_KEYWORDS.items():
        market, language, status, note = LOCALE_STATUS[locale]
        for theme in THEMES:
            for keyword in themes[theme]:
                for match_type in ("Exact", "Phrase"):
                    rows.append({
                        "platform": "Google Ads",
                        "market": market,
                        "locale": locale,
                        "language": language,
                        "theme": theme,
                        "match_type": match_type,
                        "keyword": keyword,
                        "keyword_length": len(keyword),
                        "use_tier": "NATIVE_LANGUAGE_SECOND_STAGE",
                        "status": status,
                        "review_gate": note,
                        "upload_status": "REVIEW_ONLY_NOT_UPLOAD",
                    })
    return rows


def build_negative_review_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for locale, terms in NEGATIVE_KEYWORD_REVIEW_PLAN.items():
        market, language, status, note = LOCALE_STATUS[locale]
        for term in terms:
            if term in {"temu", "shein", "amazon", "aliexpress", "alibaba"}:
                category = "marketplace_or_supplier"
                match_type = "Exact"
            elif term in {"pdf", "second hand"}:
                category = "non_purchase_or_used_intent"
                match_type = "Exact|Phrase"
            elif term in {"gratis", "grátis", "gratuit", "kostenlos", "za darmo", "zdarma", "δωρεάν"}:
                category = "free_intent"
                match_type = "Broad or Phrase after native review"
            else:
                category = "diy_pattern_used_wholesale_or_costume_intent"
                match_type = "Phrase after native review"
            rows.append({
                "platform": "Google Ads",
                "market": market,
                "locale": locale,
                "language": language,
                "negative_keyword": term,
                "recommended_match_type": match_type,
                "category": category,
                "status": status,
                "review_gate": f"Review local ambiguity before upload. {note}",
                "upload_status": "REVIEW_ONLY_NOT_UPLOAD",
            })
    return rows


def build_rsa_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for locale, themes in NATIVE_KEYWORDS.items():
        market, language, status, note = LOCALE_STATUS[locale]
        common = COMMON_HEADLINES[locale]
        templates = DESCRIPTION_TEMPLATES[locale]
        for theme in THEMES:
            theme_terms = [natural_headline(kw) for kw in themes[theme][:5]]
            candidates = []
            for phrase in theme_terms + common:
                if phrase not in candidates and len(phrase) <= 30:
                    candidates.append(phrase)
            # Fill only from approved common lines if a long title-cased keyword was skipped.
            for phrase in common:
                if len(candidates) >= 15:
                    break
                if phrase not in candidates:
                    candidates.append(phrase)
            if len(candidates) < 15:
                raise ValueError(f"Not enough headline candidates for {locale} {theme}: {len(candidates)}")
            headlines = candidates[:15]
            theme_desc_term = themes[theme][0]
            descriptions = [t.format(t=theme_desc_term) for t in templates]
            max_h = max(len(x) for x in headlines)
            max_d = max(len(x) for x in descriptions)
            if max_h > 30 or max_d > 90:
                raise ValueError(f"RSA limit failure {locale} {theme}: h={max_h}, d={max_d}")
            joined = " ".join(headlines + descriptions)
            rows.append({
                "platform": "Google Ads",
                "market": market,
                "locale": locale,
                "language": language,
                "theme": theme,
                "headline_count": len(headlines),
                "description_count": len(descriptions),
                "headlines": "|".join(headlines),
                "descriptions": "|".join(descriptions),
                "max_headline_length": max_h,
                "max_description_length": max_d,
                "forbidden_pattern_hits": "|".join(sorted(set(claim_hits(joined)))),
                "status": status,
                "review_gate": note,
                "upload_status": "REVIEW_ONLY_NOT_UPLOAD",
            })
    return rows


def build_native_campaign_shell_rows() -> list[dict[str, object]]:
    rows = []
    for locale in sorted(LOCALE_STATUS):
        market, language, status, note = LOCALE_STATUS[locale]
        campaign_name = f"DLM_{market}_SEARCH_NONBRAND_NATIVE_{locale.replace('-', '_').upper()}_EXACT_PHRASE_PAUSED_20260510"
        if locale in {"fr-BE", "nl-BE"}:
            campaign_name = f"DLM_BE_SEARCH_NONBRAND_NATIVE_{locale.replace('-', '_').upper()}_EXACT_PHRASE_PAUSED_20260510"
        rows.append({
            "platform": "Google Ads",
            "market": market,
            "locale": locale,
            "language": language,
            "proposed_campaign_name": campaign_name,
            "recommended_campaign_language": locale.split("-")[0],
            "recommended_location": market,
            "ad_groups": "10 if mirroring exact/phrase theme structure",
            "keyword_policy": "Exact and phrase only; no broad match until conversion data and Smart Bidding gates exist.",
            "rsa_policy": "One native RSA per ad group with 15 headlines and 4 descriptions after native review.",
            "status": status,
            "gate": note,
            "account_action_status": "LOCAL_ONLY_NOT_APPROVED_NOT_UPLOAD",
        })
    rows.append({
        "platform": "Google Ads",
        "market": "CH",
        "locale": "de-CH|fr-CH|it-CH",
        "language": "Swiss German/French/Italian split decision",
        "proposed_campaign_name": "DO_NOT_CREATE_AMBIGUOUS_CH_NATIVE_CAMPAIGN",
        "recommended_campaign_language": "TBD",
        "recommended_location": "CH",
        "ad_groups": "TBD after split decision",
        "keyword_policy": "Reuse DE/FR/IT concepts only after native review and country-language routing proof.",
        "rsa_policy": "Build separate native RSAs only after split decision.",
        "status": "PLATFORM_USE_BLOCKED_CH_LANGUAGE_SPLIT",
        "gate": "Switzerland needs a German/French/Italian or English-first decision before native campaign build.",
        "account_action_status": "LOCAL_ONLY_NOT_APPROVED_NOT_UPLOAD",
    })
    return rows


def build_english_expansion_rows(markets: list[str]) -> list[dict[str, object]]:
    rows = []
    for market in markets:
        campaign_id, state, campaign_name, current_locale = MARKET_STATE[market]
        for theme, keywords in ENGLISH_EXPANSION.items():
            for kw in keywords:
                rows.append({
                    "platform": "Google Ads",
                    "market": market,
                    "campaign_id": campaign_id,
                    "campaign": campaign_name,
                    "theme": theme,
                    "keyword": kw,
                    "match_types_to_consider": "Exact|Phrase",
                    "use_tier": "SEARCH_TERM_PROOF_EXPANSION_NOT_INITIAL_BLOAT",
                    "quality_note": "High-intent English expansion candidate. Do not add live by inference; review search terms first or add in a separate approved paused edit.",
                    "account_action_status": "LOCAL_ONLY_NOT_UPLOAD",
                })
    return rows


def build_pinterest_rows() -> list[dict[str, object]]:
    rows = []
    market_readiness_path = AUTHORITY_PACKET / "lanes/pinterest-non-us-local-drafts/pinterest_non_us_market_readiness_matrix.csv"
    if market_readiness_path.exists():
        p_rows = read_csv(market_readiness_path)
    else:
        p_rows = []
    by_market = {r["market"]: r for r in p_rows}
    group_theme_map = {
        "MOMMY_ME": "Mommy & Me Dresses",
        "FAMILY_MATCHING": "Family Matching",
        "PAJAMAS": "Matching Pajamas",
    }
    for market in ["US"] + list(by_market):
        if market == "US":
            readiness = {
                "primary_locale": "en-US",
                "current_pinterest_account_readiness": "US_EN_CLEAN_SCOPE_REVIEW_ONLY_TEMPLATES",
                "recommended_pinterest_path": "Paused US catalog/retargeting draft only after exact approval and Event Quality readback.",
                "source_proof_required": "Existing clean 342-row EN-US scope, 4 exclusions; read back before account action.",
                "copy_gate": "English claim-safe copy only.",
                "country_gate": "US only.",
                "stop_reason_if_attempted_now": "Account write still requires exact approval; Event Quality remains Fair.",
            }
        else:
            readiness = by_market[market]
        locale = readiness.get("primary_locale", "en-US")
        source_locale = locale
        if locale in {"fr-BE or nl-BE", "fr-BE|nl-BE"}:
            source_locale = "fr-BE"
        if source_locale not in NATIVE_KEYWORDS:
            source_locale = "es-ES" if market == "ES" else "it-IT" if market == "IT" else "en-US"
        for group_key, theme in group_theme_map.items():
            terms = ENGLISH_EXPANSION.get(theme, []) if source_locale == "en-US" else NATIVE_KEYWORDS[source_locale].get(theme, [])
            rows.append({
                "platform": "Pinterest",
                "market": market,
                "locale_posture": readiness.get("primary_locale", locale),
                "product_group_key": group_key,
                "theme": theme,
                "keyword_or_catalog_terms_for_copy_review": "|".join(terms[:5]),
                "targeting_note": "Pinterest catalog sales shopping ads use catalog/product data; keyword or interest targeting is not necessary for catalog sales campaigns.",
                "creative_quality_note": "Use clean product data, product groups, readable creative, destination consistency, and claim-safe copy.",
                "current_readiness": readiness.get("current_pinterest_account_readiness", ""),
                "source_proof_required": readiness.get("source_proof_required", ""),
                "copy_gate": readiness.get("copy_gate", ""),
                "country_gate": readiness.get("country_gate", ""),
                "stop_reason_if_attempted_now": readiness.get("stop_reason_if_attempted_now", ""),
                "account_action_status": "REVIEW_ONLY_NOT_UPLOAD",
            })
    return rows


def write_report(summary: dict[str, object]) -> None:
    report = f"""# Paid Growth Multilingual Keyword Quality Upgrade

Generated: {DATE}

Anchor: `{ANCHOR}`

Mode: local-only evidence and campaign-quality planning. No Google Ads or Pinterest account objects were created or edited. No live spend, enablement, budget, bid, status, feed, product, product-group, conversion-goal, Merchant, Shopify, Pinterest, GA4/GTM, or theme change occurred.

## Executive Decision

`LOCAL_EXPERT_HARDENED_KEYWORD_QUALITY_PACKET_READY_NATIVE_REVIEW_GATED`

The existing Google Search campaign infrastructure is structurally complete for the safe paused English-first path: all one-country split files still contain tightly scoped exact/phrase keywords, one RSA per ad group, paused statuses, country-qualified final URLs, and tight negatives. The quality gap is language depth, not raw campaign structure.

To satisfy "best keywords in each language" without bloating live accounts or violating guardrails, this packet stages a separate native-language second-stage plan:

- `google_ads_native_language_keyword_master.csv`: {summary['native_keyword_rows']} native exact/phrase keyword rows across {summary['native_locale_count']} locale variants and {len(THEMES)} themes.
- `google_ads_native_language_rsa_quality_pack.csv`: {summary['native_rsa_rows']} RSA rows, each with 15 headlines and 4 descriptions, all under Google character limits.
- `google_ads_native_negative_keyword_review_plan.csv`: {summary['native_negative_rows']} localized negative-keyword review rows for DIY, pattern, used, wholesale, costume, PDF, marketplace, and supplier intent.
- `google_ads_native_campaign_shell_plan.csv`: proposed native campaign naming and gating for every local-language lane, marked `REVIEW_ONLY_NOT_UPLOAD`.
- `google_ads_english_first_keyword_expansion_candidates.csv`: expansion candidates for existing English-first Search campaigns, held for search-term-proof or a separately approved paused edit.
- `pinterest_multilingual_keyword_interest_quality_plan.csv`: Pinterest local copy/catalog-term plan that respects Pinterest catalog-sales behavior and keeps non-US Pinterest account writes gated.

All native Google Ads and Pinterest planning rows in this packet are local-only and marked `REVIEW_ONLY_NOT_UPLOAD`; none are upload-ready account instructions.

## Official Platform Basis

Google's Search quality guidance ties Quality Score diagnostics to expected CTR, ad relevance, and landing-page experience. Google also says responsive search ad Ad Strength should be improved with more unique assets, keyword-relevant copy, and enough headlines/descriptions. Google keyword match documentation confirms exact match provides tighter steering and phrase match is broader but still controlled. This packet therefore keeps first-launch Search exact/phrase only and avoids broad-match expansion until conversion tracking and bidding gates are trustworthy.

Pinterest's Shopping Ads help states that shopping ads require a business account, uploaded catalog, and product groups, and that keyword or interest targeting is not necessary for catalog sales campaigns. Pinterest campaign structure guidance puts regions, product lines, targeting, budget, and bids at the ad group level, and Pinterest policy emphasizes consistent ad/landing-page experience and ad quality. This packet therefore treats Pinterest "keyword quality" as catalog terms, product-group naming, promoted Pin copy, and destination consistency, not as a Google-style keyword import.

Sources used:

- Google Ads Help, About Quality Score for Search campaigns: https://support.google.com/google-ads/answer/6167118
- Google Ads Help, About keyword matching options: https://support.google.com/google-ads/answer/7478529
- Google Ads Help, About Ad Strength for responsive search ads: https://support.google.com/google-ads/answer/9921843
- Google Ads Help, Create effective Search ads: https://support.google.com/google-ads/answer/6167122
- Pinterest Business Help, Create shopping ads: https://help.pinterest.com/en/business/article/shopping-ads
- Pinterest Business Help, Campaign structure: https://help.pinterest.com/en-gb/business/article/campaign-structure
- Pinterest Advertising Guidelines: https://policy.pinterest.com/en/advertising-guidelines

## Google Ads Status

- Current English-first non-US campaign build: `12 built / 3 absent / 2 parked`, unchanged from the authority-safe-launch-prep anchor.
- Current US nonbrand Search: campaign `23827590655` exists as paused infrastructure and must not be duplicated.
- All current Search keyword rows remain exact/phrase only.
- Every existing RSA row parsed in the audited files has 15 headlines. Current split non-US files have 4 descriptions per RSA; the US nonbrand packet also has one RSA per ad group.
- Native-language copy is not platform-ready until native review, landing-language QA, and exact approval.
- The US paused nonbrand packet still contains `Vacation Family` ad groups. They remain a hold under the existing beach/Christmas metadata blocker and must not be included in a future enable action unless the metadata blocker is solved or those ad groups are deliberately excluded.

## Native-Language Gates

- Expert hardening note: RSA headline casing now preserves natural phrase casing instead of forcing title case across all languages. This avoids obvious machine-generated casing in Spanish, Italian, French, Dutch, Swedish, Danish, Polish, Czech, Romanian, Portuguese, and Greek.
- `es-ES`, `it-IT`, `ro-RO`: concept-ready after this packet, still native-review and landing-QA gated.
- `de-DE`, `nl-NL`, `fr-FR`, `sv-SE`, `pl-PL`, `cs-CZ`, `el-GR`: keyword/RSA pack exists, still native-review plus native landing-language QA gated.
- `pt-PT`: platform-use-blocked until Portugal storefront language behavior is resolved or explicitly accepted because prior `/pt` behavior read as `pt-BR`.
- `da-DK`: platform-use-blocked until Danish native review/rewrite confirms the corrected wording.
- `fr-BE`, `nl-BE`: platform-use-blocked until Belgium French/Dutch split and route proof are decided.
- `CH`: no ambiguous native Swiss campaign should be created; decide English-first, German, French, Italian, or split setup first.

## Pinterest Status

Pinterest is not keyword-import-ready for non-US. The local plan provides catalog/copy terms, but every non-US Pinterest market remains account-write-gated because country-specific source/catalog/product-group readbacks do not exist. For Pinterest catalog sales, the safe quality focus is:

- clean product source and product groups,
- destination consistency,
- readable and policy-safe creative,
- market/country targeting readbacks,
- Event Quality/tag proof before spend.

## Expert-Level Stop Conditions

- Do not import machine-generated native rows directly. Native reviewer PASS/REWRITE/REJECT is required per locale.
- Do not add all expansion keywords at once. Keep the existing English-first campaigns tight and use expansion terms only after search-term proof or separately approved paused edits.
- Do not use broad match until conversion tracking, Smart Bidding readiness, search-term hygiene, and ROAS guardrails are proven.
- Do not use native-language ads where the storefront still serves English or a different dialect unless the owner explicitly accepts that mismatch.
- Do not treat Pinterest as a keyword-import platform; use Pinterest catalog/source, product groups, creative consistency, and Event Quality as the quality system.

## Files Created

- `README.md`
- `PAID_GROWTH_MULTILINGUAL_KEYWORD_QUALITY_UPGRADE_REPORT.md`
- `google_ads_current_search_campaign_quality_audit.csv`
- `google_ads_existing_keywords_by_market_theme.csv`
- `google_ads_native_language_keyword_master.csv`
- `google_ads_native_language_rsa_quality_pack.csv`
- `google_ads_native_negative_keyword_review_plan.csv`
- `google_ads_native_campaign_shell_plan.csv`
- `google_ads_english_first_keyword_expansion_candidates.csv`
- `pinterest_multilingual_keyword_interest_quality_plan.csv`
- `keyword_quality_validation_summary.json`
- `GOOGLE_ADS_NATIVE_LANGUAGE_IMPORT_GATES.md`
- `PINTEREST_KEYWORD_QUALITY_GATES.md`
- `EXPERT_QA_REVIEW_NOTES.md`
- `NEXT_CONTINUATION_PROMPT.md`
- `working/build_keyword_quality_upgrade_packet.py`

## Guardrails Preserved

- No live spend.
- No campaign enablement.
- No budget, bid, or status changes.
- No PMax, Standard Shopping, product-scope, feed-label, product-group, or conversion-goal change.
- No Merchant upload/source edit/sync.
- No Shopify live product-data change.
- No Pinterest account/campaign/draft/product-group/catalog/source/tag/CAPI/audience/budget/bid/status/spend write.
- No checkout payment, order, refund, or cancelation.

## Next Best Action

1. Native review the `google_ads_native_language_keyword_master.csv` and `google_ads_native_language_rsa_quality_pack.csv` rows per locale.
2. Keep the existing English-first paused campaigns as the first controlled Search path after measurement proof and exact enable approval.
3. Do not import the native campaign shell plan until native review, landing-language QA, and exact action-time approval are complete.
4. For Pinterest, resolve the US/Event Quality gate before non-US account builds; use the Pinterest CSV here only as local copy/catalog-term guidance.
"""
    (PACKET / "PAID_GROWTH_MULTILINGUAL_KEYWORD_QUALITY_UPGRADE_REPORT.md").write_text(report, encoding="utf-8")
    (PACKET / "README.md").write_text(
        "# Paid Growth Multilingual Keyword Quality Upgrade\n\n"
        "Local-only packet created on 2026-05-10. Start with "
        "`PAID_GROWTH_MULTILINGUAL_KEYWORD_QUALITY_UPGRADE_REPORT.md`.\n",
        encoding="utf-8",
    )


def write_gate_docs() -> None:
    (PACKET / "GOOGLE_ADS_NATIVE_LANGUAGE_IMPORT_GATES.md").write_text(
        f"""# Google Ads Native-Language Import Gates

Anchor: `{ANCHOR}`

These rows are marked `REVIEW_ONLY_NOT_UPLOAD` and are not upload-ready. Before any native-language Google Ads preview/import:

1. Native reviewer signs off each keyword, headline, and description for the target locale.
2. Country-qualified landing QA passes for PDP, cart, checkout entry, currency, rates, and policy links.
3. The parent creates a one-country paused native CSV only after exact owner approval.
4. Google Ads preview must return clean row validation before apply.
5. Read back campaign, language, location presence-only settings, networks, statuses, budgets, bids, ads, keywords, and final URLs after any approved apply.
6. Keep every campaign, ad group, ad, and keyword paused until separate live-spend approval.

Stop immediately if the flow requires budget/bid/status changes outside the exact approval, any PMax/Shopping/product/feed/conversion change, Merchant upload, Shopify product edit, or campaign enablement.
""",
        encoding="utf-8",
    )
    (PACKET / "PINTEREST_KEYWORD_QUALITY_GATES.md").write_text(
        f"""# Pinterest Keyword And Catalog Quality Gates

Anchor: `{ANCHOR}`

Pinterest catalog-sales shopping ads are not Google-style keyword campaigns. The local term plan is marked `REVIEW_ONLY_NOT_UPLOAD` and is for product-group naming, copy review, promoted Pin wording, and catalog/landing consistency.

Before any Pinterest account action:

1. Confirm the selected country-specific source/catalog/feed profile exists.
2. Read back clean item scope, exclusions, product group filters, and item links.
3. Confirm Event Quality/tag/CAPI status is acceptable for the selected setup.
4. Native/country copy must be reviewed where the market is not English-first.
5. Request exact owner approval for paused drafts/account objects.
6. Read back paused campaign, ad group, ad, product group, budget/bid/status, targeting, source, and destination settings after any approved action.

Stop if the UI requires a catalog source, product data, feed label, campaign status, budget, bid, audience, tag/CAPI, or spend action outside the exact approval.
""",
        encoding="utf-8",
    )
    (PACKET / "EXPERT_QA_REVIEW_NOTES.md").write_text(
        f"""# Expert QA Review Notes

Anchor: `{ANCHOR}`

This is a local-only expert hardening layer on top of the first keyword-quality packet.

## What Was Tightened

- Natural headline casing: native RSA headline phrases now preserve sentence/native casing instead of forced title case.
- Negative-keyword quality: added `google_ads_native_negative_keyword_review_plan.csv` with localized review-only exclusions for DIY, pattern, used, wholesale, costume, PDF, marketplace, and supplier intent.
- Pinterest quality framing: Pinterest rows remain catalog/copy/product-group terms only, because catalog sales shopping ads do not need Google-style keyword targeting.
- Launch discipline: all native Google Ads and Pinterest rows remain `REVIEW_ONLY_NOT_UPLOAD`.

## Expert Bar Before Platform Use

1. Native reviewer approves or rewrites every locale row.
2. Landing-language QA confirms the ad language matches the country-qualified storefront path.
3. Measurement proves non-US purchase currency/value before non-US live spend.
4. Google Ads preview/readback confirms paused state, language, location, networks, bids, budgets, final URLs, and no duplicate campaign.
5. Pinterest source/catalog/product-group readbacks exist before any non-US Pinterest account action.

## Known Intentional Holds

- `pt-PT`: held until pt-PT vs pt-BR storefront behavior is resolved or accepted.
- `da-DK`: held for Danish native review.
- `fr-BE` / `nl-BE`: held until Belgium language split and route proof.
- `CH`: held until German/French/Italian/English split decision.
- US `Vacation Family`: held until the beach/Christmas metadata blocker is solved or explicitly excluded.
""",
        encoding="utf-8",
    )
    continuation = f"""# Next Continuation Prompt

Latest anchor: `{ANCHOR}`

Use the canonical owner-standard prompt in `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.

Newest state to preserve:

- Local-only keyword quality upgrade packet exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-keyword-quality-upgrade/`.
- Existing English-first Google Search campaigns are structurally complete for paused controlled use, but native-language use remains review-gated.
- Native keyword/RSA packs now cover 14 locale variants with natural-cased 15-headline/4-description RSA rows and exact/phrase keyword concepts, all marked `REVIEW_ONLY_NOT_UPLOAD`.
- Localized negative-keyword review plan now exists with `205` review-only rows.
- Pinterest multilingual keyword quality remains catalog/copy/product-group guidance only; non-US Pinterest account writes remain gated by missing country-specific source/catalog/product-group readbacks.
- No account writes or live spend happened in the keyword-quality upgrade.

Next exact work:

1. Native review the language rows, starting with `es-ES`, `it-IT`, and `ro-RO`.
2. Close the non-US purchase currency/value measurement gate before enabling any non-US spend.
3. Keep `RO` Ads branch behind upload-throttle/one-country retry gates; do not re-upload completed countries.
4. Keep `Vacation Family` out of any future Search enable action until the beach/Christmas metadata blocker is solved or excluded.
"""
    (PACKET / "NEXT_CONTINUATION_PROMPT.md").write_text(continuation, encoding="utf-8")


def main() -> None:
    PACKET.mkdir(parents=True, exist_ok=True)

    google_audit = []
    existing_keywords = []
    us_summary, us_keywords = summarize_google_csv("US", US_CSV, "US_PAUSED_REBUILD_PACKET")
    google_audit.append(us_summary)
    existing_keywords.extend(us_keywords)
    for csv_path in sorted(SPLIT_DIR.glob("*_intl_search_paused_draft_web_bulk.csv")):
        market = csv_path.name.split("_", 1)[0]
        summary, keywords = summarize_google_csv(market, csv_path, "NON_US_SPLIT_PACKET")
        google_audit.append(summary)
        existing_keywords.extend(keywords)

    native_keywords = build_native_keyword_rows()
    native_negative_rows = build_negative_review_rows()
    rsa_rows = build_rsa_rows()
    shell_rows = build_native_campaign_shell_rows()
    expansion_rows = build_english_expansion_rows(["US", "GB", "CA", "AU", "CH", "DK", "DE", "NL", "SE", "ES", "IT", "PL", "CZ", "RO", "PT", "GR", "FR", "BE"])
    pinterest_rows = build_pinterest_rows()

    write_csv(PACKET / "google_ads_current_search_campaign_quality_audit.csv", google_audit, list(google_audit[0].keys()))
    write_csv(PACKET / "google_ads_existing_keywords_by_market_theme.csv", existing_keywords, list(existing_keywords[0].keys()))
    write_csv(PACKET / "google_ads_native_language_keyword_master.csv", native_keywords, list(native_keywords[0].keys()))
    write_csv(PACKET / "google_ads_native_negative_keyword_review_plan.csv", native_negative_rows, list(native_negative_rows[0].keys()))
    write_csv(PACKET / "google_ads_native_language_rsa_quality_pack.csv", rsa_rows, list(rsa_rows[0].keys()))
    write_csv(PACKET / "google_ads_native_campaign_shell_plan.csv", shell_rows, list(shell_rows[0].keys()))
    write_csv(PACKET / "google_ads_english_first_keyword_expansion_candidates.csv", expansion_rows, list(expansion_rows[0].keys()))
    write_csv(PACKET / "pinterest_multilingual_keyword_interest_quality_plan.csv", pinterest_rows, list(pinterest_rows[0].keys()))

    validation = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "anchor": ANCHOR,
        "mode": "LOCAL_ONLY_NO_ACCOUNT_WRITES",
        "google_campaign_audit_rows": len(google_audit),
        "existing_keyword_rows": len(existing_keywords),
        "native_keyword_rows": len(native_keywords),
        "native_negative_rows": len(native_negative_rows),
        "native_locale_count": len(LOCALE_STATUS),
        "native_rsa_rows": len(rsa_rows),
        "native_rsa_rows_with_15_headlines": sum(1 for r in rsa_rows if r["headline_count"] == 15),
        "native_rsa_rows_with_4_descriptions": sum(1 for r in rsa_rows if r["description_count"] == 4),
        "native_rsa_max_headline_length": max(r["max_headline_length"] for r in rsa_rows),
        "native_rsa_max_description_length": max(r["max_description_length"] for r in rsa_rows),
        "native_rsa_forbidden_pattern_rows": [r for r in rsa_rows if r["forbidden_pattern_hits"]],
        "native_keyword_forbidden_pattern_rows": [r for r in native_keywords if claim_hits(str(r["keyword"]))],
        "native_negative_forbidden_terms_are_expected": True,
        "pinterest_rows": len(pinterest_rows),
        "guardrails": [
            "no account writes",
            "no live spend",
            "no campaign enablement",
            "no budget bid status changes",
            "no product feed conversion or Shopify product data changes",
        ],
    }
    if validation["native_rsa_forbidden_pattern_rows"] or validation["native_keyword_forbidden_pattern_rows"]:
        raise ValueError("Forbidden-pattern validation failed")
    (PACKET / "keyword_quality_validation_summary.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_report(validation)
    write_gate_docs()
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
