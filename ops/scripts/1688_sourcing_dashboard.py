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
import re
import subprocess
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote_from_bytes, urlparse
import urllib.request


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCING_ROOT = REPO_ROOT / "ops" / "sourcing"
CATEGORIES_PATH = SOURCING_ROOT / "sourcing-categories.json"
DECISIONS_PATH = SOURCING_ROOT / "state" / "decisions.json"
SEARCH_HISTORY_PATH = SOURCING_ROOT / "state" / "search-history.json"
DRAFT_PACKAGES_ROOT = SOURCING_ROOT / "draft-packages"
IMAGE_CACHE_ROOT = SOURCING_ROOT / "image-cache"
PHOTOSHOOT_PROMPT_PATH = REPO_ROOT / "ops" / "prompts" / "dlm-6-image-photoshoot.md"
COLLECTOR_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_cdp_collect.py"
DETAIL_ENRICH_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_detail_enrich.py"
CDP_PORT = 9333
HELPER_CHROME_PROFILE = Path.home() / ".dlm-1688-chrome-profile"
COLLECTION_JOBS: dict[str, dict[str, Any]] = {}
COLLECTION_LOCK = threading.Lock()
DETAIL_JOBS: dict[str, dict[str, Any]] = {}
DETAIL_LOCK = threading.Lock()


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


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_categories() -> list[dict[str, Any]]:
    payload = read_json(CATEGORIES_PATH, {"categories": []})
    return payload.get("categories", [])


def category_lookup() -> dict[str, dict[str, Any]]:
    return {category["id"]: category for category in load_categories()}


def load_search_history() -> dict[str, Any]:
    payload = read_json(SEARCH_HISTORY_PATH, {"version": 1, "updated_at": "", "categories": {}})
    payload.setdefault("version", 1)
    payload.setdefault("updated_at", "")
    payload.setdefault("categories", {})
    return payload


def save_search_history(payload: dict[str, Any]) -> None:
    payload["updated_at"] = now_iso()
    write_json(SEARCH_HISTORY_PATH, payload)


def advance_query_index(category_id: str, used_index: int) -> None:
    queries = configured_queries(category_id)
    if not queries:
        return
    history = load_search_history()
    categories = history.setdefault("categories", {})
    state = categories.setdefault(category_id, {})
    if not isinstance(state, dict):
        state = {}
        categories[category_id] = state
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


def listing_ready(evidence: dict[str, Any]) -> bool:
    required = [
        "size_chart_source",
        "vendor_images_path",
        "generated_images_path",
        "dropship_confirmed",
        "dispatch_confirmed",
        "supplier_confirmed",
    ]
    return all(clean(evidence.get(field)) for field in required)


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


def configured_queries(category_id: str) -> list[str]:
    categories = category_lookup()
    category = categories.get(category_id) or categories.get("family-matching") or {}
    raw_queries = category.get("queries") or ["亲子装 连衣裙 衬衫 一件代发"]
    queries: list[str] = []
    for item in raw_queries:
        if isinstance(item, dict):
            query = clean(item.get("text"))
        else:
            query = clean(item)
        if query:
            queries.append(query)
    return queries or ["亲子装 连衣裙 衬衫 一件代发"]


def next_query_index(category_id: str) -> int:
    queries = configured_queries(category_id)
    history = load_search_history()
    state = history.get("categories", {}).get(category_id, {})
    if not isinstance(state, dict):
        return 0
    return int(state.get("next_query_index") or 0) % len(queries)


def category_search_url(category_id: str, query_index: int = 0) -> str:
    queries = configured_queries(category_id)
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


def open_1688_helper_browser(category_id: str, query_index: int = 0) -> str:
    category = category_id if category_id != "all" else "family-matching"
    if query_index < 0:
        query_index = next_query_index(category)
    url = category_search_url(category, query_index)
    try:
        page = reusable_1688_page(cdp_pages())
    except Exception:
        page = None
    if page and navigate_existing_cdp_tab(page, url):
        close_duplicate_1688_search_tabs(clean(page.get("id")))
        advance_query_index(category, query_index)
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
    advance_query_index(category, query_index)
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


def detail_job_snapshot(job_id: str) -> dict[str, Any]:
    with DETAIL_LOCK:
        return dict(DETAIL_JOBS.get(job_id, {}))


def update_detail_job(job_id: str, **updates: Any) -> None:
    with DETAIL_LOCK:
        job = DETAIL_JOBS.setdefault(job_id, {})
        job.update(updates)


