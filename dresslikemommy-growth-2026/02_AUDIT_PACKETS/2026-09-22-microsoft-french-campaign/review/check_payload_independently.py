"""Independent local attachment-to-payload review; no browser or account writes."""
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

packet = Path(__file__).resolve().parent.parent
payload_path = packet / "payload/campaign_fr_payload.json"
payload = json.loads(payload_path.read_text())
attachment_path = Path(payload["source_attachment"])
attachment = attachment_path.read_text()
errors = []
checks = []


def check(label, actual, expected):
    passed = actual == expected
    checks.append({"check": label, "passed": passed})
    if not passed:
        errors.append({"check": label, "actual": actual, "expected": expected})


def entries(block):
    return re.findall(r'^(?:\[[^\n]+\]|"[^\n]+")$', block, flags=re.M)


def cleaned_lines(block):
    return [line.strip() for line in block.splitlines() if line.strip()]


def normalized(text):
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.findall(r"\w+", text))


check("attachment_sha256", hashlib.sha256(attachment_path.read_bytes()).hexdigest(), payload["source_sha256"])
group_sections = re.split(r"^\d+\. Groupe \d+ — ", attachment, flags=re.M)[1:]
check("group_count", len(payload["groups"]), 8)
check("attachment_group_count", len(group_sections), 8)
for group, section in zip(payload["groups"], group_sections):
    section = re.split(r"^11\. Exclusions de campagne", section, flags=re.M)[0]
    label = "group_" + str(group["number"])
    check(label + "_name", group["name"], section.splitlines()[0].strip())
    check(label + "_url", group["final_url"], re.search(r"^https://[^\n]+$", section, re.M)[0])
    keyword_block = section.split("Mots-clés positifs\n", 1)[1].split("Titres", 1)[0]
    headline_block = re.split(r"^Titres[^\n]*\n", section, flags=re.M)[1].split("Descriptions", 1)[0]
    description_block = re.split(r"^Descriptions[^\n]*\n", section, flags=re.M)[1].split("Exclusions", 1)[0]
    negative_block = section.split("Exclusions", 1)[1]
    check(label + "_keywords_attachment_parity", [k["entry"] for k in group["positive_keywords"]], entries(keyword_block))
    check(label + "_headlines_attachment_parity", group["headlines"], cleaned_lines(headline_block))
    check(label + "_descriptions_attachment_parity", group["descriptions"], cleaned_lines(description_block))
    check(label + "_negatives_attachment_parity", [k["entry"] for k in group["negative_keywords"]], entries(negative_block))
    check(label + "_headline_count", len(group["headlines"]), 15)
    check(label + "_description_count", len(group["descriptions"]), 4)
    for field, maximum in (("headlines", 30), ("descriptions", 90)):
        check(label + "_" + field + "_length", [v for v in group[field] if len(v) > maximum], [])
    for field in ("path1", "path2"):
        check(label + "_" + field + "_length", len(group[field]) <= 15, True)
    for field in ("positive_keywords", "negative_keywords"):
        keywords = group[field]
        check(label + "_" + field + "_entry_consistency", [k for k in keywords if k["entry"] != ("[" + k["text"] + "]" if k["match_type"] == "Exact" else '"' + k["text"] + '"')], [])
        check(label + "_" + field + "_line_consistency", group[field + "_lines"].splitlines(), [k["entry"] for k in keywords])
        check(label + "_" + field + "_unique", len({(k["text"], k["match_type"]) for k in keywords}), len(keywords))

sections = {
    "french_phrase": attachment.split("A. Exclusions françaises — Expression", 1)[1].split("B. Complément anglais", 1)[0],
    "english_phrase": attachment.split("B. Complément anglais pour recherches mixtes — Expression", 1)[1].split("C. Restrictions temporaires", 1)[0],
    "temporary_catalog_exact": attachment.split("C. Restrictions temporaires de catalogue — Exacte", 1)[1].split("D. Ce qui reste", 1)[0],
}
for field, section in sections.items():
    check("campaign_" + field + "_attachment_parity", [k["entry"] for k in payload["campaign_negatives"][field]], entries(section))
