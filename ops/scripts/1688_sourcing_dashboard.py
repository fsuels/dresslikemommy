#!/usr/bin/env python3
"""Local Dress Like Mommy sourcing dashboard.

This is a dev/operator app. It reads local 1688 shortlist outputs, persists
Keep/Reject decisions, and prepares handoff prompts. It does not publish to
Shopify and it does not scrape 1688 by itself.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import mimetypes
import os
import re
import subprocess
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, quote_from_bytes, urlparse
import urllib.request


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCING_ROOT = REPO_ROOT / "ops" / "sourcing"
CATEGORIES_PATH = SOURCING_ROOT / "sourcing-categories.json"
SEASONAL_RULES_PATH = SOURCING_ROOT / "seasonal-sourcing.json"
DASHBOARD_TEMPLATE_PATH = SOURCING_ROOT / "sourcing-studio.html"
DECISIONS_PATH = SOURCING_ROOT / "state" / "decisions.json"
SEARCH_HISTORY_PATH = SOURCING_ROOT / "state" / "search-history.json"
SCOUT_STATE_PATH = Path(
    os.environ.get("DLM_SCOUT_STATE_PATH") or (SOURCING_ROOT / "state" / "opportunity-scout.json")
).expanduser()
DRAFT_PACKAGES_ROOT = SOURCING_ROOT / "draft-packages"
IMAGE_CACHE_ROOT = SOURCING_ROOT / "image-cache"
PHOTOSHOOT_PROMPT_PATH = REPO_ROOT / "ops" / "prompts" / "dlm-6-image-photoshoot.md"
COLLECTOR_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_cdp_collect.py"
DETAIL_ENRICH_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_detail_enrich.py"
CDP_PORT = 9333
HELPER_CHROME_PROFILE = Path.home() / ".dlm-1688-chrome-profile"
MEMORY_CACHE_ROOT = Path.home() / ".cache" / "dresslikemommy"
MEMORY_WING = "dresslikemommy-pilot"
COLLECTION_JOBS: dict[str, dict[str, Any]] = {}
COLLECTION_LOCK = threading.Lock()
DETAIL_JOBS: dict[str, dict[str, Any]] = {}
DETAIL_LOCK = threading.Lock()
DECISION_LOCK = threading.RLock()
BROWSER_AUTOMATION_LOCK = threading.Lock()
SCOUT_STATE_LOCK = threading.RLock()
SCOUT_WORKER_LOCK = threading.Lock()
SCOUT_THREADS: dict[str, threading.Thread] = {}
DEFAULT_MARKET_TARGET = "balanced"
MINIMUM_SUPPLIER_YEARS = 5
DEFAULT_SCOUT_INTERVAL_HOURS = 24
DEFAULT_SCOUT_QUERY_BUDGET = 2
DEFAULT_SCOUT_DETAIL_LIMIT = 2


def clean(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def offer_key(product_url: str) -> str:
    match = re.search(r"/offer/(\d+)\.html", clean(product_url))
    if match:
        return match.group(1)
    return clean(product_url)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_json_atomic(path: Path, payload: Any) -> None:
    """Persist resumable operator state without leaving a half-written JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def latest_memory_pilot_root() -> Path:
    configured = clean(os.environ.get("DLM_MEMORY_PILOT_ROOT"))
    if configured:
        return Path(configured).expanduser()
    candidates = [
        path
        for path in MEMORY_CACHE_ROOT.glob("mempalace-pilot-*")
        if (path / "venv" / "bin" / "mempalace").exists() and (path / "palace-small").exists()
    ]
    if not candidates:
        return MEMORY_CACHE_ROOT / "mempalace-pilot-20260425-010721"
    return max(candidates, key=lambda path: (path.stat().st_mtime, path.name))


def memory_paths() -> dict[str, Path]:
    root = latest_memory_pilot_root()
    return {
        "root": root,
        "home": root / "home",
        "bin": root / "venv" / "bin" / "mempalace",
        "palace": root / "palace-small",
        "corpus": root / "corpus-small",
    }


def memory_cli_command(paths: dict[str, Path], *args: str) -> list[str]:
    command = [str(paths["bin"]), *args]
    arch = Path("/usr/bin/arch")
    if arch.exists():
        return [str(arch), "-arm64", *command]
    return command


def memory_status() -> dict[str, Any]:
    paths = memory_paths()
    missing = [name for name, path in paths.items() if name != "corpus" and not path.exists()]
    available = not missing
    status = {
        "available": available,
        "root": str(paths["root"]),
        "wing": MEMORY_WING,
        "missing": missing,
        "message": "Project Memory is ready." if available else "Project Memory is not set up yet.",
    }
    if not available:
        return status
    try:
        completed = subprocess.run(
            memory_cli_command(paths, "--palace", str(paths["palace"]), "status"),
            cwd=str(REPO_ROOT),
            env={**os.environ, "HOME": str(paths["home"]), "ANONYMIZED_TELEMETRY": "FALSE"},
            capture_output=True,
            text=True,
            timeout=12,
            check=False,
        )
    except Exception as exc:
        status.update({"available": False, "message": f"Project Memory exists but could not start: {exc}"})
        return status
    output = completed.stdout or completed.stderr or ""
    drawers_match = re.search(r"MemPalace Status\s+—\s+(\d+)\s+drawers", output)
    status.update(
        {
            "available": completed.returncode == 0,
            "drawers": int(drawers_match.group(1)) if drawers_match else None,
            "message": (
                f"Project Memory is ready with {drawers_match.group(1)} indexed notes."
                if completed.returncode == 0 and drawers_match
                else "Project Memory exists, but status could not be confirmed."
            ),
            "raw_status": output,
        }
    )
    return status


def parse_memory_results(output: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    blocks = re.split(r"\n\s*─{8,}\s*\n", output)
    for block in blocks:
        index_match = re.search(r"\[(\d+)\]\s+([^\n]+)", block)
        if not index_match:
            continue
        source_match = re.search(r"Source:\s*(.+)", block)
        score_match = re.search(r"Match:\s*([0-9.]+)", block)
        snippet = block[score_match.end() :] if score_match else block[index_match.end() :]
        snippet = re.sub(r"^\s+", "", snippet.strip(), flags=re.MULTILINE)
        snippet = re.sub(r"\n{3,}", "\n\n", snippet).strip()
        results.append(
            {
                "rank": int(index_match.group(1)),
                "location": clean(index_match.group(2)),
                "source": clean(source_match.group(1)) if source_match else "",
                "score": float(score_match.group(1)) if score_match else None,
                "snippet": snippet,
            }
        )
    return results


def memory_answer(title: str, summary: str, steps: list[str] | None = None, note: str = "") -> dict[str, Any]:
    return {
        "title": title,
        "summary": summary,
        "steps": steps or [],
        "note": note,
    }


def live_dashboard_memory_answer() -> dict[str, Any]:
    candidates = load_candidates()
    counts = category_counts(candidates)
    total = len(candidates)
    active = sum(bucket.get("active", 0) for bucket in counts.values())
    kept = sum(bucket.get("kept", 0) for bucket in counts.values())
    ready = sum(bucket.get("ready", 0) for bucket in counts.values())
    category_lines: list[str] = []
    categories = category_lookup()
    for category_id, category in categories.items():
        bucket = counts.get(category_id, {})
        category_lines.append(
            f"{category.get('label', category_id)}: {bucket.get('active', 0)} active leads from {bucket.get('total', 0)} stored cards"
        )
    return memory_answer(
        "Current dashboard state",
        f"Right now the local dashboard has {total} stored cards, {active} active leads, {kept} saved products, and {ready} products ready for draft.",
        category_lines,
        "This answer uses the live dashboard data, so it is safer than an old memory note for current counts.",
    )


def humanize_memory_answer(query: str, results: list[dict[str, Any]]) -> dict[str, Any]:
    q_lower = query.lower()
    text = f"{query} " + " ".join(clean(result.get("snippet")) for result in results[:3])
    lower = text.lower()

    if ("latest" in q_lower or "current" in q_lower or "now" in q_lower) and "dashboard" in q_lower:
        return live_dashboard_memory_answer()
    if "captcha" in q_lower or "interception" in q_lower or "blocked" in q_lower or "1688 is blocked" in q_lower:
        return memory_answer(
            "1688 is asking for a browser check",
            "Do not try to bypass it. Open the 1688 helper browser, complete the login or CAPTCHA check in Chrome, then come back to this app and click Find 20 Leads again.",
            [
                "Click Open 1688 Login/Search.",
                "Finish the login or CAPTCHA check in the Chrome tab that opens.",
                "Return to this dashboard.",
                "Click Find 20 Leads again, one category at a time.",
            ],
            "If 1688 keeps blocking, wait a bit before trying again. The app should not force or bypass that check.",
        )
    if ("keep" in q_lower or "reject" in q_lower or "decision" in q_lower) and (
        "live" in q_lower or "memory" in q_lower or "where" in q_lower or "remember" in q_lower
    ):
        return memory_answer(
            "Saved and rejected products are remembered automatically",
            "Use the Save and Reject buttons on product cards. The app remembers those choices so rejected products should not keep coming back.",
            [
                "Click Save when a product is worth checking later.",
                "Click Reject when a product is wrong, stale, risky, or not useful.",
                "Rejected products stay hidden from the active shortlist unless you restore them.",
                "You do not need to edit the decision file yourself.",
            ],
        )
    if "draft package" in q_lower or "package" in q_lower:
        return memory_answer(
            "Draft Package is the handoff for creating a Shopify draft",
            "After proof is complete, Draft Package gathers the product details, listing request, and image prompt into one local package. It is for draft creation only, not live publishing.",
            [
                "Fill and save all proof fields first.",
                "Click Draft Package on the product card.",
                "The app copies the agent handoff prompt.",
                "The product should remain a Shopify draft until you approve it.",
            ],
        )
    if "ready" in q_lower or "proof" in q_lower or "draft" in q_lower:
        return memory_answer(
            "A product needs proof before it can become a draft",
            "The Draft Package button stays blocked until the important proof fields are filled in. This protects the store from weak or unverified listings.",
            [
                "Add the size chart source.",
                "Add the vendor image folder or path.",
                "Add the generated 6-image folder or path.",
                "Confirm dropship support.",
                "Confirm dispatch speed.",
                "Confirm the supplier looks usable.",
                "Click Save Proof.",
            ],
        )
    if "prompt" in q_lower or "listing" in q_lower or "shopify" in q_lower:
        return memory_answer(
            "Use the built-in listing prompt buttons",
            "For listing work, use Copy Listing Agent Prompt or Draft Package from the product card. Those prompts point the agent to the right workflow and keep the product as a draft unless you ask to publish.",
            [
                "Use Copy Listing Agent Prompt when you want help creating listing copy.",
                "Use Copy 6-Image Prompt when you are ready to generate product images.",
                "Use Draft Package only after proof is complete.",
                "Do not publish live unless you explicitly ask for that.",
            ],
        )
    if "category" in q_lower or "categories" in q_lower:
        return memory_answer(
            "The sourcing app uses five store categories",
            "The dashboard groups products by the same main sourcing buckets you use for the shop.",
            ["Mommy & Me", "Daddy & Me", "Family Matching", "Couples", "Maternity"],
        )
    if results:
        sources = ", ".join(result.get("source", "memory note") for result in results[:2])
        return memory_answer(
            "I found related memory notes",
            "I found project notes that may answer this, but I am not confident enough to turn them into a simple instruction yet.",
            [
                f"Best matching source: {sources}.",
                "Try asking with simpler words, for example: 'What proof is needed?' or 'What do I do if 1688 is blocked?'",
            ],
            "The detailed source cards are hidden below so the screen stays readable.",
        )
    return memory_answer(
        "I did not find a clear memory answer",
        "Try asking a shorter question with everyday words.",
        [
            "Examples: 'What proof is needed?'",
            "Examples: 'Where are rejects remembered?'",
            "Examples: 'What do I do if 1688 is blocked?'",
        ],
    )


def search_project_memory(query: str, result_count: int = 5) -> dict[str, Any]:
    query = clean(query)
    if not query:
        raise ValueError("Ask a question first.")
    result_count = max(1, min(result_count, 8))
    status = memory_status()
    if not status.get("available"):
        return {"ok": False, "status": status, "results": [], "message": status.get("message")}
    paths = memory_paths()
    completed = subprocess.run(
        memory_cli_command(
            paths,
            "--palace",
            str(paths["palace"]),
            "search",
            query,
            "--wing",
            MEMORY_WING,
            "--results",
            str(result_count),
        ),
        cwd=str(REPO_ROOT),
        env={**os.environ, "HOME": str(paths["home"]), "ANONYMIZED_TELEMETRY": "FALSE"},
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    output = completed.stdout or ""
    if completed.returncode != 0:
        return {
            "ok": False,
            "status": status,
            "results": [],
            "message": clean(completed.stderr) or "Project Memory search failed.",
            "raw": output,
        }
    results = parse_memory_results(output)
    return {
        "ok": True,
        "status": status,
        "query": query,
        "results": results,
        "raw": output,
        "message": "Memory search finished.",
        "answer": humanize_memory_answer(query, results),
    }


def load_categories() -> list[dict[str, Any]]:
    payload = read_json(CATEGORIES_PATH, {"categories": []})
    return payload.get("categories", [])


def load_market_profiles() -> list[dict[str, Any]]:
    payload = read_json(CATEGORIES_PATH, {"market_profiles": []})
    profiles = [item for item in payload.get("market_profiles", []) if isinstance(item, dict) and clean(item.get("id"))]
    if not any(clean(item.get("id")) == DEFAULT_MARKET_TARGET for item in profiles):
        profiles.insert(
            0,
            {
                "id": DEFAULT_MARKET_TARGET,
                "label": "Balanced",
                "short_label": "Balanced",
                "description": "Use the base category searches.",
                "query_modifiers": [],
            },
        )
    return profiles


def category_lookup() -> dict[str, dict[str, Any]]:
    return {category["id"]: category for category in load_categories()}


def market_profile_lookup() -> dict[str, dict[str, Any]]:
    return {clean(profile.get("id")): profile for profile in load_market_profiles()}


def normalize_market_target(market_target: str) -> str:
    key = clean(market_target).lower().replace("-", "_")
    aliases = {
        "": DEFAULT_MARKET_TARGET,
        "usa": "us",
        "american": "us",
        "american_market": "us",
        "europe": "eu",
        "european": "eu",
        "european_market": "eu",
    }
    key = aliases.get(key, key)
    return key if key in market_profile_lookup() else DEFAULT_MARKET_TARGET


def market_profile(market_target: str) -> dict[str, Any]:
    profiles = market_profile_lookup()
    target = normalize_market_target(market_target)
    return profiles.get(target, profiles[DEFAULT_MARKET_TARGET])


def search_history_key(category_id: str, market_target: str = DEFAULT_MARKET_TARGET) -> str:
    target = normalize_market_target(market_target)
    return category_id if target == DEFAULT_MARKET_TARGET else f"{category_id}:{target}"


def load_search_history() -> dict[str, Any]:
    payload = read_json(SEARCH_HISTORY_PATH, {"version": 1, "updated_at": "", "categories": {}})
    payload.setdefault("version", 1)
    payload.setdefault("updated_at", "")
    payload.setdefault("categories", {})
    return payload


def save_search_history(payload: dict[str, Any]) -> None:
    payload["updated_at"] = now_iso()
    write_json(SEARCH_HISTORY_PATH, payload)


def advance_query_index(category_id: str, used_index: int, market_target: str = DEFAULT_MARKET_TARGET) -> None:
    queries = configured_queries(category_id, market_target)
    if not queries:
        return
    history = load_search_history()
    categories = history.setdefault("categories", {})
    state_key = search_history_key(category_id, market_target)
    state = categories.setdefault(state_key, {})
    if not isinstance(state, dict):
        state = {}
        categories[state_key] = state
    state["category_id"] = category_id
    state["market_target"] = normalize_market_target(market_target)
    state["next_query_index"] = (used_index + 1) % len(queries)
    state["last_opened_at"] = now_iso()
    save_search_history(history)


def load_decisions() -> dict[str, Any]:
    payload = read_json(DECISIONS_PATH, {"version": 1, "updated_at": "", "items": {}})
    payload.setdefault("version", 1)
    payload.setdefault("updated_at", "")
    payload.setdefault("items", {})
    return payload


def save_decisions(payload: dict[str, Any]) -> None:
    payload["updated_at"] = now_iso()
    write_json(DECISIONS_PATH, payload)


def persist_workflow_state(
    candidate: dict[str, Any],
    stage: str,
    message: str,
    *,
    detail_job_id: str = "",
) -> dict[str, Any]:
    key = clean(candidate.get("key"))
    if not key:
        raise ValueError("candidate is missing a key")
    with DECISION_LOCK:
        decisions = load_decisions()
        items = decisions.setdefault("items", {})
        existing = items.get(key, {})
        if not isinstance(existing, dict):
            existing = {}
        evidence = existing.get("evidence", {})
        if not isinstance(evidence, dict):
            evidence = {}
        workflow = existing.get("workflow", {})
        if not isinstance(workflow, dict):
            workflow = {}
        workflow.update(
            {
                "stage": stage,
                "message": clean(message),
                "updated_at": now_iso(),
            }
        )
        if detail_job_id:
            workflow["detail_job_id"] = detail_job_id
        workflow.setdefault("started_at", now_iso())
        existing.update(
            {
                "action": "keep",
                "product_url": clean(candidate.get("product_url")) or existing.get("product_url", ""),
                "title": clean(candidate.get("title")) or existing.get("title", ""),
                "category_id": clean(candidate.get("category_id")) or existing.get("category_id", ""),
                "run_id": clean(candidate.get("run_id")) or existing.get("run_id", ""),
                "verdict": clean(candidate.get("verdict")) or existing.get("verdict", ""),
                "score": candidate.get("score", existing.get("score", "")),
                "evidence": evidence,
                "workflow": workflow,
                "updated_at": now_iso(),
            }
        )
        items[key] = existing
        save_decisions(decisions)
    return existing


def confirmed_evidence_value(value: Any) -> bool:
    text = clean(value).lower()
    if not text:
        return False
    negative_values = {"0", "false", "no", "none", "unknown", "unavailable", "pending", "missing", "unconfirmed"}
    if text in negative_values:
        return False
    return not (
        text.startswith(("no ", "not ", "needs ", "cannot ", "can't "))
        or any(phrase in text for phrase in ("not confirmed", "not verified", "still unknown", "not available"))
    )


def listing_ready(evidence: dict[str, Any]) -> bool:
    required = ("dropship_confirmed", "dispatch_confirmed", "supplier_confirmed")
    has_images = bool(clean(evidence.get("generated_images_path")) or clean(evidence.get("vendor_images_path")))
    return (
        bool(clean(evidence.get("size_chart_source")))
        and has_images
        and all(confirmed_evidence_value(evidence.get(field)) for field in required)
    )


PROOF_FIELD_LABELS = {
    "detail_proof": "Verify the current supplier product page",
    "detail_rejection": "Resolve the rejected supplier detail result or choose another product",
    "size_chart_source": "Provide or verify the source size chart",
    "product_images": "Provide usable product images",
    "dropship_confirmed": "Confirm one-piece dropshipping",
    "dispatch_confirmed": "Confirm dispatch or ready-stock timing",
    "supplier_confirmed": "Confirm supplier identity and reliability",
}

EDITABLE_EVIDENCE_FIELDS = (
    "size_chart_source",
    "vendor_images_path",
    "generated_images_path",
    "dropship_confirmed",
    "dispatch_confirmed",
    "supplier_confirmed",
    "notes",
)


def merge_editable_evidence(existing: Any, incoming: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing) if isinstance(existing, dict) else {}
    for field in EDITABLE_EVIDENCE_FIELDS:
        if field in incoming:
            merged[field] = clean(incoming.get(field))
    return merged


def numeric_value(value: Any, default: float = 0.0) -> float:
    match = re.search(r"-?\d+(?:\.\d+)?", clean(value).replace(",", ""))
    return float(match.group(0)) if match else default


def preparation_missing(candidate: dict[str, Any]) -> list[dict[str, str]]:
    evidence = candidate.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}
    missing: list[str] = []
    if not has_detail_proof(candidate):
        missing.append("detail_proof")
    elif not detail_verdict_acceptable(candidate):
        missing.append("detail_rejection")
    if not clean(evidence.get("size_chart_source")):
        missing.append("size_chart_source")
    if not (clean(evidence.get("generated_images_path")) or clean(evidence.get("vendor_images_path"))):
        missing.append("product_images")
    for field in ("dropship_confirmed", "dispatch_confirmed", "supplier_confirmed"):
        if not confirmed_evidence_value(evidence.get(field)):
            missing.append(field)
    return [{"field": field, "label": PROOF_FIELD_LABELS[field]} for field in missing]


def parse_run_observed_at(payload: dict[str, Any], run_id: str, scored_path: Path) -> str:
    generated = clean(payload.get("generated_at") or payload.get("collected_at"))
    if generated:
        return generated
    match = re.search(r"(20\d{2})-(\d{2})-(\d{2})-(\d{2})(\d{2})(\d{2})", run_id)
    if match:
        year, month, day, hour, minute, second = match.groups()
        return f"{year}-{month}-{day}T{hour}:{minute}:{second}+00:00"
    return dt.datetime.fromtimestamp(scored_path.stat().st_mtime, tz=dt.timezone.utc).isoformat()


def freshness_label(observed_at: str) -> str:
    try:
        parsed = dt.datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return "Last check unavailable"
    today = dt.datetime.now(dt.timezone.utc).date()
    delta = (today - parsed.astimezone(dt.timezone.utc).date()).days
    if delta <= 0:
        return "Found today"
    if delta == 1:
        return "Checked yesterday"
    return f"Checked {delta} days ago"


def opportunity_confidence(candidate: dict[str, Any]) -> str:
    evidence = candidate.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}
    detail_verdict = clean(evidence.get("detail_verdict") or candidate.get("verdict"))
    if clean(candidate.get("decision")) == "reject" or (has_detail_proof(candidate) and detail_verdict == "Reject"):
        return "Low"
    proof_count = sum(
        (
            bool(clean(evidence.get("size_chart_source"))),
            bool(clean(evidence.get("vendor_images_path")) or clean(evidence.get("generated_images_path"))),
            confirmed_evidence_value(evidence.get("dropship_confirmed")),
            confirmed_evidence_value(evidence.get("dispatch_confirmed")),
            confirmed_evidence_value(evidence.get("supplier_confirmed")),
        )
    )
    if detail_verdict_acceptable(candidate) and proof_count >= 4:
        return "High"
    demand_signals = sum(
        bool(clean(candidate.get(field)))
        for field in ("monthly_sales", "repurchase_rate_pct", "moq", "image_url")
    )
    return "Medium" if demand_signals >= 3 and numeric_value(candidate.get("category_match")) >= 4 else "Low"


