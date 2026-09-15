"""Independent checks of saved accepted browser evidence; no browser actions."""
from pathlib import Path
import datetime
import hashlib
import json
import re
from urllib.parse import urlsplit, parse_qs

P = Path(__file__).resolve().parent.parent


def load(name):
    return json.loads((P / name).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks = []
observations = []
used = set()


def check(name, passed, details=None):
    checks.append({"name": name, "pass": bool(passed), "details": details})


def evidence(name):
    used.add(name)
    return load(name)


def number(value):
    match = re.search(r"[0-9]+(?:[.,][0-9]+)?", str(value))
    return float(match.group().replace(",", ".")) if match else None


def table(state):
    tables = [t for p in state.get("panels", []) if p.get("hidden") is False for t in p.get("tables", [])]
    return tables[0] if len(tables) == 1 else None


def columns(headers):
    bust = [i for i, h in enumerate(headers) if any(x in h for x in ["Chest/Bust", "Poitrine/Buste", "الصدر/الصدر"])]
    length = [i for i, h in enumerate(headers) if any(x in h for x in ["Garment Length", "Longueur du vêtement", "طول الملابس"])]
    return (bust[0], length[0]) if len(bust) == len(length) == 1 else (None, None)


source = {t["id"]: t for t in load("arabic-before.json")["state"]["tables"] if t.get("id")}
used.add("arabic-before.json")
expected_module_url = None
guide_count = compact_count = imperial_count = reopen_count = no_type_count = 0
role_text = {"en": {"mother": "Mother", "girl": "Girl"}, "fr": {"mother": "Maman", "girl": "Fille"}, "ar": {"mother": "الأم", "girl": "البنت"}}


def source_value(role, garment, column, unit):
    row = source["size-chart-cardigan" if garment == "cardigan" else "size-chart"]["rows"][7 if role == "mother" else 0]
    parts = row[column].split("/")
    return number(parts[1 if unit == "imperial" else 0])


def inspect_guide(name, locale, role, garment, unit, width):
    state = evidence(name)
    t = table(state)
    check(name + ":one_visible_table", t is not None)
    if t is None:
        return state
    selected = [r for r in t["rows"] if "is-selected" in r.get("cls", "")]
    row = selected[0]["text"].split("\t") if len(selected) == 1 else []
    bi, li = columns(t["headers"])
    check(name + ":role_row_count", len(t["rows"]) == (5 if role == "mother" else 7))
    check(name + ":one_matching_selected_row", len(selected) == 1 and (row[0] == "S" if role == "mother" else row[0] in ["2 Years", "2 ans", "سنتين", "2 سنة"]))
    check(name + ":source_bust_and_garment_length", bool(row) and bi is not None and li is not None and number(row[bi]) == source_value(role, garment, 4, unit) and number(row[li]) == source_value(role, garment, 9, unit))
    matching_triggers = [x for x in state["triggers"] if x.get("aria-expanded") == "true" and x.get("data-fit-role-key") == role and x.get("data-fit-garment-key") == garment]
    check(name + ":actual_role_garment_and_size_context", len(matching_triggers) == 1 and bool(row) and (matching_triggers[0]["data-fit-size-label"] == row[0] or (locale == "ar" and role == "girl" and matching_triggers[0]["data-fit-size-label"] == "سنتين" and row[0] == "2 سنة")))
    active_units = [x["attrs"].get("data-size-guide-unit") for panel in state["panels"] if panel.get("hidden") is False for x in panel.get("buttons", []) if x["attrs"].get("aria-pressed") == "true"]
    check(name + ":guide_unit_selected", active_units == [unit])
    check(name + ":language_viewport_no_document_overflow_cart_zero", state["lang"] == locale and state["viewport"]["width"] == width and state["viewport"]["scrollWidth"] <= width and state["cart"].splitlines()[1] == "0")
    check(name + ":final_module_url", state["modules"] == [expected_module_url])
    observations.append({"path": name, "role": role, "garment": garment, "unit": unit, "rows": len(t["rows"]), "selectedSize": row[0] if row else None, "bust": number(row[bi]) if row and bi is not None else None, "garmentLength": number(row[li]) if row and li is not None else None})
    return state


for locale in ["en", "fr", "ar"]:
    for mode, width, height in [("desktop", 1280, 720), ("mobile", 390, 844)]:
        prefix = f"browser/accepted-{locale}-{mode}"
        initial = evidence(prefix + "-initial.json")
        if expected_module_url is None:
            expected_module_url = initial["modules"][0]
        check(prefix + ":initial_locale_viewport_module", initial["lang"] == locale and initial["viewport"]["width"] == width and initial["viewport"]["height"] == height and initial["modules"] == [expected_module_url])
        no_type = evidence(prefix + "-no-type.json")
        no_type_count += 1
        check(prefix + ":no_type_clear_prompt_without_measurements", not no_type["measurements"] and table(no_type) is None and any(x.get("hidden") is False and x.get("text", "").strip() for x in no_type["panels"]) and any(x.get("data-fit-pending-axis") for x in no_type["triggers"]))
        for role in ["mother", "girl"]:
            for step, garment in [("cardigan-initial", "cardigan"), ("dress", "dress"), ("cardigan", "cardigan"), ("dress-return", "dress")]:
                inspect_guide(f"{prefix}-{role}-{step}-metric.json", locale, role, garment, "metric", width)
                guide_count += 1
            for unit in ["metric", "imperial"]:
                name = f"{prefix}-{role}-cardigan-compact-{unit}.json"
                state = evidence(name)
                compact_count += 1
                headers = [x["label"] for x in state["measurements"]]
                bi, li = columns(headers)
                expected_suffix = " (in)" if unit == "imperial" else " (cm)"
                check(name + ":correct_compact_role_unit_and_source_values", state["text"].startswith(role_text[locale][role]) and [x["unit"] for x in state["units"] if x["pressed"] == "true"] == [unit] and bi is not None and li is not None and headers[bi].lower().endswith(expected_suffix) and headers[li].lower().endswith(expected_suffix) and number(state["measurements"][bi]["value"]) == source_value(role, "cardigan", 4, unit) and number(state["measurements"][li]["value"]) == source_value(role, "cardigan", 9, unit))
                if locale == "fr":
                    check(name + ":French_units_not_capitalized", all(x["transform"] == "none" for x in state["measurements"]))
            imperial_name = f"{prefix}-{role}-cardigan-guide-imperial.json"
            imperial = inspect_guide(imperial_name, locale, role, "cardigan", "imperial", width)
            imperial_count += 1
            reopened_name = f"{prefix}-{role}-cardigan-reopen.json"
            reopened = inspect_guide(reopened_name, locale, role, "cardigan", "imperial", width)
            reopen_count += 1
            first_table, reopened_table = table(imperial), table(reopened)
            check(reopened_name + ":same_guide_rows_headers_after_reopen", first_table is not None and reopened_table is not None and first_table["headers"] == reopened_table["headers"] and [r["text"] for r in first_table["rows"]] == [r["text"] for r in reopened_table["rows"]])

no_size = evidence("browser/accepted-en-desktop-dress-no-size.json")
check("no_size_guide_has_no_false_selected_row", table(no_size) is not None and len(table(no_size)["rows"]) == 5 and not any("is-selected" in r.get("cls", "") for r in table(no_size)["rows"]) and all(not x.get("data-fit-size-label") for x in no_size["triggers"]))


def luminance(rgb):
    values = [float(x) / 255 for x in re.findall(r"[0-9.]+", rgb)[:3]]
    linear = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in values]
    return sum(a * b for a, b in zip(linear, [.2126, .7152, .0722]))


