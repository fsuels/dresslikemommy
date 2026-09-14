"""Build the reviewed local overlay; never produce a Microsoft import or mutate sources."""
import csv
import hashlib
import json
import re
import unicodedata
from urllib.parse import urlparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
REVIEW = BASE / "negative-review-20260911"


def rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(text):
    return re.findall(r"\w+", unicodedata.normalize("NFKC", text).casefold())


def contains(needle, haystack):
    return any(haystack[i:i + len(needle)] == needle for i in range(len(haystack) - len(needle) + 1))


source = rows(BASE / "negative_keywords.csv")
reviewed = rows(REVIEW / "negative_review.csv")
receipt = json.loads((REVIEW / "review_receipt.json").read_text())
positives = rows(BASE / "keywords.csv")
groups = {r["ad_group_key"]: r for r in rows(BASE / "ad_groups.csv")}
checks = []


def check(name, result, **evidence):
    checks.append({"check": name, "passed": bool(result), **evidence})
    if not result:
        raise AssertionError(name)


check("ten frozen source inputs preserved", all(digest(BASE / p) == h for p, h in receipt["input_hashes_verified_before_and_after"].items()))
check("all five reviewer output hashes match", all(digest(REVIEW / p) == h for p, h in receipt["files"].items()))
review_by_line = {int(r["source_csv_line"]): r for r in reviewed}
held_lines = {i for i, r in enumerate(source, 2) if r["local_state"] == "HOLD_SEMANTIC_REVIEW"}
check("exact 103 held source lines reviewed once", len(reviewed) == len(review_by_line) == 103 and set(review_by_line) == held_lines)
identity_fields = ["campaign_key", "ad_group_key", "scope", "negative_keyword", "match_type"]
check("all reviewed source identities match", all(all(r[k] == source[i - 2][k] for k in identity_fields) for i, r in review_by_line.items()))
decisions = Counter(r["decision"] for r in reviewed)
check("decision partition reconciles", decisions == {"QUALIFIED_LOCAL_SEED": 48, "KEEP_HELD": 44, "REJECT": 11})
qualified = [r for r in reviewed if r["decision"] == "QUALIFIED_LOCAL_SEED"]
check("48 qualified candidates retain exact tee ad-group scope", all(r["scope"] == "AdGroup" and r["ad_group_key"].endswith("_tees") and groups[r["ad_group_key"]]["intent"] == "tees" for r in qualified))
sunshine_handle = json.loads((BASE / "launch-plan-20260911/shopify_candidate_readback.json").read_text())["data"]["sunshine"]["handle"]
check("qualified landing stays on fixed Sunshine product", all(urlparse(r["final_url"]).hostname == "www.dresslikemommy.com" and urlparse(r["final_url"]).path.endswith("/products/" + sunshine_handle) and r["final_url"] == groups[r["ad_group_key"]]["final_url"] for r in qualified))
check("zero qualified initial dress stage additions", all(r["initial_dress_stage_eligible"] == "false" for r in qualified))
same_group_conflicts = []
sibling_conflicts = []
for negative in qualified:
    for positive in positives:
        if positive["campaign_key"] != negative["campaign_key"]:
            continue
        if contains(tokens(negative["negative_keyword"]), tokens(positive["keyword"])):
            pair = [negative["local_negative_key"], positive["keyword_key"]]
            (same_group_conflicts if positive["ad_group_key"] == negative["ad_group_key"] else sibling_conflicts).append(pair)
check("independent literal screen finds no same-group collision", not same_group_conflicts)
check("eight scoped candidates retain explicit sibling conflict warning", len({x[0] for x in sibling_conflicts}) == 8, conflicting_candidate_keys=sorted({x[0] for x in sibling_conflicts}))
check("qualified subset is exact", rows(REVIEW / "qualified_local_seeds.csv") == qualified)
priority = [r for r in reviewed if r["campaign_key"] in {"ms_us_en_202609", "ms_de_de_202609"}]
check("priority subset is exact and remains tee reserves", rows(REVIEW / "us_germany_priority.csv") == priority and Counter(r["decision"] for r in priority) == {"QUALIFIED_LOCAL_SEED": 11, "KEEP_HELD": 8, "REJECT": 1})
initial = [r for r in source if r["local_staging_state"] == "MINIMAL_PAUSED_STAGE_PROPOSAL"]
check("14 original initial dress negatives preserved", len(initial) == 14 and all(r["local_state"] != "HOLD_SEMANTIC_REVIEW" for r in initial))

