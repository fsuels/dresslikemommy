#!/usr/bin/env python3
"""Export current Merchant Center product diagnostics through Google APIs.

This is a read-only exporter. It tries the current Merchant API first and then
the legacy Content API product status endpoint. If the local Google credential
is missing the required scopes, it writes a blocker summary and a header-only
evidence CSV instead of fabricating Merchant Center status.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, parse, request


DEFAULT_MERCHANT_ID = "124884876"
DEFAULT_INPUT = Path(
    "dresslikemommy-growth-2026/03_LOCAL_ANALYSIS/"
    "2026-04-28-variant-cost-50pct-post-sync_PAID_LABEL_FRESH_SHOPIFY_product_eligibility.csv"
)
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY"
)
NEEDS_DATA = "NEEDS_DATA"

FIELDNAMES = [
    "merchant_center_item_id",
    "shopify_product_id",
    "shopify_variant_id",
    "merchant_center_status",
    "merchant_center_destination",
    "merchant_center_issue_count",
    "merchant_center_issues",
    "image_status",
    "price_status",
    "availability_status",
    "shipping_policy_status",
    "return_policy_status",
    "evidence_source",
    "evidence_notes",
]


class ApiError(RuntimeError):
    def __init__(self, endpoint: str, status: int, payload: dict[str, Any] | str):
        self.endpoint = endpoint
        self.status = status
        self.payload = payload
        super().__init__(f"{endpoint} returned HTTP {status}")


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", clean(value).lower()).strip("_")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def merchant_item_id(row: dict[str, str]) -> str:
    value = clean(row.get("merchant_center_id") or row.get("merchant_center_item_id"))
    if value:
        return value
    product_id = clean(row.get("product_id") or row.get("shopify_product_id"))
    variant_id = clean(row.get("variant_id") or row.get("shopify_variant_id"))
    return f"shopify_US_{product_id}_{variant_id}" if product_id and variant_id else ""


def extract_shopify_item_id(value: object) -> str:
    text = clean(value)
    match = re.search(r"shopify_[A-Z]{2}_\d+_\d+", text)
    return match.group(0) if match else text


def get_access_token() -> tuple[str, str]:
    env_token = os.environ.get("GOOGLE_ACCESS_TOKEN", "").strip()
    if env_token:
        return env_token, "GOOGLE_ACCESS_TOKEN"
    try:
        result = subprocess.run(
            ["gcloud", "auth", "print-access-token"],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Could not run gcloud auth print-access-token: {exc}") from exc
    token = result.stdout.strip()
    if result.returncode != 0 or not token:
        raise RuntimeError(clean(result.stderr) or "gcloud did not return an access token")
    return token, "gcloud auth print-access-token"


def api_get_json(url: str, token: str) -> dict[str, Any]:
    req = request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    try:
        with request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload: dict[str, Any] | str = json.loads(body)
        except json.JSONDecodeError:
            payload = body[:1000]
        raise ApiError(url, exc.code, payload) from exc


def paged_get(url: str, token: str, page_token_name: str, list_key: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    page_token = ""
    while True:
        separator = "&" if "?" in url else "?"
        page_url = f"{url}{separator}{page_token_name}={parse.quote(page_token)}" if page_token else url
        payload = api_get_json(page_url, token)
        rows.extend(payload.get(list_key) or [])
        page_token = clean(payload.get("nextPageToken"))
        if not page_token:
            return rows


def merchant_product_status(product: dict[str, Any]) -> tuple[str, str, list[dict[str, Any]]]:
    status = product.get("productStatus") or {}
    destinations = status.get("destinationStatuses") or []
    issues = status.get("itemLevelIssues") or []
    shopping = [
        item
        for item in destinations
        if normalize(item.get("reportingContext") or item.get("destination")) in {"shopping_ads", "shopping"}
    ]
    approved = any("US" in (item.get("approvedCountries") or []) for item in shopping)
    pending = any("US" in (item.get("pendingCountries") or []) for item in shopping)
    disapproved = any("US" in (item.get("disapprovedCountries") or []) for item in shopping)
    if approved:
        return "Approved", "Shopping ads eligible", issues
    if disapproved:
        return "Disapproved", "Shopping ads not eligible", issues
    if pending:
        return "Under review", "Shopping ads pending", issues
    return NEEDS_DATA, NEEDS_DATA, issues


def content_product_status(product: dict[str, Any]) -> tuple[str, str, list[dict[str, Any]]]:
    destinations = product.get("destinationStatuses") or []
    issues = product.get("itemLevelIssues") or []
    shopping = [
        item
        for item in destinations
        if normalize(item.get("destination") or item.get("reportingContext")) in {"shopping", "shopping_ads"}
    ]
    statuses = {normalize(item.get("status")) for item in shopping if item.get("status")}
    if "approved" in statuses:
        return "Approved", "Shopping ads eligible", issues
    if "disapproved" in statuses:
        return "Disapproved", "Shopping ads not eligible", issues
    if "pending" in statuses or "under_review" in statuses:
        return "Under review", "Shopping ads pending", issues
    return NEEDS_DATA, NEEDS_DATA, issues


def issue_text(issue: dict[str, Any]) -> str:
    return clean(
        issue.get("description")
        or issue.get("detail")
        or issue.get("code")
        or issue.get("attribute")
        or issue.get("servability")
    )


def issue_applies_to_us_shopping(issue: dict[str, Any]) -> bool:
    countries = issue.get("applicableCountries") or issue.get("applicableCountriesWithSubStatus") or []
    if countries and "US" not in countries:
        return False
    context = normalize(issue.get("reportingContext") or issue.get("destination"))
    return not context or context in {"shopping", "shopping_ads"}


def bucket_status(issues: list[dict[str, Any]], bucket: str, approved: bool) -> str:
    bucket_tokens = {
        "image": ("image", "additional_image", "link"),
        "price": ("price",),
        "availability": ("availability", "stock"),
        "shipping": ("shipping",),
        "return": ("return",),
    }[bucket]
    for issue in issues:
        text = normalize(" ".join(clean(issue.get(key)) for key in ("code", "attribute", "description", "detail")))
        if any(token in text for token in bucket_tokens):
            return "FAIL"
    return "PASS" if approved else NEEDS_DATA


def evidence_row(
    current: dict[str, str],
    *,
    status: str,
    destination: str,
    issues: list[dict[str, Any]],
    source: str,
) -> dict[str, str]:
    us_issues = [issue for issue in issues if issue_applies_to_us_shopping(issue)]
    issue_labels = sorted({issue_text(issue) for issue in us_issues if issue_text(issue)})
    approved = normalize(status) == "approved" and not us_issues
    return {
        "merchant_center_item_id": merchant_item_id(current),
        "shopify_product_id": clean(current.get("product_id") or current.get("shopify_product_id")),
        "shopify_variant_id": clean(current.get("variant_id") or current.get("shopify_variant_id")),
        "merchant_center_status": status,
        "merchant_center_destination": destination,
        "merchant_center_issue_count": str(len(us_issues)),
        "merchant_center_issues": "|".join(issue_labels),
        "image_status": bucket_status(us_issues, "image", approved),
        "price_status": bucket_status(us_issues, "price", approved),
        "availability_status": bucket_status(us_issues, "availability", approved),
        "shipping_policy_status": bucket_status(us_issues, "shipping", approved),
        "return_policy_status": bucket_status(us_issues, "return", approved),
        "evidence_source": source,
        "evidence_notes": "Read-only API product diagnostics; shipping/return pass means no item-level issue was returned for that bucket.",
    }


def error_summary(exc: Exception) -> dict[str, Any]:
    if isinstance(exc, ApiError):
        error_payload = exc.payload
        if isinstance(error_payload, dict):
            err = error_payload.get("error") or error_payload
            return {
                "endpoint": exc.endpoint,
                "http_status": exc.status,
                "api_status": err.get("status"),
                "message": clean(err.get("message"))[:500],
            }
        return {"endpoint": exc.endpoint, "http_status": exc.status, "message": clean(error_payload)[:500]}
    return {"message": clean(str(exc))[:500]}


def build_outputs(input_eligibility: Path, output_dir: Path, merchant_id: str) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    current_rows = read_csv(input_eligibility)
    current_by_item = {merchant_item_id(row): row for row in current_rows if merchant_item_id(row)}
    evidence_rows: list[dict[str, str]] = []
    raw_rows: list[dict[str, Any]] = []
    attempted: list[dict[str, Any]] = []
    source = ""
    token_source = "unavailable"

    try:
        token, token_source = get_access_token()
        merchant_url = f"https://merchantapi.googleapis.com/products/v1/accounts/{merchant_id}/products?pageSize=250"
        try:
            raw_rows = paged_get(merchant_url, token, "pageToken", "products")
            source = "Merchant API products.list"
            for product in raw_rows:
                item_id = extract_shopify_item_id(product.get("offerId") or product.get("name"))
                current = current_by_item.get(item_id)
                if not current:
                    continue
                status, destination, issues = merchant_product_status(product)
                evidence_rows.append(
                    evidence_row(current, status=status, destination=destination, issues=issues, source=source)
                )
        except Exception as exc:  # noqa: BLE001
            attempted.append({"api": "Merchant API products.list", **error_summary(exc)})
            content_url = f"https://shoppingcontent.googleapis.com/content/v2.1/{merchant_id}/productstatuses?maxResults=250"
            raw_rows = paged_get(content_url, token, "pageToken", "resources")
            source = "Content API productstatuses.list"
            for product in raw_rows:
                item_id = extract_shopify_item_id(product.get("productId"))
                current = current_by_item.get(item_id)
                if not current:
                    continue
                status, destination, issues = content_product_status(product)
                evidence_rows.append(
                    evidence_row(current, status=status, destination=destination, issues=issues, source=source)
                )
    except Exception as exc:  # noqa: BLE001
        attempted.append({"api": "Content API productstatuses.list", **error_summary(exc)})

    paths = {
        "evidence": output_dir / "merchant_center_api_diagnostics_evidence.csv",
        "raw_jsonl": output_dir / "merchant_center_api_diagnostics_raw.jsonl",
        "summary": output_dir / "merchant_center_api_diagnostics_summary.json",
    }
    write_csv(paths["evidence"], evidence_rows)
    with paths["raw_jsonl"].open("w", encoding="utf-8") as handle:
        for row in raw_rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_GOOGLE_API_DIAGNOSTICS",
        "merchant_id": merchant_id,
        "input_eligibility": str(input_eligibility),
        "token_source": token_source,
        "api_source": source,
        "api_attempt_errors": attempted,
        "current_variant_rows_scanned": len(current_rows),
        "api_raw_rows": len(raw_rows),
        "merchant_evidence_rows": len(evidence_rows),
        "status_counts": dict(Counter(row["merchant_center_status"] for row in evidence_rows).most_common()),
        "issue_rows": sum(int(row["merchant_center_issue_count"]) for row in evidence_rows if row["merchant_center_issue_count"].isdigit()),
        "outputs": {key: str(path) for key, path in paths.items()},
    }
    paths["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-eligibility", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--merchant-id", default=DEFAULT_MERCHANT_ID)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_outputs(args.input_eligibility, args.output_dir, args.merchant_id)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["merchant_evidence_rows"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
