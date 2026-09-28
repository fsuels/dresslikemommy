#!/usr/bin/env python3
"""Merge plan_en.json + translations/*.json into plan.json for apply_rewrite.py."""
import json, glob, pathlib
HERE = pathlib.Path(__file__).resolve().parent
plan = json.load(open(HERE / "plan_en.json"))
for f in sorted(glob.glob(str(HERE / "translations" / "*.json"))):
    for loc, items in json.load(open(f)).items():
        for pid, v in items.items(): plan[pid].setdefault("translations", {})[loc] = v
json.dump(plan, open(HERE / "plan.json", "w"), ensure_ascii=False, indent=1)
print("plan", len(plan), "locales per product", sorted({len(v.get("translations", {})) for v in plan.values()}))
