#!/usr/bin/env python3
"""Build local-only native rewrite and measurement continuation artifacts.

This script only writes evidence/review files inside this packet. It does not
create Google Ads import files and does not touch external accounts.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PACKET = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation"
SOURCE_PACKET = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-keyword-quality-upgrade"
TRIAGE_PACKET = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-review-measurement-readonly-continuation"

DATE = "2026-05-11"
ANCHOR = "AGENT_CONTINUITY_ANCHOR: 2026-05-11-paid-growth-native-rewrite-local-measurement-continuation"

THEMES = [
    "Mommy & Me Dresses",
    "Family Matching",
    "Matching Pajamas",
    "Matching Swimwear",
    "Daddy & Me",
]

LOCALE_META = {
    "es-ES": ("ES", "Spanish", "REWRITE_PACKET_READY_NATIVE_REVIEW_REQUIRED"),
    "it-IT": ("IT", "Italian", "REWRITE_PACKET_READY_NATIVE_REVIEW_REQUIRED"),
    "ro-RO": ("RO", "Romanian", "REWRITE_PACKET_READY_NATIVE_REVIEW_REQUIRED"),
    "de-DE": ("DE", "German", "REWRITE_PACKET_READY_NATIVE_REVIEW_REQUIRED"),
    "nl-NL": ("NL", "Dutch", "REWRITE_PACKET_READY_NATIVE_REVIEW_REQUIRED"),
    "fr-FR": ("FR", "French", "REWRITE_PACKET_READY_NATIVE_REVIEW_REQUIRED"),
    "sv-SE": ("SE", "Swedish", "REWRITE_PACKET_READY_NATIVE_REVIEW_REQUIRED"),
    "pl-PL": ("PL", "Polish", "REWRITE_PACKET_READY_NATIVE_REVIEW_REQUIRED"),
    "cs-CZ": ("CZ", "Czech", "REWRITE_PACKET_READY_NATIVE_REVIEW_REQUIRED"),
}

BLOCKED_LOCALES = [
    ("pt-PT", "PT", "Portuguese", "BLOCKED_DIALECT_DECISION_PT_PT_VS_PT_BR"),
    ("da-DK", "DK", "Danish", "BLOCKED_DANISH_NATIVE_REWRITE_REQUIRED"),
    ("fr-BE", "BE", "French for Belgium", "BLOCKED_BE_FR_NL_SPLIT_AND_ROUTE_PROOF"),
    ("nl-BE", "BE", "Dutch for Belgium", "BLOCKED_BE_FR_NL_SPLIT_AND_ROUTE_PROOF"),
    ("el-GR", "GR", "Greek", "PASS_AI_TRIAGE_NATIVE_REVIEW_STILL_REQUIRED"),
    ("CH-SPLIT", "CH", "Swiss language split", "BLOCKED_NO_NATIVE_ROWS_CH_SPLIT_DECISION_REQUIRED"),
]

KEYWORDS = {
    "es-ES": {
        "Mommy & Me Dresses": ["vestidos mamá e hija", "vestidos madre e hija", "vestidos madre hija a juego", "conjuntos mamá e hija", "ropa madre e hija"],
        "Family Matching": ["ropa familiar a juego", "conjuntos familiares a juego", "looks familiares coordinados", "outfits familiares coordinados", "ropa para fotos familiares"],
        "Matching Pajamas": ["pijamas familiares", "pijamas familiares a juego", "pijamas madre e hija", "pijamas mamá e hija", "pijamas para fotos familiares"],
        "Matching Swimwear": ["bañadores familiares", "bañadores familiares a juego", "trajes de baño familiares", "bañadores madre e hija", "moda de baño familiar"],
        "Daddy & Me": ["ropa papá e hijo", "conjuntos papá e hijo", "camisas papá e hijo", "looks padre e hijo", "ropa padre e hijo a juego"],
    },
    "it-IT": {
        "Mommy & Me Dresses": ["abiti mamma e figlia", "vestiti mamma e figlia", "abiti madre e figlia", "look mamma e figlia", "outfit mamma e figlia"],
        "Family Matching": ["outfit coordinati famiglia", "look coordinati famiglia", "abiti coordinati famiglia", "vestiti coordinati famiglia", "abbigliamento famiglia coordinato"],
        "Matching Pajamas": ["pigiami famiglia", "pigiami coordinati famiglia", "pigiami mamma e figlia", "pigiami famiglia abbinati", "pigiami per foto in famiglia"],
        "Matching Swimwear": ["costumi da bagno famiglia", "costumi coordinati famiglia", "costumi mamma e figlia", "moda mare famiglia", "costumi da bagno abbinati"],
        "Daddy & Me": ["outfit papà e figlio", "look padre e figlio", "magliette papà e figlio", "camicie papà e figlio", "abbigliamento papà e figlio"],
    },
    "ro-RO": {
        "Mommy & Me Dresses": ["rochii mamă și fiică", "rochii asortate mamă și fiică", "ținute mamă și fiică", "haine mamă și fiică", "seturi mamă și fiică"],
        "Family Matching": ["ținute de familie asortate", "haine de familie asortate", "ținute coordonate pentru familie", "lookuri de familie asortate", "haine pentru poze de familie"],
        "Matching Pajamas": ["pijamale pentru familie", "pijamale asortate pentru familie", "pijamale mamă și fiică", "pijamale mamă și copil", "pijamale pentru poze de familie"],
        "Matching Swimwear": ["costume de baie pentru familie", "costume de baie asortate", "costume de baie mamă și fiică", "costume de baie pentru mamă și copil", "modă de baie pentru familie"],
        "Daddy & Me": ["ținute tată și copil", "haine tată și fiu", "ținute asortate tată și copil", "haine asortate tată și copil", "lookuri tată și copil"],
    },
    "de-DE": {
        "Mommy & Me Dresses": ["Mama-Tochter-Kleider", "Mutter-Tochter-Kleider", "Partnerlook-Kleider", "Mama-Kind-Kleider", "Mutter-Kind-Outfits"],
        "Family Matching": ["Familien-Outfits", "Partnerlook für Familien", "Familienkleidung", "Familien-Look", "abgestimmte Familien-Outfits"],
        "Matching Pajamas": ["Familienpyjamas", "Partnerlook-Pyjamas", "Mama-Kind-Pyjamas", "Familienschlafanzüge", "Pyjamas für Familien"],
        "Matching Swimwear": ["Bademode für Familien", "Partnerlook-Bademode", "Mama-Kind-Badeanzüge", "Familien-Bademode", "Mutter-Tochter-Badeanzüge"],
        "Daddy & Me": ["Papa-Kind-Outfits", "Vater-Kind-Outfits", "Vater-Sohn-Shirts", "Papa-Sohn-Shirts", "Vater-Kind-Kleidung"],
    },
    "nl-NL": {
        "Mommy & Me Dresses": ["mama-dochterjurken", "moeder-dochterjurken", "bijpassende jurken", "mama-dochterkleding", "moeder-dochteroutfits"],
        "Family Matching": ["familieoutfits", "bijpassende familiekleding", "familielook", "familiekleding", "bijpassende familieoutfits"],
        "Matching Pajamas": ["familiepyjama's", "bijpassende pyjama's", "moeder-dochterpyjama", "mama-dochterpyjama", "familiepyjama's set"],
        "Matching Swimwear": ["badmode voor het gezin", "bijpassende badmode", "mama-kind badmode", "moeder-dochter badmode", "familiebadmode"],
        "Daddy & Me": ["papa-kind outfits", "vader-kind kleding", "vader-zoon shirts", "papa-zoon shirts", "vader-kind outfits"],
    },
    "fr-FR": {
        "Mommy & Me Dresses": ["robes mère-fille", "robes maman-fille", "looks mère-fille", "tenues mère-fille", "robes assorties mère-fille"],
        "Family Matching": ["tenues familiales assorties", "looks de famille", "vêtements pour la famille", "tenues familiales", "vêtements assortis pour la famille"],
        "Matching Pajamas": ["pyjamas pour la famille", "pyjamas assortis", "pyjamas maman-fille", "pyjamas mère-fille", "pyjamas familiaux assortis"],
        "Matching Swimwear": ["maillots de bain assortis", "maillots assortis", "maillots mère-fille", "maillots maman-fille", "maillots de bain pour la famille"],
        "Daddy & Me": ["tenues père-enfant", "looks papa-enfant", "tenues papa-fils", "chemises père-fils", "vêtements papa-fils"],
    },
    "sv-SE": {
        "Mommy & Me Dresses": ["mamma-dotter-klänningar", "mor-dotter-klänningar", "matchande klänningar", "mamma-barn-klänningar", "matchande klänningar för mamma och dotter"],
        "Family Matching": ["familjeoutfits", "matchande familjekläder", "familjekläder", "matchande familjeoutfits", "familjekläder för familjen"],
        "Matching Pajamas": ["familjepyjamas", "matchande pyjamas", "mamma-barn-pyjamas", "pyjamas för familjen", "matchande familjepyjamas"],
        "Matching Swimwear": ["familjebadkläder", "matchande badkläder", "mamma-barn-badkläder", "badkläder för familjen", "badmode för familjen"],
        "Daddy & Me": ["pappa-barn-outfits", "far-barn-kläder", "pappa-son-kläder", "far-son-kläder", "matchande kläder för pappa och barn"],
    },
    "pl-PL": {
        "Mommy & Me Dresses": ["sukienki mama-córka", "sukienki dla mamy i córki", "stylizacje mama-córka", "ubrania dla mamy i córki", "zestawy mama-córka"],
        "Family Matching": ["stylizacje rodzinne", "ubrania dla rodziny", "dopasowane stroje rodzinne", "rodzinne zestawy ubrań", "odzież rodzinna"],
        "Matching Pajamas": ["piżamy rodzinne", "piżamy dla rodziny", "piżamy dla mamy i dziecka", "dopasowane piżamy rodzinne", "piżamy mama-córka"],
        "Matching Swimwear": ["rodzinne stroje kąpielowe", "stroje kąpielowe dla rodziny", "stroje kąpielowe mama-dziecko", "dopasowane stroje kąpielowe", "stroje plażowe dla rodziny"],
        "Daddy & Me": ["ubrania tata-syn", "koszule tata-syn", "stylizacje tata-dziecko", "ubrania dla taty i dziecka", "zestawy tata-dziecko"],
    },
    "cs-CZ": {
        "Mommy & Me Dresses": ["šaty pro mámu a dceru", "sladěné šaty pro mámu a dceru", "oblečení pro mámu a dceru", "styl pro mámu a dceru", "sety pro mámu a dceru"],
        "Family Matching": ["rodinné outfity", "sladěné rodinné oblečení", "oblečení pro rodinu", "rodinné sladěné sety", "rodinná móda"],
        "Matching Pajamas": ["rodinná pyžama", "sladěná pyžama pro rodinu", "pyžama pro mámu a dítě", "pyžama pro rodinu", "pyžama pro mámu a dceru"],
        "Matching Swimwear": ["rodinné plavky", "sladěné plavky pro rodinu", "plavky pro mámu a dítě", "plavky pro rodinu", "rodinné plavky k moři"],
        "Daddy & Me": ["oblečení pro tátu a syna", "košile pro tátu a syna", "styl pro tátu a dítě", "oblečení pro tátu a dítě", "sety pro tátu a dítě"],
    },
}

COMMON_HEADLINES = {
    "es-ES": ["Dress Like Mommy", "Looks coordinados", "Para fotos familiares", "Tallas por separado", "Moda familiar", "Ideas para la familia", "Momentos especiales", "Looks a juego", "Para padres e hijos", "Estilo familiar"],
    "it-IT": ["Dress Like Mommy", "Look coordinati", "Per foto in famiglia", "Taglie separate", "Moda per la famiglia", "Idee per la famiglia", "Momenti speciali", "Look abbinati", "Per genitori e bambini", "Stile per la famiglia", "Scegli le taglie"],
    "ro-RO": ["Dress Like Mommy", "Ținute coordonate", "Poze de familie", "Mărimi separate", "Idei pentru familie", "Momente speciale", "Lookuri asortate", "Pentru părinți și copii", "Stil de familie", "Alege mărimi", "Zile în familie", "Pentru poze speciale"],
    "de-DE": ["Dress Like Mommy", "Abgestimmte Looks", "Für Familienfotos", "Größen separat wählen", "Familienmode", "Ideen für Familien", "Besondere Momente", "Partnerlook-Ideen", "Für Eltern und Kinder", "Looks für Fotos"],
    "nl-NL": ["Dress Like Mommy", "Gecoördineerde looks", "Voor familiefoto's", "Aparte maten kiezen", "Familiemode", "Ideeën voor familie", "Bijpassende looks", "Voor ouders en kinderen", "Looks voor foto's", "Speciale momenten"],
    "fr-FR": ["Dress Like Mommy", "Looks coordonnés", "Pour photos de famille", "Tailles séparées", "Mode famille", "Idées pour la famille", "Moments spéciaux", "Tenues assorties", "Pour parents et enfants", "Looks pour photos", "Choisir les tailles"],
    "sv-SE": ["Dress Like Mommy", "Samordnade looks", "För familjefoton", "Välj storlekar", "Familjemode", "Idéer för familjen", "Särskilda stunder", "Matchande looks", "För föräldrar och barn", "Looks för foton", "Välj varje storlek"],
    "pl-PL": ["Dress Like Mommy", "Dopasowane stroje", "Na rodzinne zdjęcia", "Osobne rozmiary", "Moda rodzinna", "Pomysły dla rodziny", "Wyjątkowe chwile", "Pasujące stylizacje", "Dla rodziców i dzieci", "Styl do zdjęć"],
    "cs-CZ": ["Dress Like Mommy", "Sladěné outfity", "Pro rodinné fotky", "Vyberte velikosti", "Rodinná móda", "Nápady pro rodinu", "Výjimečné chvíle", "Sladěné looky", "Pro rodiče a děti", "Looky na fotky", "Vyberte pro každého"],
}

DESCRIPTIONS = {
    "es-ES": ["{t} para fotos, cumpleaños y días en familia.", "Elige una talla para cada adulto, niña o niño.", "Compra estilos coordinados para momentos familiares.", "Consulta la página del producto para elegir cada talla."],
    "it-IT": ["{t} per foto, compleanni e giornate in famiglia.", "Scegli una taglia per ogni adulto, bambina o bambino.", "Crea look coordinati per momenti speciali.", "Usa la pagina prodotto per scegliere ogni taglia."],
    "ro-RO": ["{t} pentru poze, aniversări și zile în familie.", "Alege separat mărimea pentru fiecare adult sau copil.", "Creează ținute coordonate pentru momente speciale.", "Folosește pagina produsului pentru fiecare mărime."],
    "de-DE": ["{t} für Fotos, Geburtstage und Familienmomente.", "Wähle Größen für Erwachsene und Kinder separat.", "Stelle abgestimmte Looks für besondere Momente zusammen.", "Nutze die Produktseite, um jede Größe auszuwählen."],
    "nl-NL": ["{t} voor foto's, verjaardagen en familiedagen.", "Kies een aparte maat voor elke volwassene en elk kind.", "Maak bijpassende looks voor bijzondere momenten.", "Gebruik de productpagina om elke maat te kiezen."],
    "fr-FR": ["{t} pour photos, anniversaires et moments en famille.", "Choisissez une taille pour chaque adulte et enfant.", "Créez des tenues coordonnées pour vos moments spéciaux.", "Utilisez la page produit pour choisir chaque taille."],
    "sv-SE": ["{t} för foton, födelsedagar och familjedagar.", "Välj separat storlek för varje vuxen och barn.", "Skapa matchande looks för särskilda stunder.", "Använd produktsidan för att välja varje storlek."],
    "pl-PL": ["{t} na zdjęcia, urodziny i rodzinne dni.", "Wybierz osobny rozmiar dla każdej osoby.", "Twórz dopasowane stylizacje na wyjątkowe chwile.", "Użyj strony produktu, aby wybrać każdy rozmiar."],
    "cs-CZ": ["{t} na fotky, narozeniny a rodinné dny.", "Vyberte zvlášť velikost pro každou osobu.", "Tvořte sladěné outfity pro výjimečné chvíle.", "Velikost pro každého vyberete na stránce produktu."],
}

NEGATIVES = {
    "es-ES": [
        ("gratis", "Exact review", "free_intent_caution"),
        ("patrón", "Phrase review", "diy_pattern"),
        ("patrones", "Phrase review", "diy_pattern"),
        ("coser", "Phrase review", "diy_sewing"),
        ("costura", "Phrase review", "diy_sewing"),
        ("segunda mano", "Phrase review", "used_intent"),
        ("usado", "Exact review", "used_intent"),
        ("mayorista", "Phrase review", "wholesale_intent"),
        ("disfraz", "Exact review", "costume_intent"),
    ],
    "it-IT": [
        ("gratis", "Exact review", "free_intent_caution"),
        ("cartamodello", "Phrase review", "diy_pattern"),
        ("cartamodelli", "Phrase review", "diy_pattern"),
        ("cucire", "Phrase review", "diy_sewing"),
        ("cucito", "Phrase review", "diy_sewing"),
        ("seconda mano", "Phrase review", "used_intent"),
        ("usato", "Exact review", "used_intent"),
        ("ingrosso", "Phrase review", "wholesale_intent"),
        ("costume carnevale", "Phrase review", "narrowed_costume_intent"),
        ("travestimento", "Exact review", "narrowed_costume_intent"),
        ("costumi teatrali", "Phrase review", "narrowed_costume_intent"),
    ],
    "ro-RO": [
        ("gratis", "Exact review", "free_intent_caution"),
        ("tipar", "Phrase review", "diy_pattern"),
        ("tipare", "Phrase review", "diy_pattern"),
        ("cusut", "Phrase review", "diy_sewing"),
        ("croitorie", "Phrase review", "diy_sewing"),
        ("second hand", "Phrase review", "used_intent"),
        ("folosit", "Exact review", "used_intent"),
        ("angro", "Phrase review", "wholesale_intent"),
        ("costum de carnaval", "Phrase review", "narrowed_costume_intent"),
        ("deghizare", "Exact review", "narrowed_costume_intent"),
        ("costume teatru", "Phrase review", "narrowed_costume_intent"),
    ],
    "de-DE": [
        ("kostenlos", "Exact review", "free_intent_caution"),
        ("Schnittmuster", "Phrase review", "diy_pattern"),
        ("nähen", "Phrase review", "diy_sewing"),
        ("Nähanleitung", "Phrase review", "diy_sewing"),
        ("gebraucht", "Exact review", "used_intent"),
        ("second hand", "Phrase review", "used_intent"),
        ("Großhandel", "Phrase review", "wholesale_intent"),
        ("Karnevalskostüm", "Phrase review", "narrowed_costume_intent"),
        ("Halloween Kostüm", "Phrase review", "narrowed_costume_intent"),
    ],
    "nl-NL": [
        ("gratis", "Exact review", "free_intent_caution"),
        ("naaipatroon", "Phrase review", "diy_pattern"),
        ("naaien", "Phrase review", "diy_sewing"),
        ("tweedehands", "Phrase review", "used_intent"),
        ("gebruikt", "Exact review", "used_intent"),
        ("groothandel", "Phrase review", "wholesale_intent"),
        ("carnavalskostuum", "Phrase review", "narrowed_costume_intent"),
        ("verkleedkostuum", "Phrase review", "narrowed_costume_intent"),
    ],
    "fr-FR": [
        ("gratuit", "Exact review", "free_intent_caution"),
        ("patron", "Phrase review", "diy_pattern"),
        ("patrons", "Phrase review", "diy_pattern"),
        ("couture", "Phrase review", "diy_sewing"),
        ("coudre", "Phrase review", "diy_sewing"),
        ("d'occasion", "Phrase review", "used_intent"),
        ("seconde main", "Phrase review", "used_intent"),
        ("grossiste", "Phrase review", "wholesale_intent"),
        ("déguisement", "Exact review", "narrowed_costume_intent"),
        ("costume carnaval", "Phrase review", "narrowed_costume_intent"),
    ],
    "sv-SE": [
        ("gratis", "Exact review", "free_intent_caution"),
        ("symönster", "Phrase review", "diy_pattern"),
        ("sy", "Phrase review", "diy_sewing"),
        ("sömnad", "Phrase review", "diy_sewing"),
        ("begagnad", "Exact review", "used_intent"),
        ("second hand", "Phrase review", "used_intent"),
        ("grossist", "Phrase review", "wholesale_intent"),
        ("maskeradkostym", "Phrase review", "narrowed_costume_intent"),
        ("halloweenkostym", "Phrase review", "narrowed_costume_intent"),
    ],
    "pl-PL": [
        ("za darmo", "Exact review", "free_intent_caution"),
        ("wykrój", "Phrase review", "diy_pattern"),
        ("wykroje", "Phrase review", "diy_pattern"),
        ("szyć", "Phrase review", "diy_sewing"),
        ("szycie", "Phrase review", "diy_sewing"),
        ("używane", "Exact review", "used_intent"),
        ("second hand", "Phrase review", "used_intent"),
        ("hurt", "Phrase review", "wholesale_intent"),
        ("kostium karnawałowy", "Phrase review", "narrowed_costume_intent"),
        ("przebranie", "Exact review", "narrowed_costume_intent"),
        ("kostium teatralny", "Phrase review", "narrowed_costume_intent"),
    ],
    "cs-CZ": [
        ("zdarma", "Exact review", "free_intent_caution"),
        ("střih", "Phrase review", "diy_pattern"),
        ("střihy", "Phrase review", "diy_pattern"),
        ("šít", "Phrase review", "diy_sewing"),
        ("šití", "Phrase review", "diy_sewing"),
        ("použité", "Exact review", "used_intent"),
        ("second hand", "Phrase review", "used_intent"),
        ("velkoobchod", "Phrase review", "wholesale_intent"),
        ("karnevalový kostým", "Phrase review", "narrowed_costume_intent"),
        ("kostým na maškarní", "Phrase review", "narrowed_costume_intent"),
    ],
}

MARKETPLACE_NEGATIVES = ["temu", "shein", "amazon", "aliexpress", "alibaba"]

FORBIDDEN_SNIPPETS = [
    "fast shipping",
    "free shipping",
    "warehouse",
    "in stock now",
    "guaranteed",
    "best seller",
    "bestseller",
    "limited time",
    "discount",
    "sale",
    "1688",
    "alibaba",
    "aliexpress",
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def title_first(value: str) -> str:
    return value[:1].upper() + value[1:] if value else value


def source_counts() -> dict[str, int]:
    counts = {}
    for name in [
        "google_ads_native_language_keyword_master.csv",
        "google_ads_native_language_rsa_quality_pack.csv",
        "google_ads_native_negative_keyword_review_plan.csv",
    ]:
        path = SOURCE_PACKET / name
        with path.open(newline="", encoding="utf-8-sig") as f:
            counts[name] = sum(1 for _ in csv.DictReader(f))
    return counts


def build_keyword_rows() -> list[dict[str, object]]:
    rows = []
    for locale, themes in KEYWORDS.items():
        market, language, status = LOCALE_META[locale]
        for theme in THEMES:
            for term in themes[theme]:
                for match_type in ("Exact", "Phrase"):
                    rows.append({
                        "platform": "Google Ads",
                        "market": market,
                        "locale": locale,
                        "language": language,
                        "theme": theme,
                        "match_type": match_type,
                        "corrected_keyword": term,
                        "keyword_length": len(term),
                        "source_status": "REWRITE_RECOMMENDED",
                        "rewrite_status": status,
                        "review_gate": "Native-speaker signoff and country-qualified landing-language QA required before any Google Ads preview/import.",
                        "upload_status": "REVIEW_ONLY_NOT_UPLOAD",
                    })
    return rows


def build_rsa_rows() -> list[dict[str, object]]:
    rows = []
    for locale, themes in KEYWORDS.items():
        market, language, status = LOCALE_META[locale]
        for theme in THEMES:
            candidates = []
            for term in themes[theme]:
                candidate = title_first(term)
                if len(candidate) <= 30 and candidate not in candidates:
                    candidates.append(candidate)
            for candidate in COMMON_HEADLINES[locale]:
                if len(candidates) >= 15:
                    break
                if len(candidate) <= 30 and candidate not in candidates:
                    candidates.append(candidate)
            if len(candidates) != 15:
                raise ValueError(f"{locale} {theme} has {len(candidates)} headlines")
            descs = [d.format(t=themes[theme][0]) for d in DESCRIPTIONS[locale]]
            bad_h = [h for h in candidates if len(h) > 30]
            bad_d = [d for d in descs if len(d) > 90]
            if bad_h or bad_d:
                raise ValueError(f"Length failure {locale} {theme}: {bad_h} {bad_d}")
            text = " ".join(candidates + descs).lower()
            hits = [snippet for snippet in FORBIDDEN_SNIPPETS if snippet in text]
            rows.append({
                "platform": "Google Ads",
                "market": market,
                "locale": locale,
                "language": language,
                "theme": theme,
                "headline_count": 15,
                "description_count": 4,
                "headlines": "|".join(candidates),
                "descriptions": "|".join(descs),
                "max_headline_length": max(len(h) for h in candidates),
                "max_description_length": max(len(d) for d in descs),
                "forbidden_pattern_hits": "|".join(hits),
                "source_status": "REWRITE_RECOMMENDED",
                "rewrite_status": status,
                "review_gate": "Native-speaker ad-copy signoff and destination-language QA required before any Google Ads preview/import.",
                "upload_status": "REVIEW_ONLY_NOT_UPLOAD",
            })
    return rows


def build_negative_rows() -> list[dict[str, object]]:
    rows = []
    for locale, terms in NEGATIVES.items():
        market, language, status = LOCALE_META[locale]
        for term, match_type, category in terms:
            rows.append({
                "platform": "Google Ads",
                "market": market,
                "locale": locale,
                "language": language,
                "negative_keyword": term,
                "recommended_match_type": match_type,
                "category": category,
                "rewrite_status": status,
                "review_gate": "Review local ambiguity and search-term evidence before upload; avoid broad negatives until live waste proves need.",
                "upload_status": "REVIEW_ONLY_NOT_UPLOAD",
            })
        for term in MARKETPLACE_NEGATIVES:
            rows.append({
                "platform": "Google Ads",
                "market": market,
                "locale": locale,
                "language": language,
                "negative_keyword": term,
                "recommended_match_type": "Exact only",
                "category": "marketplace_or_supplier",
                "rewrite_status": status,
                "review_gate": "Exact-only review candidate. Do not use phrase/broad unless search-term waste proves it.",
                "upload_status": "REVIEW_ONLY_NOT_UPLOAD",
            })
    return rows


def build_locale_status(keyword_rows: list[dict[str, object]], rsa_rows: list[dict[str, object]], negative_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for locale, (market, language, status) in LOCALE_META.items():
        rows.append({
            "market": market,
            "locale": locale,
            "language": language,
            "replacement_keyword_rows": sum(1 for r in keyword_rows if r["locale"] == locale),
            "replacement_rsa_rows": sum(1 for r in rsa_rows if r["locale"] == locale),
            "replacement_negative_review_rows": sum(1 for r in negative_rows if r["locale"] == locale),
            "status": status,
            "upload_status": "REVIEW_ONLY_NOT_UPLOAD",
            "next_action": "Send this replacement slice to native reviewer, then run country-qualified landing-language QA.",
        })
    for locale, market, language, status in BLOCKED_LOCALES:
        rows.append({
            "market": market,
            "locale": locale,
            "language": language,
            "replacement_keyword_rows": 0,
            "replacement_rsa_rows": 0,
            "replacement_negative_review_rows": 0,
            "status": status,
            "upload_status": "NO_PLATFORM_USE",
            "next_action": "Keep gated until the documented dialect/split/native-review decision is resolved.",
        })
    return rows


def write_docs(summary: dict[str, object]) -> None:
    report = f"""# Native Rewrite Local-only + Measurement Continuation

