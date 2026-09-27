#!/usr/bin/env python3
"""Apply reviewer corrections: {"<locale>": {"<gid>": {"from": old, "to": new}}}.
Guard: English digest equals before_state.json and live value equals "from".
Also rewrites translations/<locale>.json so the packet records the final value.
Usage: python3 patch_titles.py <patch.json> [--execute]"""
import importlib.util, json, sys, pathlib, datetime
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("s", ROOT / "ops/scripts/sync_live_theme_from_main.py")
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
patch = json.loads(pathlib.Path(sys.argv[1]).read_text()); before = json.loads((HERE / "before_state.json").read_text())
execute = "--execute" in sys.argv; log = []
for loc, items in patch.items():
    for pid, ch in items.items():
        r = s.gql('query($id:ID!,$l:String!){translatableResource(resourceId:$id){translatableContent{key digest} translations(locale:$l){key value}}}', {"id": pid, "l": loc})["translatableResource"]
        dig = next(c["digest"] for c in r["translatableContent"] if c["key"] == "title")
        cur = next((t["value"] for t in r["translations"] if t["key"] == "title"), None)
        if dig != before[pid]["digest"] or cur != ch["from"]:
            raise SystemExit(f"GUARD FAIL {pid} {loc}: live={cur!r}")
        print(f"{loc} {pid.split('/')[-1]}: {cur!r} -> {ch['to']!r}")
        if not execute: continue
        t = s.gql('mutation($id:ID!,$t:[TranslationInput!]!){translationsRegister(resourceId:$id,translations:$t){userErrors{message}}}',
                  {"id": pid, "t": [{"locale": loc, "key": "title", "value": ch["to"], "translatableContentDigest": dig}]})["translationsRegister"]
        if t["userErrors"]: raise SystemExit(t["userErrors"])
        f = HERE / "translations" / f"{loc}.json"; d = json.loads(f.read_text()); d[loc][pid] = ch["to"]; f.write_text(json.dumps(d, ensure_ascii=False, indent=1))
        log.append({"id": pid, "locale": loc, "from": ch["from"], "to": ch["to"], "at": datetime.datetime.utcnow().isoformat() + "Z"})
if execute:
    out = HERE / "patch_log.json"; prev = json.loads(out.read_text()) if out.exists() else []
    out.write_text(json.dumps(prev + log, ensure_ascii=False, indent=1)); print("patched", len(log))
