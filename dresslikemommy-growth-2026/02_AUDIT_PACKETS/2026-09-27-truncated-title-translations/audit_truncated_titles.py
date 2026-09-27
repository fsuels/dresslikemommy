#!/usr/bin/env python3
"""Audit ACTIVE products' `title` translations in every published locale for
truncation markers ("| DLM", "...", "…") and titles copied from the SEO title.
Read-only. Usage: python3 audit_truncated_titles.py <out.json>"""
import importlib.util, json, sys, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("s", ROOT / "ops/scripts/sync_live_theme_from_main.py")
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
locs = [l["locale"] for l in s.gql('{shopLocales{locale primary published}}')["shopLocales"] if not l["primary"] and l["published"]]
ids, cur = [], None
while True:
    d = s.gql('query($c:String){products(first:250,after:$c,query:"status:active"){pageInfo{hasNextPage endCursor} nodes{id handle title}}}', {"c": cur})["products"]
    ids += d["nodes"]
    if not d["pageInfo"]["hasNextPage"]: break
    cur = d["pageInfo"]["endCursor"]
byid = {p["id"]: p for p in ids}
MARK = re.compile(r"\|\s*DLM|\.\.\.|…")
findings = []
for l in locs:
    for i in range(0, len(ids), 50):
        chunk = [p["id"] for p in ids[i:i+50]]
        d = s.gql('query($ids:[ID!]!,$l:String!){translatableResourcesByIds(first:50,resourceIds:$ids){nodes{resourceId translatableContent{key value} translations(locale:$l){key value outdated}}}}', {"ids": chunk, "l": l})
        for n in d["translatableResourcesByIds"]["nodes"]:
            tr = {t["key"]: t for t in n["translations"]}
            src = {c["key"]: c["value"] for c in n["translatableContent"]}
            t = tr.get("title")
            if not t: continue
            reasons = []
            if MARK.search(t["value"]) and not MARK.search(src.get("title", "")): reasons.append("marker")
            mt = tr.get("meta_title")
            if mt and mt["value"].strip() == t["value"].strip() and src.get("title") != src.get("meta_title"): reasons.append("equals_seo_title")
            if reasons:
                p = byid[n["resourceId"]]
                findings.append({"id": n["resourceId"], "handle": p["handle"], "en_title": p["title"], "locale": l, "value": t["value"], "outdated": t["outdated"], "reasons": reasons})
    print(l, sum(1 for f in findings if f["locale"] == l), flush=True)
json.dump({"active_products": len(ids), "locales": locs, "findings": findings}, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("active", len(ids), "findings", len(findings), "products", len({f["id"] for f in findings}))