def is_review_recommended(candidate: dict[str, Any]) -> bool:
    if clean(candidate.get("decision")) == "reject":
        return False
    if clean(candidate.get("verdict")) in {"Gold", "Test"}:
        return True
    if clean(candidate.get("review_stage")) != "search":
        return False
    if numeric_value(candidate.get("score")) < 50 or numeric_value(candidate.get("category_match")) < 4:
        return False
    if clean(candidate.get("ip_risk_flags")):
        return False
    moq_text = clean(candidate.get("moq"))
    moq_match = re.search(r"\d+(?:\.\d+)?", moq_text)
    if moq_match and float(moq_match.group(0)) > 3:
        return False
    blocking_phrases = (
        "poor fit for Dress Like Mommy",
        "weak visible match for selected store category",
        "stale listing year signal",
        "older 1688 offer ID",
        "MOQ too high",
        "not one-piece/dropship friendly",
        "possible IP/brand risk",
        "missing product URL",
    )
    concerns = " | ".join(candidate.get("concerns", [])) if isinstance(candidate.get("concerns"), list) else clean(candidate.get("concerns"))
    return not any(phrase.lower() in concerns.lower() for phrase in blocking_phrases)


def workflow_snapshot(candidate: dict[str, Any]) -> dict[str, Any]:
    decision = candidate.get("decision_record", {})
    if not isinstance(decision, dict):
        decision = {}
    saved = decision.get("workflow", {})
    if not isinstance(saved, dict):
        saved = {}
    missing = preparation_missing(candidate)
    package_path = package_dir_for_key(clean(candidate.get("key")))
    package_exists = (package_path / "candidate.json").exists()
    stage = clean(saved.get("stage"))
    job_id = clean(saved.get("detail_job_id"))
    active_job = detail_job_snapshot(job_id) if job_id else {}
    if active_job.get("status") in {"queued", "running"}:
        stage = "verifying"
    elif clean(candidate.get("decision")) == "reject":
        stage = "passed"
    elif clean(candidate.get("decision")) == "keep":
        if not missing:
            stage = "prep_ready"
        elif stage not in {"needs_attention", "needs_input", "liked"}:
            stage = "needs_input" if has_detail_proof(candidate) else "liked"
    else:
        stage = "new"
    labels = {
        "new": "Ready to review",
        "liked": "Liked — verification not started",
        "verifying": "Verifying supplier source",
        "needs_attention": "Liked — helper browser needs attention",
        "needs_input": "Liked — a few details are still needed",
        "prep_ready": "Preparation ready",
        "passed": "Passed",
    }
    return {
        "stage": stage,
        "label": labels.get(stage, stage.replace("_", " ").title()),
        "message": clean(saved.get("message")),
        "detail_job_id": job_id,
        "missing": missing,
        "package_exists": package_exists,
        "package_path": str(package_path.relative_to(REPO_ROOT)),
        "updated_at": clean(saved.get("updated_at") or candidate.get("decision_updated_at")),
    }


def has_detail_proof(candidate: dict[str, Any]) -> bool:
    evidence = candidate.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}
    return any(
        clean(value)
        for value in [
            candidate.get("detail_evidence_path"),
            evidence.get("detail_evidence_path"),
            evidence.get("detail_verdict"),
        ]
    ) or clean(candidate.get("review_stage")) == "detail"


def detail_verdict_acceptable(candidate: dict[str, Any]) -> bool:
    evidence = candidate.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}
    verdict = clean(evidence.get("detail_verdict") or candidate.get("verdict"))
    return has_detail_proof(candidate) and verdict in {"Gold", "Test"}


def draft_handoff_ready(candidate: dict[str, Any]) -> bool:
    evidence = candidate.get("evidence", {})
    return (
        isinstance(evidence, dict)
        and clean(candidate.get("decision")) != "reject"
        and detail_verdict_acceptable(candidate)
        and listing_ready(evidence)
    )


def apply_detail_gate(candidate: dict[str, Any]) -> None:
    raw_verdict = clean(candidate.get("verdict"))
    evidence = candidate.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}
    detail_verdict = clean(evidence.get("detail_verdict"))
    detail_verified = has_detail_proof(candidate)
    candidate["raw_verdict"] = raw_verdict
    candidate["detail_proof_verified"] = detail_verified
    if detail_verdict:
        candidate["verdict"] = detail_verdict
    if clean(candidate.get("verdict")) == "Gold" and not detail_verified:
        candidate["verdict"] = "Test"
        candidate["detail_gate_note"] = "Needs detail-page proof before this can become a Best Lead."
        gate_concern = "Detail-page proof required before Best Lead"
        concerns = candidate.get("concerns")
        if isinstance(concerns, list):
            if gate_concern not in concerns:
                candidate["concerns"] = concerns + [gate_concern]
        else:
            concerns_text = clean(concerns)
            candidate["concerns"] = f"{concerns_text} | {gate_concern}" if concerns_text else gate_concern


def explicit_yes(value: Any) -> bool:
    """Return true only for positive evidence, with explicit negatives winning."""
    text = clean(value).lower()
    if not text:
        return False
    negative = (
        "not supported",
        "unsupported",
        "not available",
        "unavailable",
        "sold out",
        "out of stock",
        "不支持",
        "不可",
        "无货",
        "缺货",
        "下架",
    )
    if any(term in text for term in negative):
        return False
    return any(
        term in text
        for term in (
            "yes",
            "confirmed",
            "supported",
            "available",
            "in stock",
            "ready stock",
            "dropship",
            "one piece",
            "一件代发",
            "代发",
            "现货",
            "有货",
        )
    )


def supplier_years_value(candidate: dict[str, Any]) -> int | None:
    text = clean(candidate.get("years_on_1688"))
    match = re.search(r"\d+", text)
    return int(match.group(0)) if match else None


def supplier_years_provenance_verified(candidate: dict[str, Any]) -> bool:
    return clean(candidate.get("years_on_1688_scope")) == "supplier_context_phrase"


def valid_supplier_rating(candidate: dict[str, Any]) -> float | None:
    text = clean(candidate.get("rating"))
    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        return None
    rating = float(match.group(0))
    return rating if 0 <= rating <= 5 else None


def current_year_product_claim(candidate: dict[str, Any]) -> bool:
    """A product-scoped freshness claim, not proof of the original listing date."""
    year = str(dt.datetime.now(dt.timezone.utc).year)
    product_text = " ".join(
        clean(candidate.get(field))
        for field in ("title", "display_title")
    )
    return year in product_text


def observed_age_days(candidate: dict[str, Any]) -> int | None:
    text = clean(candidate.get("observed_at"))
    if not text:
        return None
    try:
        observed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        if observed.tzinfo is None:
            observed = observed.replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None
    return max(0, (dt.datetime.now(dt.timezone.utc) - observed.astimezone(dt.timezone.utc)).days)


def title_phrase_present(text: str, phrase: str) -> bool:
    """Match Chinese substrings and complete English phrases, never word fragments."""
    phrase = clean(phrase).lower()
    if not phrase:
        return False
    if any(ord(character) > 127 for character in phrase):
        return phrase in text
    return bool(re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", text))


def title_has_any_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    return any(title_phrase_present(text, phrase) for phrase in phrases)


def exact_relationship_fit(candidate: dict[str, Any]) -> bool:
    """Require product-title role composition instead of trusting generic 亲子/category scores."""
    text = " ".join(clean(candidate.get(field)).lower() for field in ("title", "display_title"))
    category_id = clean(candidate.get("category_id"))
    obvious_wrong_products = (
        "lingerie", "intimates", "underwear", "bralette", "panties", "thong", "sexy uniform",
        "doll clothes", "doll clothing", "doll outfit", "dress accessories", "hair accessory",
        "headband", "stiletto", "pumps", "fabric for dresses", "内衣", "文胸", "胸罩", "内裤",
        "丁字裤", "情趣", "娃衣", "玩偶服",
    )
    if title_has_any_phrase(text, obvious_wrong_products):
        return False
    patterns = {
        "mommy-and-me": (
            "mother-daughter", "mother and daughter", "mother daughter", "mommy and me", "mommy & me", "mother-son", "mother and son", "母女", "母子",
        ),
        "daddy-and-me": (
            "father-son", "father and son", "father son", "father-daughter", "father and daughter", "dad and", "daddy and me", "daddy & me", "父子", "父女",
        ),
        "siblings-matching": (
            "siblings", "sibling", "brother-sister", "brother and sister", "sister-brother", "sisters", "brothers", "twins", "兄妹", "姐弟", "姐妹", "兄弟", "双胞胎",
        ),
        "couples": (
            "couple", "couples", "his and hers", "boyfriend", "girlfriend", "husband", "wife", "情侣", "男女同款",
        ),
    }
    if category_id in patterns:
        return title_has_any_phrase(text, patterns[category_id])
    if category_id == "family-matching":
        return title_has_any_phrase(
            text,
            (
                "family of three", "family of four", "family matching", "matching family", "whole family",
                "mom, dad", "mother-daughter", "father-son", "全家", "一家三口", "一家四口", "家庭装",
                "家庭亲子", "亲子装",
            ),
        )
    if category_id == "maternity":
        maternity = title_has_any_phrase(
            text,
            ("maternity", "pregnant", "pregnancy", "mom-to-be", "baby bump", "孕妇", "孕妈", "孕肚"),
        )
        matching = title_has_any_phrase(
            text,
            (
                "mother-daughter", "mother daughter", "mother and daughter", "mommy and me", "mommy & me",
                "mom and me", "mom & me", "family matching", "matching family", "family outfit", "family outfits",
                "family of three", "family of four", "母女", "全家", "一家三口", "一家四口", "家庭装",
                "家庭亲子", "亲子装",
            ),
        )
        return maternity and matching
    return False


def opportunity_assessment(candidate: dict[str, Any]) -> dict[str, Any]:
    """Build an honest UI tier from confirmed evidence; missing proof earns nothing."""
    evidence = candidate.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}
    detail = has_detail_proof(candidate)
    years = supplier_years_value(candidate)
    tenure_provenance = supplier_years_provenance_verified(candidate)
    rating = valid_supplier_rating(candidate)
    dropship = explicit_yes(candidate.get("dropship_supported")) or explicit_yes(evidence.get("dropship_confirmed"))
    availability_text = " ".join(clean(candidate.get(field)).lower() for field in ("availability", "service_flags"))
    availability = not any(term in availability_text for term in ("sold out", "out of stock", "unavailable", "无货", "缺货", "下架")) and any(
        term in availability_text for term in ("available", "in stock", "ready stock", "现货", "有货", "可售", "库存")
    )
    dispatch_text = " ".join((clean(evidence.get("dispatch_confirmed")), clean(candidate.get("service_flags")))).lower()
    dispatch = confirmed_evidence_value(evidence.get("dispatch_confirmed")) or any(
        term in dispatch_text for term in ("dispatch", "ships in", "ship within", "48 hour", "72 hour", "发货", "小时")
    )
    supplier_identity = bool(clean(candidate.get("vendor_name"))) and rating is not None
    size_chart = bool(clean(candidate.get("size_chart")) or clean(evidence.get("size_chart_source")))
    images = bool(
        clean(candidate.get("vendor_image_urls"))
        or clean(candidate.get("vendor_images_path"))
        or clean(evidence.get("vendor_images_path"))
        or clean(evidence.get("generated_images_path"))
    )
    year_claim = current_year_product_claim(candidate)
    relationship_fit = exact_relationship_fit(candidate)
    age_days = observed_age_days(candidate)
    recently_found = age_days is not None and age_days <= 14
    availability_fresh = age_days is not None and age_days <= 7
    confirmed = {
        "detail": detail,
        "relationship_fit": relationship_fit,
        "recently_checked": availability_fresh if detail else recently_found,
        "supplier_age": detail and tenure_provenance and years is not None and years >= MINIMUM_SUPPLIER_YEARS,
        "supplier_identity": supplier_identity,
        "current_year_claim": year_claim and detail,
        "availability": availability,
        "dropship": dropship,
        "dispatch": dispatch,
        "size_chart": size_chart,
        "images": images,
    }
    evidence_confidence = round(100 * sum(1 for value in confirmed.values() if value) / len(confirmed))
    failures: list[str] = []
    if clean(candidate.get("decision")) == "reject":
        failures.append("You passed this product")
    if not relationship_fit:
        failures.append("The product title does not prove the matching relationship required for this lane")
    if not year_claim:
        failures.append(f"The product itself does not show a {dt.datetime.now(dt.timezone.utc).year} current-year claim")
    if detail and not availability_fresh:
        failures.append("Supplier availability proof is older than 7 days and must be refreshed")
    if detail and not detail_verdict_acceptable(candidate):
        failures.append("Supplier detail check rejected this product")
    if detail and (years is None or not tenure_provenance):
        failures.append(
            f"Supplier history could not be verified from supplier-context evidence "
            f"(minimum {MINIMUM_SUPPLIER_YEARS} years)"
        )
    if tenure_provenance and years is not None and years < MINIMUM_SUPPLIER_YEARS:
        failures.append(f"Supplier has only {years} verified year{'s' if years != 1 else ''}; minimum is {MINIMUM_SUPPLIER_YEARS}")
    if detail and rating is None:
        failures.append("Supplier rating is missing or invalid")
    if detail and not dropship:
        failures.append("One-piece dropshipping was not confirmed")
    if detail and not availability:
        failures.append("Current availability was not confirmed")

    verified = detail and not failures and all(confirmed.values())
    if verified:
        tier = "verified"
        label = "VERIFIED OPPORTUNITY"
        reason = f"Supplier has {years}+ verified years and every required sourcing check passed."
    elif failures and detail:
        tier = "rejected"
        label = "REJECTED BY SCOUT"
        reason = failures[0]
    elif is_review_recommended(candidate) and relationship_fit and year_claim and recently_found:
        tier = "promising"
        label = "PROMISING — SUPPLIER CHECK PENDING"
        reason = "The current-year product claim and exact matching roles look useful, but supplier age, stock, dropshipping, and listing proof still need detail verification."
    else:
        tier = "rejected"
        label = "FILTERED BY SCOUT"
        reason = "This product did not meet the current store-fit and sourcing-readiness gates."
    return {
        "tier": tier,
        "label": label,
        "reason": reason,
        "failures": failures,
        "evidence_confidence": evidence_confidence,
        "confirmed": confirmed,
        "supplier_years": years,
        "supplier_years_label": (
            f"{years} year{'s' if years != 1 else ''} verified"
            if detail and tenure_provenance and years is not None
            else "Not verified"
        ),
        "supplier_years_provenance": clean(candidate.get("years_on_1688_label")) if tenure_provenance else "",
        "minimum_supplier_years": MINIMUM_SUPPLIER_YEARS,
        "observed_age_days": age_days,
        "rating": rating,
        "listing_year_label": (
            f"{dt.datetime.now(dt.timezone.utc).year} product claim seen on detail page"
            if year_claim and detail
            else (
                f"{dt.datetime.now(dt.timezone.utc).year} search-card claim only"
                if year_claim
                else "Listing year not verified"
            )
        ),
    }


def package_dir_for_key(key: str) -> Path:
    return DRAFT_PACKAGES_ROOT / clean(key)