Generated: {DATE}
Anchor: `{ANCHOR}`
Mode: `LOCAL_ONLY_REVIEW_PACKET_AND_READONLY_MEASUREMENT_CONTINUATION`

## Scope

This packet continues from `AGENT_CONTINUITY_ANCHOR: 2026-05-11-paid-growth-native-review-measurement-readonly-continuation`.

It does not redo the expert keyword packet. It creates a replacement review layer for the locales the May 11 triage marked `REWRITE_RECOMMENDED`:

- `es-ES`, `it-IT`, `ro-RO`
- `de-DE`, `nl-NL`, `fr-FR`, `sv-SE`
- `pl-PL`, `cs-CZ`

Source counts preserved from the expert packet:

- Source native keyword rows: `{summary['source_keyword_rows']}`
- Source RSA rows: `{summary['source_rsa_rows']}`
- Source negative-review rows: `{summary['source_negative_rows']}`

Replacement artifacts created:

- `google_ads_native_keyword_replacements_local_only.csv`: `{summary['replacement_keyword_rows']}` rows
- `google_ads_native_rsa_replacements_local_only.csv`: `{summary['replacement_rsa_rows']}` rows
- `google_ads_native_negative_replacements_local_only.csv`: `{summary['replacement_negative_rows']}` rows
- `native_rewrite_locale_status.csv`: `{summary['locale_status_rows']}` rows