overlay = []
status_map = {"QUALIFIED_LOCAL_SEED": "ROOT_REVIEWED_LOCAL_TEE_RESERVE", "KEEP_HELD": "HOLD_SPECIFIC_EVIDENCE", "REJECT": "REJECTED_AS_WRITTEN"}
for line, original in enumerate(source, 2):
    decision = review_by_line.get(line)
    overlay.append({
        **original,
        "source_csv_line": line,
        "effective_review_state": status_map[decision["decision"]] if decision else "UNCHANGED_STRONG_INTENT_PROPOSAL",
        "effective_stage": "LOCAL_TEE_RESERVE_ONLY" if decision and decision["decision"] == "QUALIFIED_LOCAL_SEED" else "EXCLUDED_FROM_STAGING" if decision else original["local_staging_state"],
        "scope_guard": "EXACT_AD_GROUP_ONLY_NO_CAMPAIGN_OR_SHARED_LIST" if decision else "PRESERVE_ORIGINAL_SCOPE",
        "native_import_or_activation_approved": "false",
        "decision_key": decision["local_negative_key"] if decision else "",
        "decision_rationale": decision["rationale"] if decision else original["reason"],
    })
check("overlay covers all 180 sources without changing originals", len(overlay) == 180 and all(all(r[k] == original[k] for k in original) for r, original in zip(overlay, source)))
check("11 rejected and 44 held rows remain excluded", all(r["effective_stage"] == "EXCLUDED_FROM_STAGING" for r in overlay if r["effective_review_state"] in {"HOLD_SPECIFIC_EVIDENCE", "REJECTED_AS_WRITTEN"}))
check("no platform import or activation authorization", all(r["native_import_or_activation_approved"] == "false" for r in overlay))
overlay_path = OUT / "effective_negative_review.csv"
with overlay_path.open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(overlay[0]))
    writer.writeheader()
    writer.writerows(overlay)

result = {
    "as_of_utc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS_LOCAL_INTEGRATION__NO_IMPORT_OR_ACTIVATION",
    "reviewer": "root01a08703; did not author the 103 row judgments",
    "semantic_challenge": {
        "accepted_with_limits": "All 48 candidates apply only to the advertised fixed Sunshine tee offer, never the store or sibling dress groups. Offer changes and actual mixed-intent queries require re-review.",
        "rejected_wording": "11 broad French/German/Spanish/Italian phrases remain rejected as written, including maillot, kleider, vestido(s), abito/i and vestito/i.",
        "alternative_considered": "Promoting these to campaign negatives would block sibling dress intent; explicit ad-group scope is retained. Using no cross-garment seeds also remains a valid native-test choice.",
        "source_limits": "Current product variants are configuration evidence, not supplier stock or a complete store assortment. Dictionary senses demonstrate ambiguity, not observed lost sales. No native-language certification or query-performance evidence.",
        "primary_sources": receipt["primary_sources"],
        "root_refreshed_sources": ["Microsoft negative-keyword rules", "Duden Kleid plural sense", "RAE vestido", "Treccani vestito"],
        "matching_limits": "Independent token screen is diagnostic only and does not emulate Microsoft negative matching or close variants.",
    },
    "counts": dict(Counter(r["effective_review_state"] for r in overlay)),
    "initial_dress_stage": {"negative_rows": 14, "new_negative_rows": 0, "tee_ad_groups_added": 0},
    "checks_passed": len(checks),
    "checks": checks,
    "overlay": {"path": overlay_path.name, "sha256": digest(overlay_path), "not_a_platform_import": True},
    "source_preservation": receipt["input_hashes_verified_before_and_after"],
    "rollback": "Stop using this dated overlay and revert its campaign-plan pointer; all original CSVs remain byte-identical. No external rollback required.",
}
(OUT / "negative_integration_review.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"status": result["status"], "checks_passed": len(checks), "counts": result["counts"], "initial_dress_stage": result["initial_dress_stage"]}))
