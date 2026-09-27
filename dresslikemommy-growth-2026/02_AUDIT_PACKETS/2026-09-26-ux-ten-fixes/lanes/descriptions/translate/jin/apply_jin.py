#!/usr/bin/env python3
"""Replace the 'jin/source' sentence in shine-star-family-matching-sweatshirts (English, sha-guarded)
and patch the same text leaf in its 20 body_html translations (tag-guarded). Dry run unless --execute."""
import hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[6]
sys.path.insert(0, str(REPO))
src = (HERE.parent / "patch_register.py").read_text().split("TR = {")[0]
ns = {"__file__": str(HERE.parent / "patch_register.py")}
exec(src, ns)                      # reuse split/join/leaf_map/gql/LOCALES from the verified patcher
split, join, leaf_map, gql, LOCALES = ns["split"], ns["join"], ns["leaf_map"], ns["gql"], ns["LOCALES"]
FIX = json.load(open(HERE / "jin_fix.json", encoding="utf-8"))
P = ns["FIX"]["shine-star-family-matching-sweatshirts"]
GID, EXPECT = P["gid"], P["after_sha256"]
EXECUTE = "--execute" in sys.argv
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
log = {"handle": P["handle"]}

cur = gql("query($id:ID!){ product(id:$id){ descriptionHtml } }", {"id": GID})["product"]["descriptionHtml"]
if sha(cur) != EXPECT:
    sys.exit("ABORT: English description changed since the cleanup (sha mismatch)")
assert cur.count(FIX["old_en"]) == 1
new_html = cur.replace(FIX["old_en"], FIX["new_en"])
ot, ol = split(cur); nt, nl = split(new_html)
assert ot == nt
changed = [i for i, (a, b) in enumerate(zip(ol, nl)) if a != b]
assert len(changed) == 1
i = changed[0]
log["english"] = "WOULD_APPLY"
if EXECUTE:
    r = gql("mutation($p:ProductUpdateInput!){ productUpdate(product:$p){ userErrors{ message } } }",
            {"p": {"id": GID, "descriptionHtml": new_html}})["productUpdate"]
    assert not r["userErrors"], r
    back = gql("query($id:ID!){ product(id:$id){ descriptionHtml } }", {"id": GID})["product"]["descriptionHtml"]
    log["english"] = "APPLIED_VERIFIED" if back == new_html else "READBACK_MISMATCH"
    log["after_sha256"] = sha(back)

Q = ("query($id:ID!){ translatableResource(resourceId:$id){ translatableContent { key digest } "
     + " ".join(f'{l.replace("-", "_")}: translations(locale:"{l}"){{ key value outdated }}' for l in LOCALES) + " } }")
res = gql(Q, {"id": GID})["translatableResource"]
digest = next(c["digest"] for c in res["translatableContent"] if c["key"] == "body_html")
batch, per = [], {}
for l in LOCALES:
    t = next((x for x in res[l.replace("-", "_")] if x["key"] == "body_html"), None)
    if not t or not t["value"]:
        per[l] = "SKIP_MISSING"; continue
    tt, tl = split(t["value"])
    m = {k: k for k in range(len(ol))} if tt == ot else leaf_map(ot, tt)
    if i not in m:
        per[l] = "SKIP_UNMAPPED"; continue
    if "jin" not in tl[m[i]].lower() and "斤" not in tl[m[i]] and "근" not in tl[m[i]] and "ג׳ין" not in tl[m[i]] and "जिन" not in tl[m[i]] and "جين" not in tl[m[i]] and "цзин" not in tl[m[i]]:
        per[l] = "SKIP_LEAF_NOT_THE_JIN_SENTENCE"; continue
    tl2 = list(tl); tl2[m[i]] = FIX["translations"][l]
    value = join(tt, tl2)
    if split(value)[0] != tt:
        per[l] = "SKIP_TAG_GUARD"; continue
    per[l] = "READY"
    batch.append({"locale": l, "key": "body_html", "value": value, "translatableContentDigest": digest})
if EXECUTE and batch and log["english"] == "APPLIED_VERIFIED":
    # digest must be for the NEW English body
    res2 = gql(Q, {"id": GID})["translatableResource"]
    digest2 = next(c["digest"] for c in res2["translatableContent"] if c["key"] == "body_html")
    for b in batch: b["translatableContentDigest"] = digest2
    r = gql("mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ field message } } }",
            {"id": GID, "t": batch})["translationsRegister"]
    assert not r["userErrors"], r
    back = gql(Q, {"id": GID})["translatableResource"]
    for b in batch:
        got = next(x for x in back[b["locale"].replace("-", "_")] if x["key"] == "body_html")
        per[b["locale"]] = "REGISTERED_VERIFIED" if got["value"] == b["value"] and got["outdated"] is False else "READBACK_MISMATCH"
log["locales"] = per
json.dump(log, open(HERE / ("apply_log.json" if EXECUTE else "dry_run.json"), "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(log["english"], dict(Counter(per.values())))
