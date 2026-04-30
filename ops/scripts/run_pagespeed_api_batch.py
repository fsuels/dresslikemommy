#!/usr/bin/env python3
"""Run PageSpeed Insights API captures for a CSV of target URLs.

The script is intentionally dependency-free so it can run from the normal
macOS Python. Store the API key outside the repo, for example:

    ~/.config/dresslikemommy/pagespeed.env

with:

    PAGESPEED_INSIGHTS_API_KEY=...
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


DEFAULT_TARGETS = Path(
    "ops/reports/pagespeed-baseline-2026-04-30T093756-0400/psi-targets-canonical-default.csv"
)
DEFAULT_ENV_FILE = Path.home() / ".config/dresslikemommy/pagespeed.env"
DEFAULT_API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
DEFAULT_CATEGORIES = ("performance", "accessibility", "best-practices", "seo")
DEFAULT_STRATEGIES = ("mobile", "desktop")
QUOTA_ERROR_REASONS = {
    "RATE_LIMIT_EXCEEDED",
    "RESOURCE_EXHAUSTED",
    "quotaExceeded",
    "dailyLimitExceeded",
    "userRateLimitExceeded",
}


def clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_api_key(env_file: Path) -> str:
    load_env_file(env_file)
    return (
        os.environ.get("PAGESPEED_INSIGHTS_API_KEY")
        or os.environ.get("PSI_API_KEY")
        or os.environ.get("PAGESPEED_API_KEY")
        or ""
    ).strip()


def slugify_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip("/") or "home"
    if parsed.query:
        path = f"{path}-{parsed.query}"
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", path).strip("-").lower()
    return slug[:80] or "url"


def raw_filename(url: str, strategy: str) -> str:
    digest = hashlib.sha256(f"{strategy}:{url}".encode("utf-8")).hexdigest()[:12]
    return f"{strategy}-{slugify_url(url)}-{digest}.json.gz"


def read_targets(path: Path, limit: Optional[int] = None) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = [dict(row) for row in reader]
    rows = [row for row in rows if clean(row.get("url"))]
    if limit is not None:
        rows = rows[:limit]
    return rows


def score(category: Dict[str, Any], key: str) -> str:
    value = category.get(key, {}).get("score")
    if value is None:
        return ""
    try:
        return str(round(float(value) * 100))
    except (TypeError, ValueError):
        return ""


def audit_numeric(audits: Dict[str, Any], key: str, digits: int = 3) -> str:
    value = audits.get(key, {}).get("numericValue")
    if value is None:
        return ""
    try:
        return str(round(float(value), digits))
    except (TypeError, ValueError):
        return ""


def field_metric(payload: Dict[str, Any], scope: str, metric: str) -> str:
    bucket = payload.get(scope, {}).get("metrics", {}).get(metric, {})
    value = bucket.get("percentile")
    if value is None:
        return ""
    return str(value)


def extract_error_reason(error_payload: Dict[str, Any]) -> Tuple[str, str]:
    error = error_payload.get("error") if isinstance(error_payload, dict) else None
    if not isinstance(error, dict):
        return "", ""
    status = clean(error.get("status"))
    message = clean(error.get("message"))
    reasons = [status] if status else []
    for detail in error.get("details", []) or []:
        if not isinstance(detail, dict):
            continue
        for violation in detail.get("violations", []) or []:
            subject = clean(violation.get("subject"))
            if subject:
                reasons.append(subject)
    return status or "|".join(reasons), message


def summarize_payload(
    target: Dict[str, str],
    strategy: str,
    payload: Dict[str, Any],
    raw_path: Path,
    http_status: int,
) -> Dict[str, Any]:
    error_reason, error_message = extract_error_reason(payload)
    lighthouse = payload.get("lighthouseResult", {}) if isinstance(payload, dict) else {}
    categories = lighthouse.get("categories", {}) if isinstance(lighthouse, dict) else {}
    audits = lighthouse.get("audits", {}) if isinstance(lighthouse, dict) else {}
    ok = bool(lighthouse) and not error_reason
    return {
        "ok": str(ok).lower(),
        "http_status": http_status,
        "strategy": strategy,
        "type": clean(target.get("type")),
        "locale": clean(target.get("locale")),
        "url": clean(target.get("url")),
        "canonical_path": clean(target.get("canonical_path")),
        "requested_url": clean(lighthouse.get("requestedUrl")),
        "final_url": clean(lighthouse.get("finalUrl")),
        "fetch_time": clean(lighthouse.get("fetchTime")),
        "performance": score(categories, "performance"),
        "accessibility": score(categories, "accessibility"),
        "best_practices": score(categories, "best-practices"),
        "seo": score(categories, "seo"),
        "fcp_ms": audit_numeric(audits, "first-contentful-paint"),
        "lcp_ms": audit_numeric(audits, "largest-contentful-paint"),
        "tbt_ms": audit_numeric(audits, "total-blocking-time"),
        "cls": audit_numeric(audits, "cumulative-layout-shift"),
        "speed_index_ms": audit_numeric(audits, "speed-index"),
        "field_page_category": clean(payload.get("loadingExperience", {}).get("overall_category")),
        "field_origin_category": clean(payload.get("originLoadingExperience", {}).get("overall_category")),
        "field_page_lcp_percentile": field_metric(payload, "loadingExperience", "LARGEST_CONTENTFUL_PAINT_MS"),
        "field_page_cls_percentile": field_metric(payload, "loadingExperience", "CUMULATIVE_LAYOUT_SHIFT_SCORE"),
        "field_origin_lcp_percentile": field_metric(payload, "originLoadingExperience", "LARGEST_CONTENTFUL_PAINT_MS"),
        "field_origin_cls_percentile": field_metric(payload, "originLoadingExperience", "CUMULATIVE_LAYOUT_SHIFT_SCORE"),
        "error_status": error_reason,
        "error_message": error_message,
        "raw_path": str(raw_path),
    }


def write_json_gz(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False)


def read_json_gz(path: Path) -> Dict[str, Any]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def request_pagespeed(
    api_url: str,
    api_key: str,
    url: str,
    strategy: str,
    categories: Sequence[str],
    timeout: int,
) -> Tuple[int, Dict[str, Any]]:
    params: List[Tuple[str, str]] = [
        ("url", url),
        ("strategy", strategy),
        ("key", api_key),
    ]
    params.extend(("category", category) for category in categories)
    request_url = f"{api_url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        request_url,
        headers={"Accept": "application/json", "User-Agent": "dresslikemommy-pagespeed-batch/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return int(response.status), json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"error": {"status": str(exc.code), "message": body[:1000]}}
        return int(exc.code), payload
    except (TimeoutError, socket.timeout, urllib.error.URLError) as exc:
        return 0, {"error": {"status": "REQUEST_FAILED", "message": clean(exc)}}


def write_summary(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "ok",
        "http_status",
        "strategy",
        "type",
        "locale",
        "url",
        "canonical_path",
        "requested_url",
        "final_url",
        "fetch_time",
        "performance",
        "accessibility",
        "best_practices",
        "seo",
        "fcp_ms",
        "lcp_ms",
        "tbt_ms",
        "cls",
        "speed_index_ms",
        "field_page_category",
        "field_origin_category",
        "field_page_lcp_percentile",
        "field_page_cls_percentile",
        "field_origin_lcp_percentile",
        "field_origin_cls_percentile",
        "error_status",
        "error_message",
        "raw_path",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_manifest(
    path: Path,
    *,
    args: argparse.Namespace,
    target_count: int,
    request_count: int,
    completed_count: int,
    ok_count: int,
    blocked: bool,
) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target_csv": str(args.targets),
        "output_dir": str(args.output_dir),
        "strategies": args.strategies,
        "categories": args.categories,
        "target_count": target_count,
        "planned_request_count": request_count,
        "completed_request_count": completed_count,
        "ok_count": ok_count,
        "blocked": blocked,
        "delay_seconds": args.delay,
        "timeout_seconds": args.timeout,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def is_quota_or_auth_error(row: Dict[str, Any]) -> bool:
    status = clean(row.get("error_status"))
    message = clean(row.get("error_message")).lower()
    http_status = clean(row.get("http_status"))
    if http_status in {"400", "401", "403", "429"}:
        return True
    if status in QUOTA_ERROR_REASONS:
        return True
    return any(term in message for term in ("quota", "api key", "permission", "unauthorized"))


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGETS)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--api-url", default=DEFAULT_API_URL)
    parser.add_argument("--strategies", nargs="+", default=list(DEFAULT_STRATEGIES), choices=list(DEFAULT_STRATEGIES))
    parser.add_argument("--categories", nargs="+", default=list(DEFAULT_CATEGORIES))
    parser.add_argument("--limit", type=int, default=None, help="Limit URL targets, useful for probes.")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between API requests.")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--force", action="store_true", help="Re-fetch even if raw JSON already exists.")
    parser.add_argument(
        "--stop-after-blockers",
        type=int,
        default=3,
        help="Stop after this many consecutive auth/quota failures. Use 0 to never stop early.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    api_key = get_api_key(args.env_file)
    if not api_key:
        print(
            f"Missing PAGESPEED_INSIGHTS_API_KEY. Put it in {args.env_file} or export it in the shell.",
            file=sys.stderr,
        )
        return 2

    if args.output_dir is None:
        stamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
        args.output_dir = Path(f"ops/reports/pagespeed-api-{stamp}")

    targets = read_targets(args.targets, args.limit)
    request_count = len(targets) * len(args.strategies)
    raw_dir = args.output_dir / "raw"
    summary_path = args.output_dir / "psi-api-summary.csv"
    manifest_path = args.output_dir / "manifest.json"

    rows: List[Dict[str, Any]] = []
    consecutive_blockers = 0
    blocked = False

    for index, target in enumerate(targets, start=1):
        url = clean(target.get("url"))
        for strategy in args.strategies:
            raw_path = raw_dir / raw_filename(url, strategy)
            if raw_path.exists() and not args.force:
                payload = read_json_gz(raw_path)
                row = summarize_payload(target, strategy, payload, raw_path, 200)
                rows.append(row)
                print(f"[skip] {index}/{len(targets)} {strategy} {url}")
                continue

            print(f"[fetch] {index}/{len(targets)} {strategy} {url}", flush=True)
            http_status, payload = request_pagespeed(
                args.api_url,
                api_key,
                url,
                strategy,
                args.categories,
                args.timeout,
            )
            write_json_gz(raw_path, payload)
            row = summarize_payload(target, strategy, payload, raw_path, http_status)
            rows.append(row)
            write_summary(summary_path, rows)

            if not row.get("ok") == "true" and is_quota_or_auth_error(row):
                consecutive_blockers += 1
                if args.stop_after_blockers and consecutive_blockers >= args.stop_after_blockers:
                    blocked = True
                    print(
                        f"Stopping after {consecutive_blockers} consecutive auth/quota failures. "
                        f"Last status: {row.get('error_status') or row.get('http_status')}",
                        file=sys.stderr,
                    )
                    write_manifest(
                        manifest_path,
                        args=args,
                        target_count=len(targets),
                        request_count=request_count,
                        completed_count=len(rows),
                        ok_count=sum(1 for item in rows if item.get("ok") == "true"),
                        blocked=blocked,
                    )
                    return 3
            else:
                consecutive_blockers = 0

            if args.delay > 0:
                time.sleep(args.delay)

    write_summary(summary_path, rows)
    write_manifest(
        manifest_path,
        args=args,
        target_count=len(targets),
        request_count=request_count,
        completed_count=len(rows),
        ok_count=sum(1 for item in rows if item.get("ok") == "true"),
        blocked=blocked,
    )
    print(f"Wrote {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
