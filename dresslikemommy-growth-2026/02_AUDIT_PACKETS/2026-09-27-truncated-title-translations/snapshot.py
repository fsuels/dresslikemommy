#!/usr/bin/env python3
"""Snapshot English title, digest and every locale's title translation for the
scoped products. Usage: python3 snapshot.py <ids.json> <out.json>"""
import importlib.util, json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("s", ROOT / "ops/scripts/sync_live_theme_from_main.py")
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
ids = json.load(open(sys.argv[1]))
locs = [l["locale"] for l in s.gql('{shopLocales{locale primary published}}')["shopLocales"] if not l["primary"] and l["published"]]
out = {}
for i in range(0, len(ids), 50):
    chunk = ids[i:i+50]
    d = s.gql('query($ids:[ID!]!){nodes(ids:$ids){... on Product{id handle title status collections(first:30){nodes{handle}}}}}', {"ids": chunk})["nodes"]
    for p in d:
        out[p["id"]] = {"handle": p["handle"], "en_title": p["title"], "status": p["status"], "collections": [c["handle"] for c in p["collections"]["nodes"]], "titles": {}}
    for l in locs:
        r = s.gql('query($ids:[ID!]!,$l:String!){translatableResourcesByIds(first:50,resourceIds:$ids){nodes{resourceId translatableContent{key digest value} translations(locale:$l){key value outdated}}}}', {"ids": chunk, "l": l})
        for n in r["translatableResourcesByIds"]["nodes"]:
            tc = next(c for c in n["translatableContent"] if c["key"] == "title")
            out[n["resourceId"]]["digest"] = tc["digest"]
            t = next((t for t in n["translations"] if t["key"] == "title"), None)
            out[n["resourceId"]]["titles"][l] = t
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print("snapshot", len(out), "products x", len(locs), "locales")
