#!/usr/bin/env python3
"""Plan a segment-level translation patch for the 32 copy-cleaned descriptions.
For each product: split old/new English body_html into (tags, text leaves) with the
same HTML_TAG_RE the translation backend uses; find changed text leaves; fetch each
locale's current body_html translation and check its tag sequence equals the OLD
English tag sequence (so leaf i maps to leaf i). Output plan.json + strings_en.json."""
import json, pathlib, re, sys, difflib, urllib.request
REPO = pathlib.Path(__file__).resolve().parents[6]
sys.path.insert(0, str(REPO))
from ops.scripts.translation_utils import HTML_TAG_RE
from ops.scripts.shopify_admin_config import load_access_token
HERE = pathlib.Path(__file__).resolve().parent
FIX = json.load(open(HERE.parent / "copy_fixes.json"))["products"]
APPLIED = {r["handle"] for r in json.load(open(HERE.parent / "apply" / "apply_log.json")) if r["result"] == "APPLIED_VERIFIED"}
LOCALES = ["ar","cs","da","de","el","es","fi","fr","he","hi","it","ja","ko","nl","no","pl","pt-BR","ro","ru","sv"]
TOKEN = load_access_token()
def gql(q, v):
    req = urllib.request.Request("https://dresslikemommy-com.myshopify.com/admin/api/2026-01/graphql.json",
        data=json.dumps({"query": q, "variables": v}).encode(), headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["data"]
def split(html):  # (tags, leaves) by match spans; HTML_TAG_RE has a capture group, so re.split would interleave tags
    tags, leaves, pos = [], [], 0
    for m in HTML_TAG_RE.finditer(html):
        leaves.append(html[pos:m.start()]); tags.append(m.group(0)); pos = m.end()
    leaves.append(html[pos:])
    return tags, leaves
Q = "query($id:ID!){ translatableResource(resourceId:$id){ " + " ".join(
    f'{l.replace("-","_")}: translations(locale:"{l}"){{ key value outdated }}' for l in LOCALES) + " } }"
plan, strings = [], {}
for p in FIX:
    if p["handle"] not in APPLIED: continue
    ot, ol = split(p["before_html"]); nt, nl = split(p["after_html"])
    row = {"handle": p["handle"], "gid": p["gid"], "same_tags": ot == nt, "changed": [], "locales": {}}
    if ot == nt:
        for i, (a, b) in enumerate(zip(ol, nl)):
            if a != b and b.strip():
                row["changed"].append(i); strings[b] = 1
    tr = gql(Q, {"id": p["gid"]})["translatableResource"]
    for l in LOCALES:
        body = next((x for x in tr[l.replace("-","_")] if x["key"] == "body_html"), None)
        if not body or not body["value"]:
            row["locales"][l] = "MISSING"; continue
        row["locales"][l] = "ALIGNED" if HTML_TAG_RE.findall(body["value"]) == ot else "TAGS_DIFFER"
    plan.append(row)
json.dump(plan, open(HERE / "plan.json", "w"), indent=1)
json.dump(sorted(strings), open(HERE / "strings_en.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print("products", len(plan), "| same tag structure old/new:", sum(r["same_tags"] for r in plan))
print("locale alignment:", Counter(s for r in plan for s in r["locales"].values()))
print("changed leaves total:", sum(len(r["changed"]) for r in plan), "| unique new EN strings:", len(strings), "| chars:", sum(len(s) for s in strings))
for r in plan:
    if not r["same_tags"] or "TAGS_DIFFER" in r["locales"].values() or "MISSING" in r["locales"].values():
        print("  ", r["handle"][:45], "same_tags=", r["same_tags"], Counter(r["locales"].values()))
