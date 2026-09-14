"""Read-only validation of this review packet; writes only sibling validation.json."""
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import collections
import csv
import datetime
import hashlib
import io
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
checks = {}


def rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(name, result):
    checks[name] = bool(result)


candidates = rows(HERE / "candidate_rows_all.csv")
scopes = rows(HERE / "country_language_scopes.csv")
countries = rows(HERE / "country_coverage.csv")
negatives = rows(HERE / "negative_candidates.csv")
risks = rows(HERE / "negative_do_not_apply.csv")
audit = rows(HERE / "legacy_universe_audit.csv")
duplicate_groups = rows(HERE / "cross_source_duplicates.csv")
manifest = json.loads((HERE / "canonical_corrections_manifest.json").read_text())
source_manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text())
current_market_rows = rows(HERE.parent / "markets/active_country_inventory.csv")
locale_roots = {
    r["locale"]: r["root_url"]
    for r in rows(HERE.parent / "markets/locale_routes.csv")
}

record("60_candidates_3_text_prepared_57_held", len(candidates) == 60 and
       collections.Counter(r["status"] for r in candidates) == {"PREPARED": 3, "HELD": 57})
record("all_activation_held", all(r["activation_gate"].startswith("HELD:") for r in candidates))
record("no_current_cpc_volume_or_campaign_invented", all(
    r["current_cpc_usd"] == r["current_volume"] == r["proposed_campaign_id"] == ""
    for r in candidates))
record("unique_country_language_text_match", len({
    (r["country"], r["language"], r["keyword"].casefold(), r["match_candidate"])
    for r in candidates}) == len(candidates))
record("unique_candidate_ids", len({r["candidate_id"] for r in candidates}) == len(candidates))
record("exact_phrase_only", all(r["match_candidate"] in {"EXACT", "PHRASE"} for r in candidates))
record("native_and_overlap_gates_present", all(
    r["required_native_validation"] and r["existing_campaign_overlap"].startswith("UNKNOWN")
    for r in candidates))
record("first_batch_is_only_US_sunshine_exact", all(
    r["market_scope"] == "US_EN" and r["match_candidate"] == "EXACT" and
    "/products/sunshine-stripe-family-matching-tops" in r["landing_candidate"]
    for r in candidates if r["status"] == "PREPARED"))

route_ok = True
for row in candidates:
    url = urlparse(row["landing_candidate"])
    locale = "pt-BR" if row["language"] == "pt" else row["language"]
    root_path = urlparse(locale_roots.get(locale, "")).path
    route_ok &= (url.scheme == "https" and url.netloc == "www.dresslikemommy.com"
                 and parse_qs(url.query) == {"country": [row["country"]]}
                 and bool(root_path) and url.path.startswith(root_path))
record("candidate_country_and_configured_locale_routes", route_ok)

market_files = sorted((HERE / "markets").glob("*.csv"))
partition = [r for f in market_files for r in rows(f)]
record("23_market_csv_partition_matches_all_rows", len(market_files) == 23 and
       sorted(partition, key=lambda r: r["candidate_id"]) ==
       sorted(candidates, key=lambda r: r["candidate_id"]))
record("23_scopes_18_countries", len(scopes) == 23 and len({r["country"] for r in scopes}) == 18)
record("scope_row_counts", all(int(s["candidate_rows"]) == sum(
    r["market_scope"] == s["market_scope"] for r in candidates) for s in scopes))
record("65_countries_unique_and_all_held", len(countries) == len({r["country"] for r in countries}) == 65
       and all(r["status"] == "HELD" for r in countries))
current_by_country = {r["country_code"]: r for r in current_market_rows}
record("country_currency_membership_matches_fresh_peer_readback", all(
    r["country"] in current_by_country and
    r["configured_currency"] == current_by_country[r["country"]]["configured_currency"] and
    r["shopify_active_market_membership"] == current_by_country[r["country"]]["market_handles"]
    for r in countries))
record("scope_countries_present_and_google_unknown", all(
    r["country"] in current_by_country and r["current_ads_active_for_country_language"] == "UNKNOWN"
    and r["current_approved_google_offers"] == "NOT_PROVEN" for r in scopes))
record("38_negatives_campaign_held", len(negatives) == 38 and all(
    r["status"] == "HELD" and r["proposed_scope"] == "ONE_REVIEWED_CAMPAIGN_ONLY"
    and r["current_live_change"] == "NONE" for r in negatives))
record("11_false_positive_risks", len(risks) == 11 and {"adult", "free", "pattern"} <=
       {r["term"] for r in risks})
record("no_false_positive_blanket_negative", not (
    {r["negative_keyword"].casefold() for r in negatives} & {r["term"].casefold() for r in risks}))
record("105_universe_audit_rows_and_36_library_duplicate_groups", len(audit) == 105 and len(duplicate_groups) == 36)

source_cache = {}
provenance_ok = True
for row in candidates + negatives:
    path = ROOT / row["source_file"]
    provenance_ok &= path.is_file()
    if row["source_row"].isdigit():
        if path not in source_cache:
            source_cache[path] = rows(path)
        index = int(row["source_row"]) - 2
        source = source_cache[path]
        if not 0 <= index < len(source):
            provenance_ok = False
        else:
            text = row.get("keyword", row.get("negative_keyword"))
            provenance_ok &= text in source[index].values()
record("source_file_and_csv_line_provenance", provenance_ok)

base_texts, new_texts = {}, {}
baseline_matches, candidate_matches = True, True
for rel, target in manifest["targets"].items():
    baseline = ROOT / rel
    candidate = HERE / "canonical_candidate" / rel
    baseline_matches &= sha(baseline) == target["baseline_sha256"]
    candidate_matches &= sha(candidate) == target["candidate_sha256"]
    if rel.endswith(".md"):
        base_texts[Path(rel).name] = baseline.read_text()
        new_texts[Path(rel).name] = candidate.read_text()