def cache_image(url: str) -> tuple[Path, str]:
    text = clean(url)
    if not text.startswith(("https://", "http://")):
        raise ValueError("unsupported image URL")
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
    suffix = Path(urlparse(text).path).suffix or ".img"
    path = IMAGE_CACHE_ROOT / f"{digest}{suffix}"
    meta_path = IMAGE_CACHE_ROOT / f"{digest}.json"
    if path.exists():
        content_type = "image/webp" if suffix == ".webp" else mimetypes.guess_type(path.name)[0] or "image/jpeg"
        return path, content_type

    request = urllib.request.Request(
        text,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36",
            "Referer": "https://detail.1688.com/",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        content_type = response.headers.get("Content-Type") or mimetypes.guess_type(path.name)[0] or "image/jpeg"
        data = response.read()
    IMAGE_CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    write_json(meta_path, {"url": text, "content_type": content_type, "cached_at": now_iso()})
    return path, content_type


def gbk_quote(query: str) -> str:
    return quote_from_bytes(query.encode("gbk", errors="ignore"))


def clean_query_terms(parts: list[Any]) -> str:
    seen: set[str] = set()
    terms: list[str] = []
    for part in parts:
        if isinstance(part, list):
            values = part
        elif isinstance(part, tuple):
            values = list(part)
        else:
            values = [part]
        for value in values:
            text = clean(value)
            if not text:
                continue
            for term in text.split():
                if term and term not in seen:
                    seen.add(term)
                    terms.append(term)
    return " ".join(terms)


def configured_query_text(
    item: Any,
    defaults: dict[str, Any] | None = None,
    market: dict[str, Any] | None = None,
) -> str:
    """Return a concise 1688 product query, not a stack of proof requirements.

    Freshness, fulfillment, supplier quality, and destination-market fit are
    evidence gates after discovery. Putting all of them in the search box made
    1688 broaden otherwise useful relationship/apparel searches.
    """
    defaults = defaults if isinstance(defaults, dict) else {}
    if isinstance(item, dict):
        return clean_query_terms(
            [
                item.get("text"),
                item.get("launch_season") or item.get("season") or defaults.get("launch_season"),
            ]
        )
    return clean(item)


def configured_queries(category_id: str, market_target: str = DEFAULT_MARKET_TARGET) -> list[str]:
    categories = category_lookup()
    category = categories.get(category_id) or categories.get("family-matching") or {}
    raw_queries = category.get("queries") or ["亲子装 连衣裙 衬衫 一件代发"]
    defaults = category.get("search_defaults", {})
    market = market_profile(market_target)
    queries: list[str] = []
    for item in raw_queries:
        query = configured_query_text(item, defaults, market)
        if query:
            queries.append(query)
    return queries or ["亲子装 连衣裙 衬衫 一件代发"]


def search_term_catalog() -> dict[str, list[dict[str, Any]]]:
    """Expose stable English labels while retaining the exact Chinese source terms."""
    catalog: dict[str, list[dict[str, Any]]] = {}
    for category in load_categories():
        category_id = clean(category.get("id"))
        defaults = category.get("search_defaults", {})
        terms: list[dict[str, Any]] = []
        for index, item in enumerate(category.get("queries", [])):
            if isinstance(item, dict):
                english = clean(item.get("intent")) or clean(item.get("text"))
                chinese = configured_query_text(item, defaults, {})
                base_chinese = clean(item.get("text"))
                season = clean(item.get("launch_season") or item.get("season"))
            else:
                english = clean(item)
                chinese = configured_query_text(item, defaults, {})
                base_chinese = clean(item)
                season = ""
            terms.append(
                {
                    "id": index,
                    "english": english,
                    "chinese": chinese,
                    "base_chinese": base_chinese,
                    "season": season,
                }
            )
        catalog[category_id] = terms
    return catalog


def load_seasonal_rules() -> dict[str, Any]:
    rules = read_json(SEASONAL_RULES_PATH, {})
    if not isinstance(rules, dict):
        raise ValueError("seasonal sourcing configuration must be an object")
    return rules


def plan_date(value: Any = None) -> dt.date:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    text = clean(value)
    if text:
        try:
            return dt.date.fromisoformat(text[:10])
        except ValueError as exc:
            raise ValueError("plan_as_of must be an ISO date") from exc
    return dt.date.today()


def option_lookup(items: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        return {}
    return {
        clean(item.get("id")): item
        for item in items
        if isinstance(item, dict) and clean(item.get("id"))
    }


def seasonal_recommendation(as_of: Any = None) -> dict[str, Any]:
    """Return the configurable northern-market recommendation for a calendar date."""
    date = plan_date(as_of)
    rules = load_seasonal_rules()
    seasons = option_lookup(rules.get("seasons"))
    phases = rules.get("phases", {}) if isinstance(rules.get("phases"), dict) else {}
    raw_entries = rules.get("calendar", {}).get(str(date.month), [])
    entries: list[dict[str, Any]] = []
    for raw in raw_entries if isinstance(raw_entries, list) else []:
        if not isinstance(raw, dict):
            continue
        season_id = clean(raw.get("season_id"))
        season = seasons.get(season_id)
        if not season:
            continue
        phase = clean(raw.get("phase")) or "source_ahead"
        entries.append(
            {
                "season_id": season_id,
                "label": clean(season.get("label")) or season_id.title(),
                "year": date.year,
                "phase": phase,
                "phase_label": clean(phases.get(phase)) or phase.replace("_", " ").title(),
                "chinese": clean(season.get("chinese")),
            }
        )
    if not entries:
        fallback = seasons.get("evergreen") or next(iter(seasons.values()), {"id": "evergreen", "label": "Evergreen", "chinese": "四季款"})
        entries.append(
            {
                "season_id": clean(fallback.get("id")) or "evergreen",
                "label": clean(fallback.get("label")) or "Evergreen",
                "year": date.year,
                "phase": "sell_now",
                "phase_label": clean(phases.get("sell_now")) or "Sell now",
                "chinese": clean(fallback.get("chinese")),
            }
        )
    selected = [entry["season_id"] for entry in entries]
    excluded = [
        {"season_id": season_id, "label": clean(season.get("label")) or season_id.title()}
        for season_id, season in seasons.items()
        if season_id not in selected and season_id != "evergreen"
    ]
    display_date = f"{date.strftime('%B')} {date.day}, {date.year}"
    return {
        "as_of_date": date.isoformat(),
        "display_date": display_date,
        "entries": entries,
        "season_ids": selected,
        "excluded": excluded,
        "reason": "Based on today's date, the selected US/Europe markets, and the configurable sourcing lead-time calendar.",
    }


def normalized_option_ids(values: Any, allowed: dict[str, Any]) -> list[str]:
    if not isinstance(values, list):
        return []
    result: list[str] = []
    for value in values:
        option_id = clean(value)
        if option_id in allowed and option_id not in result:
            result.append(option_id)
    return result


def default_sourcing_brief(as_of: Any = None) -> dict[str, Any]:
    rules = load_seasonal_rules()
    defaults = rules.get("defaults", {}) if isinstance(rules.get("defaults"), dict) else {}
    recommendation = seasonal_recommendation(as_of)
    return {
        "season_mode": "recommended",
        "season_ids": recommendation["season_ids"],
        "product_type_ids": list(defaults.get("product_type_ids", ["dresses", "sets"])),
        "occasion_ids": list(defaults.get("occasion_ids", ["casual", "formal"])),
        "excluded_query_ids": [],
        "max_queries_per_lane": max(1, min(int(defaults.get("max_queries_per_lane", 6)), 8)),
    }


def normalize_sourcing_brief(
    payload: Any,
    fallback: Any = None,
    *,
    as_of: Any = None,
) -> dict[str, Any]:
    rules = load_seasonal_rules()
    products = option_lookup(rules.get("product_types"))
    occasions = option_lookup(rules.get("occasions"))
    seasons = option_lookup(rules.get("seasons"))
    defaults = default_sourcing_brief(as_of)
    source = payload if isinstance(payload, dict) else (fallback if isinstance(fallback, dict) else {})
    fallback_source = fallback if isinstance(fallback, dict) else {}
    mode = clean(source.get("season_mode") or fallback_source.get("season_mode") or "recommended").lower()
    mode = "manual" if mode == "manual" else "recommended"
    product_ids = normalized_option_ids(source.get("product_type_ids"), products)
    if not product_ids:
        product_ids = normalized_option_ids(fallback_source.get("product_type_ids"), products)
    if not product_ids:
        product_ids = normalized_option_ids(defaults["product_type_ids"], products)
    occasion_ids = normalized_option_ids(source.get("occasion_ids"), occasions)
    if not occasion_ids:
        occasion_ids = normalized_option_ids(fallback_source.get("occasion_ids"), occasions)
    if not occasion_ids:
        occasion_ids = normalized_option_ids(defaults["occasion_ids"], occasions)
    if mode == "recommended":
        season_ids = seasonal_recommendation(as_of)["season_ids"]
    else:
        season_ids = normalized_option_ids(source.get("season_ids"), seasons)
        if not season_ids:
            season_ids = normalized_option_ids(fallback_source.get("season_ids"), seasons)
        if not season_ids:
            season_ids = seasonal_recommendation(as_of)["season_ids"]
    excluded = source.get("excluded_query_ids", fallback_source.get("excluded_query_ids", []))
    excluded_query_ids = sorted({clean(value) for value in excluded if clean(value)}) if isinstance(excluded, list) else []
    raw_max = source.get("max_queries_per_lane", fallback_source.get("max_queries_per_lane", defaults["max_queries_per_lane"]))
    return {
        "season_mode": mode,
        "season_ids": season_ids,
        "product_type_ids": product_ids,
        "occasion_ids": occasion_ids,
        "excluded_query_ids": excluded_query_ids,
        "max_queries_per_lane": max(1, min(int(raw_max), 8)),
    }


def selected_season_entries(brief: dict[str, Any], as_of: Any = None) -> list[dict[str, Any]]:
    date = plan_date(as_of)
    rules = load_seasonal_rules()
    seasons = option_lookup(rules.get("seasons"))
    phases = rules.get("phases", {}) if isinstance(rules.get("phases"), dict) else {}
    recommended = {entry["season_id"]: entry for entry in seasonal_recommendation(date)["entries"]}
    result: list[dict[str, Any]] = []
    for season_id in brief.get("season_ids", []):
        season = seasons.get(season_id)
        if not season:
            continue
        known = recommended.get(season_id, {})
        phase = clean(known.get("phase")) or "owner_selected"
        result.append(
            {
                "season_id": season_id,
                "label": clean(season.get("label")) or season_id.title(),
                "year": date.year,
                "phase": phase,
                "phase_label": clean(known.get("phase_label")) or clean(phases.get(phase)) or "Owner selected",
                "chinese": clean(season.get("chinese")),
            }
        )
    return result


def build_sourcing_plan(config: dict[str, Any], as_of: Any = None) -> dict[str, Any]:
    """Compile a stable, visible query batch. No cursor or random state participates."""
    date = plan_date(as_of)
    rules = load_seasonal_rules()
    categories = category_lookup()
    markets = market_profile_lookup()
    products = option_lookup(rules.get("product_types"))
    occasions = option_lookup(rules.get("occasions"))
    brief = normalize_sourcing_brief(config.get("sourcing_brief"), as_of=date)
    season_entries = selected_season_entries(brief, date)
    product_entries = [products[item] for item in brief["product_type_ids"] if item in products]
    occasion_entries = [occasions[item] for item in brief["occasion_ids"] if item in occasions]
    category_terms = rules.get("category_terms", {}) if isinstance(rules.get("category_terms"), dict) else {}
    category_product_overrides = rules.get("category_product_overrides", {}) if isinstance(rules.get("category_product_overrides"), dict) else {}
    query_strategy = rules.get("query_strategy", {}) if isinstance(rules.get("query_strategy"), dict) else {}
    review_gate = rules.get("review_gate", {}) if isinstance(rules.get("review_gate"), dict) else {}
    deferred_category_ids = {
        clean(value)
        for value in review_gate.get("deferred_category_ids", [])
        if clean(value)
    }
    fixed_query_overrides: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for raw_override in rules.get("fixed_query_overrides", []):
        if not isinstance(raw_override, dict):
            continue
        override_key = (
            clean(raw_override.get("category_id")),
            clean(raw_override.get("season_id")),
            clean(raw_override.get("product_type_id")),
            clean(raw_override.get("occasion_id")),
        )
        if all(override_key):
            fixed_query_overrides[override_key] = raw_override
    term_translations = rules.get("chinese_term_translations", {}) if isinstance(rules.get("chinese_term_translations"), dict) else {}
    max_query_terms = max(2, int(query_strategy.get("max_terms") or 4))
    max_query_characters = max(6, int(query_strategy.get("max_chinese_characters") or 18))
    post_search_checks = [clean(value) for value in query_strategy.get("post_search_checks", []) if clean(value)]
    excluded = set(brief.get("excluded_query_ids", []))
    query_records: list[dict[str, Any]] = []
    lanes: dict[str, list[dict[str, Any]]] = {}
    selected_market_targets = [target for target in config.get("market_targets", []) if target in markets]
    selected_market_labels = [
        clean(markets[target].get("short_label")) or clean(markets[target].get("label")) or target
        for target in selected_market_targets
    ]
    market_scope_label = " + ".join(selected_market_labels) or "Balanced"
    for category_id in config.get("category_ids", []):
        category = categories.get(category_id, {})
        bases = [clean(value) for value in category_terms.get(category_id, []) if clean(value)]
        if not bases:
            bases = [clean(category.get("label")) or category_id]
        lane_id = f"{category_id}:shared"
        count = min(
            int(brief["max_queries_per_lane"]),
            max(len(season_entries), len(product_entries), len(occasion_entries), len(bases)),
        )
        lane_queries: list[dict[str, Any]] = []
        for index in range(count):
            season = season_entries[index % len(season_entries)]
            product = product_entries[index % len(product_entries)]
            occasion = occasion_entries[index % len(occasion_entries)]
            if season["season_id"] == "holiday":
                preferred = "holiday" if "holiday" in brief["occasion_ids"] else "formal"
                if preferred in occasions and preferred in brief["occasion_ids"]:
                    occasion = occasions[preferred]
            raw_override = category_product_overrides.get(category_id, {}).get(clean(product.get("id")), {})
            product_override = raw_override if isinstance(raw_override, dict) else {}
            base = clean(product_override.get("base")) or bases[index % len(bases)]
            product_terms = product_override.get("occasion_terms", {})
            if not isinstance(product_terms, dict):
                product_terms = {}
            default_product_terms = product.get("occasion_terms", {})
            if not isinstance(default_product_terms, dict):
                default_product_terms = {}
            product_chinese = (
                clean(product_terms.get(clean(occasion.get("id"))))
                or clean(default_product_terms.get(clean(occasion.get("id"))))
                or clean(product_override.get("chinese"))
                or clean(product.get("chinese"))
            )
            fixed_override = fixed_query_overrides.get(
                (
                    category_id,
                    season["season_id"],
                    clean(product.get("id")),
                    clean(occasion.get("id")),
                ),
                {},
            )
            product_label = (
                clean(fixed_override.get("merchandise_label"))
                or clean(product_override.get("label"))
                or clean(product.get("label"))
            )
            occasion_chinese = "" if clean(occasion.get("id")) in {"casual", "formal"} else clean(occasion.get("chinese"))
            chinese = clean(fixed_override.get("chinese")) or clean_query_terms(
                [base, product_chinese, season.get("chinese"), occasion_chinese]
            )
            query_term_count = len(chinese.split())
            query_character_count = len(chinese.replace(" ", ""))
            if query_term_count > max_query_terms or query_character_count > max_query_characters:
                raise ValueError(
                    f"1688 query is too long ({query_term_count} terms, {query_character_count} Chinese characters): {chinese}"
                )
            missing_translations = [term for term in chinese.split() if not clean(term_translations.get(term))]
            if missing_translations:
                raise ValueError(f"1688 query is missing an English translation for: {', '.join(missing_translations)}")
            english = " · ".join(clean(term_translations[term]) for term in chinese.split())
            is_deferred = category_id in deferred_category_ids
            search_role = "deferred" if is_deferred else clean(fixed_override.get("search_role")) or "custom"
            signature = "|".join(
                [
                    category_id,
                    ",".join(selected_market_targets),
                    season["season_id"],
                    clean(product.get("id")),
                    clean(occasion.get("id")),
                    base,
                    chinese,
                    search_role,
                ]
            )
            query_id = hashlib.sha1(signature.encode("utf-8")).hexdigest()[:12]
            record = {
                "id": query_id,
                "lane_id": lane_id,
                "category_id": category_id,
                "category_label": clean(category.get("label")) or category_id,
                "market_target": DEFAULT_MARKET_TARGET,
                "market_targets": list(selected_market_targets),
                "market_label": market_scope_label,
                "season_id": season["season_id"],
                "season_label": f"{season['label']} {date.year}",
                "phase": season["phase"],
                "phase_label": season["phase_label"],
                "product_type_id": clean(product.get("id")),
                "product_type_label": product_label,
                "occasion_id": clean(occasion.get("id")),
                "occasion_label": clean(occasion.get("label")),
                "english": english,
                "selection_label": (
                    f"{clean(category.get('label')) or category_id} · {product_label} · "
                    f"{clean(occasion.get('label'))} · {season['label']} {date.year}"
                ),
                "chinese": chinese,
                "query_term_count": query_term_count,
                "query_character_count": query_character_count,
                "search_role": search_role,
                "previous_chinese": clean(fixed_override.get("previous_chinese")),
                "first_batch_match": clean(fixed_override.get("first_batch_match")),
                "evidence_note": (
                    clean(review_gate.get("deferred_reason"))
                    if is_deferred
                    else clean(fixed_override.get("evidence_note"))
                ),
                "deferred": is_deferred,
                "included": not is_deferred and query_id not in excluded,
            }
            query_records.append(record)
            if record["included"]:
                lane_queries.append(record)
        if lane_queries:
            lanes[lane_id] = lane_queries
    included_queries = [record for record in query_records if record["included"]]
    if not included_queries:
        raise ValueError("Choose at least one exact search before saving or running the plan")
    active_category_ids = list(dict.fromkeys(row["category_id"] for row in included_queries))
    deferred_selected_ids = [
        category_id
        for category_id in config.get("category_ids", [])
        if category_id in deferred_category_ids and category_id in categories
    ]
    category_labels = [clean(categories[item].get("label")) for item in active_category_ids]
    active_product_labels = list(dict.fromkeys(clean(row.get("product_type_label")) for row in included_queries if clean(row.get("product_type_label"))))
    summary = {
        "matching_groups": category_labels,
        "deferred_matching_groups": [clean(categories[item].get("label")) for item in deferred_selected_ids],
        "product_types": active_product_labels,
        "occasions": [clean(item.get("label")) for item in occasion_entries],
        "seasons": [f"{item['label']} {date.year}" for item in season_entries],
        "markets": selected_market_labels,
        "lane_count": len(lanes),
        "query_count": len(included_queries),
        "replacement_count": sum(row.get("search_role") == "replacement" and row.get("included") for row in query_records),
        "control_count": sum(row.get("search_role") == "control" and row.get("included") for row in query_records),
        "deferred_count": sum(row.get("search_role") == "deferred" for row in query_records),
    }
    hash_payload = {
        "as_of_date": date.isoformat(),
        "brief": brief,
        "market_targets": selected_market_targets,
        "queries": [{"id": row["id"], "chinese": row["chinese"], "included": row["included"]} for row in query_records],
    }
    plan_hash = hashlib.sha256(json.dumps(hash_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    review_required = bool(review_gate.get("required"))
    reviewed_plan_hash = clean(config.get("reviewed_plan_hash"))
    execution_allowed = not review_required or reviewed_plan_hash == plan_hash
    return {
        "version": 1,
        "as_of_date": date.isoformat(),
        "display_date": f"{date.strftime('%B')} {date.day}, {date.year}",
        "brief": brief,
        "recommendation": seasonal_recommendation(date),
        "summary": summary,
        "queries": query_records,
        "lanes": lanes,
        "plan_hash": plan_hash,
        "frozen_message": "These short, relationship-first searches stay fixed. No random rotation or market duplicates.",
        "execution_allowed": execution_allowed,
        "review": {
            "required": review_required,
            "status": "approved" if execution_allowed else "owner_review_required",
            "plan_label": clean(review_gate.get("plan_label")) or "Exact search review",
            "paused_reason": clean(review_gate.get("paused_reason")) or "review every exact search before running",
            "reviewed_plan_hash": reviewed_plan_hash,
            "deferred_category_ids": sorted(deferred_category_ids),
            "deferred_reason": clean(review_gate.get("deferred_reason")),
        },
        "query_policy": (
            f"1688 receives only the relationship, garment, season, and at most one occasion term "
            f"({max_query_terms} terms / {max_query_characters} Chinese characters maximum). "
            "Freshness, stock, dropshipping, supplier age/quality, and market fit are checked after search."
        ),
        "query_strategy": {
            "max_terms": max_query_terms,
            "max_chinese_characters": max_query_characters,
            "relationship_first": True,
            "post_search_checks": post_search_checks,
            "search_once_for_selected_markets": True,
        },
    }


def sourcing_guide(as_of: Any = None) -> dict[str, Any]:
    date = plan_date(as_of)
    rules = load_seasonal_rules()
    review_gate = rules.get("review_gate", {}) if isinstance(rules.get("review_gate"), dict) else {}
    return {
        "as_of_date": date.isoformat(),
        "display_date": f"{date.strftime('%B')} {date.day}, {date.year}",
        "recommendation": seasonal_recommendation(date),
        "seasons": list(option_lookup(rules.get("seasons")).values()),
        "product_types": list(option_lookup(rules.get("product_types")).values()),
        "occasions": list(option_lookup(rules.get("occasions")).values()),
        "defaults": default_sourcing_brief(date),
        "deferred_category_ids": [clean(value) for value in review_gate.get("deferred_category_ids", []) if clean(value)],
        "deferred_reason": clean(review_gate.get("deferred_reason")),
    }


def next_query_index(category_id: str, market_target: str = DEFAULT_MARKET_TARGET) -> int:
    queries = configured_queries(category_id, market_target)
    history = load_search_history()
    state = history.get("categories", {}).get(search_history_key(category_id, market_target), {})
    if not isinstance(state, dict):
        return 0
    return int(state.get("next_query_index") or 0) % len(queries)


def category_search_url(
    category_id: str,
    query_index: int = 0,
    market_target: str = DEFAULT_MARKET_TARGET,
    exact_query: str = "",
) -> str:
    query = clean(exact_query)[:500]
    if not query:
        queries = configured_queries(category_id, market_target)
        query = queries[min(max(query_index, 0), len(queries) - 1)]
    return f"https://s.1688.com/selloffer/offer_search.htm?keywords={gbk_quote(query)}"


def cdp_pages() -> list[dict[str, Any]]:
    with urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=2) as response:
        pages = json.loads(response.read().decode("utf-8"))
    return pages if isinstance(pages, list) else []


def reusable_1688_page(pages: list[dict[str, Any]]) -> dict[str, Any] | None:
    normal_pages = [page for page in pages if page.get("type") == "page"]
    for page in normal_pages:
        url = clean(page.get("url"))
        if "1688.com" in url:
            return page
    for page in normal_pages:
        url = clean(page.get("url"))
        if url.startswith(("http://", "https://")):
            return page
    return normal_pages[0] if normal_pages else None


def navigate_existing_cdp_tab(page: dict[str, Any], url: str) -> bool:
    ws_url = clean(page.get("webSocketDebuggerUrl"))
    if not ws_url:
        return False
    try:
        import websocket  # type: ignore

        ws = websocket.create_connection(ws_url, timeout=8, suppress_origin=True)
        ws.send(json.dumps({"id": 1, "method": "Page.bringToFront"}))
        ws.send(json.dumps({"id": 2, "method": "Page.navigate", "params": {"url": url}}))
        ws.close()
        page_id = clean(page.get("id"))
        if page_id:
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/activate/{page_id}", timeout=1).read()
            except Exception:
                pass
        return True
    except Exception:
        return False


def create_cdp_tab(url: str) -> dict[str, Any] | None:
    encoded = quote(url or "about:blank", safe="")
    endpoint = f"http://127.0.0.1:{CDP_PORT}/json/new?{encoded}"
    request = urllib.request.Request(endpoint, method="PUT")
    try:
        with urllib.request.urlopen(request, timeout=4) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload if isinstance(payload, dict) else None
    except Exception:
        try:
            with urllib.request.urlopen(endpoint, timeout=4) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload if isinstance(payload, dict) else None
        except Exception:
            return None


def close_duplicate_1688_search_tabs(keep_id: str) -> None:
    try:
        pages = cdp_pages()
    except Exception:
        return
    for page in pages:
        page_id = clean(page.get("id"))
        url = clean(page.get("url"))
        if not page_id or page_id == keep_id:
            continue
        if "s.1688.com" not in url:
            continue
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/close/{page_id}", timeout=1).read()
        except Exception:
            pass


def open_1688_helper_browser(
    category_id: str,
    query_index: int = 0,
    market_target: str = DEFAULT_MARKET_TARGET,
    exact_query: str = "",
) -> str:
    category = category_id if category_id != "all" else "family-matching"
    market_target = normalize_market_target(market_target)
    if query_index < 0 and not clean(exact_query):
        query_index = next_query_index(category, market_target)
    url = category_search_url(category, query_index, market_target, exact_query)
    try:
        page = reusable_1688_page(cdp_pages())
    except Exception:
        page = None
    if page and navigate_existing_cdp_tab(page, url):
        close_duplicate_1688_search_tabs(clean(page.get("id")))
        return url
    if page is None:
        created = create_cdp_tab(url)
        if created:
            close_duplicate_1688_search_tabs(clean(created.get("id")))
            return url
    subprocess.Popen(
        [
            "open",
            "-na",
            "Google Chrome",
            "--args",
            f"--remote-debugging-port={CDP_PORT}",
            f"--user-data-dir={HELPER_CHROME_PROFILE}",
            "--no-first-run",
            url,
        ],
        cwd=str(REPO_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return url


def chrome_browser_status() -> dict[str, Any]:
    try:
        pages = cdp_pages()
    except Exception as exc:
        return {
            "ok": False,
            "running": False,
            "blocked": True,
            "message": f"1688 helper browser is not connected on port {CDP_PORT}: {exc}",
        }
    page = reusable_1688_page(pages) or {}
    title = clean(page.get("title"))
    url = clean(page.get("url"))
    lower = f"{title} {url}".lower()
    captcha = "captcha" in lower or "_____tmd_____" in lower or "punish" in lower
    login = "login.taobao.com" in lower or "login.1688.com" in lower
    blocked = captcha or login
    if captcha:
        message = "1688 is showing CAPTCHA/interception in Chrome. Clear that browser check before fetching."
    elif login:
        message = "1688 is on a login page in Chrome. Log in before fetching."
    elif page:
        message = "1688 helper browser is connected."
    else:
        message = "Chrome is connected, but no normal page tab is available."
        blocked = True
    return {
        "ok": bool(page) and not blocked,
        "running": True,
        "blocked": blocked,
        "captcha": captcha,
        "login": login,
        "title": title,
        "url": url,
        "message": message,
    }


def collect_job_snapshot(job_id: str) -> dict[str, Any]:
    with COLLECTION_LOCK:
        return dict(COLLECTION_JOBS.get(job_id, {}))


def update_collect_job(job_id: str, **updates: Any) -> None:
    with COLLECTION_LOCK:
        job = COLLECTION_JOBS.setdefault(job_id, {})
        job.update(updates)


def parse_collection_summary(summary_line: str) -> dict[str, int]:
    """Extract the collector's stable numeric outcome fields when present."""
    values: dict[str, int] = {}
    for name in ("reviewable", "total", "queries", "browser_errors"):
        match = re.search(rf"(?:^|\s){name}=(\d+)(?:\s|$)", summary_line)
        if match:
            values[name] = int(match.group(1))
    return values


def detail_job_snapshot(job_id: str) -> dict[str, Any]:
    with DETAIL_LOCK:
        return dict(DETAIL_JOBS.get(job_id, {}))


def update_detail_job(job_id: str, **updates: Any) -> None:
    with DETAIL_LOCK:
        job = DETAIL_JOBS.setdefault(job_id, {})
        job.update(updates)


def run_collect_job(
    job_id: str,
    category_id: str,
    limit: int,
    query_index: int,
    target_reviewable: int,
    max_pages_per_query: int,
    market_target: str,
) -> None:
    market_target = normalize_market_target(market_target)
    command = [
        "python3",
        str(COLLECTOR_PATH),
        "--category",
        category_id,
        "--limit",
        str(limit),
        "--port",
        str(CDP_PORT),
        "--query-index",
        str(query_index),
        "--target-reviewable",
        str(target_reviewable),
        "--max-pages-per-query",
        str(max_pages_per_query),
        "--market-target",
        market_target,
    ]
    update_collect_job(job_id, status="running", command=" ".join(command), started_at=now_iso())
    try:
        with BROWSER_AUTOMATION_LOCK:
            completed = subprocess.run(
                command,
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=900,
                check=False,
            )
    except subprocess.TimeoutExpired as exc:
        update_collect_job(
            job_id,
            status="failed",
            completed_at=now_iso(),
            message="The 1688 search took too long. Try one category at a time.",
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
        )
        return

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    generated_dirs = [line.strip() for line in stdout.splitlines() if line.strip().startswith("ops/sourcing/")]
    summary_line = next((line.strip() for line in stdout.splitlines() if line.strip().startswith("reviewable=")), "")
    if completed.returncode == 0:
        summary = parse_collection_summary(summary_line)
        reviewable = summary.get("reviewable", 0)
        target_met = reviewable >= target_reviewable
        outcome = "complete" if target_met else "partial"
        if summary_line and target_met:
            message = f"Search met its review goal for {category_id}. {summary_line}."
        elif summary_line:
            message = (
                f"Search finished below its review goal for {category_id}: "
                f"{reviewable} of {target_reviewable} reviewable. {summary_line}."
            )
        else:
            message = (
                f"Search finished for {category_id}, but the collector did not return an outcome summary. "
                "Review the fresh queue before relying on the result."
            )
        update_collect_job(
            job_id,
            status="complete",
            outcome=outcome,
            target_met=target_met,
            summary=summary,
            completed_at=now_iso(),
            message=message,
            generated_dirs=generated_dirs,
            stdout=stdout,
            stderr=stderr,
        )
    else:
        combined = f"{stdout}\n{stderr}"
        if "No new 1688 product cards" in combined:
            message = (
                "No new products found in this pass. The app skipped already-seen offers "
                "and rotated the configured searches; try another category or tune the query bank."
            )
        elif "did not finish loading the requested search page" in combined:
            message = (
                "1688 did not finish loading the requested category/market search, so no mismatched products were saved. "
                "Open the helper browser, confirm the intended search page loads, then try Find 20 Leads again."
            )
        elif "browser connection ended" in combined:
            message = (
                "The 1688 helper browser connection ended before new product cards were saved. "
                "Open the helper browser again, confirm it is connected, then try Find 20 Leads."
            )
        elif "CAPTCHA" in combined or "interception" in combined or "_____tmd_____" in combined:
            message = (
                "1688 blocked the search with login/CAPTCHA/interception. Open the helper browser, "
                "clear the check, then try Find 20 Leads again."
            )
        else:
            message = (
                "I could not collect products automatically. Open the 1688 helper browser, "
                "log in or clear CAPTCHA if asked, then click Find 20 Leads again."
            )
        update_collect_job(
            job_id,
            status="failed",
            completed_at=now_iso(),
            message=message,
            generated_dirs=generated_dirs,
            stdout=stdout,
            stderr=stderr,
        )


def start_collect_job(
    category_id: str,
    limit: int,
    query_index: int,
    target_reviewable: int = 20,
    max_pages_per_query: int = 2,
    market_target: str = DEFAULT_MARKET_TARGET,
) -> dict[str, Any]:
    allowed_categories = set(category_lookup()) | {"all"}
    if category_id not in allowed_categories:
        category_id = "family-matching"
    market_target = normalize_market_target(market_target)
    limit = max(1, min(limit, 240))
    target_reviewable = max(0, min(target_reviewable, 25))
    max_pages_per_query = max(1, min(max_pages_per_query, 3))
    job_id = hashlib.sha1(f"{now_iso()}-{category_id}-{market_target}-{limit}".encode("utf-8")).hexdigest()[:12]
    with COLLECTION_LOCK:
        COLLECTION_JOBS[job_id] = {
            "id": job_id,
            "status": "queued",
            "category_id": category_id,
            "market_target": market_target,
            "limit": limit,
            "query_index": query_index,
            "target_reviewable": target_reviewable,
            "max_pages_per_query": max_pages_per_query,
            "created_at": now_iso(),
            "message": (
                "Starting 1688 search. I will rotate the configured occasion keywords, "
                f"use the {market_profile(market_target).get('label', market_target)} market focus, "
                f"and aim for up to {target_reviewable} reviewable leads."
            ),
        }
    thread = threading.Thread(
        target=run_collect_job,
        args=(job_id, category_id, limit, query_index, target_reviewable, max_pages_per_query, market_target),
        daemon=True,
    )
    thread.start()
    return collect_job_snapshot(job_id)


def run_detail_job(job_id: str, key: str) -> None:
    if not DETAIL_ENRICH_PATH.exists():
        candidate = find_candidate(key)
        if candidate:
            persist_workflow_state(
                candidate,
                "needs_attention",
                "Detail verification is not installed. The product remains liked and can be resumed after repair.",
                detail_job_id=job_id,
            )
        update_detail_job(
            job_id,
            status="failed",
            completed_at=now_iso(),
            message="Detail verification is not installed yet. The dashboard found no enrichment script.",
        )
        return
    command = [
        "python3",
        str(DETAIL_ENRICH_PATH),
        "--key",
        key,
        "--port",
        str(CDP_PORT),
    ]
    update_detail_job(job_id, status="running", command=" ".join(command), started_at=now_iso())
    try:
        with BROWSER_AUTOMATION_LOCK:
            completed = subprocess.run(
                command,
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=600,
                check=False,
            )
    except subprocess.TimeoutExpired as exc:
        candidate = find_candidate(key)
        if candidate:
            persist_workflow_state(
                candidate,
                "needs_attention",
                "Detail verification timed out. The product remains liked; resume after checking the helper browser.",
                detail_job_id=job_id,
            )
        update_detail_job(
            job_id,
            status="failed",
            completed_at=now_iso(),
            message="Detail verification took too long. Try again after opening the product in the helper browser.",
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
        )
        return

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    result_line = next((line.strip() for line in stdout.splitlines() if "detail_verdict=" in line), "")
    if completed.returncode == 0:
        message = "Detail proof saved and the preparation package was refreshed."
        if result_line:
            message = f"Detail proof saved: {result_line}. The preparation package was refreshed."
        candidate = find_candidate(key)
        if candidate:
            missing = preparation_missing(candidate)
            stage = "prep_ready" if not missing else "needs_input"
            workflow_message = (
                "Source proof is complete and the local preparation package is ready."
                if not missing
                else f"Source verification finished. {len(missing)} item(s) still need your input."
            )
            persist_workflow_state(candidate, stage, workflow_message, detail_job_id=job_id)
            refreshed = find_candidate(key) or candidate
            create_draft_package(refreshed)
        update_detail_job(
            job_id,
            status="complete",
            completed_at=now_iso(),
            message=message,
            stdout=stdout,
            stderr=stderr,
        )
    else:
        candidate = find_candidate(key)
        if candidate:
            persist_workflow_state(
                candidate,
                "needs_attention",
                "Detail verification stopped at the 1688 helper-browser gate. The product remains liked.",
                detail_job_id=job_id,
            )
        update_detail_job(
            job_id,
            status="failed",
            completed_at=now_iso(),
            message=(
                "Detail verification could not finish. Open the 1688 helper browser, "
                "log in or clear CAPTCHA if asked, then try Verify Detail Proof again."
            ),
            stdout=stdout,
            stderr=stderr,
        )


def start_detail_job(key: str) -> dict[str, Any]:
    with DETAIL_LOCK:
        for job in DETAIL_JOBS.values():
            if clean(job.get("key")) == key and job.get("status") in {"queued", "running"}:
                return dict(job)
    candidate = find_candidate(key)
    if not candidate:
        raise ValueError("candidate not found")
    job_id = hashlib.sha1(f"{now_iso()}-detail-{key}".encode("utf-8")).hexdigest()[:12]
    with DETAIL_LOCK:
        DETAIL_JOBS[job_id] = {
            "id": job_id,
            "status": "queued",
            "key": key,
            "created_at": now_iso(),
            "message": "Opening the 1688 detail page and checking supplier proof.",
        }
    thread = threading.Thread(target=run_detail_job, args=(job_id, key), daemon=True)
    thread.start()
    return detail_job_snapshot(job_id)


def start_listing_prep(key: str) -> dict[str, Any]:
    candidate = find_candidate(key)
    if not candidate:
        raise ValueError("candidate not found")

    persist_workflow_state(
        candidate,
        "liked",
        "Product liked. A local preparation package has been created.",
    )
    candidate = find_candidate(key) or candidate
    package_dir = create_draft_package(candidate)

    if has_detail_proof(candidate):
        missing = preparation_missing(candidate)
        stage = "prep_ready" if not missing else "needs_input"
        message = (
            "Source proof is already available. The local preparation package is ready."
            if not missing
            else f"Source proof is already available. {len(missing)} item(s) still need your input."
        )
        persist_workflow_state(candidate, stage, message)
        candidate = find_candidate(key) or candidate
        create_draft_package(candidate)
        return {
            "ok": True,
            "stage": stage,
            "message": message,
            "requires_user": bool(missing),
            "missing": missing,
            "package_dir": str(package_dir.relative_to(REPO_ROOT)),
            "ready_for_draft": draft_handoff_ready(candidate),
        }

    browser = chrome_browser_status()
    if not browser.get("ok"):
        message = (
            f"Product liked and package saved. {browser.get('message') or 'The 1688 helper browser needs attention'} "
            "Open the helper browser, clear login or CAPTCHA if asked, then press Resume verification."
        )
        persist_workflow_state(candidate, "needs_attention", message)
        refreshed = find_candidate(key) or candidate
        package_dir = create_draft_package(refreshed)
        return {
            "ok": True,
            "stage": "needs_attention",
            "message": message,
            "requires_user": True,
            "browser": browser,
            "missing": preparation_missing(candidate),
            "package_dir": str(package_dir.relative_to(REPO_ROOT)),
            "ready_for_draft": False,
        }

    job = start_detail_job(key)
    message = "Product liked and package saved. Verifying the supplier page now."
    persist_workflow_state(candidate, "verifying", message, detail_job_id=clean(job.get("id")))
    return {
        "ok": True,
        "stage": "verifying",
        "message": message,
        "requires_user": False,
        "job": job,
        "missing": preparation_missing(candidate),
        "package_dir": str(package_dir.relative_to(REPO_ROOT)),
        "ready_for_draft": False,
    }


def infer_category(run_dir: Path, metadata: dict[str, Any]) -> str:
    explicit = clean(metadata.get("category_id"))
    if explicit:
        return explicit
    name = run_dir.name.lower()
    if "mommy" in name or "mother" in name or "mom" in name:
        return "mommy-and-me"
    if "daddy" in name or "father" in name or "dad" in name:
        return "daddy-and-me"
    if "couple" in name:
        return "couples"
    if "maternity" in name or "preg" in name:
        return "maternity"
    return "family-matching"


def candidate_search_text(candidate: dict[str, Any]) -> str:
    parts = [
        candidate.get("title"),
        candidate.get("vendor_name"),
        candidate.get("badges"),
        candidate.get("service_flags"),
        candidate.get("raw_card_text"),
        candidate.get("search_query"),
        candidate.get("sales_context"),
        candidate.get("market_label"),
        candidate.get("market_target"),
    ]
    return clean(" ".join(clean(part) for part in parts)).lower()


def display_candidate_title(candidate: dict[str, Any]) -> str:
    title = re.sub(r"^Find Similar\s+", "", clean(candidate.get("title")), flags=re.IGNORECASE)
    title = re.split(r"\s+[¥￥]\s*\d", title, maxsplit=1)[0]
    return title or clean(candidate.get("title") or candidate.get("product_url"))


def candidate_fit_summary(candidate: dict[str, Any]) -> str:
    signals = candidate.get("positive_signals", [])
    if not isinstance(signals, list):
        signals = [part for part in clean(signals).split("|") if clean(part)]
    useful = [
        clean(signal)
        for signal in signals
        if clean(signal)
        and "market search focus" not in clean(signal).lower()
        and "market style/cross-border" not in clean(signal).lower()
        and "no obvious ip-risk" not in clean(signal).lower()
    ]
    if useful:
        return "; ".join(useful[:2])
    return "Category and demand signals justify a closer source check"


def load_candidates() -> list[dict[str, Any]]:
    decisions = load_decisions().get("items", {})
    categories = category_lookup()
    markets = market_profile_lookup()
    candidates: list[dict[str, Any]] = []
    for scored_path in sorted(SOURCING_ROOT.glob("**/scored-candidates.json")):
        run_dir = scored_path.parent
        if run_dir.name == "demo-shortlist":
            continue
        payload = read_json(scored_path, {})
        if not isinstance(payload, dict):
            continue
        run_metadata = read_json(run_dir / "run.json", {})
        run_id = clean(run_metadata.get("run_id") or run_dir.name)
        observed_at = parse_run_observed_at(payload, run_id, scored_path)
        category_id = infer_category(run_dir, run_metadata)
        category = categories.get(category_id, {})
        for item in payload.get("candidates", []):
            if not isinstance(item, dict):
                continue
            key = offer_key(item.get("product_url", ""))
            decision = decisions.get(key, {})
            evidence = decision.get("evidence", {}) if isinstance(decision, dict) else {}
            market_target = normalize_market_target(item.get("market_target") or run_metadata.get("market_target"))
            market = markets.get(market_target, markets.get(DEFAULT_MARKET_TARGET, {}))
            candidate = dict(item)
            candidate["key"] = key
            candidate["run_id"] = run_id
            candidate["observed_at"] = observed_at
            candidate["run_dir"] = str(run_dir.relative_to(REPO_ROOT))
            candidate["shortlist_path"] = str((run_dir / "shortlist.html").relative_to(REPO_ROOT))
            candidate["category_id"] = category_id
            candidate["category_label"] = category.get("label", category_id)
            candidate["listing_mode"] = category.get("listing_mode", "Family Matching")
            candidate["market_target"] = market_target
            candidate["market_label"] = market.get("short_label") or market.get("label") or market_target
            candidate["decision"] = decision.get("action", "")
            candidate["decision_updated_at"] = decision.get("updated_at", "")
            candidate["decision_record"] = decision if isinstance(decision, dict) else {}
            candidate["evidence"] = evidence if isinstance(evidence, dict) else {}
            candidate["ready_for_draft"] = draft_handoff_ready(candidate)
            candidate["draft_package_path"] = str(package_dir_for_key(key).relative_to(REPO_ROOT))
            candidate["search_text"] = candidate_search_text(candidate)
            candidates.append(candidate)
    deduped: dict[str, dict[str, Any]] = {}
    stage_rank = {"detail": 2, "search": 1}
    for candidate in candidates:
        key = clean(candidate.get("key")) or clean(candidate.get("product_url")) or clean(candidate.get("title"))
        if not key:
            continue
        existing = deduped.get(key)
        matched_categories = set(existing.get("matched_category_ids", [])) if existing else set()
        if clean(candidate.get("category_id")):
            matched_categories.add(clean(candidate.get("category_id")))
        candidate_rank = (
            stage_rank.get(clean(candidate.get("review_stage")), 0),
            clean(candidate.get("observed_at")),
            int(candidate.get("score") or 0),
            clean(candidate.get("run_id")),
        )
        existing_rank = (
            stage_rank.get(clean(existing.get("review_stage")), 0) if existing else 0,
            clean(existing.get("observed_at")) if existing else "",
            int(existing.get("score") or 0) if existing else 0,
            clean(existing.get("run_id")) if existing else "",
        )
        if existing is None or candidate_rank >= existing_rank:
            candidate["matched_category_ids"] = sorted(matched_categories)
            deduped[key] = candidate
        elif existing is not None:
            existing["matched_category_ids"] = sorted(matched_categories)
    candidates = list(deduped.values())
    latest_search_run_id = max(
        (
            clean(candidate.get("run_id"))
            for candidate in candidates
            if clean(candidate.get("review_stage")) == "search" and re.match(r"20\d{2}-\d{2}-\d{2}-\d{6}", clean(candidate.get("run_id")))
        ),
        default="",
    )
    for candidate in candidates:
        apply_detail_gate(candidate)
        candidate["is_latest_run"] = bool(latest_search_run_id and clean(candidate.get("run_id")) == latest_search_run_id)
        candidate["review_recommended"] = is_review_recommended(candidate)
        candidate["opportunity_score"] = int(candidate.get("score") or 0)
        candidate["opportunity_confidence"] = opportunity_confidence(candidate)
        candidate["freshness_label"] = freshness_label(clean(candidate.get("observed_at")))
        candidate["supplier_rating_label"] = clean(candidate.get("rating")) or "Unavailable"
        candidate["supplier_rating_provenance"] = (
            "Verified on the supplier detail page"
            if clean(candidate.get("rating")) and has_detail_proof(candidate)
            else "Not collected from the search card"
        )
        candidate["display_title"] = display_candidate_title(candidate)
        candidate["why_fit"] = candidate_fit_summary(candidate)
        candidate["workflow"] = workflow_snapshot(candidate)
        assessment = opportunity_assessment(candidate)
        candidate["opportunity_tier"] = assessment["tier"]
        candidate["opportunity_label"] = assessment["label"]
        candidate["opportunity_reason"] = assessment["reason"]
        candidate["opportunity_failures"] = assessment["failures"]
        candidate["evidence_confidence"] = assessment["evidence_confidence"]
        candidate["evidence_confirmed"] = assessment["confirmed"]
        candidate["supplier_years_label"] = assessment["supplier_years_label"]
        candidate["supplier_years_provenance"] = assessment["supplier_years_provenance"]
        candidate["minimum_supplier_years"] = assessment["minimum_supplier_years"]
        candidate["listing_year_label"] = assessment["listing_year_label"]
    candidates.sort(
        key=lambda item: (
            item.get("category_label", ""),
            1 if item.get("decision") == "reject" else 0,
            {"Gold": 0, "Test": 1, "Reject": 2}.get(item.get("verdict"), 9),
            -int(item.get("score") or 0),
            item.get("title", "").lower(),
        )
    )
    return candidates


def latest_run_summary(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    search_runs = [
        candidate
        for candidate in candidates
        if clean(candidate.get("review_stage")) == "search"
        and re.match(r"20\d{2}-\d{2}-\d{2}-\d{6}", clean(candidate.get("run_id")))
    ]
    if not search_runs:
        return {
            "run_id": "",
            "observed_at": "",
            "collected": 0,
            "reviewable": 0,
            "filtered": 0,
            "category_label": "",
            "market_label": "",
        }
    latest_id = max(clean(candidate.get("run_id")) for candidate in search_runs)
    items = [candidate for candidate in search_runs if clean(candidate.get("run_id")) == latest_id]
    reviewable = sum(bool(candidate.get("review_recommended")) for candidate in items)
    first = items[0]
    return {
        "run_id": latest_id,
        "observed_at": clean(first.get("observed_at")),
        "freshness_label": freshness_label(clean(first.get("observed_at"))),
        "collected": len(items),
        "reviewable": reviewable,
        "filtered": len(items) - reviewable,
        "category_id": clean(first.get("category_id")),
        "category_label": clean(first.get("category_label")),
        "market_target": clean(first.get("market_target")),
        "market_label": clean(first.get("market_label")),
    }


def candidate_ui_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    fields = (
        "key",
        "title",
        "display_title",
        "product_url",
        "image_url",
        "category_id",
        "category_label",
        "listing_mode",
        "market_target",
        "market_label",
        "run_id",
        "observed_at",
        "review_stage",
        "verdict",
        "score",
        "opportunity_score",
        "opportunity_confidence",
        "freshness_label",
        "why_fit",
        "price_cny",
        "moq",
        "monthly_sales",
        "repurchase_rate_pct",
        "rating",
        "supplier_rating_label",
        "supplier_rating_provenance",
        "vendor_name",
        "years_on_1688",
        "years_on_1688_scope",
        "years_on_1688_label",
        "supplier_years_label",
        "supplier_years_provenance",
        "minimum_supplier_years",
        "availability",
        "dropship_supported",
        "service_flags",
        "size_chart",
        "vendor_image_urls",
        "detail_proof_verified",
        "decision",
        "decision_updated_at",
        "ready_for_draft",
        "draft_package_path",
        "is_latest_run",
        "review_recommended",
        "matched_category_ids",
        "opportunity_tier",
        "opportunity_label",
        "opportunity_reason",
        "opportunity_failures",
        "evidence_confidence",
        "evidence_confirmed",
        "listing_year_label",
        "evidence",
        "workflow",
    )
    payload = {field: candidate.get(field) for field in fields}
    payload["search_text"] = clean(candidate.get("search_text"))[:1200]
    return payload


def find_candidate(key: str) -> dict[str, Any] | None:
    for candidate in load_candidates():
        if candidate.get("key") == key:
            return candidate
    return None


def category_counts(candidates: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for candidate in candidates:
        category_id = candidate.get("category_id", "uncategorized")
        bucket = result.setdefault(
            category_id,
            {"total": 0, "active": 0, "kept": 0, "ready": 0, "rejected": 0, "gold": 0, "test": 0},
        )
        bucket["total"] += 1
        if candidate.get("decision") == "reject":
            bucket["rejected"] += 1
        else:
            if candidate.get("verdict") != "Reject":
                bucket["active"] += 1
        if candidate.get("decision") == "keep":
            bucket["kept"] += 1
        if candidate.get("ready_for_draft"):
            bucket["ready"] += 1
        if candidate.get("verdict") == "Gold":
            bucket["gold"] += 1
        if candidate.get("verdict") == "Test":
            bucket["test"] += 1
    return result


def json_copy(payload: Any) -> Any:
    return json.loads(json.dumps(payload, ensure_ascii=False))


def default_scout_schedule() -> dict[str, Any]:
    category_ids = [clean(item.get("id")) for item in load_categories() if clean(item.get("id"))]
    market_ids = [clean(item.get("id")) for item in load_market_profiles() if clean(item.get("id")) in {"us", "eu"}]
    rules = load_seasonal_rules()
    review_gate = rules.get("review_gate", {}) if isinstance(rules.get("review_gate"), dict) else {}
    review_required = bool(review_gate.get("required"))
    return {
        "enabled": not review_required,
        "interval_hours": DEFAULT_SCOUT_INTERVAL_HOURS,
        "next_run_at": "",
        "last_run_at": "",
        "category_ids": category_ids,
        "market_targets": market_ids or [DEFAULT_MARKET_TARGET],
        "query_budget_per_lane": DEFAULT_SCOUT_QUERY_BUDGET,
        "pages_per_query": 1,
        "detail_limit_per_lane": DEFAULT_SCOUT_DETAIL_LIMIT,
        "minimum_supplier_years": MINIMUM_SUPPLIER_YEARS,
        "query_selections": {},
        "sourcing_brief": default_sourcing_brief(),
        "plan_as_of": "",
        "plan_hash": "",
        "plan_preview": {},
        "reviewed_plan_hash": "",
        "paused_reason": clean(review_gate.get("paused_reason")) if review_required else "",
    }


def default_scout_state() -> dict[str, Any]:
    return {
        "version": 2,
        "updated_at": "",
        "active_job_id": "",
        "schedule": default_scout_schedule(),
        "jobs": {},
        "history": [],
    }


def load_scout_state() -> dict[str, Any]:
    try:
        state = read_json(SCOUT_STATE_PATH, default_scout_state())
    except (OSError, ValueError, json.JSONDecodeError):
        state = default_scout_state()
    if not isinstance(state, dict):
        state = default_scout_state()
    state["version"] = max(2, int(state.get("version") or 1))
    state.setdefault("updated_at", "")
    state.setdefault("active_job_id", "")
    state.setdefault("jobs", {})
    state.setdefault("history", [])
    schedule = state.setdefault("schedule", {})
    defaults = default_scout_schedule()
    if not isinstance(schedule, dict):
        schedule = defaults
        state["schedule"] = schedule
    legacy_search_plan = not isinstance(schedule.get("sourcing_brief"), dict)
    for key, value in defaults.items():
        schedule.setdefault(key, value)
    if legacy_search_plan:
        schedule["category_ids"] = list(defaults["category_ids"])
        schedule["market_targets"] = list(defaults["market_targets"])
        schedule["query_selections"] = {}
        schedule["sourcing_brief"] = json_copy(defaults["sourcing_brief"])
        schedule["plan_as_of"] = ""
        schedule["plan_hash"] = ""
        schedule["plan_preview"] = {}
    schedule["minimum_supplier_years"] = MINIMUM_SUPPLIER_YEARS
    return state


def save_scout_state(state: dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    write_json_atomic(SCOUT_STATE_PATH, state)


def scout_snapshot() -> dict[str, Any]:
    with SCOUT_STATE_LOCK:
        state = load_scout_state()
        active_id = clean(state.get("active_job_id"))
        active = state.get("jobs", {}).get(active_id, {}) if active_id else {}
        return {
            "version": state.get("version", 2),
            "updated_at": state.get("updated_at", ""),
            "active_job_id": active_id,
            "active_job": json_copy(active) if isinstance(active, dict) else {},
            "schedule": json_copy(state.get("schedule", {})),
            "history": json_copy(state.get("history", [])[-10:]),
        }


def normalize_scout_config(
    payload: dict[str, Any],
    fallback: dict[str, Any] | None = None,
    *,
    as_of: Any = None,
) -> dict[str, Any]:
    fallback = fallback if isinstance(fallback, dict) else default_scout_schedule()
    date = plan_date(as_of if as_of is not None else payload.get("plan_as_of"))
    allowed_categories = list(category_lookup())
    requested_categories = payload.get("category_ids", fallback.get("category_ids", allowed_categories))
    category_ids = [clean(item) for item in requested_categories if clean(item) in allowed_categories]
    if not category_ids:
        category_ids = allowed_categories
    allowed_markets = list(market_profile_lookup())
    requested_markets = payload.get("market_targets", fallback.get("market_targets", [DEFAULT_MARKET_TARGET]))
    market_targets = []
    for item in requested_markets:
        target = normalize_market_target(item)
        if target in allowed_markets and target not in market_targets:
            market_targets.append(target)
    if not market_targets:
        market_targets = [DEFAULT_MARKET_TARGET]
    raw_selections = payload.get("query_selections", fallback.get("query_selections", {}))
    query_selections: dict[str, list[int]] = {}
    if isinstance(raw_selections, dict):
        for category_id in category_ids:
            total = len(configured_queries(category_id))
            values = raw_selections.get(category_id, [])
            if not isinstance(values, list):
                continue
            selected = sorted({int(value) for value in values if str(value).lstrip("-").isdigit() and 0 <= int(value) < total})
            if selected:
                query_selections[category_id] = selected
    raw_brief = payload.get("sourcing_brief")
    if not isinstance(raw_brief, dict):
        raw_brief = fallback.get("sourcing_brief", {})
    sourcing_brief = normalize_sourcing_brief(raw_brief, fallback.get("sourcing_brief", {}), as_of=date)
    return {
        "enabled": bool(payload.get("enabled", fallback.get("enabled", True))),
        "interval_hours": max(6, min(int(payload.get("interval_hours", fallback.get("interval_hours", DEFAULT_SCOUT_INTERVAL_HOURS))), 168)),
        "category_ids": category_ids,
        "market_targets": market_targets,
        "query_budget_per_lane": max(1, min(int(payload.get("query_budget_per_lane", fallback.get("query_budget_per_lane", DEFAULT_SCOUT_QUERY_BUDGET))), 8)),
        "pages_per_query": max(1, min(int(payload.get("pages_per_query", fallback.get("pages_per_query", 1))), 2)),
        "detail_limit_per_lane": max(1, min(int(payload.get("detail_limit_per_lane", fallback.get("detail_limit_per_lane", DEFAULT_SCOUT_DETAIL_LIMIT))), 4)),
        "minimum_supplier_years": MINIMUM_SUPPLIER_YEARS,
        "query_selections": query_selections,
        "sourcing_brief": sourcing_brief,
        "plan_as_of": date.isoformat(),
        "reviewed_plan_hash": clean(payload.get("reviewed_plan_hash", fallback.get("reviewed_plan_hash"))),
    }


def scout_lane_plan(config: dict[str, Any], search_plan: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    categories = category_lookup()
    markets = market_profile_lookup()
    lanes: list[dict[str, Any]] = []
    planned_lanes: list[tuple[str, str, list[str], str, list[dict[str, Any]], list[int]]] = []
    if search_plan is not None:
        for lane_id, raw_queries in (search_plan.get("lanes", {}) or {}).items():
            exact_queries = [row for row in raw_queries if isinstance(row, dict)] if isinstance(raw_queries, list) else []
            if not exact_queries:
                continue
            first = exact_queries[0]
            category_id = clean(first.get("category_id"))
            market_target = normalize_market_target(first.get("market_target"))
            market_targets = [clean(value) for value in first.get("market_targets", []) if clean(value)]
            market_label = clean(first.get("market_label")) or clean(markets.get(market_target, {}).get("short_label")) or market_target
            planned_lanes.append((clean(lane_id), category_id, market_targets, market_label, exact_queries, []))
    else:
        for category_id in config["category_ids"]:
            for market_target in config["market_targets"]:
                lane_id = f"{category_id}:{market_target}"
                query_indexes = list(config.get("query_selections", {}).get(category_id, []))
                planned_lanes.append(
                    (
                        lane_id,
                        category_id,
                        [market_target],
                        clean(markets.get(market_target, {}).get("short_label")) or market_target,
                        [],
                        query_indexes,
                    )
                )
    for lane_id, category_id, market_targets, market_label, exact_queries, query_indexes in planned_lanes:
        market_target = normalize_market_target(exact_queries[0].get("market_target")) if exact_queries else normalize_market_target(market_targets[0] if market_targets else "")
        query_total = len(exact_queries) if exact_queries else len(configured_queries(category_id, market_target))
        planned = len(exact_queries) if exact_queries else (len(query_indexes) if query_indexes else min(config["query_budget_per_lane"], query_total))
        lanes.append(
            {
                "id": lane_id,
                "category_id": category_id,
                "category_label": clean(categories.get(category_id, {}).get("label")) or category_id,
                "market_target": market_target,
                "market_targets": market_targets or [market_target],
                "market_label": market_label,
                "status": "queued",
                "outcome": "",
                "message": "Queued for one concise discovery pass and supplier verification.",
                "query_total": query_total,
                "queries_planned": planned,
                "queries_attempted": 0,
                "query_indexes": query_indexes,
                "exact_queries": json_copy(exact_queries),
                "query_cursor": 0,
                "search_complete": False,
                "run_dirs": [],
                "new_offer_ids": [],
                "detail_queue": [],
                "detail_cursor": 0,
                "detail_results": {},
                "counts": {
                    "new": 0,
                    "promising": 0,
                    "verified": 0,
                    "rejected": 0,
                    "duplicates": 0,
                },
                "blocker": {},
            }
        )
    return lanes


def save_scout_schedule(payload: dict[str, Any]) -> dict[str, Any]:
    with SCOUT_STATE_LOCK:
        state = load_scout_state()
        existing = state.get("schedule", {})
        date = plan_date(payload.get("plan_as_of"))
        config = normalize_scout_config(payload, existing, as_of=date)
        config["reviewed_plan_hash"] = clean(existing.get("reviewed_plan_hash"))
        preview = build_sourcing_plan(config, date)
        config["plan_as_of"] = preview["as_of_date"]
        config["plan_hash"] = preview["plan_hash"]
        config["plan_preview"] = preview
        config["last_run_at"] = clean(existing.get("last_run_at"))
        config["next_run_at"] = clean(existing.get("next_run_at"))
        if not preview.get("execution_allowed", True):
            config["enabled"] = False
            config["paused_reason"] = clean(preview.get("review", {}).get("paused_reason"))
        elif config["enabled"]:
            config["paused_reason"] = ""
        if config["enabled"] and not config["next_run_at"]:
            config["next_run_at"] = now_iso()
        if not config["enabled"]:
            config["next_run_at"] = ""
        state["schedule"] = config
        save_scout_state(state)
        return json_copy(config)


def confirm_scout_plan_review(payload: dict[str, Any]) -> dict[str, Any]:
    """Record an explicit local review acknowledgement without starting a search."""
    with SCOUT_STATE_LOCK:
        state = load_scout_state()
        existing = state.get("schedule", {})
        date = plan_date(payload.get("plan_as_of"))
        config = normalize_scout_config(payload, existing, as_of=date)
        config["reviewed_plan_hash"] = ""
        preview = build_sourcing_plan(config, date)
        config["reviewed_plan_hash"] = preview["plan_hash"]
        preview = build_sourcing_plan(config, date)
        config["enabled"] = False
        config["plan_as_of"] = preview["as_of_date"]
        config["plan_hash"] = preview["plan_hash"]
        config["plan_preview"] = preview
        config["last_run_at"] = clean(existing.get("last_run_at"))
        config["next_run_at"] = ""
        config["paused_reason"] = "exact searches reviewed; automatic scouting remains off"
        state["schedule"] = config
        save_scout_state(state)
        return {"schedule": json_copy(config), "plan": preview}


def active_scout_job(state: dict[str, Any]) -> dict[str, Any]:
    job_id = clean(state.get("active_job_id"))
    job = state.get("jobs", {}).get(job_id, {}) if job_id else {}
    return job if isinstance(job, dict) else {}


def start_scout_job(payload: dict[str, Any] | None = None, *, scheduled: bool = False) -> dict[str, Any]:
    payload = payload if isinstance(payload, dict) else {}
    with SCOUT_STATE_LOCK:
        state = load_scout_state()
        existing = active_scout_job(state)
        if clean(existing.get("status")) in {"queued", "running", "waiting_for_user"}:
            launch_scout_worker(clean(existing.get("id")))
            return json_copy(existing)
        schedule = state.get("schedule", {})
        date = dt.date.today() if scheduled else plan_date(payload.get("plan_as_of"))
        config = normalize_scout_config(payload, schedule, as_of=date)
        config["reviewed_plan_hash"] = clean(schedule.get("reviewed_plan_hash"))
        search_plan = build_sourcing_plan(config, date)
        if not search_plan.get("execution_allowed", True):
            reason = clean(search_plan.get("review", {}).get("paused_reason")) or "review the exact searches before running"
            raise ValueError(f"Search plan {search_plan['plan_hash']} is review-only: {reason}.")
        config["plan_as_of"] = search_plan["as_of_date"]
        config["plan_hash"] = search_plan["plan_hash"]
        if not scheduled:
            schedule.update(config)
            schedule["minimum_supplier_years"] = MINIMUM_SUPPLIER_YEARS
            schedule["plan_preview"] = search_plan
            state["schedule"] = schedule
        job_id = hashlib.sha1(f"{now_iso()}-opportunity-scout".encode("utf-8")).hexdigest()[:12]
        job = {
            "id": job_id,
            "status": "queued",
            "outcome": "",
            "created_at": now_iso(),
            "started_at": "",
            "completed_at": "",
            "requires_user": False,
            "message": "Opportunity Scout queued. You can leave this page; progress is saved.",
            "config": config,
            "search_plan": search_plan,
            "cursor": {"lane_index": 0},
            "lanes": scout_lane_plan(config, search_plan),
            "verified_keys": [],
            "promising_keys": [],
            "rejected_keys": [],
            "trigger": "schedule" if scheduled else "owner",
        }
        jobs = state.setdefault("jobs", {})
        jobs[job_id] = job
        state["active_job_id"] = job_id
        ordered = sorted(jobs, key=lambda key: clean(jobs[key].get("created_at")))
        for old_id in ordered[:-20]:
            jobs.pop(old_id, None)
        save_scout_state(state)
    launch_scout_worker(job_id)
    return json_copy(job)


def mutate_scout_job(job_id: str, mutator: Any) -> dict[str, Any]:
    with SCOUT_STATE_LOCK:
        state = load_scout_state()
        job = state.get("jobs", {}).get(job_id)
        if not isinstance(job, dict):
            return {}
        mutator(job, state)
        save_scout_state(state)
        return json_copy(job)


def mark_scout_waiting(job_id: str, lane_id: str, message: str) -> None:
    def apply(job: dict[str, Any], _state: dict[str, Any]) -> None:
        job.update({"status": "waiting_for_user", "requires_user": True, "message": message})
        for lane in job.get("lanes", []):
            if lane.get("id") == lane_id:
                lane.update(
                    {
                        "status": "waiting_for_user",
                        "message": message,
                        "blocker": {"kind": "1688_access", "at": now_iso(), "message": message},
                    }
                )
                break
    mutate_scout_job(job_id, apply)


def sourcing_run_dirs() -> set[str]:
    result: set[str] = set()
    for run_path in SOURCING_ROOT.glob("*/run.json"):
        metadata = read_json(run_path, {})
        if clean(metadata.get("stage")) == "search":
            result.add(str(run_path.parent.relative_to(REPO_ROOT)))
    return result


def parse_generated_run_dirs(stdout: str, before: set[str]) -> list[str]:
    generated = {
        clean(line)
        for line in stdout.splitlines()
        if clean(line).startswith("ops/sourcing/") and (REPO_ROOT / clean(line) / "scored-candidates.json").exists()
    }
    generated.update(sourcing_run_dirs() - before)
    return sorted(generated)


def scout_collection_once(
    category_id: str,
    market_target: str,
    *,
    query_index: int,
    max_queries: int,
    pages_per_query: int,
    exact_query: str = "",
) -> dict[str, Any]:
    before = sourcing_run_dirs()
    command = [
        "python3",
        str(COLLECTOR_PATH),
        "--category",
        category_id,
        "--limit",
        "120",
        "--port",
        str(CDP_PORT),
        "--query-index",
        str(query_index),
        "--target-reviewable",
        "3" if query_index < 0 else "0",
        "--max-pages-per-query",
        str(pages_per_query),
        "--max-queries",
        str(max_queries),
        "--market-target",
        market_target,
    ]
    if clean(exact_query):
        command.extend(["--exact-query", clean(exact_query)[:500]])
    try:
        with BROWSER_AUTOMATION_LOCK:
            completed = subprocess.run(
                command,
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=720,
                check=False,
            )
    except subprocess.TimeoutExpired:
        return {"status": "failed", "message": "This lane timed out; the scout will continue with the other lanes.", "run_dirs": [], "summary": {}}
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    combined = f"{stdout}\n{stderr}"
    run_dirs = parse_generated_run_dirs(stdout, before)
    summary_line = next((clean(line) for line in stdout.splitlines() if clean(line).startswith("reviewable=")), "")
    summary = parse_collection_summary(summary_line)
    blocked = any(term.lower() in combined.lower() for term in ("CAPTCHA", "interception", "login.1688", "login.taobao", "_____tmd_____"))
    if blocked:
        return {
            "status": "waiting_for_user",
            "message": "1688 needs one login or browser check. Open it once; the scout will resume this saved scan automatically.",
            "run_dirs": run_dirs,
            "summary": summary,
        }
    if completed.returncode == 0:
        return {
            "status": "complete",
            "message": "Search coverage completed for this lane.",
            "run_dirs": run_dirs,
            "summary": summary,
        }
    if "No new 1688 product cards" in combined:
        return {
            "status": "complete",
            "message": "No unseen products were found in this coverage slice.",
            "run_dirs": run_dirs,
            "summary": summary,
        }
    return {
        "status": "failed",
        "message": "This search slice could not finish; the scout recorded it and will continue with the other lanes.",
        "run_dirs": run_dirs,
        "summary": summary,
    }


def candidates_for_run_dirs(run_dirs: list[str], limit: int) -> list[str]:
    wanted = set(run_dirs)
    candidates = [
        candidate
        for candidate in load_candidates()
        if clean(candidate.get("run_dir")) in wanted
        and clean(candidate.get("review_stage")) == "search"
        and candidate.get("review_recommended")
        and clean(candidate.get("decision")) != "reject"
    ]
    candidates.sort(key=lambda item: (-int(item.get("score") or 0), clean(item.get("key"))))
    return [clean(candidate.get("key")) for candidate in candidates[:limit] if clean(candidate.get("key"))]


def scout_detail_once(key: str) -> dict[str, Any]:
    command = ["python3", str(DETAIL_ENRICH_PATH), "--key", key, "--port", str(CDP_PORT)]
    try:
        with BROWSER_AUTOMATION_LOCK:
            completed = subprocess.run(
                command,
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=600,
                check=False,
            )
    except subprocess.TimeoutExpired:
        return {"status": "failed", "message": "Supplier verification timed out."}
    combined = f"{completed.stdout or ''}\n{completed.stderr or ''}"
    if any(term.lower() in combined.lower() for term in ("CAPTCHA", "interception", "login.1688", "login.taobao", "_____tmd_____")):
        return {
            "status": "waiting_for_user",
            "message": "1688 needs one browser check during supplier verification. Clear it once and the scout will resume.",
        }
    if completed.returncode != 0:
        return {"status": "failed", "message": "Supplier verification could not complete for this product."}
    candidate = find_candidate(key)
    assessment = opportunity_assessment(candidate) if candidate else {"tier": "rejected", "reason": "Verified product record was not found."}
    return {
        "status": "complete",
        "message": clean(assessment.get("reason")),
        "tier": clean(assessment.get("tier")),
        "supplier_years": assessment.get("supplier_years"),
        "evidence_confidence": assessment.get("evidence_confidence", 0),
    }


def merge_lane_run_result(job_id: str, lane_id: str, result: dict[str, Any], attempted: int) -> dict[str, Any]:
    def apply(job: dict[str, Any], _state: dict[str, Any]) -> None:
        for lane in job.get("lanes", []):
            if lane.get("id") != lane_id:
                continue
            lane["run_dirs"] = sorted(set(lane.get("run_dirs", [])) | set(result.get("run_dirs", [])))
            lane["queries_attempted"] = min(
                int(lane.get("queries_planned") or 0),
                int(lane.get("queries_attempted") or 0) + max(0, attempted),
            )
            lane["message"] = clean(result.get("message"))
            if result.get("status") == "failed":
                lane["outcome"] = "partial"
            break
    return mutate_scout_job(job_id, apply)


def run_scout_job(job_id: str) -> None:
    if not SCOUT_WORKER_LOCK.acquire(blocking=False):
        return
    try:
        mutate_scout_job(
            job_id,
            lambda job, _state: job.update(
                {
                    "status": "running",
                    "started_at": clean(job.get("started_at")) or now_iso(),
                    "requires_user": False,
                    "message": "Opportunity Scout is checking every selected lane and verifying the strongest products.",
                }
            ),
        )
        while True:
            snapshot = scout_snapshot()
            job = snapshot.get("active_job", {})
            if clean(job.get("id")) != job_id:
                return
            lane_index = int(job.get("cursor", {}).get("lane_index") or 0)
            lanes = job.get("lanes", [])
            if lane_index >= len(lanes):
                break
            lane = lanes[lane_index]
            lane_id = clean(lane.get("id"))
            category_id = clean(lane.get("category_id"))
            market_target = clean(lane.get("market_target")) or DEFAULT_MARKET_TARGET

            browser = chrome_browser_status()
            if not browser.get("ok"):
                if not browser.get("running"):
                    exact_queries = list(lane.get("exact_queries", []))
                    exact_query = clean(exact_queries[0].get("chinese")) if exact_queries and isinstance(exact_queries[0], dict) else ""
                    query_index = lane.get("query_indexes", [next_query_index(category_id, market_target)])
                    first_index = int(query_index[0]) if query_index else next_query_index(category_id, market_target)
                    try:
                        open_1688_helper_browser(category_id, first_index, market_target, exact_query)
                    except Exception:
                        pass
                    time.sleep(1)
                    browser = chrome_browser_status()
                if not browser.get("ok"):
                    mark_scout_waiting(
                        job_id,
                        lane_id,
                        clean(browser.get("message"))
                        or "1688 needs one login or browser check. Open it once; this scan will resume automatically.",
                    )
                    return

            def mark_searching(active: dict[str, Any], _state: dict[str, Any]) -> None:
                active.update({"status": "running", "requires_user": False})
                for row in active.get("lanes", []):
                    if row.get("id") == lane_id:
                        row.update({"status": "searching", "blocker": {}, "message": "Searching saved source terms…"})
                        break
            mutate_scout_job(job_id, mark_searching)

            if not lane.get("search_complete"):
                exact_queries = [row for row in lane.get("exact_queries", []) if isinstance(row, dict) and clean(row.get("chinese"))]
                query_indexes = list(lane.get("query_indexes", []))
                if exact_queries:
                    cursor = int(lane.get("query_cursor") or 0)
                    while cursor < len(exact_queries):
                        result = scout_collection_once(
                            category_id,
                            market_target,
                            query_index=0,
                            max_queries=1,
                            pages_per_query=int(job.get("config", {}).get("pages_per_query") or 1),
                            exact_query=clean(exact_queries[cursor].get("chinese")),
                        )
                        merge_lane_run_result(job_id, lane_id, result, 1)
                        if result.get("status") == "waiting_for_user":
                            mark_scout_waiting(job_id, lane_id, clean(result.get("message")))
                            return
                        cursor += 1

                        def move_exact_query(active: dict[str, Any], _state: dict[str, Any], value: int = cursor) -> None:
                            for row in active.get("lanes", []):
                                if row.get("id") == lane_id:
                                    row["query_cursor"] = value
                                    break

                        mutate_scout_job(job_id, move_exact_query)
                elif query_indexes:
                    cursor = int(lane.get("query_cursor") or 0)
                    while cursor < len(query_indexes):
                        result = scout_collection_once(
                            category_id,
                            market_target,
                            query_index=int(query_indexes[cursor]),
                            max_queries=1,
                            pages_per_query=int(job.get("config", {}).get("pages_per_query") or 1),
                        )
                        merge_lane_run_result(job_id, lane_id, result, 1)
                        if result.get("status") == "waiting_for_user":
                            mark_scout_waiting(job_id, lane_id, clean(result.get("message")))
                            return
                        cursor += 1
                        def move_query(active: dict[str, Any], _state: dict[str, Any], value: int = cursor) -> None:
                            for row in active.get("lanes", []):
                                if row.get("id") == lane_id:
                                    row["query_cursor"] = value
                                    break
                        mutate_scout_job(job_id, move_query)
                else:
                    budget = int(job.get("config", {}).get("query_budget_per_lane") or DEFAULT_SCOUT_QUERY_BUDGET)
                    result = scout_collection_once(
                        category_id,
                        market_target,
                        query_index=-1,
                        max_queries=budget,
                        pages_per_query=int(job.get("config", {}).get("pages_per_query") or 1),
                    )
                    attempted = int(result.get("summary", {}).get("queries") or budget)
                    merge_lane_run_result(job_id, lane_id, result, attempted)
                    if result.get("status") == "waiting_for_user":
                        mark_scout_waiting(job_id, lane_id, clean(result.get("message")))
                        return

                def finish_search(active: dict[str, Any], _state: dict[str, Any]) -> None:
                    for row in active.get("lanes", []):
                        if row.get("id") != lane_id:
                            continue
                        row["search_complete"] = True
                        keys = candidates_for_run_dirs(
                            row.get("run_dirs", []),
                            int(active.get("config", {}).get("detail_limit_per_lane") or DEFAULT_SCOUT_DETAIL_LIMIT),
                        )
                        row["new_offer_ids"] = sorted(set(row.get("new_offer_ids", [])) | set(keys))
                        row["detail_queue"] = keys
                        row["counts"]["new"] = len(row["new_offer_ids"])
                        row["counts"]["promising"] = len(keys)
                        row["status"] = "verifying" if keys else "complete"
                        row["message"] = (
                            f"Automatically verifying {len(keys)} strongest product{'s' if len(keys) != 1 else ''}."
                            if keys
                            else "Coverage finished; no products qualified for supplier verification."
                        )
                        break
                mutate_scout_job(job_id, finish_search)

            snapshot = scout_snapshot()
            job = snapshot.get("active_job", {})
            lane = job.get("lanes", [])[lane_index]
            detail_queue = list(lane.get("detail_queue", []))
            detail_cursor = int(lane.get("detail_cursor") or 0)
            while detail_cursor < len(detail_queue):
                browser = chrome_browser_status()
                if not browser.get("ok"):
                    mark_scout_waiting(job_id, lane_id, clean(browser.get("message")))
                    return
                key = clean(detail_queue[detail_cursor])
                result = scout_detail_once(key)
                if result.get("status") == "waiting_for_user":
                    mark_scout_waiting(job_id, lane_id, clean(result.get("message")))
                    return
                detail_cursor += 1

                def record_detail(active: dict[str, Any], _state: dict[str, Any], value: int = detail_cursor, offer_key: str = key, detail: dict[str, Any] = result) -> None:
                    for row in active.get("lanes", []):
                        if row.get("id") != lane_id:
                            continue
                        row["detail_cursor"] = value
                        row.setdefault("detail_results", {})[offer_key] = detail
                        tier = clean(detail.get("tier"))
                        if tier == "verified":
                            row["counts"]["verified"] += 1
                            if offer_key not in active["verified_keys"]:
                                active["verified_keys"].append(offer_key)
                        elif tier == "promising":
                            if offer_key not in active["promising_keys"]:
                                active["promising_keys"].append(offer_key)
                        else:
                            row["counts"]["rejected"] += 1
                            if offer_key not in active["rejected_keys"]:
                                active["rejected_keys"].append(offer_key)
                        break
                mutate_scout_job(job_id, record_detail)

            def finish_lane(active: dict[str, Any], _state: dict[str, Any]) -> None:
                for row in active.get("lanes", []):
                    if row.get("id") == lane_id:
                        row["status"] = "complete"
                        row["outcome"] = row.get("outcome") or "complete"
                        row["message"] = (
                            f"Complete: {row['counts']['verified']} verified, "
                            f"{row['counts']['promising']} nominated for checking, {row['counts']['rejected']} filtered after detail proof."
                        )
                        break
                active.setdefault("cursor", {})["lane_index"] = int(active.get("cursor", {}).get("lane_index") or 0) + 1
                active["message"] = f"Completed {active['cursor']['lane_index']} of {len(active.get('lanes', []))} lanes."
            mutate_scout_job(job_id, finish_lane)

        def finish_job(job: dict[str, Any], state: dict[str, Any]) -> None:
            partial = any(clean(lane.get("outcome")) == "partial" for lane in job.get("lanes", []))
            job.update(
                {
                    "status": "complete",
                    "outcome": "partial" if partial else "complete",
                    "requires_user": False,
                    "completed_at": now_iso(),
                    "message": (
                        f"Scout complete: {len(job.get('verified_keys', []))} verified opportunities, "
                        f"{len(job.get('promising_keys', []))} still promising, "
                        f"{len(job.get('rejected_keys', []))} filtered after supplier checks."
                    ),
                }
            )
            schedule = state.get("schedule", {})
            schedule["last_run_at"] = job["completed_at"]
            if schedule.get("enabled"):
                interval = int(schedule.get("interval_hours") or DEFAULT_SCOUT_INTERVAL_HOURS)
                schedule["next_run_at"] = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=interval)).isoformat()
            history = state.setdefault("history", [])
            history.append(
                {
                    "id": job.get("id"),
                    "completed_at": job.get("completed_at"),
                    "outcome": job.get("outcome"),
                    "verified": len(job.get("verified_keys", [])),
                    "promising": len(job.get("promising_keys", [])),
                    "filtered": len(job.get("rejected_keys", [])),
                }
            )
            del history[:-20]
        mutate_scout_job(job_id, finish_job)
    finally:
        SCOUT_WORKER_LOCK.release()
        SCOUT_THREADS.pop(job_id, None)


def launch_scout_worker(job_id: str) -> None:
    if not job_id:
        return
    if clean(os.environ.get("DLM_SCOUT_WORKER_DISABLED")).lower() in {"1", "true", "yes"}:
        return
    existing = SCOUT_THREADS.get(job_id)
    if existing and existing.is_alive():
        return
    thread = threading.Thread(target=run_scout_job, args=(job_id,), daemon=True, name=f"opportunity-scout-{job_id}")
    SCOUT_THREADS[job_id] = thread
    thread.start()


def scout_scheduler_loop() -> None:
    while True:
        try:
            snapshot = scout_snapshot()
            job = snapshot.get("active_job", {})
            status = clean(job.get("status"))
            if status in {"queued", "running"}:
                launch_scout_worker(clean(job.get("id")))
            elif status == "waiting_for_user" and chrome_browser_status().get("ok"):
                launch_scout_worker(clean(job.get("id")))
            elif status not in {"queued", "running", "waiting_for_user"}:
                schedule = snapshot.get("schedule", {})
                if schedule.get("enabled"):
                    due_text = clean(schedule.get("next_run_at"))
                    try:
                        due = not due_text or dt.datetime.fromisoformat(due_text.replace("Z", "+00:00")) <= dt.datetime.now(dt.timezone.utc)
                    except ValueError:
                        due = True
                    if due:
                        start_scout_job(schedule, scheduled=True)
        except Exception:
            pass
        time.sleep(5)


def start_scout_scheduler() -> threading.Thread:
    thread = threading.Thread(target=scout_scheduler_loop, daemon=True, name="opportunity-scout-scheduler")
    thread.start()
    return thread


def build_listing_prompt(candidate: dict[str, Any]) -> str:
    title = clean(candidate.get("title"))
    evidence = candidate.get("evidence", {})
    size_chart_source = clean(evidence.get("size_chart_source")) or "attached image"
    generated_images = clean(evidence.get("generated_images_path"))
    vendor_images = clean(evidence.get("vendor_images_path"))
    image_note = ""
    if generated_images:
        image_note = f" Generated Shopify images path: {generated_images}."
    elif vendor_images:
        image_note = f" Vendor image evidence path: {vendor_images}."
    notes = (
        f"Sourcing category: {candidate.get('category_label')}; "
        f"market focus: {candidate.get('market_label', 'Balanced')}; "
        f"score {candidate.get('score')}; verdict {candidate.get('verdict')}. "
        f"Product title: {title}. Confirm size chart, images, dropship support, "
        f"dispatch speed, and supplier evidence before draft creation or any later publishing.{image_note}"
    )
    return "\n".join(
        [
            "You are working in the dresslikemommy repository.",
            "",
            "Before doing any listing work, read these files in order:",
            "1. ops/prompts/START-HERE.md",
            "2. ops/prompts/shopify-listing-master-prompt.md",
            "3. ops/prompts/shopify-listing-from-1688.md",
            "",
            "Then execute the canonical Shopify listing workflow from those files for this request:",
            "",
            "Create or update a Shopify DRAFT product only. Do not set the product ACTIVE, call publishablePublish, or publish to any sales channel unless the operator explicitly asks for a separate publish-live action.",
            "Set Shopify Cost per item on every variant to exactly 50% of its selling price; if any cost is missing after verification, report paid_eligible=false and keep the product in DRAFT.",
            "",
            "LISTING REQUEST",
            "",
            f"VENDOR_URL: {candidate.get('product_url', '')}",
            f"SIZE_CHART_SOURCE: {size_chart_source}",
            f"LISTING_MODE: {candidate.get('listing_mode', 'Family Matching')}",
            "PRIMARY_CATEGORY: auto",
            "DESIGNS_TO_LIST: auto",
            "EXCLUDE_ITEMS:",
            f"NOTES: {notes}",
            "PRICE_OVERRIDES:",
            "SHORTCODE_OVERRIDE:",
            "COLOR_TOKEN_OVERRIDE:",
            "FORCE_SPEC_PRICES: true",
        ]
    )


def build_photoshoot_prompt(candidate: dict[str, Any]) -> str:
    template = PHOTOSHOOT_PROMPT_PATH.read_text(encoding="utf-8")
    context = "\n".join(
        [
            "PRODUCT CONTEXT FOR THIS LISTING",
            f"Vendor URL: {candidate.get('product_url', '')}",
            f"Detected category: {candidate.get('category_label', '')}",
            f"Listing mode: {candidate.get('listing_mode', '')}",
            f"Product title: {candidate.get('title', '')}",
            "",
            "Upload the vendor product images first, then use the prompt below.",
            "",
        ]
    )
    return context + template


def build_draft_agent_prompt(candidate: dict[str, Any]) -> str:
    evidence = candidate.get("evidence", {})
    package_path = str(package_dir_for_key(candidate["key"]).relative_to(REPO_ROOT))
    ready = draft_handoff_ready(candidate)
    missing_labels = [item["label"] for item in preparation_missing(candidate)]
    return "\n".join(
        [
            "You are working in /Users/fsuels/Projects/dresslikemommy.",
            "",
            "Read these files first:",
            "1. ops/prompts/START-HERE.md",
            "2. ops/prompts/shopify-listing-master-prompt.md",
            "3. ops/prompts/shopify-listing-from-1688.md",
            "",
            "Create a Shopify DRAFT product only. Do not publish live until the operator asks.",
            "Use the evidence package below as the source of truth:",
            f"PACKAGE_DIR: {package_path}",
            f"READY_FOR_SHOPIFY_DRAFT: {str(ready).lower()}",
            f"UNRESOLVED_PROOF: {'; '.join(missing_labels) if missing_labels else 'none'}",
            (
                "STOP: This is a preparation package only. Do not create or update a Shopify product until READY_FOR_SHOPIFY_DRAFT is true."
                if not ready
                else "The evidence gate is complete; proceed with the canonical DRAFT-only workflow and verify every field."
            ),
            "",
            "Evidence paths:",
            f"- Size chart source: {evidence.get('size_chart_source', '')}",
            f"- Vendor images: {evidence.get('vendor_images_path', '')}",
            f"- Generated Shopify images: {evidence.get('generated_images_path', '')}",
            f"- Detail notes: {evidence.get('notes', '')}",
            "",
            "Required behavior:",
            "- Parse the size chart into SIZE_CHART JSON before creating variants.",
            "- Use generated Shopify images if present; otherwise use the best vendor images only for draft review.",
            "- Create or update only a DRAFT product in Shopify.",
            "- Attach images to the draft product.",
            "- Set Cost per item on every variant to price x 50%.",
            "- Verify the draft product in Shopify Admin and save verification artifacts.",
            "",
            "Listing request:",
            build_listing_prompt(candidate),
        ]
    )


def create_draft_package(candidate: dict[str, Any]) -> Path:
    package_dir = package_dir_for_key(candidate["key"])
    evidence = candidate.get("evidence", {})
    metadata = {
        "created_at": now_iso(),
        "offer_key": candidate["key"],
        "candidate": candidate,
        "evidence": evidence,
        "ready_for_draft": draft_handoff_ready(candidate),
        "unresolved_proof": preparation_missing(candidate),
    }
    write_json(package_dir / "candidate.json", metadata)
    write_text(package_dir / "listing-request.txt", build_listing_prompt(candidate))
    write_text(package_dir / "photoshoot-prompt.md", build_photoshoot_prompt(candidate))
    write_text(package_dir / "draft-agent-prompt.md", build_draft_agent_prompt(candidate))
    write_text(
        package_dir / "README.md",
        "\n".join(
            [
                "# Draft Package",
                "",
                f"Vendor URL: {candidate.get('product_url', '')}",
                f"Category: {candidate.get('category_label', '')}",
                f"Listing mode: {candidate.get('listing_mode', '')}",
                f"Ready for draft: {draft_handoff_ready(candidate)}",
                "",
                (
                    "Use `draft-agent-prompt.md` to create a Shopify DRAFT product with images."
                    if draft_handoff_ready(candidate)
                    else "Preparation only: resolve every item in `candidate.json` under `unresolved_proof` before running `draft-agent-prompt.md`."
                ),
                "Do not publish live until the operator explicitly asks.",
            ]
        ),
    )
    return package_dir


def dashboard_html() -> str:
    if DASHBOARD_TEMPLATE_PATH.exists():
        return DASHBOARD_TEMPLATE_PATH.read_text(encoding="utf-8")
    return r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dress Like Mommy Sourcing</title>
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%232f6f5e'/%3E%3Cpath d='M18 39h28M22 25h20M27 49h10' stroke='white' stroke-width='6' stroke-linecap='round'/%3E%3C/svg%3E">
  <style>
    :root {
      --bg: #f5f7f6;
      --panel: #ffffff;
      --ink: #1f2523;
      --muted: #69746e;
      --line: #d8ded9;
      --accent: #c45d45;
      --green: #2f6f5e;
      --green-bg: #e3f3ec;
      --red: #a6423b;
      --red-bg: #ffe3df;
      --gold-bg: #fff3ce;
      --test-bg: #dff4f1;
      --shadow: 0 18px 45px rgba(31, 37, 35, .1);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
    }
    header {
      padding: 24px clamp(18px, 4vw, 44px) 18px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #fbfdfb 0%, var(--bg) 100%);
    }
    .top {
      display: flex;
      gap: 18px;
      justify-content: space-between;
      align-items: end;
      flex-wrap: wrap;
    }
    h1 {
      margin: 0;
      font-size: clamp(28px, 3vw, 42px);
      line-height: 1.05;
      letter-spacing: 0;
    }
    .sub {
      margin: 9px 0 0;
      color: var(--muted);
      max-width: 980px;
      line-height: 1.45;
    }
    .runbox {
      max-width: 430px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }
    .runbox strong {
      display: block;
      color: var(--ink);
      font-size: 14px;
      margin-bottom: 4px;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(7, minmax(105px, 1fr));
      gap: 10px;
      margin-top: 18px;
    }
    .stat {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
    }
    .stat span {
      display: block;
      color: var(--muted);
      font-size: 12px;
    }
    .stat em {
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-size: 11px;
      font-style: normal;
      line-height: 1.25;
    }
    .stat strong {
      display: block;
      margin-top: 4px;
      font-size: 24px;
    }
    .toolbar {
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
      padding: 12px clamp(18px, 4vw, 44px);
      background: rgba(245, 247, 246, .95);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(12px);
    }
    input, button, select, .button {
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      font: inherit;
    }
    input {
      flex: 1 1 280px;
      min-width: 220px;
      padding: 0 12px;
      background: #fff;
      color: var(--ink);
    }
    button, .button, select {
      padding: 0 12px;
      background: #fff;
      color: var(--ink);
      cursor: pointer;
    }
    button:disabled, .button.disabled {
      opacity: .56;
      cursor: not-allowed;
    }
    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      font-weight: 750;
    }
    .primary {
      background: var(--ink);
      color: #fff;
      border-color: var(--ink);
    }
    .chip.active {
      border-color: var(--accent);
      background: #fff1ec;
      color: #7b301f;
    }
    .categories {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 14px clamp(18px, 4vw, 44px);
      border-bottom: 1px solid var(--line);
      background: #fff;
    }
    .category.active {
      background: var(--green-bg);
      border-color: var(--green);
      color: var(--green);
    }
    main {
      padding: 22px clamp(18px, 4vw, 44px) 52px;
    }
    .guide {
      display: grid;
      grid-template-columns: minmax(280px, 1.35fr) minmax(280px, .9fr);
      gap: 14px;
      margin-bottom: 18px;
    }
    .guide-panel {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 16px;
      box-shadow: 0 10px 24px rgba(31, 37, 35, .06);
    }
    .guide-panel h3 {
      margin: 0 0 10px;
      font-size: 17px;
      letter-spacing: 0;
    }
    .steps {
      display: grid;
      grid-template-columns: repeat(5, minmax(110px, 1fr));
      gap: 8px;
    }
    .step {
      min-height: 92px;
      padding: 10px;
      border: 1px solid #e2e8e4;
      border-radius: 8px;
      background: #f7faf8;
    }
    .step strong {
      display: block;
      margin-bottom: 5px;
      font-size: 13px;
    }
    .step span {
      display: block;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }
    .search-panel {
      display: grid;
      gap: 9px;
    }
    .search-panel .row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .market-control {
      display: grid;
      gap: 5px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }
    .market-control select {
      width: 100%;
      min-height: 38px;
      color: var(--ink);
      font-weight: 500;
    }
    .status-box {
      min-height: 46px;
      padding: 10px;
      border: 1px solid #e2e8e4;
      border-radius: 8px;
      background: #f7faf8;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
    }
    .status-box.good {
      color: var(--green);
      background: var(--green-bg);
      border-color: rgba(47,111,94,.28);
    }
    .status-box.bad {
      color: var(--red);
      background: var(--red-bg);
      border-color: rgba(166,66,59,.28);
    }
    .detail-status {
      margin: -4px 0 10px;
      min-height: 0;
      font-size: 12px;
    }
    .search-plan {
      display: grid;
      gap: 8px;
      padding: 10px;
      border: 1px solid #e2e8e4;
      border-radius: 8px;
      background: #f7faf8;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }
    .search-plan strong {
      color: var(--ink);
    }
    .query-list {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 0;
      padding: 0;
      list-style: none;
    }
    .query-list li {
      padding: 5px 7px;
      border: 1px solid #dce4df;
      border-radius: 999px;
      background: #fff;
      color: var(--ink);
      font-size: 12px;
    }
    .memory-panel {
      display: grid;
      gap: 12px;
      margin-bottom: 18px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      box-shadow: 0 10px 24px rgba(31, 37, 35, .06);
    }
    .memory-top {
      display: flex;
      justify-content: space-between;
      gap: 14px;
      align-items: start;
      flex-wrap: wrap;
    }
    .memory-top h3 {
      margin: 0 0 5px;
      font-size: 17px;
      letter-spacing: 0;
    }
    .memory-top p {
      margin: 0;
      max-width: 760px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }
    .memory-status {
      min-height: 30px;
      display: inline-flex;
      align-items: center;
      padding: 5px 9px;
      border: 1px solid #dce4df;
      border-radius: 999px;
      background: #f7faf8;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }
    .memory-status.good {
      color: var(--green);
      background: var(--green-bg);
      border-color: rgba(47,111,94,.28);
    }
    .memory-status.bad {
      color: var(--red);
      background: var(--red-bg);
      border-color: rgba(166,66,59,.28);
    }
    .memory-form {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .memory-form input {
      min-width: min(100%, 420px);
    }
    .memory-examples {
      display: flex;
      gap: 7px;
      flex-wrap: wrap;
    }
    .memory-examples button {
      min-height: 32px;
      font-size: 12px;
      color: var(--green);
      border-color: rgba(47,111,94,.28);
      background: var(--green-bg);
    }
    .memory-results {
      display: grid;
      gap: 10px;
    }
    .memory-answer {
      display: grid;
      gap: 8px;
      padding: 14px;
      border: 1px solid rgba(47,111,94,.28);
      border-radius: 8px;
      background: var(--green-bg);
      color: var(--ink);
    }
    .memory-answer h4 {
      margin: 0;
      font-size: 16px;
      letter-spacing: 0;
    }
    .memory-answer p {
      margin: 0;
      color: #24433a;
      font-size: 14px;
      line-height: 1.45;
    }
    .memory-answer ol {
      margin: 4px 0 0;
      padding-left: 22px;
      color: #24433a;
      font-size: 14px;
      line-height: 1.45;
    }
    .memory-answer li + li {
      margin-top: 3px;
    }
    .memory-note {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
    }
    .memory-details {
      display: grid;
      gap: 10px;
    }
    .memory-details summary {
      cursor: pointer;
      color: var(--muted);
      font-size: 13px;
      font-weight: 800;
    }
    .memory-details[open] summary {
      margin-bottom: 10px;
    }
    .memory-empty {
      padding: 12px;
      border: 1px dashed var(--line);
      border-radius: 8px;
      background: #f7faf8;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }
    .memory-card {
      display: grid;
      gap: 8px;
      padding: 12px;
      border: 1px solid #e2e8e4;
      border-radius: 8px;
      background: #f7faf8;
    }
    .memory-card-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: start;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }
    .memory-card-head strong {
      display: block;
      color: var(--ink);
      font-size: 13px;
    }
    .memory-score {
      color: var(--accent);
      font-weight: 900;
      white-space: nowrap;
    }
    .memory-snippet {
      max-height: 220px;
      overflow: auto;
      padding: 10px;
      border: 1px solid #dce4df;
      border-radius: 8px;
      background: #fff;
      color: var(--ink);
      font-size: 13px;
      line-height: 1.45;
      white-space: pre-wrap;
    }
    .memory-card button {
      justify-self: start;
      min-height: 32px;
      font-size: 12px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 18px;
      align-items: start;
    }
    .card {
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--shadow);
    }
    .card.rejected {
      opacity: .62;
      background: #f0f2f1;
    }
    .card.kept {
      border-color: var(--green);
      box-shadow: 0 0 0 3px rgba(47,111,94,.16), var(--shadow);
    }
    .image {
      position: relative;
      aspect-ratio: 4 / 3;
      background: #e7ece9;
      overflow: hidden;
    }
    .image img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .badge {
      position: absolute;
      top: 12px;
      left: 12px;
      min-height: 28px;
      display: inline-flex;
      align-items: center;
      padding: 4px 10px;
      border-radius: 999px;
      font-weight: 850;
      font-size: 12px;
      border: 1px solid rgba(255,255,255,.75);
      background: var(--test-bg);
      color: #135b5a;
    }
    .badge.Gold { background: var(--gold-bg); color: #6f4d07; }
    .badge.Reject { background: var(--red-bg); color: #7a211b; }
    .body {
      padding: 14px;
    }
    .decision-row, .actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 11px;
    }
    .keep.active {
      background: var(--green-bg);
      border-color: var(--green);
      color: var(--green);
      font-weight: 850;
    }
    .reject.active {
      background: var(--red-bg);
      border-color: var(--red);
      color: var(--red);
      font-weight: 850;
    }
    .meta {
      display: flex;
      gap: 12px;
      justify-content: space-between;
      align-items: start;
    }
    h2 {
      margin: 0;
      font-size: 17px;
      line-height: 1.25;
      letter-spacing: 0;
    }
    .small {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }
    .score {
      min-width: 52px;
      text-align: center;
      color: var(--accent);
      font-size: 28px;
      font-weight: 900;
      line-height: 1;
    }
    .metrics {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin: 12px 0;
    }
    .metric {
      padding: 8px;
      border: 1px solid #e2e8e4;
      border-radius: 8px;
      background: #f7faf8;
      min-width: 0;
    }
    .metric span {
      display: block;
      color: var(--muted);
      font-size: 11px;
    }
    .metric strong {
      display: block;
      margin-top: 2px;
      overflow-wrap: anywhere;
    }
    .why {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
      min-height: 38px;
    }
    .signal-block {
      display: grid;
      gap: 8px;
      margin: 12px 0;
    }
    .signal {
      padding: 9px;
      border-radius: 8px;
      border: 1px solid #e2e8e4;
      background: #f7faf8;
      font-size: 13px;
      line-height: 1.35;
      color: var(--muted);
    }
    .signal strong {
      color: var(--ink);
    }
    .evidence {
      display: grid;
      gap: 7px;
      margin: 12px 0;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f7faf8;
    }
    .evidence-title {
      display: flex;
      justify-content: space-between;
      gap: 8px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }
    .ready-pill {
      color: var(--green);
    }
    .evidence input, .evidence textarea {
      width: 100%;
      min-height: 34px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 7px 9px;
      font: inherit;
      font-size: 13px;
      background: #fff;
      color: var(--ink);
    }
    .evidence textarea {
      min-height: 58px;
      resize: vertical;
    }
    .evidence-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 7px;
    }
    .empty {
      display: none;
      padding: 34px;
      border: 1px dashed var(--line);
      border-radius: 8px;
      color: var(--muted);
      background: #fff;
    }
    @media (max-width: 760px) {
      .stats { grid-template-columns: repeat(2, 1fr); }
      .guide { grid-template-columns: 1fr; }
      .steps { grid-template-columns: 1fr; }
      .memory-form input, .memory-form button { width: 100%; }
      .grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <div class="top">
      <div>
        <h1>Dress Like Mommy Sourcing</h1>
        <p class="sub">Find matching-family products on 1688, save only the good ones, remember rejects forever, and prepare draft listing packages with the right prompts and image workflow.</p>
      </div>
      <div class="runbox">
        <strong>Plain English:</strong>
        Click <b>Find 20 Leads</b>. The app searches normal logged-in 1688 pages, fills the shortlist with promising products, then blocks drafts until detail proof is verified.
      </div>
    </div>
    <div class="stats">
      <div class="stat"><span>Stored Cards</span><strong id="stat-total">0</strong><em>Raw cards saved locally.</em></div>
      <div class="stat"><span>Buyer Shortlist</span><strong id="stat-active">0</strong><em>Fresh, category-fit leads only.</em></div>
      <div class="stat"><span>Saved</span><strong id="stat-kept">0</strong><em>You clicked Keep.</em></div>
      <div class="stat"><span>Ready for Draft</span><strong id="stat-ready">0</strong><em>Proof is filled in.</em></div>
      <div class="stat"><span>Rejected</span><strong id="stat-rejected">0</strong><em>Remembered so we do not repeat work.</em></div>
      <div class="stat"><span>Best Leads</span><strong id="stat-gold">0</strong><em>Strong enough to prioritize.</em></div>
      <div class="stat"><span>Unverified Leads</span><strong id="stat-test">0</strong><em>Fresh leads needing supplier proof.</em></div>
    </div>
  </header>
  <nav class="categories" id="categories"></nav>
  <div class="toolbar">
    <input id="search" type="search" placeholder="Search product title, supplier, badge, raw text">
    <button class="chip active" data-filter="active">Buyer Shortlist</button>
    <button class="chip" data-filter="kept">Saved</button>
    <button class="chip" data-filter="ready">Ready for Draft</button>
    <button class="chip" data-filter="rejected">Rejected</button>
    <button class="chip" data-filter="gold">Best Leads</button>
    <button class="chip" data-filter="test">Unverified Leads</button>
    <button class="chip" data-filter="all">All</button>
    <select id="sort">
      <option value="score-desc">Score high to low</option>
      <option value="category">Category</option>
      <option value="newest">Newest run</option>
    </select>
    <button id="refresh">Refresh View</button>
  </div>
  <main>
    <section class="guide">
      <div class="guide-panel">
        <h3>How this is supposed to work</h3>
        <div class="steps">
          <div class="step"><strong>1. Find</strong><span>The app searches 1688 by category and collects product cards.</span></div>
          <div class="step"><strong>2. Review</strong><span>You look at images, price, MOQ, sales, repeat rate, and risks.</span></div>
          <div class="step"><strong>3. Keep or Reject</strong><span>Rejects are remembered so we do not waste time again.</span></div>
          <div class="step"><strong>4. Verify Proof</strong><span>Use Verify Detail Proof to collect supplier, size chart, dropship, dispatch, and image evidence.</span></div>
          <div class="step"><strong>5. Draft</strong><span>Create a draft package for the listing and 6-image workflow.</span></div>
        </div>
      </div>
      <div class="guide-panel search-panel">
        <h3>Find new products</h3>
        <label class="market-control">
          <span>Market focus</span>
          <select id="market-focus"></select>
        </label>
        <div class="row">
          <button id="find-products" class="primary">Find 20 Leads</button>
          <button id="open-1688">Open 1688 Login/Search</button>
        </div>
        <div id="search-plan" class="search-plan"></div>
        <div id="collector-status" class="status-box">Choose a category above, then click Find 20 Leads. The app rotates occasion keyword searches with configured launch-year and season terms, checks up to two pages per query, and skips offers already saved locally. If 1688 asks for login or CAPTCHA, use Open 1688 Login/Search once, complete the browser check, then click Find again.</div>
      </div>
    </section>
    <section class="memory-panel" aria-labelledby="memory-title">
      <div class="memory-top">
        <div>
          <h3 id="memory-title">Ask project memory</h3>
          <p>Ask normal questions about this sourcing system, listing workflow, proof gates, prompts, or past decisions. Results come from the curated local memory pilot, not the live website.</p>
        </div>
        <span id="memory-status" class="memory-status">Checking memory</span>
      </div>
      <form id="memory-form" class="memory-form">
        <input id="memory-query" type="search" placeholder="Ask: What do I do when 1688 shows CAPTCHA?">
        <button id="memory-search" class="primary" type="submit">Search Memory</button>
      </form>
      <div class="memory-examples">
        <button type="button" data-memory-query="What do I do when 1688 shows CAPTCHA?">1688 is blocked</button>
        <button type="button" data-memory-query="Where do Keep and Reject decisions live?">Keep and Reject memory</button>
        <button type="button" data-memory-query="What proof is required before Ready for Draft?">Ready proof fields</button>
        <button type="button" data-memory-query="Which prompts must be read before creating a 1688 Shopify listing?">Listing prompts</button>
        <button type="button" data-memory-query="What is the latest sourcing dashboard state?">Latest dashboard state</button>
      </div>
      <div id="memory-results" class="memory-results">
        <div class="memory-empty">Type a question or click one of the quick questions above.</div>
      </div>
    </section>
    <div id="empty" class="empty">No candidates match this view.</div>
    <div id="grid" class="grid"></div>
  </main>
  <script>
    let data = { categories: [], market_profiles: [], candidates: [], counts: {} };
    let activeCategory = 'all';
    let activeFilter = 'active';
    let activeMarket = 'balanced';
    let searchTerm = '';

    const grid = document.querySelector('#grid');
    const empty = document.querySelector('#empty');
    const categoriesEl = document.querySelector('#categories');
    const search = document.querySelector('#search');
    const sort = document.querySelector('#sort');
    const marketFocus = document.querySelector('#market-focus');
    const collectorStatus = document.querySelector('#collector-status');
    const searchPlan = document.querySelector('#search-plan');
    const memoryStatus = document.querySelector('#memory-status');
    const memoryForm = document.querySelector('#memory-form');
    const memoryQuery = document.querySelector('#memory-query');
    const memorySearchButton = document.querySelector('#memory-search');
    const memoryResults = document.querySelector('#memory-results');

    async function api(path, options = {}) {
      const response = await fetch(path, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
      });
      if (!response.ok) throw new Error(await response.text());
      return response.json();
    }

    async function copyText(text) {
      if (navigator.clipboard?.writeText && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(text);
          return;
        } catch {}
      }
      const area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.left = '-9999px';
      document.body.appendChild(area);
      area.select();
      document.execCommand('copy');
      area.remove();
    }

    function flash(button, text) {
      const old = button.textContent;
      button.textContent = text;
      setTimeout(() => button.textContent = old, 1200);
    }

    function escapeHtml(value) {
      return String(value ?? '').replace(/[&<>"']/g, char => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
      }[char]));
    }

    function metric(label, value) {
      return `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value || '-')}</strong></div>`;
    }

    function asList(value) {
      if (Array.isArray(value)) return value.filter(Boolean);
      if (!value) return [];
      return String(value).split('|').map(item => item.trim()).filter(Boolean);
    }

    function shortList(value, fallback) {
      const items = asList(value).slice(0, 4);
      return items.length ? items.join('; ') : fallback;
    }

    function imageSrc(url) {
      return url ? `/image?url=${encodeURIComponent(url)}` : '';
    }

    function verdictLabel(verdict) {
      if (verdict === 'Gold') return 'Best lead';
      if (verdict === 'Test') return 'Unverified lead';
      if (verdict === 'Reject') return 'Auto rejected';
      return verdict || 'Review';
    }

    function setCollectorStatus(message, mode = '') {
      collectorStatus.textContent = message;
      collectorStatus.className = `status-box ${mode}`.trim();
    }

    function setMemoryStatus(message, mode = '') {
      memoryStatus.textContent = message;
      memoryStatus.className = `memory-status ${mode}`.trim();
    }

    function renderMemoryResults(payload) {
      if (!payload.ok) {
        memoryResults.innerHTML = `<div class="memory-empty">${escapeHtml(payload.message || 'Project Memory is not ready yet.')}</div>`;
        return;
      }
      const results = payload.results || [];
      const answer = payload.answer || {
        title: 'Memory search finished',
        summary: results.length ? 'I found related memory notes.' : 'No memory notes matched. Try a simpler phrase.',
        steps: [],
        note: ''
      };
      const answerSteps = (answer.steps || []).map(step => `<li>${escapeHtml(step)}</li>`).join('');
      const answerHtml = `
        <section class="memory-answer">
          <h4>${escapeHtml(answer.title || 'Plain answer')}</h4>
          <p>${escapeHtml(answer.summary || '')}</p>
          ${answerSteps ? `<ol>${answerSteps}</ol>` : ''}
          ${answer.note ? `<div class="memory-note">${escapeHtml(answer.note)}</div>` : ''}
          <button type="button" class="copy-memory-answer">Copy plain answer</button>
        </section>
      `;
      const detailCards = results.map(result => `
        <article class="memory-card">
          <div class="memory-card-head">
            <div>
              <strong>${escapeHtml(result.source || 'Memory note')}</strong>
              <span>${escapeHtml(result.location || 'dresslikemommy-pilot')}</span>
            </div>
            <span class="memory-score">${result.score == null ? '' : escapeHtml(Number(result.score).toFixed(3))}</span>
          </div>
          <div class="memory-snippet">${escapeHtml(result.snippet || '')}</div>
          <button type="button" class="copy-memory">Copy this result</button>
        </article>
      `).join('');
      memoryResults.innerHTML = `
        ${answerHtml}
        ${results.length ? `<details class="memory-details"><summary>Show source details for verification</summary>${detailCards}</details>` : ''}
      `;
      memoryResults.querySelector('.copy-memory-answer')?.addEventListener('click', async event => {
        const text = [
          answer.title || 'Plain answer',
          answer.summary || '',
          ...(answer.steps || []).map((step, index) => `${index + 1}. ${step}`),
          answer.note || '',
        ].filter(Boolean).join('\\n');
        await copyText(text);
        flash(event.currentTarget, 'Copied');
      });
      memoryResults.querySelectorAll('.copy-memory').forEach((button, index) => {
        button.addEventListener('click', async () => {
          const result = results[index];
          await copyText(`${result.source || 'Memory note'}\n\n${result.snippet || ''}`);
          flash(button, 'Copied');
        });
      });
    }

    async function loadMemoryStatus() {
      try {
        const status = await api('/api/memory-status');
        setMemoryStatus(status.message || 'Memory ready', status.available ? 'good' : 'bad');
      } catch (error) {
        setMemoryStatus('Memory status unavailable', 'bad');
      }
    }

    async function searchMemory(query) {
      const text = query.trim();
      if (!text) {
        memoryResults.innerHTML = '<div class="memory-empty">Type a question first.</div>';
        return;
      }
      memorySearchButton.disabled = true;
      const old = memorySearchButton.textContent;
      memorySearchButton.textContent = 'Searching...';
      setMemoryStatus('Searching memory');
      memoryResults.innerHTML = '<div class="memory-empty">Looking through the local project memory...</div>';
      try {
        const payload = await api('/api/memory-search', {
          method: 'POST',
          body: JSON.stringify({ query: text, results: 5 }),
        });
        setMemoryStatus(payload.status?.message || payload.message || 'Memory search finished', payload.ok ? 'good' : 'bad');
        renderMemoryResults(payload);
      } catch (error) {
        setMemoryStatus('Memory search failed', 'bad');
        memoryResults.innerHTML = `<div class="memory-empty">I could not search memory: ${escapeHtml(error.message)}</div>`;
      } finally {
        memorySearchButton.disabled = false;
        memorySearchButton.textContent = old;
      }
    }

    function activeCategoryConfig() {
      return data.categories.find(category => category.id === activeCategory) || null;
    }

    function activeMarketProfile() {
      return (data.market_profiles || []).find(profile => profile.id === activeMarket)
        || (data.market_profiles || []).find(profile => profile.id === 'balanced')
        || { id: 'balanced', label: 'Balanced', short_label: 'Balanced', description: '', query_modifiers: [] };
    }

    function queryTerms(parts) {
      const seen = new Set();
      const terms = [];
      for (const part of parts) {
        const values = Array.isArray(part) ? part : [part];
        for (const value of values) {
          const text = String(value || '').trim();
          if (!text) continue;
          for (const term of text.split(/\s+/)) {
            if (!term || seen.has(term)) continue;
            seen.add(term);
            terms.push(term);
          }
        }
      }
      return terms.join(' ');
    }

    function queryDisplayText(query, category, marketProfile = activeMarketProfile()) {
      if (typeof query === 'string') return query;
      const defaults = category?.search_defaults || {};
      return queryTerms([
        query?.text,
        query?.launch_year || defaults.launch_year,
        query?.launch_season || query?.season || defaults.launch_season,
        query?.freshness || defaults.freshness,
        query?.modifiers || defaults.modifiers,
        marketProfile?.query_modifiers || [],
        query?.fulfillment || defaults.fulfillment,
      ]);
    }

    function renderSearchPlan() {
      const category = activeCategoryConfig();
      const marketProfile = activeMarketProfile();
      const queries = category
        ? (category.queries || []).map(query => queryDisplayText(query, category, marketProfile))
        : data.categories.flatMap(item => (item.queries || []).map(query => queryDisplayText(query, item, marketProfile))).slice(0, 8);
      const queryItems = queries.slice(0, 10).map(query => `<li>${escapeHtml(query)}</li>`).join('');
      const label = category ? category.label : 'All Categories';
      searchPlan.innerHTML = `
        <div><strong>What the button searches:</strong> ${escapeHtml(label)} keyword searches on normal 1688 search pages with ${escapeHtml(marketProfile.label || activeMarket)} focus. It rotates the starting query, uses configured launch year/season terms, and skips offers already saved locally.</div>
        <ul class="query-list">${queryItems}</ul>
        <div><strong>Market rule:</strong> ${escapeHtml(marketProfile.description || 'Use the base category searches.')}</div>
        <div><strong>What becomes Buyer Shortlist:</strong> correct category, usable product image, low MOQ, newer 1688 offer ID or visible 2025/2026/new-style wording, and a useful signal such as repeat rate, sales, stock, dispatch, or dropship wording. US/Europe focus requires stronger fresh-listing and reputable-vendor proof.</div>
        <div><strong>What gets hidden:</strong> previous reject, old 1688 offer ID, old year signal such as 2020-2024, wrong category, no product URL/image, high MOQ, no-dropship/no-size-chart evidence, brand/IP risk, or no useful demand/fulfillment signal.</div>
        <div><strong>Sales:</strong> the number visible on the 1688 search card. If 1688 does not show a time window, treat it as a popularity clue and confirm on the detail page.</div>
      `;
    }

    function visibleCandidates() {
      const term = searchTerm.trim().toLowerCase();
      let items = data.candidates.filter(item => activeCategory === 'all' || item.category_id === activeCategory);
      items = items.filter(item => {
        if (activeFilter === 'active') return item.decision !== 'reject' && item.verdict !== 'Reject';
        if (activeFilter === 'kept') return item.decision === 'keep';
        if (activeFilter === 'ready') return item.ready_for_draft && item.decision !== 'reject';
        if (activeFilter === 'rejected') return item.decision === 'reject';
        if (activeFilter === 'gold') return item.verdict === 'Gold' && item.decision !== 'reject';
        if (activeFilter === 'test') return item.verdict === 'Test' && item.decision !== 'reject';
        return true;
      });
      if (term) items = items.filter(item => item.search_text.includes(term));
      if (sort.value === 'category') items.sort((a, b) => a.category_label.localeCompare(b.category_label) || b.score - a.score);
      if (sort.value === 'score-desc') items.sort((a, b) => b.score - a.score);
      if (sort.value === 'newest') items.sort((a, b) => b.run_id.localeCompare(a.run_id) || b.score - a.score);
      return items;
    }

    function updateStats() {
      const items = activeCategory === 'all'
        ? data.candidates
        : data.candidates.filter(item => item.category_id === activeCategory);
      const stats = {
        total: items.length,
        active: items.filter(item => item.decision !== 'reject' && item.verdict !== 'Reject').length,
        kept: items.filter(item => item.decision === 'keep').length,
        ready: items.filter(item => item.ready_for_draft && item.decision !== 'reject').length,
        rejected: items.filter(item => item.decision === 'reject').length,
        gold: items.filter(item => item.verdict === 'Gold').length,
        test: items.filter(item => item.verdict === 'Test').length,
      };
      for (const [key, value] of Object.entries(stats)) {
        document.querySelector(`#stat-${key}`).textContent = String(value);
      }
    }

    function renderCategories() {
      const all = document.createElement('button');
      all.className = `category ${activeCategory === 'all' ? 'active' : ''}`;
      all.textContent = 'All Categories';
      all.addEventListener('click', () => { activeCategory = 'all'; render(); });
      categoriesEl.replaceChildren(all);
      for (const category of data.categories) {
        const count = data.counts[category.id]?.active || 0;
        const button = document.createElement('button');
        button.className = `category ${activeCategory === category.id ? 'active' : ''}`;
        button.textContent = `${category.label} (${count})`;
        button.addEventListener('click', () => { activeCategory = category.id; render(); });
        categoriesEl.appendChild(button);
      }
    }

    function renderMarketOptions() {
      const profiles = data.market_profiles?.length
        ? data.market_profiles
        : [{ id: 'balanced', label: 'Balanced', short_label: 'Balanced' }];
      const prior = activeMarket;
      marketFocus.replaceChildren(...profiles.map(profile => {
        const option = document.createElement('option');
        option.value = profile.id;
        option.textContent = profile.label || profile.id;
        return option;
      }));
      activeMarket = profiles.some(profile => profile.id === prior) ? prior : 'balanced';
      marketFocus.value = activeMarket;
    }

    async function pollCollection(jobId, button) {
      const started = Date.now();
      while (Date.now() - started < 20 * 60 * 1000) {
        const job = await api(`/api/collect-status?job=${encodeURIComponent(jobId)}`);
        if (job.status === 'complete') {
          await loadData();
          setCollectorStatus(`${job.message} New products are now in the review cards.`, 'good');
          flash(button, 'Done');
          return;
        }
        if (job.status === 'failed') {
          const detail = (job.stderr || '').split('\\n').filter(Boolean).pop() || '';
          const shortDetail = detail.length > 220 ? `${detail.slice(0, 220)}...` : detail;
          setCollectorStatus(`${job.message} ${shortDetail}`.trim(), 'bad');
          flash(button, 'Try again');
          return;
        }
        setCollectorStatus(`${job.message || 'Searching 1688...'} Trying rotated occasion searches and skipping already-seen offers; this can take 1-3 minutes.`);
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
      setCollectorStatus('The search is still running. Refresh the view in a minute.', 'bad');
    }

    async function findFreshProducts(button) {
      const category = activeCategory === 'all' ? 'all' : activeCategory;
      const marketProfile = activeMarketProfile();
      button.disabled = true;
      const old = button.textContent;
      button.textContent = 'Searching...';
      setCollectorStatus(`Checking 1688 browser status before searching.`);
      try {
        const browser = await api('/api/browser-status');
        if (!browser.ok) {
          setCollectorStatus(`${browser.message} Click Open 1688 Login/Search, complete the browser check, then try Find 20 Leads again.`, 'bad');
          flash(button, 'Blocked');
          return;
        }
        setCollectorStatus(`Searching 1688 for ${category === 'all' ? 'all categories' : category} with ${marketProfile.label || activeMarket} focus. I am aiming for 20 reviewable leads, rotating fresh-listing keywords, checking extra pages, skipping already-seen offers, and hiding weak supplier matches before they reach your shortlist.`);
        const job = await api('/api/collect', {
          method: 'POST',
          body: JSON.stringify({ category_id: category, market_target: activeMarket, limit: 200, query_index: -1, target_reviewable: 20, max_pages_per_query: 2 }),
        });
        await pollCollection(job.id, button);
      } catch (error) {
        setCollectorStatus(`I could not start the search: ${error.message}`, 'bad');
      } finally {
        button.disabled = false;
        button.textContent = old;
      }
    }

    async function open1688Helper(button) {
      const category = activeCategory === 'all' ? 'family-matching' : activeCategory;
      try {
        const payload = await api('/api/open-1688-browser', {
          method: 'POST',
          body: JSON.stringify({ category_id: category, market_target: activeMarket, query_index: -1 }),
        });
        setCollectorStatus(`Reused the 1688 helper tab with ${activeMarketProfile().label || activeMarket} focus. Login or clear CAPTCHA once if asked, then click Find 20 Leads. Search page: ${payload.url}`, 'good');
        flash(button, 'Opened');
      } catch (error) {
        setCollectorStatus(`Could not open Chrome helper: ${error.message}`, 'bad');
      }
    }

    async function setDecision(candidate, action, button) {
      const nextAction = candidate.decision === action ? 'clear' : action;
      await api('/api/decision', {
        method: 'POST',
        body: JSON.stringify({
          key: candidate.key,
          action: nextAction,
          product_url: candidate.product_url,
          title: candidate.title,
          category_id: candidate.category_id,
          run_id: candidate.run_id,
          verdict: candidate.verdict,
          score: candidate.score,
        }),
      });
      await loadData(false);
      flash(button, nextAction === 'clear' ? 'Cleared' : 'Saved');
    }

    async function copyPrompt(candidate, type, button) {
      const payload = await api(`/api/prompt?key=${encodeURIComponent(candidate.key)}&type=${encodeURIComponent(type)}`);
      await copyText(payload.prompt);
      flash(button, 'Copied');
    }

    async function saveEvidence(candidate, article, button) {
      const field = name => article.querySelector(`[data-evidence="${name}"]`)?.value || '';
      await api('/api/evidence', {
        method: 'POST',
        body: JSON.stringify({
          key: candidate.key,
          product_url: candidate.product_url,
          title: candidate.title,
          category_id: candidate.category_id,
          run_id: candidate.run_id,
          evidence: {
            size_chart_source: field('size_chart_source'),
            vendor_images_path: field('vendor_images_path'),
            generated_images_path: field('generated_images_path'),
            dropship_confirmed: field('dropship_confirmed'),
            dispatch_confirmed: field('dispatch_confirmed'),
            supplier_confirmed: field('supplier_confirmed'),
            notes: field('notes'),
          },
        }),
      });
      await loadData(false);
      flash(button, 'Saved');
    }

    function setCardStatus(article, message, mode = '') {
      const status = article.querySelector('.detail-status');
      if (!status) return;
      status.textContent = message;
      status.className = `status-box detail-status ${mode}`.trim();
    }

    async function pollDetailProof(jobId, article, button) {
      const started = Date.now();
      while (Date.now() - started < 12 * 60 * 1000) {
        const job = await api(`/api/detail-status?job=${encodeURIComponent(jobId)}`);
        if (job.status === 'complete') {
          setCardStatus(article, `${job.message} The card has been refreshed.`, 'good');
          await loadData(false);
          return;
        }
        if (job.status === 'failed') {
          const detail = (job.stderr || '').split('\\n').filter(Boolean).pop() || '';
          const shortDetail = detail.length > 220 ? `${detail.slice(0, 220)}...` : detail;
          setCardStatus(article, `${job.message} ${shortDetail}`.trim(), 'bad');
          return;
        }
        setCardStatus(article, job.message || 'Checking the 1688 detail page...');
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
      setCardStatus(article, 'Detail verification is still running. Refresh the view in a minute.', 'bad');
    }

    async function verifyDetailProof(candidate, article, button) {
      button.disabled = true;
      const old = button.textContent;
      button.textContent = 'Checking...';
      try {
        const browser = await api('/api/browser-status');
        if (!browser.ok) {
          setCardStatus(article, `${browser.message} Click Open 1688 Login/Search, complete the browser check, then try Verify Detail Proof again.`, 'bad');
          return;
        }
        setCardStatus(article, 'Opening the product detail page and saving proof from 1688.');
        const job = await api('/api/detail-enrich', {
          method: 'POST',
          body: JSON.stringify({ key: candidate.key }),
        });
        await pollDetailProof(job.id, article, button);
      } catch (error) {
        setCardStatus(article, `I could not start detail verification: ${error.message}`, 'bad');
      } finally {
        button.disabled = false;
        button.textContent = old;
      }
    }

    async function createDraftPackage(candidate, button) {
      if (!candidate.ready_for_draft) {
        flash(button, 'Needs proof');
        return;
      }
      const payload = await api('/api/draft-package', {
        method: 'POST',
        body: JSON.stringify({ key: candidate.key }),
      });
      await copyText(payload.agent_prompt);
      await loadData(false);
      flash(button, 'Package copied');
    }

    function card(candidate) {
      const article = document.createElement('article');
      article.className = `card ${candidate.decision === 'keep' ? 'kept' : ''} ${candidate.decision === 'reject' ? 'rejected' : ''}`;
      const positives = shortList(candidate.positive_signals, 'No strong signal captured yet.');
      const concerns = shortList(candidate.concerns, 'No major concern captured yet.');
      const evidence = candidate.evidence || {};
      const searchQuery = candidate.search_query ? `Search: ${candidate.search_query}` : 'Search keyword not captured';
      const salesContext = candidate.sales_context || '1688 did not show a clear sales time window on the search card.';
      const detailStatus = candidate.detail_proof_verified
        ? 'Detail proof saved from the 1688 product page.'
        : (candidate.detail_gate_note || 'Run detail proof before treating this as a Best Lead.');
      article.innerHTML = `
        <div class="image">
          ${candidate.image_url ? `<img loading="lazy" src="${escapeHtml(imageSrc(candidate.image_url))}" alt="${escapeHtml(candidate.title)}">` : ''}
          <div class="badge ${escapeHtml(candidate.verdict)}">${escapeHtml(verdictLabel(candidate.verdict))}</div>
        </div>
        <div class="body">
          <div class="decision-row">
            <button class="keep ${candidate.decision === 'keep' ? 'active' : ''}">${candidate.decision === 'keep' ? 'Saved' : 'Save'}</button>
            <button class="reject ${candidate.decision === 'reject' ? 'active' : ''}">${candidate.decision === 'reject' ? 'Restore' : 'Reject'}</button>
          </div>
          <div class="meta">
            <div>
              <div class="small">${escapeHtml(candidate.category_label)} - ${escapeHtml(candidate.run_id)}</div>
              <div class="small">Market: ${escapeHtml(candidate.market_label || candidate.market_target || 'Balanced')}</div>
              <div class="small">${escapeHtml(searchQuery)}</div>
              <h2>${escapeHtml(candidate.title || candidate.product_url)}</h2>
            </div>
            <div class="score">${escapeHtml(candidate.score)}</div>
          </div>
          <div class="metrics">
            ${metric('Price CNY', candidate.price_cny)}
            ${metric('MOQ', candidate.moq)}
            ${metric('Sales', candidate.monthly_sales)}
            ${metric('Repeat', candidate.repurchase_rate_pct)}
            ${metric('Rating', candidate.rating)}
            ${metric('Years', candidate.years_on_1688)}
          </div>
          <div class="signal"><strong>Sales meaning:</strong> ${escapeHtml(salesContext)}</div>
          <div class="signal"><strong>Detail proof:</strong> ${escapeHtml(detailStatus)}</div>
          <div class="signal-block">
            <div class="signal"><strong>Why it may be good:</strong> ${escapeHtml(positives)}</div>
            <div class="signal"><strong>What still needs checking:</strong> ${escapeHtml(concerns)}</div>
          </div>
          <div class="evidence">
            <div class="evidence-title">
              <span>Proof needed before Shopify draft</span>
              <span class="${candidate.ready_for_draft ? 'ready-pill' : ''}">${candidate.ready_for_draft ? 'Ready for draft' : 'Needs proof'}</span>
            </div>
            <input data-evidence="size_chart_source" value="${escapeHtml(evidence.size_chart_source || '')}" placeholder="Size chart screenshot/path or attached image note">
            <input data-evidence="vendor_images_path" value="${escapeHtml(evidence.vendor_images_path || '')}" placeholder="Vendor image folder/path">
            <input data-evidence="generated_images_path" value="${escapeHtml(evidence.generated_images_path || '')}" placeholder="Generated 6-image folder/path">
            <div class="evidence-grid">
              <input data-evidence="dropship_confirmed" value="${escapeHtml(evidence.dropship_confirmed || '')}" placeholder="Dropship yes">
              <input data-evidence="dispatch_confirmed" value="${escapeHtml(evidence.dispatch_confirmed || '')}" placeholder="Dispatch speed">
              <input data-evidence="supplier_confirmed" value="${escapeHtml(evidence.supplier_confirmed || '')}" placeholder="Supplier ok">
            </div>
            <textarea data-evidence="notes" placeholder="Your notes: colors to list, exclude items, quality concerns">${escapeHtml(evidence.notes || '')}</textarea>
          </div>
          <div class="status-box detail-status">${escapeHtml(detailStatus)}</div>
          <div class="actions">
            <a class="button primary" href="${escapeHtml(candidate.product_url)}" target="_blank" rel="noreferrer">Open 1688</a>
            <button class="verify-detail">${candidate.detail_proof_verified ? 'Verify Detail Again' : 'Verify Detail Proof'}</button>
            <button class="save-evidence">Save Proof</button>
            <button class="draft-package" ${candidate.ready_for_draft ? '' : 'disabled title="Fill the proof fields before creating a draft package"'}>${candidate.ready_for_draft ? 'Draft Package' : 'Draft Blocked: Needs Proof'}</button>
            <button class="copy-listing">Copy Listing Agent Prompt</button>
            <button class="copy-photo">Copy 6-Image Prompt</button>
          </div>
        </div>
      `;
      article.querySelector('.keep').addEventListener('click', event => setDecision(candidate, 'keep', event.currentTarget));
      article.querySelector('.reject').addEventListener('click', event => setDecision(candidate, 'reject', event.currentTarget));
      article.querySelector('.verify-detail').addEventListener('click', event => verifyDetailProof(candidate, article, event.currentTarget));
      article.querySelector('.save-evidence').addEventListener('click', event => saveEvidence(candidate, article, event.currentTarget));
      article.querySelector('.draft-package').addEventListener('click', event => createDraftPackage(candidate, event.currentTarget));
      article.querySelector('.copy-listing').addEventListener('click', event => copyPrompt(candidate, 'listing', event.currentTarget));
      article.querySelector('.copy-photo').addEventListener('click', event => copyPrompt(candidate, 'photoshoot', event.currentTarget));
      return article;
    }

    function renderCards() {
      const items = visibleCandidates();
      grid.replaceChildren(...items.map(card));
      empty.style.display = items.length ? 'none' : 'block';
    }

    function render() {
      renderMarketOptions();
      renderCategories();
      renderSearchPlan();
      updateStats();
      renderCards();
    }

    async function loadData(shouldRender = true) {
      data = await api('/api/data');
      if (shouldRender) render();
      else render();
    }

    document.querySelectorAll('.chip').forEach(button => {
      button.addEventListener('click', () => {
        document.querySelectorAll('.chip').forEach(item => item.classList.remove('active'));
        button.classList.add('active');
        activeFilter = button.dataset.filter;
        renderCards();
      });
    });
    search.addEventListener('input', () => { searchTerm = search.value; renderCards(); });
    sort.addEventListener('change', renderCards);
    marketFocus.addEventListener('change', () => { activeMarket = marketFocus.value || 'balanced'; renderSearchPlan(); });
    document.querySelector('#refresh').addEventListener('click', async event => {
      const button = event.currentTarget;
      await loadData();
      flash(button, 'Refreshed');
    });
    document.querySelector('#find-products').addEventListener('click', event => findFreshProducts(event.currentTarget));
    document.querySelector('#open-1688').addEventListener('click', event => open1688Helper(event.currentTarget));
    memoryForm.addEventListener('submit', event => {
      event.preventDefault();
      searchMemory(memoryQuery.value);
    });
    document.querySelectorAll('[data-memory-query]').forEach(button => {
      button.addEventListener('click', () => {
        memoryQuery.value = button.dataset.memoryQuery || '';
        searchMemory(memoryQuery.value);
      });
    });

    loadData();
    loadMemoryStatus();
  </script>
</body>
</html>
"""


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "DLMSourcing/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        return

    def send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        try:
            self.wfile.write(encoded)
        except (BrokenPipeError, ConnectionResetError):
            return

    def send_text(self, text: str, content_type: str = "text/html; charset=utf-8") -> None:
        encoded = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        try:
            self.wfile.write(encoded)
        except (BrokenPipeError, ConnectionResetError):
            return

    def send_file(self, path: Path, content_type: str) -> None:
        data = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "public, max-age=604800")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            return

    def read_body_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index.html"}:
            self.send_text(dashboard_html())
            return
        if parsed.path == "/image":
            query = parse_qs(parsed.query)
            image_url = clean(query.get("url", [""])[0])
            try:
                path, content_type = cache_image(image_url)
            except Exception as exc:
                self.send_json({"error": str(exc)}, HTTPStatus.BAD_GATEWAY)
                return
            self.send_file(path, content_type)
            return
        if parsed.path == "/api/data":
            candidates = load_candidates()
            scout = scout_snapshot()
            active_job = scout.get("active_job", {})
            active_keys = {
                clean(key)
                for lane in active_job.get("lanes", [])
                for key in list(lane.get("new_offer_ids", [])) + list(lane.get("detail_queue", []))
                if clean(key)
            }
            query = parse_qs(parsed.query)
            scope = clean(query.get("scope", ["focus"])[0])
            visible_candidates = candidates
            if scope != "all":
                visible_candidates = [
                    candidate
                    for candidate in candidates
                    if clean(candidate.get("key")) in active_keys
                    or candidate.get("opportunity_tier") in {"verified", "promising"}
                    or candidate.get("review_recommended")
                    or clean(candidate.get("decision")) in {"keep", "reject"}
                    or candidate.get("ready_for_draft")
                ]
            self.send_json(
                {
                    "categories": load_categories(),
                    "market_profiles": load_market_profiles(),
                    "search_terms": search_term_catalog(),
                    "sourcing_guide": sourcing_guide(),
                    "candidates": [candidate_ui_payload(candidate) for candidate in visible_candidates],
                    "counts": category_counts(candidates),
                    "latest_run": latest_run_summary(candidates),
                    "scope": "all" if scope == "all" else "focus",
                    "total_candidate_count": len(candidates),
                    "opportunity_counts": {
                        "verified": sum(candidate.get("opportunity_tier") == "verified" for candidate in candidates),
                        "promising": sum(candidate.get("opportunity_tier") == "promising" for candidate in candidates),
                        "liked": sum(candidate.get("decision") == "keep" for candidate in candidates),
                        "filtered": sum(candidate.get("opportunity_tier") == "rejected" for candidate in candidates),
                    },
                    "scout": scout,
                    "decisions_path": str(DECISIONS_PATH.relative_to(REPO_ROOT)),
                }
            )
            return
        if parsed.path == "/api/scout-status":
            self.send_json(scout_snapshot())
            return
        if parsed.path == "/api/collect-status":
            query = parse_qs(parsed.query)
            job_id = clean(query.get("job", [""])[0])
            job = collect_job_snapshot(job_id)
            if not job:
                self.send_json({"error": "job not found"}, HTTPStatus.NOT_FOUND)
                return
            self.send_json(job)
            return
        if parsed.path == "/api/detail-status":
            query = parse_qs(parsed.query)
            job_id = clean(query.get("job", [""])[0])
            job = detail_job_snapshot(job_id)
            if not job:
                self.send_json({"error": "job not found"}, HTTPStatus.NOT_FOUND)
                return
            self.send_json(job)
            return
        if parsed.path == "/api/workflow-status":
            query = parse_qs(parsed.query)
            key = clean(query.get("key", [""])[0])
            candidate = find_candidate(key)
            if not candidate:
                self.send_json({"error": "candidate not found"}, HTTPStatus.NOT_FOUND)
                return
            workflow = workflow_snapshot(candidate)
            job_id = clean(workflow.get("detail_job_id"))
            self.send_json(
                {
                    "ok": True,
                    "key": key,
                    "workflow": workflow,
                    "job": detail_job_snapshot(job_id) if job_id else {},
                    "ready_for_draft": candidate.get("ready_for_draft", False),
                }
            )
            return
        if parsed.path == "/api/browser-status":
            self.send_json(chrome_browser_status())
            return
        if parsed.path == "/api/memory-status":
            self.send_json(memory_status())
            return
        if parsed.path == "/api/prompt":
            query = parse_qs(parsed.query)
            key = clean(query.get("key", [""])[0])
            prompt_type = clean(query.get("type", ["listing"])[0])
            candidate = find_candidate(key)
            if not candidate:
                self.send_json({"error": "candidate not found"}, HTTPStatus.NOT_FOUND)
                return
            prompt = build_photoshoot_prompt(candidate) if prompt_type == "photoshoot" else build_listing_prompt(candidate)
            self.send_json({"prompt": prompt})
            return
        if parsed.path == "/api/draft-package":
            query = parse_qs(parsed.query)
            key = clean(query.get("key", [""])[0])
            candidate = find_candidate(key)
            if not candidate:
                self.send_json({"error": "candidate not found"}, HTTPStatus.NOT_FOUND)
                return
            package_dir = create_draft_package(candidate)
            self.send_json(
                {
                    "package_dir": str(package_dir.relative_to(REPO_ROOT)),
                    "agent_prompt": build_draft_agent_prompt(candidate),
                    "ready_for_draft": candidate.get("ready_for_draft", False),
                    "missing": preparation_missing(candidate),
                }
            )
            return
        if parsed.path == "/api/export":
            query = parse_qs(parsed.query)
            action = clean(query.get("action", ["keep"])[0])
            category_id = clean(query.get("category", [""])[0])
            items = [
                candidate
                for candidate in load_candidates()
                if candidate.get("decision") == action
                and (not category_id or candidate.get("category_id") == category_id)
            ]
            self.send_json({"items": items, "count": len(items)})
            return
        self.send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/search-plan-preview":
            payload = self.read_body_json()
            try:
                with SCOUT_STATE_LOCK:
                    schedule = load_scout_state().get("schedule", {})
                date = plan_date(payload.get("plan_as_of"))
                config = normalize_scout_config(payload, schedule, as_of=date)
                config["reviewed_plan_hash"] = clean(schedule.get("reviewed_plan_hash"))
                self.send_json({"ok": True, "plan": build_sourcing_plan(config, date)})
            except Exception as exc:
                self.send_json({"error": f"Could not build the search plan: {exc}"}, HTTPStatus.BAD_REQUEST)
            return
        if parsed.path == "/api/search-plan-review":
            payload = self.read_body_json()
            try:
                result = confirm_scout_plan_review(payload)
                self.send_json({"ok": True, **result})
            except Exception as exc:
                self.send_json({"error": f"Could not confirm the search-plan review: {exc}"}, HTTPStatus.BAD_REQUEST)
            return
        if parsed.path == "/api/open-1688-browser":
            payload = self.read_body_json()
            category_id = clean(payload.get("category_id")) or "family-matching"
            query_index = int(payload.get("query_index") or 0)
            market_target = normalize_market_target(payload.get("market_target"))
            exact_query = clean(payload.get("exact_query"))[:500]
            try:
                url = open_1688_helper_browser(category_id, query_index, market_target, exact_query)
            except Exception as exc:
                self.send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
                return
            self.send_json(
                {
                    "ok": True,
                    "url": url,
                    "market_target": market_target,
                    "message": "Opened the fixed 1688 search term. Log in or clear CAPTCHA if asked; Opportunity Scout will resume this same saved plan automatically.",
                }
            )
            return
        if parsed.path == "/api/scout":
            payload = self.read_body_json()
            try:
                self.send_json(start_scout_job(payload))
            except ValueError as exc:
                self.send_json({"error": f"Could not start Opportunity Scout: {exc}"}, HTTPStatus.BAD_REQUEST)
            except Exception as exc:
                self.send_json({"error": f"Could not start Opportunity Scout: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if parsed.path == "/api/scout-schedule":
            payload = self.read_body_json()
            try:
                self.send_json({"ok": True, "schedule": save_scout_schedule(payload)})
            except Exception as exc:
                self.send_json({"error": f"Could not save scout settings: {exc}"}, HTTPStatus.BAD_REQUEST)
            return
        if parsed.path == "/api/collect":
            payload = self.read_body_json()
            category_id = clean(payload.get("category_id")) or "family-matching"
            limit = int(payload.get("limit") or 24)
            query_index = int(payload.get("query_index") or 0)
            target_reviewable = int(payload.get("target_reviewable") or 20)
            max_pages_per_query = int(payload.get("max_pages_per_query") or 2)
            market_target = normalize_market_target(payload.get("market_target"))
            job = start_collect_job(category_id, limit, query_index, target_reviewable, max_pages_per_query, market_target)
            self.send_json(job)
            return
        if parsed.path == "/api/workflow/start":
            payload = self.read_body_json()
            key = clean(payload.get("key"))
            if not key:
                self.send_json({"error": "missing key"}, HTTPStatus.BAD_REQUEST)
                return
            try:
                self.send_json(start_listing_prep(key))
            except ValueError as exc:
                self.send_json({"error": str(exc)}, HTTPStatus.NOT_FOUND)
            except Exception as exc:
                self.send_json({"error": f"Could not start listing preparation: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if parsed.path == "/api/detail-enrich":
            payload = self.read_body_json()
            key = clean(payload.get("key"))
            if not key:
                self.send_json({"error": "missing key"}, HTTPStatus.BAD_REQUEST)
                return
            browser = chrome_browser_status()
            if not browser.get("ok"):
                self.send_json(
                    {
                        "error": browser.get("message") or "1688 helper browser is not ready.",
                        "browser": browser,
                    },
                    HTTPStatus.CONFLICT,
                )
                return
            try:
                job = start_detail_job(key)
            except ValueError as exc:
                self.send_json({"error": str(exc)}, HTTPStatus.NOT_FOUND)
                return
            self.send_json(job)
            return
        if parsed.path == "/api/memory-search":
            payload = self.read_body_json()
            query = clean(payload.get("query"))
            result_count = int(payload.get("results") or 5)
            try:
                self.send_json(search_project_memory(query, result_count))
            except ValueError as exc:
                self.send_json({"ok": False, "message": str(exc), "results": []}, HTTPStatus.BAD_REQUEST)
            except subprocess.TimeoutExpired:
                self.send_json(
                    {
                        "ok": False,
                        "message": "Project Memory search took too long. Try a shorter question.",
                        "results": [],
                    },
                    HTTPStatus.GATEWAY_TIMEOUT,
                )
            except Exception as exc:
                self.send_json(
                    {"ok": False, "message": f"Project Memory search failed: {exc}", "results": []},
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            return
        if parsed.path == "/api/evidence":
            payload = self.read_body_json()
            key = clean(payload.get("key"))
            if not key:
                self.send_json({"error": "missing key"}, HTTPStatus.BAD_REQUEST)
                return
            evidence = payload.get("evidence", {})
            if not isinstance(evidence, dict):
                self.send_json({"error": "evidence must be an object"}, HTTPStatus.BAD_REQUEST)
                return
            with DECISION_LOCK:
                decisions = load_decisions()
                items = decisions.setdefault("items", {})
                existing = items.get(key, {})
                if not isinstance(existing, dict):
                    existing = {}
                workflow = existing.get("workflow", {})
                if not isinstance(workflow, dict):
                    workflow = {}
                normalized_evidence = merge_editable_evidence(existing.get("evidence", {}), evidence)
                existing.update(
                    {
                        "action": existing.get("action") or "keep",
                        "product_url": clean(payload.get("product_url")) or existing.get("product_url", ""),
                        "title": clean(payload.get("title")) or existing.get("title", ""),
                        "category_id": clean(payload.get("category_id")) or existing.get("category_id", ""),
                        "run_id": clean(payload.get("run_id")) or existing.get("run_id", ""),
                        "evidence": normalized_evidence,
                        "workflow": workflow,
                        "updated_at": now_iso(),
                    }
                )
                items[key] = existing
                save_decisions(decisions)
            candidate = find_candidate(key)
            if candidate:
                missing = preparation_missing(candidate)
                stage = "prep_ready" if not missing else "needs_input"
                persist_workflow_state(
                    candidate,
                    stage,
                    "Preparation proof is complete." if not missing else f"Saved. {len(missing)} item(s) still need attention.",
                )
                candidate = find_candidate(key) or candidate
                create_draft_package(candidate)
            else:
                missing = []
            self.send_json(
                {
                    "ok": True,
                    "ready_for_draft": bool(candidate and draft_handoff_ready(candidate)),
                    "missing": missing,
                }
            )
            return
        if parsed.path == "/api/draft-package":
            payload = self.read_body_json()
            key = clean(payload.get("key"))
            candidate = find_candidate(key)
            if not candidate:
                self.send_json({"error": "candidate not found"}, HTTPStatus.NOT_FOUND)
                return
            package_dir = create_draft_package(candidate)
            self.send_json(
                {
                    "ok": True,
                    "package_dir": str(package_dir.relative_to(REPO_ROOT)),
                    "agent_prompt": build_draft_agent_prompt(candidate),
                    "ready_for_draft": candidate.get("ready_for_draft", False),
                    "missing": preparation_missing(candidate),
                }
            )
            return
        if parsed.path != "/api/decision":
            self.send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return
        payload = self.read_body_json()
        key = clean(payload.get("key"))
        action = clean(payload.get("action"))
        if not key:
            self.send_json({"error": "missing key"}, HTTPStatus.BAD_REQUEST)
            return
        with DECISION_LOCK:
            decisions = load_decisions()
            items = decisions.setdefault("items", {})
            if action == "clear":
                items.pop(key, None)
            elif action in {"keep", "reject"}:
                existing = items.get(key, {})
                evidence = existing.get("evidence", {}) if isinstance(existing, dict) else {}
                workflow = existing.get("workflow", {}) if isinstance(existing, dict) else {}
                items[key] = {
                    "action": action,
                    "product_url": clean(payload.get("product_url")),
                    "title": clean(payload.get("title")),
                    "category_id": clean(payload.get("category_id")),
                    "run_id": clean(payload.get("run_id")),
                    "verdict": clean(payload.get("verdict")),
                    "score": payload.get("score"),
                    "evidence": evidence,
                    "workflow": workflow if action == "keep" else {},
                    "updated_at": now_iso(),
                }
            else:
                self.send_json({"error": "unsupported action"}, HTTPStatus.BAD_REQUEST)
                return
            save_decisions(decisions)
        self.send_json({"ok": True, "items": len(items)})


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local Dress Like Mommy sourcing dashboard.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--open", action="store_true", help="Open the dashboard in the default browser.")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    if clean(os.environ.get("DLM_SCOUT_SCHEDULER_DISABLED")).lower() not in {"1", "true", "yes"}:
        start_scout_scheduler()
    url = f"http://{args.host}:{args.port}/"
    if args.open:
        webbrowser.open(url)
    print(f"Dress Like Mommy sourcing dashboard: {url}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