cta_rows = []
for locale in ["en", "ar", "nl"]:
    normal = evidence(f"browser/{locale}-article-normal.json")["cta"][0]
    for label, suffix in [("normal", "normal"), ("hover", "hover-verified"), ("focus", "focus-verified")]:
        name = f"browser/{locale}-article-{suffix}.json"
        state = evidence(name)
        cta = state["cta"][0]
        lum = sorted([luminance(cta["color"]), luminance(cta["background"])])
        ratio = (lum[1] + .05) / (lum[0] + .05)
        check(name + ":readable_preserved_CTA", cta["text"] == normal["text"] and cta["href"] == normal["href"] and ratio >= 4.5 and cta["rect"]["height"] >= 44)
        if label == "hover":
            check(name + ":actual_hover", cta["hover"] is True)
        if label == "focus":
            check(name + ":actual_visible_focus", cta["focus"] is True and cta["focusVisible"] is True and cta["boxShadow"] != "none")
        cta_rows.append({"path": name, "contrastRatio": round(ratio, 2), "href": cta["href"], "text": cta["text"]})
    arrival = evidence(f"browser/{locale}-article-arrival.json")
    check(locale + ":CTA_actual_arrival_and_cart_zero", arrival["url"] == normal["href"] and arrival["cart"].splitlines()[1] == "0")

