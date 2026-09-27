#!/usr/bin/env python3
"""Seed validated translations for the 2026 Christmas pajama drafts into the
shared product-translation cache, keyed by the exact English source strings the
runners create (title, SEO title/description, body_html, print-name and shared
metafield strings, new color names).

Workaround for PROB-2026-09-25-TRANSLATION-FALLBACK-UNREACHABLE-ON-GOOGLE-429
(Google's free endpoint redirects to a block page from this host). Same method
as the Sept 25 Monster Bloom / Spooky Skeleton / Trick or Treat seeds: only
missing or None cache values are filled; an existing valid value is never
overwritten; refuses to run while any translation poller/closeout is running.

Usage: seed_cache.py [--dry-run] [handle ...]   (default: every spec)
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
CACHE = ROOT / "ops/content/shopify-product-translation-live-cache.json"
REUSE = ROOT / "ops/listings/translation-seed-trick-or-treat-family-matching-pajamas"
LOCALES = ["ar", "cs", "da", "de", "el", "es", "fi", "fr", "he", "hi", "it", "ja", "ko", "nl", "no", "pl", "pt-BR", "ro", "ru", "sv"]
BLOCKED = ("1688", "alibaba", "taobao", "http", "www.", "supplier", "grinch", "rudolph", "disney")
sys.path.insert(0, str(TOOLS))
from engine_loader import load  # noqa: E402

DRY = "--dry-run" in sys.argv
wanted = [a for a in sys.argv[1:] if not a.startswith("--")]

# Validated labels/headers already used on live listings (Trick or Treat / Beanie Ghost seeds).
reuse_tr = {}
for part in range(1, 5):
    reuse_tr.update(json.loads((REUSE / f"tr_part{part}.json").read_text(encoding="utf-8")))
reuse_hdr = json.loads((REUSE / "reuse_headers_beanie.json").read_text(encoding="utf-8"))
TR = {loc: json.loads((TOOLS / "i18n" / f"tr_{loc}.json").read_text(encoding="utf-8")) for loc in LOCALES}
EN = json.loads((TOOLS / "i18n" / "en_source.json").read_text(encoding="utf-8"))

errors: list[str] = []


def check(loc: str, key: str, en: str, value, *, label: bool = False, keep_numbers: bool = True) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{loc}.{key}: empty")
        return ""
    v = value.strip()
    if v == en.strip():
        errors.append(f"{loc}.{key}: source-equal")
    low = v.lower()
    for b in BLOCKED:
        if b in low:
            errors.append(f"{loc}.{key}: blocked token {b!r}")
    if re.search(r"[<>]", v) or re.search(r"\{(?!P\}|FABRIC\}|SIZES\})", v):
        errors.append(f"{loc}.{key}: markup or stray brace")
    if label and not v.endswith((":", "：")):
        errors.append(f"{loc}.{key}: label lacks colon")
    if keep_numbers:
        for num in re.findall(r"\d+(?:\.\d+)?%?", en):
            if num not in v:
                errors.append(f"{loc}.{key}: number {num} missing")
    return v


def structure_check(loc: str, tr: dict) -> None:
    for section, en_section in EN.items():
        if section.startswith("_"):
            continue
        got = tr.get(section)
        if not isinstance(got, dict) or set(got) != set(en_section):
            errors.append(f"{loc}.{section}: key set differs from source")
    for ph_key, phs in (("title", ["{P}"]), ("seo_title", ["{P}"]), ("seo_description", ["{P}", "{FABRIC}", "{SIZES}"])):
        t = tr.get("templates", {}).get(ph_key, "")
        for ph in phs:
            if t.count(ph) != 1:
                errors.append(f"{loc}.templates.{ph_key}: placeholder {ph} count {t.count(ph)}")
    if not tr.get("templates", {}).get("title", "").startswith("{P}"):
        errors.append(f"{loc}.templates.title: must start with {{P}}")
    if "Dress Like Mommy" not in tr.get("templates", {}).get("seo_title", ""):
        errors.append(f"{loc}.templates.seo_title: brand missing")


def build_for(spec_path: Path) -> dict[str, dict[str, str]]:
    ns = load(spec_path)
    spec = ns["SPEC"]
    handle = spec["handle"]
    fabric = spec["fabric_key"]
    skey = ns["size_key"]()
    en_seg = ns["en_segments"]()
    body_en = ns["build_body"]()
    out: dict[str, dict[str, str]] = {}
    for loc in LOCALES:
        tr = TR[loc]
        rt = reuse_tr[loc]
        d = tr["designs"][handle]
        sv = tr["size_variants"][skey]
        p = f"{loc}:{handle}"
        mm = ns.get("MM", False)
        sk = lambda key: key + "_mm" if mm and key in ("fam_text", "p1", "p2", "kf1_text", "kf4_text", "cta", "kf5_label") else key
        seg = {
            "fab_label": rt["li1_label"], "fam_label": rt["li2_label"], "prt_label": rt["li3_label"],
            "des_label": rt["li4_label"], "care_label": rt["li5_label"], "size_label": rt["li6_label"],
            "kf1_label": check(p, "kf1_label", en_seg["kf1_label"], tr["shared"]["kf1_label_mm"], label=True) if mm else rt["li7_label"],
            "h3_chart": reuse_hdr[loc]["h3"][0], "h3_kf": reuse_hdr[loc]["h3"][1], "th": list(reuse_hdr[loc]["th"]),
            "fam_text": check(p, "fam_text", en_seg["fam_text"], tr["shared"][sk("fam_text")]),
            "care_text": check(p, "care_text", en_seg["care_text"], tr["shared"]["care_text"]),
            "p1": check(p, "p1", en_seg["p1"], tr["shared"][sk("p1")]),
            "p2": check(p, "p2", en_seg["p2"], tr["shared"]["p2_mm" if mm else ("p2_single" if ns["WAIST_SINGLE"] else "p2")]),
            "kf1_text": check(p, "kf1_text", en_seg["kf1_text"], tr["shared"][sk("kf1_text")]),
            "kf4_label": check(p, "kf4_label", en_seg["kf4_label"], tr["shared"]["kf4_label"], label=True),
            "kf4_text": check(p, "kf4_text", en_seg["kf4_text"], tr["shared"][sk("kf4_text")]),
            "kf5_label": check(p, "kf5_label", en_seg["kf5_label"], tr["shared"][sk("kf5_label")], label=True),
            "cta": check(p, "cta", en_seg["cta"], tr["shared"][sk("cta")]),
            "kf3_label": check(p, "kf3_label", en_seg["kf3_label"], tr["shared"]["kf3_label"], label=True),
            "fab_text": check(p, "fab_text", en_seg["fab_text"], tr["fabric_text"][fabric]),
            "kf3_text": check(p, "kf3_text", en_seg["kf3_text"], tr["fabric_feature_text"][fabric]),
            "des_text": check(p, "des_text", en_seg["des_text"], tr["design_text"][spec["design_key"]]),
            "size_text": check(p, "size_text", en_seg["size_text"], sv["size_text"]),
            "kf5_text": check(p, "kf5_text", en_seg["kf5_text"], sv["kf5_text"], keep_numbers=False),
            "prt_text": check(p, "print_sentence", en_seg["prt_text"], d["print_sentence"]),
            "kf2_label": check(p, "feature_label", en_seg["kf2_label"], d["feature_label"], label=True),
            "kf2_text": check(p, "feature_text", en_seg["kf2_text"], d["feature_text"]),
        }
        if len(seg["th"]) != 10 or not all(h.endswith("(cm)") for h in seg["th"][3:]) or not seg["th"][2].endswith("(kg)"):
            errors.append(f"{p}: reused header shape unexpected")
        print_loc = check(p, "print", spec["print_name"], d["print"], keep_numbers=False)
        body_loc = ns["build_body_from"](seg)
        tag_re = re.compile(r"<[^>]+>")
        if tag_re.findall(body_loc) != tag_re.findall(body_en):
            errors.append(f"{p}: body tag sequence differs from source")
        t = tr["templates_mm" if mm else "templates"]
        mapping = {
            ns["TITLE"]: t["title"].replace("{P}", print_loc),
            ns["SEO_TITLE"]: t["seo_title"].replace("{P}", print_loc),
            ns["SEO_DESCRIPTION"]: t["seo_description"].replace("{P}", print_loc)
                .replace("{FABRIC}", tr["fabric_seo"][fabric]).replace("{SIZES}", sv["size_short"]),
            body_en: body_loc,
            spec["print_name"]: print_loc,
        }
        for en_value, loc_value in tr["metafield_strings"].items():
            mapping[en_value] = check(p, f"mf:{en_value}", en_value, loc_value, keep_numbers=False)
        for color in ns["COLOR_NAMES"]:
            if color in tr["colors"]:
                mapping[color] = check(p, f"color:{color}", color, tr["colors"][color], keep_numbers=False)
        for key in (ns["TITLE"], ns["SEO_TITLE"], ns["SEO_DESCRIPTION"]):
            if "{" in mapping[key] or mapping[key] == key:
                errors.append(f"{p}: template output invalid for {key[:40]}")
        for num in re.findall(r"\d+(?:\.\d+)?%?", ns["SEO_DESCRIPTION"]):
            if num not in mapping[ns["SEO_DESCRIPTION"]]:
                errors.append(f"{p}: seo description lacks {num}")
        out[loc] = mapping
    return out


def main() -> None:
    for loc in LOCALES:
        structure_check(loc, TR[loc])
    specs = sorted((TOOLS / "specs").glob("*.json"))
    if wanted:
        specs = [s for s in specs if s.stem in wanted]
    built = {s.stem: build_for(s) for s in specs}
    if errors:
        print(f"VALIDATION FAILED ({len(errors)}):\n- " + "\n- ".join(errors[:120]))
        sys.exit(1)
    total = sum(len(m) for per in built.values() for m in per.values())
    print(f"validated {len(built)} products x {len(LOCALES)} locales ({total} strings)")
    sample = built[specs[0].stem]["de"]
    (TOOLS / "i18n" / f"sample_de_{specs[0].stem}.json").write_text(json.dumps(sample, ensure_ascii=False, indent=1), encoding="utf-8")
    if DRY:
        return
    running = subprocess.run(
        ["pgrep", "-fl", r"[Pp]ython[^ ]* .*ops/scripts/(poll_shopify_product_translations|finalize_shopify_listing_localization|repair_localized_product_size_charts)\.py"],
        capture_output=True, text=True).stdout.strip()
    if running:
        print("REFUSING: translation process running:", running)
        sys.exit(2)
    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    filled = kept = 0
    for per in built.values():
        for loc, mapping in per.items():
            bucket = cache.setdefault(loc, {})
            for source, value in mapping.items():
                if isinstance(bucket.get(source), str) and bucket[source].strip():
                    kept += 1
                    continue
                bucket[source] = value
                filled += 1
    tmp = CACHE.with_suffix(".json.seed-tmp")
    tmp.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, CACHE)
    print(f"filled={filled} kept_existing={kept}")


if __name__ == "__main__":
    main()
