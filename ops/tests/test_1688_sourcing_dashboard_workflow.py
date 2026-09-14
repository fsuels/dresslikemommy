#!/usr/bin/env python3
"""Focused regressions for the Sourcing Studio review and preparation workflow."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_dashboard.py"


def load_dashboard():
    spec = importlib.util.spec_from_file_location("sourcing_dashboard_workflow_test", DASHBOARD_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {DASHBOARD_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def candidate(score: int, *, title: str) -> dict[str, object]:
    return {
        "candidate_id": "workflow-fixture",
        "review_stage": "search",
        "verdict": "Reject",
        "score": score,
        "product_url": "https://supplier.example.invalid/offer/917144772399.html",
        "image_url": "https://image.example.invalid/product.jpg",
        "title": title,
        "price_cny": "39.90",
        "moq": "1",
        "monthly_sales": "300",
        "repurchase_rate_pct": "83%",
        "rating": "",
        "years_on_1688": "",
        "category_match": "5",
        "style_fit": "4",
        "image_quality": "4",
        "ip_risk_flags": "",
        "positive_signals": ["strong repeat-buyer signal (83%)", "MOQ 1"],
        "concerns": [
            "European market focus requires a 2026/new-listing freshness signal or newer 1688 offer ID",
            "size chart still needs confirmation",
            "shop/service rating missing",
        ],
        "search_query": "母女沙滩裙 2026 夏季 新款",
        "market_target": "eu",
        "category_id": "mommy-and-me",
    }


def main() -> None:
    dashboard = load_dashboard()
    with tempfile.TemporaryDirectory(prefix="dlm-sourcing-workflow-") as temporary:
        root = Path(temporary)
        sourcing = root / "ops" / "sourcing"
        dashboard.REPO_ROOT = root
        dashboard.SOURCING_ROOT = sourcing
        dashboard.CATEGORIES_PATH = sourcing / "sourcing-categories.json"
        dashboard.DECISIONS_PATH = sourcing / "state" / "decisions.json"
        dashboard.SEARCH_HISTORY_PATH = sourcing / "state" / "search-history.json"
        dashboard.DRAFT_PACKAGES_ROOT = sourcing / "draft-packages"
        dashboard.PHOTOSHOOT_PROMPT_PATH = root / "ops" / "prompts" / "photoshoot.md"
        dashboard.PHOTOSHOOT_PROMPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        dashboard.PHOTOSHOOT_PROMPT_PATH.write_text("# Image brief\n", encoding="utf-8")
        write_json(
            dashboard.CATEGORIES_PATH,
            {
                "market_profiles": [
                    {"id": "balanced", "label": "Balanced", "short_label": "Balanced", "query_modifiers": []},
                    {"id": "eu", "label": "Europe", "short_label": "Europe", "query_modifiers": []},
                ],
                "categories": [
                    {
                        "id": "mommy-and-me",
                        "label": "Mommy & Me",
                        "listing_mode": "Mommy and Me",
                        "primary_focus": "Mother-child matching dresses and sets.",
                        "queries": [],
                    }
                ],
            },
        )
        write_json(dashboard.DECISIONS_PATH, {"version": 1, "updated_at": "", "items": {}})

        old_run = sourcing / "2026-09-01-100000-mommy-and-me-eu-1688-auto"
        new_run = sourcing / "2026-09-02-100000-mommy-and-me-eu-1688-auto"
        write_json(
            old_run / "run.json",
            {"run_id": old_run.name, "category_id": "mommy-and-me", "market_target": "eu", "stage": "search"},
        )
        write_json(
            old_run / "scored-candidates.json",
            {"generated_at": "2026-09-01T10:00:00+00:00", "candidates": [candidate(88, title="Old high score")]},
        )
        write_json(
            new_run / "run.json",
            {"run_id": new_run.name, "category_id": "mommy-and-me", "market_target": "eu", "stage": "search"},
        )
        write_json(
            new_run / "scored-candidates.json",
            {"generated_at": "2026-09-02T10:00:00+00:00", "candidates": [candidate(53, title="New current evidence")]},
        )

        candidates = dashboard.load_candidates()
        assert len(candidates) == 1
        selected = candidates[0]
        assert selected["title"] == "New current evidence", "newer search evidence must beat an older higher score"
        assert selected["opportunity_score"] == 53
        assert selected["review_recommended"] is True, "strong category/demand fit should be routed to verification"
        assert selected["supplier_rating_label"] == "Unavailable"
        assert selected["supplier_rating_provenance"] == "Not collected from the search card"
        assert dashboard.latest_run_summary(candidates)["reviewable"] == 1
        summary = dashboard.parse_collection_summary("reviewable=6 total=210 queries=10 browser_errors=1")
        assert summary == {"reviewable": 6, "total": 210, "queries": 10, "browser_errors": 1}

        dashboard.chrome_browser_status = lambda: {
            "ok": False,
            "blocked": True,
            "message": "Helper browser login required.",
        }
        first = dashboard.start_listing_prep(selected["key"])
        second = dashboard.start_listing_prep(selected["key"])
        assert first["stage"] == "needs_attention"
        assert second["stage"] == "needs_attention", "starting preparation again must resume instead of duplicating state"
        decisions = json.loads(dashboard.DECISIONS_PATH.read_text(encoding="utf-8"))
        assert len(decisions["items"]) == 1
        decision = decisions["items"][selected["key"]]
        assert decision["action"] == "keep"
        assert decision["workflow"]["stage"] == "needs_attention"
        package = dashboard.DRAFT_PACKAGES_ROOT / selected["key"]
        assert (package / "candidate.json").exists()
        assert "STOP: This is a preparation package only" in (package / "draft-agent-prompt.md").read_text(encoding="utf-8")

        complete_evidence = {
                "size_chart_source": "attached chart",
                "vendor_images_path": "local images",
                "generated_images_path": "",
                "dropship_confirmed": "yes",
                "dispatch_confirmed": "48 hours",
                "supplier_confirmed": "verified supplier",
            }
        assert dashboard.listing_ready(complete_evidence), "usable vendor images must satisfy the image gate without requiring generated images"
        assert not dashboard.listing_ready(
            {**complete_evidence, "dropship_confirmed": "not confirmed"}
        ), "negative proof text must not unlock the handoff"
        merged_evidence = dashboard.merge_editable_evidence(
            {"detail_evidence_path": "local/detail-evidence.json", "detail_verdict": "Test"},
            {"notes": "operator note", "detail_verdict": "Gold"},
        )
        assert merged_evidence["detail_evidence_path"] == "local/detail-evidence.json"
        assert merged_evidence["detail_verdict"] == "Test", "operator proof edits must not overwrite verifier-owned fields"
        assert merged_evidence["notes"] == "operator note"
        assert not dashboard.draft_handoff_ready({**selected, "evidence": complete_evidence}), "search-card evidence alone must not unlock the Shopify-draft handoff"
        assert dashboard.draft_handoff_ready(
            {**selected, "review_stage": "detail", "verdict": "Test", "evidence": complete_evidence}
        ), "detail proof plus complete evidence should unlock the DRAFT-only handoff"
        rejected_detail = {
            **selected,
            "review_stage": "detail",
            "verdict": "Reject",
            "evidence": {**complete_evidence, "detail_evidence_path": "local/detail.json", "detail_verdict": "Reject"},
        }
        assert not dashboard.draft_handoff_ready(rejected_detail), "a rejected supplier detail result must fail closed"
        assert [item["field"] for item in dashboard.preparation_missing(rejected_detail)] == ["detail_rejection"]
        assert dashboard.opportunity_confidence(rejected_detail) == "Low", "rejected detail proof must not display high confidence"

        dashboard.DETAIL_JOBS.clear()
        dashboard.DETAIL_JOBS["existing-job"] = {
            "id": "existing-job",
            "key": selected["key"],
            "status": "running",
        }
        assert dashboard.start_detail_job(selected["key"])["id"] == "existing-job"

    print("ok")


if __name__ == "__main__":
    main()