Every Google Ads row remains `REVIEW_ONLY_NOT_UPLOAD`.

## Quality Changes

- Spanish rows replace non-native noun chains such as `looks familia coordinados` and `moda baño familiar`.
- Italian rows replace literal constructions such as `vestiti papà figlio`, `Idee per famiglia`, and broad `costume` negative intent.
- Romanian rows add missing prepositions/conjunctions such as `de baie pentru familie` and `tată și copil`.
- German rows normalize compounds/capitalization such as `Mama-Tochter-Kleider` and `Familienpyjamas`.
- Dutch rows replace English-influenced forms with `bijpassende` or compact Dutch compounds.
- French rows add connectors/hyphenation such as `robes mère-fille` and `looks de famille`.
- Swedish rows fix separated compounds such as `familjekläder`, `familjepyjamas`, and `badkläder för familjen`.
- Polish rows add case/connectors such as `sukienki mama-córka` and `rodzinne stroje kąpielowe`.
- Czech rows replace noun-chain phrases with `šaty pro mámu a dceru`, `rodinné plavky`, and related forms.

Negative keywords were narrowed where broad terms could block valid apparel intent. Marketplace/supplier terms remain exact-only review candidates.

## Still Gated

- `pt-PT`: no platform use until the Portugal `pt-PT` versus `pt-BR` storefront/dialect decision is made and read back.
- `da-DK`: remains blocked for true Danish-native rewrite.
- `fr-BE` and `nl-BE`: remain blocked until Belgium FR/NL split and route proof are resolved.
- `el-GR`: still requires Greek-native review and landing-language QA before platform use.
- `CH`: still has no native rows and needs a de-CH/fr-CH/it-CH/English split decision.