def run_collect_job(job_id: str, category_id: str, limit: int, query_index: int, target_reviewable: int) -> None:
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
    ]
    update_collect_job(job_id, status="running", command=" ".join(command), started_at=now_iso())
    try:
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
        message = f"Found and scored fresh candidates for {category_id}."
        if summary_line:
            message = f"{message} {summary_line}."
        update_collect_job(
            job_id,
            status="complete",
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
        elif "CAPTCHA" in combined or "interception" in combined or "_____tmd_____" in combined:
            message = (
                "1688 blocked the search with login/CAPTCHA/interception. Open the helper browser, "
                "clear the check, then try Find Qualified Leads again."
            )
        else:
            message = (
                "I could not collect products automatically. Open the 1688 helper browser, "
                "log in or clear CAPTCHA if asked, then click Find Qualified Leads again."
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


def start_collect_job(category_id: str, limit: int, query_index: int, target_reviewable: int = 3) -> dict[str, Any]:
    allowed_categories = set(category_lookup()) | {"all"}
    if category_id not in allowed_categories:
        category_id = "family-matching"
    limit = max(1, min(limit, 80))
    target_reviewable = max(0, min(target_reviewable, 12))
    job_id = hashlib.sha1(f"{now_iso()}-{category_id}-{limit}".encode("utf-8")).hexdigest()[:12]
    with COLLECTION_LOCK:
        COLLECTION_JOBS[job_id] = {
            "id": job_id,
            "status": "queued",
            "category_id": category_id,
            "limit": limit,
            "query_index": query_index,
            "target_reviewable": target_reviewable,
            "created_at": now_iso(),
            "message": "Starting 1688 search. I will try the configured keywords and aim for at least 3 reviewable candidates.",
        }
    thread = threading.Thread(
        target=run_collect_job,
        args=(job_id, category_id, limit, query_index, target_reviewable),
        daemon=True,
    )
    thread.start()
    return collect_job_snapshot(job_id)


def run_detail_job(job_id: str, key: str) -> None:
    if not DETAIL_ENRICH_PATH.exists():
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
        completed = subprocess.run(
            command,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
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
        message = "Detail proof saved. Refreshing this card now."
        if result_line:
            message = f"Detail proof saved: {result_line}."
        update_detail_job(
            job_id,
            status="complete",
            completed_at=now_iso(),
            message=message,
            stdout=stdout,
            stderr=stderr,
        )
    else:
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
    ]
    return clean(" ".join(clean(part) for part in parts)).lower()


def load_candidates() -> list[dict[str, Any]]:
    decisions = load_decisions().get("items", {})
    categories = category_lookup()
    candidates: list[dict[str, Any]] = []
    for scored_path in sorted(SOURCING_ROOT.glob("**/scored-candidates.json")):
        run_dir = scored_path.parent
        if run_dir.name == "demo-shortlist":
            continue
        payload = read_json(scored_path, {})
        if not isinstance(payload, dict):
            continue
        run_metadata = read_json(run_dir / "run.json", {})
        category_id = infer_category(run_dir, run_metadata)
        category = categories.get(category_id, {})
        for item in payload.get("candidates", []):
            if not isinstance(item, dict):
                continue
            key = offer_key(item.get("product_url", ""))
            decision = decisions.get(key, {})
            evidence = decision.get("evidence", {}) if isinstance(decision, dict) else {}
            candidate = dict(item)
            candidate["key"] = key
            candidate["run_id"] = run_metadata.get("run_id") or run_dir.name
            candidate["run_dir"] = str(run_dir.relative_to(REPO_ROOT))
            candidate["shortlist_path"] = str((run_dir / "shortlist.html").relative_to(REPO_ROOT))
            candidate["category_id"] = category_id
            candidate["category_label"] = category.get("label", category_id)
            candidate["listing_mode"] = category.get("listing_mode", "Family Matching")
            candidate["decision"] = decision.get("action", "")
            candidate["decision_updated_at"] = decision.get("updated_at", "")
            candidate["evidence"] = evidence if isinstance(evidence, dict) else {}
            candidate["ready_for_draft"] = listing_ready(candidate["evidence"])
            candidate["draft_package_path"] = str(package_dir_for_key(key).relative_to(REPO_ROOT))
            candidate["search_text"] = candidate_search_text(candidate)
            candidates.append(candidate)
    deduped: dict[str, dict[str, Any]] = {}
    stage_rank = {"detail": 2, "search": 1}
    verdict_rank = {"Gold": 3, "Test": 2, "Reject": 1}
    for candidate in candidates:
        key = clean(candidate.get("key")) or clean(candidate.get("product_url")) or clean(candidate.get("title"))
        if not key:
            continue
        existing = deduped.get(key)
        candidate_rank = (
            stage_rank.get(clean(candidate.get("review_stage")), 0),
            verdict_rank.get(candidate.get("verdict"), 0),
            int(candidate.get("score") or 0),
            clean(candidate.get("run_id")),
        )
        existing_rank = (
            stage_rank.get(clean(existing.get("review_stage")), 0) if existing else 0,
            verdict_rank.get(existing.get("verdict"), 0) if existing else 0,
            int(existing.get("score") or 0) if existing else 0,
            clean(existing.get("run_id")) if existing else "",
        )
        if existing is None or candidate_rank >= existing_rank:
            deduped[key] = candidate
    candidates = list(deduped.values())
    for candidate in candidates:
        apply_detail_gate(candidate)
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
        f"score {candidate.get('score')}; verdict {candidate.get('verdict')}. "
        f"Product title: {title}. Confirm size chart, images, dropship support, "
        f"dispatch speed, and supplier evidence before publishing.{image_note}"
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
        "ready_for_draft": listing_ready(evidence),
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
                f"Ready for draft: {listing_ready(evidence)}",
                "",
                "Use `draft-agent-prompt.md` to create a Shopify DRAFT product with images.",
                "Do not publish live until the operator explicitly asks.",
            ]
        ),
    )
    return package_dir


