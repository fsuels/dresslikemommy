#!/usr/bin/env python3
"""Patch current body_html translations for the 32 copy-cleaned products.

For each product and locale, the current translated body_html is split into text
leaves between HTML tags (same HTML_TAG_RE the translation backend uses). Only the
leaves whose English text changed in the copy cleanup are replaced with
tr_<locale>.json translations. Leaf positions map by identical tag sequence, or by
difflib-aligned tag neighbours when a locale's tags differ (size-chart repairs).

Guards:
- skip locales that were already outdated before the cleanup (copy_fixes.json),
  and locales with no translation;
- skip the pair if any changed leaf cannot be mapped, or if the translated leaf being
  replaced still equals the OLD English (already untranslated there);
- the patched value must keep the translation's exact tag sequence.
Dry run by default; --execute registers with translationsRegister against the
current body_html digest and reads back outdated=false and value equality.
"""
import difflib, json, pathlib, sys, urllib.request
from collections import Counter
REPO = pathlib.Path(__file__).resolve().parents[6]
sys.path.insert(0, str(REPO))
from ops.scripts.translation_utils import HTML_TAG_RE
from ops.scripts.shopify_admin_config import load_access_token

HERE = pathlib.Path(__file__).resolve().parent
FIX = {p["handle"]: p for p in json.load(open(HERE.parent / "copy_fixes.json"))["products"]}
PLAN = json.load(open(HERE / "plan.json"))
LOCALES = ["ar","cs","da","de","el","es","fi","fr","he","hi","it","ja","ko","nl","no","pl","pt-BR","ro","ru","sv"]
EXECUTE = "--execute" in sys.argv
TOKEN = load_access_token()


def gql(q, v):
    req = urllib.request.Request("https://dresslikemommy-com.myshopify.com/admin/api/2026-01/graphql.json",
        data=json.dumps({"query": q, "variables": v}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    d = json.loads(urllib.request.urlopen(req, timeout=60).read())
    if d.get("errors"):
        raise RuntimeError(d["errors"])
    return d["data"]


def split(html):  # (tags, leaves) by match spans; HTML_TAG_RE has a capture group, so re.split would interleave tags
    tags, leaves, pos = [], [], 0
    for m in HTML_TAG_RE.finditer(html):
        leaves.append(html[pos:m.start()]); tags.append(m.group(0)); pos = m.end()
    leaves.append(html[pos:])
    return tags, leaves


def join(tags, leaves):
    out = [leaves[0]]
    for t, l in zip(tags, leaves[1:]):
        out += [t, l]
    return "".join(out)


def leaf_map(en_tags, tr_tags):
    """Map English leaf index -> translated leaf index via aligned tag neighbours."""
    tag_map = {}
    for a, b, size in difflib.SequenceMatcher(None, en_tags, tr_tags, autojunk=False).get_matching_blocks():
        for k in range(size):
            tag_map[a + k] = b + k
    n_en, n_tr = len(en_tags), len(tr_tags)
    mapping = {}
    for i in range(n_en + 1):
        left = -1 if i == 0 else tag_map.get(i - 1)
        right = n_tr if i == n_en else tag_map.get(i)
        if left is None or right is None:
            continue
        if right == left + 1:  # both neighbours aligned and adjacent in the translation
            mapping[i] = left + 1
    return mapping


TR = {l: json.load(open(HERE / f"tr_{l}.json", encoding="utf-8")) for l in LOCALES}
Q = "query($id:ID!){ translatableResource(resourceId:$id){ translatableContent { key digest } " + " ".join(
    f'{l.replace("-", "_")}: translations(locale:"{l}"){{ key value outdated }}' for l in LOCALES) + " } }"
REG = ("mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)"
       "{ translations { locale key } userErrors { field message code } } }")

stats, log = Counter(), []
for row in PLAN:
    fix = FIX[row["handle"]]
    pre_outdated = set(fix["translation_impact"].get("locales_already_outdated") or [])
    ot, ol = split(fix["before_html"])
    nt, nl = split(fix["after_html"])
    changed = row["changed"]
    res = gql(Q, {"id": row["gid"]})["translatableResource"]
    digest = next(c["digest"] for c in res["translatableContent"] if c["key"] == "body_html")
    batch = []
    for l in LOCALES:
        cur = next((x for x in res[l.replace("-", "_")] if x["key"] == "body_html"), None)
        entry = {"handle": row["handle"], "locale": l}
        if not cur or not cur["value"]:
            entry["result"] = "SKIP_MISSING"
        elif l in pre_outdated:
            entry["result"] = "SKIP_PRE_OUTDATED"
        else:
            tt, tl = split(cur["value"])
            m = {i: i for i in range(len(ol))} if tt == ot else leaf_map(ot, tt)
            if any(i not in m for i in changed):
                entry["result"] = "SKIP_UNMAPPED"
            elif any(tl[m[i]].strip() and tl[m[i]] == ol[i] for i in changed):
                entry["result"] = "SKIP_LEAF_UNTRANSLATED"
            else:
                new_leaves = list(tl)
                for i in changed:
                    new_leaves[m[i]] = TR[l][nl[i]]
                value = join(tt, new_leaves)
                if HTML_TAG_RE.findall(value) != tt:
                    entry["result"] = "SKIP_TAG_GUARD"
                else:
                    entry["result"] = "READY_IDENTITY" if tt == ot else "READY_ALIGNED"
                    batch.append({"locale": l, "key": "body_html", "value": value, "translatableContentDigest": digest})
        stats[entry["result"]] += 1
        log.append(entry)
    if EXECUTE and batch:
        r = gql(REG, {"id": row["gid"], "t": batch})["translationsRegister"]
        if r["userErrors"]:
            for e in log[-len(LOCALES):]:
                if e["result"].startswith("READY"):
                    e["result"] = f"ERROR {r['userErrors'][:1]}"
            stats["ERROR"] += len(batch)
            continue
        back = gql(Q, {"id": row["gid"]})["translatableResource"]
        want = {b["locale"]: b["value"] for b in batch}
        for e in log[-len(LOCALES):]:
            if e["locale"] in want:
                got = next((x for x in back[e["locale"].replace("-", "_")] if x["key"] == "body_html"), {})
                ok = got.get("value") == want[e["locale"]] and got.get("outdated") is False
                e["result"] = "REGISTERED_VERIFIED" if ok else "REGISTERED_READBACK_MISMATCH"
                stats[e["result"]] += 1

out = HERE / ("register_log.json" if EXECUTE else "register_dry_run.json")
json.dump(log, open(out, "w"), indent=1, ensure_ascii=False)
print(dict(stats))
