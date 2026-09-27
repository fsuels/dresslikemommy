#!/usr/bin/env python3
"""Replace one English text leaf in a product description (sha-guarded against copy_fixes before_sha256
or --expect-sha) and patch the mapped leaf in each body_html translation (tag-guarded, keeps the
translated leaf's own leading/trailing whitespace). Usage: apply_leaf_generic.py <fix.json> [--execute] [--expect-sha=...]"""
import hashlib, json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
PATCHER = HERE.parent / "patch_register.py"
ns = {"__file__": str(PATCHER)}
exec(PATCHER.read_text().split("TR = {")[0], ns)
split, join, leaf_map, gql, LOCALES, FIXES = ns["split"], ns["join"], ns["leaf_map"], ns["gql"], ns["LOCALES"], ns["FIX"]
fix_path = HERE / sys.argv[1]
FIX = json.load(open(fix_path, encoding="utf-8"))
EXECUTE = "--execute" in sys.argv
P = FIXES[FIX["handle"]]
GID = P["gid"]
EXPECT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--expect-sha=")), P["before_sha256"])
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
log = {"handle": FIX["handle"]}
cur = gql("query($id:ID!){ product(id:$id){ descriptionHtml } }", {"id": GID})["product"]["descriptionHtml"]
if sha(cur) != EXPECT:
    sys.exit("ABORT: English description changed (sha mismatch)")
ot, ol = split(cur)
idx = [k for k, leaf in enumerate(ol) if leaf.strip() == FIX["old_en"]]
assert len(idx) == 1, idx
i = idx[0]
lead, trail = re.match(r"\s*", ol[i]).group(), re.search(r"\s*$", ol[i]).group()
nl = list(ol); nl[i] = lead + FIX["new_en"] + trail
new_html = join(ot, nl)
log["english"] = "WOULD_APPLY"
if EXECUTE:
    r = gql("mutation($p:ProductUpdateInput!){ productUpdate(product:$p){ userErrors{ message } } }", {"p": {"id": GID, "descriptionHtml": new_html}})["productUpdate"]
    assert not r["userErrors"], r
    back = gql("query($id:ID!){ product(id:$id){ descriptionHtml } }", {"id": GID})["product"]["descriptionHtml"]
    log["english"] = "APPLIED_VERIFIED" if back == new_html else "READBACK_MISMATCH"
    log["after_sha256"] = sha(back)
Q = ("query($id:ID!){ translatableResource(resourceId:$id){ translatableContent { key digest } "
     + " ".join(f'{l.replace("-", "_")}: translations(locale:"{l}"){{ key value outdated }}' for l in LOCALES) + " } }")
res = gql(Q, {"id": GID})["translatableResource"]
batch, per = [], {}
for l in LOCALES:
    t = next((x for x in res[l.replace("-", "_")] if x["key"] == "body_html"), None)
    if not t or not t["value"]:
        per[l] = "SKIP_MISSING"; continue
    tt, tl = split(t["value"])
    m = {k: k for k in range(len(ol))} if tt == ot else leaf_map(ot, tt)
    if i not in m or not tl[m[i]].strip():
        per[l] = "SKIP_UNMAPPED"; continue
    old_tr = tl[m[i]]
    tl2 = list(tl)
    tl2[m[i]] = re.match(r"\s*", old_tr).group() + FIX["translations"][l] + re.search(r"\s*$", old_tr).group()
    value = join(tt, tl2)
    if split(value)[0] != tt:
        per[l] = "SKIP_TAG_GUARD"; continue
    per[l] = "READY"
    log.setdefault("replaced", {})[l] = old_tr.strip()[:140]
    batch.append({"locale": l, "key": "body_html", "value": value})
if EXECUTE and batch and log["english"] == "APPLIED_VERIFIED":
    res2 = gql(Q, {"id": GID})["translatableResource"]
    digest = next(c["digest"] for c in res2["translatableContent"] if c["key"] == "body_html")
    for b in batch:
        b["translatableContentDigest"] = digest
    r = gql("mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ field message } } }", {"id": GID, "t": batch})["translationsRegister"]
    assert not r["userErrors"], r
    back = gql(Q, {"id": GID})["translatableResource"]
    for b in batch:
        got = next(x for x in back[b["locale"].replace("-", "_")] if x["key"] == "body_html")
        per[b["locale"]] = "REGISTERED_VERIFIED" if got["value"] == b["value"] and got["outdated"] is False else "READBACK_MISMATCH"
log["locales"] = per
json.dump(log, open(HERE / (fix_path.stem + ("_apply_log.json" if EXECUTE else "_dry_run.json")), "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(FIX["handle"][:40], log["english"], dict(Counter(per.values())))
