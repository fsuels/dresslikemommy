#!/usr/bin/env python3
"""Rebuild complete body_html translations for the products/locales in full_todo.json.

Every translation is assembled from the CURRENT English body_html by replacing each
non-numeric text leaf with tr_full_<locale>.json, so the tag sequence is identical to
English by construction (verified). A locale is skipped if any text leaf lacks a
translation. Registers with translationsRegister against the current digest and reads
back value equality + outdated=false. Dry run unless --execute.
"""
import json, pathlib, re, sys
from collections import Counter
HERE = pathlib.Path(__file__).resolve().parent
ns = {"__file__": str(HERE / "patch_register.py")}
exec((HERE / "patch_register.py").read_text().split("TR = {")[0], ns)
split, join, gql = ns["split"], ns["join"], ns["gql"]
EXECUTE = "--execute" in sys.argv
TODO = json.load(open(HERE / "full_todo.json", encoding="utf-8"))["todo"]
NUMERIC = re.compile(r"[\d\s.,/\-–~≈()%+cmkg]*")
TR = {}
for path in HERE.glob("tr_full_*.json"):
    TR[path.stem.replace("tr_full_", "")] = json.load(open(path, encoding="utf-8"))

Q = ("query($h:String!){ productByHandle(handle:$h){ id translatableResource: id } }")
stats, log = Counter(), []
for handle, locales in TODO.items():
    pid = gql("query($h:String!){ productByHandle(handle:$h){ id } }", {"h": handle})["productByHandle"]["id"]
    res = gql("query($id:ID!){ translatableResource(resourceId:$id){ translatableContent { key value digest } } }", {"id": pid})["translatableResource"]
    body = next(c for c in res["translatableContent"] if c["key"] == "body_html")
    et, el = split(body["value"])
    batch = []
    for l in locales:
        entry = {"handle": handle, "locale": l}
        tr = TR.get(l)
        if tr is None:
            entry["result"] = "SKIP_NO_LOCALE_FILE"
        else:
            out, missing = [], 0
            for leaf in el:
                s = leaf.strip()
                if not s or NUMERIC.fullmatch(s):
                    out.append(leaf)
                elif s in tr:
                    lead = re.match(r"\s*", leaf).group()
                    trail = re.search(r"\s*$", leaf).group()
                    out.append(lead + tr[s] + trail)
                else:
                    missing += 1
                    out.append(leaf)
            value = join(et, out)
            if missing:
                entry["result"] = f"SKIP_MISSING_{missing}_LEAVES"
            elif split(value)[0] != et:
                entry["result"] = "SKIP_TAG_GUARD"
            else:
                entry["result"] = "READY"
                batch.append({"locale": l, "key": "body_html", "value": value, "translatableContentDigest": body["digest"]})
        log.append(entry)
    if EXECUTE and batch:
        r = gql("mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ field message } } }",
                {"id": pid, "t": batch})["translationsRegister"]
        if r["userErrors"]:
            for e in log:
                if e["handle"] == handle and e["result"] == "READY":
                    e["result"] = f"ERROR {r['userErrors'][:1]}"
            continue
        want = {b["locale"]: b["value"] for b in batch}
        for l in want:
            got = gql('query($id:ID!,$l:String!){ translatableResource(resourceId:$id){ translations(locale:$l){ key value outdated } } }',
                      {"id": pid, "l": l})["translatableResource"]["translations"]
            g = next((x for x in got if x["key"] == "body_html"), {})
            ok = g.get("value") == want[l] and g.get("outdated") is False
            for e in log:
                if e["handle"] == handle and e["locale"] == l:
                    e["result"] = "REGISTERED_VERIFIED" if ok else "REGISTERED_READBACK_MISMATCH"
for e in log:
    stats[e["result"]] += 1
json.dump(log, open(HERE / ("full_register_log.json" if EXECUTE else "full_register_dry_run.json"), "w"), indent=1, ensure_ascii=False)
print(dict(stats))
