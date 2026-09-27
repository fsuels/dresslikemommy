#!/usr/bin/env python3
"""Register (or roll back) the shortened German `title` translations.

Usage: python3 apply_de_titles.py [--execute] [--rollback]
Guarded: each product's English title digest must equal before_state.json,
and the live German title must equal the expected starting value.
"""
import importlib.util, json, sys, pathlib, datetime
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("s", ROOT / "ops/scripts/sync_live_theme_from_main.py")
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
plan = json.loads((HERE / "plan.json").read_text())
before = {p["id"]: p for p in json.loads((HERE / "before_state.json").read_text())}
execute = "--execute" in sys.argv; rollback = "--rollback" in sys.argv
log = []
for pid, new_de in plan.items():
    b = before[pid]
    old_de = b["de_title"]["value"]
    exp, target = (new_de, old_de) if rollback else (old_de, new_de)
    r = s.gql('query($id:ID!){translatableResource(resourceId:$id){translatableContent{key digest} translations(locale:"de"){key value}}}', {"id": pid})["translatableResource"]
    digest = next(c["digest"] for c in r["translatableContent"] if c["key"] == "title")
    cur = next((t["value"] for t in r["translations"] if t["key"] == "title"), None)
    if digest != b["title_digest"] or cur != exp:
        raise SystemExit(f"GUARD FAIL {pid}: digest_ok={digest == b['title_digest']} live_de={cur!r} expected={exp!r}")
    print(f"{pid.split('/')[-1]}: {cur!r}\n   -> {target!r}")
    if not execute:
        continue
    t = s.gql('mutation($id:ID!,$t:[TranslationInput!]!){translationsRegister(resourceId:$id,translations:$t){translations{locale key value} userErrors{field message}}}',
              {"id": pid, "t": [{"locale": "de", "key": "title", "value": target, "translatableContentDigest": digest}]})["translationsRegister"]
    if t["userErrors"]:
        raise SystemExit(f"userErrors {pid}: {t['userErrors']}")
    log.append({"id": pid, "at": datetime.datetime.utcnow().isoformat() + "Z", "rollback": rollback, "value": t["translations"][0]["value"]})
if execute:
    out = HERE / ("rollback_log.json" if rollback else "apply_log.json")
    prev = json.loads(out.read_text()) if out.exists() else []
    out.write_text(json.dumps(prev + log, ensure_ascii=False, indent=1))
    print(f"registered {len(log)}")