record("five_canonical_baseline_hashes_match", len(manifest["targets"]) == 5 and baseline_matches)
record("five_candidate_hashes_match", candidate_matches)
rel = "ops/marketing/keyword_universe.csv"
before, after = rows(ROOT / rel), rows(HERE / "canonical_candidate" / rel)
allowed = set(manifest["changed_csv_fields_only"])
record("universe_schema_order_identity_and_status_preserved", len(before) == len(after) == 105
       and list(before[0]) == list(after[0]) and all(
           all(a[k] == b[k] for k in a if k not in allowed) for a, b in zip(before, after)))
components = [k for k in before[0] if re.search(r"_(?:25|20|15|10|5)$", k)]
record("candidate_score_arithmetic_and_thresholds", all(
    int(r["total_score"]) == sum(int(r[k]) for k in components) and
    r["threshold"] == ("GREEN" if int(r["total_score"]) >= 85 else
                       "YELLOW" if int(r["total_score"]) >= 70 else "RED") for r in after))
record("candidate_thresholds_77_yellow_28_red", collections.Counter(r["threshold"] for r in after) ==
       {"YELLOW": 77, "RED": 28})
record("unknown_economic_serveability_points_zero", all(
    r["economic_fit_10"] == r["serveability_10"] == "0" for r in after))
record("eight_content_watchlist_identities_preserved", sum(r["match_candidate"] == "watchlist"
       for r in after) == 8 and all(a["promotion_status"] == b["promotion_status"] and
       a["live_action"] == b["live_action"] for a, b in zip(before, after)
       if a["match_candidate"] == "watchlist"))
record("owner_limits_present_all_four_guides", all(
    all(x in s for x in ["0.15", "6.5", "30%"]) for s in new_texts.values()))
record("negative_meaning_guard_all_four_guides", all(
    "adult sizes are valid apparel" in s and "“free shipping”" in s and
    "“pattern” can describe a garment" in s for s in new_texts.values()))
record("reviewed_economics_convention_all_four_guides", all(
    "A ≤ min(R/6.5, CM − H − 0.30R, approved cash/loss allowance)" in s
    and "H is" in s and "overhead" in s and "excluding tax" in s
    for s in new_texts.values()))


def failure_cases(texts, universe):
    return {
        "F1_unknown_economic_serveability_points": all(
            r["economic_fit_10"] == r["serveability_10"] == "0" for r in universe),
        "F2_unearned_green_scores": all(r["threshold"] != "GREEN" for r in universe),
        "F3_unqualified_historical_live_labels":
            "Current live US paid lane in the command layer:" not in texts["us_primary_keyword_lane.md"]
            and "GB/CA/AU Search campaigns are live but" not in texts["keyword_strategy.md"],
        "F4_fixed_assumed_CPA_stop_threshold":
            "About `$5.38` spend" not in texts["keyword_scoring_rubric.md"] and
            "Use the rough planning target CPA of `$10.77`." not in texts["keyword_scoring_rubric.md"],
        "F5_broad_negative_false_positives": all(
            "adult sizes are valid apparel" in s and "“free shipping”" in s and
            "“pattern” can describe a garment" in s for s in texts.values()),
    }


frozen_failure_results = {"baseline": failure_cases(base_texts, before),
                          "candidate": failure_cases(new_texts, after)}
record("five_observed_failure_cases_improve", not any(frozen_failure_results["baseline"].values())
       and all(frozen_failure_results["candidate"].values()))
record("rollback_snapshot_hashes_match", all(
    sha(HERE / "canonical_baseline" / rel) == target["baseline_sha256"]
    for rel, target in manifest["targets"].items()))

patch_check = subprocess.run(["git", "apply", "--check", str(HERE / "canonical_corrections.patch")],
                             cwd=ROOT, capture_output=True, text=True)
record("canonical_patch_applies_without_writing", patch_check.returncode == 0)
record("canonical_baselines_unchanged_after_check", all(
    sha(ROOT / rel) == target["baseline_sha256"] for rel, target in manifest["targets"].items()))
record("packet_no_trailing_spaces", all(not any(line.rstrip("\r\n").endswith((" ", "\t"))
    for line in f.read_text().splitlines(keepends=True)) for f in HERE.rglob("*")
    if f.is_file() and f.suffix in {".md", ".csv", ".json", ".py"}))
links = re.findall(r"\]\(([^)]+)\)", (HERE / "README.md").read_text())
record("readme_links_resolve", all(Path(link).exists() or Path(link) == HERE / "validation.json"
                                    for link in links))
source_drift = [rel for rel, entry in source_manifest["sources"].items()
                if sha(ROOT / rel) != entry["sha256"]]
result = {
    "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "VERIFIED_LOCAL_PACKET" if all(checks.values()) else "FAILED",
    "scope": "Local structure, provenance, unchanged canonical baselines and patch applicability only; no live acceptance.",
    "checks": checks,
    "frozen_failure_results": frozen_failure_results,
    "patch_check": {"exit_code": patch_check.returncode, "output": patch_check.stdout + patch_check.stderr},
    "historical_source_hash_drift": source_drift,
    "source_drift_note": "Historical snapshot hashes remain provenance; independently owned mutable canonical state may advance. Any patch target drift fails its dedicated check.",
    "canonical_written": False,
    "external_actions": "NOT RUN",
}
(HERE / "validation.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"status": result["status"], "checks_passed": sum(checks.values()),
                  "checks_total": len(checks), "failed": [k for k, v in checks.items() if not v],
                  "historical_source_hash_drift": source_drift}, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
