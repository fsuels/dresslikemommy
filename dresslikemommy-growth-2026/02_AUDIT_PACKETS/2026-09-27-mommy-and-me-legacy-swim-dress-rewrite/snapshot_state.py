#!/usr/bin/env python3
"""Snapshot title/handle/seo/status/collections and title+handle+meta_title translations
for the products in plan.json. Usage: python3 snapshot_state.py <out.json>"""
import importlib.util, json, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("s", ROOT / "ops/scripts/sync_live_theme_from_main.py"); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
plan = json.load(open(HERE / "plan_en.json")); ids = list(plan)
locs = [l["locale"] for l in s.gql('{shopLocales{locale primary published}}')["shopLocales"] if not l["primary"] and l["published"]]
out = {}
for i in range(0, len(ids), 50):
    ch = ids[i:i+50]
    for p in s.gql('query($ids:[ID!]!){nodes(ids:$ids){... on Product{id title handle status seo{title description} collections(first:40){nodes{handle}}}}}', {"ids": ch})["nodes"]:
        out[p["id"]] = {**p, "collections": sorted(c["handle"] for c in p["collections"]["nodes"]), "translations": {}}
    for l in locs:
        for n in s.gql('query($ids:[ID!]!,$l:String!){translatableResourcesByIds(first:50,resourceIds:$ids){nodes{resourceId translatableContent{key digest} translations(locale:$l){key value outdated}}}}', {"ids": ch, "l": l})["translatableResourcesByIds"]["nodes"]:
            out[n["resourceId"]]["title_digest"] = next(c["digest"] for c in n["translatableContent"] if c["key"] == "title")
            out[n["resourceId"]]["translations"][l] = [t for t in n["translations"] if t["key"] in ("title", "handle", "meta_title")]
json.dump(list(out.values()), open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("snapshot", len(out), "| handle translations:", sum(1 for p in out.values() for l in locs if any(t["key"] == "handle" for t in p["translations"][l])))
