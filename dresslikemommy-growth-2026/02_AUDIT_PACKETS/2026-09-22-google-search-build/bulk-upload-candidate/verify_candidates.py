from pathlib import Path
from collections import Counter
import csv
import hashlib
import json

BASE = Path(__file__).parent
payload = json.loads((BASE.parent / "payload.json").read_text())
manifest = json.loads((BASE / "candidate_manifest.json").read_text())
sources = json.loads((BASE / "sources/template_manifest.json").read_text())
campaign = payload["campaign"]["name"]
checks = 0
def check(value):
    global checks
    assert value
    checks += 1

rows_by_file = {}
for entry in manifest["files"]:
    data = (BASE / entry["file"]).read_bytes()
    check(hashlib.sha256(data).hexdigest() == entry["sha256"])
    with (BASE / entry["file"]).open(newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        check(reader.fieldnames == entry["headers"])
    source = next(s for s in sources if s["file"] == entry["sourceFile"])
    source_header = next(r for r in source["tables"]["CSV"] if r and r[0] in ["Row Type", "Row type", "Action"])
    check(set(entry["headers"]).issubset(source_header))
    check(len(rows) == entry["rowCount"])
    for row in rows:
        check(None not in row and row["Campaign"] == campaign)
        check(row["Action"].lower() == "add")
        if entry["statusColumn"]:
            check(row[entry["statusColumn"]] == "Paused")
    rows_by_file[entry["file"]] = rows

group_rows = rows_by_file["01_ad_groups.PREVIEW_ONLY.csv"]
keyword_rows = rows_by_file["02_keywords.PREVIEW_ONLY.csv"]
ad_rows = rows_by_file["03_responsive_search_ads.PREVIEW_ONLY.csv"]
for group in payload["ad_groups"]:
    imported_group = next(g for g in group_rows if g["Ad group"] == group["name"])
    check(float(imported_group["Default max. CPC"]) == float(group["proposed_default_cpc_usd"]))
    found = [k for k in keyword_rows if k["Ad group"] == group["name"]]
    check(len(found) == 8)
    for keyword in group["keywords"]:
        expected_type = "Exact match" if keyword["match_type"] == "EXACT" else "Phrase match"
        row = next(k for k in found if k["Keyword"] == keyword["text"] and k["Type"] == expected_type)
        if keyword["match_type"] == "EXACT":
            check(float(row["Default max. CPC"]) == float(keyword["proposed_max_cpc_usd"]))
        else:
            check(row["Default max. CPC"] == "")
    ad = next(a for a in ad_rows if a["Ad group"] == group["name"])
    check(ad["Description 1 position"] == "1")
    check(not any(k.endswith(" position") for k in ad if k != "Description 1 position"))
    for i, text in enumerate(group["rsa"]["headlines"], 1):
        check(ad[f"Headline {i}"] == text["text"] and len(ad[f"Headline {i}"]) <= 30)
    for i, text in enumerate(group["rsa"]["descriptions"], 1):
        check(ad[f"Description {i}"] == text["text"] and len(ad[f"Description {i}"]) <= 90)
    check(ad["Final URL"] == group["rsa"]["final_url"])
    check([ad["Path 1"], ad["Path 2"]] == [p["text"] for p in group["rsa"]["display_paths"]])

negative_rows = rows_by_file["04_campaign_negatives.PREVIEW_ONLY.csv"] + rows_by_file["05_ad_group_negatives.PREVIEW_ONLY.csv"]
expected_negatives = payload["negative_keywords"]["campaign"] + payload["negative_keywords"]["ad_groups"]
actual_keys = Counter((n["Level"], n["Ad group"], n["Negative keyword"], n["Type"]) for n in negative_rows)
expected_keys = Counter(("Campaign" if n["scope"] == "CAMPAIGN" else "Ad group", n.get("ad_group", ""), n["text"], "Exact match" if n["match_type"] == "EXACT" else "Phrase match") for n in expected_negatives)
check(actual_keys == expected_keys)
check(len(negative_rows) == 67)

links = rows_by_file["06_sitelink_associations.HELP_TEMPLATE_PREVIEW_ONLY.csv"]
check(Counter((r["Ad group"], r["Sitelink text"]) for r in links) == Counter((a["ad_group"], a["sitelink_id"]) for a in payload["assets"]["sitelink_associations"]))
check(len({(r["Sitelink text"], r["Description"], r["Description 2"], r["Final URL"]) for r in links}) == 6)
for row in links:
    asset = next(a for a in payload["assets"]["sitelinks"] if a["text"] == row["Sitelink text"])
    check(row["Description"] == asset["description_1"] and row["Description 2"] == asset["description_2"] and row["Final URL"] == asset["final_url"])
    check(row["Level"] == "Ad group")
callouts = rows_by_file["07_callouts.HELP_TEMPLATE_PREVIEW_ONLY.csv"]
check([c["Callout text"] for c in callouts] == [c["text"] for c in payload["assets"]["callouts"]])
check(all(c["Ad group"] == "" for c in callouts))
snippet = rows_by_file["08_structured_snippet.HELP_TEMPLATE_PREVIEW_ONLY.csv"][0]
check(snippet["Ad group"] == "Mommy & Me Outfits" and snippet["Structured snippet header"] == "Types")
check(snippet["Structured snippet values"] == "Dresses;Pajamas;Matching Sets")
stub = json.loads((BASE / "campaign_stub.NOT_UPLOADABLE.json").read_text())
check(stub["proposedRow"]["Budget"] is None and stub["proposedRow"]["Budget type"] is None)
check(stub["proposedRow"]["Campaign status"] == "Paused")
check(not any("campaign_template" in p.name for p in BASE.glob("*.csv")))
check(len(list(BASE.glob("*.csv"))) == 8)
check(sum(len(r) for r in rows_by_file.values()) == 146)
check(hashlib.sha256((BASE.parent / "payload.json").read_bytes()).hexdigest() == manifest["payloadSha256"])
result = {"status": "PASS_WITH_LIMITS_LOCAL_SCHEMA_AND_CONTENT_ONLY", "assertions": checks, "csv_files": 8, "csv_data_rows": 146, "paused_entity_and_negative_rows": 127, "executable_campaign_csv_rows": 0, "native_preview": "NOT_RUN", "external_apply": "NOT_RUN"}
(BASE / "independent_validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
