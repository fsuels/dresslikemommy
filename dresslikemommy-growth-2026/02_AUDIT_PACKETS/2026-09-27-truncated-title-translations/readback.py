import json, glob, urllib.request, concurrent.futures, re
ROUTE = {"pt-BR": "pt"}
before = json.load(open("before_state.json")); after = json.load(open("after_state.json"))
plan = {}
for f in glob.glob("translations/*.json"):
    for loc, items in json.load(open(f)).items():
        for pid, v in items.items():
            if loc == "de" or pid in plan.get(loc, {}) or True: plan.setdefault(loc, {})[pid] = v
M = re.compile(r"\|\s*DLM|\.\.\.|…")
pairs = [(loc, pid, v) for loc, d in plan.items() for pid, v in d.items() if before[pid]["titles"].get(loc) and M.search(before[pid]["titles"][loc]["value"])]
admin_bad = [(l, p) for l, p, v in pairs if (after[p]["titles"].get(l) or {}).get("value") != v or (after[p]["titles"].get(l) or {}).get("outdated")]
def sf(x):
    l, p, v = x
    try:
        t = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://www.dresslikemommy.com/{ROUTE.get(l, l.lower())}/products/{before[p]['handle']}.js", headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read())["title"]
        return None if t == v else (l, p, t)
    except Exception as e: return (l, p, f"ERR {e}")
with concurrent.futures.ThreadPoolExecutor(8) as ex: sf_bad = [r for r in ex.map(sf, pairs) if r]
en_changed = [p for p in before if before[p]["en_title"] != after[p]["en_title"] or before[p]["digest"] != after[p]["digest"]]
res = {"pairs_written": len(pairs), "admin_mismatch_or_outdated": admin_bad, "storefront_mismatch": sf_bad[:20], "storefront_mismatch_count": len(sf_bad), "english_changed": en_changed}
json.dump(res, open("after_readback.json", "w"), ensure_ascii=False, indent=1)
print({k: (v if isinstance(v, int) else len(v)) for k, v in res.items()})