## Measurement Lane

The non-US purchase-event currency/value gate remains open. This packet does not claim it is solved.

Read-only evidence available from the prior packet:

- Shopify Admin sanitized non-USD order candidates: `7` rows across `DKK`, `GBP`, and `CHF`.
- GA4 UI access to property `330266838` was proven.
- GA4 Home showed `Purchases: 7` for May 4-10, but did not expose order-level currency/value.
- Google Ads conversion action `Google Shopping App Purchase` remains healthy at aggregate/configuration level.
- GA4 Admin/Data API with the existing `gcloud` token is blocked by `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT`.

The cleanest remaining read-only proof path is GA4 UI Explore/report export for property `330266838`, filtered to `eventName = purchase` for `2026-04-01` through `2026-05-10`, with transaction ID/currency/country/date/value dimensions if the UI exposes them. If the UI cannot expose the event-level fields, the exact next gate is read-only GA4 API scope refresh or controlled non-US test-purchase approval.

## Guardrails

No live spend, campaign enablement, account-object creation, upload/preview/apply, budget/bid/status change, PMax, Standard Shopping, product-scope/feed-label/product-group change, conversion-goal change, Merchant upload/source edit/sync, Shopify live product-data/theme write, Pinterest write, GA4/GTM write, checkout payment/order/refund/cancel, credential/account/billing edit, CAPTCHA bypass, destructive filesystem action, or unrelated dirty-worktree cleanup occurred.
"""
    (PACKET / "NATIVE_REWRITE_LOCAL_ONLY_REPORT.md").write_text(report, encoding="utf-8")

    measurement = f"""# Non-US Purchase Measurement Read-only Continuation