au_rows = []
for variant, role, size, color, price in [("41871506735201", "girl", "3-4 Years", "yellow", "4700"), ("41871520235617", "boy", "3-4 Years", "blue", "3700"), ("44047092613217", "mother", "S", "Polar Adventure Cream", "5700")]:
    name = f"browser/au-numeric-{variant}.json"
    state = evidence(name)
    native = evidence(name.replace(".json", "-native.json"))
    query = parse_qs(urlsplit(state["url"]).query)
    attributes = [x["attributes"] for x in state["selected"]]
    check(name + ":automatic_role_size_price_color_market", query.get("variant") == [variant] and query.get("country") == ["AU"] and query.get("currency") == ["AUD"] and any(x.get("data-select-role-group") == role for x in attributes) and any(x.get("data-size-label") == size and x.get("data-price") == price for x in attributes) and any(x.get("value") == color for x in native["native"]) and "Australia | AUD" in native["country"] and "AUD" in state["mainPrice"] and state["cart"].splitlines()[1] == "0")
    au_rows.append({"path": name, "role": role, "size": size, "color": color, "minorUnitPrice": price, "sourceVersion": "First saved86; one subsequent French normalization line does not alter variant code."})

console = evidence("browser/captured-console-errors.json")
check("captured_console_errors_empty", console == [])
check("expected_acceptance_counts_reconciled", (guide_count, compact_count, imperial_count, reopen_count, no_type_count, len(cta_rows), len(au_rows)) == (48, 24, 12, 12, 6, 9, 3))
report = {
    "reviewer": "/root/main_sync_review",
    "reviewedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASS" if all(c["pass"] for c in checks) else "FAIL",
    "checks": checks,
    "guideObservations": observations,
    "ctaObservations": cta_rows,
    "auObservations": au_rows,
    "counts": {"metricGuides": guide_count, "compactUnits": compact_count, "imperialGuides": imperial_count, "reopens": reopen_count, "noType": no_type_count, "noSize": 1, "CTAStates": len(cta_rows), "CTAArrivals": 3, "AUPreselections": len(au_rows)},
    "finalModuleURLInAcceptedSnapshots": expected_module_url,
    "reviewedFileHashes": {name: sha(P / name) for name in sorted(used)},
    "limits": ["Independent local evaluation of root-owned raw captures, no reviewer browser actions. Revision2 only recognizes observed baseline EN/AR unit capitalization and the exact Arabic two-year size spelling equivalence; all role, numeric source, selected unit, and count assertions remain.", "Numeric chest and garment-length values are compared with source cells; localized suffixes and extra valid height columns are retained, not treated as formatting failures.", "Unit controls and role-switch resets retain their pre-existing separate behavior; no cross-role persistence claim.", "Only cited accepted captures plus CTA/AU evidence support this review; diagnostic/intermediate files are excluded from acceptance."],
}
destination = P / "review/final-browser-independent-checks-v2.json"
assert not destination.exists(), "Keep original review results"
destination.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"status": report["status"], "checks": len(checks), "failed": [c for c in checks if not c["pass"]], "reportSha256": sha(destination)}, indent=2))