def dashboard_html() -> str:
    return """<!doctype html>
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
        Click <b>Find Qualified Leads</b>. The app should hide weak search cards and only show fresh products worth checking.
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
        <div class="row">
          <button id="find-products" class="primary">Find Qualified Leads</button>
          <button id="open-1688">Open 1688 Login/Search</button>
        </div>
        <div id="search-plan" class="search-plan"></div>
        <div id="collector-status" class="status-box">Choose a category above, then click Find Qualified Leads. The app rotates keyword searches and skips offers already saved locally. If 1688 asks for login or CAPTCHA, use Open 1688 Login/Search once, complete the browser check, then click Find again.</div>
      </div>
    </section>
    <div id="empty" class="empty">No candidates match this view.</div>
    <div id="grid" class="grid"></div>
  </main>
  <script>
    let data = { categories: [], candidates: [], counts: {} };
    let activeCategory = 'all';
    let activeFilter = 'active';
    let searchTerm = '';

    const grid = document.querySelector('#grid');
    const empty = document.querySelector('#empty');
    const categoriesEl = document.querySelector('#categories');
    const search = document.querySelector('#search');
    const sort = document.querySelector('#sort');
    const collectorStatus = document.querySelector('#collector-status');
    const searchPlan = document.querySelector('#search-plan');

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

    function activeCategoryConfig() {
      return data.categories.find(category => category.id === activeCategory) || null;
    }

    function renderSearchPlan() {
      const category = activeCategoryConfig();
      const queries = category?.queries || data.categories.flatMap(item => item.queries || []).slice(0, 8);
      const queryItems = queries.slice(0, 8).map(query => `<li>${escapeHtml(query)}</li>`).join('');
      const label = category ? category.label : 'All Categories';
      searchPlan.innerHTML = `
        <div><strong>What the button searches:</strong> ${escapeHtml(label)} keyword searches on normal 1688 search pages. It now rotates the starting query and skips offers already saved locally.</div>
        <ul class="query-list">${queryItems}</ul>
        <div><strong>What becomes Buyer Shortlist:</strong> correct category, visible 2025/2026 or Chinese new-style signal, newer 1688 offer ID, usable image, low MOQ, and a useful signal such as repeat rate, sales, or dropship wording.</div>
        <div><strong>What gets hidden:</strong> previous reject, old 1688 offer ID, old year signal such as 2020-2024, no visible freshness signal, wrong category, no product URL/image, high MOQ, no-dropship/no-size-chart evidence, or brand/IP risk.</div>
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
        setCollectorStatus(`${job.message || 'Searching 1688...'} Trying rotated keyword searches and skipping already-seen offers; this can take 1-3 minutes.`);
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
      setCollectorStatus('The search is still running. Refresh the view in a minute.', 'bad');
    }

    async function findFreshProducts(button) {
      const category = activeCategory === 'all' ? 'all' : activeCategory;
      button.disabled = true;
      const old = button.textContent;
      button.textContent = 'Searching...';
      setCollectorStatus(`Checking 1688 browser status before searching.`);
      try {
        const browser = await api('/api/browser-status');
        if (!browser.ok) {
          setCollectorStatus(`${browser.message} Click Open 1688 Login/Search, complete the browser check, then try Find Qualified Leads again.`, 'bad');
          flash(button, 'Blocked');
          return;
        }
        setCollectorStatus(`Searching 1688 for ${category === 'all' ? 'all categories' : category}. I am rotating keywords, skipping already-seen offers, and hiding weak matches before they reach your shortlist.`);
        const job = await api('/api/collect', {
          method: 'POST',
          body: JSON.stringify({ category_id: category, limit: 48, query_index: -1, target_reviewable: 3 }),
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
          body: JSON.stringify({ category_id: category, query_index: -1 }),
        });
        setCollectorStatus(`Reused the 1688 helper tab. Login or clear CAPTCHA once if asked, then click Find Qualified Leads. Search page: ${payload.url}`, 'good');
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
    document.querySelector('#refresh').addEventListener('click', async event => {
      const button = event.currentTarget;
      await loadData();
      flash(button, 'Refreshed');
    });
    document.querySelector('#find-products').addEventListener('click', event => findFreshProducts(event.currentTarget));
    document.querySelector('#open-1688').addEventListener('click', event => open1688Helper(event.currentTarget));

    loadData();
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
        self.wfile.write(encoded)

    def send_text(self, text: str, content_type: str = "text/html; charset=utf-8") -> None:
        encoded = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_file(self, path: Path, content_type: str) -> None:
        data = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "public, max-age=604800")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

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
            self.send_json(
                {
                    "categories": load_categories(),
                    "candidates": candidates,
                    "counts": category_counts(candidates),
                    "decisions_path": str(DECISIONS_PATH.relative_to(REPO_ROOT)),
                }
            )
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
        if parsed.path == "/api/browser-status":
            self.send_json(chrome_browser_status())
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
            if not candidate.get("ready_for_draft"):
                self.send_json(
                    {
                        "error": "Draft Package is blocked until size chart, images, dropship, dispatch, and supplier proof are filled in.",
                        "ready_for_draft": False,
                    },
                    HTTPStatus.BAD_REQUEST,
                )
                return
            package_dir = create_draft_package(candidate)
            self.send_json(
                {
                    "package_dir": str(package_dir.relative_to(REPO_ROOT)),
                    "agent_prompt": build_draft_agent_prompt(candidate),
                    "ready_for_draft": candidate.get("ready_for_draft", False),
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
        if parsed.path == "/api/open-1688-browser":
            payload = self.read_body_json()
            category_id = clean(payload.get("category_id")) or "family-matching"
            query_index = int(payload.get("query_index") or 0)
            try:
                url = open_1688_helper_browser(category_id, query_index)
            except Exception as exc:
                self.send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
                return
            self.send_json(
                {
                    "ok": True,
                    "url": url,
                    "message": "Opened 1688 helper browser. Log in or clear CAPTCHA if asked, then run Find Qualified Leads.",
                }
            )
            return
        if parsed.path == "/api/collect":
            payload = self.read_body_json()
            category_id = clean(payload.get("category_id")) or "family-matching"
            limit = int(payload.get("limit") or 24)
            query_index = int(payload.get("query_index") or 0)
            target_reviewable = int(payload.get("target_reviewable") or 3)
            job = start_collect_job(category_id, limit, query_index, target_reviewable)
            self.send_json(job)
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
            decisions = load_decisions()
            items = decisions.setdefault("items", {})
            existing = items.get(key, {})
            if not isinstance(existing, dict):
                existing = {}
            existing.update(
                {
                    "action": existing.get("action") or "keep",
                    "product_url": clean(payload.get("product_url")) or existing.get("product_url", ""),
                    "title": clean(payload.get("title")) or existing.get("title", ""),
                    "category_id": clean(payload.get("category_id")) or existing.get("category_id", ""),
                    "run_id": clean(payload.get("run_id")) or existing.get("run_id", ""),
                    "evidence": {name: clean(value) for name, value in evidence.items()},
                    "updated_at": now_iso(),
                }
            )
            items[key] = existing
            save_decisions(decisions)
            self.send_json({"ok": True, "ready_for_draft": listing_ready(existing["evidence"])})
            return
        if parsed.path == "/api/draft-package":
            payload = self.read_body_json()
            key = clean(payload.get("key"))
            candidate = find_candidate(key)
            if not candidate:
                self.send_json({"error": "candidate not found"}, HTTPStatus.NOT_FOUND)
                return
            if not candidate.get("ready_for_draft"):
                self.send_json(
                    {
                        "error": "Draft Package is blocked until size chart, images, dropship, dispatch, and supplier proof are filled in.",
                        "ready_for_draft": False,
                    },
                    HTTPStatus.BAD_REQUEST,
                )
                return
            package_dir = create_draft_package(candidate)
            self.send_json(
                {
                    "ok": True,
                    "package_dir": str(package_dir.relative_to(REPO_ROOT)),
                    "agent_prompt": build_draft_agent_prompt(candidate),
                    "ready_for_draft": candidate.get("ready_for_draft", False),
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
        decisions = load_decisions()
        items = decisions.setdefault("items", {})
        if action == "clear":
            items.pop(key, None)
        elif action in {"keep", "reject"}:
            existing = items.get(key, {})
            evidence = existing.get("evidence", {}) if isinstance(existing, dict) else {}
            items[key] = {
                "action": action,
                "product_url": clean(payload.get("product_url")),
                "title": clean(payload.get("title")),
                "category_id": clean(payload.get("category_id")),
                "run_id": clean(payload.get("run_id")),
                "verdict": clean(payload.get("verdict")),
                "score": payload.get("score"),
                "evidence": evidence,
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