Anchor: `{ANCHOR}`
Status: `READONLY_PATH_IDENTIFIED_PURCHASE_EVENT_PROOF_STILL_REQUIRED`

## Current Evidence

- Shopify has `7` sanitized non-USD order candidates since `2026-04-01` across `DKK`, `GBP`, and `CHF`.
- GA4 UI access was previously proven for account `88409806`, property `330266838`, visible property `dresslikemommy.com - GA4`.
- Google Ads conversion configuration still points to one primary purchase action with dynamic value, but this is not order-level non-US proof.
- GA4 CLI/API matching remains blocked by insufficient OAuth scopes.

## Best Remaining Read-only Path

Use logged-in GA4 UI, not a live checkout, to attempt:

1. Date range `2026-04-01` through `2026-05-10`.
2. Filter `eventName = purchase`.
3. Pull visible/exportable dimensions: transaction ID, currency code, country, date, hour/minute if available.
4. Pull metrics: purchases, purchase revenue/total revenue, event value if available.
5. Match against sanitized Shopify candidates by timestamp window, country, currency, and value.

Strongest candidate windows:

- `2026-05-07 13:22 UTC`, `DK`, `201 DKK`
- `2026-05-04 07:29 UTC`, `DK`, `434 DKK`
- `2026-04-18 13:19 UTC`, `GB`, `24 GBP`
- `2026-04-15 19:20 UTC`, `CH`, `34 CHF`