all_negatives = [k for field in sections for k in payload["campaign_negatives"][field]]
check("campaign_negative_aggregate", payload["campaign_negatives"]["all"], all_negatives)
check("campaign_negative_lines", payload["campaign_negatives"]["all_lines"].splitlines(), [k["entry"] for k in all_negatives])
check("positive_total", sum(len(g["positive_keywords"]) for g in payload["groups"]), 144)
check("group_negative_total", sum(len(g["negative_keywords"]) for g in payload["groups"]), 58)
check("campaign_french_phrase_total", len(payload["campaign_negatives"]["french_phrase"]), 151)
check("campaign_english_phrase_total", len(payload["campaign_negatives"]["english_phrase"]), 86)
check("campaign_exact_total", len(payload["campaign_negatives"]["temporary_catalog_exact"]), 14)

conflicts = []
for group in payload["groups"]:
    for positive in group["positive_keywords"]:
        for negative in all_negatives + group["negative_keywords"]:
            positive_text = normalized(positive["text"])
            negative_text = normalized(negative["text"])
            blocked = positive_text == negative_text if negative["match_type"] == "Exact" else " " + negative_text + " " in " " + positive_text + " "
            if blocked:
                conflicts.append({"group": group["name"], "positive": positive, "negative": negative})
check("literal_and_accent_folded_negative_conflicts", conflicts, [])

extensions = payload["extensions"]
check("callout_count", len(extensions["callouts"]), 6)
check("callout_lengths", [s for s in extensions["callouts"] if len(s) > 25], [])
check("sitelink_count", len(extensions["sitelinks"]), 8)
for sitelink in extensions["sitelinks"]:
    for field, limit in (("text", 25), ("description1", 35), ("description2", 35)):
        check("sitelink_" + sitelink["text"] + "_" + field + "_length", len(sitelink[field]) <= limit, True)
    group = next(g for g in payload["groups"] if g["number"] == sitelink["group_number"])
    check("sitelink_" + sitelink["text"] + "_url", sitelink["final_url"], group["final_url"])
for group in payload["groups"]:
    check("group_" + str(group["number"]) + "_sitelink_associations", all(name in {s["text"] for s in extensions["sitelinks"]} for name in group["sitelink_associations"]), True)
    check("group_" + str(group["number"]) + "_snippet_lengths", max(map(len, group["structured_snippet"]["values"])) <= 25, True)
    check("group_" + str(group["number"]) + "_source_suffix", group["source_final_url_suffix"] in attachment, True)
    check("group_" + str(group["number"]) + "_candidate_suffix", group["candidate_final_url_suffix_for_fr_ca"], group["source_final_url_suffix"].replace("dlm_ms_us_fr_search_202609", "dlm_ms_fr_ca_fr_search_202609"))

report = {
    "review_type": "INDEPENDENT_LOCAL_PAYLOAD_REVIEW_NO_EXTERNAL_WRITES",
    "payload_sha256": hashlib.sha256(payload_path.read_bytes()).hexdigest(),
    "attachment_sha256": hashlib.sha256(attachment_path.read_bytes()).hexdigest(),
    "checks_total": len(checks),
    "checks_passed": sum(c["passed"] for c in checks),
    "errors": errors,
    "negative_conflicts": conflicts,
    "counts": {
        "groups": len(payload["groups"]),
        "positive_keywords": sum(len(g["positive_keywords"]) for g in payload["groups"]),
        "group_negatives": sum(len(g["negative_keywords"]) for g in payload["groups"]),
        "campaign_negatives": len(all_negatives),
        "headlines": sum(len(g["headlines"]) for g in payload["groups"]),
        "descriptions": sum(len(g["descriptions"]) for g in payload["groups"]),
        "positive_match_types": dict(Counter(k["match_type"] for g in payload["groups"] for k in g["positive_keywords"])),
    },
    "limits": "Local negative comparison tests equality or contiguous words after case/accent/punctuation folding. It does not model Microsoft semantic matching or inherited live negative lists.",
    "checks": checks,
}
output = packet / "review/independent_payload_validation.json"
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({key: value for key, value in report.items() if key != "checks"}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
