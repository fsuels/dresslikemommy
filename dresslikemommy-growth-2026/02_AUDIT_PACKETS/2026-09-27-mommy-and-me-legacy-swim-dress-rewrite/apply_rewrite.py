#!/usr/bin/env python3
"""Apply (or roll back) the Mommy & Me legacy swimsuit/dress title/handle rewrite.

Usage: python3 apply_rewrite.py <product-gid|all> [--execute] [--rollback]
Guarded: refuses to write unless the live title+handle equal the expected
starting state (before_state.json for apply, plan.json for rollback).
"""
import importlib.util, json, sys, pathlib, datetime
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("s", ROOT / "ops/scripts/sync_live_theme_from_main.py")
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)

plan = json.loads((HERE / "plan.json").read_text())
before = {p["id"]: p for p in json.loads((HERE / "before_state.json").read_text())}
target = sys.argv[1]; execute = "--execute" in sys.argv; rollback = "--rollback" in sys.argv
ids = list(plan) if target == "all" else [target]
log = []

for pid in ids:
    p, b = plan[pid], before[pid]
    if rollback:
        exp_title, exp_handle = p["new_title"], p["new_handle"]
        new_title, new_handle = b["title"], b["handle"]
        tr = {l: next((x["value"] for x in b["translations"][l] if x["key"] == "title"), None) for l in b["translations"]}
    else:
        exp_title, exp_handle = b["title"], b["handle"]
        new_title, new_handle = p["new_title"], p["new_handle"]
        tr = p["translations"]
    cur = s.gql("query($id:ID!){product(id:$id){title handle}}", {"id": pid})["product"]
    if (cur["title"], cur["handle"]) != (exp_title, exp_handle):
        raise SystemExit(f"GUARD FAIL {pid}: live {cur} != expected ({exp_title!r}, {exp_handle!r})")
    print(f"{pid}: {cur['handle']} -> {new_handle}\n   {cur['title']!r} -> {new_title!r}")
    if not execute:
        continue
    r = s.gql("""mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{id title handle} userErrors{field message}}}""",
              {"p": {"id": pid, "title": new_title, "handle": new_handle, "redirectNewHandle": True}})["productUpdate"]
    if r["userErrors"]:
        raise SystemExit(f"productUpdate userErrors {pid}: {r['userErrors']}")
    tc = s.gql("query($id:ID!){translatableResource(resourceId:$id){translatableContent{key value digest}}}", {"id": pid})["translatableResource"]["translatableContent"]
    title_c = next(c for c in tc if c["key"] == "title")
    assert title_c["value"] == new_title, title_c
    inputs = [{"locale": l, "key": "title", "value": v, "translatableContentDigest": title_c["digest"]} for l, v in tr.items() if v]
    t = s.gql("""mutation($id:ID!,$t:[TranslationInput!]!){translationsRegister(resourceId:$id,translations:$t){translations{locale key} userErrors{field message}}}""",
              {"id": pid, "t": inputs})["translationsRegister"]
    if t["userErrors"]:
        raise SystemExit(f"translationsRegister userErrors {pid}: {t['userErrors']}")
    print(f"   updated -> {r['product']['handle']}; translations registered: {len(t['translations'])}")
    log.append({"id": pid, "at": datetime.datetime.utcnow().isoformat() + "Z", "rollback": rollback,
                "product": r["product"], "translations_registered": len(t["translations"])})

if execute:
    out = HERE / ("rollback_log.json" if rollback else "apply_log.json")
    prev = json.loads(out.read_text()) if out.exists() else []
    out.write_text(json.dumps(prev + log, ensure_ascii=False, indent=1))