## If Read-only UI Cannot Expose The Fields

Exact unblock options:

- Provide/refresh a read-only Google Analytics OAuth token with Analytics Data/Admin API scopes for property `330266838`; or
- Approve the controlled non-US test-purchase/refund/cancel procedure already documented in the prior packet.

No campaign can be enabled from this packet. This lane is not closed until non-US `purchase` currency/value/transaction evidence is saved.
"""
    (PACKET / "MEASUREMENT_READONLY_CONTINUATION.md").write_text(measurement, encoding="utf-8")

    readme = f"""# Paid Growth Native Rewrite + Measurement Continuation

Anchor: `{ANCHOR}`

This packet is local-only and read-only. It creates corrected replacement review rows for the nine locales that the May 11 native-review triage marked `REWRITE_RECOMMENDED`, and it records the safest remaining path for the non-US purchase-event currency/value gate.

Start with:

- `NATIVE_REWRITE_LOCAL_ONLY_REPORT.md`
- `google_ads_native_keyword_replacements_local_only.csv`
- `google_ads_native_rsa_replacements_local_only.csv`
- `google_ads_native_negative_replacements_local_only.csv`
- `MEASUREMENT_READONLY_CONTINUATION.md`
"""
    (PACKET / "README.md").write_text(readme, encoding="utf-8")

    continuation = f"""Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical operating prompt. Latest anchor: `{ANCHOR}`.

