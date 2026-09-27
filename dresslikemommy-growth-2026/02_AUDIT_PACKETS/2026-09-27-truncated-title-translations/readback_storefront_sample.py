import json, glob, urllib.request, random, time, re
ROUTE = {"pt-BR": "pt"}; random.seed(7)
before = json.load(open("before_state.json")); M = re.compile(r"\|\s*DLM|\.\.\.|…")
final = {}
for f in glob.glob("translations/*.json"):
    for loc, items in json.load(open(f)).items(): final.setdefault(loc, {}).update(items)
checked, bad = 0, []
for loc, items in sorted(final.items()):
    elig = [p for p in items if before[p]["titles"].get(loc) and M.search(before[p]["titles"][loc]["value"])]
    for pid in random.sample(elig, min(10, len(elig))):
        url = f"https://www.dresslikemommy.com/{ROUTE.get(loc, loc.lower())}/products/{before[pid]['handle']}.js"
        for attempt in range(5):
            try:
                t = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read())["title"]; break
            except urllib.error.HTTPError as e:
                if e.code == 429: time.sleep(5 * (attempt + 1)); continue
                t = f"HTTP {e.code}"; break
        checked += 1
        if t != items[pid]: bad.append((loc, pid, t, items[pid]))
        time.sleep(0.6)
res = {"sampled": checked, "mismatches": bad}
json.dump(res, open("after_storefront_sample.json", "w"), ensure_ascii=False, indent=1)
print("sampled", checked, "mismatches", len(bad), bad[:3])
