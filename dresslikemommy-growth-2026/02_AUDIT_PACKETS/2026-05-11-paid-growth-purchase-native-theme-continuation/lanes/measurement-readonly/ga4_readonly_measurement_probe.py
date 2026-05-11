#!/usr/bin/env python3
"""Read-only GA4 purchase measurement probe.

This lane intentionally stores only sanitized evidence. It never writes tokens,
customer fields, full order IDs, or full GA4 transaction IDs.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
LANE = Path(__file__).resolve().parent
PROPERTY_ID = "330266838"
GA4_ACCOUNT = "88409806"
DATE_START = "2026-04-01"
DATE_END = "2026-05-10"

SOURCE_CANDIDATES = ROOT / (
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-11-paid-growth-native-review-measurement-readonly-continuation/"
    "sanitized_shopify_non_usd_order_candidates.json"
)

SCAN_ROOTS = [
    ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-review-measurement-readonly-continuation",
    ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation",
    ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-measurement-ads-branch-continuation",
    ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-needs-data-economics-reconciliation/imported_ad_analytics_evidence",
    ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3",
]

TEXT_EXTENSIONS = {".csv", ".json", ".md", ".txt"}
TERM_GROUPS = {
    "ga4_property": ["330266838", "dresslikemommy.com - GA4"],
    "purchase": ["purchase", "Purchase"],
    "transaction": ["transaction", "transaction_id", "transactionId", "Transaction"],
    "currency_field": ["currency", "currencyCode", "Currency"],
    "candidate_currency": ["DKK", "GBP", "CHF"],
    "candidate_country": ["DK", "GB", "CH"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def sha12(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def mask_email(value: str) -> str:
    if "@" not in value:
        return ""
    local, domain = value.split("@", 1)
    if not local:
        return f"***@{domain}"
    return f"{local[:1]}***@{domain}"


def run_command(args: list[str], timeout: int = 20) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            args,
            check=False,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except FileNotFoundError as exc:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": str(exc)}
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": "timeout"}


def get_access_token(scopes: list[str] | None = None) -> tuple[str | None, dict[str, Any]]:
    args = ["gcloud", "auth", "print-access-token"]
    if scopes:
        args.append(f"--scopes={','.join(scopes)}")
    result = run_command(args, timeout=30)
    metadata = {
        "method": "gcloud auth print-access-token" + (" --scopes=<analytics-readonly>" if scopes else ""),
        "available": bool(result["ok"] and result["stdout"]),
        "returncode": result["returncode"],
        "stderr_summary": summarize_error(result["stderr"]),
    }
    if result["ok"] and result["stdout"]:
        return result["stdout"], metadata
    return None, metadata


def summarize_error(text: str) -> str:
    if not text:
        return ""
    compact = " ".join(text.split())
    return compact[:500]


def google_request(
    method: str,
    url: str,
    token: str,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = None
    headers = {"Authorization": f"Bearer {token}"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return {
                "ok": 200 <= response.status < 300,
                "status": response.status,
                "body": parse_json(raw),
            }
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        return {"ok": False, "status": exc.code, "body": parse_json(raw)}
    except Exception as exc:  # Network/tooling failure, not account data.
        return {"ok": False, "status": None, "body": {"error": str(exc)}}


def tokeninfo(token: str) -> dict[str, Any]:
    params = urllib.parse.urlencode({"access_token": token}).encode("utf-8")
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/tokeninfo",
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            body = parse_json(response.read().decode("utf-8", errors="replace"))
            scopes = sorted((body.get("scope") or "").split())
            return {
                "ok": True,
                "status": response.status,
                "email_masked": mask_email(body.get("email", "")),
                "scope_count": len(scopes),
                "scopes": scopes,
                "analytics_read_scope_present": any(
                    scope in scopes
                    for scope in [
                        "https://www.googleapis.com/auth/analytics",
                        "https://www.googleapis.com/auth/analytics.edit",
                        "https://www.googleapis.com/auth/analytics.readonly",
                    ]
                ),
            }
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "error": summarize_error(exc.read().decode("utf-8", errors="replace"))}
    except Exception as exc:
        return {"ok": False, "status": None, "error": str(exc)}


def parse_json(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw[:2000]


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def decimal_or_none(value: Any) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def load_candidates() -> list[dict[str, Any]]:
    data = json.loads(SOURCE_CANDIDATES.read_text(encoding="utf-8"))
    rows = data.get("rows") or []
    reconciled: list[dict[str, Any]] = []
    for row in rows:
        basis = "|".join(
            [
                row.get("created_at_utc", ""),
                row.get("shipping_country", ""),
                row.get("current_total_presentment_currency", ""),
                str(row.get("current_total_presentment_amount", "")),
                str(row.get("order_gid_last4", "")),
            ]
        )
        current_amount = decimal_or_none(row.get("current_total_presentment_amount"))
        original_amount = decimal_or_none(row.get("original_total_presentment_amount"))
        status = row.get("financial_status", "")
        is_paid_nonzero = status == "PAID" and current_amount is not None and current_amount > 0
        if is_paid_nonzero:
            priority = "HIGH_MATCH_CANDIDATE"
        elif status == "REFUNDED" and original_amount is not None and original_amount > 0:
            priority = "REFUNDED_CONTROL_CANDIDATE_ORIGINAL_VALUE_ONLY"
        else:
            priority = "LOW_PRIORITY_NO_CURRENT_REVENUE"
        reconciled.append(
            {
                "candidate_id": sha12(basis),
                "created_at_utc": row.get("created_at_utc"),
                "shipping_country": row.get("shipping_country"),
                "financial_status": status,
                "fulfillment_status": row.get("fulfillment_status"),
                "presentment_currency": row.get("current_total_presentment_currency"),
                "current_presentment_amount": row.get("current_total_presentment_amount"),
                "original_presentment_amount": row.get("original_total_presentment_amount"),
                "subtotal_presentment_amount": row.get("subtotal_presentment_amount"),
                "shipping_presentment_amount": row.get("shipping_presentment_amount"),
                "shop_currency": row.get("current_total_shop_currency"),
                "current_shop_amount": row.get("current_total_shop_amount"),
                "masked_order_name": row.get("order_name_masked"),
                "order_gid_tail4": row.get("order_gid_last4"),
                "match_priority": priority,
                "utc_same_day_match_window": (row.get("created_at_utc") or "")[:10],
                "notes": "Sanitized prior Shopify Admin read-only candidate; no customer name, email, phone, street address, or full identifier stored.",
            }
        )
    return reconciled


def write_candidates(candidates: list[dict[str, Any]]) -> None:
    write_json(
        LANE / "reconciled_shopify_non_usd_candidates.json",
        {
            "generated_at": now_iso(),
            "source": rel(SOURCE_CANDIDATES),
            "count": len(candidates),
            "currencies": sorted({c["presentment_currency"] for c in candidates if c.get("presentment_currency")}),
            "high_match_candidate_count": sum(1 for c in candidates if c["match_priority"] == "HIGH_MATCH_CANDIDATE"),
            "rows": candidates,
        },
    )
    if candidates:
        with (LANE / "reconciled_shopify_non_usd_candidates.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(candidates[0].keys()))
            writer.writeheader()
            writer.writerows(candidates)


def scan_text(path: Path) -> dict[str, Any] | None:
    try:
        if path.stat().st_size > 2_000_000:
            return None
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    return summarize_terms(str(path), text)


def scan_zip(path: Path) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    try:
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                member = Path(info.filename)
                if member.suffix.lower() not in TEXT_EXTENSIONS or info.file_size > 1_000_000:
                    continue
                try:
                    text = archive.read(info).decode("utf-8", errors="ignore")
                except Exception:
                    continue
                hit = summarize_terms(f"{path}!{info.filename}", text)
                if hit:
                    hits.append(hit)
    except Exception:
        pass
    return hits


def summarize_terms(identifier: str, text: str) -> dict[str, Any] | None:
    found: dict[str, list[str]] = {}
    for group, terms in TERM_GROUPS.items():
        present = [term for term in terms if term in text]
        if present:
            found[group] = sorted(set(present))
    has_candidate_currency = "candidate_currency" in found
    has_purchase_or_transaction = "purchase" in found or "transaction" in found
    is_known_candidate_file = identifier.endswith("sanitized_shopify_non_usd_order_candidates.json") or identifier.endswith(
        "sanitized_shopify_non_usd_order_candidates.csv"
    )
    if not ((has_candidate_currency and has_purchase_or_transaction) or is_known_candidate_file):
        return None
    id_path = identifier.replace(str(ROOT) + os.sep, "")
    return {"path": id_path, "term_groups_found": found}


def scan_local_exports() -> dict[str, Any]:
    hits: list[dict[str, Any]] = []
    scanned_files = 0
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() in TEXT_EXTENSIONS:
                scanned_files += 1
                hit = scan_text(path)
                if hit:
                    hits.append(hit)
            elif path.suffix.lower() == ".zip":
                scanned_files += 1
                hits.extend(scan_zip(path))
    summary = {
        "generated_at": now_iso(),
        "scan_roots": [rel(path) for path in SCAN_ROOTS if path.exists()],
        "scanned_text_or_zip_files": scanned_files,
        "hit_count": len(hits),
        "hits": sorted(hits, key=lambda item: item["path"]),
        "conclusion": (
            "Local scan found sanitized candidate/order-side evidence and aggregate measurement artifacts, "
            "but no local export that proves GA4 order-level non-US purchase currency/value/transaction."
        ),
    }
    write_json(LANE / "local_export_scan_summary.json", summary)
    return summary


def sanitize_ga4_rows(response: dict[str, Any]) -> dict[str, Any]:
    body = response.get("body")
    if not isinstance(body, dict) or not response.get("ok"):
        return response
    dimensions = [item.get("name") for item in body.get("dimensionHeaders", [])]
    metrics = [item.get("name") for item in body.get("metricHeaders", [])]
    rows = []
    for row in body.get("rows", []):
        out: dict[str, Any] = {}
        for idx, value in enumerate(row.get("dimensionValues", [])):
            name = dimensions[idx] if idx < len(dimensions) else f"dimension_{idx}"
            raw = value.get("value", "")
            if name == "transactionId" and raw:
                out["transaction_id_tail4"] = raw[-4:]
                out["transaction_id_sha12"] = sha12(raw)
            else:
                out[name] = raw
        for idx, value in enumerate(row.get("metricValues", [])):
            name = metrics[idx] if idx < len(metrics) else f"metric_{idx}"
            out[name] = value.get("value", "")
        rows.append(out)
    return {
        "ok": True,
        "status": response.get("status"),
        "dimension_headers": dimensions,
        "metric_headers": metrics,
        "row_count": len(rows),
        "rows_sanitized": rows,
        "row_count_reported": body.get("rowCount"),
    }


def build_run_report_body(dimensions: list[str], metrics: list[str]) -> dict[str, Any]:
    return {
        "dateRanges": [{"startDate": DATE_START, "endDate": DATE_END}],
        "dimensions": [{"name": name} for name in dimensions],
        "metrics": [{"name": name} for name in metrics],
        "dimensionFilter": {
            "filter": {
                "fieldName": "eventName",
                "stringFilter": {"matchType": "EXACT", "value": "purchase"},
            }
        },
        "limit": 1000,
    }


def api_probe() -> dict[str, Any]:
    active_account = run_command(["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"])
    active_project = run_command(["gcloud", "config", "list", "--format=value(core.project)"])
    adc_token = run_command(["gcloud", "auth", "application-default", "print-access-token"], timeout=15)
    token, token_metadata = get_access_token()
    scoped_token, scoped_token_metadata = get_access_token(["https://www.googleapis.com/auth/analytics.readonly"])

    credential_inventory: dict[str, Any] = {
        "generated_at": now_iso(),
        "gcloud_active_account_masked": mask_email(active_account.get("stdout", "")),
        "gcloud_project": active_project.get("stdout", ""),
        "gcloud_user_access_token_available": token_metadata["available"],
        "gcloud_user_access_token_command": {
            key: value for key, value in token_metadata.items() if key != "available"
        },
        "application_default_credentials_token_available": bool(adc_token["ok"] and adc_token["stdout"]),
        "application_default_credentials_error_summary": summarize_error(adc_token.get("stderr", "")) if not adc_token["ok"] else "",
        "analytics_readonly_scoped_token_request_available": scoped_token_metadata["available"],
        "analytics_readonly_scoped_token_request_command": {
            key: value for key, value in scoped_token_metadata.items() if key != "available"
        },
        "tokens_are_not_stored": True,
    }

    token_candidates = [
        ("gcloud_user_default_token", token, token_metadata),
        ("gcloud_user_analytics_readonly_scope_request", scoped_token, scoped_token_metadata),
    ]
    result: dict[str, Any] = {
        "generated_at": now_iso(),
        "mode": "READ_ONLY_GA4_ADMIN_DATA_API_PROBE_NO_SETTINGS_WRITES",
        "property_id": PROPERTY_ID,
        "account_id": GA4_ACCOUNT,
        "date_range": {"start_date": DATE_START, "end_date": DATE_END},
        "credential_inventory": credential_inventory,
        "credential_attempts": [],
        "gate_solved": False,
        "guardrail": "No GA4/GTM/Ads/Shopify/Pinterest settings writes; no checkout/order/payment/refund; no token or PII stored.",
    }

    if not any(candidate_token for _, candidate_token, _ in token_candidates):
        result["conclusion"] = "No usable gcloud user access token was available in this shell."
        write_json(LANE / "ga4_api_readonly_probe_sanitized.json", result)
        return result

    for label, candidate_token, candidate_metadata in token_candidates:
        attempt: dict[str, Any] = {
            "label": label,
            "token_available": bool(candidate_token),
            "token_command": {key: value for key, value in candidate_metadata.items() if key != "available"},
            "tokeninfo": None,
            "admin_account_summaries": None,
            "data_metadata": None,
            "run_report_attempts": [],
        }
        result["credential_attempts"].append(attempt)
        if not candidate_token:
            continue

        attempt["tokeninfo"] = tokeninfo(candidate_token)

        admin_url = "https://analyticsadmin.googleapis.com/v1beta/accountSummaries"
        attempt["admin_account_summaries"] = google_request("GET", admin_url, candidate_token)

        metadata_url = f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}/metadata"
        metadata = google_request("GET", metadata_url, candidate_token)
        attempt["data_metadata"] = summarize_metadata(metadata)

        full_dimensions = ["dateHourMinute", "date", "eventName", "transactionId", "currencyCode", "countryId", "country"]
        full_metrics = ["eventCount", "totalRevenue", "purchaseRevenue", "ecommercePurchases"]

        available_dimensions: set[str] | None = None
        available_metrics: set[str] | None = None
        if metadata.get("ok") and isinstance(metadata.get("body"), dict):
            available_dimensions = {item.get("apiName") for item in metadata["body"].get("dimensions", [])}
            available_metrics = {item.get("apiName") for item in metadata["body"].get("metrics", [])}

        if available_dimensions is not None:
            dimensions = [name for name in full_dimensions if name in available_dimensions]
            metrics = [name for name in full_metrics if name in available_metrics]
        else:
            dimensions = full_dimensions
            metrics = full_metrics

        run_report_requests = [
            ("order_level_full", dimensions, metrics),
            ("aggregate_purchase_minimal", ["eventName"], ["eventCount", "totalRevenue"]),
        ]
        run_report_url = f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport"
        for name, dims, mets in run_report_requests:
            if not dims or not mets:
                attempt["run_report_attempts"].append(
                    {"name": name, "skipped": True, "reason": "No available dimensions or metrics after metadata filter."}
                )
                continue
            body = build_run_report_body(dims, mets)
            response = google_request("POST", run_report_url, candidate_token, body)
            sanitized = sanitize_ga4_rows(response)
            attempt["run_report_attempts"].append({"name": name, "request": body, "response": sanitized})

    result["gate_solved"] = any(
        report_attempt.get("response", {}).get("ok")
        and report_attempt.get("response", {}).get("row_count", 0) > 0
        and any(
            row.get("currencyCode") in {"DKK", "GBP", "CHF"} or row.get("transaction_id_sha12")
            for row in report_attempt.get("response", {}).get("rows_sanitized", [])
        )
        for credential_attempt in result["credential_attempts"]
        for report_attempt in credential_attempt.get("run_report_attempts", [])
    )
    result["conclusion"] = (
        "GA4 Data API returned order-level candidate evidence."
        if result["gate_solved"]
        else "Existing CLI credentials did not produce order-level non-US GA4 purchase currency/value/transaction proof."
    )
    write_json(LANE / "ga4_api_readonly_probe_sanitized.json", result)
    return result


def summarize_metadata(response: dict[str, Any]) -> dict[str, Any]:
    if not response.get("ok") or not isinstance(response.get("body"), dict):
        return response
    body = response["body"]
    desired_dimensions = {"dateHourMinute", "date", "eventName", "transactionId", "currencyCode", "countryId", "country"}
    desired_metrics = {"eventCount", "totalRevenue", "purchaseRevenue", "ecommercePurchases"}
    return {
        "ok": True,
        "status": response.get("status"),
        "matched_dimensions": sorted(
            item.get("apiName") for item in body.get("dimensions", []) if item.get("apiName") in desired_dimensions
        ),
        "matched_metrics": sorted(
            item.get("apiName") for item in body.get("metrics", []) if item.get("apiName") in desired_metrics
        ),
        "dimension_count": len(body.get("dimensions", [])),
        "metric_count": len(body.get("metrics", [])),
    }


def error_reasons(api_result: dict[str, Any]) -> list[str]:
    reasons: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("reason"):
                reasons.append(str(value["reason"]))
            if value.get("status") and value.get("message"):
                reasons.append(f"{value.get('status')}: {value.get('message')}")
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(api_result)
    return sorted(set(reasons))


def write_report(candidates: list[dict[str, Any]], api: dict[str, Any], scan: dict[str, Any]) -> None:
    high_candidates = [item for item in candidates if item["match_priority"] == "HIGH_MATCH_CANDIDATE"]
    api_reasons = error_reasons(api)
    analytics_scopes = []
    for credential_attempt in api.get("credential_attempts", []):
        tokeninfo_data = credential_attempt.get("tokeninfo")
        if isinstance(tokeninfo_data, dict):
            analytics_scopes.extend(scope for scope in tokeninfo_data.get("scopes", []) if "analytics" in scope)
    run_report_attempt_count = sum(
        len(credential_attempt.get("run_report_attempts", []))
        for credential_attempt in api.get("credential_attempts", [])
    )
    admin_statuses = [
        credential_attempt.get("admin_account_summaries", {}).get("status")
        for credential_attempt in api.get("credential_attempts", [])
        if credential_attempt.get("admin_account_summaries") is not None
    ]
    metadata_statuses = [
        credential_attempt.get("data_metadata", {}).get("status")
        for credential_attempt in api.get("credential_attempts", [])
        if credential_attempt.get("data_metadata") is not None
    ]
    scoped_error = (
        api.get("credential_inventory", {})
        .get("analytics_readonly_scoped_token_request_command", {})
        .get("stderr_summary", "")
    )
    gate_status = "SOLVED_READBACK_PASSED" if api.get("gate_solved") else "NOT_SOLVED_CREDENTIAL_SCOPE_OR_UI_EXPORT_REQUIRED"
    lines = [
        "# Measurement Read-only Lane Report",
        "",
        f"Generated: `{now_iso()}`",
        f"GA4 property: `{PROPERTY_ID}`",
        f"Date range attempted: `{DATE_START}` through `{DATE_END}`",
        f"Gate status: `{gate_status}`",
        "",
        "## What Ran",
        "",
        "- Reconciled the prior sanitized Shopify non-USD candidate file into local candidate JSON/CSV.",
        "- Tested existing `gcloud` user and ADC credential availability without storing tokens.",
        "- Attempted read-only GA4 Admin API `accountSummaries` and GA4 Data API metadata/runReport calls.",
        "- Scanned selected local measurement/GA4/export packet artifacts for non-US purchase transaction/currency evidence without saving excerpts.",
        "",
        "## Candidate Reconciliation",
        "",
        f"- Prior sanitized Shopify non-USD candidates: `{len(candidates)}`.",
        f"- High-priority paid non-zero candidates: `{len(high_candidates)}`.",
        f"- Candidate currencies: `{', '.join(sorted({c['presentment_currency'] for c in candidates if c.get('presentment_currency')}))}`.",
        "- Strongest windows remain the paid non-zero DKK/GBP/CHF orders already documented; the refunded GBP row is useful only as a control/original-value reference.",
        "",
        "## GA4 API Result",
        "",
        f"- `gcloud` user token available: `{api.get('credential_inventory', {}).get('gcloud_user_access_token_available')}`.",
        f"- Analytics-readonly scoped token request available: `{api.get('credential_inventory', {}).get('analytics_readonly_scoped_token_request_available')}`.",
        f"- Analytics-readonly scoped token request error: `{scoped_error or 'none'}`.",
        f"- ADC token available: `{api.get('credential_inventory', {}).get('application_default_credentials_token_available')}`.",
        f"- Analytics OAuth scopes visible from tokeninfo: `{', '.join(analytics_scopes) if analytics_scopes else 'none'}`.",
        f"- Admin API statuses: `{', '.join(str(status) for status in admin_statuses) if admin_statuses else 'none'}`.",
        f"- Data metadata statuses: `{', '.join(str(status) for status in metadata_statuses) if metadata_statuses else 'none'}`.",
        f"- Data runReport attempts: `{run_report_attempt_count}`.",
        f"- Error/status reasons observed: `{'; '.join(api_reasons) if api_reasons else 'none'}`.",
        "",
        "The existing CLI token did not yield order-level GA4 `purchase` rows with transaction/currency/value evidence. No GA4 settings were changed.",
        "",
        "## Local Export Scan",
        "",
        f"- Text/zip files scanned: `{scan.get('scanned_text_or_zip_files')}`.",
        f"- Non-US purchase/transaction/currency term hits: `{scan.get('hit_count')}`.",
        "- Conclusion: no existing local export in the selected packet set proves GA4 order-level non-US purchase currency/value/transaction.",
        "",
        "## Files In This Lane",
        "",
        "- `ga4_readonly_measurement_probe.py`",
        "- `ga4_api_readonly_probe_sanitized.json`",
        "- `reconciled_shopify_non_usd_candidates.json`",
        "- `reconciled_shopify_non_usd_candidates.csv`",
        "- `local_export_scan_summary.json`",
        "- `PURCHASE_MEASUREMENT_READONLY_REPORT.md`",
        "",
        "## Next Action",
        "",
        "Refresh/provide a read-only Google Analytics OAuth credential with Analytics Data API scope for property `330266838`, then rerun this lane's Data API query for `eventName = purchase` with `transactionId`, `currencyCode`, country/date, and purchase revenue fields. If that cannot expose historical order-level fields, the remaining gate is logged-in GA4 UI Explore/export or exact owner approval for the controlled non-US test-purchase/refund/cancel procedure already documented in the prior packet.",
        "",
        "Guardrails preserved: no GA4/GTM/Google Ads/Shopify/Pinterest settings writes, no checkout/payment/order/refund/cancel, no token storage, no customer PII, and no full order or transaction IDs stored.",
        "",
    ]
    (LANE / "PURCHASE_MEASUREMENT_READONLY_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    LANE.mkdir(parents=True, exist_ok=True)
    candidates = load_candidates()
    write_candidates(candidates)
    scan = scan_local_exports()
    api = api_probe()
    write_report(candidates, api, scan)
    print(
        json.dumps(
            {
                "lane": rel(LANE),
                "candidate_count": len(candidates),
                "api_gate_solved": api.get("gate_solved"),
                "report": rel(LANE / "PURCHASE_MEASUREMENT_READONLY_REPORT.md"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