Do not redo the expert keyword packet and do not redo the 2026-05-11 native triage. Use the new local-only replacement packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation/` as the current rewrite layer.

Next best action: native-speaker review the corrected replacement slices for `es-ES`, `it-IT`, `ro-RO`, `de-DE`, `nl-NL`, `fr-FR`, `sv-SE`, `pl-PL`, and `cs-CZ`, then run country-qualified landing-language QA. Keep `pt-PT`, `da-DK`, `fr-BE`, `nl-BE`, `el-GR`, and `CH` gated exactly as documented.

Separately close the non-US purchase-event currency/value measurement gate before any live spend. Use logged-in GA4 UI property `330266838` or refreshed read-only GA4 API scopes to match sanitized Shopify non-USD order candidates to actual `purchase` event currency/value/transaction evidence. Do not enable campaigns or upload/apply native rows until measurement and native-copy gates are closed or explicitly approved.
"""
    (PACKET / "NEXT_CONTINUATION_PROMPT.md").write_text(continuation, encoding="utf-8")


def main() -> None:
    PACKET.mkdir(parents=True, exist_ok=True)
    keyword_rows = build_keyword_rows()
    rsa_rows = build_rsa_rows()
    negative_rows = build_negative_rows()
    locale_rows = build_locale_status(keyword_rows, rsa_rows, negative_rows)
    counts = source_counts()
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "anchor": ANCHOR,
        "mode": "LOCAL_ONLY_REVIEW_PACKET_NO_ACCOUNT_WRITES",
        "source_keyword_rows": counts["google_ads_native_language_keyword_master.csv"],
        "source_rsa_rows": counts["google_ads_native_language_rsa_quality_pack.csv"],
        "source_negative_rows": counts["google_ads_native_negative_keyword_review_plan.csv"],
        "replacement_keyword_rows": len(keyword_rows),
        "replacement_rsa_rows": len(rsa_rows),
        "replacement_negative_rows": len(negative_rows),
        "locale_status_rows": len(locale_rows),
        "locales_rewritten": sorted(LOCALE_META),
        "blocked_or_gated_locales": [row[0] for row in BLOCKED_LOCALES],
        "max_keyword_length": max(len(str(r["corrected_keyword"])) for r in keyword_rows),
        "max_headline_length": max(int(r["max_headline_length"]) for r in rsa_rows),
        "max_description_length": max(int(r["max_description_length"]) for r in rsa_rows),
        "rsa_rows_with_forbidden_hits": [r for r in rsa_rows if r["forbidden_pattern_hits"]],
        "upload_status_values": sorted(set(str(r["upload_status"]) for r in keyword_rows + rsa_rows + negative_rows)),
        "measurement_gate_status": "READONLY_PATH_IDENTIFIED_PURCHASE_EVENT_PROOF_STILL_REQUIRED",
    }
    write_csv(PACKET / "google_ads_native_keyword_replacements_local_only.csv", keyword_rows, [
        "platform", "market", "locale", "language", "theme", "match_type",
        "corrected_keyword", "keyword_length", "source_status", "rewrite_status",
        "review_gate", "upload_status",
    ])
    write_csv(PACKET / "google_ads_native_rsa_replacements_local_only.csv", rsa_rows, [
        "platform", "market", "locale", "language", "theme", "headline_count",
        "description_count", "headlines", "descriptions", "max_headline_length",
        "max_description_length", "forbidden_pattern_hits", "source_status",
        "rewrite_status", "review_gate", "upload_status",
    ])
    write_csv(PACKET / "google_ads_native_negative_replacements_local_only.csv", negative_rows, [
        "platform", "market", "locale", "language", "negative_keyword",
        "recommended_match_type", "category", "rewrite_status", "review_gate",
        "upload_status",
    ])
    write_csv(PACKET / "native_rewrite_locale_status.csv", locale_rows, [
        "market", "locale", "language", "replacement_keyword_rows",
        "replacement_rsa_rows", "replacement_negative_review_rows", "status",
        "upload_status", "next_action",
    ])
    (PACKET / "validation_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_docs(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
