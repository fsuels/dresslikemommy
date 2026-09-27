#!/usr/bin/env python3
"""Register (or roll back) `title` translations from a translations file.

Usage: python3 apply_titles.py <translations.json> [--execute] [--rollback]
translations.json = {"<locale>": {"<product gid>": "<title>"}}
Guards per (product, locale): the English title digest equals before_state.json,
and the live translation equals the before-state value (apply) or the planned
value (rollback). Only pairs whose before-state value is truncated are applied.
"""
import importlib.util, json, sys, pathlib, datetime, re
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("s", ROOT / "ops/scripts/sync_live_theme_from_main.py")
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
MARK = re.compile(r"\|\s*DLM|\.\.\.|…")
plan = json.loads(pathlib.Path(sys.argv[1]).read_text())
before = json.loads((HERE / "before_state.json").read_text())
execute = "--execute" in sys.argv; rollback = "--rollback" in sys.argv
log, skipped = [], []
for loc, items in plan.items():
    ids = list(items)
    live = {}
    for i in range(0, len(ids), 50):
        r = s.gql('query($ids:[ID!]!,$l:String!){translatableResourcesByIds(first:50,resourceIds:$ids){nodes{resourceId translatableContent{key digest} translations(locale:$l){key value}}}}', {"ids": ids[i:i+50], "l": loc})
        for n in r["translatableResourcesByIds"]["nodes"]:
            live[n["resourceId"]] = (next(c["digest"] for c in n["translatableContent"] if c["key"] == "title"),
                                     next((t["value"] for t in n["translations"] if t["key"] == "title"), None))
    batch = []
    for pid, new in items.items():
        b = before[pid]; old = (b["titles"].get(loc) or {}).get("value")
        if not old or not MARK.search(old):
            skipped.append((pid, loc, "before value not truncated")); continue
        exp, target = (new, old) if rollback else (old, new)
        dig, cur = live[pid]
        if dig != b["digest"] or cur != exp:
            raise SystemExit(f"GUARD FAIL {pid} {loc}: digest_ok={dig == b['digest']} live={cur!r} expected={exp!r}")
        batch.append((pid, target, dig))
    print(f"{loc}: {len(batch)} to write, {sum(1 for x in skipped if x[1] == loc)} skipped")
    if not execute: continue
    for pid, target, dig in batch:
        t = s.gql('mutation($id:ID!,$t:[TranslationInput!]!){translationsRegister(resourceId:$id,translations:$t){translations{value} userErrors{field message}}}',
                  {"id": pid, "t": [{"locale": loc, "key": "title", "value": target, "translatableContentDigest": dig}]})["translationsRegister"]
        if t["userErrors"]: raise SystemExit(f"userErrors {pid} {loc}: {t['userErrors']}")
        log.append({"id": pid, "locale": loc, "rollback": rollback, "value": target, "at": datetime.datetime.utcnow().isoformat() + "Z"})
if execute:
    out = HERE / ("rollback_log.json" if rollback else "apply_log.json")
    prev = json.loads(out.read_text()) if out.exists() else []
    out.write_text(json.dumps(prev + log, ensure_ascii=False, indent=1))
    print(f"registered {len(log)}")
if skipped: print("skipped:", skipped[:5])
